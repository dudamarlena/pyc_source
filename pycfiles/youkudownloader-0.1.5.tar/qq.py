# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youkudownloader/youkudownloader/qq.py
# Compiled at: 2013-02-19 21:05:22
__all__ = [
 'qq_download_by_id']
import re
from common import *

def qq_download_by_id(id, title, merge=True):
    url = 'http://vsrc.store.qq.com/%s.flv' % id
    print 'Video url: ', url
    download_urls([url], title, 'flv', total_size=None, merge=merge)
    return


def qq_download(url, merge=True):
    html = get_html(url, 'utf-8')
    id = r1('vid=(\\w+)', url)
    if not id:
        id = r1('vid\\w*:\\w*"(\\w+)"\\w*,', html)
    if not id:
        raise AssertionError("can't find video info")
        title = r1('v?id="' + id + '" +info="([^"]+)"', html)
        if not title:
            title = r1('v?id="' + id + '" +title="([^"]+)"', html)
        title = title or r1('title\\w*:\\w*"([^"]+)"', html)
    assert title, "can't get title"
    title = unescape_html(title)
    print 'Video title: ', title
    return qq_download_by_id(id, title)


download = qq_download
download_playlist = playlist_not_supported('qq')

def main():
    script_main('qq', qq_download)


if __name__ == '__main__':
    main()