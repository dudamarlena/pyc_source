# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youkudownloader/youkudownloader/yesky.py
# Compiled at: 2013-02-19 21:05:22
__all__ = [
 'yesky_download']
import re, time
from common import *

def yesky_download(url, merge=True):
    html = get_html(url)
    title = r1('video_title\\s*[:=]\\s*["\\\']([^"\\\']+)["\\\']', html)
    title = unescape_html(title).decode('gb2312')
    assert title
    print 'Video title: ', title
    url = r1('FLV_URL\\s*[:=]\\s*[\\\'"]([^"\\\']+)[\\\'"]', html)
    assert url
    print 'Video url: ', url
    return download_urls([url], title, 'flv', total_size=None, merge=merge)


download = yesky_download
download_playlist = playlist_not_supported('yesky')

def main():
    script_main('yesky', yesky_download)


if __name__ == '__main__':
    main()