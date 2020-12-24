# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/editor/signals.py
# Compiled at: 2012-02-14 23:34:00
import django.dispatch
book_created = django.dispatch.Signal(providing_args=['book'])
book_version_created = django.dispatch.Signal(providing_args=['book', 'version'])
chapter_created = django.dispatch.Signal(providing_args=['chapter'])
chapter_modified = django.dispatch.Signal(providing_args=['user', 'chapter'])
attachment_uploaded = django.dispatch.Signal(providing_args=['attachment'])
book_toc_changed = django.dispatch.Signal()