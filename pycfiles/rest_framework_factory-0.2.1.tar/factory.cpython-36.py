# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/dev/rest_framework_factory/rest_framework_factory/factory.py
# Compiled at: 2019-01-23 09:16:58
# Size of source mod 2**32: 1044 bytes
import os
from django.conf import settings
skel_dir = os.path.join(os.path.dirname(__file__), 'skel')

class Factory:

    def __init__(self):
        self.apis = {}
        self.apis['TestModel'] = self.create_from_scratch(model_name='TestModel')

    def create_from_scratch(self, model_name=None):
        """Create a new DRF API, model and all. """
        model_name_lcase = model_name.lower()
        skel_file_model = os.path.join(skel_dir, 'models.py.txt')
        skel_file_api = os.path.join(skel_dir, 'api.py.txt')
        with open(skel_file_model) as (f):
            content = f.read().format(model_name=model_name, model_name_lcase=model_name_lcase)
        with open(skel_file_api) as (f):
            content += f.read().format(model_name=model_name, model_name_lcase=model_name_lcase)
        return content

    def build_from_model(self, app_name=None, models=None):
        """Build a DRF API from an existing django model"""
        pass

    def build_from_app(self, app_name=None):
        assert app_name in settings.INSTALLED_APPS