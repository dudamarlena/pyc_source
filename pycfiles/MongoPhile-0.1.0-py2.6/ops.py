# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/mongophile/ops.py
# Compiled at: 2011-02-18 14:31:06
from __future__ import division
try:
    import json
except:
    import simplejson as json

class MongoOp(object):

    def __repr__(self):
        return "{ [MongoOp '%s'] %sms }" % (self.opType, self.millis)


class MongoInsert(MongoOp):
    opType = 'insert'


class MongoQuery(MongoOp):
    opType = 'query'

    def __init__(self, log, ts, millis, db, coll, ntoreturn, scanAndOrder, reslen, nscanned, query, nreturned):
        self.log = log
        self.ts = ts
        self.millis = millis
        self.db = db
        self.coll = coll
        self.ntoreturn = ntoreturn
        self.scanAndOrder = scanAndOrder is None
        self.reslen = reslen
        self.nscanned = int(nscanned)
        self.query = query
        self.nreturned = int(nreturned)
        if self.nscanned == 0:
            self.scanRatio = 0.0
        else:
            self.scanRatio = '%.2f' % (self.nreturned / self.nscanned * 100)
        return

    def __str__(self):
        return "* Query against %s.%s ; returned %s documents (after scanning %s, for a Scan:Return ratio of %s%%) in %s bytes, taking %sms using query '%s'" % (self.db, self.coll, self.nreturned, self.nscanned, self.scanRatio, self.reslen, self.millis, self.query)


class MongoCommand(MongoOp):
    opType = 'command'

    def __init__(self, log, ts, millis, db, ntoreturn, command, reslen):
        self.log = log
        self.db = db
        self.ts = ts
        self.millis = millis
        self.ntoreturn = ntoreturn
        self.command = command
        self.reslen = reslen

    def __str__(self):
        return "* Command in database %s ; returned %s bytes, taking %sms with command query '%s'" % (self.db, self.reslen, self.millis, self.command)


class MongoUpdate(MongoOp):
    opType = 'update'

    def __init__(self, log, ts, millis, db, coll, query, nscanned, updateType):
        self.log = log
        self.db = db
        self.coll = coll
        self.ts = ts
        self.millis = millis
        self.query = query
        self.nscanned = nscanned
        self.updateType = updateType
        self.opType = self.opType + ' {%s}' % updateType

    def __str__(self):
        return "* Update of subtype '%s' against %s.%s; scanned %s documents, taking %sms using query '%s'" % (self.updateType, self.db, self.coll, self.nscanned, self.millis, self.query)