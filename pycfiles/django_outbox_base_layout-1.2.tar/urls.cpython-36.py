# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/edsonjunior/PycharmProjects/base_django/base/django_outbox_base_layout/urls.py
# Compiled at: 2018-10-26 14:45:39
# Size of source mod 2**32: 1007 bytes
from django.urls import path
from . import views
urlpatterns = [
 path('', (views.LoginView.as_view()), name='sbadmin_login'),
 path('index/', (views.IndexView.as_view()), name='sbadmin_index'),
 path('blank/', (views.BlankView.as_view()), name='sbadmin_blank'),
 path('buttons/', (views.ButtonsView.as_view()), name='sbadmin_buttons'),
 path('flot/', (views.FlotView.as_view()), name='sbadmin_flot'),
 path('forms/', (views.FormsView.as_view()), name='sbadmin_forms'),
 path('grid/', (views.GridView.as_view()), name='sbadmin_grid'),
 path('icons/', (views.IconsView.as_view()), name='sbadmin_icons'),
 path('morris/', (views.MorrisView.as_view()), name='sbadmin_morris'),
 path('notifications/', (views.NotificationsView.as_view()), name='sbadmin_notifications'),
 path('panels/', (views.PanelsView.as_view()), name='sbadmin_panels'),
 path('tables/', (views.TablesView.as_view()), name='sbadmin_tables'),
 path('typography/', (views.TypographyView.as_view()), name='sbadmin_typography')]