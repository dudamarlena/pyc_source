# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/view_handlers/category_page.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 3296 bytes
from mycms.models import CMSEntries
from mycms.models import CMSPageTypes
from mycms.view_handlers.mycms_view import ViewObject
from mycms.view_handlers.mycms_view import ArticleList
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import logging
logger = logging.getLogger('mycms.page_handlers')
from .page_types import singlepageview_pagetype_obj
from .page_types import multipageview_pagetype_obj
from .page_types import allarticles_pagetype_obj

class CategoryPage(object):

    def __init__(self, page_object, request=None):
        self.page_object = page_object
        self.request = request

    @property
    def articles(self):
        """Here we load all pages that says we are their parent."""
        from django.db.models import Q
        article_list = ArticleList()
        if self.request:
            limit = int(self.request.GET.get('limit', 10))
            offset = int(self.request.GET.get('offset', 0))
        obj_list = CMSEntries.objects.filter((Q(page_type=singlepageview_pagetype_obj) | Q(page_type=multipageview_pagetype_obj)) & Q(path__parent__id=(self.page_object.path.id)) & Q(published=True))[offset:offset + limit]
        for obj in obj_list:
            article_list.append(ViewObject(page_object=obj))

        return article_list

    def get_categories(self):
        """Returns a list of all child categories of type: CATEGORY"""
        print('doping query')
        try:
            obj_list = CMSEntries.objects.filter(path__parent__id=(self.page_object.id), page_type=(self.page_object.page_type))
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

        print('done with the query')
        return obj_list

    @property
    def categories(self):
        return self.get_categories()

    def page_types(self):
        """
        Refactor me into a parent class.
        returns a list fo page_types
        """
        pagetype_objs = CMSPageTypes.objects.all()
        return pagetype_objs

    def on_create(self):
        pass

    def all_sub_articles(self):
        """
        Returns all articles under this category.
        """
        from django.db.models import Q
        obj_list = CMSEntries.objects.filter((Q(page_type=singlepageview_pagetype_obj) | Q(page_type=multipageview_pagetype_obj)) & Q(path__path__startswith=(self.page_object.path.path)))
        return obj_list