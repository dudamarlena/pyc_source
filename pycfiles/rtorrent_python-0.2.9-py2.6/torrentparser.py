# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/rtorrent/lib/torrentparser.py
# Compiled at: 2012-04-10 18:00:40
from rtorrent.common import _py3
import os.path, re, rtorrent.lib.bencode as bencode, hashlib
if _py3:
    from urllib.request import urlopen
else:
    from urllib2 import urlopen

class TorrentParser:

    def __init__(self, torrent):
        """Decode and parse given torrent
        
        @param torrent: handles: urls, file paths, string of torrent data
        @type torrent: str
                
        @raise AssertionError: Can be raised for a couple reasons:
                               - If _get_raw_torrent() couldn't figure out 
                               what X{torrent} is
                               - if X{torrent} isn't a valid bencoded torrent file
        """
        self.torrent = torrent
        self._raw_torrent = None
        self._torrent_decoded = None
        self.file_type = None
        self._get_raw_torrent()
        assert self._raw_torrent is not None, "Couldn't get raw_torrent."
        if self._torrent_decoded is None:
            self._decode_torrent()
        assert isinstance(self._torrent_decoded, dict), 'Invalid torrent file.'
        self._parse_torrent()
        return

    def _is_raw(self):
        raw = False
        if isinstance(self.torrent, (str, bytes)):
            if isinstance(self._decode_torrent(self.torrent), dict):
                raw = True
            else:
                self._torrent_decoded = None
        return raw

    def _get_raw_torrent(self):
        """Get raw torrent data by determining what self.torrent is"""
        if self._is_raw():
            self.file_type = 'raw'
            self._raw_torrent = self.torrent
            return
        if os.path.isfile(self.torrent):
            self.file_type = 'file'
            self._raw_torrent = open(self.torrent, 'rb').read()
        elif re.search('^(http|ftp):\\/\\/', self.torrent, re.I):
            self.file_type = 'url'
            self._raw_torrent = urlopen(self.torrent).read()

    def _decode_torrent(self, raw_torrent=None):
        if raw_torrent is None:
            raw_torrent = self._raw_torrent
        self._torrent_decoded = bencode.decode(raw_torrent)
        return self._torrent_decoded

    def _calc_info_hash(self):
        self.info_hash = None
        if 'info' in self._torrent_decoded.keys():
            info_dict = self._torrent_decoded['info']
            self.info_hash = hashlib.sha1(bencode.encode(info_dict)).hexdigest().upper()
        return self.info_hash

    def _parse_torrent(self):
        for k in self._torrent_decoded:
            key = k.replace(' ', '_').lower()
            setattr(self, key, self._torrent_decoded[k])

        self._calc_info_hash()