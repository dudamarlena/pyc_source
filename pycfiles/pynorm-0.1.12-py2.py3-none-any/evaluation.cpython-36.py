# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/expression/evaluation.py
# Compiled at: 2019-05-21 18:06:07
# Size of source mod 2**32: 18663 bytes
import uuid
from norm.utils import hash_df
from pandas import DataFrame, Series, Index
from norm.grammar.literals import COP
from norm.executable import NormError, Projection
from norm.executable.expression.argument import ArgumentExpr
from norm.executable.schema.variable import VariableName, ColumnVariable, JoinVariable
from norm.executable.expression import NormExpression
from collections import OrderedDict
from typing import List, Dict
import logging
logger = logging.getLogger(__name__)

class EvaluationExpr(NormExpression):

    def __init__(self, args, variable=None, projection=None):
        """
        The evaluation of an expression either led by a variable name
        :param args: the arguments provided
        :type args: List[ArgumentExpr]
        :param variable: the variable name to evaluate
        :type variable: VariableName
        :type projection: Projection
        """
        super().__init__()
        self.variable = variable
        self.args = args
        self.inputs = None
        self.outputs = None
        self.joins = []
        self.projection = projection

    @property
    def is_constant_arguments(self):
        return all(arg.is_constant for arg in self.args)

    def check_assignment_arguments--- This code section failed: ---

 L.  49         0  LOAD_CONST               False
                2  STORE_FAST               'keyword_arg'

 L.  50         4  SETUP_LOOP          100  'to 100'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                args
               10  GET_ITER         
               12  FOR_ITER             98  'to 98'
               14  STORE_FAST               'arg'

 L.  51        16  LOAD_FAST                'arg'
               18  LOAD_ATTR                op
               20  LOAD_CONST               None
               22  COMPARE_OP               is
               24  POP_JUMP_IF_FALSE    92  'to 92'

 L.  52        26  LOAD_FAST                'arg'
               28  LOAD_ATTR                variable
               30  LOAD_CONST               None
               32  COMPARE_OP               is
               34  POP_JUMP_IF_FALSE    86  'to 86'

 L.  53        36  LOAD_FAST                'keyword_arg'
               38  POP_JUMP_IF_FALSE    90  'to 90'

 L.  54        40  LOAD_STR                 'Keyword based arguments should come after positional arguments'
               42  STORE_FAST               'msg'

 L.  55        44  LOAD_GLOBAL              logger
               46  LOAD_ATTR                error
               48  LOAD_FAST                'msg'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  POP_TOP          

 L.  56        54  LOAD_GLOBAL              logger
               56  LOAD_ATTR                error
               58  LOAD_LISTCOMP            '<code_object <listcomp>>'
               60  LOAD_STR                 'EvaluationExpr.check_assignment_arguments.<locals>.<listcomp>'
               62  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                args
               68  GET_ITER         
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  POP_TOP          

 L.  57        76  LOAD_GLOBAL              NormError
               78  LOAD_FAST                'msg'
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  RAISE_VARARGS_1       1  'exception'
               84  JUMP_ABSOLUTE        96  'to 96'
               86  ELSE                     '90'

 L.  59        86  LOAD_CONST               True
               88  STORE_FAST               'keyword_arg'
             90_0  COME_FROM            38  '38'
               90  JUMP_BACK            12  'to 12'
               92  ELSE                     '96'

 L.  61        92  LOAD_CONST               False
               94  RETURN_VALUE     
               96  JUMP_BACK            12  'to 12'
               98  POP_BLOCK        
            100_0  COME_FROM_LOOP        4  '4'

 L.  62       100  LOAD_CONST               True
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ELSE' instruction at offset 92

    def build_assignment_inputs(self, lam):
        """
        If the arguments are in assignment style, build the inputs as assignments
        :param lam: given the Lambda to be evaluated
        :return: a dictionary mapping from a variable to an expression for the inputs
        :rtype: Dict
        """
        if lam.nargs == 0:
            from norm.models.norm import Lambda
            return OrderedDict((arg.variable.name if arg.variable else '{}{}'.format(Lambda.VAR_ANONYMOUS_STUB, i), arg.expr) for i, arg in enumerate(self.args))
        else:
            keyword_arg = False
            inputs = OrderedDict()
            from norm.models.norm import Variable
            for ov, arg in zip(lam.variables, self.args):
                if arg.expr is None:
                    pass
                else:
                    if arg.op is None:
                        if arg.variable is not None:
                            keyword_arg = True
                        inputs[ov.name] = keyword_arg or arg.expr
                    else:
                        inputs[arg.variable.name] = arg.expr

            return inputs

    def build_conditional_inputs(self):
        """
        If the arguments are in conditional style, build the inputs as conditionals
        :return: a query string
        :rtype: Dict
        """
        inputs = []
        for arg in self.args:
            if not arg.op is None:
                if arg.expr is None:
                    pass
                else:
                    vn = arg.variable.name
                    if isinstance(arg.variable, JoinVariable):
                        self.joins.append(arg.variable)
                        vn = str(arg.variable)
                    if arg.op == COP.LK:
                        condition = '{}.str.contains({})'.format(vn, arg.expr)
                    else:
                        condition = '{} {} ({})'.format(vn, arg.op, arg.expr)
                    inputs.append(condition)

        return ' and '.join(inputs)

    def build_outputs(self, lam):
        """
        Build the outputs according to the projection
        :return: a dictionary mapping from the original variable to the new variable
        :rtype: Dict
        """
        from norm.models.norm import Lambda
        assert isinstance(lam, Lambda)
        outputs = OrderedDict()
        from norm.models.norm import Variable
        for ov, arg in zip(lam.variables, self.args):
            if arg.projection is not None:
                if not len(arg.projection.variables) <= 1:
                    raise AssertionError
                elif not not arg.projection.to_evaluate:
                    raise AssertionError
                if arg.variable is None:
                    outputs[ov.name] = arg.projection.variables[0].name
                else:
                    if len(arg.projection.variables) == 0:
                        outputs[arg.variable.name] = arg.variable.name
                    else:
                        outputs[arg.variable.name] = arg.projection.variables[0].name

        if self.projection is not None:
            if not len(self.projection.variables) <= 1:
                raise AssertionError
            else:
                if not not self.projection.to_evaluate:
                    raise AssertionError
                else:
                    if self.projection.num == 1:
                        new_lambda_name = self.projection.variables[0].name
                    else:
                        new_lambda_name = lam.name
                outputs = OrderedDict((key, self.VARIABLE_SEPARATOR.join([new_lambda_name, value])) for key, value in outputs.items())
                if lam.is_functional:
                    outputs[lam.VAR_OUTPUT] = new_lambda_name
                else:
                    outputs[lam.VAR_OID] = new_lambda_name
        return outputs

    def compile(self, context):
        if self.variable is None:
            from norm.models.norm import Lambda
            assert context.scope is not None
            assert isinstance(context.scope, Lambda)
            lam = context.scope
            assert self.check_assignment_arguments()
            self.inputs = self.build_assignment_inputs(lam)
            self.outputs = None
            is_to_add_data = True
        else:
            lam = self.variable.lam
            if lam is None:
                return self
            if self.check_assignment_arguments():
                self.inputs = self.build_assignment_inputs(lam)
                is_to_add_data = not lam.atomic
            else:
                self.inputs = self.build_conditional_inputs()
                is_to_add_data = False
            self.outputs = self.build_outputs(lam)
            is_to_add_data &= len(self.outputs) == 0
        if is_to_add_data:
            return AddDataEvaluationExpr(lam, self.inputs, self.variable is not None).compile(context)
        else:
            if isinstance(self.inputs, dict):
                if self.projection is not None and self.projection.num == 1:
                    output_projection = self.projection.variables[0].name
                else:
                    output_projection = None
            else:
                if lam.atomic:
                    return AtomicEvaluationExpr(lam, self.inputs, output_projection).compile(context)
                if len(self.inputs) == 0:
                    if isinstance(self.variable, ColumnVariable):
                        return ArgumentExpr(self.variable, None, None, self.projection).compile(context)
                    else:
                        if self.projection is not None:
                            if len(self.outputs) == 1:
                                return RetrieveAllDataExpr(lam, output_projection).compile(context)
                        return RetrievePartialDataExpr(lam, self.outputs).compile(context)
                self.eval_lam = lam
                from norm.models import Lambda, Variable
                if len(self.outputs) > 0:
                    variables = [Variable(self.outputs[v.name], v.type_) for v in self.eval_lam.variables if v.name in self.outputs.keys()]
                else:
                    variables = self.eval_lam.variables
            self.lam = Lambda((context.context_namespace), (context.TMP_VARIABLE_STUB + str(uuid.uuid4())), variables=variables)
            return self

    def execute(self, context):
        for jv in self.joins:
            jv.execute(context)

        df = self.eval_lam.data.query((self.inputs), engine='python')
        if isinstance(df, DataFrame):
            if len(self.outputs) > 0:
                df = df[self.outputs.keys()].rename(columns=(self.outputs))
        self.lam.data = df
        return df


class AtomicEvaluationExpr(NormExpression):

    def __init__(self, lam, inputs, output_projection=None):
        """
        Evaluate the atomic function
        :param lam: the function to evaluate
        :param inputs: the input values
        :param output_projection: the output projection
        """
        super().__init__()
        from norm.models.norm import Lambda
        if not lam is not None:
            raise AssertionError
        else:
            assert isinstance(lam, Lambda)
            assert isinstance(inputs, dict)
        self.eval_lam = lam
        self.lam = lam.output_type
        self.inputs = inputs
        self.output_projection = output_projection

    def __str__(self):
        return '{}({})'.format(self.eval_lam.signature, ', '.join('{}={}'.format(key, value) for key, value in self.inputs.items()))

    def compile(self, context):
        return self

    def execute(self, context):
        inputs = dict((key, value.execute(context)) for key, value in self.inputs.items())
        result = (self.eval_lam)(**inputs)
        if self.output_projection is not None:
            import numpy
            if isinstance(result, (list, numpy.ndarray)):
                return Series(result, name=(self.output_projection))
            if isinstance(result, (Series, Index)):
                return result.rename(self.output_projection)
            if isinstance(result, DataFrame):
                cols = {col:'{}{}{}'.format(self.output_projection, self.VARIABLE_SEPARATOR, col) for col in result.columns}
                return result.loc[result.index.rename(self.output_projection)].rename(columns=cols)
            return Series([result], name=(self.output_projection))
        else:
            return result


class RetrievePartialDataExpr(NormExpression):

    def __init__(self, lam, outputs):
        super().__init__()
        from norm.models.norm import Lambda
        if not lam is not None:
            raise AssertionError
        else:
            assert isinstance(lam, Lambda)
            assert not lam.atomic
        self.eval_lam = lam
        self.lam = None
        self.outputs = outputs

    def __str__(self):
        oid = self.eval_lam.VAR_OID
        out = self.eval_lam.VAR_OUTPUT
        return '{}({}){}'.format(self.eval_lam.signature, ', '.join('{}?'.format(c) for c in self.outputs.keys() if c != oid if c != out), '?' if self.outputs.get(oid) or self.outputs.get(out) else '')

    def compile(self, context):
        from norm.models import Lambda, Variable
        if len(self.outputs) > 0:
            variables = [Variable(self.outputs[v.name], v.type_) for v in self.eval_lam.variables if v.name in self.outputs.keys()]
        else:
            variables = self.eval_lam.variables
        self.lam = Lambda((context.context_namespace), (context.TMP_VARIABLE_STUB + str(uuid.uuid4())), variables=variables)
        return self

    def execute(self, context):
        oid_output_col = self.outputs.get(self.eval_lam.VAR_OID)
        if oid_output_col is not None:
            del self.outputs[self.eval_lam.VAR_OID]
        result = self.eval_lam.data
        result = result[self.outputs.keys()].rename(columns=(self.outputs))
        self.lam.data = result
        if oid_output_col is not None:
            result.index.rename(oid_output_col, inplace=True)
        return result


class RetrieveAllDataExpr(NormExpression):

    def __init__(self, lam, output_projection=None):
        """
        Retrieve all data from the given Lambda
        :param lam: the given Lambda
        :param output_projection: the output projection variable name
        """
        super().__init__()
        from norm.models.norm import Lambda
        if not lam is not None:
            raise AssertionError
        else:
            assert isinstance(lam, Lambda)
            assert not lam.atomic
        self.eval_lam = lam
        self.lam = lam
        self.output_projection = output_projection

    def __str__(self):
        return '{}?'.format(self.lam.signature)

    def compile(self, context):
        return self

    def execute(self, context):
        if self.lam.is_functional:
            result = self.lam.data[self.lam.VAR_OUTPUT]
        else:
            result = self.lam.data.index
        if self.output_projection is not None:
            return result.rename(self.output_projection)
        else:
            return result


class AddDataEvaluationExpr(NormExpression):

    def __init__(self, lam, data, immediately=True):
        """
        Add data to a Lambda. If the lambda is not the current scope, revision occurs immediately. Otherwise,
        revision is delayed to TypeImplementation
        :param lam: the Lambda to add data
        :type lam: norm.model.norm.Lambda
        :param data: the data to add
        :type data: Dict
        :param immediately: whether to revise Lambda as a disjunction immediately, default to True
        :type immediately: bool
        """
        super().__init__()
        from norm.models.norm import Lambda
        self.lam = lam
        self.data = data
        self.immediately = immediately
        self.description = 'add data'
        self._query_str = None

    def __str__(self):
        if self._query_str is None:
            msg = 'Need to execute first!'
            logger.error(msg)
            raise NormError(msg)
        return self._query_str

    def compile(self, context):
        if not self.immediately:
            if len(self.data) == 1:
                expr = list(self.data.values())[0]
                from norm.executable.expression.arithmetic import ArithmeticExpr
                if isinstance(expr, ArithmeticExpr):
                    if expr.op is not None:
                        return expr
        return self

    def execute(self, context):
        if len(self.data) == 0:
            return DataFrame(data=[self.lam.default])
        else:
            data = OrderedDict((key, value.execute(context)) for key, value in self.data.items())
            data = self.unify(data)
            df = DataFrame(data=data, columns=(data.keys()))
            query_str = hash_df(df)
            self._query_str = query_str
            df = self.lam.fill_primary(df)
            df = self.lam.fill_time(df)
            df = self.lam.fill_oid(df)
            if self.lam.VAR_OID in df.columns:
                df = df.set_index(self.lam.VAR_OID)
            else:
                df.index.rename((self.lam.VAR_OID), inplace=True)
            if self.immediately:
                from norm.models.norm import RevisionType
                df = self.lam.revise(query_str, self.description, df, RevisionType.DISJUNCTION)
                if self.lam.is_functional:
                    return df[self.lam.VAR_OUTPUT]
                else:
                    return df.index
            return df


class ChainedEvaluationExpr(NormExpression):

    def __init__(self, lexpr, rexpr):
        super().__init__()
        self.lexpr = lexpr
        self.rexpr = rexpr

    def compile(self, context):
        if isinstance(self.rexpr, VariableName):
            if isinstance(self.lexpr, VariableName):
                return VariableName(self.lexpr, self.rexpr.name).compile(context)
            if isinstance(self.lexpr, EvaluationExpr):
                if self.rexpr.name in self.lexpr.lam:
                    return ColumnVariable(self.lexpr, self.rexpr.name)
                msg = '{} does not exist in the {}'.format(self.rexpr, self.lexpr)
                logger.error(msg)
                raise NormError(msg)
            else:
                msg = 'Only a variable or an evaluation can have chained operation for now, but got {}'.format(self.lexpr)
                logger.error(msg)
                raise NormError(msg)
        else:
            if isinstance(self.rexpr, EvaluationExpr):
                if self.rexpr.lam is None:
                    if isinstance(self.lexpr, ColumnVariable):
                        return DataFrameColumnFunctionExpr(self.lexpr, self.rexpr).compile(context)
                self.rexpr.args = [ArgumentExpr(expr=(self.lexpr))] + self.rexpr.args
                return self.rexpr.compile(context)
            else:
                msg = 'Only chaining on a variable or an evaluation, but got {}'.format(self.rexpr)
                logger.error(msg)
                raise NormError(msg)


class DataFrameColumnFunctionExpr(EvaluationExpr):

    def __init__(self, column_variable, expr):
        super().__init__([])
        self.column_variable = column_variable
        self.expr = expr

    def compile(self, context):
        return self

    def execute(self, context):
        col = self.column_variable.execute(context)
        args = []
        kwargs = {}
        for arg in self.expr.args:
            if arg.expr is None:
                continue
            if arg.op is None and arg.variable is not None:
                kwargs[arg.variable.name] = arg.expr.execute(context)
            else:
                args.append(arg.expr.execute(context))

        func = self.expr.variable.name
        try:
            df = (getattr(col, func))(*args, **kwargs)
        except:
            print('error on {}'.format(col))
            df = (getattr(col.str, func))(*args, **kwargs)
            print(args, kwargs)
            print(df)

        return df