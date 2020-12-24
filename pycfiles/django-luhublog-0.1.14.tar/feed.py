# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johsanca/Projects/luhu-blog-app/luhublog/feed.py
# Compiled at: 2015-10-22 11:15:07
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse, reverse_lazy
from models import Entry, Blog
BLOG = Blog.objects.get_blog()

class BlogFeed(Feed):
    title = getattr(BLOG, 'title', '')
    link = reverse_lazy('luhublog-list')
    description = getattr(BLOG, 'tag_line', '')

    def items(self):
        return Entry.objects.all()

    def item_description(self, item):
        return item.lead_entry

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.start_publication

    def item_link(self, item):
        return reverse('lihublog-detail', kwargs={'slug': item.slug})

    def item_author_name(self, item):
        return item.author.full_name