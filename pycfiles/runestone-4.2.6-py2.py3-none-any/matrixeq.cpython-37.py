# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/matrixeq/matrixeq.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 17672 bytes
from __future__ import print_function
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.common.runestonedirective import RunestoneDirective, RunestoneNode
import re
__author__ = 'Wayne Brown'

def setup(app):
    app.add_directive('matrixeq', MatrixEq)
    app.add_role('inline_matrixeq', inline_matrixeq)
    app.add_autoversioned_stylesheet('matrixeq.css')
    app.add_autoversioned_javascript('matrixeq.js')
    app.add_node(MatrixEqNode, html=(visit_matrixeq_node, depart_matrixeq_node))
    app.add_node(InlineMatrixEqNode,
      html=(
     visit_inline_matrixeq_node, depart_inline_matrixeq_node))
    app.connect('doctree-resolved', process_matrixeq_nodes)
    app.connect('env-purge-doc', purge_matrixeq)


class MatrixEq(RunestoneDirective):
    __doc__ = '\n.. matrixeq:: uniqueid\n    :notexecutable: -- the matrix equation can\'t be executed by the user\n    :comment: -- A comment to include to the right of the equation\n    :nolabel: -- don\'t label the equation using the uniqueid provided\n    :backgroundcolor: -- the color of the background; either #RRBBGG or a color name\n    :foregroundcolor: -- the color used for the matrix elements; either #RRBBGG or a color name\n    :highlightcolor: -- the color used for "bolded" elements; ; either #RRBBGG or a color name\n\n    A single matrix is defined using javascript array notation, e.g., [a,b,c;d,e,f]\n\n    A "name" can be assigned to a matrix by including a string and a colon after the\n    beginning [, but before the first value, e.g., [M1: a,b,c;d,e,f]. If no name is\n    specified, a default name is assigned.\n\n    A background color can be assigned to a matrix by including a color specifier\n    after the matrix\'s name. The color can be one of the standard HTML color names\n    or a color value (#RRGGBB). To specify a color, you must give the matrix a name.\n    E.g., [M1,lightcyan: a,b,c;d,e,f] or [M1,#DF85E8: a,b,c;d,e,f]\n\n    Individual elements of a matrix can have no special formatting, be highlighted,\n    be editable, or be both highlighted and editable. To make an element:\n        - highlighted, add an asterisk in front of the value, e.g., *a\n        - editable, put the value inside {}, e.g, {a}\n        - both highlighted and editable, *{a} or {*a}\n\n    The content of the directive is a matrix equation. E.g.,\n    [M1: 1, 0, 0, 0; 0, 1, 0, 0; 0, 0, -c2, c1; 0, 0, -1, 0]*[M2: x;y;z;1] = [M3: x\';y\';z\';w\']\n    '
    required_arguments = 1
    optional_arguments = 0
    has_content = True
    option_spec = {'notexecutable':directives.flag, 
     'comment':directives.unchanged, 
     'nolabel':directives.flag, 
     'backgroundcolor':directives.unchanged, 
     'foregroundcolor':directives.unchanged, 
     'highlightcolor':directives.unchanged}

    def run(self):
        env = self.state.document.settings.env
        if not hasattr(env, 'matrixeqcounter'):
            env.matrixeqcounter = 0
        else:
            env.matrixeqcounter += 1
            text = ''.join(self.content)
            text = text.replace("u'", "'")
            self.options['name'] = self.arguments[0].strip()
            self.options['contents'] = text
            self.options['equationnumber'] = self.arguments[0]
            self.options['equationcounter'] = env.matrixeqcounter
            self.options['executable'] = 'notexecutable' not in self.options
            self.options['nolabel'] = 'nolabel' in self.options
            if 'comment' in self.options:
                self.options['comment'] = self.options['comment'].strip()
            else:
                self.options['comment'] = ''
            color_scheme = ' style="background-color:'
            if 'backgroundcolor' in self.options:
                color_scheme += self.options['backgroundcolor'].strip() + ';'
            else:
                color_scheme += '#fcf8e3;'
            if 'foregroundcolor' in self.options:
                color_scheme += ' color:' + self.options['foregroundcolor'].strip() + ';'
            self.options['colorscheme'] = color_scheme + '"'
            if 'highlightcolor' in self.options:
                self.options['highlightcolor'] = self.options['highlightcolor'].strip()
            else:
                self.options['highlightcolor'] = 'red'
        return [
         MatrixEqNode(self.options)]


class MatrixEqNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(MatrixEqNode, self).__init__)(name=content['name'], **kwargs)
        self.components = content


def matrixToHTML(text, nodeID, node):
    parts = text.split(':')
    if len(parts) == 1:
        header = nodeID
        valuesStr = parts[0]
    else:
        header = parts[0]
        valuesStr = parts[1]
    if ',' in header:
        nodeName, matrixColor = header.split(',')
        matrixColor = ' style="background-color: ' + matrixColor + '" '
    else:
        nodeName = header
        matrixColor = ''
    if '*' in nodeName:
        highlight = ' style="color:#C8255D" '
    else:
        highlight = ''
    fieldSize = 6
    precision = str(fieldSize) + '.' + str(3) + 'f'
    values = []
    valuesFormat = []
    rowStrings = valuesStr.split(';')
    for row in range(len(rowStrings)):
        rowTextValues = rowStrings[row].split(',')
        rowValues = []
        rowFormat = []
        for col in range(len(rowTextValues)):
            s = rowTextValues[col].strip()
            formatValue = 0
            if s[0] == '*':
                formatValue |= 1
                s = s[1:]
            if s[0] == '{':
                formatValue |= 2
                s = s[1:]
                if s[(-1)] == '}':
                    s = s[:-1]
            if s[0] == '*':
                formatValue |= 1
                s = s[1:]
            try:
                valueAsNumber = float(s)
                if valueAsNumber.is_integer():
                    valueAsString = format(valueAsNumber, '6d')
                else:
                    valueAsString = format(valueAsNumber, precision)
            except ValueError:
                valueAsString = s

            rowValues.append(valueAsString)
            rowFormat.append(formatValue)

        values.append(rowValues)
        valuesFormat.append(rowFormat)

    res = '<span id="' + nodeID + '" class="matrix_table"' + highlight + matrixColor + '>'
    nRows = len(values)
    nCols = len(values[0])
    for r in range(0, nRows):
        if len(values[r]) != nCols:
            res = 'matrixeq directive error: row ' + str(r) + ' does not have ' + str(nCols) + ' values <br />'
            res += text
            return (res, nRows)

    for c in range(0, nCols):
        res += '<span class="matrix_column">'
        for r in range(0, nRows):
            valueStr = values[r][c]
            expIndex = valueStr.find('^(')
            if expIndex >= 0:
                expIndexEnd = valueStr.find(')', expIndex)
                if expIndexEnd > 0:
                    exp = valueStr[expIndex + 2:expIndexEnd]
                    valueStr = valueStr[0:expIndex] + '<sup>' + exp + '</sup>' + valueStr[expIndexEnd + 1:]
                if valuesFormat[r][c] == 0:
                    res += '<span>' + valueStr + '<br /></span>'
                elif valuesFormat[r][c] == 1:
                    res += '<span style="color:' + node.components['highlightcolor'] + ';">' + valueStr + '<br /></span>'
                elif valuesFormat[r][c] == 2:
                    res += '<span><input type="text" value="' + valueStr + '"></span>'
                elif valuesFormat[r][c] == 3:
                    res += '<span><input type="text" value="' + valueStr + '" style="color:' + node.components['highlightcolor'] + '";></span>'

        res += '</span>'

    res += '</span>'
    return (
     res, nRows)


def divide_matrixeq_into_its_parts(text):
    parts = []
    while len(text) > 0:
        matrix_start = text.find('[')
        if matrix_start >= 0:
            matrix_end = text.find(']', matrix_start)
            before = text[0:matrix_start]
            matrix = text[matrix_start:matrix_end + 1]
            text = text[matrix_end + 1:]
        else:
            before = text
            matrix = ''
            text = ''
        before = before.strip()
        if len(before) > 0:
            parts.append(before)
        if len(matrix) > 0:
            parts.append(matrix)

    return parts


def visit_matrixeq_node(self, node):
    parts = divide_matrixeq_into_its_parts(node.components['contents'].strip())
    id = 'M' + str(node.components['equationcounter'])
    node.components['equationcounter'] += 1
    res = '<!-- matrixeq start -->\n'
    res += "<div id='" + id + "' class='matrixeq_container'" + node.components['colorscheme'] + '>\n'
    for j in range(0, len(parts)):
        if parts[j][0] == '[':
            text, nRows = matrixToHTML(parts[j][1:-1], id + '_' + str(j), node)
            res += text
        else:
            if node.components['executable']:
                event = ' onclick="Matrixeq_directive(this);"'
            else:
                event = ''
            res += '<span class="matrix_operator"' + event + '>' + parts[j] + '</span>'

    comment = ''
    if len(node.components['comment']) > 0:
        comment = ' - ' + node.components['comment']
    label = node.components['equationnumber']
    if node.components['nolabel']:
        label = ''
    res += "<span class='matrix_label'> " + label + comment + '</span>'
    res += '</div>\n'
    res += '<!-- end of matrixeq -->'
    self.body.append(res)


def depart_matrixeq_node(self, node):
    """
    This is called at the start of processing an activecode node.  If activecode had recursive nodes
    etc and did not want to do all of the processing in visit_matrixeq_node any finishing touches could be
    added here.
    """
    pass


def process_matrixeq_nodes(app, env, docname):
    pass


def purge_matrixeq(app, env, docname):
    pass


class InlineMatrixEqNode(nodes.General, nodes.Element, RunestoneNode):
    __doc__ = '\n:inline_matrixeq:`[a,b;c,d]`\n\n    A inline_matrixeq role allows a matrix equation to be defined inside a\n    paragraph. The syntax for the matrix equation is identical to a matrixeq\n    directive. The operators in an in-line matrix equation are not executable.\n\n    In the future it would be nice to figure out how to make the background\n    color user configurable. (For some reason, inheriting the background color\n    from the enclosing parent makes the brackets of the matrices render\n    incorrectly.)\n\n    The background color is hardcoded to a light yellow.\n    The highlight color is hardcoded to red.\n    '

    def __init__(self, content, **kwargs):
        (super(InlineMatrixEqNode, self).__init__)(**kwargs)
        matrix_text = re.search(':inline_matrixeq:`(.*)`', content).group(1)
        self.components = {'contents':matrix_text, 
         'colorscheme':' style="background-color:inherit; color: inherit"', 
         'highlightcolor':'red', 
         'equationcounter':0}


def inline_matrixeq(roleName, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    """
    matrix_node = InlineMatrixEqNode(rawtext)
    matrix_node.line = lineno
    return ([matrix_node], [])


def visit_inline_matrixeq_node(self, node):
    parts = divide_matrixeq_into_its_parts(node.components['contents'].strip())
    id = 'M' + str(node.components['equationcounter'])
    node.components['equationcounter'] += 1
    res = '<!-- inline_matrixeq start -->\n'
    res += "<span id='" + id + "' class='matrixeq_container'" + node.components['colorscheme'] + '>\n'
    for j in range(0, len(parts)):
        if parts[j][0] == '[':
            text, nRows = matrixToHTML(parts[j][1:-1], id + '_' + str(j), node)
            res += text
        else:
            res += '<span class="matrix_operator">' + parts[j] + '</span>'

    res += '</span>\n'
    res += '<!-- end of inline_matrixeq -->'
    self.body.append(res)


def depart_inline_matrixeq_node(self, node):
    pass