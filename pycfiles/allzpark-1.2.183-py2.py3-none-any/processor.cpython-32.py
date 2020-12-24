# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_http_asyncore_server/processor.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 24, 2011\n\n@package: ally http\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the setup for the asyncore processor.\n'
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