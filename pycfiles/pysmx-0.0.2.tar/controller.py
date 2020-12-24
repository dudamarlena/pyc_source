# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/controller.py
# Compiled at: 2010-05-30 13:30:03
from traceback import format_exc
import logging
from werkzeug.routing import RequestRedirect
from werkzeug.exceptions import HTTPException, NotFound, InternalServerError, MethodNotAllowed
from pysmvt import settings, session, user, rg, ag, _getview
from pysmvt.exceptions import ForwardException, ProgrammingError, Redirect, ExceptionToClient
from pysmvt.mail import mail_programmers
from pysmvt.utils import randchars, pprint, werkzeug_multi_dict_conv
from pysmvt.utils.html import escape
from pysmvt.wrappers import Request, Response
log = logging.getLogger(__name__)

class Controller(object):
    """
    The controller is responsible for handling the request and responding
    appropriately
    """

    def __init__(self, settings):
        self.settings = settings

    def dispatch_request(self, environ, start_response):
        self._wsgi_request_setup(environ)
        try:
            if rg.request.path == '/[[__handle_callable__]]':
                response = self._handle_callable()
            else:
                response = self._error_documents_handler(environ)
            self._wsgi_request_cleanup()
            return response(environ, start_response)
        finally:
            pass

    def _handle_callable(self):
        from pysmvt.view import HtmlPageViewBase
        r = Response()
        respview = HtmlPageViewBase('', '', {})
        r.data = unicode(rg.environ['pysmvt.callable']())
        return r

    def _wsgi_request_setup(self, environ):
        rg.ident = randchars()
        rg.environ = environ
        request = Request(environ)

    def _wsgi_request_cleanup(self):
        session.save()

    def _response_cleanup(self):
        try:
            del rg.respview
        except AttributeError:
            pass

        if rg.environ.get('sqlalchemy.sess', None):
            try:
                rg.environ['sqlalchemy.sess'].rollback()
            except:
                pass

        return

    def _error_documents_handler(self, environ):
        response = orig_resp = self._exception_handling('client', environ)

        def get_status_code(response):
            if isinstance(response, HTTPException):
                return response.code
            else:
                return response.status_code

        code = get_status_code(response)
        if code in settings.error_docs and not isinstance(response, ExceptionToClient):
            handling_endpoint = settings.error_docs.get(code)
            log.debug('error docs: handling code %d with %s' % (code, handling_endpoint))
            environ['pysmvt.controller.error_docs_handler.response'] = response
            new_response = self._exception_handling('error docs', endpoint=handling_endpoint)
            if get_status_code(new_response) == 200:
                try:
                    new_response.status_code = code
                except AttributeError, e:
                    if "object has no attribute 'status_code'" not in str(e):
                        raise
                    new_response.code = code
                else:
                    response = new_response
            else:
                log.error('error docs: encountered non-200 status code response (%d) when trying to handle with %s' % (
                 get_status_code(new_response), handling_endpoint))
        if isinstance(response, HTTPException) and not isinstance(response, (Redirect, ExceptionToClient)):
            messages = user.get_messages()
            if messages:
                msg_html = [
                 '<h2>Error Details:</h2><ul>']
                for msg in messages:
                    msg_html.append('<li>(%s) %s</li>' % (msg.severity, msg.text))

                msg_html.append('</ul>')
                response.description = str(response.description) + ('\n').join(msg_html)
        return response

    def _exception_handling(self, called_from, environ=None, endpoint=None, args={}):

        def exception_info():
            retval = '\n== TRACE ==\n\n%s' % format_exc()
            retval += '\n\n== ENVIRON ==\n\n%s' % pprint(rg.environ, 4, True)
            retval += '\n\n== POST ==\n\n%s\n\n' % pprint(werkzeug_multi_dict_conv(rg.request.form), 4, True)
            return retval

        try:
            if environ:
                (endpoint, args) = self._endpoint_args_from_env(environ)
            response = self._inner_requests_wrapper(endpoint, args, called_from)
        except HTTPException, e:
            log.debug('exception handling caught HTTPException "%s", sending as response' % e.__class__.__name__)
            response = e
        except Exception, e:
            if settings.exceptions.log:
                log.error('exception encountered: %s' % exception_info())
            if settings.exceptions.email:
                try:
                    mail_programmers('exception encountered', exception_info())
                except Exception, e:
                    log.exception('exception when trying to email exception')

            if settings.exceptions.to_client:
                response = ExceptionToClient()
                response.description = '<pre>%s</pre>' % escape(exception_info())
            elif settings.exceptions.hide:
                response = InternalServerError()
            else:
                raise

        return response

    def _endpoint_args_from_env(self, environ):
        try:
            urls = rg.urladapter = ag.route_map.bind_to_environ(environ)
            endpoint = None
            return urls.match()
        except (NotFound, MethodNotAllowed, RequestRedirect):
            if endpoint is None:
                log.debug('URL (%s) generated HTTPException' % environ['PATH_INFO'])
            raise

        return

    def _inner_requests_wrapper(self, endpoint, args, called_from):
        rg.forward_queue = [(endpoint, args)]
        while True:
            try:
                try:
                    (endpoint, args) = rg.forward_queue[(-1)]
                    response = _getview(endpoint, args, called_from)
                    if not isinstance(response, Response):
                        raise ProgrammingError('view %s did not return a response object' % endpoint)
                    return response
                except ForwardException:
                    called_from = 'forward'

            finally:
                self._response_cleanup()

    def __call__(self, environ, start_response):
        """Just forward a WSGI call to the first internal middleware."""
        return self.dispatch_request(environ, start_response)