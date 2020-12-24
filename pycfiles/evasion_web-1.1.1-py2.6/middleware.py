# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\evasion\web\middleware.py
# Compiled at: 2010-07-09 08:13:43
"""
"""
import sys, logging, traceback, simplejson
from weberror.errormiddleware import Supplement
from weberror.errormiddleware import ErrorMiddleware
from weberror.errormiddleware import ResponseStartChecker

def get_log():
    return logging.getLogger('newman.accountservice.middleware')


class ErrorHandler(ErrorMiddleware):
    """Based on weberror.errormiddleware:ErrorMiddleware
    
    Override the error handler and implement a different exception
    handler, to return a JSON encoded dict for newman-client to handle
    more easily.
    
    """

    def __init__(self, *args, **kwargs):
        ErrorMiddleware.__init__(self, *args, **kwargs)
        self.log = logging.getLogger('newman.accountservice.middleware.ErrorHandler')
        self._logTheTraceback = False

    def showTracebacks(self):
        """ Enable the logging of tracebacks to aid internal error debugging. """
        self._logTheTraceback = True

    def __call__(self, environ, start_response):
        """
        The WSGI application interface.
        """
        if environ.get('paste.throw_errors'):
            return self.application(environ, start_response)
        else:
            environ['paste.throw_errors'] = True
            try:
                __traceback_supplement__ = (Supplement, self, environ)
                sr_checker = ResponseStartChecker(start_response)
                app_iter = self.application(environ, sr_checker)
                return self.make_catching_iter(app_iter, environ, sr_checker)
            except:
                exc_info = sys.exc_info()
                try:
                    response = self.exception_handler(start_response, exc_info, environ)
                    if isinstance(response, unicode):
                        response = response.encode('utf8')
                    return [
                     response]
                finally:
                    exc_info = None

            return

    def exception_handler(self, start_response, exc_info, environ):
        """Override base class version to return JSON instead.
        
        The HTTP status code will also be set 
        
        :returns: JSON encoded dict(
                exception='a.b.c.Exception', 
                value='exception message'
            )
        
        """
        returned_status = '500 Internal Server Error'
        self.log.error('exception_handler exc_info:\n%s\n' % str(exc_info))
        (exc_type, exc_value, trace_back) = exc_info
        if self._logTheTraceback:
            self.log.warn('** TRACEBACK DEBUG\n%s\n' % ('').join(traceback.format_tb(trace_back)))
        try:
            returned_status = '400 Bad Request'
            exception_name = '%s.%s' % (exc_type.__module__, exc_type.__name__)
            returned = dict(exception=exception_name, value=str(exc_value))
        except:
            self.log.exception('exception_handler failed to handle exception! ')
            returned = dict(exception='SystemError', value='Internal Server Exception :(')

        start_response(returned_status, [
         ('content-type', 'text/html; charset=utf8')], exc_info)
        return simplejson.dumps(returned)


def rest_errorhandling_setup(app, global_conf, app_conf, middleware_list):
    """Configure the custom error handling.
    """
    get_log().info('rest_errorhandling_setup: setting up special REST error middleware.')
    app = ErrorHandler(app)
    debug = global_conf.get('debug', 'false')
    if debug == 'true':
        get_log().warn('global_conf: [DEFAULT] debug = true enabling traceback printing.')
        app.showTracebacks()
    return app