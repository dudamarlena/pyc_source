# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/pyramid_oauth2_provider/authentication.py
# Compiled at: 2013-02-13 23:59:52
import logging
from zope.interface import implementer
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPUnauthorized
from .models import Oauth2Token
from .models import DBSession as db
from .errors import InvalidToken
from .errors import InvalidRequest
from .util import getClientCredentials
log = logging.getLogger('pyramid_oauth2_provider.authentication')

@implementer(IAuthenticationPolicy)
class OauthAuthenticationPolicy(CallbackAuthenticationPolicy):

    def _isOauth(self, request):
        return bool(getClientCredentials(request))

    def _get_auth_token(self, request):
        token_type, token = getClientCredentials(request)
        if token_type != 'bearer':
            return None
        else:
            auth_token = db.query(Oauth2Token).filter_by(access_token=token).first()
            if not auth_token:
                raise HTTPBadRequest(InvalidRequest())
            if auth_token.isRevoked():
                raise HTTPUnauthorized(InvalidToken())
            return auth_token

    def unauthenticated_userid(self, request):
        auth_token = self._get_auth_token(request)
        if not auth_token:
            return None
        else:
            return auth_token.user_id

    def remember(self, request, principal, **kw):
        """
        I don't think there is anything to do for an oauth request here.
        """
        pass

    def forget(self, request):
        auth_token = self._get_auth_token(request)
        if not auth_token:
            return
        else:
            auth_token.revoke()
            return


@implementer(IAuthenticationPolicy)
class OauthTktAuthenticationPolicy(OauthAuthenticationPolicy, AuthTktAuthenticationPolicy):

    def __init__(self, *args, **kwargs):
        OauthAuthenticationPolicy.__init__(self)
        AuthTktAuthenticationPolicy.__init__(self, *args, **kwargs)

    def unauthenticated_userid(self, request):
        if self._isOauth(request):
            return OauthAuthenticationPolicy.unauthenticated_userid(self, request)
        else:
            return AuthTktAuthenticationPolicy.unauthenticated_userid(self, request)

    def remember(self, request, principal, **kw):
        if self._isOauth(request):
            return OauthAuthenticationPolicy.remember(self, request, principal, **kw)
        else:
            return AuthTktAuthenticationPolicy.remember(self, request, principal, **kw)

    def forget(self, request):
        if self._isOauth(request):
            return OauthAuthenticationPolicy.forget(self, request)
        else:
            return AuthTktAuthenticationPolicy.forget(self, request)