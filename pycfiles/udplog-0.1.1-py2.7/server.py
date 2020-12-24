# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted/plugins/server.py
# Compiled at: 2013-09-08 09:30:41
"""
Twisted Plugins for udplog services.
"""
from __future__ import division, absolute_import
from twisted.application.service import ServiceMaker
UDPLogServer = ServiceMaker('UDPLog Server', 'udplog.tap', 'A service that accepts structured logs via UDP and dispatches them to Scribe or RabbitMQ.', 'udplog')