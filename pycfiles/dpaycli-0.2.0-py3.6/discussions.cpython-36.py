# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycli/discussions.py
# Compiled at: 2018-10-15 03:13:48
# Size of source mod 2**32: 27902 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from .instance import shared_dpay_instance
from .account import Account
from .comment import Comment
from .utils import resolve_authorperm
import logging
log = logging.getLogger(__name__)

class Query(dict):
    __doc__ = ' Query to be used for all discussion queries\n\n        :param int limit: limits the number of posts\n        :param str tag: tag query\n        :param int truncate_body:\n        :param array filter_tags:\n        :param array select_authors:\n        :param array select_tags:\n        :param str start_author:\n        :param str start_permlink:\n        :param str start_tag:\n        :param str parent_author:\n        :param str parent_permlink:\n        :param str start_parent_author:\n        :param str before_date:\n        :param str author: Author (see Discussions_by_author_before_date)\n\n        .. testcode::\n\n            from dpaycli.discussions import Query\n            query = Query(limit=10, tag="dsocial")\n\n    '

    def __init__(self, limit=0, tag='', truncate_body=0, filter_tags=[], select_authors=[], select_tags=[], start_author=None, start_permlink=None, start_tag=None, parent_author=None, parent_permlink=None, start_parent_author=None, before_date=None, author=None):
        self['limit'] = limit
        self['truncate_body'] = truncate_body
        self['tag'] = tag
        self['filter_tags'] = filter_tags
        self['select_authors'] = select_authors
        self['select_tags'] = select_tags
        self['start_author'] = start_author
        self['start_permlink'] = start_permlink
        self['start_tag'] = start_tag
        self['parent_author'] = parent_author
        self['parent_permlink'] = parent_permlink
        self['start_parent_author'] = start_parent_author
        self['before_date'] = before_date
        self['author'] = author


class Discussions(object):
    __doc__ = ' Get Discussions\n\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n    '

    def __init__(self, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.lazy = lazy

    def get_discussions(self, discussion_type, discussion_query, limit=1000):
        """ Get Discussions

            :param str discussion_type: Defines the used discussion query
            :param dpaycli.discussions.Query discussion_query:

            .. testcode::

                from dpaycli.discussions import Query, Discussions
                query = Query(limit=51, tag="dsocial")
                discussions = Discussions()
                count = 0
                for d in discussions.get_discussions("tags", query, limit=200):
                    print(("%d. " % (count + 1)) + str(d))
                    count += 1

        """
        if limit >= 100:
            if discussion_query['limit'] == 0:
                discussion_query['limit'] = 100
        else:
            if limit < 100:
                if discussion_query['limit'] == 0:
                    discussion_query['limit'] = limit
            else:
                query_count = 0
                found_more_than_start_entry = True
                if 'start_author' in discussion_query:
                    start_author = discussion_query['start_author']
                else:
                    start_author = None
                if 'start_permlink' in discussion_query:
                    start_permlink = discussion_query['start_permlink']
                else:
                    start_permlink = None
                if 'start_tag' in discussion_query:
                    start_tag = discussion_query['start_tag']
                else:
                    start_tag = None
                if 'start_parent_author' in discussion_query:
                    start_parent_author = discussion_query['start_parent_author']
                else:
                    start_parent_author = None
            discussion_query['before_date'] = discussion_query['before_date'] or '1970-01-01T00:00:00'
        while query_count < limit and found_more_than_start_entry:
            rpc_query_count = 0
            discussion_query['start_author'] = start_author
            discussion_query['start_permlink'] = start_permlink
            discussion_query['start_tag'] = start_tag
            discussion_query['start_parent_author'] = start_parent_author
            if discussion_type == 'trending':
                dd = Discussions_by_trending(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
            else:
                if discussion_type == 'author_before_date':
                    dd = Discussions_by_author_before_date(author=(discussion_query['author']), start_permlink=(discussion_query['start_permlink']),
                      before_date=(discussion_query['before_date']),
                      limit=(discussion_query['limit']),
                      dpay_instance=(self.dpay),
                      lazy=(self.lazy))
                else:
                    if discussion_type == 'payout':
                        dd = Comment_discussions_by_payout(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                    else:
                        if discussion_type == 'post_payout':
                            dd = Post_discussions_by_payout(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                        else:
                            if discussion_type == 'created':
                                dd = Discussions_by_created(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                            else:
                                if discussion_type == 'active':
                                    dd = Discussions_by_active(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                                else:
                                    if discussion_type == 'cashout':
                                        dd = Discussions_by_cashout(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                                    else:
                                        if discussion_type == 'votes':
                                            dd = Discussions_by_votes(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                                        else:
                                            if discussion_type == 'children':
                                                dd = Discussions_by_children(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                                            else:
                                                if discussion_type == 'hot':
                                                    dd = Discussions_by_hot(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                                                else:
                                                    if discussion_type == 'feed':
                                                        dd = Discussions_by_feed(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                                                    else:
                                                        if discussion_type == 'blog':
                                                            dd = Discussions_by_blog(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                                                        else:
                                                            if discussion_type == 'comments':
                                                                dd = Discussions_by_comments(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                                                            else:
                                                                if discussion_type == 'promoted':
                                                                    dd = Discussions_by_promoted(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                                                                else:
                                                                    if discussion_type == 'replies':
                                                                        dd = Replies_by_last_update(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
                                                                    else:
                                                                        if discussion_type == 'tags':
                                                                            dd = Trending_tags(discussion_query, dpay_instance=(self.dpay), lazy=(self.lazy))
            if not dd:
                return
            for d in dd:
                double_result = False
                if discussion_type == 'tags':
                    if query_count != 0:
                        if rpc_query_count == 0:
                            if d['name'] == start_tag:
                                double_result = True
                                if len(dd) == 1:
                                    found_more_than_start_entry = False
                        start_tag = d['name']
                    else:
                        if discussion_type == 'replies':
                            if query_count != 0:
                                if rpc_query_count == 0:
                                    if d['author'] == start_parent_author:
                                        if d['permlink'] == start_permlink:
                                            double_result = True
                                            if len(dd) == 1:
                                                found_more_than_start_entry = False
                            start_parent_author = d['author']
                            start_permlink = d['permlink']
                        else:
                            if query_count != 0:
                                if rpc_query_count == 0:
                                    if d['author'] == start_author:
                                        if d['permlink'] == start_permlink:
                                            double_result = True
                                            if len(dd) == 1:
                                                found_more_than_start_entry = False
                            start_author = d['author']
                            start_permlink = d['permlink']
                    rpc_query_count += 1
                    if not double_result:
                        query_count += 1
                        if query_count <= limit:
                            yield d


class Discussions_by_trending(list):
    __doc__ = ' Get Discussions by trending\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter for\n            searching posts\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Discussions_by_trending\n            q = Query(limit=10, tag="dpay")\n            for h in Discussions_by_trending(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_discussions_by_trending(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_trending(discussion_query)
        super(Discussions_by_trending, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Discussions_by_author_before_date(list):
    __doc__ = ' Get Discussions by author before date\n\n        .. note:: To retrieve discussions before date, the time of creation\n                  of the discussion @author/start_permlink must be older than\n                  the specified before_date parameter.\n\n        :param str author: Defines the author *(required)*\n        :param str start_permlink: Defines the permlink of a starting discussion\n        :param str before_date: Defines the before date for query\n        :param int limit: Defines the limit of discussions\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n            from dpaycli.discussions import Query, Discussions_by_author_before_date\n            for h in Discussions_by_author_before_date(limit=10, author="gtg"):\n                print(h)\n\n    '

    def __init__(self, author='', start_permlink='', before_date='1970-01-01T00:00:00', limit=100, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            discussion_query = {'author':author, 
             'start_permlink':start_permlink,  'before_date':before_date,  'limit':limit}
            posts = self.dpay.rpc.get_discussions_by_author_before_date(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_author_before_date(author, start_permlink, before_date, limit)
        super(Discussions_by_author_before_date, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Comment_discussions_by_payout(list):
    __doc__ = ' Get comment_discussions_by_payout\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter for\n            searching posts\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Comment_discussions_by_payout\n            q = Query(limit=10)\n            for h in Comment_discussions_by_payout(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_comment_discussions_by_payout(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_comment_discussions_by_payout(discussion_query)
        super(Comment_discussions_by_payout, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Post_discussions_by_payout(list):
    __doc__ = ' Get post_discussions_by_payout\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter for\n            searching posts\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Post_discussions_by_payout\n            q = Query(limit=10)\n            for h in Post_discussions_by_payout(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_post_discussions_by_payout(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_post_discussions_by_payout(discussion_query)
        super(Post_discussions_by_payout, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Discussions_by_created(list):
    __doc__ = ' Get discussions_by_created\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter for\n            searching posts\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Discussions_by_created\n            q = Query(limit=10)\n            for h in Discussions_by_created(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_discussions_by_created(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_created(discussion_query)
        super(Discussions_by_created, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Discussions_by_active(list):
    __doc__ = ' get_discussions_by_active\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter\n            searching posts\n        :param dpay dpay_instance: DPay() instance to use when accesing a RPC\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Discussions_by_active\n            q = Query(limit=10)\n            for h in Discussions_by_active(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_discussions_by_active(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_active(discussion_query)
        super(Discussions_by_active, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Discussions_by_cashout(list):
    __doc__ = ' Get discussions_by_cashout. This query seems to be broken at the moment.\n        The output is always empty.\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter\n            searching posts\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Discussions_by_cashout\n            q = Query(limit=10)\n            for h in Discussions_by_cashout(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_discussions_by_cashout(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_cashout(discussion_query)
        super(Discussions_by_cashout, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Discussions_by_votes(list):
    __doc__ = ' Get discussions_by_votes\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter\n            searching posts\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Discussions_by_votes\n            q = Query(limit=10)\n            for h in Discussions_by_votes(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_discussions_by_votes(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_votes(discussion_query)
        super(Discussions_by_votes, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Discussions_by_children(list):
    __doc__ = ' Get discussions by children\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter\n            searching posts\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Discussions_by_children\n            q = Query(limit=10)\n            for h in Discussions_by_children(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_discussions_by_children(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_children(discussion_query)
        super(Discussions_by_children, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Discussions_by_hot(list):
    __doc__ = ' Get discussions by hot\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter\n            searching posts\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Discussions_by_hot\n            q = Query(limit=10, tag="dpay")\n            for h in Discussions_by_hot(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_discussions_by_hot(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_hot(discussion_query)
        super(Discussions_by_hot, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Discussions_by_feed(list):
    __doc__ = ' Get discussions by feed\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter\n            searching posts, tag musst be set to a username\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Discussions_by_feed\n            q = Query(limit=10, tag="dpay")\n            for h in Discussions_by_feed(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_discussions_by_feed(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_feed(discussion_query)
        super(Discussions_by_feed, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Discussions_by_blog(list):
    __doc__ = ' Get discussions by blog\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter\n            searching posts, tag musst be set to a username\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Discussions_by_blog\n            q = Query(limit=10)\n            for h in Discussions_by_blog(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_discussions_by_blog(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_blog(discussion_query)
        super(Discussions_by_blog, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Discussions_by_comments(list):
    __doc__ = ' Get discussions by comments\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter\n            searching posts, start_author and start_permlink must be set.\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Discussions_by_comments\n            q = Query(limit=10, start_author="dsocial", start_permlink="firstpost")\n            for h in Discussions_by_comments(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_discussions_by_comments(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_comments(discussion_query)
        super(Discussions_by_comments, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Discussions_by_promoted(list):
    __doc__ = ' Get discussions by promoted\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter\n            searching posts\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Discussions_by_promoted\n            q = Query(limit=10, tag="dpay")\n            for h in Discussions_by_promoted(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_discussions_by_promoted(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_discussions_by_promoted(discussion_query)
        super(Discussions_by_promoted, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Replies_by_last_update(list):
    __doc__ = ' Returns a list of replies by last update\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter\n            searching posts start_parent_author and start_permlink must be set.\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Replies_by_last_update\n            q = Query(limit=10, start_parent_author="dsocial", start_permlink="firstpost")\n            for h in Replies_by_last_update(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            posts = self.dpay.rpc.get_replies_by_last_update(discussion_query, api='tags')['discussions']
        else:
            posts = self.dpay.rpc.get_replies_by_last_update(discussion_query['start_parent_author'], discussion_query['start_permlink'], discussion_query['limit'])
        super(Replies_by_last_update, self).__init__([Comment(x, lazy=lazy, dpay_instance=(self.dpay)) for x in posts])


class Trending_tags(list):
    __doc__ = ' Returns the list of trending tags.\n\n        :param dpaycli.discussions.Query discussion_query: Defines the parameter\n            searching posts, start_tag can be set.\n        :param dpaycli.dpay.DPay dpay_instance: DPay instance\n\n        .. testcode::\n\n            from dpaycli.discussions import Query, Trending_tags\n            q = Query(limit=10, start_tag="")\n            for h in Trending_tags(q):\n                print(h)\n\n    '

    def __init__(self, discussion_query, lazy=False, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.dpay.rpc.set_next_node_on_empty_reply(self.dpay.rpc.get_use_appbase())
        if self.dpay.rpc.get_use_appbase():
            tags = self.dpay.rpc.get_trending_tags(discussion_query, api='tags')['tags']
        else:
            tags = self.dpay.rpc.get_trending_tags((discussion_query['start_tag']), (discussion_query['limit']), api='tags')
        super(Trending_tags, self).__init__([x for x in tags])