from os.path import join
from sqlite3 import connect
from time import time

from globals import *

def getDbCursor(db):
    db_conn = connect(join(dbs_path, db))
    db_cursor = db_conn.cursor()
    return (db_conn, db_cursor)

def newLessonData(index, title, code, page_type):
    return {'index' : index, 'chapters' : [],
            'title' : title, 'readable' : code,
            'type' : page_type}

def readLessonData(path):
    f = open(join(course_material, path, 'lesson.data'), 'r')
    data = eval(f.read())
    f.close()

    return data

def writeLessonData(path, data):
    f = open(join(course_material, path, 'lesson.data'), 'w')
    f.write(str(data))
    f.close()

def checkReadable(lesson_data, user):
    print 'checking readable:', lesson_data['readable']
    func = eval('lambda time, user: %s' % (lesson_data['readable']))
    return func(time() * 1000, user)

def checkAccessed(index, user):
    print 'checking if user %s accessed page %s' % (user, index)
    (conn, cursor) = getDbCursor(course_db)
    cursor.execute('SELECT * from visits v where v.login = "%s" and v.chapter_id = "%s"' % (user, str(index)))

    rows = cursor.fetchall()
    cursor.close()
    
    return len(rows) == 1

def storeVisit(index, user):
    if not checkAccessed(index, user):
        print "storing visit: %s just accessed page %s" % (user, index)
        (conn, cursor) = getDbCursor(course_db)
        cursor.execute('INSERT into visits values("%s", "%s");' % (user, str(index)))
        conn.commit()
        cursor.close()
    else:
        print "%s have already accessed page %s before" % (user, index)

def convertToRealPath(path):
    return apply(join, path.split('-'))

def isAdmin(user):
    (conn, cursor) = getDbCursor(admin_db)
    cursor.execute('SELECT * from users a WHERE a.login = "%s";' % (user))
    rows = cursor.fetchall()
    return len(rows) == 1

def isStudent(user):
    (conn, cursor) = getDbCursor(student_db)
    cursor.execute('SELECT * from users u WHERE u.login = "%s";' % (user))
    rows = cursor.fetchall()
    return len(rows) == 1


def setup_dbs():
    (conn, cursor) = getDbCursor(course_db)
    cursor.execute('CREATE TABLE chapter(id INTEGER PRIMARY KEY, path TEXT);')
    cursor.execute('CREATE TABLE visits(login TEXT, chapter_id INTEGER);')
    conn.commit()
    cursor.close()

    (conn, cursor) = getDbCursor(admin_db)
    cursor.execute('CREATE TABLE users (login TEXT primary key, salt TEXT, saltpw TEXT);')
    conn.commit()
    cursor.close()

    (conn, cursor) = getDbCursor(student_db)
    cursor.execute('CREATE TABLE users (login TEXT primary key, salt TEXT, saltpw TEXT);')
    conn.commit()
    cursor.close()
