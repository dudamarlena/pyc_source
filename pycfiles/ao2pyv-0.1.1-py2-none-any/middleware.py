# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ao/social/middleware.py
# Compiled at: 2010-04-14 12:03:38
import webob, webob.exc
from ao import social
from oauth import oauth

class AuthMiddleware(object):
    """Authentication and authorization middleware."""
    _popup_html = '\n<!doctype html>\n<html lang="en">\n  <head>\n    <meta charset="utf-8"/>\n    <title></title>\n    <script>\n      try {\n        %(postlogin)s;\n      } catch (e) {};\n      close();\n    </script>\n  </head>\n</html>'

    def __init__(self, app, config={}):
        """Configure the middleware."""
        self._app = app
        self._user_class = self._import_user(config['user_class'])
        self._login_path = config['login_path']
        self._clients = {}
        for method in ('facebook', 'google', 'twitter', 'linkedin'):
            if method in config:
                self._clients[method] = social.registerClient(method, config[method])

    def __call__(self, environ, start_response):
        """Put the user object into the WSGI environment."""
        request = webob.Request(environ, charset='utf-8')
        environ['ao.social.login'] = self._build_absolute_uri(environ, self._login_path)
        session = environ['beaker.session']
        environ['ao.social.user'] = None
        if 'ao.social.user' in session:
            environ['ao.social.user'] = self._user_class.get_user(session['ao.social.user'])
        for method in ('facebook', 'twitter', 'google', 'linkedin'):
            if request.path_info == self._login_path % method:
                response = self._handle_user(request, method, 'login')
                if response is not None:
                    return response(environ, start_response)

        return self._app(environ, start_response)

    def _build_absolute_uri(environ, path='/'):
        """Constructs an absolute URI."""
        root = '%s://%s' % (environ['wsgi.url_scheme'], environ['HTTP_HOST'])
        path = not path.startswith('/') and environ['PATH_INFO'] + path or path
        return root + path

    _build_absolute_uri = staticmethod(_build_absolute_uri)

    def _import_user(cls):
        """Import the provided `User` class."""
        (modstr, _, cls) = cls.rpartition('.')
        mod = __import__(modstr)
        for sub in modstr.split('.')[1:]:
            mod = getattr(mod, sub)

        return getattr(mod, cls)

    _import_user = staticmethod(_import_user)

    def _login_user(self, request, method, credentials):
        """Looks up the user and initiates a session."""
        id = str(credentials['id'])
        uid = (':').join((method, id))
        session = request.environ['beaker.session']
        user = self._user_class.lookup_user(uid)
        if method == 'facebook':
            info = [
             'name', 'first_name', 'last_name', 'email', 'pic_square']
            data = self._clients[method].users.getInfo(id, info)[0]
            user.update_details({'name': data['name'], 
               'first_name': data['first_name'], 
               'last_name': data['last_name'], 
               'avatar': data['pic_square'], 
               'email': data['email']})
            user.set_token('facebook', {'uid': id, 
               'token': credentials['token'], 
               'secret': credentials['secret']})
        elif method == 'twitter':
            (first_name, _, last_name) = credentials['name'].partition(' ')
            user.update_details({'name': credentials['name'], 
               'first_name': first_name, 
               'last_name': last_name, 
               'avatar': credentials['profile_image_url']})
            user.set_token('twitter', {'uid': id, 
               'token': credentials['token'], 
               'secret': credentials['secret']})
        elif method == 'google':
            user.update_details({'name': '%s %s' % (credentials['first_name'],
                      credentials['last_name']), 
               'first_name': credentials['first_name'], 
               'last_name': credentials['last_name'], 
               'email': credentials['email']})
            user.set_token('google', {'uid': id})
        elif method == 'linkedin':
            user.update_details({'name': '%s %s' % (credentials['first_name'],
                      credentials['last_name']), 
               'first_name': credentials['first_name'], 
               'last_name': credentials['last_name']})
            user.set_token('linkedin', {'uid': id, 
               'token': credentials['token'], 
               'secret': credentials['secret']})
        postlogin = ''
        if 'postlogin' in session:
            postlogin = session['postlogin']
            del session['postlogin']
        body = self._popup_html % {'postlogin': postlogin}
        response = webob.Response(body=body)
        session['ao.social.user'] = str(user.get_key())
        session.save()
        user.save_user()
        return response

    def _connect_user(self, request, method, credentials):
        """Connects the account to the current user."""
        id = str(credentials['id'])
        user = request.environ['ao.social.user']
        session = request.environ['beaker.session']
        if method == 'facebook':
            user.set_token('facebook', {'uid': id, 
               'token': credentials['token'], 
               'secret': credentials['secret']})
        elif method == 'twitter':
            user.set_token('twitter', {'uid': id, 
               'token': credentials['token'], 
               'secret': credentials['secret']})
        elif method == 'google':
            user.set_token('google', {'uid': id})
        elif method == 'linkedin':
            user.set_token('linkedin', {'uid': id, 
               'token': credentials['token'], 
               'secret': credentials['secret']})
        postlogin = ''
        if 'postlogin' in session:
            postlogin = session['postlogin']
            del session['postlogin']
        body = self._popup_html % {'postlogin': postlogin}
        response = webob.Response(body=body)
        user.save_user()
        return response

    def _handle_user(self, request, method, mode='login'):
        """Handles authentication for the user.

        If `mode` is set to 'connect', it will assume that a user is already
        logged in and connects the new account to the logged in user.
        Otherwise, simply logs in the user.

        """
        user = request.environ['ao.social.user']
        session = request.environ['beaker.session']
        if 'postlogin' in request.GET:
            session['postlogin'] = request.GET['postlogin']
            session.save()
        if method == 'facebook':
            facebook_user = self._clients[method].get_user(request)
            if facebook_user is None:
                raise social.Unauthorized('Facebook Connect authentication failed.')
            if user is None:
                return self._login_user(request, method, facebook_user)
            return self._connect_user(request, method, facebook_user)
        if method == 'twitter':
            keys = ('oauth_token', 'oauth_verifier')
            if not all((key in request.GET for key in keys)):
                auth_url = self._login_path % method
                auth_url = self._clients[method].get_authorization_url(self._build_absolute_uri(request.environ, auth_url))
                return webob.Response(status=302, headers={'Location': auth_url})
            try:
                twitter_user = self._clients[method].get_user_info(request.GET['oauth_token'], request.GET['oauth_verifier'])
                if user is None:
                    return self._login_user(request, method, twitter_user)
                return self._connect_user(request, method, twitter_user)
            except oauth.OAuthError:
                raise social.Unauthorized('Twitter OAuth authentication failed.')

        if method == 'google':
            if len(request.GET) < 2:
                return webob.exc.HTTPTemporaryRedirect(location=self._clients[method].redirect())
            callback = self._build_absolute_uri(request.environ, self._login_path % method)
            google_user = self._clients[method].get_user(request.GET, callback)
            if google_user is None:
                raise social.Unauthorized('Google OpenID authentication failed.')
            if user is None:
                return self._login_user(request, method, google_user)
            return self._connect_user(request, method, google_user)
        if method == 'linkedin':
            keys = ('oauth_token', 'oauth_verifier')
            if not all((key in request.GET for key in keys)):
                auth_url = self._login_path % method
                auth_url = self._clients[method].get_authorization_url(self._build_absolute_uri(request.environ, auth_url))
                return webob.Response(status=302, headers={'Location': auth_url})
            try:
                linkedin_user = self._clients[method].get_user_info(request.GET['oauth_token'], request.GET['oauth_verifier'])
                if user is None:
                    return self._login_user(request, method, linkedin_user)
                return self._connect_user(request, method, linkedin_user)
            except oauth.OAuthError:
                raise social.Unauthorized('LinkedIn OAuth authentication failed.')

        return