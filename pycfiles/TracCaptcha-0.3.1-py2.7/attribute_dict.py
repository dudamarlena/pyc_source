# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/lib/attribute_dict.py
# Compiled at: 2010-06-13 02:14:12
from unittest import TestCase
__all__ = [
 'AttrDict']

class AttrDict(dict):

    def __getattr__(self, name):
        if name not in self:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))
        return self[name]


class AttributDictTests(TestCase):

    def test_can_use_class_as_dict(self):
        obj = AttrDict(foo=1, bar=2)
        self.assertEquals(1, obj['foo'])
        self.assertEquals(2, obj['bar'])

    def test_can_access_items_as_attributes(self):
        obj = AttrDict(foo=1, bar=2)
        self.assertEquals(1, obj.foo)
        self.assertEquals(2, obj.bar)

    def test_raise_attribute_error_for_non_existent_keys(self):
        obj = AttrDict(foo=1)
        self.assertRaises(AttributeError, getattr, obj, 'invalid')