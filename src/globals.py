import web

from time import mktime

dbs_path = 'dbs'
permission_files_path = 'student_progress'
render = web.template.render('templates/')
course_material = 'static/course_material'

course_db = 'course.db'
student_db = 'student_login.db'
admin_db = 'admin_login.db'

# every semester we will have to change this to a new day
# do time.mktime((YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, something, something, something)) * 1000
starting_date = mktime((2011, 1, 1, 0, 0, 0, 0, 0, 0)) * 1000
weeks = 15

week_milliseconds = 604800000

requests_dir = 'requests'
quiz_requests = 'requests/quiz'
admin_requests = 'requests/admin'

# Special flags
SF_PROGRAMMED = "PROGRAMMED"
SF_SCHEME = "KNOW_SCHEME"
SF_RECURSION = "KNOW_RECURSION"

