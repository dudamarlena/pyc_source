# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/badgr/context_processors.py
# Compiled at: 2012-09-15 17:11:48
import flickrapi
from django.core.cache import cache
from badgr import settings

def flickr(request):
    """Return the most recent photos for user."""
    flickr_badge = cache.get('flickr_badge')
    if flickr_badge:
        return {'flickr_badge': flickr_badge}
    else:
        flickr_badge = []
        flickr = flickrapi.FlickrAPI(settings.FLICKR_APIKEY)
        try:
            pool = flickr.photos_search(user_id=settings.FLICKR_USERID, per_page=settings.FLICKR_NUMPHOTOS)
        except:
            flickr_badge = None
        else:
            if pool.get('stat') == 'ok':
                for photo in pool[0]:
                    filename = '%s_%s' % (photo.get('id'), photo.get('secret'))
                    if settings.FLICKR_IMAGESIZE:
                        filename += '_%s' % settings.FLICKR_IMAGESIZE
                    filename += '.jpg'
                    photo.set('image', 'http://farm%s.static.flickr.com/%s/%s' % (
                     photo.get('farm'),
                     photo.get('server'),
                     filename))
                    photo.set('url', 'http://www.flickr.com/photos/%s/%s' % (
                     photo.get('owner'), photo.get('id')))
                    flickr_badge.append(photo.attrib)

            cache.set('flickr_badge', flickr_badge, settings.FLICKR_TIMEOUT)

        return {'flickr_badge': flickr_badge}