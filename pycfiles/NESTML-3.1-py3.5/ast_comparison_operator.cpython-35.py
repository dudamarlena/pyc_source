# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_comparison_operator.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3444 bytes
from pynestml.meta_model.ast_node import ASTNode
from pynestml.meta_model.ast_source_location import ASTSourceLocation

class ASTComparisonOperator(ASTNode):
    __doc__ = "\n    This class is used to store a single comparison operator.\n    Grammar:\n        comparisonOperator : (lt='<' | le='<=' | eq='==' | ne='!=' | ne2='<>' | ge='>=' | gt='>');\n    Attributes:\n        is_lt = False\n        is_le = False\n        is_eq = False\n        is_ne = False\n        is_ne2 = False\n        is_ge = False\n        is_gt = False\n    "

    def __init__(self, is_lt=False, is_le=False, is_eq=False, is_ne=False, is_ne2=False, is_ge=False, is_gt=False, source_position=None):
        """
        Standard constructor.
        :param is_lt: is less than operator.
        :type is_lt: bool
        :param is_le: is less equal operator.
        :type is_le: bool
        :param is_eq: is equality operator.
        :type is_eq: bool
        :param is_ne: is not equal operator.
        :type is_ne: bool
        :param is_ne2: is not equal operator (alternative syntax).
        :type is_ne2: bool
        :param is_ge: is greater equal operator.
        :type is_ge: bool
        :param is_gt: is greater than operator.
        :type is_gt: bool
        :param source_position: the position of the element in the source
        :type source_position: ASTSourceLocation
        """
        assert is_lt + is_le + is_eq + is_ne + is_ne2 + is_ge + is_gt == 1, '(PyNestML.AST.ComparisonOperator) Comparison operator not correctly specified!'
        super(ASTComparisonOperator, self).__init__(source_position)
        self.is_gt = is_gt
        self.is_ge = is_ge
        self.is_ne2 = is_ne2
        self.is_ne = is_ne
        self.is_eq = is_eq
        self.is_le = is_le
        self.is_lt = is_lt

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        pass

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTComparisonOperator):
            return False
        return self.is_lt == other.is_lt and self.is_le == other.is_le and self.is_eq == other.is_eq and self.is_ne == other.is_ne and self.is_ne2 == other.is_ne2 and self.is_ge == other.is_ge and self.is_gt == other.is_gt