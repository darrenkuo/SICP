from sys import argv

def format_code(code):
    def level(line):
        l = 0
        for i in line:
            if i == '(':
                l += 1
            elif i == ')':
                l -= 1
        return l

    output = '<div style="padding: 10px; display: inline-block; border-style: solid; border-width: 1px; background-color: #66CCFF;">\n'
    indent = '&nbsp;&nbsp;'

    l = 0
    for i in code:
        output += (indent * l)
        l += level(i)
        output += '%s</br>\n' % (i.strip())

    output += '</div>'
    code.close()
    return output

if __name__ == '__main__':
    print format_code(open(argv[1], 'r'))
