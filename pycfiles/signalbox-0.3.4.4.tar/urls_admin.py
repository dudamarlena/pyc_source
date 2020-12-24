# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/ask/urls_admin.py
# Compiled at: 2014-08-27 19:26:12
"""Administrator urls for the ask app."""
from ask.models import Asker
from ask.views import preview_asker, show_page, start_anonymous_survey
from ask.views import print_asker, show_codebook, preview_questions
from ask.views.asker_text_editing import edit_asker_as_text
from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from django.views.generic.detail import DetailView
from signalbox.decorators import group_required
from signalbox.views.replies import *
urlpatterns = patterns('', url('^asker/(?P<asker_id>\\d+)/text/$', edit_asker_as_text, name='edit_asker_as_text'), url('^asker/(?P<asker_id>\\d+)/codebook/$', show_codebook, name='show_codebook'), url('^asker/(?P<asker_id>\\d+)/print/$', print_asker, name='print_asker'), url('^preview/questions/(?P<ids>[\\w,]+)/$', preview_questions, name='preview_questions'), url('asker/(?P<pk>\\d+)/export/$', group_required(['Researchers', 'Research Assistants'])(DetailView.as_view(model=Asker, template_name='admin/ask/asker/asker_export.html')), name='export_asker'))