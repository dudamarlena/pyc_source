# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/work/python/django-likertblock/likertblock/urls.py
# Compiled at: 2015-07-15 14:35:47
from django.conf.urls import patterns
from .views import EditQuestionnaireView, DeleteQuestionView, ReorderQuestionsView, AddQuestionToQuestionnaireView, EditQuestionView
urlpatterns = patterns('likertblock.views', (
 '^edit_questionnaire/(?P<pk>\\d+)/$', EditQuestionnaireView.as_view(), {}, 'edit-questionnaire'), (
 '^edit_questionnaire/(?P<pk>\\d+)/add_question/$',
 AddQuestionToQuestionnaireView.as_view(), {},
 'add-question-to-questionnaire'), (
 '^edit_question/(?P<pk>\\d+)/$', EditQuestionView.as_view(), {},
 'likert-edit-question'), (
 '^delete_question/(?P<pk>\\d+)/$', DeleteQuestionView.as_view(), {},
 'likert-delete-question'), (
 '^reorder_questions/(?P<pk>\\d+)/$', ReorderQuestionsView.as_view(), {},
 'likert-reorder-questions'))