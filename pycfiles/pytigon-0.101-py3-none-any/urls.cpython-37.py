# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sch/prj/setup/pytigon/pytigon/prj/_schwiki/schwiki/urls.py
# Compiled at: 2020-05-02 15:32:44
# Size of source mod 2**32: 1135 bytes
from django.conf.urls import url
import django.utils.translation as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views
urlpatterns = [
 url('^(?P<app_or_subject>[^/]*)/(?P<page_path>[^/]*)/view/$', views.view_page),
 url('^(?P<app_or_subject>\\w*)/(?P<page_name>\\w*)/edit/$', views.edit_page),
 gen_row_action('PageObjectsConf', 'insert_object_to_editor', views.insert_object_to_editor),
 gen_tab_action('PageObjectsConf', 'edit_page_object', views.edit_page_object),
 gen_row_action('WikiConf', 'publish', views.publish),
 url('(?P<q>.*)/search/$', views.search, {})]
gen = generic_table_start(urlpatterns, 'schwiki', views)
gen.standard('PageObjectsConf', _('Page objects configurations'), _('Page objects configurations'))
gen.standard('Page', _('Page'), _('Page'))
gen.standard('WikiConf', _('Wiki config'), _('Wiki config'))