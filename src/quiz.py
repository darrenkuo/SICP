import web

from web import form
from globals import *
from html import *
from utils import *
from renderobjects import *

from re import match

def makeQuiz(html_code):
    html = '<div id="quiz">\n'
    html += '<ol>\n'
    lines = html_code.split('\n')

    print lines
    i = 0
    q = 0
    question_types = {}
    while i < len(lines): 
        m = match(r'^###Q[\s]([\s\S]+)$', lines[i])
        if not m:
            print lines[i]
            print "ERROR! parsing quiz content"
            return html + '</ol>\n</div>\n'

        question = m.groups()[0]
        html += '<li>%s\n' % (question)

        i += 1
        r = []
        b = None
        n = 0
        while True and i < len(lines):
            print "processing i: ", i
            print "processing line: ", lines[i]
            m = match(r'^@R[\s]([\s\S]+)$', lines[i])
            if m:
                choice = m.groups()[0]
                r.append('<label for="number%d"><input type="radio" value="%s" name="q%d" id="number0">%s</label>\n' % (n, choice, q, choice))
                i += 1
                n += 1
                continue

            m = match(r'^@B', lines[i])
            if m:
                b = '<textarea id="q%d" rows="10" cols="100" style="resize:none; overflow: auto"></textarea>\n' % (q)
                i += 1
                continue

            print "break!"
            break

        i += 1
        html += '<form name="q%d-form" method="get" action="">\n' % (q)

        if len(r) > 0:
            for radio in r:
                html += radio
            question_types[q] = 'r'
        elif b:
            html += b
            question_types[q] = 'b'

        q += 1

        html += '</form>\n'
        html += '</li>\n'

    html += '<button type="button" onclick="submit()">Submit!</button>'
    
    return html + '</ol>\n</div>\n', question_types

def getQuiz(user, page=''):
    
    path = '.'
    if page:
        path = convertToRealPath(page)

    data = readLessonData(path)
    if not checkReadable(data, user):
        return css(), lesson_layout(content=unreadable_content())

    storeVisit(data['index'], user)

    f = open(join(course_material, path, 'content.html'), 'r')
    html_code = f.read().strip()
    f.close()

    html, question_type = makeQuiz(html_code)
    print html

    return (sidebar_css(), quiz_js(question_type=question_type, page=page), 
            lesson_layout(content=lesson_content(title=data['title'], 
                                                 content=html, path=page)))
    
class quiz:
    def GET(self):
        data = web.input()
        session = web.config.get('_session')
        if 'page' in data:
            print 'quiz data:', data
            return render.quiz(getQuiz(session.user, data['page']))
        return render.quiz(getQuiz(session.user, ''))

    def POST(self):
        return self.GET()

