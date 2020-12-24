# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/cgitb_catcher.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = '\nWSGI middleware\n\nCaptures any exceptions and prints a pretty report.  See the `cgitb\ndocumentation <http://python.org/doc/current/lib/module-cgitb.html>`_\nfor more.\n'
import cgitb
from cStringIO import StringIO
import sys
from paste.util import converters

class NoDefault(object):
    pass


class CgitbMiddleware(object):

    def __init__(self, app, global_conf=None, display=NoDefault, logdir=None, context=5, format='html'):
        self.app = app
        if global_conf is None:
            global_conf = {}
        if display is NoDefault:
            display = global_conf.get('debug')
        if isinstance(display, basestring):
            display = converters.asbool(display)
        self.display = display
        self.logdir = logdir
        self.context = int(context)
        self.format = format
        return

    def __call__(self, environ, start_response):
        try:
            app_iter = self.app(environ, start_response)
            return self.catching_iter(app_iter, environ)
        except:
            exc_info = sys.exc_info()
            start_response('500 Internal Server Error', [
             ('content-type', 'text/html')], exc_info)
            response = self.exception_handler(exc_info, environ)
            return [
             response]

    def catching_iter(self, app_iter, environ):
        if not app_iter:
            raise StopIteration
        error_on_close = False
        try:
            for v in app_iter:
                yield v

            if hasattr(app_iter, 'close'):
                error_on_close = True
                app_iter.close()
        except:
            response = self.exception_handler(sys.exc_info(), environ)
            if not error_on_close and hasattr(app_iter, 'close'):
                try:
                    app_iter.close()
                except:
                    close_response = self.exception_handler(sys.exc_info(), environ)
                    response += '<hr noshade>Error in .close():<br>%s' % close_response

            yield response

    def exception_handler(self, exc_info, environ):
        dummy_file = StringIO()
        hook = cgitb.Hook(file=dummy_file, display=self.display, logdir=self.logdir, context=self.context, format=self.format)
        hook(*exc_info)
        return dummy_file.getvalue()


def make_cgitb_middleware(app, global_conf, display=NoDefault, logdir=None, context=5, format='html'):
    """
    Wraps the application in the ``cgitb`` (standard library)
    error catcher.
        
      display:
        If true (or debug is set in the global configuration)
        then the traceback will be displayed in the browser

      logdir:
        Writes logs of all errors in that directory

      context:
        Number of lines of context to show around each line of
        source code
    """
    from paste.deploy.converters import asbool
    if display is not NoDefault:
        display = asbool(display)
    if 'debug' in global_conf:
        global_conf['debug'] = asbool(global_conf['debug'])
    return CgitbMiddleware(app, global_conf=global_conf, display=display, logdir=logdir, context=context, format=format)