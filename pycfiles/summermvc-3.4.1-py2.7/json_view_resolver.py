# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/json_view_resolver.py
# Compiled at: 2018-05-30 05:31:20
__all__ = [
 'JsonViewResolver']
__authors__ = ['Tim Chow']
import json
from .interface import ViewResolver, View
from .model_and_view import Model
from .constrant import HTTPStatus

class JsonView(View):

    def get_content_type(self):
        return 'application/json'

    def render(self, model):
        return self.__dumps(model)

    def __dumps(self, model):
        return json.dumps(model, default=self.default)

    def default(self, obj):
        if isinstance(obj, Model):
            return obj.asmap()
        return obj


class JsonViewResolver(ViewResolver):

    def __init__(self):
        self._json_view = JsonView()

    def get_view(self, view_name, status_code):
        return self._json_view