# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/linkify/linkify.py
# Compiled at: 2009-10-28 14:01:28
from urlparse import urlparse

def linkify(url, width=400, height=200):
    url = validate_url(url)
    if 'youtube' in url.netloc and '/watch' in url.path:
        youtube_url = 'http://youtube.com/v/' + str(url.query[2:len(url.query)])
        video_link = generate_tag(youtube_url, width, height)
    elif 'vimeo' in url.netloc:
        vimeo_url = 'http://vimeo.com/moogaloop.swf?clip_id=' + str(url.path.strip('/')) + '&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=0'
        video_link = generate_tag(vimeo_url, width, height)
    else:
        return False
    return video_link


def validate_url(url):
    try:
        url = urlparse(url)
        return url
    except ValueError:
        print 'Not a valid URL'


def generate_tag(video_link, width, height):
    object_tag = '<object width="' + str(width) + '" height="' + str(height) + '"><param name="movie" value="' + video_link + '"/><param name="wmode" value="transparent"/><embed src="' + video_link + '" type="application/x-shockwave-flash" wmode="transparent" width="' + str(width) + '" height="' + str(height) + '" /></object>'
    return object_tag