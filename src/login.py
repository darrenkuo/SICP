import web

from hashlib import sha1
from os.path import join
from random import randint

#from student_progress import create_user_permission_file
from utils import getDbCursor
from web import form

from globals import *

# Helper functions

# A simple user object that doesn't store passwords in plain text
# see http://en.wikipedia.org/wiki/Salt_(cryptography)
class PasswordHash(object):
    def getSaltedpw(self, password_):
        salt = "".join(chr(randint(48,127)) for x in xrange(64))
        saltedpw = sha1(password_ + salt).hexdigest()
        return (salt, saltedpw)

    def check_password(self, password_, salt, saltedpw):
        """checks if the password is correct"""
        return saltedpw == sha1(password_ + salt).hexdigest()

passwordHasher = PasswordHash()
def debug(e):
    web.debug(e)

def getPwDbCursor(db):
    return getDbCursor(db)
    
def checkLogin(username, db):
    (pw_db_conn, pw_db_cursor) = getPwDbCursor(db)
    web.debug("checking login!")
    try:
        pw_db_cursor.execute("""select * from USERS u where u.login = '%s'""" % (
                username))
    except Exception as e:
        web.debug(str(e))

    rows = pw_db_cursor.fetchall()
    pw_db_conn.close()
    return len(rows) == 1

def checkPassword(login, password, db):
    global passwordHasher
    (pw_db_conn, pw_db_cursor) = getPwDbCursor(db)
    try:
        pw_db_cursor.execute("""select * from USERS u where u.login = '%s'""" % (login))
    except Exception as e:
        web.debug(str(e))
    
    rows = pw_db_cursor.fetchall()
    pw_db_conn.close()

    web.debug("User %s is trying to login." % (login))

    if passwordHasher.check_password(password, rows[0][1], rows[0][2]):
        web.debug("User %s logged in." % (login))
        return True
    else:
        return False

def register_user(login, password, db):
    global passwordHasher
    (pw_db_conn, pw_db_cursor) = getPwDbCursor(db)
    (salt, saltpw) = passwordHasher.getSaltedpw(password)
    try:
        command = """insert into USERS values('%s','%s','%s')""" % (login, salt, saltpw)
        web.debug("executing command: " + command)
        pw_db_cursor.execute(command)
    except Exception as e:
        web.debug(str(e))

    #create_user_permission_file(login)

    try:
        import mail
        mail.send_mail(subject = "[CS61AS] New User Registered - %s" % (login), 
                       to = "darren.kuo.cs@gmail.com", 
                       sender = "cs61as@inst.eecs.berkeley.edu", 
                       body = "\"\"")
    except Exception as e:
        web.debug(str(e))
        
    pw_db_conn.commit()
    pw_db_conn.close()
# TODO: admin and student ids might conflict and overwrite visits
# forms
signin_form = form.Form(form.Textbox('username',
                                     form.Validator('Unknown username.',
                                                    lambda x: checkLogin(x, student_db)),
                                     description='Username:'),
                        form.Password('password',
                                      description='Password:'),
                        
                        validators = [form.Validator("Username and password didn't match.", lambda x: checkPassword(x.username, x.password, student_db))])

admin_signin_form = form.Form(form.Textbox('username',
                                     form.Validator('Unknown username.',
                                                    lambda x: checkLogin(x, admin_db)),
                                     description='Username:'),
                        form.Password('password',
                                      description='Password:'),
                        
                        validators = [form.Validator("Username and password didn't match.", lambda x: checkPassword(x.username, x.password, admin_db))])


signup_form = form.Form(form.Textbox('username', description='Username:'),
                        form.Password('password', description='Password:'),
                        form.Password('password_again',
                                      description='Repeat your password:'),
                        validators = [form.Validator("Passwords didn't match.",
                             lambda i: i.password == i.password_again),
                                      form.Validator('Username already exists.',
                                                     lambda i: not checkLogin(i.username, student_db)),
                                      form.Validator('Username needs to be at least 5 characters', lambda i: len(i.username) > 5),
                                      form.Validator('password needs to be at least 5 characters', lambda i: len(i.password) > 5)])

admin_signup_form = form.Form(form.Textbox('username', description='Username:'),
                        form.Password('password', description='Password:'),
                        form.Password('password_again',
                                      description='Repeat your password:'),
                        validators = [form.Validator("Passwords didn't match.",
                             lambda i: i.password == i.password_again),
                                      form.Validator('Username already exists.',
                                                     lambda i: not checkLogin(i.username, admin_db)),

                                      form.Validator('Username needs to be at least 5 characters', lambda i: len(i.username) > 5),
                                      form.Validator('password needs to be at least 5 characters', lambda i: len(i.password) > 5)])


class register:
    def GET(self):
        my_signup = signup_form()
        return render.signup(my_signup)

    def POST(self):
        my_signup = signup_form()
        if not my_signup.validates(): 
            return render.signup(my_signup)
        else:
            username = my_signup['username'].value
            password = my_signup['password'].value
            debug('Someone is trying to register with username: %s and password: %s' % (username, password))
            register_user(username, password, student_db)
            raise web.seeother('/')

class register_admin:
    def GET(self):
        my_signup = admin_signup_form()
        return render.register_admin(my_signup)

    def POST(self):
        my_signup = admin_signup_form()
        if not my_signup.validates(): 
            return render.register_admin(my_signup)
        else:
            username = my_signup['username'].value
            password = my_signup['password'].value
            debug('Someone is trying to register with username: %s and password: %s' % (username, password))
            #register_user(username, password, student_db)
            admin_register(username, password, admin_db)
            raise web.seeother('/')

def admin_register(login, password, db):
    f = open("%s.request" % login, 'w')
    global passwordHasher
    (pw_db_conn, pw_db_cursor) = getPwDbCursor(db)
    (salt, saltpw) = passwordHasher.getSaltedpw(password)
    f.write("%s\n" % (login))
    f.write("%s\n" % (salt))
    f.write("%s\n" % (saltpw))
    f.close()

