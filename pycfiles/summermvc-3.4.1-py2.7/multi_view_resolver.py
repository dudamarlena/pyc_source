# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/src/view_resolver/multi_view_resolver.py
# Compiled at: 2018-06-01 03:44:03
import json
from dicttoxml import dicttoxml
from summermvc.decorator import *
from summermvc.mvc import *

@component
class MultiViewResolver(ViewResolver):

    @post_construct
    def setup(self):
        self._xml_view = XMLView()
        self._json_view = JsonView()

    @override
    def get_view(self, view_name, status_code):
        print 'view name is: %s, status_code is: %d' % (
         view_name, status_code)
        if view_name == 'xml':
            return self._xml_view
        return self._json_view


class XMLView(View):

    @override
    def render(self, model):
        return dicttoxml(model.asmap())

    @override
    def get_content_type(self):
        return 'application/xml'


class JsonView(View):

    @override
    def render(self, model):
        return json.dumps(model, default=self._default)

    def _default(self, obj):
        if isinstance(obj, Model):
            return obj.asmap()
        return obj

    @override
    def get_content_type(self):
        return 'application/json'