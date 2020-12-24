# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/api.py
# Compiled at: 2020-04-13 07:58:16
# Size of source mod 2**32: 634 bytes
import json
from flask import Response, request

class APIHandler:
    __doc__ = ' class APIHandler to link routes to specific handler function\n\n    USAGE:\n            api = APIHandler(host=host, port=port, username=username, password=password, dbname=dbname)\n\n    '

    def __init__(self):
        """
                self.db = DBFetcher()
        try:
            self.db.connect(host=host, port=port, username=username, password=password, dbname=dbname, minConn=1, maxConn=5)
        except Exception as e:
            print(e)

        """
        pass

    def index(self):
        """

        :return:
        """
        return 'hello world'