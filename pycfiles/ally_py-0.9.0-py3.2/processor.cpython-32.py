# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_http_asyncore_server/processor.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Nov 24, 2011

@package: ally http
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the setup for the asyncore processor.
"""
from ally.container import ioc
from ally.design.processor.handler import Handler
from ally.http.impl.processor.asyncore_content import AsyncoreContentHandler
from os import path

@ioc.config
def dump_requests_size():
    """The minimum size of the request length to be dumped on the file system in bytes"""
    return 1048576


@ioc.config
def dump_requests_path():
    """The path where the requests are dumped when they are to big to keep in memory"""
    return path.join('workspace', 'asyncore')


@ioc.entity
def asyncoreContent() -> Handler:
    b = AsyncoreContentHandler()
    b.dumpRequestsSize = dump_requests_size()
    b.dumpRequestsPath = dump_requests_path()
    return b