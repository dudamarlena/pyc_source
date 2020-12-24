# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/torrent/test_parser.py
# Compiled at: 2015-06-17 00:29:03
import glob, os, testtools
from seedbox.tests import test
from seedbox.torrent import parser
torrent_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testdata')

class TorrentParserTest(test.BaseTestCase):

    def test_parse(self):
        tfiles = glob.glob(os.path.join(torrent_path, 'other-*.torrent'))
        for tfile in tfiles:
            torrent = parser.TorrentParser(tfile)
            self.assertIsNotNone(torrent)
            self.assertIsNotNone(torrent.content)
            self.assertTrue(len(torrent.get_file_details()) > 0)

    def test_custom_parser1(self):
        tfile = os.path.join(torrent_path, 'bencode-bad-1.torrent')
        torrent = parser.TorrentParser(tfile)
        self.assertIsNotNone(torrent)

    def test_custom_parser2(self):
        tfile = os.path.join(torrent_path, 'bencode-bad-2.torrent')
        torrent = parser.TorrentParser(tfile)
        self.assertIsNotNone(torrent)

    def test_custom_parser3(self):
        tfile = os.path.join(torrent_path, 'bencode-bad-3.torrent')
        torrent = parser.TorrentParser(tfile)
        self.assertIsNotNone(torrent)

    def test_tiny_torrent(self):
        tfile = os.path.join(torrent_path, 'tiny-torrent.torrent')
        torrent = parser.TorrentParser(tfile)
        self.assertIsNotNone(torrent)

    def test_medium_torrent(self):
        tfile = os.path.join(torrent_path, 'medium-torrent.torrent')
        torrent = parser.TorrentParser(tfile)
        self.assertIsNotNone(torrent)

    def test_large_torrent(self):
        tfile = os.path.join(torrent_path, 'large-torrent.torrent')
        torrent = parser.TorrentParser(tfile)
        self.assertIsNotNone(torrent)

    def test_missing_file(self):
        with testtools.ExpectedException(IOError):
            parser.TorrentParser('dummy/file/does/not/exist')

    def test_parse_negative_integer(self):
        self.assertEqual(parser.Bdecode.parse('i-123e'), -123)

    def test_parse_invalid_integer(self):
        self.assertRaises(parser.ParsingError, parser.Bdecode.parse, 'i123ae')

    def test_parse_invalid_str(self):
        self.assertRaises(parser.ParsingError, parser.Bdecode.parse, '0:ae')