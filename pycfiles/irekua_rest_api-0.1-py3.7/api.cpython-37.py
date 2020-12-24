# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/urls/api.py
# Compiled at: 2019-10-31 17:28:40
# Size of source mod 2**32: 339 bytes
from django.conf.urls import url, include
from .additional import additional_router
from .main import main_router
from .object_types import object_types_router
urlpatterns = [
 url('^', include(main_router.urls)),
 url('^types/', include(object_types_router.urls)),
 url('^additional/', include(additional_router.urls))]