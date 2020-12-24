# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youkudownloader/youkudownloader/cntv.py
# Compiled at: 2013-02-19 21:05:22
__all__ = [
 'cntv_download', 'cntv_download_by_id']
from common import *
import json, re

def cntv_download_by_id(id, title=None, output_dir='.', merge=True):
    assert id
    info = json.loads(get_html('http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=' + id).decode('utf-8'))
    title = title or info['title']
    video = info['video']
    alternatives = [ x for x in video.keys() if x.startswith('chapters') ]
    assert alternatives in (['chapters'], ['chapters', 'chapters2']), alternatives
    chapters = video['chapters2'] if 'chapters2' in video else video['chapters']
    urls = [ x['url'] for x in chapters ]
    ext = r1('\\.([^.]+)$', urls[0])
    assert ext in ('flv', 'mp4')
    print 'Video ext: ', ext
    print 'Video url: ', urls
    print 'Video title: ', title
    download_urls(urls, title, str(ext), total_size=None, merge=merge)
    return


def cntv_download(url, merge=True):
    html = get_html(url)
    id = r1('<!--repaste.video.code.begin-->(\\w+)<!--repaste.video.code.end-->', html)
    if not id:
        id = r1('http://xiyou.cntv.cn/v-([\\w-]+)\\.html', url)
    if not id:
        id = r1('"videoCenterId","(\\w+)"', html)
    if not id:
        raise NotImplementedError(url)
    cntv_download_by_id(id, merge=merge)


download = cntv_download
download_playlist = playlist_not_supported('cntv')

def main():
    script_main('cntv', cntv_download)


if __name__ == '__main__':
    main()