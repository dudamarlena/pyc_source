# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/gobry/src/canal/build/lib/canalweb/xspf.py
# Compiled at: 2008-12-18 16:11:18
__doc__ = 'Generate a playlist in XSPF format.'
from xml.sax import saxutils

def videos_to_xspf(videos):
    tracks = []
    for video in videos:
        if video.local_path:
            url = 'file://' + video.local_path
        else:
            url = video.url
        url = saxutils.escape(url)
        title = '%s %s (%d)' % (
         video.show.fullname, video.nice_date(), video.vid)
        title = saxutils.escape(title.encode('utf-8'))
        tracks.append('    <track>\n      <location>%(location)s</location>\n      <title>%(title)s</title>\n    </track>' % {'title': title, 'location': url})

    return '<?xml version="1.0" encoding="UTF-8"?>\n<playlist version="1" xmlns="http://xspf.org/ns/0/">\n  <trackList>\n%s\n  </trackList>\n</playlist>\n' % (('\n').join(tracks),)