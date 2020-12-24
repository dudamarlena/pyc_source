# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/servable.py
# Compiled at: 2009-04-03 14:43:58
from wsgiref.simple_server import make_server
from types import *
import re, cgi, traceback
from urlparse import urlparse
try:
    from simplejson import loads as json_loads
except ImportError:
    from json import loads as json_loads

def function_arg_names(func):
    return func.func_code.co_varnames[0:func.func_code.co_argcount]


def method_arg_names(meth):
    return function_arg_names(meth)[1:]


def method_name(meth):
    return meth.func_name


def method_path(meth):
    if hasattr(meth, 'path'):
        return meth.path
    else:
        return '/' + method_name(meth) + '$'


def methods(cls):
    for name in dir(cls):
        attr = getattr(cls, name)
        if type(attr) == UnboundMethodType:
            yield attr


def xstr(arg):
    if arg is None:
        return ''
    else:
        return arg.encode('utf8')
        return


class Servable:
    DEFAULT_MIME = 'text/plain'

    def patterns(self):
        """returns list of (path,argnames,method)"""
        for method in methods(self.__class__):
            if method_name(method)[0] != '_' and not (hasattr(method, 'serve') and method.serve == False):
                yield (
                 re.compile(method_path(method)), method_arg_names(method), method)

    patterns.serve = False

    def wsgi_app(self):
        """returns a wsgi app which exposes this object as a webservice"""

        def myapp(environ, start_response):
            if 'REQUEST_URI' in environ:
                parsed_url = urlparse(environ['REQUEST_URI'])
                path_info = parsed_url[2]
                query_string = parsed_url[4]
            else:
                path_info = environ['PATH_INFO']
                query_string = environ['QUERY_STRING']
            if not hasattr(self, 'pattern_cache'):
                self.pattern_cache = [ (pth, args, pfunc) for (pth, args, pfunc) in self.patterns() ]
            for (ppath, pargs, pfunc) in self.pattern_cache:
                if ppath.match(path_info):
                    args = cgi.parse_qs(query_string)
                    args = dict([ (k, v[0]) for (k, v) in args.iteritems() ])
                    try:
                        args = dict([ (k, json_loads(v)) for (k, v) in args.iteritems() ])
                        rr = xstr(pfunc(self, **args))
                        if hasattr(pfunc, 'mime'):
                            mime = pfunc.mime
                        else:
                            mime = self.DEFAULT_MIME
                        start_response('200 OK', [('Content-type', mime), ('Content-Length', str(len(rr)))])
                        return [rr]
                    except:
                        problem = traceback.format_exc()
                        start_response('500 Internal Error', [('Content-type', 'text/plain'), ('Content-Length', str(len(problem)))])
                        return [problem]

            problem = "No method corresponds to path '%s'" % environ['PATH_INFO']
            start_response('404 Not Found', [('Content-type', 'text/plain'), ('Content-Length', str(len(problem)))])
            return [problem]

        return myapp

    wsgi_app.serve = False

    def run_test_server(self, port=8080):
        print 'starting HTTP server'
        httpd = make_server('', port, self.wsgi_app())
        httpd.serve_forever()

    run_test_server.serve = False

    def usage(self):
        ret = [
         "<?xml version='1.0'?><api>"]
        for (ppath, pargs, pfunc) in self.patterns():
            ret.append('<method><path>%s</path>' % ppath.pattern)
            if pfunc.__doc__:
                ret.append('<doc>%s</doc>' % pfunc.__doc__)
            ret.append('<params>')
            if pargs:
                for p in pargs:
                    ret.append('<param>%s</param>' % p)

            ret.append('</params></method>')

        ret.append('</api>')
        return ('').join(ret)

    usage.path = '/$'
    usage.mime = 'text/xml'
    usage.serve = True