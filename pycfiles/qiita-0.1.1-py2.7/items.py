# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/qiita/items.py
# Compiled at: 2012-10-18 12:06:31
"""
    qiita.items
    ~~~~~~~~~~~

    Wrapper for Qiita items.

    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from .client import Client

class Items(Client):

    def post_item(self, params):
        """Post new item.

        :param params:
        """
        return self.post('/items', params)

    def update_item(self, uuid, params):
        """Update item.

        :param uuid:
        :param params:
        """
        return self.put(('/items/{0}').format(uuid), params)

    def delete_item(self, uuid):
        """Delete item.

        :param uuid:
        """
        return self.delete(('/items/{0}').format(uuid))

    def item(self, uuid):
        """Get newest post.

        If authorized, get user's post otherwise public newest post.

        :param uuid:
        """
        return self.get(('/items/{0}').format(uuid))

    def search_items(self, query, params=None):
        """Search items.

        Following query parameters are available.
          - q
          - stocked

        :param query:
        :param params:
        """
        if params is None:
            params = {'q': query}
        else:
            params['q'] = query
        return self.get('/search', params)

    def stock_item(self, uuid):
        """Stock item.

        :param uuid:
        """
        return self.put(('/items/{0}/stock').format(uuid))

    def unstock_item(self, uuid):
        """Unstock item.

        :param uuid:
        """
        return self.delete(('/items/{0}/stock').format(uuid))