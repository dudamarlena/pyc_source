# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/flow/sequence.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import ActionCommand

class GetSequenceValue(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'get-sequence-value'
    __aliases__ = ['getSequenceValue', 'getSequenceValueAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        sequence_target = None
        if self._seq_scope == 'process':
            sequence_target = self.process
        elif self._seq_scope == 'route':
            sequence_target = self.process.route
        elif self._seq_scope == 'global':
            raise NotImplementedException()
        else:
            raise CoilsException('Invalid execution path! Possible security model violation.')
        if not sequence_target:
            raise CoilsException(('Unable to determine the target for scope of sequence "{0}"').format(self._seq_name))
        prop = self._ctx.property_manager.get_property(sequence_target, 'http://www.opengroupware.us', self._seq_name)
        value = None
        if prop:
            value = prop.get_value()
            if value:
                try:
                    value = long(value)
                except:
                    error = ('Workflow sequence value is corrupted: sequence={0} value="{1}" scope={2}').format(self._seq_name, value, self._seq_scope)
                    raise CoilsException(error)

        if not value:
            value = self._first_value
        if value:
            value = value + self._increment
            self._ctx.property_manager.set_property(sequence_target, 'http://www.opengroupware.us', self._seq_name, value)
        self.wfile.write(unicode(value))
        return

    def parse_action_parameters(self):
        self._seq_name = self.process_label_substitutions(self.action_parameters.get('name', ''))
        if not self._seq_name:
            raise CoilsException('A sequence name must be specified for getSequenceValueAction')
        self._seq_name = ('sequence_{0}').format(self._seq_name.lower())
        self._seq_scope = self.action_parameters.get('scope', 'process')
        self._seq_scope = self.process_label_substitutions(self._seq_scope)
        self._seq_scope = self._seq_scope.lower()
        if self._seq_scope not in ('process', 'global', 'route'):
            error = ('scope parameter for getSequenceValueAction must be "process", "route", or "global"; value was "{0}"').format(self._seq_scope)
            raise CoilsException(error)
        self._increment = self.process_label_substitutions(self.action_parameters.get('increment', '1'))
        try:
            self._increment = long(self._increment)
        except:
            error = ('increment parameter for getSequenceValueAction must be numeric; value was "{0}"').format(self._increment)
            raise CoilsException(error)

        self._first_value = self.action_parameters.get('initialValue', None)
        if self._first_value:
            self._first_value = self.process_label_substitutions(self._first_value)
            try:
                self._first_value = long(self._first_value)
            except:
                error = ('initialValue parameter for getSequenceValueAction must be numeric; value was "{0}"').format(self._increment)
                raise CoilsException(error)

        return

    def do_epilogue(self):
        pass