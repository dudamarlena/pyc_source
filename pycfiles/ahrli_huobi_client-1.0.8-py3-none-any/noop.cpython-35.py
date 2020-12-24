# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/noop.py
# Compiled at: 2016-10-17 07:52:17
# Size of source mod 2**32: 226 bytes
from ahqapiclient.resources import Resource

class Noop(Resource):

    def __init__(self, http_client):
        super(Noop, self).__init__('/noop', http_client)

    def noop(self):
        return self.get(path=self.rurl())