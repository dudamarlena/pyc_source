# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rohan/Django/django-admin-kit/.venv/lib/python3.6/site-packages/tests/test_duplicate/admin.py
# Compiled at: 2017-11-30 08:43:33
# Size of source mod 2**32: 260 bytes
from django.contrib import admin
from .models import Author, Book

class BookAdmin(admin.StackedInline):
    model = Book
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    model = Author
    inlines = [BookAdmin]


admin.site.register(Author, AuthorAdmin)