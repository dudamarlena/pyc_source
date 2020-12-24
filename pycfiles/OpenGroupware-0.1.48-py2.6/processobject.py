# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/attachfs/processobject.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.net import PathObject
from coils.net.ossf import MarshallOSSFChain

class ProcessObject(PathObject):

    def __init__(self, parent, name, **params):
        self.name = name
        PathObject.__init__(self, parent, **params)

    def do_HEAD(self):
        self.request.simple_response(200, data=None, mimetype=self.entity.mimetype, headers={'etag': self.entity.uuid, 'Content-Length': str(self.entity.size)})
        return

    def do_GET(self):
        log_text = self.context.run_command('process::get-log', pid=self.entity.object_id)
        self.request.simple_response(200, data=log_text, mimetype='text/plain', headers={'etag': self.entity.uuid})
        BLOBManager.Close(handle)