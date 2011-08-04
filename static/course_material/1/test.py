#from src.utils import *
#from src.globals import *
from sys import path

def test(user, data):
    path.insert(0, 'src')

    from utils import *
    from globals import *
    
    i = 0
    (conn, cursor) = getDbCursor(course_db)

    print data
    while True:
        if str(i) not in data:
            break
        
        if i == 0 and data[str(i)].lower() == 'yes':
            cursor.execute('INSERT into SPECIAL_FLAG values("%s", "%s");' % (user, SF_PROGRAMMED))
        elif i == 1 and data[str(i)].lower() == 'yes':
            cursor.execute('INSERT into SPECIAL_FLAG values("%s", "%s");' % (user, SF_SCHEME))
        elif i == 2 and data[str(i)].lower() == 'yes':
            cursor.execute('INSERT into SPECIAL_FLAG values("%s", "%s");' % (user, SF_RECURSION))

        i += 1

    conn.commit()
    cursor.close()

