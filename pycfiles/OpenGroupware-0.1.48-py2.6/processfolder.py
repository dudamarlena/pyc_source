# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/processfolder.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.net import *
from messagefolder import MessageFolder
from labelfolder import LabelFolder
from bpmlobject import BPMLObject
from messageobject import MessageObject
from signalobject import SignalObject
from versionsfolder import VersionsFolder
from proplistobject import PropertyListObject
from processlogobject import ProcessLogObject

class ProcessFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)
        self.entity = params['entity']
        self.process_id = self.entity.object_id

    @property
    def label_type(self):
        return 'label'

    def _load_contents(self):
        self.insert_child('Messages', None)
        self.insert_child('Labels', None)
        self.insert_child('input', None)
        self.insert_child('markup.xml', None)
        self.insert_child('Versions', None)
        self.insert_child('propertyList.txt', None)
        self.insert_child('log.html', None)
        if self.entity.completed is not None:
            if self.entity.state == 'C':
                self.insert_child('output', None)
            else:
                self.insert_child('exception', None)
        return True

    def get_input_message(self):
        return self.context.run_command('process::get-input-message', process=self.entity)

    def get_output_message(self):
        if self.entity.completed is None:
            return
        else:
            return self.context.run_command('process::get-output-message', process=self.entity)

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        self.log.debug(('Request for folder key {0}').format(name))
        if name == 'Messages':
            return MessageFolder(self, name, entity=self.entity, parameters=self.parameters, context=self.context, request=self.request)
        else:
            if name == 'Labels':
                return LabelFolder(self, name, entity=self.entity, parameters=self.parameters, context=self.context, request=self.request)
            if name in ('input', 'output', 'exception'):
                if name in ('output', 'exception') and self.entity.output_message is None:
                    self.no_such_path()
                if name == 'input' and self.entity.input_message is None:
                    self.no_such_path()
                if name == 'exception':
                    message = getattr(self, ('get_output_message').format(name))()
                else:
                    message = getattr(self, ('get_{0}_message').format(name))()
                return MessageObject(self, name, entity=message, parameters=self.parameters, process=self.entity, context=self.context, request=self.request)
            if name == 'markup.xml':
                return BPMLObject(self, name, entity=self.entity, context=self.context, request=self.request)
            if name == 'log.html':
                return ProcessLogObject(self, name, entity=self.entity, context=self.context, request=self.request)
            if name == 'signal':
                return SignalObject(self, name, parameters=self.parameters, entity=self.entity, context=self.context, request=self.request)
            if name == 'propertyList.txt':
                return PropertyListObject(self, name, entity=self.entity, context=self.context, request=self.request)
            if name == 'Versions':
                return VersionsFolder(self, name, parameters=self.parameters, entity=self.entity, context=self.context, request=self.request)
            self.no_such_path()
            return