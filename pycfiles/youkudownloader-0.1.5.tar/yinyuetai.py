# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youkudownloader/youkudownloader/yinyuetai.py
# Compiled at: 2013-02-19 21:05:22
__all__ = [
 'yinyuetai_download', 'yinyuetai_download_by_id']
from common import *

def url_info(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    headers = response.headers
    type = headers['content-type']
    mapping = {'video/mp4': 'mp4'}
    assert type in mapping, type
    type = mapping[type]
    size = int(headers['content-length'])
    return (
     type, size)


def yinyuetai_download_by_id(id, title=None, merge=True):
    assert title
    amf = get_html('http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId=' + id)
    url = r1('(http://\\w+\\.yinyuetai\\.com/uploads/videos/common/\\w+\\.(?:flv|mp4)\\?(?:sc=[a-f0-9]{16}|v=\\d{12}))', amf)
    assert url
    ext, size = url_info(url)
    download_urls([url], title, ext, total_size=size, merge=merge)


def yinyuetai_download(url, merge=True):
    id = r1('http://www.yinyuetai.com/video/(\\d+)$', url)
    assert id
    html = get_html(url, 'utf-8')
    import urllib
    title = r1('<meta property="og:title" content="([^"]+)"/>', html)
    assert title
    title = urllib.unquote(title)
    title = escape_file_path(title)
    yinyuetai_download_by_id(id, title, merge=merge)


download = yinyuetai_download
download_playlist = playlist_not_supported('yinyuetai')

def main():
    script_main('yinyuetai', yinyuetai_download)


if __name__ == '__main__':
    main()