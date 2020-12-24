# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/attachfs/viewobject.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.net import PathObject
from documentobject import DocumentObject
from attachmentobject import AttachmentObject
from messageobject import MessageObject
from processobject import ProcessObject

class ViewObject(PathObject):

    def __init__(self, parent, name, **params):
        self.name = name
        PathObject.__init__(self, parent, **params)

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if self.name == 'download':
            disposition = 'attachment'
        else:
            disposition = 'inline'
        if name.isdigit():
            kind = self.context.type_manager.get_type(int(name))
        else:
            kind = 'attachment'
        if kind == 'attachment':
            entity = self.context.run_command('attachment::get', uuid=name)
            if entity:
                return AttachmentObject(self, name, entity=entity, disposition=disposition, parameters=self.parameters, request=self.request, context=self.context)
            if name.startswith('{'):
                message_uuid = name
            else:
                message_uuid = ('{{{0}}}').format(name)
            entity = self.context.run_command('message::get', uuid=message_uuid)
            if entity:
                return MessageObject(self, name, entity=entity, disposition=disposition, parameters=self.parameters, request=self.request, context=self.context)
            raise CoilsException(('Unable to access attachment "{0}"').format(name))
        else:
            if kind == 'Document':
                entity = self.context.run_command('document::get', id=int(name))
                if entity is None:
                    raise CoilsException(('Unable to access documentId#{0}').format(name))
                return DocumentObject(self, name, entity=entity, disposition=disposition, parameters=self.parameters, request=self.request, context=self.context)
            if kind == 'Process':
                entity = self.context.run_command('process::get', id=int(name))
                if entity is None:
                    raise CoilsException(('Unable to access processId#{0}').format(name))
                return ProcessObject(self, name, entity=entity, disposition=disposition, parameters=self.parameters, request=self.request, context=self.context)
            raise CoilsException(('Unable to access object type "{0}" via attachfs.').format(kind))
        return