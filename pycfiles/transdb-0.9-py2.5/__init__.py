# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/transdb/__init__.py
# Compiled at: 2010-11-15 07:25:19
"""
TransDb Django application

TransDb provides translated fields into the Django application modules
using TransCharField (for single line texts) and TransTextField (for
multiple line texts).

Simple usage:

    from django.db import models
    import transdb

    class MyModel(models.Model):
        single_language_field = models.CharField(max_length=32)
        multi_language_field = transdb.TransCharField(max_length=32)

Further information is available at project page:
    http://code.google.com/transdb
"""
from fields import TransCharField, TransTextField