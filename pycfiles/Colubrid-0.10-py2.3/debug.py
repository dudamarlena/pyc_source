# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/colubrid/debug.py
# Compiled at: 2006-09-07 03:06:30
"""
    Colubrid Debugging Module
    =========================

    Adds debug support to colubrid applications.
"""
from __future__ import generators
import os, sys, re, traceback, keyword, token, tokenize, string, pprint, inspect, threading, cgi
from random import random
from cStringIO import StringIO
from xml.sax.saxutils import escape
JAVASCRIPT = '\nfunction toggleBlock(handler) {\n    if (handler.nodeName == \'H3\') {\n        var table = handler;\n        do {\n            table = table.nextSibling;\n            if (typeof table == \'undefined\') {\n                return;\n            }\n        }\n        while (table.nodeName != \'TABLE\');\n    }\n    \n    else if (handler.nodeName == \'DT\') {\n        var parent = handler.parentNode;\n        var table = parent.getElementsByTagName(\'TABLE\')[0];\n    }\n    \n    var lines = table.getElementsByTagName("TR");\n    for (var i = 0; i < lines.length; i++) {\n        var line = lines[i];\n        if (line.className == \'pre\' || line.className == \'post\') {\n            line.style.display = (line.style.display == \'none\') ? \'\' : \'none\';\n        }\n        else if (line.parentNode.parentNode.className == \'vars\' ||\n                 line.parentNode.parentNode.className == \'exec_code\') {\n            line.style.display = (line.style.display == \'none\') ? \'\' : \'none\';\n            var input = line.getElementsByTagName(\'TEXTAREA\');\n            if (input.length) {\n                input[0].focus();\n            }\n        }\n    }\n}\n\nfunction initTB() {\n    var tb = document.getElementById(\'wsgi-traceback\');\n    var handlers = tb.getElementsByTagName(\'H3\');\n    for (var i = 0; i < handlers.length; i++) {\n        toggleBlock(handlers[i]);\n        handlers[i].setAttribute(\'onclick\', \'toggleBlock(this)\');\n    }\n    handlers = tb.getElementsByTagName(\'DT\');\n    for (var i = 0; i < handlers.length; i++) {\n        toggleBlock(handlers[i]);\n        handlers[i].setAttribute(\'onclick\', \'toggleBlock(this)\');\n    }\n    var handlers = tb.getElementsByTagName(\'TEXTAREA\');\n    for (var i = 0; i < handlers.length; i++) {\n        var hid = handlers[i].getAttribute(\'id\');\n        if (hid && hid.substr(0, 6) == \'input-\') {\n            var p = handlers[i].getAttribute(\'id\').split(\'-\');\n            handlers[i].onkeyup = makeEnter(p[1], p[2]);\n        }\n    }\n}\n\nAJAX_ACTIVEX = [\'Msxml2.XMLHTTP\', \'Microsoft.XMLHTTP\', \'Msxml2.XMLHTTP.4.0\'];\n\nfunction ajaxConnect() {\n    var con = null;\n    try {\n        con = new XMLHttpRequest();\n    }\n    catch (e) {\n        if (typeof AJAX_ACTIVEX == \'string\') {\n            con = new ActiveXObject(AJAX_ACTIVEX);\n        }\n        else {\n            for (var i=0; i < AJAX_ACTIVEX.length; i++) {\n                var axid = AJAX_ACTIVEX[i];\n                try {\n                    con = new ActiveXObject(axid);\n                }\n                catch (e) {}\n                if (con) {\n                    AJAX_ACTIVEX = axid;\n                    break;\n                }\n            }\n        }\n    }\n    return con;\n}\n\nfunction execCode(traceback, frame) {\n    var input = document.getElementById(\'input-\' + traceback + \'-\' +\n                                        frame);\n    var e = encodeURIComponent;\n    var data = \'tb=\' + e(traceback) + \'&\' +\n               \'frame=\' + e(frame) + \'&\' +\n               \'code=\' + e(input.value);\n    writeToOutput(traceback, frame, \'>>> \' + input.value);\n    var con = ajaxConnect();\n    con.onreadystatechange = function() {\n        if (con.readyState == 4 && con.status == 200) {\n            writeToOutput(traceback, frame, con.responseText);\n            input.focus();\n            input.value = \'\';\n        }\n    };\n    con.open(\'GET\', \'__traceback__?\' + data);\n    con.send(data);\n}\n\nfunction makeEnter(traceback, frame) {\n    return function(e) {\n        var e = (e) ? e : window.event;\n        var code = (e.keyCode) ? e.keyCode : e.which;\n        if (code == 13) {\n            var input = document.getElementById(\'input-\' + traceback +\n                                                \'-\' + frame);\n            if (input.className == \'big\') {\n                if (input.value.substr(input.value.length - 2) != \'\\n\\n\') {\n                    return;\n                }\n                input.value = input.value.substr(0, input.value.length - 1);\n                input.className = \'small\';\n            }\n            if (input.value == \'clear\\n\') {\n                clearOutput(traceback, frame);\n                input.value = \'\';\n            }\n            else {\n                execCode(traceback, frame);\n            }\n        }\n    }\n}\n\nfunction writeToOutput(traceback, frame, text) {\n    var output = document.getElementById(\'output-\' + traceback + \'-\' +\n                                         frame);\n    if (text && text != \'\\n\') {\n        var node = document.createTextNode(text);\n        output.appendChild(node);\n    }\n}\n\nfunction clearOutput(traceback, frame) {\n    var output = document.getElementById(\'output-\' + traceback + \'-\' +\n                                         frame);\n    output.innerHTML = \'\';\n}\n\nfunction toggleExtend(traceback, frame) {\n    var input = document.getElementById(\'input-\' + traceback + \'-\' +\n                                        frame);\n    input.className = (input.className == \'small\') ? \'big\' : \'small\';\n    input.focus();\n}\n\nfunction change_tb() {\n    interactive = document.getElementById(\'interactive\');\n    plain = document.getElementById(\'plain\');\n    interactive.style.display = ((interactive.style.display == \'block\') | (interactive.style.display == \'\')) ? \'none\' : \'block\';\n    plain.style.display = (plain.style.display == \'block\') ? \'none\' : \'block\';\n}\n'
STYLESHEET = '\nbody {\n  font-size:0.9em;\n}\n\n* {\n  margin:0;\n  padding:0;\n}\n\n#wsgi-traceback {\n  margin: 1em;\n  border: 1px solid #5F9CC4;\n  background-color: #F6F6F6;\n}\n\n.footer {\n  margin: 1em;\n  text-align: right;\n  font-style: italic;\n}\n\nh1 {\n  background-color: #3F7CA4;\n  font-size:1.2em;\n  color:#FFFFFF;\n  padding:0.3em;\n  margin:0 0 0.2em 0;\n}\n\nh2 {\n  background-color:#5F9CC4;\n  font-size:1em;\n  color:#FFFFFF;\n  padding:0.3em;\n  margin:0.4em 0 0.2em 0;\n}\n\nh2.tb {\n  cursor:pointer;\n}\n\nh3 {\n  font-size:1em;\n  cursor:pointer;\n}\n\nh3.fn {\n  margin-top: 0.5em;\n}\n\nh3.fn:hover:before {\n  content: "\\21D2   ";\n}\n\nh3.indent {\n  margin:0 0.7em 0 0.7em;\n  font-weight:normal;\n}\n\np.text {\n  padding:0.1em 0.5em 0.1em 0.5em;\n}\n\np.important {\n  font-weight: bold;\n}\n\ndiv.frame {\n  margin:0 1em 0 1em;\n}\n\ntable.code {\n  margin:0.5em 0.7em 0.3em 0.7em;\n  background-color:#E0E0E0;\n  width:100%;\n  font-size:0.9em;\n  border:1px solid #C9C9C9;\n  border-collapse:collapse;\n}\n\ntable.code td.lineno {\n  width:42px;\n  text-align:right;\n  padding:0 5px 0 0;\n  color:#444444;\n  border-right:1px solid #888888;\n}\n\ntable.code td.code {\n  background-color:#EFEFEF;\n  padding:0 0 0 5px;\n  white-space:pre;\n}\n\ntable.code tr.cur td.code {\n  background-color: #FAFAFA;\n  padding: 1px 0 1px 5px;\n  white-space: pre;\n}\n\npre.plain {\n  margin:0.5em 1em 1em 1em;\n  padding:0.5em;\n  border:1px solid #999999;\n  background-color: #FFFFFF;\n  line-height: 120%;\n  font-family: monospace;\n}\n\ntable.exec_code {\n  width:100%;\n  margin:0 1em 0 1em;\n}\n\ntable.exec_code td.input {\n  width:100%;\n}\n\ntable.exec_code textarea.small {\n  width:100%;\n  height:1.5em;\n  border:1px solid #999999;\n}\n\ntable.exec_code textarea.big {\n  width:100%;\n  height:5em;\n  border:1px solid #999999;\n}\n\ntable.exec_code input {\n  height:1.5em;\n  border:1px solid #999999;\n  background-color:#FFFFFF;\n}\n\ntable.exec_code td.extend {\n  width:70px;\n  padding:0 5px 0 5px;\n}\n\ntable.exec_code td.output pre {\n  font-family: monospace;\n  white-space: pre-wrap;       /* css-3 should we be so lucky... */\n  white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */\n  white-space: -pre-wrap;      /* Opera 4-6 ?? */\n  white-space: -o-pre-wrap;    /* Opera 7 ?? */\n  word-wrap: break-word;       /* Internet Explorer 5.5+ */\n  _white-space: pre;   /* IE only hack to re-specify in addition to word-wrap  */\n}\n\ntable.vars {\n  margin:0 1.5em 0 1.5em;\n  border-collapse:collapse;\n  font-size: 0.9em;\n}\n\ntable.vars td {\n  font-family: \'Bitstream Vera Sans Mono\', \'Courier New\', monospace;\n  padding: 0.3em;\n  border: 1px solid #ddd;\n  vertical-align: top;\n  background-color: white;\n}\n\ntable.vars .name {\n  font-style: italic;\n}\n\ntable.vars .value {\n  color: #555;\n}\n\ntable.vars th {\n  padding: 0.2em;\n  border: 1px solid #ddd;\n  background-color: #f2f2f2;\n  text-align: left;\n}\n\n#plain {\n  display: none;\n}\n\ndl dt {\n    padding: 0.2em 0 0.2em 1em;\n    font-weight: bold;\n    cursor: pointer;\n    background-color: #ddd;\n}\n\ndl dt:hover {\n    background-color: #bbb; color: white;\n}\n\ndl dd {\n    padding: 0 0 0 2em;\n    background-color: #eee;\n}\n\nspan.p-kw {\n  font-weight:bold;\n}\n\nspan.p-cmt {\n  color:#8CBF83;\n}\n\nspan.p-str {\n  color:#DEA39B;\n}\n\nspan.p-num {\n  color:#D2A2D6;\n}\n\nspan.p-op {\n    color:#0000AA;\n}\n'

def get_uid():
    return str(random()).encode('base64')[3:11]


def get_frame_info(tb, context_lines=7):
    """
    Return a dict of informations about a given traceback.
    """
    lineno = tb.tb_lineno
    function = tb.tb_frame.f_code.co_name
    variables = tb.tb_frame.f_locals
    fn = tb.tb_frame.f_globals.get('__file__')
    if not fn:
        fn = os.path.realpath(inspect.getsourcefile(tb) or inspect.getfile(tb))
    if fn[-4:] in ('.pyc', '.pyo'):
        fn = fn[:-1]
    modname = tb.tb_frame.f_globals.get('__name__')
    loader = tb.tb_frame.f_globals.get('__loader__')
    try:
        if not loader is None:
            source = loader.get_source(modname)
        else:
            source = file(fn).read()
    except:
        source = ''
        (pre_context, post_context) = ([], [])
        (context_line, context_lineno) = (None, None)
    else:
        parser = PythonParser(source)
        parser.parse()
        parsed_source = parser.get_html_output()
        lbound = max(0, lineno - context_lines - 1)
        ubound = lineno + context_lines
        try:
            context_line = parsed_source[(lineno - 1)]
            pre_context = parsed_source[lbound:lineno - 1]
            post_context = parsed_source[lineno:ubound]
        except IndexError:
            context_line = None
            pre_context = post_context = ([], [])

        context_lineno = lbound

    return {'tb': tb, 'filename': fn, 'loader': loader, 'function': function, 'lineno': lineno, 'vars': variables, 'pre_context': pre_context, 'context_line': context_line, 'post_context': post_context, 'context_lineno': context_lineno, 'source': source}
    return


def debug_info(request, context=None, evalex=True):
    """
    Return debug info for the request
    """
    if context is None:
        context = Namespace()
    req_vars = []
    for item in dir(request):
        attr = getattr(request, item)
        if not (item.startswith('_') or inspect.isroutine(attr)):
            req_vars.append((item, attr))

    req_vars.sort()
    context.req_vars = req_vars
    return DebugRender(context, evalex).render()
    return


def get_current_thread():
    return threading.currentThread()


class Namespace(object):
    __module__ = __name__

    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class ThreadedStream(object):
    __module__ = __name__
    _orig = None

    def __init__(self):
        self._buffer = {}

    def install(cls, environ):
        if cls._orig or not environ['wsgi.multithread']:
            return
        cls._orig = sys.stdout
        sys.stdout = cls()

    install = classmethod(install)

    def can_interact(cls):
        return not cls._orig is None
        return

    can_interact = classmethod(can_interact)

    def push(self):
        tid = get_current_thread()
        self._buffer[tid] = StringIO()

    def release(self):
        tid = get_current_thread()
        if tid in self._buffer:
            result = self._buffer[tid].getvalue()
            del self._buffer[tid]
        else:
            result = ''
        return result

    def write(self, d):
        tid = get_current_thread()
        if tid in self._buffer:
            self._buffer[tid].write(d)
        else:
            self._orig.write(d)


class EvalContext(object):
    __module__ = __name__

    def __init__(self, frm):
        self.locals = frm.f_locals
        self.globals = frm.f_globals

    def exec_expr(self, s):
        sys.stdout.push()
        try:
            try:
                code = compile(s, '<stdin>', 'single', 0, 1)
                exec code in self.globals, self.locals
            except:
                (etype, value, tb) = sys.exc_info()
                tb = tb.tb_next
                msg = ('').join(traceback.format_exception(etype, value, tb))
                sys.stdout.write(msg)

        finally:
            output = sys.stdout.release()
        return output


class PythonParser(object):
    """
    Simple python sourcecode highlighter.
    Usage::

        p = PythonParser(source)
        p.parse()
        for line in p.get_html_output():
            print line
    """
    __module__ = __name__
    _KEYWORD = token.NT_OFFSET + 1
    _TEXT = token.NT_OFFSET + 2
    _classes = {token.NUMBER: 'num', token.OP: 'op', token.STRING: 'str', tokenize.COMMENT: 'cmt', token.NAME: 'id', token.ERRORTOKEN: 'error', _KEYWORD: 'kw', _TEXT: 'txt'}

    def __init__(self, raw):
        self.raw = raw.expandtabs(8).strip()
        self.out = StringIO()

    def parse(self):
        self.lines = [
         0, 0]
        pos = 0
        while 1:
            pos = string.find(self.raw, '\n', pos) + 1
            if not pos:
                break
            self.lines.append(pos)

        self.lines.append(len(self.raw))
        self.pos = 0
        text = StringIO(self.raw)
        try:
            tokenize.tokenize(text.readline, self)
        except tokenize.TokenError:
            pass

    def get_html_output(self):
        """ Return line generator. """

        def html_splitlines(lines):
            open_tag_re = re.compile('<(\\w+)(\\s.*)?[^/]?>')
            close_tag_re = re.compile('</(\\w+)>')
            open_tags = []
            for line in lines:
                for tag in open_tags:
                    line = tag.group(0) + line

                open_tags = []
                for tag in open_tag_re.finditer(line):
                    open_tags.append(tag)

                open_tags.reverse()
                for ctag in close_tag_re.finditer(line):
                    for otag in open_tags:
                        if otag.group(1) == ctag.group(1):
                            open_tags.remove(otag)
                            break

                for tag in open_tags:
                    line += '</%s>' % tag.group(1)

                yield line

        return list(html_splitlines(self.out.getvalue().splitlines()))

    def __call__(self, toktype, toktext, (srow, scol), (erow, ecol), line):
        oldpos = self.pos
        newpos = self.lines[srow] + scol
        self.pos = newpos + len(toktext)
        if toktype in [token.NEWLINE, tokenize.NL]:
            self.out.write('\n')
            return
        if newpos > oldpos:
            self.out.write(self.raw[oldpos:newpos])
        if toktype in [token.INDENT, token.DEDENT]:
            self.pos = newpos
            return
        if token.LPAR <= toktype and toktype <= token.OP:
            toktype = token.OP
        elif toktype == token.NAME and keyword.iskeyword(toktext):
            toktype = self._KEYWORD
        clsname = self._classes.get(toktype, 'txt')
        self.out.write('<span class="code-item p-%s">' % clsname)
        self.out.write(escape(toktext))
        self.out.write('</span>')


class DebugRender(object):
    __module__ = __name__

    def __init__(self, context, evalex):
        self.c = context
        self.evalex = evalex

    def render(self):
        return ('\n').join([self.header(), self.traceback(), self.request_information(), self.footer()])

    def header(self):
        data = [
         '<script type="text/javascript">%s</script>' % JAVASCRIPT, '<style type="text/css">%s</style>' % STYLESHEET, '<div id="wsgi-traceback">']
        if hasattr(self.c, 'exception_type'):
            title = escape(self.c.exception_type)
            exc = escape(self.c.exception_value)
            data += ['<h1>%s</h1>' % title, '<p class="text important">%s</p>' % exc]
        if hasattr(self.c, 'last_frame'):
            data += ['<p class="text important">%s in %s, line %s</p>' % (self.c.last_frame['filename'], self.c.last_frame['function'], self.c.last_frame['lineno'])]
        return ('\n').join(data)

    def render_code(self, frame):

        def render_line(mode, lineno, code):
            return ('').join(['<tr class="%s">' % mode, '<td class="lineno">%i</td>' % lineno, '<td class="code">%s</td></tr>' % code])

        tmp = [
         '<table class="code">']
        lineno = frame['context_lineno']
        if not lineno is None:
            lineno += 1
            for l in frame['pre_context']:
                tmp.append(render_line('pre', lineno, l))
                lineno += 1

            tmp.append(render_line('cur', lineno, frame['context_line']))
            lineno += 1
            for l in frame['post_context']:
                tmp.append(render_line('post', lineno, l))
                lineno += 1

        else:
            tmp.append(render_line('cur', 1, 'Sourcecode not available'))
        tmp.append('</table>')
        return ('\n').join(tmp)
        return

    def var_table(self, var):
        if isinstance(var, basestring) or isinstance(var, float) or isinstance(var, int) or isinstance(var, long):
            return '<table class="vars"><tr><td class="value">%r</td></tr></table>' % var
        if isinstance(var, dict) or hasattr(var, 'items'):
            items = var.items()
            items.sort()
            if not items:
                return '<table class="vars"><tr><th>no data given</th></tr></table>'
            result = [
             '<table class="vars"><tr><th>Name</th><th>Value</th></tr>']
            for (key, value) in items:
                try:
                    val = escape(pprint.pformat(value))
                except:
                    val = '?'

                result.append('<tr><td class="name">%s</td><td class="value">%s</td></tr>' % (escape(repr(key)), val))

            result.append('</table>')
            return ('\n').join(result)
        if isinstance(var, list):
            if not var:
                return '<table class="vars"><tr><th>no data given</th></tr></table>'
            result = [
             '<table class="vars">']
            for line in var:
                try:
                    val = escape(pprint.pformat(line))
                except:
                    val = '?'

                result.append('<tr><td class="value">%s</td></tr>' % val)

            result.append('</table>')
            return ('\n').join(result)
        try:
            value = escape(repr(var))
        except:
            value = '?'

        return '<table class="vars"><tr><th>%s</th></tr></table>' % value

    def exec_code_table(self, uid):
        return '\n        <table class="exec_code">\n          <tr>\n            <td class="output" colspan="2"><pre id="output-%(tb_uid)s-%(frame_uid)s"></pre></td>\n           </tr>\n          <tr>\n            <td class="input">\n              <textarea class="small" id="input-%(tb_uid)s-%(frame_uid)s" value=""></textarea>\n            </td>\n            <td class="extend">\n              <input type="button" onclick="toggleExtend(\'%(tb_uid)s\', \'%(frame_uid)s\')" value="extend">\n            </td>\n          </tr>\n        </table>\n        ' % {'target': '#', 'tb_uid': self.c.tb_uid, 'frame_uid': uid}

    def traceback(self):
        if not hasattr(self.c, 'frames'):
            return ''
        result = ['<h2 onclick="change_tb()" class="tb">Traceback (click to switch to raw view)</h2>']
        result.append('<div id="interactive"><p class="text">A problem occurred in your Python WSGI application. Here is the sequence of function calls leading up to the error, in the order they occurred. Click on a header to show context lines.</p>')
        for (num, frame) in enumerate(self.c.frames):
            line = [
             '<div class="frame" id="frame-%i">' % num, '<h3 class="fn">%s in %s</h3>' % (frame['function'], frame['filename']), self.render_code(frame)]
            if frame['vars']:
                line.append(('\n').join(['<h3 class="indent">&rArr; local variables</h3>', self.var_table(frame['vars'])]))
            if self.evalex and self.c.tb_uid:
                line.append(('\n').join(['<h3 class="indent">&rArr; execute code</h3>', self.exec_code_table(frame['frame_uid'])]))
            line.append('</div>')
            result.append(('').join(line))

        result.append(('\n').join(['</div>', self.plain()]))
        return ('\n').join(result)

    def plain(self):
        if not hasattr(self.c, 'plaintb'):
            return ''
        return '\n        <div id="plain">\n        <p class="text">Here is the plain Python traceback for copy and paste:</p>\n        <pre class="plain">\n%s</pre>\n        </div>\n        ' % self.c.plaintb

    def request_information(self):
        result = [
         '<h2>Request Data</h2>', '<p class="text">The following list contains all important', 'request variables. Click on a header to expand the list.</p>']
        if not hasattr(self.c, 'frames'):
            del result[0]
        for (key, info) in self.c.req_vars:
            result.append('<dl><dt>%s</dt><dd>%s</dd></dl>' % (escape(key), self.var_table(info)))

        return ('\n').join(result)

    def footer(self):
        return ('\n').join(['<script type="text/javascript">initTB();</script>', '</div>', '<div class="footer">Brought to you by <span style="font-style: normal">DON\'T PANIC</span>, your friendly Colubrid traceback interpreter system.</div>', hasattr(self.c, 'plaintb') and '<!-- Plain traceback:\n\n%s-->' % self.c.plaintb or ''])


class DebuggedApplication(object):
    """
    Enables debugging support for a given application::

        from colubrid.debug import DebuggedApplication
        from myapp import app
        app = DebuggedApplication(app)

    Or for a whole package::
        
        app = DebuggedApplication("myapp:app")
    """
    __module__ = __name__

    def __init__(self, application, evalex=True):
        self.evalex = bool(evalex)
        if not isinstance(application, basestring):
            self.application = application
        else:
            try:
                (self.module, self.handler) = application.split(':', 1)
            except ValueError:
                self.module = application
                self.handler = 'app'

        self.tracebacks = {}

    def __call__(self, environ, start_response):
        if self.evalex and environ.get('PATH_INFO', '').strip('/').endswith('__traceback__'):
            parameters = cgi.parse_qs(environ['QUERY_STRING'])
            try:
                tb = self.tracebacks[parameters['tb'][0]]
                frame = parameters['frame'][0]
                context = tb[frame]
                code = parameters['code'][0].replace('\r', '')
            except (IndexError, KeyError):
                pass
            else:
                result = context.exec_expr(code)
                start_response('200 OK', [('Content-Type', 'text/plain')])
                yield result
                return
        appiter = None
        try:
            if hasattr(self, 'application'):
                result = self.application(environ, start_response)
            else:
                module = __import__(self.module, '', '', [''])
                app = getattr(module, self.handler)
                result = app(environ, start_response)
            appiter = iter(result)
            for line in appiter:
                yield line

        except:
            ThreadedStream.install(environ)
            exc_info = sys.exc_info()
            try:
                headers = [
                 (
                  'Content-Type', 'text/html')]
                start_response('500 INTERNAL SERVER ERROR', headers)
            except:
                pass
            else:
                debug_context = self.get_debug_context(exc_info)
                yield debug_info(environ.get('colubrid.request'), debug_context, self.evalex)

        if hasattr(appiter, 'close'):
            appiter.close()
        return

    def get_debug_context(self, exc_info):
        (exception_type, exception_value, tb) = exc_info
        if not tb.tb_next is None:
            tb = tb.tb_next
        plaintb = ('').join(traceback.format_exception(*exc_info))
        frames = []
        frame_map = {}
        tb_uid = None
        if ThreadedStream.can_interact():
            tb_uid = get_uid()
            frame_map = self.tracebacks[tb_uid] = {}
        while tb is not None:
            if tb_uid:
                frame_uid = get_uid()
                frame_map[frame_uid] = EvalContext(tb.tb_frame)
            else:
                frame_uid = None
            frame = get_frame_info(tb)
            frame['frame_uid'] = frame_uid
            frames.append(frame)
            tb = tb.tb_next

        if exception_type.__module__ == 'exceptions':
            extypestr = exception_type.__name__
        else:
            extypestr = str(exception_type)
        return Namespace(exception_type=extypestr, exception_value=str(exception_value), frames=frames, last_frame=frames[(-1)], plaintb=plaintb, tb_uid=tb_uid, frame_map=frame_map)
        return