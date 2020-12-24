# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/foorti/foorti_list.py
# Compiled at: 2017-02-13 23:00:12
from .foorti_systems import *

class List(redis_object):

    def right_append(self, item):
        self.conn.rpush(self.name, item)

    def left_append(self, item):
        self.conn.lpush(self.name, item)

    def left_remove(self):
        self.conn.lpop(self.name)

    def right_remove(self):
        self.conn.rpop(self.name)

    def list_len(self):
        self.conn.llen(self.name)

    def trim_list(self, start, stop):
        self.conn.ltrim(self.name, start, stop)