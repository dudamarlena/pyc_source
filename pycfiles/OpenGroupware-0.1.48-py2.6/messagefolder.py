# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/messagefolder.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.net import *
from messageobject import MessageObject
from workflow import WorkflowPresentation

class MessageFolder(DAVFolder, WorkflowPresentation):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)
        self.process_id = self.entity.object_id

    @property
    def label_type(self):
        return 'uuid'

    def _load_contents(self):
        self.log.debug(('Returning enumeration of messages of process {0}.').format(self.process_id))
        messages = self.get_process_messages(self.entity)
        for message in messages:
            self.insert_child(message.uuid.strip()[1:-1], message)

        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        self.log.debug(('Request for folder key {0}').format(name))
        if self.load_contents():
            if self.has_child(name):
                return MessageObject(self, name, entity=self.get_child(name), parameters=self.parameters, process=self.entity, context=self.context, request=self.request)
        raise NoSuchPathException('Not such path as %s' % self.request.path)