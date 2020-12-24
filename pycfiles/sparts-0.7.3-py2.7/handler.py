# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/tasks/thrift/handler.py
# Compiled at: 2015-08-18 20:00:57
"""thrift-related helper tasks"""
from __future__ import absolute_import
from sparts.vtask import VTask

class ThriftHandlerTask(VTask):
    """A loopless task that handles thrift requests.

    You will need to subclass this task, set MODULE, and implement the
    necessary methods in order for requests to be mapped here."""
    LOOPLESS = True
    MODULE = None
    SERVICE_NAME = None
    _processor = None

    def initTask(self):
        super(ThriftHandlerTask, self).initTask()
        assert self.MODULE is not None
        self._verifyInterface()
        return

    def _verifyInterface(self):
        iface = self.MODULE.Iface
        missing_methods = []
        for k in dir(iface):
            v = getattr(iface, k, None)
            if not callable(v) or k.startswith('_'):
                continue
            v2 = getattr(self, k, None)
            if v2 is None or not callable(v):
                missing_methods.append(k)

        if missing_methods:
            raise TypeError('%s is missing the following methods: %s' % (
             self.__class__.__name__, missing_methods))
        return

    def _makeProcessor(self):
        return self.MODULE.Processor(self)

    @property
    def processor(self):
        if self._processor is None:
            self._processor = self._makeProcessor()
        return self._processor

    @property
    def service_name(self):
        if self.SERVICE_NAME is not None:
            return self.SERVICE_NAME
        else:
            return self.name