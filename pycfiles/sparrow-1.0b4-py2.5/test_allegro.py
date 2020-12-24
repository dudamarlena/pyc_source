# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sparrow/tests/test_allegro.py
# Compiled at: 2009-07-20 09:57:48
import os
from unittest import TestCase, TestSuite, makeSuite, main
import sparrow
from sparrow.error import ConnectionError
from sparrow.tests.base_tests import TripleStoreTest, TripleStoreQueryTest, open_test_file

class AllegroTest(TripleStoreTest):

    def setUp(self):
        self.db = sparrow.database('allegro', get_allegro_url())

    def tearDown(self):
        self.db.clear('test')
        self.db.disconnect()
        del self.db


class AllegroQueryTest(TripleStoreQueryTest):

    def setUp(self):
        self.db = sparrow.database('allegro', get_allegro_url())
        fp = open_test_file('ntriples')
        self.db.add_ntriples(fp, 'test')
        fp.close()

    def tearDown(self):
        self.db.clear('test')
        self.db.disconnect()
        del self.db


def get_allegro_url():
    url = 'http://%s:%s/test' % (os.environ.get('ALLEGRO_HOST', 'localhost'),
     os.environ.get('ALLEGRO_PORT', '8000'))
    return url


def test_suite():
    try:
        sparrow.database('allegro', get_allegro_url())
    except ConnectionError, err:
        return TestSuite()

    suite = TestSuite()
    suite.addTest(makeSuite(AllegroTest))
    suite.addTest(makeSuite(AllegroQueryTest))
    return suite


if __name__ == '__main__':
    main(defaultTest='test_suite')