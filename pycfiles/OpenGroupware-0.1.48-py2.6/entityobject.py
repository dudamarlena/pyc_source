# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/attachfs/entityobject.py
# Compiled at: 2012-10-12 07:02:39
import uuid
from coils.core import *
from coils.net import PathObject

class EntityObject(PathObject):

    def __init__(self, parent, name, **params):
        self.name = name
        PathObject.__init__(self, parent, **params)

    def do_PUT(self, name):
        payload = self.request.get_request_payload()
        mimetype = self.request.headers.get('Content-Type', 'application/octet-stream')
        scratch_file = BLOBManager.ScratchFile()
        scratch_file.write(payload)
        scratch_file.seek(0)
        attachment = None
        mode = None
        if 'mode' in self.parameters:
            mode = self.parameters['mode'][0].lower()
        else:
            mode = 'default'
        if mode == 'file':
            document = None
            if isinstance(self.entity, Folder):
                if name:
                    document = self.context.run_command('folder::ls', id=self.entity.object_id, name=name)
                    if document:
                        document = document[0]
                else:
                    name = ('{0}.bin').format(uuid.uuid4().hex)
            elif isinstance(self.entity, Document):
                document = self.entity
            else:
                raise CoilsException(('Mode "file" not support by AttachFS for entities of type "{0}"').format(self.entity))
            if not document:
                document = self.context.run_command('document::new', name=name, values={}, folder=self.entity, handle=scratch_file)
            else:
                self.context.run_command('document::set', object=document, name=name, values={}, handle=scratch_file)
            self.context.property_manager.set_property(document, 'http://www.opengroupware.us/mswebdav', 'isTransient', 'NO')
            self.context.property_manager.set_property(document, 'http://www.opengroupware.us/mswebdav', 'contentType', mimetype)
            self.context.commit()
            self.request.simple_response(201, mimetype=mimetype, headers={'Content-Length': str(document.file_size), 'X-OpenGroupware-Document-Id': str(document.object_id), 
               'X-OpenGroupware-Folder-Id': str(document.folder_id), 
               'Etag': ('{0}:{1}').format(document.object_id, document.version), 
               'Content-Type': document.mimetype})
        elif mode == 'default':
            attachment = self.context.run_command('attachment::new', handle=scratch_file, name=name, entity=self.entity, mimetype=mimetype)
            self.context.commit()
            if attachment is not None:
                self.request.simple_response(201, mimetype=mimetype, headers={'Content-Length': str(attachment.size), 'Etag': attachment.uuid, 
                   'Content-Type': attachment.mimetype})
            else:
                raise CoilsExcpetion('Ooops!')
        else:
            raise CoilsException(('Unrecognized mode "{0}" specified for AttachFS operation.').format(mode))
        return