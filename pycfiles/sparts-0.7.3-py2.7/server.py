# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/tasks/thrift/server.py
# Compiled at: 2015-08-18 20:49:57
"""Base Task for implementing thrift servers"""
from __future__ import absolute_import
from sparts.vtask import VTask
from sparts.tasks.thrift.handler import ThriftHandlerTask
from thrift.TMultiplexedProcessor import TMultiplexedProcessor

class ThriftServerTask(VTask):
    """Base class for various thrift server implementations."""
    MODULE = None
    MULTIPLEX = False

    def initTask(self):
        super(ThriftServerTask, self).initTask()
        processors = self._findProcessors()
        if not len(processors) > 0:
            raise AssertionError('No processors found for %s' % self.MODULE)
            assert self.MULTIPLEX or len(processors) == 1, 'Too many processors found for %s.  Did you mean to set MULTIPLEX = True on your server?' % self.MODULE
            self.processor = processors[0].processor
        else:
            self.processor = TMultiplexedProcessor()
            for processor_task in processors:
                self.logger.info("Registering %s as Multiplexed Service, '%s'", processor_task.processor, processor_task.service_name)
                self.processor.registerProcessor(processor_task.service_name, processor_task.processor)

    def _checkTaskModule(self, task):
        """Returns True if `task` implements the appropriate MODULE Iface"""
        if not isinstance(task, ThriftHandlerTask):
            return False
        else:
            if self.MODULE is None:
                return True
            if self.MODULE is task.MODULE:
                return True
            iface = self.MODULE.Iface
            for method_name in dir(iface):
                method = getattr(iface, method_name)
                if not callable(method):
                    continue
                handler_method = getattr(task, method_name, None)
                if handler_method is None:
                    self.logger.debug('Skipping Task %s (missing method %s)', task.name, method_name)
                    return False
                if not callable(handler_method):
                    self.logger.debug('Skipping Task %s (%s not callable)', task.name, method_name)
                    return False

            return True

    def _findProcessors(self):
        """Returns all processors that match this tasks' MODULE"""
        processors = []
        for task in self.service.tasks:
            if self._checkTaskModule(task):
                processors.append(task)

        return processors