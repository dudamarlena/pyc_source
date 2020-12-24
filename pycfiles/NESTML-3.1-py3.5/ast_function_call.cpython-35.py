# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_function_call.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3622 bytes
from pynestml.meta_model.ast_node import ASTNode

class ASTFunctionCall(ASTNode):
    __doc__ = '\n    This class is used to store a single function call.\n    ASTFunctionCall Represents a function call, e.g. myFun("a", "b").\n    @attribute name The (qualified) name of the function\n    @attribute args Comma separated list of expressions representing parameters.\n    Grammar:\n        functionCall : calleeName=NAME \'(\' (rhs (\',\' rhs)*)? \')\';\n    Attributes:\n        callee_name = None\n        args = None\n    '

    def __init__(self, callee_name, args, source_position):
        """
        Standard constructor.
        :param callee_name: the name of the function which is called.
        :type callee_name: str
        :param args: (Optional) List of arguments
        :type args: list(ASTExpression)
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        super(ASTFunctionCall, self).__init__(source_position)
        self.callee_name = callee_name
        self.args = args

    def get_name(self):
        """
        Returns the name of the called function.
        :return: the name of the function.
        :rtype: str.
        """
        return self.callee_name

    def has_args(self):
        """
        Returns whether function call has arguments or not.
        :return: True if has arguments, otherwise False.
        :rtype: bool
        """
        return self.args is not None and len(self.args) > 0

    def get_args(self):
        """
        Returns the list of arguments.
        :return: the list of arguments.
        :rtype: list(ASTExpression)
        """
        return self.args

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        for param in self.get_args():
            if param is ast:
                return self
            if param.get_parent(ast) is not None:
                return param.get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTFunctionCall):
            return False
        if self.get_name() != other.get_name():
            return False
        if len(self.get_args()) != len(other.get_args()):
            return False
        my_args = self.get_args()
        your_args = other.get_args()
        for i in range(0, len(my_args)):
            if not my_args[i].equals(your_args[i]):
                return False

        return True