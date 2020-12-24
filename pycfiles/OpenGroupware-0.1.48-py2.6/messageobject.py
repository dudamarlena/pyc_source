# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/messageobject.py
# Compiled at: 2012-10-12 07:02:39
import io
from datetime import datetime
from coils.core import *
from coils.net import *
from coils.net.ossf import MarshallOSSFChain
from workflow import WorkflowPresentation

class MessageObject(DAVObject, WorkflowPresentation):
    """ Represents a workflow message in a process with a DAV hierarchy. """

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)
        self.log.debug((' MessageObject named {0} is entity {1}').format(name, repr(self.entity)))

    def get_property_webdav_getetag(self):
        return ('{0}:{1}').format(self.entity.uuid, self.entity.version)

    def get_property_webdav_displayname(self):
        if hasattr(self.parent, 'label_type'):
            if self.parent.label_type == 'label':
                if self.entity.label is not None:
                    return self.entity.label
        return self.entity.uuid[1:-1]

    def get_property_webdav_getcontentlength(self):
        return str(self.entity.size)

    def get_property_webdav_getcontenttype(self):
        return self.entity.mimetype

    def get_property_webdav_creationdate(self):
        if self.entity.created is None:
            return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        else:
            return self.entity.created.strftime('%a, %d %b %Y %H:%M:%S GMT')
            return

    def do_HEAD(self):
        if self.entity.label is None:
            label = '__undefined__'
        else:
            label = self.entity.label
        self.request.simple_response(201, mimetype=self.entity.mimetype, headers={'Content-Length': str(self.entity.size), 'ETag': self.get_property_webdav_getetag(), 
           'X-COILS-WORKFLOW-MESSAGE-UUID': self.entity.uuid, 
           'X-COILS-WORKFLOW-PROCESS-ID': self.process.object_id, 
           'X-COILS-WORKFLOW-MESSAGE-LABEL': label})
        return

    def do_GET(self):
        if self.entity.label is None:
            label = '__undefined__'
        else:
            label = self.entity.label
        handle = self.get_message_handle(self.entity)
        if handle is None:
            raise CoilsException('Unable to open handle to message content.')
        self.log.debug(('Document MIME-Type is "{0}"').format(self.entity.mimetype))
        (handle, mimetype) = MarshallOSSFChain(handle, self.entity.mimetype, self.parameters)
        self.log.debug(('MIME-Type after OSSF processing is {0}').format(mimetype))
        self.request.stream_response(200, stream=handle, mimetype=mimetype, headers={'ETag': self.get_property_webdav_getetag(), 
           'X-COILS-WORKFLOW-MESSAGE-UUID': self.entity.uuid, 
           'X-COILS-WORKFLOW-MESSAGE-LABEL': label, 
           'X-COILS-WORKFLOW-PROCESS-ID': self.process.object_id})
        return