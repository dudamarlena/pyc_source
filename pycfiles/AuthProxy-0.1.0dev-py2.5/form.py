# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/lib/authkit_adapter/authenticate/form.py
# Compiled at: 2007-12-04 10:18:33
"""Form and cookie based authentication middleware

As with all the other AuthKit middleware, this middleware is described in
detail in the AuthKit manual and should be used via the
``authkit.authenticate.middleware`` function.

The option form.status can be set to "200 OK" if the Pylons error document
middleware is intercepting the 401 response and just showing the standard 401
error document. This will not happen in recent versions of Pylons (0.9.6)
because this middleware sets the environ['pylons.error_call'] key so that the
error documents middleware doesn't intercept the response.
"""
from paste.auth.form import AuthFormHandler
from paste.request import construct_url, parse_formvars
from authproxy.lib.authkit_adapter.authenticate import get_template, valid_password, get_authenticate_function, strip_base, RequireEnvironKey, AuthKitAuthHandler
from authkit.authenticate.multi import MultiHandler, status_checker
import logging
log = logging.getLogger('authkit.authenticate.form')

def template():
    return '<html>\n  <head><title>Please Sign In</title></head>\n  <body>\n    <h1>Please Sign In</h1>\n    <form action="%s" method="post">\n      <dl>\n        <dt>Username:</dt>\n        <dd><input type="text" name="username"></dd>\n        <dt>Password:</dt>\n        <dd><input type="password" name="password"></dd>\n      </dl>\n      <input type="submit" name="authform" value="Sign In" />\n    </form>\n  </body>\n</html>\n'


class FormAuthHandler(AuthKitAuthHandler, AuthFormHandler):

    def __init__(self, app, charset=None, status='401 Unauthorized', **p):
        AuthFormHandler.__init__(self, app, **p)
        self.status = status
        if charset is None:
            self.charset = ''
        else:
            self.charset = '; charset=' + charset
        return

    def on_authorized(self, environ, start_response):
        environ['paste.auth_tkt.set_user'](userid=environ['REMOTE_USER'])
        return self.application(environ, start_response)

    def __call__(self, environ, start_response):
        username = environ.get('REMOTE_USER', '')
        if 'POST' == environ['REQUEST_METHOD']:
            formvars = parse_formvars(environ, include_get_vars=False)
            username = formvars.get('username')
            password = formvars.get('password')
            if username and password:
                if self.authfunc(environ, username, password):
                    environ['AUTH_TYPE'] = 'form'
                    environ['REMOTE_USER'] = username
                    environ['REQUEST_METHOD'] = 'GET'
                    environ['CONTENT_LENGTH'] = ''
                    environ['CONTENT_TYPE'] = ''
                    del environ['paste.parsed_formvars']
                    return self.on_authorized(environ, start_response)
        action = construct_url(environ)
        log.debug('Form action is: %s', action)
        content = self.template() % action
        environ['pylons.error_call'] = 'authkit'
        start_response(self.status, [('Content-Type', 'text/html' + self.charset),
         (
          'Content-Length', str(len(content)))])
        return [content]


def load_form_config(app, auth_conf, app_conf=None, global_conf=None, prefix='authkit.method.form'):
    app = RequireEnvironKey(app, 'paste.auth_tkt.set_user', missing_error='Missing the key %(key)s from the environ. Have you added the cookie method after the form method?')
    template_conf = strip_base(auth_conf, 'template.')
    if template_conf:
        template_ = get_template(template_conf, prefix=prefix + 'template.')
    else:
        template_ = template
    authenticate_conf = strip_base(auth_conf, 'authenticate.')
    (app, authfunc, users) = get_authenticate_function(app, authenticate_conf, prefix=prefix + 'authenticate.', format='basic')
    charset = auth_conf.get('charset')
    return (app, {'authfunc': authfunc, 'template': template_, 'charset': charset}, None)


def make_form_handler(app, auth_conf, app_conf=None, global_conf=None, prefix='authkit.method.form'):
    (app, auth_handler_params, user_setter_params) = load_form_config(app, auth_conf, app_conf=None, global_conf=None, prefix='authkit.method.form')
    app = MultiHandler(app)
    app.add_method('form', FormAuthHandler, authfunc=auth_handler_params['authfunc'], template=auth_handler_params['template'], charset=auth_handler_params['charset'])
    app.add_checker('form', status_checker)
    return app


Form = FormAuthHandler