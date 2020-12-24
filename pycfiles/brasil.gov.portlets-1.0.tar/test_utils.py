# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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