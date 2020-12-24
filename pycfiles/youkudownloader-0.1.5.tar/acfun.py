# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youkudownloader/youkudownloader/acfun.py
# Compiled at: 2013-02-19 21:05:22
__all__ = [
 'acfun_download']
import re
from common import *
from sina import sina_download_by_vid
from youku import youku_download_by_id
from tudou import tudou_download_by_iid
from qq import qq_download_by_id
import json

def get_srt_json(id):
    url = 'http://comment.acfun.tv/%s.json' % id
    return get_html(url)


def acfun_download_by_id(id, title, merge=True):
    info = json.loads(get_html('http://www.acfun.tv/api/getVideoByID.aspx?vid=' + id))
    t = info['vtype']
    vid = info['vid']
    if t == 'sina':
        sina_download_by_vid(vid, title, merge=merge)
    elif t == 'youku':
        youku_download_by_id(vid, title, merge=merge)
    elif t == 'tudou':
        tudou_download_by_iid(vid, title, merge=merge)
    elif t == 'qq':
        qq_download_by_id(vid, title, merge=merge)
    else:
        raise NotImplementedError(t)
    srt = get_srt_json(vid)
    with open(title + '.json', 'w') as (x):
        x.write(srt)


def acfun_download(url, merge=True):
    assert re.match('http://www.acfun.tv/v/ac(\\d+)', url)
    html = get_html(url).decode('utf-8')
    title = r1('<h1 id="title-article" class="title"[^<>]*>([^<>]+)<span', html)
    assert title
    title = unescape_html(title)
    title = escape_file_path(title)
    title = title.replace(' - AcFun.tv', '')
    id = r1('\\[[Vv]ideo\\](\\d+)\\[/[Vv]ideo\\]', html)
    if id:
        return acfun_download_by_id(id, title, merge=merge)
    id = r1('<embed [^<>]* src="[^"]+id=(\\d+)[^"]+"', html)
    assert id
    sina_download_by_vid(id, title, merge=merge)


download = acfun_download
download_playlist = playlist_not_supported('acfun')

def main():
    script_main('acfun', acfun_download)


if __name__ == '__main__':
    main()