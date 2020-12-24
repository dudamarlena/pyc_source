# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deforest/tests/test_tags.py
# Compiled at: 2020-03-13 12:20:39
# Size of source mod 2**32: 539 bytes
import unittest
import deforest.tags as tags

class TestAWSTag(unittest.TestCase):
    sut = tags.AWSTag('!GetAtt')

    def test_init(self):
        assert self.sut.var == '!GetAtt'

    def test_repr(self):
        assert repr(self.sut) == '!GetAtt'

    def test_to_yaml(self):
        assert tags.AWSTag.to_yaml(None, None) == ''

    def test_from_yaml(self):

        class a:
            value = 'hello'

        actual = tags.AWSTag.from_yaml(None, a)
        assert type(actual) is tags.AWSTag
        assert actual.var == 'hello'