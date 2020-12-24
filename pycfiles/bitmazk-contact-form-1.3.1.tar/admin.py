# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Tyrdall/projects/bitmazk-contact-form/src/contact_form/admin.py
# Compiled at: 2016-04-11 01:51:28
"""Admins for the ``contact_form`` app."""
from django.contrib import admin
from hvad.admin import TranslatableAdmin
from .models import ContactFormCategory
admin.site.register(ContactFormCategory, TranslatableAdmin)