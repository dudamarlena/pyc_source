# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gobry/src/canal/build/lib/canalweb/test_xspf.py
# Compiled at: 2008-12-18 16:14:47
import datetime, canalweb
from canalweb import vod
from canalweb import xspf

def test_format_xspf():
    now = datetime.date(2008, 12, 12)
    videos = [
     vod.VOD('http://foo/bar', canalweb.SHOW_BY_NICK['zapping'], 456, now),
     vod.VOD('http://foo/baz', canalweb.SHOW_BY_NICK['zapping'], 457, now)]
    videos[1].local_path = '/to/the/file'
    data = xspf.videos_to_xspf(videos)
    print data
    assert data == '<?xml version="1.0" encoding="UTF-8"?>\n<playlist version="1" xmlns="http://xspf.org/ns/0/">\n  <trackList>\n    <track>\n      <location>http://foo/bar</location>\n      <title>Le Zapping 2008-12-12 (456)</title>\n    </track>\n    <track>\n      <location>file:///to/the/file</location>\n      <title>Le Zapping 2008-12-12 (457)</title>\n    </track>\n  </trackList>\n</playlist>\n'