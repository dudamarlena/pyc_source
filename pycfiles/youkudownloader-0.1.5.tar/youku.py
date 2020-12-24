# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/youku/youkudownloader/youku.py
# Compiled at: 2013-02-19 22:24:09
__all__ = [
 'youku_download', 'youku_download_playlist', 'youku_download_by_id']
import urllib2, json
from random import randint
from time import time
import re, sys
from common import *

def find_video_id_from_url(url):
    patterns = [
     '^http://v.youku.com/v_show/id_([\\w=]+).html',
     '^http://player.youku.com/player.php/sid/([\\w=]+)/v.swf',
     '^loader\\.swf\\?VideoIDS=([\\w=]+)',
     '^([\\w=]+)$']
    return r1_of(patterns, url)


def find_video_id_from_show_page(url):
    return re.search('<div class="btnplay">.*href="([^"]+)"', get_html(url)).group(1)


def youku_url(url):
    id = find_video_id_from_url(url)
    if id:
        return 'http://v.youku.com/v_show/id_%s.html' % id
    if re.match('http://www.youku.com/show_page/id_\\w+.html', url):
        return find_video_id_from_show_page(url)
    if re.match('http://v.youku.com/v_playlist/\\w+.html', url):
        return url
    raise Exception('Invalid youku URL: ' + url)


def trim_title(title):
    title = title.replace(' - 视频 - 优酷视频 - 在线观看', '')
    title = title.replace(' - 专辑 - 优酷视频', '')
    title = re.sub('—([^—]+)—优酷网，视频高清在线观看', '', title)
    return title


def parse_video_title(url, page):
    if re.search('v_playlist', url):
        title = r1_of(['<div class="show_title" title="([^"]+)">[^<]', '<title>([^<>]*)</title>'], page).decode('utf-8')
    else:
        title = r1_of(['<div class="show_title" title="([^"]+)">[^<]', '<meta name="title" content="([^"]*)"'], page).decode('utf-8')
    assert title
    title = trim_title(title)
    if re.search('v_playlist', url) and re.search('-.*\\S+', title):
        title = re.sub('^[^-]+-\\s*', '', title)
    title = re.sub('—专辑：.*', '', title)
    title = unescape_html(title)
    subtitle = re.search('<span class="subtitle" id="subtitle">([^<>]*)</span>', page)
    if subtitle:
        subtitle = subtitle.group(1).decode('utf-8').strip()
    if subtitle == title:
        subtitle = None
    if subtitle:
        title += '-' + subtitle
    return title


def parse_playlist_title(url, page):
    if re.search('v_playlist', url):
        title = re.search('<title>([^<>]*)</title>', page).group(1).decode('utf-8')
    else:
        title = re.search('<meta name="title" content="([^"]*)"', page).group(1).decode('utf-8')
    title = trim_title(title)
    if re.search('v_playlist', url) and re.search('-.*\\S+', title):
        title = re.sub('^[^-]+-\\s*', '', title)
    title = re.sub('^.*—专辑：《(.+)》', '\\1', title)
    title = unescape_html(title)
    return title


def parse_page(url):
    url = youku_url(url)
    page = get_html(url)
    id2 = re.search("var\\s+videoId2\\s*=\\s*'(\\S+)'", page).group(1)
    title = parse_video_title(url, page)
    return (id2, title)


def get_info(videoId2):
    return json.loads(get_html('http://v.youku.com/player/getPlayList/VideoIDS/' + videoId2))


def find_video(info, stream_type=None):
    segs = info['data'][0]['segs']
    types = segs.keys()
    if not stream_type:
        for x in ['hd2', 'mp4', 'flv']:
            if x in types:
                stream_type = x
                break
        else:
            raise NotImplementedError()

    assert stream_type in ('hd2', 'mp4', 'flv')
    file_type = {'hd2': 'flv', 'mp4': 'mp4', 'flv': 'flv'}[stream_type]
    seed = info['data'][0]['seed']
    source = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890')
    mixed = ''
    while source:
        seed = seed * 211 + 30031 & 65535
        index = seed * len(source) >> 16
        c = source.pop(index)
        mixed += c

    ids = info['data'][0]['streamfileids'][stream_type].split('*')[:-1]
    vid = ('').join(mixed[int(i)] for i in ids)
    sid = '%s%s%s' % (int(time() * 1000), randint(1000, 1999), randint(1000, 9999))
    urls = []
    for s in segs[stream_type]:
        no = '%02x' % int(s['no'])
        url = 'http://f.youku.com/player/getFlvPath/sid/%s_%s/st/%s/fileid/%s%s%s?K=%s&ts=%s' % (sid, no, file_type, vid[:8], no.upper(), vid[10:], s['k'], s['seconds'])
        urls.append((url, int(s['size'])))

    return urls


def file_type_of_url(url):
    return str(re.search('/st/([^/]+)/', url).group(1))


def youku_download_by_id(id2, title, output_dir='.', stream_type=None, merge=True):
    info = get_info(id2)
    urls, sizes = zip(*find_video(info, stream_type))
    total_size = sum(sizes)
    download_urls(urls, title, file_type_of_url(urls[0]), total_size, output_dir, merge=merge)


def youku_download(url, output_dir='', stream_type=None, merge=True):
    id2, title = parse_page(url)
    if type(title) == unicode:
        title = title.encode(default_encoding)
        title = title.replace('?', '-')
    youku_download_by_id(id2, title, output_dir, merge=merge)


def parse_playlist_videos(html):
    return re.findall('id="A_(\\w+)"', html)


def parse_playlist_pages(html):
    m = re.search('<ul class="pages">.*?</ul>', html, flags=re.S)
    if m:
        urls = re.findall('href="([^"]+)"', m.group())
        x1, x2, x3 = re.match('^(.*page_)(\\d+)(_.*)$', urls[(-1)]).groups()
        return [ 'http://v.youku.com%s%s%s?__rt=1&__ro=listShow' % (x1, i, x3) for i in range(2, int(x2) + 1) ]
    else:
        return []


def parse_playlist(url):
    html = get_html(url)
    video_id = re.search("var\\s+videoId\\s*=\\s*'(\\d+)'", html).group(1)
    show_id = re.search('var\\s+showid\\s*=\\s*"(\\d+)"', html).group(1)
    list_url = 'http://v.youku.com/v_vpofficiallist/page_1_showid_%s_id_%s.html?__rt=1&__ro=listShow' % (show_id, video_id)
    html = get_html(list_url)
    ids = parse_playlist_videos(html)
    for url in parse_playlist_pages(html):
        ids.extend(parse_playlist_videos(get_html(url)))

    return ids


def parse_vplaylist(url):
    id = r1_of(['^http://www.youku.com/playlist_show/id_(\\d+)(?:_ascending_\\d_mode_pic(?:_page_\\d+)?)?.html',
     '^http://v.youku.com/v_playlist/f(\\d+)o[01]p\\d+.html',
     '^http://u.youku.com/user_playlist/pid_(\\d+)_id_[\\w=]+(?:_page_\\d+)?.html'], url)
    assert id, 'not valid vplaylist url: ' + url
    url = 'http://www.youku.com/playlist_show/id_%s.html' % id
    n = int(re.search('<span class="num">(\\d+)</span>', get_html(url)).group(1))
    return [ 'http://v.youku.com/v_playlist/f%so0p%s.html' % (id, i) for i in range(n) ]


def youku_download_playlist(url, create_dir=False, merge=True):
    if re.match('http://www.youku.com/show_page/id_\\w+.html', url):
        url = find_video_id_from_show_page(url)
    if re.match('http://www.youku.com/playlist_show/id_\\d+(?:_ascending_\\d_mode_pic(?:_page_\\d+)?)?.html', url):
        ids = parse_vplaylist(url)
    else:
        if re.match('http://v.youku.com/v_playlist/f\\d+o[01]p\\d+.html', url):
            ids = parse_vplaylist(url)
        elif re.match('http://u.youku.com/user_playlist/pid_(\\d+)_id_[\\w=]+(?:_page_\\d+)?.html', url):
            ids = parse_vplaylist(url)
        else:
            assert re.match('http://v.youku.com/v_show/id_([\\w=]+).html', url), 'URL not supported as playlist'
            ids = parse_playlist(url)
        output_dir = '.'
        if create_dir:
            title = parse_playlist_title(url, get_html(url))
            title = title.encode(default_encoding)
            title = title.replace('?', '-')
            import os
            if not os.path.exists(title):
                os.makedirs(title)
            output_dir = title
        for i, id in enumerate(ids):
            print 'Downloading %s of %s videos...' % (i + 1, len(ids))
            youku_download(id, output_dir=output_dir, merge=merge)


download = youku_download
download_playlist = youku_download_playlist

def main():
    script_main('youku', youku_download, youku_download_playlist)


if __name__ == '__main__':
    main()