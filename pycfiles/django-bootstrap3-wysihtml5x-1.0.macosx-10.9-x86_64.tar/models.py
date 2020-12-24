# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/bootstrap3_wysihtml5x/tests/models.py
# Compiled at: 2014-10-27 10:46:01
from django.db import models
from bootstrap3_wysihtml5x.fields import Wysihtml5xTextField

class ModelTest(models.Model):
    first_text = models.TextField()
    second_text = Wysihtml5xTextField()