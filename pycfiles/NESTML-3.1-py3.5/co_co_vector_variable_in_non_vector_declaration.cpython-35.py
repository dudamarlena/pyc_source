# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_vector_variable_in_non_vector_declaration.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3177 bytes
from pynestml.meta_model.ast_neuron import ASTNeuron
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.symbol import SymbolKind
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoVectorVariableInNonVectorDeclaration(CoCo):
    __doc__ = '\n    This coco ensures that vector variables are not used in non vector declarations.\n    Not allowed:\n        function three integer[n] = 3\n        threePlusFour integer = three + 4 <- error: threePlusFour is not a vector\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ASTNeuron
        """
        assert node is not None and isinstance(node, ASTNeuron), '(PyNestML.CoCo.BufferNotAssigned) No or wrong type of neuron provided (%s)!' % type(node)
        node.accept(VectorInDeclarationVisitor())


class VectorInDeclarationVisitor(ASTVisitor):
    __doc__ = '\n    This visitor checks if somewhere in a declaration of a non-vector value, a vector is used.\n    '

    def visit_declaration(self, node):
        """
        Checks the coco.
        :param node: a single declaration.
        :type node: ast_declaration
        """
        if node.has_expression():
            variables = node.get_expression().get_variables()
            for variable in variables:
                if variable is not None:
                    symbol = node.get_scope().resolve_to_symbol(variable.get_complete_name(), SymbolKind.VARIABLE)
                    if symbol is not None and symbol.has_vector_parameter() and not node.has_size_parameter():
                        code, message = Messages.get_vector_in_non_vector(vector=symbol.get_symbol_name(), non_vector=list(var.get_complete_name() for var in node.get_variables()))
                        Logger.log_message(error_position=node.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)