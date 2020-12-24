# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imagesitemaps/__init__.py
# Compiled at: 2012-05-03 12:04:52
from django.core import urlresolvers, paginator
from django.contrib.sitemaps import Sitemap
from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site
import urllib

class ImageTagException(Exception):
    pass


REQUIRED_IMAGE_TAGS = [
 'loc']
OPTIONAL_IMAGE_TAGS = [
 'caption',
 'geo_location',
 'title',
 'license']

class ImageSitemap(Sitemap):
    """
    Represents a Google image sitemap.
    """

    def image_loc(self, img):
        return img.get_absolute_url()

    def image_title(self, img):
        return unicode(img)

    def images(self, obj):
        return [
         obj]

    def get_urls(self, page=1, site=None):
        if site is None:
            if Site._meta.installed:
                try:
                    site = Site.objects.get_current()
                except Site.DoesNotExist:
                    pass

            if site is None:
                raise ImproperlyConfigured('In order to use Sitemaps you must either use the sites framework or pass in a Site or RequestSite object in your view code.')
        urls = []
        get = self._Sitemap__get
        ATTR_PREFIX = 'image_'
        for item in self.paginator.page(page).object_list:
            loc = 'http://%s%s' % (site.domain, get('location', item))
            image_tags = []
            for attr in dir(self):
                if attr.startswith(ATTR_PREFIX):
                    image_tags.append(attr[len(ATTR_PREFIX):])

            url_info = {'location': loc}
            optional_tags = image_tags[:]
            url_info['images'] = []
            for idx, img in enumerate(self.images(item)):
                url_info['images'].append({})
                for req_tag in REQUIRED_IMAGE_TAGS:
                    if req_tag not in image_tags:
                        raise ImageTagException('<image:%s> is a required tag.' % req_tag)
                    url_info['images'][idx][req_tag] = get('%s%s' % (ATTR_PREFIX, req_tag), img, None)
                    if req_tag in optional_tags:
                        optional_tags.remove(req_tag)

                for tag in optional_tags:
                    if tag not in OPTIONAL_IMAGE_TAGS:
                        raise ImageTagException('<image:%s> tag is not supported.' % tag)

                url_info['images'][idx]['optional'] = {}
                for tag in optional_tags:
                    url_info['images'][idx]['optional'][tag] = get('%s%s' % (ATTR_PREFIX, tag), img, None)

            urls.append(url_info)

        return urls