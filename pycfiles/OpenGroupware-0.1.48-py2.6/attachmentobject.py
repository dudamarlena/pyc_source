# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/attachfs/attachmentobject.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.net import PathObject
from coils.net.ossf import MarshallOSSFChain

class AttachmentObject(PathObject):
    _MIME_MAP_ = None

    def __init__(self, parent, name, **params):
        self.name = name
        PathObject.__init__(self, parent, **params)

    def do_HEAD(self):
        mimetype = self.entity.get_mimetype(type_map=self._mime_type_map)
        self.request.simple_response(200, data=None, mimetype=mimetype, headers={'etag': self.entity.uuid, 'Content-Length': str(self.entity.size)})
        return

    def do_GET(self):
        handle = self.context.run_command('attachment::get-handle', uuid=self.entity.uuid)
        mimetype = self.entity.mimetype
        self.log.debug(('Attachment MIME-Type is "{0}"').format(mimetype))
        (handle, mimetype) = MarshallOSSFChain(handle, mimetype, self.parameters)
        self.log.debug(('MIME-Type after OSSF processing is {0}').format(mimetype))
        self.context.commit()
        self.request.stream_response(200, stream=handle, mimetype=mimetype, headers={'etag': self.entity.uuid})
        BLOBManager.Close(handle)