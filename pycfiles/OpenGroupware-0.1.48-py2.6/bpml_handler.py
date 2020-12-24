# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/bpml_handler.py
# Compiled at: 2012-10-12 07:02:39
import logging
from coils.core import NotImplementedException, CoilsException
from xml.sax.handler import ContentHandler
BPML_BOOTSTRAP_MODE = 0
BPML_PACKAGE_MODE = 1
BPML_PROCESS_MODE = 2
BPML_CONTEXT_MODE = 3
BPML_ACTION_MODE = 4
BPML_INPUT_MODE = 5
BPML_EXTENSION_MODE = 6
BPML_OUTPUT_MODE = 7
BPML_SOURCE_MODE = 8
BPML_EXCEPTION_MODE = 9
BPML_EVENT_MODE = 10
BPML_FAULTS_MODE = 11
BPML_ATTRIBUTES_MODE = 12
BPML_FOREACH_MODE = 13
BPML_SWITCH_MODE = 14
BPML_CASE_MODE = 15
BPML_UNTIL_MODE = 16
BPML_WHILE_MODE = 17
BPML_SEQUENCE_MODE = 18
BPML_CONDITION_MODE = 19
BPML_DEFAULT_MODE = 20
BPML_UNDEFINED_MODE = 21

class BPMLSAXHandler(ContentHandler):

    def __init__(self):
        ContentHandler.__init__(self)
        self.mode = [BPML_BOOTSTRAP_MODE]
        self.actions = {}
        self.result = {}
        self.log = logging.getLogger('xml:bpml')
        self._io_flip = True
        self._stack = []

    @property
    def stack_tip(self):
        if len(self._stack) > 0:
            return self._stack[(-1)]
        else:
            return

    def pop_stack(self):
        if len(self._stack) > 0:
            return self._stack.pop()
        else:
            return

    @property
    def current_mode(self):
        return self.mode[(-1)]

    def startElement(self, name, attrs):
        if name == 'package' and self.mode[(-1)] == BPML_BOOTSTRAP_MODE:
            self.mode.append(BPML_PACKAGE_MODE)
            self.current_uuid = None
            self.previous_uuid = None
            self.context_uuid = None
            self._stack = []
            self.result['__namespace__'] = attrs.get('targetNamespace')
        elif name == 'process' and self.current_mode == BPML_PACKAGE_MODE:
            self.mode.append(BPML_PROCESS_MODE)
            self.process_name = attrs.get('name', None)
        elif name == 'event' and self.current_mode == BPML_PROCESS_MODE:
            self.mode.append(BPML_EVENT_MODE)
        elif name == 'context':
            self.mode.append(BPML_CONTEXT_MODE)
        else:
            if name == 'action':
                if self.current_mode in [BPML_CONTEXT_MODE, BPML_PROCESS_MODE]:
                    self.previous_uuid = None
                self.current_uuid = attrs.get('id', None)
                if self.previous_uuid == None:
                    if self.current_mode == BPML_EXCEPTION_MODE:
                        self.actions['__error__'] = self.current_uuid
                    elif self.current_mode == BPML_PROCESS_MODE:
                        self.actions['__start__'] = self.current_uuid
                        self._io_flip = False
                elif self.current_mode == BPML_FOREACH_MODE and self.stack_tip == self.previous_uuid:
                    self.actions[self.previous_uuid]['branch'] = self.current_uuid
                    self._io_flip = True
                elif self.current_mode == BPML_CASE_MODE and self.stack_tip == self.previous_uuid:
                    self.actions[self.previous_uuid]['cases'][(-1)]['action'] = self.current_uuid
                    self._io_flip = True
                elif self.current_mode == BPML_DEFAULT_MODE and self.stack_tip == self.previous_uuid:
                    self.actions[self.stack_tip]['default']['action'] = self.current_uuid
                    self._io_flip = True
                else:
                    self.actions[self.previous_uuid]['next'] = self.current_uuid
                    self._io_flip = True
                if self.current_mode == BPML_EXCEPTION_MODE:
                    self.actions[self.current_uuid] = {'previous': None, 'next': None, 'control': None, 
                       'input': None, 
                       'output': None, 
                       'params': {}, 'name': attrs.get('name')}
                elif self.previous_uuid is None:
                    self.actions[self.current_uuid] = {'previous': None, 'next': None, 'control': 'start', 
                       'input': None, 
                       'output': None, 
                       'params': {}, 'name': attrs.get('name')}
                else:
                    self.actions[self.current_uuid] = {'previous': self.previous_uuid, 'next': None, 
                       'control': None, 
                       'input': None, 
                       'output': None, 
                       'params': {}, 'name': attrs.get('name')}
                self.mode.append(BPML_ACTION_MODE)
                if self.previous_uuid:
                    if 'tails' in self.actions[self.previous_uuid]:
                        for tail in self.actions[self.previous_uuid]['tails']:
                            self.actions[tail]['next'] = self.current_uuid

                self.previous_uuid = self.current_uuid
            elif name == 'faults':
                self.mode.append(BPML_FAULTS_MODE)
            elif name == 'attributes':
                self.mode.append(BPML_ATTRIBUTES_MODE)
            elif name == 'input' and self.mode[(-1)] == BPML_ACTION_MODE:
                self.mode.append(BPML_INPUT_MODE)
                if self._io_flip:
                    self.actions[self.current_uuid]['output'] = {'label': attrs.get('property'), 'format': attrs.get('formatter')}
                else:
                    self.actions[self.current_uuid]['input'] = {'label': attrs.get('property'), 'format': attrs.get('formatter')}
            elif name == 'output' and self.current_mode == BPML_ACTION_MODE:
                self.mode.append(BPML_OUTPUT_MODE)
            elif name == 'extension' and self.current_mode == BPML_ATTRIBUTES_MODE:
                self.mode.append(BPML_EXTENSION_MODE)
                self.name = attrs.get('name')
            elif name == 'source' and self.current_mode in (BPML_OUTPUT_MODE, BPML_FOREACH_MODE):
                self.mode.append(BPML_SOURCE_MODE)
                if self._io_flip:
                    self.actions[self.current_uuid]['input'] = {'label': attrs.get('property'), 'format': None}
                else:
                    self.actions[self.current_uuid]['output'] = {'label': attrs.get('property'), 'format': None}
            elif name == 'exception' and self.current_mode == BPML_CONTEXT_MODE:
                self.mode.append(BPML_EXCEPTION_MODE)
            elif name == 'foreach':
                self.mode.append(BPML_FOREACH_MODE)
                self.current_uuid = attrs.get('id', None)
                self._stack.append(self.current_uuid)
                self.actions[self.current_uuid] = {'previous': self.previous_uuid, 'control': 'foreach', 
                   'branch': None, 
                   'next': None, 
                   'input': None, 
                   'output': None, 
                   'params': {'xpath': attrs.get('select')}, 'name': attrs.get('name')}
                self.actions[self.previous_uuid]['next'] = self.current_uuid
                self.previous_uuid = self.current_uuid
            elif name == 'switch':
                self.current_uuid = attrs.get('id', None)
                if self.current_mode == BPML_FOREACH_MODE:
                    self.actions[self.previous_uuid]['branch'] = self.current_uuid
                self.mode.append(BPML_SWITCH_MODE)
                self._stack.append(self.current_uuid)
                self.actions[self.current_uuid] = {'previous': self.previous_uuid, 'control': 'switch', 
                   'next': None, 
                   'input': None, 
                   'output': None, 
                   'tails': [], 'cases': [], 'name': attrs.get('name')}
                if self.previous_uuid is not None:
                    self.actions[self.previous_uuid]['next'] = self.current_uuid
                self.previous_uuid = self.current_uuid
            elif name == 'case' and self.current_mode == BPML_SWITCH_MODE:
                self.mode.append(BPML_CASE_MODE)
                self.current_case = attrs.get('id')
            elif name == 'condition' and self.current_mode == BPML_CASE_MODE:
                self.mode.append(BPML_CONDITION_MODE)
                self.actions[self.current_uuid]['cases'].append({'expression': attrs.get('expression'), 'id': self.current_case, 
                   'action': None})
            elif name == 'condition' and self.current_mode == BPML_DEFAULT_MODE:
                self.mode.append(BPML_CONDITION_MODE)
            elif name == 'default' and self.current_mode == BPML_SWITCH_MODE:
                self.mode.append(BPML_DEFAULT_MODE)
                self.current_case = attrs.get('id')
                self.actions[self.previous_uuid]['default'] = {'id': self.current_case, 'action': None}
            else:
                self.mode.append(BPML_UNDEFINED_MODE)
                self.log.warn(('Unprocessed start of element {0}').format(name))
            return

    def endElement(self, name):
        if name == 'process':
            self.result[self.process_name] = self.actions
            self.actions = {}
        elif name in ('case', 'default'):
            self.previous_uuid = self.stack_tip
            self.current_case = None
            self.actions[self.previous_uuid]['tails'].append(self.last_action)
        elif name in ('foreach', 'switch', 'sequence', 'until', 'while'):
            if name == 'switch':
                for tail in self.actions[self.previous_uuid]['tails']:
                    self.actions[tail]['next'] = None

            stack_id = self.pop_stack()
            self.current_uuid = stack_id
            self.previous_uuid = stack_id
        elif name == 'action':
            self.last_action = self.current_uuid
            self.current_uuid = self.stack_tip
            do_tails = True
        self.mode = self.mode[:-1]
        return

    def characters(self, chars):
        if self.current_mode == BPML_EXTENSION_MODE and self.current_uuid is not None:
            if self.name is None:
                self.log.warn('Extension data with no name.')
            else:
                if 'params' not in self.actions[self.current_uuid]:
                    tmp = self.actions[self.current_uuid]['params'] = {}
                tmp = self.actions[self.current_uuid]['params'].get(self.name, '')
                self.actions[self.current_uuid]['params'][self.name] = ('{0}{1}').format(tmp, chars)
                tmp = None
        return

    def get_processes(self):
        return self.result