# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arrow/middleware/crossorigin.py
# Compiled at: 2018-09-05 10:22:56
# Size of source mod 2**32: 986 bytes


class Crossorigin(object):

    def __init__(self, origin='*', methods=None, max_age=21600, headers=None):
        self.origin = origin
        self.methods = methods
        self.max_age = max_age
        self.headers = headers

    def getmethods(self):
        if self.methods is not None:
            return ', '.join(sorted(x.upper() for x in self.methods))
        else:
            return ''

    def getheaders(self):
        if self.headers is not None:
            return ', '.join(sorted(x.upper() for x in self.headers))
        else:
            return ''

    def __call__(self, req, res):
        if req.method() == 'OPTIONS':
            res.header('Access-Control-Allow-Origin', self.origin)
            res.header('Access-Control-Allow-Methods', self.getmethods())
            if self.max_age:
                res.header('Access-Control-Max-Age', str(self.max_age))
            if self.headers:
                res.header('Access-Control-Allow-Headers', self.headers)