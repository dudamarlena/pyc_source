# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/serf_master/__init__.py
# Compiled at: 2014-10-13 03:35:48
import os, logging

class SerfHandler(object):

    def __init__(self):
        self.name = os.environ['SERF_SELF_NAME']
        self.role = os.environ.get('SERF_TAG_ROLE') or os.environ.get('SERF_SELF_ROLE')
        self.logger = logging.getLogger(type(self).__name__)
        if os.environ['SERF_EVENT'] == 'user':
            self.event = os.environ['SERF_USER_EVENT']
        elif os.environ['SERF_EVENT'] == 'query':
            self.event = os.environ['SERF_QUERY_NAME']
        else:
            self.event = os.environ['SERF_EVENT'].replace('-', '_')

    def log(self, message):
        self.logger.info(message)


class SerfHandlerProxy(SerfHandler):

    def __init__(self):
        super(SerfHandlerProxy, self).__init__()
        self.handlers = {}

    def register(self, role, handler):
        self.handlers[role] = handler

    def get_klass(self):
        klass = False
        if self.role in self.handlers:
            klass = self.handlers[self.role]
        elif 'default' in self.handlers:
            klass = self.handlers['default']
        return klass

    def run(self):
        klass = self.get_klass()
        if not klass:
            self.log('no handler for role')
        else:
            try:
                getattr(klass, self.event)()
            except AttributeError:
                self.log('event not implemented by class')