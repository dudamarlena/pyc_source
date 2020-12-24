# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/content/rpc.py
# Compiled at: 2011-02-06 06:56:22
from pypoly.content import BasicContent
import xmlrpclib

class XMLResponse(BasicContent):
    _params = None

    def __init__(self, params):
        BasicContent.__init__(self)
        self._params = params
        self._mime_type = 'text/xml'

    def __call__(self):
        content = xmlrpclib.dumps(params=(self._params,), methodresponse=True)
        _size = len(content)
        return [
         content]