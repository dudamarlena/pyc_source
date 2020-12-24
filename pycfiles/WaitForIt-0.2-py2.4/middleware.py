# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/waitforit/middleware.py
# Compiled at: 2007-05-28 14:45:54
import threading, urllib
from itertools import count
import time, md5
from paste.request import path_info_pop, construct_url, get_cookies, parse_formvars
from paste import httpexceptions
from paste import httpheaders
from paste.util.template import Template
import simplejson, re
counter = count()

def make_id():
    value = str(time.time()) + str(counter.next())
    h = md5.new(value).hexdigest()
    return h


class WaitForIt(object):
    __module__ = __name__

    def __init__(self, app, time_limit=10, poll_time=10, template=None):
        self.app = app
        self.time_limit = time_limit
        self.poll_time = poll_time
        self.pending = {}
        if template is None:
            template = TEMPLATE
        if isinstance(template, basestring):
            template = Template(template)
        self.template = template
        return

    def __call__(self, environ, start_response):
        assert not environ['wsgi.multiprocess'], 'WaitForIt does not work in a multiprocess environment'
        path_info = environ.get('PATH_INFO', '')
        if path_info.startswith('/.waitforit/'):
            path_info_pop(environ)
            return self.check_status(environ, start_response)
        try:
            id = self.get_id(environ)
            if id:
                if id in self.pending:
                    return self.send_wait_page(environ, start_response, id=id)
                else:
                    qs = environ['QUERY_STRING']
                    qs = re.sub('&?waitforit_id=[a-f0-9]*', '', qs)
                    qs = re.sub('&send$', '', qs)
                    environ['QUERY_STRING'] = qs
                    exc = httpexceptions.HTTPMovedPermanently(headers=[('Location', construct_url(environ))])
                    return exc(environ, start_response)
        except KeyError:
            pass

        if not self.accept_html(environ):
            return self.app(environ, start_response)
        data = []
        progress = {}
        environ['waitforit.progress'] = progress
        event = threading.Event()
        self.launch_application(environ, data, event, progress)
        event.wait(self.time_limit)
        if not data:
            if progress.get('synchronous'):
                event.wait()
            id = data or make_id()
            self.pending[id] = [data, event, progress]
            return self.start_wait_page(environ, start_response, id)
        else:
            return self.send_page(start_response, data)

    def accept_html(self, environ):
        accept = httpheaders.ACCEPT.parse(environ)
        if not accept:
            return True
        for arg in accept:
            if ';' in arg:
                arg = arg.split(';', 1)[0]
            if arg in ('*/*', 'text/*', 'text/html', 'application/xhtml+xml', 'application/xml',
                       'text/xml'):
                return True

        return False

    def send_wait_page(self, environ, start_response, id=None):
        if id is None:
            id = self.get_id(environ)
        self.get_id(environ)
        if self.pending[id][0]:
            (data, event, progress) = self.pending.pop(id)
            return self.send_page(start_response, data)
        request_url = construct_url(environ)
        waitforit_url = construct_url(environ, path_info='/.waitforit/')
        page = self.template.substitute(request_url=request_url, waitforit_url=waitforit_url, poll_time=self.poll_time, time_limit=self.time_limit, environ=environ, id=id)
        if isinstance(page, unicode):
            page = page.encode('utf8')
        start_response('200 OK', [
         ('Content-Type', 'text/html; charset=utf8'), ('Content-Length', str(len(page))), ('Set-Cookie', 'waitforit_id=%s' % id)])
        return [
         page]

    def start_wait_page(self, environ, start_response, id):
        url = construct_url(environ)
        if '?' in url:
            url += '&'
        else:
            url += '?'
        url += 'waitforit_id=%s' % urllib.quote(id)
        exc = httpexceptions.HTTPTemporaryRedirect(headers=[('Location', url)])
        return exc(environ, start_response)

    def send_page(self, start_response, data):
        (status, headers, exc_info, app_iter) = data
        start_response(status, headers, exc_info)
        return app_iter

    def get_id(self, environ):
        qs = parse_formvars(environ)
        return qs['waitforit_id']

    def check_status(self, environ, start_response, id=None):
        assert environ['PATH_INFO'] == '/status.json', 'Bad PATH_INFO=%r for %r' % (environ['PATH_INFO'], construct_url(environ))
        if id is None:
            try:
                id = self.get_id(environ)
            except KeyError:
                body = 'There is no pending request with the id %s' % id
                start_response('400 Bad Request', [('Content-type', 'text/plain'), ('Content-length', str(len(body)))])
                return [
                 body]

        try:
            (data, event, progress) = self.pending[id]
        except KeyError:
            data, event, progress = True, None, None

        if not data:
            result = {'done': False, 'progress': progress}
        else:
            result = {'done': True}
        start_response('200 OK', [
         ('Content-Type', 'application/json'), ('Content-Length', str(len(result)))])
        return [
         simplejson.dumps(result)]

    def launch_application(self, environ, data, event, progress):
        t = threading.Thread(target=self.run_application, args=(environ, data, event, progress))
        t.setDaemon(True)
        t.start()

    def run_application(self, environ, data, event, progress):
        start_response_data = []
        output = []

        def start_response(status, headers, exc_info=None):
            start_response_data[:] = [status, headers, exc_info]
            return output.append

        app_iter = self.app(environ, start_response)
        if output:
            output.extend(app_iter)
            app_iter = output
        elif not start_response_data:
            app_iter = list(app_iter)
            assert start_response_data
        start_response_data.append(app_iter)
        data[:] = start_response_data
        event.set()
        return


TEMPLATE = '<html>\n <head>\n  <title>Please wait</title>\n  <script type="text/javascript">\n    waitforit_url = "{{waitforit_url}}";\n    poll_time = {{poll_time}};\n    <<JAVASCRIPT>>\n  </script>\n  <style type="text/css">\n    <<CSS>>\n  </style>\n </head>\n <body onload="checkStatus()">\n\n <h1>Please wait...</h1>\n\n <p>\n   The page you have requested is taking a while to generate...\n </p>\n\n <p id="progress-box">\n </p>\n\n <p id="percent-box">\n\n <p id="error-box">\n </p>\n \n </body>\n</html>\n'
JAVASCRIPT = 'function getXMLHttpRequest() {\n    var tryThese = [\n        function () { return new XMLHttpRequest(); },\n        function () { return new ActiveXObject(\'Msxml2.XMLHTTP\'); },\n        function () { return new ActiveXObject(\'Microsoft.XMLHTTP\'); },\n        function () { return new ActiveXObject(\'Msxml2.XMLHTTP.4.0\'); }\n        ];\n    for (var i = 0; i < tryThese.length; i++) {\n        var func = tryThese[i];\n        try {\n            return func();\n        } catch (e) {\n            // pass\n        }\n    }\n}\n\nfunction checkStatus() {\n    var xhr = getXMLHttpRequest();\n    xhr.onreadystatechange = function () {\n        if (xhr.readyState == 4) {\n            statusReceived(xhr);\n        }\n    };\n    if (waitforit_url.indexOf("?") != -1) {\n        var parts = waitforit_url.split("?");\n        var base = parts[0];\n        var qs = "?" + parts[1];\n    } else {\n        var base = waitforit_url;\n        var qs = \'\';\n    }\n    var status_url = base + "status.json" + qs;\n    xhr.open("GET", status_url);\n    xhr.send(null);\n}\n\nvar percent_inner = null;\n\nfunction statusReceived(req) {\n    if (req.status != 200) {\n        var el = document.getElementById("error-box");\n        el.innerHTML = req.responseText;\n        return;\n    }\n    var status = eval("dummy="+req.responseText);\n    if (typeof status.done == "undefined") {\n        // Something went wrong\n        var el = document.getElementById("error-box");\n        el.innerHTML = req.responseText;\n        return;\n    }\n    if (status.done) {\n        window.location.href = window.location.href + "&send";\n        return;\n    }\n    if (status.progress.message) {\n        var el = document.getElementById("progress-box");\n        el.innerHTML = status.progress.message;\n    }\n    if (status.progress.percent) {\n        if (! percent_inner) {\n            var outer = document.createElement("div");\n            outer.setAttribute("id", "percent-container");\n            percent_inner = document.createElement("div");\n            percent_inner.setAttribute("id", "percent-inner");\n            //percent_inner.innerHTML = "&nbsp;";\n            outer.appendChild(percent_inner);\n            var parent = document.getElementById("percent-box");\n            parent.appendChild(outer);\n        }\n        percent_inner.style.width = ""+Math.round(status.progress.percent) + "%";\n    }\n    setTimeout("checkStatus()", poll_time*1000);\n}\n'
CSS = 'body {\n  font-family: sans-serif;\n}\ndiv#percent-container {\n  border: 1px solid #000;\n  width: 100%;\n  height: 20px;\n}\ndiv#percent-inner {\n  background-color: #999;\n  height: 100%;\n}\n'
TEMPLATE = TEMPLATE.replace('<<JAVASCRIPT>>', JAVASCRIPT)
TEMPLATE = TEMPLATE.replace('<<CSS>>', CSS)