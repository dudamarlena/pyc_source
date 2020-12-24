# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/weargoggles/django-coreapi/django_coreapi/renderers.py
# Compiled at: 2017-05-15 07:49:40
# Size of source mod 2**32: 566 bytes
from coreapi.codecs import DisplayCodec, CoreJSONCodec
from rest_framework.renderers import BaseRenderer

class CoreAPIJSONRenderer(BaseRenderer):
    media_type = 'application/vnd.coreapi+json'
    charset = None

    def render(self, data, media_type=None, renderer_context=None):
        codec = CoreJSONCodec()
        return codec.dump(data, indent=True)


class CoreAPIHTMLRenderer(BaseRenderer):
    media_type = 'text/html'

    def render(self, data, media_type=None, renderer_context=None):
        codec = DisplayCodec()
        return codec.dump(data)