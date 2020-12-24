# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/utils/ode_transformer.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4815 bytes
from copy import copy
from pynestml.meta_model.ast_function_call import ASTFunctionCall
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.visitors.ast_higher_order_visitor import ASTHigherOrderVisitor

class OdeTransformer(object):
    __doc__ = '\n    This class contains several methods as used to transform ODEs.\n    '
    sum_functions = (PredefinedFunctions.CURR_SUM, PredefinedFunctions.COND_SUM, PredefinedFunctions.CONVOLVE)

    @classmethod
    def refactor_convolve_call(cls, _ast):
        """
        Replaces all `convolve` calls in the handed over node.
        :param _ast: a single node
        :type _ast: ASTNode
        """
        function_calls = cls.get_sum_function_calls(_ast)
        for call in function_calls:
            cls.replace_function_call_through_first_argument(_ast, call)

    @classmethod
    def replace_function_call_through_first_argument(cls, ast, function_name_to_replace):
        """
        Replaces all occurrences of the handed over function call by the first argument.
        :param ast: a single ast node
        :type ast: ASTNode
        :param function_name_to_replace: the function to replace
        :type function_name_to_replace: ASTFunctionCall
        """

        def replace_function_call_through_first_argument(_expr=None):
            if _expr.is_function_call() and _expr.get_function_call() == function_name_to_replace:
                first_arg = _expr.get_function_call().get_args()[0].get_variable()
                _expr.set_function_call(None)
                _expr.set_variable(first_arg)

        func = lambda x: replace_function_call_through_first_argument(x) if isinstance(x, ASTSimpleExpression) else True
        ast.accept(ASTHigherOrderVisitor(func))

    @classmethod
    def get_sum_function_calls(cls, ast):
        """
        Returns all sum function calls in the handed over meta_model node or one of its children.
        :param ast: a single meta_model node.
        :type ast: ASTNode
        """
        return cls.get_function_calls(ast, cls.sum_functions)

    @classmethod
    def contains_sum_function_call(cls, ast):
        """
        Indicates whether _ast or one of its child nodes contains a sum call.
        :param ast: a single meta_model
        :type ast: ASTNode
        :return: True if sum is contained, otherwise False.
        :rtype: bool
        """
        return len(cls.get_function_calls(ast, cls.sum_functions)) > 0

    @classmethod
    def get_function_calls(cls, ast_node, function_list):
        """
        For a handed over list of function names, this method retrieves all functions in the meta_model.
        :param ast_node: a single meta_model node
        :type ast_node: ASTNode
        :param function_list: a list of function names
        :type function_list: list(str)
        :return: a list of all functions in the meta_model
        :rtype: list(ASTFunctionCall)
        """
        res = list()
        from pynestml.visitors.ast_higher_order_visitor import ASTHigherOrderVisitor
        from pynestml.meta_model.ast_function_call import ASTFunctionCall
        fun = lambda x: res.append(x) if isinstance(x, ASTFunctionCall) and x.get_name() in function_list else True
        vis = ASTHigherOrderVisitor(visit_funcs=fun)
        ast_node.accept(vis)
        return res

    @classmethod
    def get_cond_sum_function_calls(cls, node):
        """
        Collects all cond_sum function calls in the meta_model.
        :param node: a single meta_model node
        :type node: ASTNode
        :return: a list of all functions in the meta_model
        :rtype: list(ASTFunctionCall)
        """
        res = list()

        def loc_get_cond_sum(a_node):
            if isinstance(a_node, ASTFunctionCall) and a_node.get_name() == PredefinedFunctions.COND_SUM:
                res.append(a_node)

        node.accept(ASTHigherOrderVisitor(loc_get_cond_sum))
        return res