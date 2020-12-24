# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_each_block_unique_and_defined.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 6394 bytes
from pynestml.meta_model.ast_neuron import ASTNeuron
from pynestml.cocos.co_co import CoCo
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages

class CoCoEachBlockUniqueAndDefined(CoCo):
    __doc__ = '\n    This context  condition ensures that each block is defined at most once.\n    Not allowed:\n        state:\n            ...\n        end\n        ...\n        state:\n            ...\n        end\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Checks whether each block is define at most once.
        :param node: a single neuron.
        :type node: ASTNeuron
        """
        assert node is not None and isinstance(node, ASTNeuron), '(PyNestML.CoCo.BlocksUniques) No or wrong type of neuron provided (%s)!' % type(node)
        if isinstance(node.get_state_blocks(), list) and len(node.get_state_blocks()) > 1:
            code, message = Messages.get_block_not_defined_correctly('State', False)
            Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
        if isinstance(node.get_update_blocks(), list) and len(node.get_update_blocks()) > 1:
            code, message = Messages.get_block_not_defined_correctly('Update', False)
            Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
        else:
            if node.get_update_blocks() is None:
                code, message = Messages.get_block_not_defined_correctly('Update', True)
                Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
            elif isinstance(node.get_update_blocks(), list) and len(node.get_update_blocks()) == 0:
                code, message = Messages.get_block_not_defined_correctly('Update', True)
                Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
        if isinstance(node.get_parameter_blocks(), list) and len(node.get_parameter_blocks()) > 1:
            code, message = Messages.get_block_not_defined_correctly('Parameters', False)
            Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
        if isinstance(node.get_internals_blocks(), list) and len(node.get_internals_blocks()) > 1:
            code, message = Messages.get_block_not_defined_correctly('Internals', False)
            Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
        if isinstance(node.get_equations_blocks(), list) and len(node.get_equations_blocks()) > 1:
            code, message = Messages.get_block_not_defined_correctly('Equations', False)
            Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
        if isinstance(node.get_input_blocks(), list) and len(node.get_input_blocks()) > 1:
            code, message = Messages.get_block_not_defined_correctly('Input', False)
            Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
        else:
            if isinstance(node.get_input_blocks(), list) and len(node.get_input_blocks()) == 0:
                code, message = Messages.get_block_not_defined_correctly('Input', True)
                Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
            else:
                if node.get_input_blocks() is None:
                    code, message = Messages.get_block_not_defined_correctly('Input', True)
                    Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
                if isinstance(node.get_output_blocks(), list) and len(node.get_output_blocks()) > 1:
                    code, message = Messages.get_block_not_defined_correctly('Output', False)
                    Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
                else:
                    if isinstance(node.get_output_blocks(), list) and len(node.get_output_blocks()) == 0:
                        code, message = Messages.get_block_not_defined_correctly('Output', True)
                        Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
                    elif node.get_output_blocks() is None:
                        code, message = Messages.get_block_not_defined_correctly('Output', True)
                        Logger.log_message(code=code, message=message, neuron=node, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)