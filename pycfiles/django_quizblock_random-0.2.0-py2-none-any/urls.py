# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/work/python/teachrecovery/quizblock_random/urls.py
# Compiled at: 2015-01-05 09:47:29
from django.conf.urls import patterns
from .views import EditQuizRandomView, AddQuestionToQuizRandomView, EditQuestionRandomView, AddAnswerToQuestionRandomView, EditAnswerRandomView, DeleteAnswerRandomView, DeleteQuestionRandomView
urlpatterns = patterns('quizblock_random.views', (
 '^edit_quiz/(?P<pk>\\d+)/$', EditQuizRandomView.as_view(), {}, 'edit-quiz-random'), (
 '^edit_quiz/(?P<pk>\\d+)/add_question/$',
 AddQuestionToQuizRandomView.as_view(), {}, 'add-question-to-quiz-random'), (
 '^edit_question/(?P<pk>\\d+)/$', EditQuestionRandomView.as_view(), {},
 'edit-question-random'), (
 '^edit_question/(?P<pk>\\d+)/add_answer/$',
 AddAnswerToQuestionRandomView.as_view(), {},
 'add-answer-to-question-random'), (
 '^delete_question/(?P<pk>\\d+)/$', DeleteQuestionRandomView.as_view(), {},
 'delete-question-random'), (
 '^delete_answer/(?P<pk>\\d+)/$', DeleteAnswerRandomView.as_view(), {}, 'delete-answer-random'), (
 '^edit_answer/(?P<pk>\\d+)/$', EditAnswerRandomView.as_view(), {}, 'edit-answer-random'))