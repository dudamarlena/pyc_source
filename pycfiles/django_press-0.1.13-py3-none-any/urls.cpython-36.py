# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\urls.py
# Compiled at: 2020-02-11 06:07:34
# Size of source mod 2**32: 265 bytes
from django.urls import path
from django_press.views import PageView, inquiry_view
urlpatterns = [
 path('', PageView.as_view()),
 path('inquiry/<path:path>', inquiry_view, name='Inquiry'),
 path('<path:path>', (PageView.as_view()), name='Page')]