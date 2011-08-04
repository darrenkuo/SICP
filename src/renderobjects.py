from os.path import join

from globals import *
from html import *

class css:
    def __init__(self):
        self.css_mapping = {}

    def add(self, id, mapping):
        self.css_mapping[id] = mapping

    def render(self):
        output = '<style type="text/css">\n'
        for i in self.css_mapping:
            output += '\t#%s { \n' % (i)
            for j in self.css_mapping[i]:
                output += '\t\t%s: %s;\n' % (j, self.css_mapping[i][j])
            output += '\t}\n'

        return output + '\t</style>'

class sidebar_css(css):
    def __init__(self):
        css.__init__(self)
        self.add('sidebar', {'overflow': 'auto',
                                         'height': '100%',
                                         'width': '15%',
                                         'float': 'left',
                                         'padding-left': '10px',
                                         'padding-top': '50px',})
        self.add('content', {'float': 'left',
                                         'height': '100%',
                                         'width': '80%',                      
                                         'padding-left': '50px',})

class quiz_js(js):
    def __init__(self, page, script='', question_type={}, *validators, **attrs):
        post_to_url = """function post_to_url(path, params, method) {
        method = method || "post"; // Set method to post by default, if not specified.
        
    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        var hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        hiddenField.setAttribute("name", key);
        hiddenField.setAttribute("value", params[key]);

        form.appendChild(hiddenField);
    }


    document.body.appendChild(form);
    form.submit();
  }
    """

        checked_value = """
function getCheckedValue(radioObj) {
if(!radioObj)
return "";
var radioLength = radioObj.length;
if(radioLength == undefined)
if(radioObj.checked)
return radioObj.value;
else
return "";
for(var i = 0; i < radioLength; i++) {
if(radioObj[i].checked) {
return radioObj[i].value;
}
}
return "";
}
    """
        submit_func = "function submit() { var data={};data['submitting']=true;"
        
        for q, t in question_type.iteritems():
            if t == 'r':
                submit_func += "data[%d] = getCheckedValue(document.forms['q%d-form'].elements['q%d']);" % (q, q, q)
            elif t == 'b':
                submit_func += "data[%d] = document.getElementById('q%d').value;" % (q, q)

        submit_func += 'post_to_url("/quiz?page=%s", data);}' % (page)

        script += post_to_url
        script += checked_value
        script += submit_func

        js.__init__(self, script)

class lesson_sidebar:
    def render(self):
        links = {'Main': '/summary',
                 'Logout': '/logout'}

        href = '\t<a href="%s">%s</a></br>'
        return ('<div id="sidebar">' +
                '\n'.join(map(lambda x: href % (x[1], x[0]),
                             links.items())) + 
                '</div>')

def makeNewPath(previous_path, path):
    if previous_path and path != '':
        return '/display?page=%s' % (previous_path + '-' + path)
    elif previous_path:
        return '/display?page=%s' % (previous_path)
    else:
        return '/display?page=%s' % (path)

def findPreviousNext(path):
    if path == '':
        return (None, '/summary')
    else:
        paths = path.strip().split('-')
        cur_ch = paths[-1]
        parent_path = join(course_material, '/'.join(paths[:-1]))

        f = open(join(parent_path, 'lesson.data'), 'r')
        x = eval(f.read())
        f.close()

        chapters = x['chapters']
        previous_join_path = '-'.join(paths[:-1])
        
        previous = None
        cur = False
        next = None
        for c in chapters:
            if cur:
                next = c
                break
            if c == cur_ch:
                cur = True

            if not cur:
                previous = c
                
        try:
            f = open(join(parent_path, cur_ch, 'lesson.data'), 'r')
            x = eval(f.read())
            y = x['chapters'][0]
            next = cur_ch + '-' + y
        except Exception, err:
            print err

        if next and previous:
            return (makeNewPath(previous_join_path, previous),
                    makeNewPath(previous_join_path, next))
        elif not previous and next:
            return (None, makeNewPath(previous_join_path, next))
        elif previous and not next:
            return (makeNewPath(previous_join_path, previous),
                    None)
        else:
            return (None, makeNewPath(previous_join_path, ''))

class unreadable_content:
    def render(self):
        return '<h2>This page is not accessible at the moment. It might be because unsatified requirements</h2>'    

class lesson_content:
    def __init__(self, title= None, content=None, path=None):
        self.title = title
        self.content = content
        self.path = path

    def render(self):
        output = '<div id="content">'

        if self.title:
            output += '<h2>%s</h2>' % (self.title)
        
        if self.content:
            if type(self.content) == str:
                output += self.content
            else:
                output += self.content.render()

        if self.path != None:
            (previous, next) = findPreviousNext(self.path)
            output += '</p>'
            output += '<table class="chapter" border="0" width="90%" cellspacing="0" cellpadding="0"><tr>'
            output += '<td class="prev">'
            if previous:
                output += '<a class="chapter" href="%s">&laquo; Previous</a>' % (previous)
            output += '</td>'
                
            output += '<td class="next" ALIGN=RIGHT>'
            if next:
                output += '<a class="chapter" href="%s">Next Chapter &raquo;</a>' % (next)
            output += '</td>'

            output += '</tr></table>'

        return output + '</div>'

class lesson_layout:
    def __init__(self, sidebar=lesson_sidebar(), content=lesson_content()):
        self.sidebar = sidebar
        self.content = content

    def render(self):
        return (self.sidebar.render() + '\n' + 
                self.content.render())
