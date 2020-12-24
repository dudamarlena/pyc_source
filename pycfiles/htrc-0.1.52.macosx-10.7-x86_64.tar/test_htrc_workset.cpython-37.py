# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shliyana/anaconda3/lib/python3.7/site-packages/tests/test_htrc_workset.py
# Compiled at: 2019-05-06 10:39:58
# Size of source mod 2**32: 5087 bytes
import sys
if sys.version_info.major == 2:
    from mock import Mock, patch
else:
    if sys.version_info.major == 3:
        from unittest.mock import Mock, patch
import unittest2 as unittest, json, os.path, htrc.workset

class TestWorkset(unittest.TestCase):

    def setUp(self):
        self.test_vols = [
         'mdp.39015050817181', 'mdp.39015055436151',
         'mdp.39015056169157', 'mdp.39015050161697', 'mdp.39015042791874']
        dirname = os.path.dirname(__file__)
        self.example_file = os.path.join(dirname, 'data/example.jsonld')
        with open(self.example_file, 'r') as (infile):
            self.json = json.load(infile)
        self.example_csv = os.path.join(dirname, 'data/example.csv')
        with open(self.example_csv, 'r') as (infile):
            self.csv = infile.read().encode('utf-8')

    def test_get_volumes(self):
        """
        Test get_volumes by ensuring that the JSON-LD data structure can be
        extracted.
        """
        vols = htrc.workset.get_volumes(self.json)
        for vol in self.test_vols:
            self.assertIn(vol, vols)

    def test_load_file(self):
        vols = htrc.workset.load(self.example_file)
        for vol in self.test_vols:
            self.assertIn(vol, vols)

    def test_get_volumes_from_csv(self):
        vols = htrc.workset.get_volumes_from_csv(self.csv)
        for vol in self.test_vols:
            self.assertIn(vol, vols)

    @patch('htrc.workset.urlopen')
    def test_load_url_hathitrust(self, urlopen_mock):
        ht_url = 'https://babel.hathitrust.org/cgi/mb?a=listis&c=548413090'
        response_mock = Mock()
        urlopen_mock.return_value = response_mock
        response_mock.read.return_value = self.csv
        vols = htrc.workset.load_url(ht_url)
        for vol in self.test_vols:
            self.assertIn(vol, vols)

    @patch('htrc.workset.urlopen')
    def test_load_url_htrc(self, urlopen_mock):
        htrc_url = 'https://htrc.hathitrust.org/wsid/123456'
        response_mock = Mock()
        urlopen_mock.return_value = response_mock
        response_mock.read.return_value = json.dumps(self.json).encode('utf-8')
        vols = htrc.workset.load_url(htrc_url)
        for vol in self.test_vols:
            self.assertIn(vol, vols)

        htrc_url2 = 'http://acbres224.ischool.illinois.edu:8080/dcWSfetch/getItems?id=http://htrc.hathitrust.org/wsid/189324102'
        vols = htrc.workset.load_url(htrc_url2)
        for vol in self.test_vols:
            self.assertIn(vol, vols)

    @patch('htrc.workset.urlopen')
    def test_load_url_error(self, urlopen_mock):
        invalid_url = 'blahblahblah'
        with self.assertRaises(ValueError):
            htrc.workset.load_url(invalid_url)

    @patch('htrc.workset.urlopen')
    def test_load_hathitrust_collection(self, urlopen_mock):
        ht_url = 'https://babel.hathitrust.org/cgi/mb?a=listis&c=548413090'
        response_mock = Mock()
        urlopen_mock.return_value = response_mock
        response_mock.read.return_value = self.csv
        vols = htrc.workset.load_hathitrust_collection(ht_url)
        for vol in self.test_vols:
            self.assertIn(vol, vols)

        ht_url = 'https://babel.hathitrust.org/cgi/mb?a=listis'
        with self.assertRaises(ValueError):
            htrc.workset.load_hathitrust_collection(ht_url)
        ht_url = 'http://babel.hathitrust.org/cgi/mb?a=listis&c=548413090'
        with self.assertRaises(ValueError):
            htrc.workset.load_hathitrust_collection(ht_url)
        ht_url = 'https://htrc.hathitrust.org/cgi/mb?a=listis&c=548413090'
        with self.assertRaises(ValueError):
            htrc.workset.load_hathitrust_collection(ht_url)

    @patch('htrc.workset.load_url')
    def test_load_with_url(self, load_url_mock):
        ht_url = 'https://babel.hathitrust.org/cgi/mb?a=listis&c=548413090'
        load_url_mock.return_value = self.test_vols
        vols = htrc.workset.load(ht_url)
        load_url_mock.assert_called_with(ht_url)


suite = unittest.TestLoader().loadTestsFromTestCase(TestWorkset)
unittest.TextTestRunner(verbosity=2).run(suite)