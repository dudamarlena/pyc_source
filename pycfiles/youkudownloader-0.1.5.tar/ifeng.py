# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youkudownloader/youkudownloader/ifeng.py
# Compiled at: 2013-02-19 21:05:22
__all__ = [
 'ifeng_download', 'ifeng_download_by_id']
from common import *

def ifeng_download_by_id(id, title=None, merge=True):
    assert r1('([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', id), id
    url = 'http://v.ifeng.com/video_info_new/%s/%s/%s.xml' % (id[(-2)], id[-2:], id)
    xml = get_html(url, 'utf-8')
    title = r1('Name="([^"]+)"', xml)
    title = unescape_html(title)
    url = r1('VideoPlayUrl="([^"]+)"', xml)
    from random import randint
    r = randint(10, 19)
    url = url.replace('http://video.ifeng.com/', 'http://video%s.ifeng.com/' % r)
    assert url.endswith('.mp4')
    download_urls([url], title, 'mp4', total_size=None, merge=merge)
    return


def ifeng_download(url, merge=True):
    id = r1('[/#]([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', url)
    if id:
        return ifeng_download_by_id(id)
    html = get_html(url)
    id = r1('var vid="([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"', html)
    assert id, "can't find video info"
    return ifeng_download_by_id(id)


download = ifeng_download
download_playlist = playlist_not_supported('ifeng')

def main():
    script_main('ifeng', ifeng_download)


if __name__ == '__main__':
    main()