# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_node.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 6669 bytes
from abc import ABCMeta, abstractmethod
from pynestml.meta_model.ast_source_location import ASTSourceLocation

class ASTNode(object):
    __doc__ = '\n    This class is not a part of the grammar but is used to store commonalities of all possible meta_model classes, e.g.,\n    the source position. This class is abstract, thus no instances can be created.\n    Attributes:\n        sourcePosition = None\n        scope = None\n        comment = None\n        #\n        pre_comments = list()\n        in_comment = None\n        post_comments = list()\n        #\n        implicit_conversion_factor = None\n    '
    __metaclass__ = ABCMeta

    def __init__(self, source_position, scope=None):
        """
        The standard constructor.
        :param source_position: a source position element.
        :type source_position: ASTSourceLocation
        :param scope: the scope in which this element is embedded in.
        :type scope: Scope
        """
        self.sourcePosition = source_position
        self.scope = scope
        self.comment = None
        self.pre_comments = list()
        self.in_comment = None
        self.post_comments = list()
        self.implicit_conversion_factor = None

    def set_implicit_conversion_factor(self, implicit_factor):
        """
        Sets a factor that, when applied to the (unit-typed) expression, converts it to the magnitude of the
        context where it is used. eg. Volt + milliVolt needs to either be
        1000*Volt + milliVolt or Volt + 0.001 * milliVolt
        :param implicit_factor: the factor to be installed
        :type implicit_factor: float
        :return: nothing
        """
        from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
        from pynestml.meta_model.ast_expression import ASTExpression
        if not isinstance(self, ASTExpression):
            assert isinstance(self, ASTSimpleExpression)
        self.implicit_conversion_factor = implicit_factor

    def get_implicit_conversion_factor(self):
        """
        Returns the factor installed as implicitConversionFactor for this expression
        :return: the conversion factor, if present, or None
        """
        from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
        from pynestml.meta_model.ast_expression import ASTExpression
        if not isinstance(self, ASTExpression):
            assert isinstance(self, ASTSimpleExpression)
        return self.implicit_conversion_factor

    def get_source_position(self):
        """
        Returns the source position of the element.
        :return: a source position object.
        :rtype: ASTSourceLocation
        """
        if self.sourcePosition is not None:
            return self.sourcePosition
        else:
            return ASTSourceLocation.get_predefined_source_position()

    def set_source_position(self, new_position):
        """
        Updates the source position of the element.
        :param new_position: a new source position
        :type new_position: ASTSourceLocation
        :return: a source position object.
        :rtype: ASTSourceLocation
        """
        self.sourcePosition = new_position

    def get_scope(self):
        """
        Returns the scope of this element.
        :return: a scope object.
        :rtype: Scope 
        """
        return self.scope

    def update_scope(self, _scope):
        """
        Updates the scope of this element.
        :param _scope: a scope object.
        :type _scope: Scope
        """
        self.scope = _scope

    def get_comment(self):
        """
        Returns the comment of this element.
        :return: a comment.
        :rtype: str
        """
        return self.comment

    def set_comment(self, comment):
        """
        Updates the comment of this element.
        :param comment: a comment
        :type comment: str
        """
        self.comment = comment

    def has_comment(self):
        """
        Indicates whether this element stores a prefix.
        :return: True if has comment, otherwise False.
        :rtype: bool
        """
        return self.comment is not None and len(self.comment) > 0

    def print_comment(self, prefix):
        """
        Prints the comment of this meta_model element.
        :param prefix: a prefix string
        :type prefix: str
        :return: a comment
        :rtype: str
        """
        ret = ''
        if not self.has_comment():
            if prefix is not None:
                return prefix
            return ''
        for comment in self.get_comment():
            ret += (prefix + ' ' if prefix is not None else '') + comment + ('\n' if self.get_comment().index(comment) < len(self.get_comment()) - 1 else '')

        return ret

    @abstractmethod
    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        pass

    def accept(self, visitor):
        """
        Double dispatch for visitor pattern.
        :param visitor: A visitor.
        :type visitor: Inherited from ASTVisitor.
        """
        visitor.handle(self)

    def __str__(self):
        from pynestml.utils.ast_nestml_printer import ASTNestMLPrinter
        return ASTNestMLPrinter().print_node(self)

    @abstractmethod
    def equals(self, other):
        """
        The equals operation.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        pass