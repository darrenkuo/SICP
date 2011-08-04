import web

from web import form
from globals import *
from renderobjects import *
from html import *
from utils import *

from os import mkdir
from os import walk
from os.path import join
from random import randint
from sys import maxint

def getCourseTree(path='.'):
    components = []
    data = readLessonData(path)

    components.append(chapter_entry(data['index'], data['title'], path))
    for child in data['chapters']:
        components.append(getCourseTree(join(path, child)))

    return ol('', components)

def getSFPairList():
    pair_list = [('SF_PROGRAMMED', 'Has programmed'),
                 ('SF_SCHEME', 'Know Scheme'),
                 ('SF_RECURSION', 'Know Recursion'),]
    return pair_list
    

def getCoursePairList(path='.'):
    components = []
    data = readLessonData(path)

    components.append((data['index'], data['title']))
    for child in data['chapters']:
        components.extend(getCoursePairList(join(path, child)))

    return components

def new_page_form():
    def enable_script(ID):
        enable = "document.getElementById('%s').disabled= !document.getElementById('%s').disabled;"
        return '%s' % (enable % (ID, ID))

    components = [js(script='function enable_weekselector(id) {%s}' % (enable_script('\'+id+\''))),
                  Label(text='Title:'),
                  form.Textbox(name='title', value='', size="50"),
                  Br(2),
                  Label(text='List of pages completed'),
                  Br(),
                  Checklist('pages', dict(getCoursePairList())),
                  Br(2),
                  Checklist('sf', dict(getSFPairList())),
                  Br(2),
                  Label(text='Date constaints'),
                  Br(),
                  Table([[Label(text='Before:'),
                          form.Checkbox('before_check', onchange="enable_weekselector('before_week')"),
                          #DateSelector(name="before_date", disable="true")],
                          WeekSelector(name="before_week", disabled="true")],
                         [Label(text='After:'),
                          form.Checkbox('after_check', onchange='enable_weekselector("after_week")'),
                          #DateSelector(name="after_date", disable="true")]]),
                          WeekSelector(name="after_week", disabled="true")]]),
                  Br(),
                  ScriptButton("Generate code", "generateConstraints()"),
                  Br(2),
                  Label(text='Advance constraint code:'),
                  Br(),
                  Label(text='lambda time, userID: '),
                  Br(),
                  form.Textarea(name='advance', value='', rows="8",
                                cols="100", 
                                style="resize:none, overflow:auto"),
                  Br(2),
                  Label(text='Page type:'),
                  form.Dropdown(name='page_type', args=['quiz', 'lesson']),
                  Br(2),
                  ScriptButton("Create", "checkAdvance();")
                  ]
    
    return div('', components)

def make_new_page(data):
    (title, path, code, page_type) = (data['title'], data['page'], data['code'], data['type'])
    print data
    from utils import *
    (conn, cursor) = getDbCursor('course.db')
    tmp_path = str(randint(0, maxint))
    cursor.execute('INSERT into chapter values(null, "%s");' % (tmp_path))
    conn.commit()
    
    cursor.execute('SELECT c.id FROM chapter c WHERE c.path = "%s";' % (tmp_path))
    rows = cursor.fetchall()
    newID = rows[0][0]

    cursor.execute('UPDATE chapter SET path = "%s" WHERE id=%d;' % (join(path, str(newID)), newID))
    conn.commit()

    new_dir = join(path, str(newID))
    mkdir(join(course_material, new_dir))
    writeLessonData(new_dir, str(newLessonData(newID, title, code, page_type)))

    parent_data = readLessonData(path)
    parent_data['chapters'].append(str(newID))
    writeLessonData(path, parent_data)

    f = open(join(course_material, new_dir, 'content.html'), 'w')
    f.write('<img src="http://www.coachnickhorton.com/wp-content/uploads/2009/11/under-construction-simpsons.gif"/>')
    f.close()

    return newID

# edit page
def edit_page_form(page):
    def enable_script(ID):
        enable = "document.getElementById('%s').disabled= !document.getElementById('%s').disabled;"
        return '%s' % (enable % (ID, ID))

    # TODO: enter in values
    data = readLessonData(page)
    components = [js(script='function enable_weekselector(id) {%s}' % (enable_script('\'+id+\''))),
                  Label(text='Title:'),
                  form.Textbox(name='title', value=data['title'], 
                               size="50"),
                  Br(2),
                  Label(text='List of pages completed'),
                  Br(),
                  Checklist('pages', dict(getCoursePairList()), code=data['readable']),
                  Br(2),
                  Label(text="Special flags"),
                  Br(),
                  Checklist('sf', dict(getSFPairList())),
                  Br(2),
                  Label(text='Date constaints'),
                  Br(),
                  Table([[Label(text='Before:'),
                          form.Checkbox('before_check', onchange="enable_weekselector('before_week')"),
                          #DateSelector(name="before_date", disable="true")],
                          WeekSelector(name="before_week", disabled="true")],
                         [Label(text='After:'),
                          form.Checkbox('after_check', onchange='enable_weekselector("after_week")'),
                          #DateSelector(name="after_date", disable="true")]]),
                          WeekSelector(name="after_week", disabled="true")]]),
                  Br(),
                  ScriptButton("Generate code", "generateConstraints()"),
                  Br(2),
                  Label(text='Advance constraint code:'),
                  Br(),
                  Label(text='lambda time, userID: '),
                  Br(),
                  form.Textarea(name='advance', rows="8",
                                cols="100", 
                                style="resize:none, overflow:auto",
                                value=data['readable']),
                  Br(2),
                  Label(text='Page type:'),
                  form.Dropdown(name='page_type', args=['quiz', 'lesson']),
                  Br(2),
                  ScriptButton("Create", "checkAdvance();")
                  ]
    
    return div('', components)

def process_edit_page(data):
    (title, path, code, page_type) = (data['title'], data['page'], data['code'], data['type'])

    ID = path.split('/')[-1]
    lesson_data = readLessonData(path)
    lesson_data['title'] = title
    lesson_data['readable'] = code
    lesson_data['type'] = page_type
    writeLessonData(path, lesson_data)

def getAdminPage():
    return sidebar_css(), lesson_layout(content=unreadable_content())

class up:
    def GET(self):
        input_data = web.input()
        if 'page' in input_data:
            page = input_data['page']
            nodes = page.split('/')
            if len(nodes) < 2:
                raise web.seeother('/course_control')
            else:
                (path, node) = (apply(join, nodes[:-1]), nodes[-1])
                lesson_data = readLessonData(path)
                previous = -1
                for i, item in enumerate(lesson_data['chapters']):
                    if item == node:
                        if previous != -1:
                            lesson_data['chapters'][i] = lesson_data['chapters'][previous]
                            lesson_data['chapters'][previous] = node
                            writeLessonData(path, lesson_data)
                        raise web.seeother('/course_control')

                    previous = i

        raise web.seeother('/course_control')

    def POST(self):
        return self.GET()


class down:
    def GET(self):
        input_data = web.input()
        if 'page' in input_data:
            page = input_data['page']
            nodes = page.split('/')
            if len(nodes) < 2:
                raise web.seeother('/course_control')
            else:
                (path, node) = (apply(join, nodes[:-1]), nodes[-1])
                lesson_data = readLessonData(path)
                if len(lesson_data['chapters']) < 2:
                    raise web.seeother('/course_control')
                next = 1
                for i, item in enumerate(lesson_data['chapters']):
                    if item == node:
                        if next != len(lesson_data['chapters']):
                            lesson_data['chapters'][i] = lesson_data['chapters'][next]
                            lesson_data['chapters'][next] = node
                            writeLessonData(path, lesson_data)
                        raise web.seeother('/course_control')

                    next += 1

        raise web.seeother('/course_control')

    def POST(self):
        return self.GET()

