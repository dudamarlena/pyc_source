# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/faq/admin.py
# Compiled at: 2014-03-27 06:14:42
from django.contrib import admin
from .models import Category, Question
from .forms import QuestionAdminForm

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
     'order', 'title']
    list_display_links = ['title']


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ['order', 'question', 'active']
    list_display_links = ['question']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)