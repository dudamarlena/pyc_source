# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/urls/staticfiles.py
# Compiled at: 2019-06-12 01:17:17
"""Utility functions for looking up static media URLs."""
from __future__ import unicode_literals
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils import six
from django.utils.functional import lazy
static_lazy = lazy(static, six.text_type)