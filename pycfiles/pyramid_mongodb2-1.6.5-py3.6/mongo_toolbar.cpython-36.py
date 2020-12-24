# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyramid_mongodb2\mongo_toolbar.py
# Compiled at: 2018-07-29 21:53:31
# Size of source mod 2**32: 2195 bytes
from datetime import datetime
from pymongo.cursor import Cursor
from pyramid_debugtoolbar.panels import DebugPanel

class DebugMongo:
    __doc__ = '\n    A simple wrapper for a mongodb database. Logs all calls made\n    '

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
    __doc__ = '\n    MongoDB Debugtoolbar Panel\n    '
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