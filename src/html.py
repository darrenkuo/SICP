import web

from web import form
from re import match

import globals as globals_61as

class p(form.Input):
    def __init__(self, txt, *validators, **attrs):
        self.txt = txt
        super(p, self).__init__('', *validators, **attrs)

    def render(self):
        return '<p>%s</p>' % (self.txt)
    
class a(form.Input):
    def __init__(self, txt, link, *validators, **attrs):
        self.txt = txt
        self.link = link
        super(a, self).__init__('', *validators, **attrs)

    def render(self):
        return '<a href="%s">%s</a>' % (self.link, self.txt)

class ol(form.Input):
    def __init__(self, name, components, *validators, **attrs):
        self.components = components
        super(ol, self).__init__(name, *validators, **attrs)

    def render(self):
        txt = '<ol>\n'
        for c in self.components:
            txt += c.render()
            txt += '\n'
        return txt + '</ol>\n'    

class ul(form.Input):
    def __init__(self, name, components, *validators, **attrs):
        self.components = components
        super(ul, self).__init__(name, *validators, **attrs)

    def render(self):
        txt = '<ul>\n'
        for c in self.components:
            txt += c.render()
            txt += '\n'
        return txt + '</ul>\n'

class li(form.Input):
    def __init__(self, name, text, *validators, **attrs):
        self.text = text
        super(li, self).__init__(name, *validators, **attrs)
        
    def render(self):
        return '<li>%s</li>' % (self.text)

class chapter_entry(form.Input):
    def __init__(self, name, text, path, *validators, **attrs):
        self.text = text
        self.path = path
        super(chapter_entry, self).__init__(name, *validators, **attrs)

    def render(self):
        return '<div>%s&nbsp;&nbsp;&nbsp;<a href="/new_page?page=%s">New Page</a>&nbsp;&nbsp;&nbsp;<a href="/edit_page?page=%s">Edit Page</a>&nbsp;&nbsp;<a href="/up?page=%s">Up</a>&nbsp;&nbsp;<a href="/down?page=%s">Down</a></div>' % (self.text, self.path, self.path, self.path, self.path)

class div(form.Input):
    def __init__(self, name, components, *validators, **attrs):
        self.components = components
        super(div, self).__init__(name, *validators, **attrs)

    def render(self):
        html_code = '<div>\n'
        for c in self.components:
            html_code += '%s\n' % (c.render())

        return '%s</div>\n' % (html_code)

class Checklist(form.Input):
    def __init__(self, name, checklist, *validators, **attrs):
        self.checklist = checklist
        self.code = ''
        if 'code' in attrs:
            self.code = attrs.pop('code')
        super(Checklist, self).__init__(name, *validators, **attrs)

    def render(self):
        indices = []
        if self.code:
            for line in self.code.split('and'):
                m = match('checkAccessed\(([\d]+), user\)', line.strip())
                if m:
                    indices.append(int(m.groups()[0]))

        html_code = '<form id="%s">\n' % (self.name)
        for ID, text in self.checklist.iteritems():
            if ID in indices:
                html_code += ('<input type="checkbox" id="%s" checked=true />%s<br/>\n' % (ID, text))
            else:
                html_code += ('<input type="checkbox" id="%s" />%s<br/>\n' % (ID, text))

        return '%s</form>\n' % (html_code)

class Label(form.Input):
    def __init__(self, text, name='', *validators, **attrs):
        self.text = text
        super(Label, self).__init__(name, *validators, **attrs)

    def render(self):
        if self.id:
            return '<label id="%s">%s</label>' % (self.id, self.text)
        return '<label>%s</label>' % (self.text)

class Br(form.Input):
    def __init__(self, n=1, *validators, **attrs):
        self.n = n
        super(Br, self).__init__('', *validators, **attrs)

    def render(self):
        return '<br/>' * self.n

class DateSelector(form.Input):
    def __init__(self, name, *validators, **attrs):
        self.disable = None
        if "disable" in attrs:
            self.disable = attrs.pop("disable")
        super(DateSelector, self).__init__(name, *validators, **attrs)

    def render(self):
        html_code = \
        """
        <div id = "%s">
        <script type="text/javascript">
        Now = new Date();
        NowDay = Now.getDate();
        NowMonth = Now.getMonth();
        NowYear = Now.getYear();
        if (NowYear < 2000) NowYear += 1900; //for Netscape
        
        //function for returning how many days there are in a month including leap years
        function DaysInMonth(WhichMonth, WhichYear)
        {
        var DaysInMonth = 31;
        if (WhichMonth == "Apr" || WhichMonth == "Jun" || WhichMonth == "Sep" || WhichMonth == "Nov") DaysInMonth = 30;
        if (WhichMonth == "Feb" && (WhichYear/4) != Math.floor(WhichYear/4))DaysInMonth = 28;
        if (WhichMonth == "Feb" && (WhichYear/4) == Math.floor(WhichYear/4))DaysInMonth = 29;
        return DaysInMonth;
        }
        
        //function to change the available days in a months
        function ChangeOptionDays(date_id)
        {
        DaysObject = document.getElementById(date_id + "Day");
        MonthObject = document.getElementById(date_id + "Month");
        YearObject = document.getElementById(date_id + "Year");
        
        Month = MonthObject[MonthObject.selectedIndex].text;
        Year = YearObject[YearObject.selectedIndex].text;
        
        DaysForThisSelection = DaysInMonth(Month, Year);
        CurrentDaysInSelection = DaysObject.length;
        if (CurrentDaysInSelection > DaysForThisSelection)
        {
        for (i=0; i<(CurrentDaysInSelection-DaysForThisSelection); i++)
        {
        DaysObject.options[DaysObject.options.length - 1] = null
        }
        }
        if (DaysForThisSelection > CurrentDaysInSelection)
        {
        for (i=0; i<(DaysForThisSelection-CurrentDaysInSelection); i++)
        {
        NewOption = new Option(DaysObject.options.length + 1);
        DaysObject.add(NewOption);
        }
        }
        if (DaysObject.selectedIndex < 0) DaysObject.selectedIndex == 0;
        }
        
        //function to set options to today
        function SetToToday(date_id)
        {
        DaysObject = document.getElementById(date_id + "Day");
        MonthObject = document.getElementById(date_id + "Month");
        YearObject = document.getElementById(date_id + "Year");
        
        YearObject[0].selected = true;
        MonthObject[NowMonth].selected = true;
        
        ChangeOptionDays(date_id);
        
        DaysObject[NowDay-1].selected = true;
        }
        
        //function to write option years plus x
        function WriteYearOptions(YearsAhead)
        {
        line = "";
        for (i=0; i<YearsAhead; i++)
        {
        line += "<OPTION>";
        line += NowYear + i;
        }
        return line;
        }
        </script>
        <SELECT id="%sDay" %s>
        <OPTION>1
        <OPTION>2
        <OPTION>3
        <OPTION>4
        <OPTION>5
        <OPTION>6
        <OPTION>7
        <OPTION>8
        <OPTION>9
        <OPTION>10
        <OPTION>11
        <OPTION>12
        <OPTION>13
        <OPTION>14
        <OPTION>15
        <OPTION>16
        <OPTION>17
        <OPTION>18
        <OPTION>19
        <OPTION>20
        <OPTION>21
        <OPTION>22
        <OPTION>23
        <OPTION>24
        <OPTION>25
        <OPTION>26
        <OPTION>27
        <OPTION>28
        <OPTION>29
        <OPTION>30
        <OPTION>31
        </SELECT>
        <SELECT id="%sMonth" onchange="ChangeOptionDays('%s')" %s>
        <OPTION>Jan
        <OPTION>Feb
        <OPTION>Mar
        <OPTION>Apr
        <OPTION>May
        <OPTION>Jun
        <OPTION>Jul
        <OPTION>Aug
        <OPTION>Sep
        <OPTION>Oct
        <OPTION>Nov
        <OPTION>Dec
        </SELECT>
        <SELECT id="%sYear" onchange="ChangeOptionDays('%s')" %s>
        <SCRIPT type="text/javascript">
        document.write(WriteYearOptions(50));
        SetToToday("%s");
        </SCRIPT>
        </SELECT>
        </div>
        """
        
        disable_code = ""
        if self.disable:
            disable_code = 'disabled="%s"' % (self.disable)

        return html_code % (self.id, self.id, disable_code,
                            self.id, self.id,
                            disable_code, self.id, self.id, disable_code,
                            self.id)

class Table(form.Input):
    def __init__(self, components, border=0, name='', *validators, **attrs):
        self.components = components
        self.border = border
        super(Table, self).__init__(name, *validators, **attrs)

    def render(self):
        html_code = '<table border="%d">\n' % (self.border)
        for row in self.components:
            html_code += '<tr>\n'
            for column in row:
                html_code += '<th>%s</th>\n' % (column.render())
            html_code += '</tr>\n'

        return '%s</table>\n' % (html_code)
        
class ScriptButton(form.Input):
    def __init__(self, name, onclick, *validators, **attrs):
        self.onclick = onclick
        super(ScriptButton, self).__init__(name, *validators, **attrs)

    def render(self):
        html_code = '<button onclick="%s">%s</button>' % (self.onclick,
                                                          self.name)

        return html_code

class ScriptCheckbox(form.Input):
    def __init__(self, name, script='', *validators, **attrs):
        self.script = script
        self.checked = attrs.pop('checked', False)
        Input.__init__(self, name, *validators, **attrs)
        
    def get_default_id(self):
        value = utils.safestr(self.value or "")
        return self.name + '_' + value.replace(' ', '_')

    def render(self):
        attrs = self.attrs.copy()
        attrs['type'] = 'checkbox'
        attrs['name'] = self.name
        attrs['value'] = self.value

        if self.checked:
            attrs['checked'] = 'checked'            
        return '<input %s/>' % attrs

    def set_value(self, value):
        self.checked = bool(value)

    def get_value(self):
        return self.checked

class js(form.Input):
    def __init__(self, script='', *validators, **attrs):
        self.script = script
        super(js, self).__init__('', *validators, **attrs)

    def render(self):
        return '<script type="text/javascript">%s</script>' % (self.script)

class WeekSelector(form.Input):
    def __init__(self, name, *validators, **attrs):
        self.attrs = attrs
        super(WeekSelector, self).__init__(name, *validators, **attrs)

    def render(self):
        html = '<select %s>\n' % (self.attrs)
        for i in range(1, globals_61as.weeks + 1):
            html += '<option value=%d>Week %d</option>\n' % (globals_61as.starting_date + (globals_61as.week_milliseconds * (i - 1)), i)
        return '%s</select>' % (html)
