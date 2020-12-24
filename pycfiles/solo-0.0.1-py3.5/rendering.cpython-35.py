# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/configurator/config/rendering.py
# Compiled at: 2016-03-29 19:23:40
# Size of source mod 2**32: 1373 bytes
import json
from aiohttp.web import Response
json_encode = json.dumps

class JsonRendererFactory(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, request, view_response):
        return Response(text=json_encode(view_response), content_type='application/json', charset='utf-8', status=200)


class StringRendererFactory(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, request, view_response):
        return Response(text=view_response, content_type='text/plain', charset='utf-8', status=200)


BUILTIN_RENDERERS = {'json': JsonRendererFactory, 
 'string': StringRendererFactory}

class RenderingConfiguratorMixin(object):

    def add_renderer(self, name, factory):
        self.renderers[name] = factory

    def get_renderer(self, name):
        try:
            template_suffix = name.rindex('.')
        except ValueError:
            renderer_name = name
        else:
            renderer_name = name[template_suffix:]
        try:
            return self.renderers[renderer_name](name)
        except KeyError:
            raise ValueError('No such renderer factory {}'.format(renderer_name))