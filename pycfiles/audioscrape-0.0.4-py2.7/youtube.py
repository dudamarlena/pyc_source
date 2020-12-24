# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/audioscrape/youtube.py
# Compiled at: 2016-12-05 03:11:37
"""Rip audio from YouTube videos."""
import os, re, pafy
try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode, urlopen

def scrape(query, include, exclude, quiet, overwrite):
    """Search YouTube and download audio from discovered videos."""
    html = urlopen('http://youtube.com/results?' + urlencode({'search_query': query})).read().decode('utf-8')
    video_ids = re.findall('href=\\"\\/watch\\?v=(.{11})', html)
    for video_id in video_ids:
        try:
            video = pafy.new(video_id)
        except:
            continue

        haystack = (' ').join([video.title, video.description, video.category] + video.keywords).lower()
        if include:
            if all(w not in haystack for w in include):
                continue
        if exclude:
            if any(w in haystack for w in exclude):
                continue
        audio = video.getbestaudio()
        if os.path.isfile(audio.filename) and not overwrite:
            continue
        audio.download(quiet=quiet)