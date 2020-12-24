# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/prism_rest/__init__.py
# Compiled at: 2013-05-03 19:56:54
from .renderer import APISerializer
from .views import APIView
from .views import APIAuthView
from .viewmodels import view_requires
from .viewmodels import view_provides
from .viewmodels import register_model
from .viewmodels import BaseViewModel
from .viewmodels import BaseCollectionViewModel

def includeme(config):
    config.add_renderer('prism_renderer', APISerializer)
    config.add_route('base', '/base')
    config.add_route('base_view_auth', '/base/auth')
    config.add_route('base_api', '/base/api')
    config.add_route('base_api_auth', '/base/api_auth')
    config.include('prism_core')
    config.scan()
    return config