# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/djingles/src/djingles/bootstrap4/urls.py
# Compiled at: 2018-04-18 07:49:33
# Size of source mod 2**32: 195 bytes
from django.urls import path
from djingles.bootstrap4 import views
urlpatterns = [
 path('form/', views.VerticalFormView.as_view()),
 path('filters/', views.InlineFormView.as_view())]