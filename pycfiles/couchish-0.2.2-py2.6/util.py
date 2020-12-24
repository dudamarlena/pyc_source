# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/couchish/tests/util.py
# Compiled at: 2009-02-28 07:27:06
import uuid, couchdb

class TempDatabaseMixin(object):

    def setUp(self):
        self.db_name = 'couchish-' + str(uuid.uuid4())
        self.db = couchdb.Server().create(self.db_name)

    def tearDown(self):
        del couchdb.Server()[self.db_name]