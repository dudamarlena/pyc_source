# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/sphboard/feeds.py
# Compiled at: 2012-03-17 12:42:14
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext as _
from sphene.sphboard.models import Category, Post
from sphene.community.models import Group

class LatestThreads(Feed):

    def get_object(self, request, category_id, group=None):
        category = Category.objects.get(pk=category_id)
        if not category.has_view_permission():
            raise PermissionDenied
        return category

    def title(self, obj):
        return _('Latest threads in %(obj_name)s') % {'obj_name': obj.name}

    def description(self, obj):
        return _('Latest threads in %(obj_name)s') % {'obj_name': obj.name}

    def link(self, obj):
        if obj is None:
            return '/'
        else:
            return obj.get_absolute_url()

    def items(self, obj):
        return Post.objects.filter(category=obj, thread__isnull=True).order_by('-postdate')[:10]

    def item_title(self, item):
        return item.subject

    def item_description(self, item):
        return item.body_escaped(with_signature=False)

    def item_pubdate(self, item):
        return item.postdate


class LatestGlobalThreads(Feed):

    def get_object(self, request, group=None):
        return group

    def title(self, obj):
        return _('Latest threads at %(obj_name)s') % {'obj_name': obj.longname and obj.longname or obj.name}

    def description(self, obj):
        return _('Latest threads at %(obj_name)s') % {'obj_name': obj.longname and obj.longname or obj.name}

    def link(self, obj):
        if obj is None:
            return '/'
        else:
            return obj.get_baseurl()

    def items(self, obj):
        return Post.objects.filter(category__group=obj, thread__isnull=True).order_by('-postdate')[:10]

    def item_title(self, item):
        return item.subject

    def item_description(self, item):
        return item.body_escaped(with_signature=False)

    def item_pubdate(self, item):
        return item.postdate