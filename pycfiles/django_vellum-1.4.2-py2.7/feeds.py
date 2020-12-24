# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vellum/feeds.py
# Compiled at: 2012-11-04 15:50:18
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.core.urlresolvers import reverse
from taggit.models import Tag
from vellum import settings
from vellum.models import Post, Category

class PostFeed(Feed):
    description = settings.BLOG_DESCRIPTION
    title_template = 'feeds/post_title.html'
    description_template = 'feeds/post_description.html'

    def title(self, obj):
        site = Site.objects.get_current().name
        if obj:
            return '%s: %s' % (site, obj)
        return site

    def link(self):
        return reverse('vellum')

    def items(self):
        return Post.objects.published()[:settings.BLOG_FEEDSIZE]

    def item_pubdate(self, obj):
        return obj.publish

    def item_author_name(self, item):
        return item.author

    def item_categories(self, item):
        return item.categories.all()


class CategoryFeed(PostFeed):

    def get_object(self, request, slug):
        return Category.objects.get(slug__exact=slug)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return 'Posts recently categorized as %s' % obj.title

    def items(self, obj):
        return obj.post_set.published()[:settings.BLOG_FEEDSIZE]


class TagFeed(CategoryFeed):

    def get_object(self, request, slug):
        return Tag.objects.get(slug__exact=slug)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('vellum_tag_feed', kwargs={'slug': obj.slug})

    def description(self, obj):
        return 'Posts recently tagged with %s' % obj.name

    def items(self, obj):
        return Post.objects.published().filter(tags__name__in=[obj.name])[:settings.BLOG_FEEDSIZE]


class CommentsFeed(Feed):
    _site = Site.objects.get_current()
    title = '%s comment feed' % _site.name
    description = '%s comments feed.' % _site.name

    def link(self):
        return reverse('vellum')

    def items(self):
        ctype = ContentType.objects.get_for_model(Post)
        return Comment.objects.filter(content_type=ctype)[:settings.BLOG_FEEDSIZE]

    def item_pubdate(self, obj):
        return obj.submit_date