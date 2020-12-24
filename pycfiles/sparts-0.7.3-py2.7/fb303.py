# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/tasks/fb303.py
# Compiled at: 2015-02-07 04:24:13
"""Module related to implementing fb303 thrift handlers"""
from __future__ import absolute_import
from sparts.tasks.thrift import ThriftHandlerTask
from sparts.gen.fb303 import FacebookService
from sparts.gen.fb303.ttypes import fb_status
import threading, time
from six import StringIO, iteritems

class FB303HandlerTask(ThriftHandlerTask):
    MODULE = FacebookService

    def initTask(self):
        super(FB303HandlerTask, self).initTask()
        self._profile_lock = threading.Lock()

    def getName(self):
        return self.service.name

    def getVersion(self):
        return str(self.service.VERSION)

    def getStatus(self):
        if self.service._stop:
            return fb_status.STOPPING
        for task in self.service.tasks:
            if not task.LOOPLESS:
                for thread in task.threads:
                    if not thread.isAlive():
                        return fb_status.WARNING

        if self.service.getWarnings():
            return fb_status.WARNING
        return fb_status.ALIVE

    def getStatusDetails(self):
        messages = []
        if self.service._stop:
            messages.append('%s is shutting down' % self.getName())
        for task in self.service.tasks:
            if not task.LOOPLESS:
                for thread in task.threads:
                    if not thread.isAlive():
                        messages.append('%s has dead threads!' % task.name)

        messages.extend(self.service.getWarnings().values())
        return ('\n').join(messages)

    def getCounters(self):
        result = {}
        for k, v in iteritems(self.service.getCounters()):
            v = v()
            if v is None:
                continue
            result[k] = int(v)

        return result

    def getCounter(self, name):
        result = self.service.getCounter(name)()
        if result is None:
            raise ValueError('%s is None' % name)
        return int(result)

    def setOption(self, name, value):
        if value == '__None__':
            value = None
        else:
            cur_value = getattr(self.service.options, name)
            if cur_value is not None:
                try:
                    value = cur_value.__class__(value)
                except Exception as e:
                    self.logger.debug('Unable to cast %s to %s (%s)', value, cur_value.__class__, e)

        self.service.setOption(name, value)
        return

    def getOption(self, name):
        value = self.service.getOption(name)
        if value is None:
            value = '__None__'
        return str(value)

    def getOptions(self):
        result = {}
        for k in self.service.getOptions():
            result[k] = self.getOption(k)

        return result

    def aliveSince(self):
        return self.service.start_time

    def reinitialize(self):
        self.service.restart()

    def shutdown(self):
        self.service.shutdown()

    def getCpuProfile(self, profileDurationInSec):
        try:
            import yappi
        except ImportError:
            self.logger.warning('getCpuProfile called without yappi installed')
            return ''

        with self._profile_lock:
            yappi.start()
            time.sleep(profileDurationInSec)
            yappi.stop()
            stats = yappi.get_func_stats()
        sio = StringIO()
        stats.print_all(out=sio)
        return sio.getvalue()