# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youkudownloader/youkudownloader/ku6.py
# Compiled at: 2013-02-19 21:05:22
__all__ = [
 'ku6_download', 'ku6_download_by_id']
import json, re
from common import *

def ku6_download_by_id(id, title=None, output_dir='.', merge=True):
    data = json.loads(get_html('http://v.ku6.com/fetch.htm?t=getVideo4Player&vid=%s...' % id))['data']
    t = data['t']
    f = data['f']
    title = title or t
    assert title
    urls = f.split(',')
    size = float(re.search('\\d+$', str(data['videosize'])).group(0))
    ext = re.sub('.*\\.', '', urls[0])
    assert ext in ('flv', 'mp4', 'f4v'), ext
    ext = {'f4v': 'flv'}.get(ext, ext)
    download_urls(urls, title, ext, total_size=size, merge=merge)


def ku6_download(url, merge=True):
    patterns = ['http://v.ku6.com/special/show_\\d+/(.*)\\.\\.\\.html',
     'http://v.ku6.com/show/(.*)\\.\\.\\.html',
     'http://my.ku6.com/watch\\?.*v=(.*)\\.\\..*']
    ids = r1_of(patterns, url)
    ku6_download_by_id(ids, merge=merge)


download = ku6_download
download_playlist = playlist_not_supported('ku6')

def main():
    script_main('ku6', ku6_download)


if __name__ == '__main__':
    main()