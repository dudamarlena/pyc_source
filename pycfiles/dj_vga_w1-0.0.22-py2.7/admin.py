# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dpl1_main/testing_app/admin.py
# Compiled at: 2014-02-26 04:44:05
from django.contrib import admin
import dpl1_main.testing_app.models

class PageInline(admin.TabularInline):
    model = dpl1_main.testing_app.models.Page


class QuestionInline(admin.TabularInline):
    model = dpl1_main.testing_app.models.Question


class AnswerInline(admin.TabularInline):
    model = dpl1_main.testing_app.models.Answer


class ResultInline(admin.TabularInline):
    model = dpl1_main.testing_app.models.Result


class TestAdmin(admin.ModelAdmin):
    inlines = (
     PageInline, ResultInline)
    list_display = ('name', 'description')


class PageAdmin(admin.ModelAdmin):
    inlines = (
     QuestionInline,)
    ordering = ('test', 'sequence')


class QuestionAdmin(admin.ModelAdmin):
    inlines = (
     AnswerInline,)
    ordering = ('page', 'text')


admin.site.register(dpl1_main.testing_app.models.Test, TestAdmin)
admin.site.register(dpl1_main.testing_app.models.Page, PageAdmin)
admin.site.register(dpl1_main.testing_app.models.Question, QuestionAdmin)