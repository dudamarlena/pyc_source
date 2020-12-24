# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plugins/indavideo.py
# Compiled at: 2012-02-18 05:20:19
"""
Downloader for http://indavideo.hu/
Author: András Veres-Szentkirályi <vsza@vsza.hu>, Stefan Marsiske <stefan.marsiske@gmail.com>
License: MIT
"""
from lxml import html
from urllib2 import urlopen
from urllib import unquote_plus
from urlparse import urlsplit
import re
__prefs__ = ('720', '360', 'webm')
__amftpl__ = '\x00\x03\x00\x00\x00\x01\x00!player.playerHandler.getVideoData\x00\x02/1\x00\x00\x00!\n\x00\x00\x00\x04\x02\x00\n{vid}\x00@(\x00\x00\x00\x00\x00\x00\x02\x00\x00\x02\x00\x00'

def convert(url):
    """Downloads the video from the URL in the url parameter"""
    if not urlsplit(unquote_plus(url))[1].endswith('indavideo.hu'):
        return url
    videos = getvideos(url)
    if not videos:
        return url
    return preferred(videos)


def preferred(videos):
    """Returns the preferred URL from the iterable in the videos parameter"""
    for pref in __prefs__:
        for video in videos:
            if pref in video:
                return video

    return videos[0]


def url2vid(url):
    """Returns the ID of the video on the URL in the url parameter"""
    video = html.parse(urlopen(url)).getroot()
    if video == None:
        return
    else:
        video_src = video.xpath('/html/head/link[@rel = "video_src"]/@href | /html/head/meta[@property="og:video"]/@content')[0]
        return re.search('vID=([^&]+)&', video_src).group(1)


def getvideos(url):
    """Returns URLs that contain the video on the URL in the url parameter"""
    vid = url2vid(url)
    if vid == None:
        return
    else:
        amfreq = __amftpl__.format(vid=vid)
        amfresp = urlopen('http://amfphp.indavideo.hu/gateway.php', amfreq).read()
        return set(re.findall('http://[a-zA-Z0-9/._]+\\.(?:mp4|webm)', amfresp))