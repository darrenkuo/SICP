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

def checkAccessed(index, user, oldconn=None, oldcursor=None):
    print 'checking if user %s accessed page %s' % (user, index)
    if not oldconn or not oldcursor:
        (conn, cursor) = getDbCursor(course_db)
    else:
        conn = oldconn
        cursor = oldcursor

    cursor.execute('SELECT * from visits v where v.login = "%s" and v.chapter_id = "%s"' % (user, str(index)))

    rows = cursor.fetchall()

    if not oldconn:
        cursor.close()
    
    return len(rows) == 1

def checkSF(SF, user):
    (conn, cursor) = getDbCursor(course_db)
    cursor.execute('SELECT * from SPECIAL_FLAG where login = "%s" and SPECIAL_FLAG = "%s";' % (user, SF))
    rows = cursor.fetchall()
    return len(rows) >= 1

def storeVisit(index, user):
    (conn, cursor) = getDbCursor(course_db)
    if not checkAccessed(index, user, conn, cursor):
        print "storing visit: %s just accessed page %s" % (user, index)
        cursor.execute('INSERT into visits values("%s", "%s");' % (user, str(index)))
        conn.commit()
    else:
        print "%s have already accessed page %s before" % (user, index)

    cursor.execute('INSERT into visits_times values("%s", "%s", "%s");' % (user, str(index), str(int(time() * 1000))))
    conn.commit()
    cursor.close()    

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
    cursor.execute('CREATE TABLE SPECIAL_FLAG(login TEXT, SPECIAL_FLAG TEXT);')
    cursor.execute('CREATE TABLE quiz_times(login TEXT, chapter_id INTEGER, timestamp INTEGER);')
    cursor.execute('CREATE TABLE visits_times(login TEXT, chapter_id INTEGER, timestamp INTEGER);')
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
