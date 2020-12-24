# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/videos/feeds.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 1037 bytes
from tendenci.apps.rss.feedsmanager import SubFeed
from tendenci.apps.perms.utils import PUBLIC_FILTER
from tendenci.apps.sitemaps import TendenciSitemap
from tendenci.apps.videos.models import Video

class LatestEntriesFeed(SubFeed):
    title = 'Latest Videos'
    link = '/videos/'
    description = 'Latest Videos'

    def items(self):
        items = (Video.objects.filter)(**PUBLIC_FILTER).order_by('-create_dt')[:20]
        return items

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.embed_code() + item.description

    def item_pubdate(self, item):
        return item.create_dt

    def item_link(self, item):
        return item.get_absolute_url()


class VideoSitemap(TendenciSitemap):
    __doc__ = ' Sitemap information for videos '
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        items = (Video.objects.filter)(**PUBLIC_FILTER).order_by('-create_dt')
        return items

    def lastmod(self, obj):
        return obj.create_dt