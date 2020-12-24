# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youkudownloader/youkudownloader/pptv.py
# Compiled at: 2013-02-19 21:05:22
__all__ = [
 'pptv_download', 'pptv_download_by_id']
import re, urllib
from common import *
import hashlib, time

def pptv_download_by_id(id, merge=True):
    xml = get_html('http://web-play.pptv.com/webplay3-0-%s.xml' % id)
    host = r1('<sh>([^<>]+)</sh>', xml)
    st = r1('<st>([^<>]+)</st>', xml)
    t = (time.mktime(time.strptime(st.replace(' UTC', ''))) - 60000) / 1000
    ts = time.strftime('%a %b %d %Y %H:%M:%S UTC', time.localtime(t))
    key = hashlib.md5(str(t)).hexdigest()
    rids = re.findall('rid="([^"]+)"', xml)
    rid = r1('rid="([^"]+)"', xml)
    title = r1('nm="([^"]+)"', xml)
    assert title
    print 'Video title: ', title
    pieces = re.findall('<sgm no="(\\d+)"[^fs]*fs="(\\d+)"', xml)
    numbers, fs = zip(*pieces)
    urls = [ 'http://%s/%s/%s?key=%s' % (host, i, rid, key) for i in numbers ]
    total_size = sum(map(int, fs))
    assert rid.endswith('.mp4')
    print 'Video url: ', urls
    download_urls(urls, title, 'mp4', total_size=total_size, merge=merge)


def pptv_download(url, merge=True):
    html = get_html(url)
    id = r1('webcfg\\s*=\\s*{"id":\\s*(\\d+)', html)
    if not id:
        id_str = r1('var allList = \\[(["\\\',\\d]+)\\]', html)
        ids = re.findall('"(\\d+)"', id_str)
        for id in ids:
            pptv_download_by_id(id, merge=merge)

    else:
        pptv_download_by_id(id, merge=merge)


download = pptv_download
download_playlist = playlist_not_supported('pptv')

def main():
    script_main('pptv', pptv_download)


if __name__ == '__main__':
    main()