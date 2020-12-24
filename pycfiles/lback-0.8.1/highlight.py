# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/highlight.py
# Compiled at: 2013-10-14 11:16:25
"""
This file is part of the web2py Web Framework
Copyrighted by Massimo Di Pierro <mdipierro@cs.depaul.edu>
License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)
"""
import re, cgi
__all__ = [
 'highlight']

class Highlighter(object):
    """
    Do syntax highlighting.
    """

    def __init__(self, mode, link=None, styles=None):
        """
        Initialise highlighter:
            mode = language (PYTHON, WEB2PY,C, CPP, HTML, HTML_PLAIN)
        """
        styles = styles or {}
        mode = mode.upper()
        if link and link[(-1)] != '/':
            link = link + '/'
        self.link = link
        self.styles = styles
        self.output = []
        self.span_style = None
        if mode == 'WEB2PY':
            mode, self.suppress_tokens = 'PYTHON', []
        elif mode == 'PYTHON':
            self.suppress_tokens = [
             'GOTOHTML']
        elif mode == 'CPP':
            mode, self.suppress_tokens = 'C', []
        elif mode == 'C':
            self.suppress_tokens = [
             'CPPKEYWORD']
        elif mode == 'HTML_PLAIN':
            mode, self.suppress_tokens = 'HTML', ['GOTOPYTHON']
        elif mode == 'HTML':
            self.suppress_tokens = []
        else:
            raise SyntaxError('Unknown mode: %s' % mode)
        self.mode = mode
        return

    def c_tokenizer(self, token, match, style):
        """
        Callback for C specific highlighting.
        """
        value = cgi.escape(match.group())
        self.change_style(token, style)
        self.output.append(value)

    def python_tokenizer(self, token, match, style):
        """
        Callback for python specific highlighting.
        """
        value = cgi.escape(match.group())
        if token == 'MULTILINESTRING':
            self.change_style(token, style)
            self.output.append(value)
            self.strMultilineString = match.group(1)
            return 'PYTHONMultilineString'
        else:
            if token == 'ENDMULTILINESTRING':
                if match.group(1) == self.strMultilineString:
                    self.output.append(value)
                    self.strMultilineString = ''
                    return 'PYTHON'
            if style and style[:5] == 'link:':
                self.change_style(None, None)
                url, style = style[5:].split(';', 1)
                if url == 'None' or url == '':
                    self.output.append('<span style="%s">%s</span>' % (
                     style, value))
                else:
                    self.output.append('<a href="%s%s" style="%s">%s</a>' % (
                     url, value, style, value))
            else:
                self.change_style(token, style)
                self.output.append(value)
            if token == 'GOTOHTML':
                return 'HTML'
            return

    def html_tokenizer(self, token, match, style):
        """
        Callback for HTML specific highlighting.
        """
        value = cgi.escape(match.group())
        self.change_style(token, style)
        self.output.append(value)
        if token == 'GOTOPYTHON':
            return 'PYTHON'
        else:
            return

    all_styles = {'C': (
           c_tokenizer,
           (
            (
             'COMMENT', re.compile('//.*\\r?\\n'),
             'color: green; font-style: italic'),
            (
             'MULTILINECOMMENT', re.compile('/\\*.*?\\*/', re.DOTALL),
             'color: green; font-style: italic'),
            (
             'PREPROCESSOR',
             re.compile('\\s*#.*?[^\\\\]\\s*\\n', re.DOTALL), 'color: magenta; font-style: italic'),
            (
             'PUNC', re.compile('[-+*!&|^~/%\\=<>\\[\\]{}(),.:]'),
             'font-weight: bold'),
            (
             'NUMBER',
             re.compile('0x[0-9a-fA-F]+|[+-]?\\d+(\\.\\d+)?([eE][+-]\\d+)?|\\d+'),
             'color: red'),
            (
             'KEYWORD',
             re.compile('(sizeof|int|long|short|char|void|' + 'signed|unsigned|float|double|' + 'goto|break|return|continue|asm|' + 'case|default|if|else|switch|while|for|do|' + 'struct|union|enum|typedef|' + 'static|register|auto|volatile|extern|const)(?![a-zA-Z0-9_])'),
             'color:#185369; font-weight: bold'),
            (
             'CPPKEYWORD',
             re.compile('(class|private|protected|public|template|new|delete|' + 'this|friend|using|inline|export|bool|throw|try|catch|' + 'operator|typeid|virtual)(?![a-zA-Z0-9_])'),
             'color: blue; font-weight: bold'),
            (
             'STRING', re.compile('r?u?\\\'(.*?)(?<!\\\\)\\\'|"(.*?)(?<!\\\\)"'),
             'color: #FF9966'),
            (
             'IDENTIFIER', re.compile('[a-zA-Z_][a-zA-Z0-9_]*'),
             None),
            (
             'WHITESPACE', re.compile('[   \\r\\n]+'), 'Keep'))), 
       'PYTHON': (
                python_tokenizer,
                (
                 (
                  'GOTOHTML', re.compile('\\}\\}'), 'color: red'),
                 (
                  'PUNC', re.compile('[-+*!|&^~/%\\=<>\\[\\]{}(),.:]'),
                  'font-weight: bold'),
                 (
                  'NUMBER',
                  re.compile('0x[0-9a-fA-F]+|[+-]?\\d+(\\.\\d+)?([eE][+-]\\d+)?|\\d+'),
                  'color: red'),
                 (
                  'KEYWORD',
                  re.compile('(def|class|break|continue|del|exec|finally|pass|' + 'print|raise|return|try|except|global|assert|lambda|' + 'yield|for|while|if|elif|else|and|in|is|not|or|import|' + 'from|True|False)(?![a-zA-Z0-9_])'),
                  'color:#185369; font-weight: bold'),
                 (
                  'WEB2PY',
                  re.compile('(request|response|session|cache|redirect|local_import|HTTP|TR|XML|URL|BEAUTIFY|A|BODY|BR|B|CAT|CENTER|CODE|COL|COLGROUP|DIV|EM|EMBED|FIELDSET|LEGEND|FORM|H1|H2|H3|H4|H5|H6|IFRAME|HEAD|HR|HTML|I|IMG|INPUT|LABEL|LI|LINK|MARKMIN|MENU|META|OBJECT|OL|ON|OPTION|P|PRE|SCRIPT|SELECT|SPAN|STYLE|TABLE|THEAD|TBODY|TFOOT|TAG|TD|TEXTAREA|TH|TITLE|TT|T|UL|XHTML|IS_SLUG|IS_STRONG|IS_LOWER|IS_UPPER|IS_ALPHANUMERIC|IS_DATETIME|IS_DATETIME_IN_RANGE|IS_DATE|IS_DATE_IN_RANGE|IS_DECIMAL_IN_RANGE|IS_EMAIL|IS_EXPR|IS_FLOAT_IN_RANGE|IS_IMAGE|IS_INT_IN_RANGE|IS_IN_SET|IS_IPV4|IS_LIST_OF|IS_LENGTH|IS_MATCH|IS_EQUAL_TO|IS_EMPTY_OR|IS_NULL_OR|IS_NOT_EMPTY|IS_TIME|IS_UPLOAD_FILENAME|IS_URL|CLEANUP|CRYPT|IS_IN_DB|IS_NOT_IN_DB|DAL|Field|SQLFORM|SQLTABLE|xmlescape|embed64)(?![a-zA-Z0-9_])'),
                  'link:%(link)s;text-decoration:None;color:#FF5C1F;'),
                 (
                  'MAGIC', re.compile('self|None'),
                  'color:#185369; font-weight: bold'),
                 (
                  'MULTILINESTRING', re.compile('r?u?(\\\'\\\'\\\'|""")'),
                  'color: #FF9966'),
                 (
                  'STRING', re.compile('r?u?\\\'(.*?)(?<!\\\\)\\\'|"(.*?)(?<!\\\\)"'),
                  'color: #FF9966'),
                 (
                  'IDENTIFIER', re.compile('[a-zA-Z_][a-zA-Z0-9_]*'),
                  None),
                 (
                  'COMMENT', re.compile('\\#.*\\r?\\n'),
                  'color: green; font-style: italic'),
                 (
                  'WHITESPACE', re.compile('[   \\r\\n]+'), 'Keep'))), 
       'PYTHONMultilineString': (
                               python_tokenizer,
                               (
                                (
                                 'ENDMULTILINESTRING',
                                 re.compile('.*?("""|\\\'\\\'\\\')', re.DOTALL), 'color: darkred'),)), 
       'HTML': (
              html_tokenizer,
              (
               (
                'GOTOPYTHON', re.compile('\\{\\{'), 'color: red'),
               (
                'COMMENT', re.compile('<!--[^>]*-->|<!>'),
                'color: green; font-style: italic'),
               (
                'XMLCRAP', re.compile('<![^>]*>'),
                'color: blue; font-style: italic'),
               (
                'SCRIPT',
                re.compile('<script .*?</script>', re.IGNORECASE + re.DOTALL), 'color: black'),
               (
                'TAG', re.compile('</?\\s*[a-zA-Z0-9]+'),
                'color: darkred; font-weight: bold'),
               (
                'ENDTAG', re.compile('/?>'),
                'color: darkred; font-weight: bold')))}

    def highlight(self, data):
        """
        Syntax highlight some python code.
        Returns html version of code.
        """
        i = 0
        mode = self.mode
        while i < len(data):
            for token, o_re, style in Highlighter.all_styles[mode][1]:
                if token not in self.suppress_tokens:
                    match = o_re.match(data, i)
                    if match:
                        if style:
                            new_mode = Highlighter.all_styles[mode][0](self, token, match, style % dict(link=self.link))
                        else:
                            new_mode = Highlighter.all_styles[mode][0](self, token, match, style)
                        if new_mode is not None:
                            mode = new_mode
                        i += max(1, len(match.group()))
                        break
            else:
                self.change_style(None, None)
                self.output.append(data[i])
                i += 1

        self.change_style(None, None)
        return ('').join(self.output).expandtabs(4)

    def change_style(self, token, style):
        """
        Generate output to change from existing style to another style only.
        """
        if token in self.styles:
            style = self.styles[token]
        if self.span_style != style:
            if style != 'Keep':
                if self.span_style is not None:
                    self.output.append('</span>')
                if style is not None:
                    self.output.append('<span style="%s">' % style)
                self.span_style = style
        return


def highlight(code, language, link='/examples/globals/vars/', counter=1, styles=None, highlight_line=None, context_lines=None, attributes=None):
    styles = styles or {}
    attributes = attributes or {}
    if 'CODE' not in styles:
        code_style = '\n        font-size: 11px;\n        font-family: Bitstream Vera Sans Mono,monospace;\n        background-color: transparent;\n        margin: 0;\n        padding: 5px;\n        border: none;\n        overflow: auto;\n        white-space: pre !important;\n'
    else:
        code_style = styles['CODE']
    if 'LINENUMBERS' not in styles:
        linenumbers_style = '\n        font-size: 11px;\n        font-family: Bitstream Vera Sans Mono,monospace;\n        background-color: transparent;\n        margin: 0;\n        padding: 5px;\n        border: none;\n        color: #A0A0A0;\n'
    else:
        linenumbers_style = styles['LINENUMBERS']
    if 'LINEHIGHLIGHT' not in styles:
        linehighlight_style = 'background-color: #EBDDE2;'
    else:
        linehighlight_style = styles['LINEHIGHLIGHT']
    if language and language.upper() in ('PYTHON', 'C', 'CPP', 'HTML', 'WEB2PY'):
        code = Highlighter(language, link, styles).highlight(code)
    else:
        code = cgi.escape(code)
    lines = code.split('\n')
    if counter is None:
        linenumbers = [
         ''] * len(lines)
    elif isinstance(counter, str):
        linenumbers = [
         cgi.escape(counter)] * len(lines)
    else:
        linenumbers = [ str(i + counter) + '.' for i in xrange(len(lines))
                      ]
    if highlight_line:
        if counter and not isinstance(counter, str):
            lineno = highlight_line - counter
        else:
            lineno = highlight_line
        if lineno < len(lines):
            lines[lineno] = '<div style="%s">%s</div>' % (
             linehighlight_style, lines[lineno])
            linenumbers[lineno] = '<div style="%s">%s</div>' % (
             linehighlight_style, linenumbers[lineno])
        if context_lines:
            if lineno + context_lines < len(lines):
                del lines[lineno + context_lines:]
                del linenumbers[lineno + context_lines:]
            if lineno - context_lines > 0:
                del lines[0:lineno - context_lines]
                del linenumbers[0:lineno - context_lines]
    code = ('<br/>').join(lines)
    numbers = ('<br/>').join(linenumbers)
    items = attributes.items()
    fa = (' ').join([ key[1:].lower() for key, value in items if key[:1] == '_' and value is None
                    ] + [ '%s="%s"' % (key[1:].lower(), str(value).replace('"', "'")) for key, value in attributes.items() if key[:1] == '_' and value
                        ])
    if fa:
        fa = ' ' + fa
    return '<table%s><tr style="vertical-align:top;"><td style="width:40px; text-align: right;"><pre style="%s">%s</pre></td><td><pre style="%s">%s</pre></td></tr></table>' % (
     fa, linenumbers_style, numbers, code_style, code)


if __name__ == '__main__':
    import sys
    argfp = open(sys.argv[1])
    data = argfp.read()
    argfp.close()
    print '<html><body>' + highlight(data, sys.argv[2]) + '</body></html>'