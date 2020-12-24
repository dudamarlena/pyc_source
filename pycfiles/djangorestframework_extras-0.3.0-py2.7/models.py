# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest_framework_extras/tests/models.py
# Compiled at: 2018-04-26 08:15:23
from django.db import models

class Bar(models.Model):
    pass


class Foo(models.Model):
    pass


class Base(models.Model):
    editable_field = models.CharField(max_length=32)
    another_editable_field = models.CharField(max_length=32)
    non_editable_field = models.CharField(max_length=32, editable=False)
    foreign_field = models.ForeignKey(Foo, on_delete=models.CASCADE)
    many_field = models.ManyToManyField(Bar)

    class Meta:
        abstract = True


class Vanilla(Base):
    pass


class WithForm(Base):
    pass


class WithTrickyForm(Base):
    pass


class WithAdminClass(Base):
    pass