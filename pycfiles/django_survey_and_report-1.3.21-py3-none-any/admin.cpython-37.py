# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/admin.py
# Compiled at: 2020-02-23 10:00:28
# Size of source mod 2**32: 1442 bytes
from django.contrib import admin
from survey.actions import make_published
from survey.exporter.csv import Survey2Csv
from survey.exporter.tex import Survey2Tex
from survey.models import Answer, Category, Question, Response, Survey

class QuestionInline(admin.TabularInline):
    model = Question
    ordering = ('order', 'category')
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'need_logged_user', 'template')
    list_filter = ('is_published', 'need_logged_user')
    inlines = [CategoryInline, QuestionInline]
    actions = [make_published, Survey2Csv.export_as_csv, Survey2Tex.export_as_tex]


class AnswerBaseInline(admin.StackedInline):
    fields = ('question', 'body')
    readonly_fields = ('question', )
    extra = 0
    model = Answer


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('interview_uuid', 'survey', 'created', 'user')
    list_filter = ('survey', 'created')
    date_hierarchy = 'created'
    inlines = [AnswerBaseInline]
    readonly_fields = ('survey', 'created', 'updated', 'interview_uuid', 'user')


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)