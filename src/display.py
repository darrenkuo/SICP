import web

from web import form
from globals import *
from lesson import *
from utils import *

class display:
    def GET(self):
        data = web.input()
        session = web.config.get('_session')
        if 'page' in data:
            lesson_data = readLessonData(convertToRealPath(data['page']))
            storeVisit(lesson_data['index'], session.user)

            if lesson_data['type'] == 'lesson':
                raise web.seeother('/lesson?page=%s' % (data['page']))
            elif lesson_data['type'] == 'quiz':
                raise web.seeother('/quiz?page=%s' % (data['page']))

        return render.lesson(getLesson(session.user, ''))

    def POST(self):
        return self.GET()
