# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marcgibbons/projects/drf_signed_auth/drf_signed_auth/views.py
# Compiled at: 2017-09-30 09:45:23
# Size of source mod 2**32: 919 bytes
from furl import furl
from rest_framework import exceptions, response, views
from . import settings
from .signing import UserSigner

class SignUrlView(views.APIView):
    __doc__ = '\n    Adds authentication signature to provided URL\n\n    url -- URL to be wrapped\n    '
    param = settings.SIGNED_URL_QUERY_PARAM
    permission_classes = settings.SIGNED_URL_PERMISSION_CLASSES

    def post(self, request):
        url = request.data.get('url')
        if not url:
            raise exceptions.ValidationError('`url` must be provided')
        return response.Response(self.get_signed_url(url))

    def get_signed_url(self, url):
        """
        Returns provided URL with an authentication
        signature.
        """
        signer = UserSigner()
        url = self.request.build_absolute_uri(url)
        signature = signer.sign(user=(self.request.user))
        return furl(url).add({self.param: signature}).url