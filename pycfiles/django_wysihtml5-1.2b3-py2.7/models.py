# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/wysihtml5/tests/models.py
# Compiled at: 2014-01-19 03:33:05
from django.db import models
from wysihtml5.fields import Wysihtml5TextField

class ModelTest(models.Model):
    first_text = models.TextField()
    second_text = Wysihtml5TextField()