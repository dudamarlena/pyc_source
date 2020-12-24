# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fast_queue/__init__.py
# Compiled at: 2017-11-05 14:08:42
import sys, os, uuid, datetime, six, json
from kombu import Connection, BrokerConnection
from kombu.pools import connections
BROKER_URL = 'amqp://'

class ModuleWrapper(object):

    def __init__(self, name):
        self.__name = name

    def __getattr__(self, name):
        if name.startswith('kombu.') or name in ('__conn', '__name'):
            return super(ModuleWrapper, self).__getattribute__(name)
        return ModuleWrapper('%s.%s' % (self.__name, name))

    def __conn(self):
        return Connection(BROKER_URL)

    def __call__(self, *args, **kw):
        url = kw['__broker_url'] if '__broker_url' in kw else BROKER_URL
        queue = kw['__queue'] if '__queue' in kw else self.__name
        with connections[Connection(url)].acquire(block=True) as (conn):
            simple_queue = conn.SimpleQueue(queue)
            message = {'id': uuid.uuid4().hex, 'task': self.__name, 
               'args': args, 
               'kwargs': kw, 
               'eta': datetime.datetime.now().isoformat()}
            simple_queue.put(message)
            simple_queue.close()


class MagicHook(object):

    def find_module(self, fullname, path=None):
        if fullname.startswith('fast_queue.'):
            return self
        else:
            return

    def load_module(self, name):
        name = name[11:]
        sys.modules[name] = ModuleWrapper(name)
        return sys.modules[name]


sys.meta_path = [
 MagicHook()]