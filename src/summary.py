import web

from web import form
from globals import *
from renderobjects import *
from html import *
from utils import *

def getSummary(user, page=''):
    path = ''
    if page:
        for i in page.split('-'):
            path = join(path, i)

    css_obj = css()
    css_obj.add('sidebar', {'overflow': 'auto',
                            'height': '100%',
                            'width': '15%',
                            'float': 'left',
                            'padding-left': '10px',
                            'padding-top': '50px',})
    css_obj.add('content', {'float': 'left',
                            'padding-left': '50px',})

    lesson_data = readLessonData(path)

    return css_obj, lesson_layout(content=lesson_content(
            title=lesson_data['title'],
            content=getTableOfContent(lesson_data, 
                                      '.', user, 0, ''),
            path=None))

n = 2
def getTableOfContent(lesson_data, path, user, level, page_path):
    global n
    #if level >=n:
    #    return 
    components = []
    print "path:", path
    print "readable:", checkReadable(lesson_data, user)
    if checkReadable(lesson_data, user):
        components.append(a(lesson_data['title'], 
                            '/display?page=%s' % (page_path)))
    else:
        components.append(p(lesson_data['title']))

    for c in lesson_data['chapters']:
        data = readLessonData(join(path, c))
        
        page = '%s-%s' % (page_path, c)
        if page_path == '':
            page = str(c[0])

        o = getTableOfContent(data, join(path, c), user,
                              level + 1, page)

        if o:
            components.append(o)

    if level == 0:
        return ol('', components)
    else:
        return ul('', components)

class summary:
    def GET(self):
        data = web.input()
        session = web.config.get('_session')
        print "user:", session.user
        if 'page' in data:
            return render.summary(getSummary(session.user, data['page']))
        else:
            return render.summary(getSummary(session.user, ''))
    
    def POST(self):
        return self.GET()

# window.open(<address>, <name>, <features>)
# features = 'left=20, top=20, width=500, height=500'
