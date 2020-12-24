# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tg/ext/repoze/who/middleware.py
# Compiled at: 2008-06-04 11:09:41


class SQLAuthenticatorPlugin:

    def __init__(self, user_class, session_factory, user_criterion, user_id_col):
        self.user_class = user_class
        self.user_criterion = user_criterion
        self.session_factory = session_factory
        self.user_id_col = user_id_col

    def authenticate(self, environ, identity):
        if 'login' not in identity:
            return
        session = self.session_factory()
        query = session.query(self.user_class)
        query = query.filter(self.user_criterion == identity['login'])
        user = query.first()
        if user:
            if user.validate_password(identity['password']):
                return getattr(user, self.user_id_col)
        return


class SQLMetadataProviderPlugin:

    def __init__(self, user_class, session_factory, criterion_token):
        self.session_factory = session_factory
        self.user_class = user_class
        self.criterion_token = criterion_token

    def add_metadata(self, environ, identity):
        session = self.session_factory()
        query = session.query(self.user_class)
        id_ = identity['repoze.who.userid']
        user = query.get(id_)
        identity['user'] = user
        if user:
            identity['groups'] = [ group.group_name for group in user.groups ]
            identity['permissions'] = [ permission.permission_name for permission in user.permissions
                                      ]
        else:
            identity['groups'] = list()
            identity['permissions'] = list()


def make_who_middleware(app, config, user_class, user_criterion, user_id_col, session_factory):
    """A sample configuration of repoze.who authentication for TurboGears 2
    """
    sqlauth = SQLAuthenticatorPlugin(user_class, session_factory, user_criterion, user_id_col)
    allmd = SQLMetadataProviderPlugin(user_class, session_factory, user_criterion)
    from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
    from repoze.who.plugins.form import RedirectingFormPlugin
    cookie = AuthTktCookiePlugin('secret', 'authtkt')
    form = RedirectingFormPlugin('/login', '/login_handler', '/logout_handler', rememberer_name='cookie')
    identifiers = [
     (
      'form', form), ('cookie', cookie)]
    authenticators = [('sqlauth', sqlauth)]
    challengers = [('form', form)]
    mdproviders = [('all', allmd)]
    from repoze.who.classifiers import default_challenge_decider
    from repoze.who.classifiers import default_request_classifier
    log_stream = None
    import os
    if os.environ.get('WHO_LOG'):
        import sys
        log_stream = sys.stdout
    from repoze.who.middleware import PluggableAuthenticationMiddleware
    import logging
    middleware = PluggableAuthenticationMiddleware(app, identifiers, authenticators, challengers, mdproviders, default_request_classifier, default_challenge_decider, log_stream=log_stream, log_level=logging.DEBUG)
    return middleware