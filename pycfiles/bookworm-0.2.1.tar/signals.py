# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/editor/signals.py
# Compiled at: 2012-02-14 23:34:00
import django.dispatch
book_created = django.dispatch.Signal(providing_args=['book'])
book_version_created = django.dispatch.Signal(providing_args=['book', 'version'])
chapter_created = django.dispatch.Signal(providing_args=['chapter'])
chapter_modified = django.dispatch.Signal(providing_args=['user', 'chapter'])
attachment_uploaded = django.dispatch.Signal(providing_args=['attachment'])
book_toc_changed = django.dispatch.Signal()