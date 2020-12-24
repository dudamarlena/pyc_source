# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Infinidat/infi.pyutils/tests/test__recursive_getattr.py
# Compiled at: 2016-09-14 06:55:36
from .test_utils import TestCase
from infi.pyutils import recursive_getattr

class RecursiveGetattrTest(TestCase):

    def setUp(self):
        super(RecursiveGetattrTest, self).setUp()
        self.obj = Object()
        self.obj.a = Object()
        self.obj.a.b = Object()
        self.obj.a.b.value = self.value = Object()

    def test__recursive_getattr_success(self):
        self.assertIs(recursive_getattr(self.obj, 'a.b.value'), self.value)

    def test__recursive_getattr_failure(self):
        with self.assertRaises(AttributeError):
            recursive_getattr(self.obj, 'a.b.bla')

    def test__recursive_getattr_failure_default(self):
        default = Object()
        self.assertIs(default, recursive_getattr(self.obj, 'a.b.bla', default))


class Object(object):
    pass