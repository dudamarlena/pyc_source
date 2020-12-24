# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/tests/models.py
# Compiled at: 2017-05-03 05:57:29
from django.db import models
from jmbo.models import ModelBase

class DummyRelationalModel1(models.Model):
    pass


class DummyRelationalModel2(models.Model):
    pass


class DummyTargetModelBase(ModelBase):
    pass


class DummySourceModelBase(ModelBase):
    points_to = models.ForeignKey('DummyModel')
    points_to_many = models.ManyToManyField('DummyModel', related_name='to_many')


class DummyModel(ModelBase):
    test_editable_field = models.CharField(max_length=32)
    test_non_editable_field = models.CharField(max_length=32, editable=False)
    test_foreign_field = models.ForeignKey('DummyRelationalModel1', blank=True, null=True)
    test_foreign_published = models.ForeignKey('DummyTargetModelBase', blank=True, null=True, related_name='foreign_published')
    test_foreign_unpublished = models.ForeignKey('DummyTargetModelBase', blank=True, null=True, related_name='foreign_unpublished')
    test_many_field = models.ManyToManyField('DummyRelationalModel2')
    test_many_published = models.ManyToManyField('DummyTargetModelBase', related_name='many_published', blank=True, null=True)
    test_many_unpublished = models.ManyToManyField('DummyTargetModelBase', related_name='many_unpublished', blank=True, null=True)
    test_member = True


class TrunkModel(ModelBase):
    pass


class BranchModel(TrunkModel):
    pass


class LeafModel(BranchModel):
    pass


class TestModel(ModelBase):
    autosave_fields = ('title', )
    content = models.TextField(null=True, blank=True)