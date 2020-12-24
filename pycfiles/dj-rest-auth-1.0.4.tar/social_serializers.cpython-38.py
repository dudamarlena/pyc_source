# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/circleci/project/dj_rest_auth/social_serializers.py
# Compiled at: 2020-03-01 00:55:21
# Size of source mod 2**32: 2999 bytes
from django.conf import settings
from django.http import HttpRequest
from rest_framework import serializers
if 'allauth.socialaccount' in settings.INSTALLED_APPS:
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import SocialToken
    from allauth.socialaccount.providers.oauth.client import OAuthError
    from dj_rest_auth.registration.serializers import SocialConnectMixin

class TwitterLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    token_secret = serializers.CharField()

    def _get_request(self):
        request = self.context.get('request')
        if not isinstance(request, HttpRequest):
            request = request._request
        return request

    def get_social_login(self, adapter, app, token, response):
        """
        :param adapter: allauth.socialaccount Adapter subclass.
            Usually OAuthAdapter or Auth2Adapter
        :param app: `allauth.socialaccount.SocialApp` instance
        :param token: `allauth.socialaccount.SocialToken` instance
        :param response: Provider's response for OAuth1. Not used in the
        :returns: A populated instance of the
            `allauth.socialaccount.SocialLoginView` instance
        """
        request = self._get_request()
        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token
        return social_login

    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()
        if not view:
            raise serializers.ValidationError('View is not defined, pass it as a context variable')
        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError('Define adapter_class in view')
        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)
        access_token = attrs.get('access_token')
        token_secret = attrs.get('token_secret')
        request.session['oauth_api.twitter.com_access_token'] = {'oauth_token':access_token, 
         'oauth_token_secret':token_secret}
        token = SocialToken(token=access_token, token_secret=token_secret)
        token.app = app
        try:
            login = self.get_social_login(adapter, app, token, access_token)
            complete_social_login(request, login)
        except OAuthError as e:
            try:
                raise serializers.ValidationError(str(e))
            finally:
                e = None
                del e

        else:
            if not login.is_existing:
                login.lookup()
                login.save(request, connect=True)
            attrs['user'] = login.account.user
            return attrs


class TwitterConnectSerializer(SocialConnectMixin, TwitterLoginSerializer):
    pass