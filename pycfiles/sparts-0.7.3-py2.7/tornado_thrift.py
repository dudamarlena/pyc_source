# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/tasks/tornado_thrift.py
# Compiled at: 2014-04-19 02:51:36
"""Module that provides helpers for supporting thrift over HTTP in tornado."""
from __future__ import absolute_import
import tornado.web
from thrift.transport.TTransport import TMemoryBuffer
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

class TornadoThriftHandler(tornado.web.RequestHandler):
    """A WebRequest handler that integrates HTTP with a thrift `Processor`.
    
    This handler MUST be initialized with a `processor` kwarg in an
    application config that includes it.
    """

    def initialize(self, processor):
        if hasattr(processor, 'processor'):
            processor = processor.processor
        self.processor = processor

    def post(self):
        """Thrift HTTP POST request.
        
        Translates the POST body to the thrift request, and returns the
        serialized thrift message in the response body.  Sets the approprate
        HTTP Content-Type header as well.
        """
        iprot = TBinaryProtocol(TMemoryBuffer(self.request.body))
        oprot = TBinaryProtocol(TMemoryBuffer())
        self.processor.process(iprot, oprot)
        self.set_header('Content-Type', 'application/x-thrift')
        self.write(oprot.trans.getvalue())