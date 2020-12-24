# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_utils.py
# Compiled at: 2018-10-18 17:35:14
from brasil.gov.portal.utils import validate_list_of_links
from zope.interface import Invalid
import unittest

class UtilsTestCase(unittest.TestCase):

    def test_validate_list_of_links_valid(self):
        self.assertTrue(validate_list_of_links([]))
        self.assertTrue(validate_list_of_links(['Title|http://example.org']))

    def test_validate_list_of_links_invalid(self):
        with self.assertRaises(Invalid):
            validate_list_of_links(['Title http://example.org'])
            validate_list_of_links(['Title||http://example.org'])
            validate_list_of_links(['Title|example.org'])
            validate_list_of_links(['Title'])
            validate_list_of_links(['http://example.org'])