# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seraf/Cycloid/Cyclosible/cyclosible/appversion/urls.py
# Compiled at: 2015-12-22 05:07:25
from cyclosible.Cyclosible.routers import main_router
from .views import AppVersionViewSet
main_router.register('app-version', AppVersionViewSet)