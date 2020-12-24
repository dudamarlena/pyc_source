# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youkudownloader/youkudownloader/chinanews.py
# Compiled at: 2013-02-19 21:05:22
__all__ = [
 'chinanews_download']
import re, time
from common import *

def chinanews_download(url, merge=True):
    html = get_decoded_html(url)
    title = r1('newstitle\\s*[:=]\\s*["\']([^\'"]+)[\'"]', html)
    if not title:
        title = r1('newstitle" +type="hidden" +value=[\'"]([^\'"]+)[\'"]', html)
    title = unescape_html(title).decode('gb2312')
    assert title
    url = r1('vInfo=([^\\\'"]+)\\.mp4', html) + '.mp4'
    assert url
    print 'Videos title', title
    print 'Videos url:', url
    download_urls([url], title, 'mp4', total_size=None, merge=merge)
    return


download = chinanews_download
download_playlist = playlist_not_supported('chinanews')

def main():
    script_main('chinanews', chinanews_download)


if __name__ == '__main__':
    main()