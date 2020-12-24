# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/djangopypi/feeds.py
# Compiled at: 2015-10-27 08:49:00
from django.shortcuts import get_object_or_404
try:
    from django.contrib.syndication.views import Feed, FeedDoesNotExist
except ImportError:
    from django.contrib.syndication.feeds import Feed as BaseFeed, FeedDoesNotExist
    from django.http import HttpResponse, Http404
    from django.core.exceptions import ObjectDoesNotExist

    class Feed(BaseFeed):

        def __call__(self, request, *args, **kwargs):
            try:
                obj = self.get_object(request, *args, **kwargs)
            except ObjectDoesNotExist:
                raise Http404('Feed object does not exist.')

            feedgen = self.get_feed(obj, request)
            response = HttpResponse(mimetype=feedgen.mime_type)
            feedgen.write(response, 'utf-8')
            return response


from djangopypi.models import Package, Release

class ReleaseFeed(Feed):
    """ A feed of releases either for the site in general or for a specific 
    package. """

    def get_object(self, request, package=None, **kwargs):
        if package:
            return get_object_or_404(Package, name=package)
        return request.build_absolute_uri('/')

    def link(self, obj):
        if isinstance(obj, Package):
            return obj.get_absolute_url()
        return obj

    def title(self, obj):
        if isinstance(obj, Package):
            return 'Releases for %s' % (obj.name,)
        return 'Package index releases'

    def description(self, obj):
        if isinstance(obj, Package):
            return 'Recent releases for the package: %s' % (obj.name,)
        return 'Recent releases on the package index server'

    def items(self, obj):
        if isinstance(obj, Package):
            return obj.releases.filter(hidden=False).order_by('-created')[:25]
        return Release.objects.filter(hidden=False).order_by('-created')[:40]

    def item_description(self, item):
        if isinstance(item, Release):
            if item.summary:
                return item.summary
        return super(ReleaseFeed, self).item_description(item)