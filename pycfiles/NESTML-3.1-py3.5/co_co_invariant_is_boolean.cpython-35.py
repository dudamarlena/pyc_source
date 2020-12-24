# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_invariant_is_boolean.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2819 bytes
from pynestml.meta_model.ast_declaration import ASTDeclaration
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.utils.logger import Logger
from pynestml.utils.logger import LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoInvariantIsBoolean(CoCo):
    __doc__ = '\n    This coco checks that all invariants are of type boolean\n\n    '

    @classmethod
    def check_co_co(cls, neuron):
        """
        Ensures the coco for the handed over neuron.
        :param neuron: a single neuron instance.
        :type neuron: ast_neuron
        """
        visitor = InvariantTypeVisitor()
        neuron.accept(visitor)


class InvariantTypeVisitor(ASTVisitor):
    __doc__ = '\n    Checks if for each invariant, the type is boolean.\n    '

    def visit_declaration(self, node):
        """
        Checks the coco for a declaration.
        :param node: a single declaration.
        :type node: ASTDeclaration
        """
        assert isinstance(node, ASTDeclaration)
        if node.has_invariant():
            invariant_type = node.get_invariant().type
            if invariant_type is None or isinstance(invariant_type, ErrorTypeSymbol):
                code, message = Messages.get_type_could_not_be_derived(str(node.get_invariant()))
                Logger.log_message(error_position=node.get_invariant().get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)
        elif not invariant_type.equals(PredefinedTypes.get_boolean_type()):
            code, message = Messages.get_type_different_from_expected(PredefinedTypes.get_boolean_type(), invariant_type)
            Logger.log_message(error_position=node.get_invariant().get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)