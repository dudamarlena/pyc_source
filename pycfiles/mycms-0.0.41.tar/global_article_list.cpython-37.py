# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/view_handlers/global_article_list.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 4205 bytes
from mycms.models import CMSEntries
from mycms.models import CMSPageTypes
from mycms.view_handlers.mycms_view import ViewObject
from mycms.view_handlers.mycms_view import ArticleList
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.utils import OperationalError
import logging
logger = logging.getLogger('mycms.page_handlers')
from .page_types import singlepageview_pagetype_obj
from .page_types import multipageview_pagetype_obj
from .page_types import allarticles_pagetype_obj

class AllArticlesPage(object):

    def __init__(self, page_object, request=None):
        self.page_object = page_object
        self.request = request
        self._article_list = None

    def articles(self):
        """Here we load all pages that says we are their parent."""
        from django.db.models import Q
        if self.request:
            try:
                limit = int(self.request.GET.get('limit', 10))
            except Exception as e:
                try:
                    limit = 10
                finally:
                    e = None
                    del e

            try:
                offset = int(self.request.GET.get('offset', 0))
            except Exception as e:
                try:
                    offset = 0
                finally:
                    e = None
                    del e

        else:
            limit = 10
            offset = 0
        if self._article_list is None or limit != self._article_list.limit or offset != self._article_list.offset:
            self._article_list = ArticleList()
            self._article_list.limit = limit
            self._article_list.offset = offset
            obj_list = CMSEntries.objects.filter((Q(page_type=singlepageview_pagetype_obj) | Q(page_type=multipageview_pagetype_obj)) & Q(lists_include=True))[offset:offset + limit + 1]
            num_results = obj_list.count()
            if num_results > limit:
                self._article_list.has_older = True
            else:
                self._article_list.has_older = False
            if offset == 0:
                self._article_list.has_newer = False
            else:
                self._article_list.has_newer = True
            for obj in obj_list:
                self._article_list.append(ViewObject(page_object=obj))

        return self._article_list

    def get_categories(self):
        """Returns a list of all child categories of type: CATEGORY"""
        obj_list = CMSEntries.objects.filter(path__path__parent__id=(self.page_object.id), page_type=(page_obj.page_type))
        return obj_list

    def page_types(self):
        """
        Refactor me into a parent class.
        returns a list fo page_types
        """
        pagetype_objs = CMSPageTypes.objects.all()
        return pagetype_objs

    def on_create(self):
        pass