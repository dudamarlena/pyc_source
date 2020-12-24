# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/templatetags/compressed.py
# Compiled at: 2019-06-12 01:17:17
"""Compatibility tags for django-pipeline <= 1.3.

django-pipeline 1.5 renamed the old ``compressed_css` and ``compressed_js``
template tags to ``stylesheet`` and ``javascript``. While this change makes a
lot of sense, it's possible that third-party users will still have templates
relying on the old names.
"""
from __future__ import unicode_literals
from django import template
from pipeline.templatetags.pipeline import javascript, stylesheet
register = template.Library()
register.tag(b'compressed_css', stylesheet)
register.tag(b'compressed_js', javascript)