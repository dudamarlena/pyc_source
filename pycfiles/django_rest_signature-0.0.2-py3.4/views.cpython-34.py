# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest_signature/views.py
# Compiled at: 2015-04-30 01:17:41
# Size of source mod 2**32: 779 bytes
from rest_framework.generics import *
from .serializers import *

class SiteList(ListCreateAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class SignatureList(ListCreateAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    response_serializer = SignatureResponseSerializer

    def get(self, request, *args, **kwargs):
        self.serializer_class = self.response_serializer
        return super(SignatureList, self).get(request, *args, **kwargs)