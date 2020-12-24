# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sparrow/tests/test_sesame.py
# Compiled at: 2009-07-20 09:57:48
import os
from unittest import TestCase, TestSuite, makeSuite, main
import sparrow
from sparrow.error import ConnectionError
from sparrow.tests.base_tests import TripleStoreTest, TripleStoreQueryTest, open_test_file

class SesameTest(TripleStoreTest):

    def setUp(self):
        self.db = sparrow.database('sesame', get_sesame_url())

    def tearDown(self):
        self.db.clear('test')
        self.db.disconnect()
        del self.db


class SesameQueryTest(TripleStoreQueryTest):

    def setUp(self):
        self.db = sparrow.database('sesame', get_sesame_url())
        fp = open_test_file('ntriples')
        self.db.add_ntriples(fp, 'test')
        fp.close()

    def tearDown(self):
        self.db.clear('test')
        self.db.disconnect()
        del self.db


def get_sesame_url():
    url = 'http://%s:%s/test' % (os.environ.get('SESAME_HOST', 'localhost'),
     os.environ.get('SESAME_PORT', '8000'))
    return url


def test_suite():
    try:
        sparrow.database('sesame', get_sesame_url())
    except ConnectionError:
        return TestSuite()

    suite = TestSuite()
    suite.addTest(makeSuite(SesameTest))
    suite.addTest(makeSuite(SesameQueryTest))
    return suite


if __name__ == '__main__':
    main(defaultTest='test_suite')