# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/source/git/django-codemirror2/examples/testapp/models.py
# Compiled at: 2016-02-02 21:43:15
# Size of source mod 2**32: 461 bytes
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class TestCss(models.Model):
    title = models.CharField(max_length=255)
    css = models.TextField()

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class TestHTML(models.Model):
    title = models.CharField(max_length=255)
    html = models.TextField()

    def __str__(self):
        return self.title