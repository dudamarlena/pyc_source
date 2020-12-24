# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/notification/admin.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 520 bytes
from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from .models import EmailNotification

class EmailNotificationAdmin(admin.ModelAdmin):
    formfield_overrides = {models.ManyToManyField: {'widget': CheckboxSelectMultiple}}
    list_display = [
     'name', 'sitenames']
    search_fields = ['name', 'subject', 'body']
    list_filter = ['sites']


admin.site.register(EmailNotification, EmailNotificationAdmin)