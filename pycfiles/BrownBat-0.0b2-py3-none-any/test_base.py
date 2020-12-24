# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/tests/test_pipeline/test_base.py
# Compiled at: 2014-10-08 05:32:06
from __future__ import absolute_import, unicode_literals
from pytest import raises
from brownant.pipeline.base import PipelineProperty

def test_required_attrs():

    class SpamProperty(PipelineProperty):
        required_attrs = {
         b'egg'}

        def provide_value(self, obj):
            return obj

    spam_property = SpamProperty(egg=42)
    assert spam_property.egg == 42
    assert b'egg' not in spam_property.options
    assert b'egg' not in spam_property.attr_names
    with raises(AttributeError):
        spam_property.foo
    with raises(TypeError) as (excinfo):
        spam_property = SpamProperty(spam=42)
    assert b'egg' in repr(excinfo.value)


def test_attr_name():

    class SpamProperty(PipelineProperty):

        def prepare(self):
            self.attr_names.setdefault(b'egg_attr', b'egg')

        def provide_value(self, obj):
            return self.get_attr(obj, b'egg_attr')

    class Spam(object):

        def __init__(self, **kwargs):
            vars(self).update(kwargs)

    spam_a = SpamProperty(egg=42)
    assert spam_a.attr_names[b'egg_attr'] == b'egg'
    assert spam_a.provide_value(Spam(egg=1024)) == 1024
    spam_b = SpamProperty(egg=42, egg_attr=b'foo_egg')
    assert spam_b.attr_names[b'egg_attr'] == b'foo_egg'
    assert spam_b.provide_value(Spam(foo_egg=2048)) == 2048


def test_optional_attr():

    class SpamProperty(PipelineProperty):
        required_attrs = {
         b'egg'}

        def provide_value(self, obj):
            return obj

    spam = SpamProperty(egg=41, foo=42, bar=43, aha_attr=44)
    assert spam.options[b'foo'] == 42
    assert spam.options[b'bar'] == 43
    assert b'egg' not in spam.options
    assert b'aha_attr' not in spam.options