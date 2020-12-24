# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/couchish/tests/util.py
# Compiled at: 2009-02-28 07:27:06
import uuid, couchdb

class TempDatabaseMixin(object):

    def setUp(self):
        self.db_name = 'couchish-' + str(uuid.uuid4())
        self.db = couchdb.Server().create(self.db_name)

    def tearDown(self):
        del couchdb.Server()[self.db_name]