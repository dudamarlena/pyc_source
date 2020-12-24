# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arrow/view.py
# Compiled at: 2018-09-05 11:57:03
# Size of source mod 2**32: 933 bytes
from webob import Response

class View(object):

    def get(self, req, res):
        res.status(501)

    def post(self, req, res):
        res.status(501)

    def put(self, req, res):
        res.status(501)

    def patch(self, req, res):
        res.status(501)

    def delete(self, req, res):
        res.status(501)

    def options(self, req, res):
        res.status(501)

    def handle(self, req, res):
        if self.middleware:
            for mw in self.middleware:
                mw(req, res)

        if req.method() == 'GET':
            self.get(req, res)
        else:
            if req.method() == 'POST':
                self.post(req, res)
            else:
                if req.method() == 'PUT':
                    self.put(req, res)
                else:
                    if req.method() == 'PATCH':
                        self.patch(req, res)
                    else:
                        if req.method() == 'DELETE':
                            self.delete(req, res)
                        elif req.method() == 'OPTIONS':
                            self.options(req, res)