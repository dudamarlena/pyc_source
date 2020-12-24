# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/makina/pasteStage/pasteFunBot/Paste-1.7.2-py2.6.egg/paste/auth/open_id.py
# Compiled at: 2009-07-20 09:44:04
"""
OpenID Authentication (Consumer)

OpenID is a distributed authentication system for single sign-on originally
developed at/for LiveJournal.com.

    http://openid.net/

URL. You can have multiple identities in the same way you can have multiple
URLs. All OpenID does is provide a way to prove that you own a URL (identity).
And it does this without passing around your password, your email address, or
anything you don't want it to. There's no profile exchange component at all:
your profiile is your identity URL, but recipients of your identity can then
learn more about you from any public, semantically interesting documents
linked thereunder (FOAF, RSS, Atom, vCARD, etc.).

``Note``: paste.auth.openid requires installation of the Python-OpenID
libraries::

    http://www.openidenabled.com/

This module is based highly off the consumer.py that Python OpenID comes with.

Using the OpenID Middleware
===========================

Using the OpenID middleware is fairly easy, the most minimal example using the
basic login form thats included::

    # Add to your wsgi app creation
    from paste.auth import open_id

    wsgi_app = open_id.middleware(wsgi_app, '/somewhere/to/store/openid/data')

You will now have the OpenID form available at /oid on your site. Logging in will
verify that the login worked.

A more complete login should involve having the OpenID middleware load your own
login page after verifying the OpenID URL so that you can retain the login
information in your webapp (session, cookies, etc.)::

    wsgi_app = open_id.middleware(wsgi_app, '/somewhere/to/store/openid/data',
                                  login_redirect='/your/login/code')

Your login code should then be configured to retrieve 'paste.auth.open_id' for
the users OpenID URL. If this key does not exist, the user has not logged in.

Once the login is retrieved, it should be saved in your webapp, and the user
should be redirected to wherever they would normally go after a successful
login.
"""
__all__ = [
 'AuthOpenIDHandler']
import cgi, urlparse, re, paste.request
from paste import httpexceptions

def quoteattr(s):
    qs = cgi.escape(s, 1)
    return '"%s"' % (qs,)


from openid.store import filestore
from openid.consumer import consumer
from openid.oidutil import appendArgs

class AuthOpenIDHandler(object):
    """
    This middleware implements OpenID Consumer behavior to authenticate a
    URL against an OpenID Server.
    """

    def __init__(self, app, data_store_path, auth_prefix='/oid', login_redirect=None, catch_401=False, url_to_username=None):
        """
        Initialize the OpenID middleware

        ``app``
            Your WSGI app to call
            
        ``data_store_path``
            Directory to store crypto data in for use with OpenID servers.
            
        ``auth_prefix``
            Location for authentication process/verification
            
        ``login_redirect``
            Location to load after successful process of login
            
        ``catch_401``
            If true, then any 401 responses will turn into open ID login
            requirements.
            
        ``url_to_username``
            A function called like ``url_to_username(environ, url)``, which should
            return a string username.  If not given, the URL will be the username.
        """
        store = filestore.FileOpenIDStore(data_store_path)
        self.oidconsumer = consumer.OpenIDConsumer(store)
        self.app = app
        self.auth_prefix = auth_prefix
        self.data_store_path = data_store_path
        self.login_redirect = login_redirect
        self.catch_401 = catch_401
        self.url_to_username = url_to_username

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.auth_prefix):
            request = dict(environ=environ, start=start_response, body=[])
            request['base_url'] = paste.request.construct_url(environ, with_path_info=False, with_query_string=False)
            path = re.sub(self.auth_prefix, '', environ['PATH_INFO'])
            request['parsed_uri'] = urlparse.urlparse(path)
            request['query'] = dict(paste.request.parse_querystring(environ))
            path = request['parsed_uri'][2]
            if path == '/' or not path:
                return self.render(request)
            if path == '/verify':
                return self.do_verify(request)
            if path == '/process':
                return self.do_process(request)
            return self.not_found(request)
        else:
            if self.catch_401:
                return self.catch_401_app_call(environ, start_response)
            else:
                return self.app(environ, start_response)

    def catch_401_app_call(self, environ, start_response):
        """
        Call the application, and redirect if the app returns a 401 response
        """
        was_401 = []

        def replacement_start_response(status, headers, exc_info=None):
            if int(status.split(None, 1)) == 401:
                was_401.append(1)

                def dummy_writer(v):
                    pass

                return dummy_writer
            else:
                return start_response(status, headers, exc_info)
                return

        app_iter = self.app(environ, replacement_start_response)
        if was_401:
            try:
                list(app_iter)
            finally:
                if hasattr(app_iter, 'close'):
                    app_iter.close()

            redir_url = paste.request.construct_url(environ, with_path_info=False, with_query_string=False)
            exc = httpexceptions.HTTPTemporaryRedirect(redir_url)
            return exc.wsgi_application(environ, start_response)
        else:
            return app_iter
            return

    def do_verify(self, request):
        """Process the form submission, initating OpenID verification.
        """
        openid_url = request['query'].get('openid_url')
        if not openid_url:
            return self.render(request, 'Enter an identity URL to verify.', css_class='error', form_contents=openid_url)
        oidconsumer = self.oidconsumer
        (status, info) = oidconsumer.beginAuth(openid_url)
        if status in [consumer.HTTP_FAILURE, consumer.PARSE_ERROR]:
            if status == consumer.HTTP_FAILURE:
                fmt = 'Failed to retrieve <q>%s</q>'
            else:
                fmt = 'Could not find OpenID information in <q>%s</q>'
            message = fmt % (cgi.escape(openid_url),)
            return self.render(request, message, css_class='error', form_contents=openid_url)
        if status == consumer.SUCCESS:
            return_to = self.build_url(request, 'process', token=info.token)
            redirect_url = oidconsumer.constructRedirect(info, return_to, trust_root=request['base_url'])
            return self.redirect(request, redirect_url)
        assert False, 'Not reached'

    def do_process(self, request):
        """Handle the redirect from the OpenID server.
        """
        oidconsumer = self.oidconsumer
        token = request['query'].get('token', '')
        (status, info) = oidconsumer.completeAuth(token, request['query'])
        css_class = 'error'
        openid_url = None
        if status == consumer.FAILURE and info:
            openid_url = info
            fmt = 'Verification of %s failed.'
            message = fmt % (cgi.escape(openid_url),)
        elif status == consumer.SUCCESS:
            css_class = 'alert'
            if info:
                openid_url = info
                if self.url_to_username:
                    username = self.url_to_username(request['environ'], openid_url)
                else:
                    username = openid_url
                if 'paste.auth_tkt.set_user' in request['environ']:
                    request['environ']['paste.auth_tkt.set_user'](username)
                if not self.login_redirect:
                    fmt = 'If you had supplied a login redirect path, you would have been redirected there.  You have successfully verified %s as your identity.'
                    message = fmt % (cgi.escape(openid_url),)
                else:
                    request['environ']['paste.auth.open_id'] = openid_url
                    request['environ']['PATH_INFO'] = self.login_redirect
                    return self.app(request['environ'], request['start'])
            else:
                message = 'Verification cancelled'
        else:
            message = 'Verification failed.'
        return self.render(request, message, css_class, openid_url)

    def build_url(self, request, action, **query):
        """Build a URL relative to the server base_url, with the given
        query parameters added."""
        base = urlparse.urljoin(request['base_url'], self.auth_prefix + '/' + action)
        return appendArgs(base, query)

    def redirect(self, request, redirect_url):
        """Send a redirect response to the given URL to the browser."""
        response_headers = [
         ('Content-type', 'text/plain'),
         (
          'Location', redirect_url)]
        request['start']('302 REDIRECT', response_headers)
        return ['Redirecting to %s' % redirect_url]

    def not_found(self, request):
        """Render a page with a 404 return code and a message."""
        fmt = 'The path <q>%s</q> was not understood by this server.'
        msg = fmt % (request['parsed_uri'],)
        openid_url = request['query'].get('openid_url')
        return self.render(request, msg, 'error', openid_url, status='404 Not Found')

    def render(self, request, message=None, css_class='alert', form_contents=None, status='200 OK', title='Python OpenID Consumer'):
        """Render a page."""
        response_headers = [
         ('Content-type', 'text/html')]
        request['start'](str(status), response_headers)
        self.page_header(request, title)
        if message:
            request['body'].append("<div class='%s'>" % (css_class,))
            request['body'].append(message)
            request['body'].append('</div>')
        self.page_footer(request, form_contents)
        return request['body']

    def page_header(self, request, title):
        """Render the page header"""
        request['body'].append('<html>\n  <head><title>%s</title></head>\n  <style type="text/css">\n      * {\n        font-family: verdana,sans-serif;\n      }\n      body {\n        width: 50em;\n        margin: 1em;\n      }\n      div {\n        padding: .5em;\n      }\n      table {\n        margin: none;\n        padding: none;\n      }\n      .alert {\n        border: 1px solid #e7dc2b;\n        background: #fff888;\n      }\n      .error {\n        border: 1px solid #ff0000;\n        background: #ffaaaa;\n      }\n      #verify-form {\n        border: 1px solid #777777;\n        background: #dddddd;\n        margin-top: 1em;\n        padding-bottom: 0em;\n      }\n  </style>\n  <body>\n    <h1>%s</h1>\n    <p>\n      This example consumer uses the <a\n      href="http://openid.schtuff.com/">Python OpenID</a> library. It\n      just verifies that the URL that you enter is your identity URL.\n    </p>\n' % (title, title))

    def page_footer(self, request, form_contents):
        """Render the page footer"""
        if not form_contents:
            form_contents = ''
        request['body'].append('    <div id="verify-form">\n      <form method="get" action=%s>\n        Identity&nbsp;URL:\n        <input type="text" name="openid_url" value=%s />\n        <input type="submit" value="Verify" />\n      </form>\n    </div>\n  </body>\n</html>\n' % (quoteattr(self.build_url(request, 'verify')), quoteattr(form_contents)))


middleware = AuthOpenIDHandler

def make_open_id_middleware(app, global_conf, data_store_path, auth_prefix='/oid', login_redirect=None, catch_401=False, url_to_username=None, apply_auth_tkt=False, auth_tkt_logout_path=None):
    from paste.deploy.converters import asbool
    from paste.util import import_string
    catch_401 = asbool(catch_401)
    if url_to_username and isinstance(url_to_username, basestring):
        url_to_username = import_string.eval_import(url_to_username)
    apply_auth_tkt = asbool(apply_auth_tkt)
    new_app = AuthOpenIDHandler(app, data_store_path=data_store_path, auth_prefix=auth_prefix, login_redirect=login_redirect, catch_401=catch_401, url_to_username=url_to_username or None)
    if apply_auth_tkt:
        from paste.auth import auth_tkt
        new_app = auth_tkt.make_auth_tkt_middleware(new_app, global_conf, logout_path=auth_tkt_logout_path)
    return new_app