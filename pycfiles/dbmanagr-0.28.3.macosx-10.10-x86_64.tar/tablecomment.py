# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/model/tablecomment.py
# Compiled at: 2015-10-11 07:17:06
import logging, json
COMMENT_ID = 'id'
COMMENT_TITLE = 'title'
COMMENT_SUBTITLE = 'subtitle'
COMMENT_ORDER_BY = 'order'
COMMENT_SEARCH = 'search'
COMMENT_DISPLAY = 'display'
logger = logging.getLogger(__name__)

class TableComment(object):
    """The comment on the given table that allows to display much more
accurate information"""

    def __init__(self, json_string):
        self.id = None
        self.title = None
        self.subtitle = None
        self.search = None
        self.display = None
        self.order = None
        self.parse(json_string)
        return

    def parse(self, json_string):
        d = {COMMENT_ORDER_BY: [], COMMENT_SEARCH: [], COMMENT_DISPLAY: []}
        if json_string:
            try:
                d.update(json.loads(json_string))
            except BaseException as e:
                logger.warn('Error parsing JSON comment: %s', e)

        if COMMENT_ID in d:
            self.id = d[COMMENT_ID]
        if COMMENT_TITLE in d and self.id:
            d[COMMENT_TITLE] = '{0}.%s' % self.id
        if COMMENT_TITLE in d:
            self.title = d[COMMENT_TITLE]
        if COMMENT_SUBTITLE in d:
            self.subtitle = d[COMMENT_SUBTITLE]
        self.search = d[COMMENT_SEARCH]
        self.display = d[COMMENT_DISPLAY]
        self.order = d[COMMENT_ORDER_BY]

    def __repr__(self):
        return self.__dict__.__repr__()