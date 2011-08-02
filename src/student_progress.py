from os import walk
from os.path import join

from globals import course_material
from globals import permission_files_path

def true_lambda():
    return True

# change to a flat format or use sqlite!
def make_blank(directory):
    g = open(join(directory, 'lesson.data'), 'r')
    lesson_data = eval(g.read())
    g.close()

    print lesson_data
    print lesson_data.keys()
    
    data = {'chapters' : list(lesson_data['chapters']),
            #'readable' : False
            'visited' : False}

    for c in data['chapters']:
        data[c[0]] = make_blank(join(directory, c[0]))
        
    return data

def create_user_permission_file(login):
    f = open(join(permission_files_path, '%s.permission' % (login)), 'w')
    
    data = make_blank(course_material)
    #data['readable'] = True
    #data[data['chapters'][0][0]]['readable'] = True
    #subchapter = data[data['chapters'][0][0]]
    #data[data['chapters'][0][0]][subchapter['chapters'][0][0]]['readable'] = True

    f.write(str(data))
    f.close()
        
        
