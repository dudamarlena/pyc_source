# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/dblog.py
# Compiled at: 2014-07-11 17:28:21
"""
Stores action logs to the "log" table in backend.
Used for long-running operations (ex. btaimport).
Automatically action status (exception occurred, interrupted, success).
"""
import sys, datetime, pkg_resources, contextlib

class DBLogEntry(object):

    def __init__(self, backend):
        self.backed = backend
        self.log = backend.open_table('log')
        self.log.ensure_created()

    @classmethod
    @contextlib.contextmanager
    def dblog_context(cls, backend):
        dblog = cls(backend)
        dblog.create_entry()
        try:
            yield dblog
        except KeyboardInterrupt:
            dblog.update_entry('Interrupted by user (Ctrl-C)')
            raise
        except Exception as e:
            dblog.update_entry('ERROR: %s' % e)
            raise
        else:
            dblog.update_entry('Graceful exit')

    def create_entry(self):
        e = dict(date=datetime.datetime.now(), program=sys.argv[0], args=sys.argv, version=pkg_resources.get_distribution('bta').version, actions=[])
        self.entry_id = self.log.insert(e)

    def update_entry(self, action):
        act = dict(date=datetime.datetime.now())
        if type(action) is dict:
            act.update(action)
        else:
            act['action'] = action
        self.log.update({'_id': self.entry_id}, {'$push': {'actions': act}})