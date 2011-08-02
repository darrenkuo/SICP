import web

from src.globals import *
from src.display import *
from src.lesson import *
from src.quiz import *
from src.login import *
from src.summary import *
from src.course_admin import *
from src.utils import *

from os.path import exists

web.config.debug = True

urls = ('/', 'main', 
        '/logout', 'logout', 
        '/register_admin', 'register_admin',
        '/register', 'register', 
        '/admin_login', 'admin_login', 
        '/admin', 'admin',
        '/display', 'display',
        '/summary', 'summary', 
        '/lesson', 'lesson',
        '/quiz', 'quiz',
        '/course_control', 'course_control',
        '/edit_page', 'edit_page',
        '/new_page', 'new_page',
        '/up', 'up', 
        '/down', 'down')

"""
, 'main',
        '/logout/', 
        '/register/',
        '/summary/', '/admin/', '/admin_login/')
"""
class main:
    def GET(self):
        my_signin = signin_form()
        session = web.config.get('_session')
        if (isStudent(session.user) or isAdmin(session.user)):
            raise web.seeother('/summary')
        return render.main(session.user, my_signin)

    def POST(self): 
        my_signin = signin_form() 

        if not my_signin.validates():
            return render.main(session.user, my_signin)
        else:
            session.user = my_signin['username'].value
            raise web.seeother('/summary')

class logout:
    def GET(self):
        web.debug('[USER] %s logged out' % (session.user))
        session.kill()
        raise web.seeother('/')

class admin_login:
    def GET(self):
        my_signin = admin_signin_form()
        return render.admin_login(session.user, my_signin)

    def POST(self): 
        my_signin = admin_signin_form() 

        if not my_signin.validates():
            return render.admin_login(session.user, my_signin)
        else:
            session.user = my_signin['username'].value
            raise web.seeother('/admin')

class admin:
    def GET(self):
        if not isAdmin(session.user):
            raise web.seeother('/admin_login')
        return render.admin(getAdminPage())
    
    def POST(self):
        return self.GET()

class course_control:
    def GET(self):
        if not isAdmin(session.user):
            raise web.seeother('/admin_login')
        return render.course_control(getCourseTree())

    def POST(self):
        return self.GET()

class edit_page:
    def GET(self):
        if not isAdmin(session.user):
            raise web.seeother('/admin_login')

        data = web.input()
        edit_page = edit_page_form(data['page'])
        return render.edit_page(edit_page)

    def POST(self):
        return self.GET()

class new_page:
    def GET(self):
        if not isAdmin(session.user):
            raise web.seeother('/admin')

        data = web.input()
        if 'page' in data and 'title' in data and 'code' in data:
            make_new_page(data)
            raise web.seeother('/course_control')

        new_page = new_page_form()
        return render.new_page(new_page, data['page'])

    def POST(self):
        return self.GET()
        
app = web.application(urls, globals(), True)

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'),
                                  initializer={'user': '!@#$%^&*anonymous*&^%$#@!'})
    web.config._session = session
else:
    session = web.config._session

if __name__ == "__main__":
    if not exists('dbs'):
        print "Creating database folder"
        mkdir('dbs')
        setup_dbs()

    app.run()
