# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hnc_forms_ext\media_helpers.py
# Compiled at: 2013-10-23 09:57:14
from urlparse import urlparse, parse_qsl
from hnc.apiclient import Mapping, IntegerField, TextField
import logging
from httplib2 import Http
import simplejson
log = logging.getLogger(__name__)

def getYoutubeVideoId(url):
    if not url or 'youtube' not in url.lower():
        return None
    scheme, netloc, path, params, query, fragment = urlparse(url)
    params = dict(parse_qsl(query))
    return params.get('v')


def getYoutubeMeta(request, url):
    videoId = getYoutubeVideoId(url)
    if not videoId:
        return
    else:
        meta = request.globals.cache.get(('YOUTUBE_{}').format(videoId))
        if not meta:
            try:
                log.info(('YOUTUBE Cache miss for {}').format(url))
                h = Http()
                resp, data = h.request(('https://gdata.youtube.com/feeds/api/videos/{}?v=2&alt=json').format(videoId))
                meta = simplejson.loads(data)
                request.globals.cache.set(('YOUTUBE_{}').format(videoId), meta)
                return meta
            except:
                return

        else:
            return meta
        return


def getVimeoVideoId(url):
    if not url or 'vimeo' not in url.lower():
        return
    scheme, netloc, path, params, query, fragment = urlparse(url)
    for e in path.split('/'):
        try:
            return int(e)
        except:
            pass

    return


class VimeoMeta(Mapping):
    id = IntegerField()
    user_id = IntegerField()
    thumbnail_small = TextField()
    thumbnail_medium = TextField()
    thumbnail_large = TextField()
    description = TextField()
    duration = TextField()
    mobile_url = TextField()
    title = TextField()
    user_name = TextField()


def getVimeoMeta(request, url):
    vimeoId = getVimeoVideoId(url)
    if not vimeoId:
        return
    else:
        meta = request.globals.cache.get(('VIMEO_{}').format(vimeoId))
        if not meta:
            try:
                log.info(('VIMEO Cache miss for {}').format(url))
                h = Http()
                resp, data = h.request(('http://vimeo.com/api/v2/video/{}.json').format(vimeoId))
                meta = VimeoMeta.wrap(simplejson.loads(data)[0])
                request.globals.cache.set(('VIMEO_{}').format(vimeoId), meta)
                return meta
            except:
                return

        else:
            return meta
        return


class SlideShareMeta(Mapping):
    id = IntegerField()
    slideshow_id = IntegerField()
    thumbnail = TextField()
    title = TextField()
    author_name = TextField()


def getSlideShareId(request, url):
    if not url:
        return
    else:
        scheme, netloc, path, params, query, fragment = urlparse(url)
        if 'embed_code' in path.split('/'):
            try:
                return int(query.split('/')[(-1)])
            except:
                pass

        elif 'slideshare' in netloc:
            try:
                result = getSlideshareMeta(request, url)
                return result.slideshow_id
            except:
                return

        return


def getSlideshareMeta(request, url):
    if not url:
        return
    else:
        meta = request.globals.cache.get(('SLIDESHARE_{}').format(url))
        if not meta:
            try:
                log.info(('Slideshare Cache miss for {}').format(url))
                h = Http()
                resp, content = h.request(('http://www.slideshare.net/api/oembed/2?url={}&format=json').format(url))
                meta = SlideShareMeta.wrap(simplejson.loads(content))
                request.globals.cache.set(('SLIDESHARE_{}').format(url), meta)
                return meta
            except:
                return

        else:
            return meta
        return