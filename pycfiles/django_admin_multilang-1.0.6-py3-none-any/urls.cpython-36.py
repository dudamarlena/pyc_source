# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\pc\Workspace\Django\zivjulete\admin_multilanguage\urls.py
# Compiled at: 2018-12-04 22:01:23
# Size of source mod 2**32: 216 bytes
from django.urls import path
from admin_multilanguage import views
app_name = 'admin_multilanguage'
urlpatterns = [
 path('change_language/', (views.ChangeLanguageView.as_view()), name='change_language')]