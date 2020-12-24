# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/codegeneration/codegenerator.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2303 bytes
from pynestml.utils.logger import Logger
from pynestml.utils.logger import LoggingLevel
from pynestml.utils.messages import Messages

class CodeGenerator(object):

    def __init__(self, target):
        assert target in self.get_known_targets()
        self._target = target

    def generate_neurons(self, neurons):
        """
        Analyse a list of neurons, solve them and generate the corresponding code.
        :param neurons: a list of neurons.
        """
        from pynestml.frontend.frontend_configuration import FrontendConfiguration
        for neuron in neurons:
            self.generate_neuron_code(neuron)
            if not Logger.has_errors(neuron):
                code, message = Messages.get_code_generated(neuron.get_name(), FrontendConfiguration.get_target_path())
                Logger.log_message(neuron, code, message, neuron.get_source_position(), LoggingLevel.INFO)

    @staticmethod
    def get_known_targets():
        return ['NEST', '']

    def generate_code(self, neurons):
        if self._target == 'NEST':
            from pynestml.codegeneration.nest_codegenerator import NESTCodeGenerator
            _codeGenerator = NESTCodeGenerator()
            _codeGenerator.generate_code(neurons)
        elif self._target == '':
            code, message = Messages.get_no_code_generated()
            Logger.log_message(None, code, message, None, LoggingLevel.INFO)