# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/qiita/tags.py
# Compiled at: 2012-10-16 12:22:13
"""
    qiita.tags
    ~~~~~~~~~~

    Wrapper for Qiita Tags.

    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from .client import Client

class Tags(Client):

    def tag_items(self, url_name, params=None):
        """Get specific tag post.

        :param url_name:
        :param params:
        """
        params = {} if params is None else params
        return self.get(('/tags/{0}/items').format(url_name), params)

    def tags(self, params=None):
        """Get tag list.

        :param params:
        """
        params = {} if params is None else params
        return self.get('/tags', params)