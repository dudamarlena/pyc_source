# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youkudownloader/youkudownloader/mtime.py
# Compiled at: 2013-02-19 21:05:22
__all__ = [
 'mtime_download']
import re
from common import *

def mtime_download_by_vid(vid, merge):
    import json
    js = json.loads(get_html('http://api.mtime.com/trailer/getvideo.aspx?vid=' + vid))
    title = js['title']
    if not title:
        raise AssertionError
        ext = 'flv'
        ext = js.has_key(ext) or 'mp4'
    url = js[ext]
    assert url
    download_urls([url], title, ext, total_size=None, merge=merge)
    return


def mtime_download(url, merge=True):
    html = get_html(url)
    vid = r1('vid[:=](\\d+)', html)
    return mtime_download_by_vid(vid, merge)


download = mtime_download
download_playlist = playlist_not_supported('mtime')

def main():
    script_main('mtime', mtime_download)


if __name__ == '__main__':
    main()