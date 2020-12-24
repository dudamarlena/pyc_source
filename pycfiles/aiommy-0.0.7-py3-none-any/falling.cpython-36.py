# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/aiommy/paginations/falling.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 1542 bytes
from aiommy.paginations.base import BaseCursorPagination

class FallingPagination(BaseCursorPagination):

    def first(self, queryset, through, last_id):
        """
        :param queryset: peewee queryset
        :param through: params for save interface for all paginate methods
        :param last_id: id of last element for exclude duplicating
        :return: first page of queryset
        """
        return queryset.order_by(-self.cursor, self.model.id).paginate(1, self.items_per_page)

    def next(self, queryset, through, last_id=None):
        """
        :param queryset: peewee queryset
        :param through: params for save interface for all paginate methods
        :param last_id: id of last element for exclude duplicating
        :return: next page of queryset
        """
        where_exp = (self.cursor < through) | (self.cursor == through) & (self.model.id > last_id)
        return queryset.where(where_exp).order_by(-self.cursor, self.model.id).paginate(1, self.items_per_page)

    def previous(self, queryset, through, last_id=None):
        """
        :param queryset: peewee queryset
        :param through: params for save interface for all paginate methods
        :param last_id: id of last element for exclude duplicating
        :return: previous page of queryset
        """
        where_exp = (self.cursor > through) | (self.cursor == through) & (self.model.id < last_id)
        return queryset.where(where_exp).order_by(-self.cursor, self.model.id)