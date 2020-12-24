# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kinopoisk/tests/base.py
# Compiled at: 2018-08-23 12:28:40
from vcr_unittest import VCRTestCase

class VCRMixin:

    def _get_vcr_kwargs(self, **kwargs):
        kwargs['record_mode'] = 'new_episodes'
        return kwargs


class BaseTest(VCRMixin, VCRTestCase):

    def assertEqualPersons(self, persons, names):
        return self.assertEqual([ person.__repr__() for person in persons ], names)