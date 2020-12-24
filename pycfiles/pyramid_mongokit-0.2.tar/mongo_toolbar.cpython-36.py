# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyramid_mongodb2\mongo_toolbar.py
# Compiled at: 2018-07-29 21:53:31
# Size of source mod 2**32: 2195 bytes
from datetime import datetime
from pymongo.cursor import Cursor
from pyramid_debugtoolbar.panels import DebugPanel

class DebugMongo:
    """DebugMongo"""

    def __init__(self, conn, request):
        self.conn = conn
        self.request = request

    def _get_conn(self, item):
        coll = self.conn[item]

        def coll_attr(attr):
            target_attr = getattr(coll, attr)
            if hasattr(target_attr, '__call__'):

                def wrapper(*args, **kwargs):
                    start = datetime.now()
                    response = target_attr(*args, **kwargs)
                    duration = datetime.now() - start
                    doc = {'duration':duration, 
                     'db':coll.database, 
                     'collection':coll, 
                     'op':target_attr.__name__, 
                     'args':args, 
                     'kwargs':kwargs}
                    if isinstance(response, Cursor):
                        doc['cursor'] = response
                    self.request.query_log.append(doc)
                    return response

                return wrapper
            else:
                return target_attr

        class DebugCollection:

            def __init__(self, coll):
                self.coll = coll

            def __getattr__(self, item):
                return coll_attr(item)

        return DebugCollection(coll)

    def __getattr__(self, item):
        return self._get_conn(item)

    def __getitem__(self, item):
        return self._get_conn(item)


class MongoToolbar(DebugPanel):
    """MongoToolbar"""
    name = 'mongodb_panel'
    is_active = True
    has_content = True
    title = 'MongoDB'
    nav_title = 'MongoDB'
    template = 'pyramid_mongodb2:templates/mongo.mako'

    def __init__(self, request):
        super().__init__(request)
        self.data = {'request_path': request}
        self.request = request

    def process_response(self, response):
        self.data['request'] = self.request