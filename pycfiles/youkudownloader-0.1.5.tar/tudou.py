# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youkudownloader/youkudownloader/tudou.py
# Compiled at: 2013-02-19 21:05:22
__all__ = [
 'tudou_download', 'tudou_download_playlist', 'tudou_download_by_id', 'tudou_download_by_iid']
from common import *

def tudou_download_by_iid(iid, title, merge=True):
    xml = get_html('http://v2.tudou.com/v?it=' + iid + '&st=1,2,3,4,99')
    from xml.dom.minidom import parseString
    doc = parseString(xml)
    title = title or doc.firstChild.getAttribute('tt') or doc.firstChild.getAttribute('title')
    urls = [ (int(n.getAttribute('brt')), n.firstChild.nodeValue.strip()) for n in doc.getElementsByTagName('f') ]
    url = max(urls, key=lambda x: x[0])[1]
    assert 'f4v' in url
    download_urls([url], title, 'flv', total_size=None, merge=merge)
    return


def tudou_download_by_id(id, title, merge=True):
    html = get_html('http://www.tudou.com/programs/view/%s/' % id)
    iid = r1('iid\\s*=\\s*(\\S+)', html)
    tudou_download_by_iid(iid, title, merge=merge)


def tudou_download(url, merge=True):
    html = get_decoded_html(url)
    iid = r1('iid\\s*[:=]\\s*(\\d+)', html)
    assert iid
    title = r1('kw\\s*[:=]\\s*"([^"]+)"', html)
    assert title
    title = unescape_html(title)
    tudou_download_by_iid(iid, title, merge=merge)


def parse_playlist(url):
    aid = r1('http://www.tudou.com/playlist/p/a(\\d+)(?:i\\d+)?\\.html', url)
    html = get_decoded_html(url)
    if not aid:
        aid = r1("aid\\s*[:=]\\s*'(\\d+)'", html)
    if re.match('http://www.tudou.com/albumcover/', url):
        atitle = r1("title\\s*:\\s*'([^']+)'", html)
    elif re.match('http://www.tudou.com/playlist/p/', url):
        atitle = r1('atitle\\s*=\\s*"([^"]+)"', html)
    else:
        raise NotImplementedError(url)
    assert aid
    assert atitle
    import json
    url = 'http://www.tudou.com/playlist/service/getAlbumItems.html?aid=' + aid
    return [ (atitle + '-' + x['title'], str(x['itemId'])) for x in json.loads(get_html(url))['message'] ]


def tudou_download_playlist(url, create_dir=False, merge=True):
    if create_dir:
        raise NotImplementedError('please report a bug so I can implement this')
    videos = parse_playlist(url)
    for i, (title, id) in enumerate(videos):
        print 'Downloading %s of %s videos...' % (i + 1, len(videos))
        tudou_download_by_iid(id, title, merge=merge)


download = tudou_download
download_playlist = tudou_download_playlist

def main():
    script_main('tudou', tudou_download, tudou_download_playlist)


if __name__ == '__main__':
    main()