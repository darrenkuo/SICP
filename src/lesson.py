import web

from web import form
from format_scheme import format_code
from globals import *
from renderobjects import *
from html import *
from utils import *

from re import match

def getLesson(user, page=''):

    path = '.'
    if page:
        path = convertToRealPath(page)

    data = readLessonData(path)
    if not checkReadable(data, user):
        return css(), lesson_layout(content=unreadable_content())

    f = open(join(course_material, path, 'content.html'), 'r')
    html_code = f.read().strip().split('\n')
    f.close()
    
    storeVisit(data['index'], user)
    
    html = ''
    for line in html_code:
        obj = match('^###([\s\S]+)###', line)
        if obj:
            html += '%s\n' % (format_code(open(
                        join(course_material, path, obj.groups()[0]), 'r')))
        else:
            html += '%s\n' % (line)

    return sidebar_css(), lesson_layout(content=lesson_content(title=data['title'], 
                                                         content=html, path=page))
    
class lesson:
    def GET(self):
        data = web.input()        
        session = web.config.get('_session')
        if 'page' in data:
            return render.lesson(getLesson(session.user, data['page']))
        return render.lesson(getLesson(session.user, ''))
    
    def POST(self):
        return self.GET()


