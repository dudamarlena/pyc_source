# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/engine.py
# Compiled at: 2019-05-21 17:50:20
# Size of source mod 2**32: 20895 bytes
import re, uuid
from antlr4 import *
import antlr4.error.ErrorListener as ErrorListener
from dateutil import parser as dateparser
from textwrap import dedent
from norm import config
from norm.executable import NormExecutable, Projection
from norm.executable.command import Command
from norm.executable.constant import Constant
from norm.executable.schema.declaration import *
from norm.executable.expression.arithmetic import *
from norm.executable.expression.evaluation import *
from norm.executable.expression.query import *
from norm.executable.expression.slice import *
from norm.executable.schema.implementation import *
from norm.executable.schema.type import *
from norm.executable.schema.namespace import *
from norm.grammar.literals import AOP, COP, LOP, ImplType, ConstantType, MOP
import norm.grammar.normLexer as normLexer
import norm.grammar.normListener as normListener
import norm.grammar.normParser as normParser

class ParseError(ValueError):
    pass


class NormErrorListener(ErrorListener):

    def __init__(self):
        super(NormErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        err_msg = 'line ' + str(line) + ':' + str(column) + ' ' + msg
        raise ValueError(err_msg)


walker = ParseTreeWalker()

class NormCompiler(normListener):
    TMP_VARIABLE_STUB = 'tmp_'

    def __init__(self, context_id, user, session=None):
        self.context_id = context_id
        self.scopes = []
        self.stack = []
        self.session = session
        self.user = user
        self.context_namespace = None
        self.user_namespace = None
        self.search_namespaces = None
        self.set_namespaces()

    def set_namespaces(self):
        if self.context_id:
            self.context_namespace = '{}.{}'.format(config.CONTEXT_NAMESPACE_STUB, self.context_id)
        if self.user:
            self.user_namespace = '{}.{}'.format(config.USER_NAMESPACE_STUB, self.user.username)
        from norm.models import NativeLambda, CoreLambda
        self.search_namespaces = [
         NativeLambda.NAMESPACE, CoreLambda.NAMESPACE, self.context_namespace,
         self.user_namespace]

    def set_temp_scope(self):
        """
        For a unnamed query, we assign a temporary type for the scope.
        For a named query, i.e., type implementation, the scope is the type.
        """
        self.scopes.append((Lambda(self.context_namespace, self.TMP_VARIABLE_STUB + str(uuid.uuid4())), 'temp'))

    def get_scope(self, name):
        for scope, scope_lex in reversed(self.scopes):
            if name in scope:
                return scope

    @property
    def scope(self):
        if len(self.scopes) > 0:
            return self.scopes[(-1)][0]

    @property
    def scope_lex(self):
        if len(self.scopes) > 0:
            return self.scopes[(-1)][1]

    def _push(self, exe):
        self.stack.append(exe)

    def _pop(self):
        """
        :rtype: NormExecutable
        """
        return self.stack.pop()

    def _peek(self):
        """
        :rtype: NormExecutable
        """
        if len(self.stack) > 0:
            return self.stack[(-1)]

    def optimize(self, exe):
        """
        Optimize the AST to have a more efficient execution plan
        # TODO: optimization strategies
        * Filtering conditions can be combined and executed in batch instead of sequential
        * Arithmetic equations can be combined and passed to DF in batch instead of sequential
        :param exe: the executable to be optimized
        :type exe: NormExecutable
        :return: the optimized executable
        :rtype: NormExecutable
        """
        return exe

    def compile(self, script):
        return script is None or isinstance(script, str) or 
        script = script.strip(' \r\n\t')
        if script == '':
            return
        lexer = normLexer(InputStream(script))
        stream = CommonTokenStream(lexer)
        parser = normParser(stream)
        parser.addErrorListener(NormErrorListener())
        tree = parser.script()
        walker.walk(self, tree)

    def execute(self, script):
        self.stack = []
        self.scopes = []
        self.compile(dedent(script))
        results = None
        while len(self.stack) > 0:
            exe = self._pop()
            if isinstance(exe, NormExecutable):
                results = exe.execute(self)
            else:
                results = exe
            if isinstance(results, Index) and isinstance(exe, NormExpression) and exe.lam is not None:
                results = exe.lam.data.loc[results]

        if isinstance(results, DataFrame):
            fix_dot_columns = OrderedDict()
            for col in results.columns:
                if col.find(NormExecutable.VARIABLE_SEPARATOR) >= 0:
                    fix_dot_columns[col] = col.replace(NormExecutable.VARIABLE_SEPARATOR, '.')

            results = results.rename(columns=fix_dot_columns)
        return results

    def exitStatement--- This code section failed: ---

 L. 156         0  LOAD_FAST                'ctx'
                2  LOAD_METHOD              typeDeclaration
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_FALSE   150  'to 150'

 L. 157         8  LOAD_FAST                'ctx'
               10  LOAD_METHOD              IMPL
               12  CALL_METHOD_0         0  ''
               14  POP_JUMP_IF_FALSE   102  'to 102'

 L. 158        16  LOAD_FAST                'self'
               18  LOAD_METHOD              _pop
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'query'

 L. 159        24  LOAD_FAST                'self'
               26  LOAD_METHOD              _pop
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'type_declaration'

 L. 160        32  LOAD_FAST                'ctx'
               34  LOAD_METHOD              comments
               36  CALL_METHOD_0         0  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'
               40  LOAD_FAST                'self'
               42  LOAD_METHOD              _pop
               44  CALL_METHOD_0         0  ''
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            38  '38'
               48  LOAD_STR                 ''
             50_0  COME_FROM            46  '46'
               50  STORE_FAST               'description'

 L. 161        52  LOAD_FAST                'description'
               54  LOAD_FAST                'type_declaration'
               56  STORE_ATTR               description

 L. 162        58  LOAD_GLOBAL              ImplType
               60  LOAD_FAST                'ctx'
               62  LOAD_METHOD              IMPL
               64  CALL_METHOD_0         0  ''
               66  LOAD_METHOD              getText
               68  CALL_METHOD_0         0  ''
               70  CALL_FUNCTION_1       1  ''
               72  STORE_FAST               'op'

 L. 163        74  LOAD_FAST                'self'
               76  LOAD_METHOD              _push
               78  LOAD_GLOBAL              TypeImplementation
               80  LOAD_FAST                'type_declaration'
               82  LOAD_FAST                'op'
               84  LOAD_FAST                'query'
               86  LOAD_FAST                'description'
               88  CALL_FUNCTION_4       4  ''
               90  LOAD_METHOD              compile
               92  LOAD_FAST                'self'
               94  CALL_METHOD_1         1  ''
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  JUMP_FORWARD        148  'to 148'
            102_0  COME_FROM            14  '14'

 L. 164       102  LOAD_FAST                'ctx'
              104  LOAD_METHOD              comments
              106  CALL_METHOD_0         0  ''
              108  POP_JUMP_IF_FALSE   148  'to 148'

 L. 166       110  LOAD_FAST                'self'
              112  LOAD_METHOD              _pop
              114  CALL_METHOD_0         0  ''
              116  STORE_FAST               'type_declaration'

 L. 167       118  LOAD_FAST                'self'
              120  LOAD_METHOD              _pop
              122  CALL_METHOD_0         0  ''
              124  STORE_FAST               'description'

 L. 168       126  LOAD_FAST                'description'
              128  LOAD_FAST                'type_declaration'
              130  STORE_ATTR               description

 L. 169       132  LOAD_FAST                'self'
              134  LOAD_METHOD              _push
              136  LOAD_FAST                'type_declaration'
              138  LOAD_METHOD              compile
              140  LOAD_FAST                'self'
              142  CALL_METHOD_1         1  ''
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
            148_0  COME_FROM           108  '108'
            148_1  COME_FROM           100  '100'
              148  JUMP_FORWARD        396  'to 396'
            150_0  COME_FROM             6  '6'

 L. 170       150  LOAD_FAST                'ctx'
              152  LOAD_METHOD              argumentDeclarations
              154  CALL_METHOD_0         0  ''
              156  POP_JUMP_IF_FALSE   198  'to 198'

 L. 171       158  LOAD_FAST                'self'
              160  LOAD_METHOD              _pop
              162  CALL_METHOD_0         0  ''
              164  STORE_FAST               'args'

 L. 172       166  LOAD_FAST                'self'
              168  LOAD_METHOD              _pop
              170  CALL_METHOD_0         0  ''
              172  STORE_FAST               'type_'

 L. 173       174  LOAD_FAST                'self'
              176  LOAD_METHOD              _push
              178  LOAD_GLOBAL              AdditionalTypeDeclaration
              180  LOAD_FAST                'type_'
              182  LOAD_FAST                'args'
              184  CALL_FUNCTION_2       2  ''
              186  LOAD_METHOD              compile
              188  LOAD_FAST                'self'
              190  CALL_METHOD_1         1  ''
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
              196  JUMP_FORWARD        396  'to 396'
            198_0  COME_FROM           156  '156'

 L. 174       198  LOAD_FAST                'ctx'
              200  LOAD_METHOD              renames
              202  CALL_METHOD_0         0  ''
              204  POP_JUMP_IF_FALSE   246  'to 246'

 L. 175       206  LOAD_FAST                'self'
              208  LOAD_METHOD              _pop
              210  CALL_METHOD_0         0  ''
              212  STORE_FAST               'renames'

 L. 176       214  LOAD_FAST                'self'
              216  LOAD_METHOD              _pop
              218  CALL_METHOD_0         0  ''
              220  STORE_FAST               'type_'

 L. 177       222  LOAD_FAST                'self'
              224  LOAD_METHOD              _push
              226  LOAD_GLOBAL              RenameTypeDeclaration
              228  LOAD_FAST                'type_'
              230  LOAD_FAST                'renames'
              232  CALL_FUNCTION_2       2  ''
              234  LOAD_METHOD              compile
              236  LOAD_FAST                'self'
              238  CALL_METHOD_1         1  ''
              240  CALL_METHOD_1         1  ''
              242  POP_TOP          
              244  JUMP_FORWARD        396  'to 396'
            246_0  COME_FROM           204  '204'

 L. 178       246  LOAD_FAST                'ctx'
              248  LOAD_METHOD              codeExpression
              250  CALL_METHOD_0         0  ''
          252_254  POP_JUMP_IF_FALSE   320  'to 320'

 L. 179       256  LOAD_FAST                'self'
              258  LOAD_METHOD              _pop
              260  CALL_METHOD_0         0  ''
              262  STORE_FAST               'code'

 L. 180       264  LOAD_FAST                'self'
              266  LOAD_METHOD              _pop
              268  CALL_METHOD_0         0  ''
              270  STORE_FAST               'type_'

 L. 181       272  LOAD_FAST                'ctx'
              274  LOAD_METHOD              comments
              276  CALL_METHOD_0         0  ''
          278_280  POP_JUMP_IF_FALSE   290  'to 290'
              282  LOAD_FAST                'self'
              284  LOAD_METHOD              _pop
              286  CALL_METHOD_0         0  ''
              288  JUMP_FORWARD        292  'to 292'
            290_0  COME_FROM           278  '278'
              290  LOAD_STR                 ''
            292_0  COME_FROM           288  '288'
              292  STORE_FAST               'description'

 L. 182       294  LOAD_FAST                'self'
              296  LOAD_METHOD              _push
              298  LOAD_GLOBAL              CodeTypeDeclaration
              300  LOAD_FAST                'type_'
              302  LOAD_FAST                'code'
              304  LOAD_FAST                'description'
              306  CALL_FUNCTION_3       3  ''
              308  LOAD_METHOD              compile
              310  LOAD_FAST                'self'
              312  CALL_METHOD_1         1  ''
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          
              318  JUMP_FORWARD        396  'to 396'
            320_0  COME_FROM           252  '252'

 L. 183       320  LOAD_FAST                'ctx'
              322  LOAD_METHOD              imports
              324  CALL_METHOD_0         0  ''
          326_328  POP_JUMP_IF_TRUE    360  'to 360'
              330  LOAD_FAST                'ctx'
              332  LOAD_METHOD              exports
              334  CALL_METHOD_0         0  ''
          336_338  POP_JUMP_IF_TRUE    360  'to 360'
              340  LOAD_FAST                'ctx'
              342  LOAD_METHOD              commands
              344  CALL_METHOD_0         0  ''
          346_348  POP_JUMP_IF_TRUE    360  'to 360'
              350  LOAD_FAST                'ctx'
              352  LOAD_METHOD              multiLineExpression
              354  CALL_METHOD_0         0  ''
          356_358  POP_JUMP_IF_FALSE   396  'to 396'
            360_0  COME_FROM           346  '346'
            360_1  COME_FROM           336  '336'
            360_2  COME_FROM           326  '326'

 L. 184       360  LOAD_FAST                'ctx'
              362  LOAD_METHOD              comments
              364  CALL_METHOD_0         0  ''
          366_368  POP_JUMP_IF_FALSE   396  'to 396'

 L. 185       370  LOAD_FAST                'self'
              372  LOAD_METHOD              _pop
              374  CALL_METHOD_0         0  ''
              376  STORE_FAST               'expr'

 L. 187       378  LOAD_FAST                'self'
              380  LOAD_METHOD              _pop
              382  CALL_METHOD_0         0  ''
              384  POP_TOP          

 L. 188       386  LOAD_FAST                'self'
              388  LOAD_METHOD              _push
              390  LOAD_FAST                'expr'
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          
            396_0  COME_FROM           366  '366'
            396_1  COME_FROM           356  '356'
            396_2  COME_FROM           318  '318'
            396_3  COME_FROM           244  '244'
            396_4  COME_FROM           196  '196'
            396_5  COME_FROM           148  '148'

Parse error at or near `COME_FROM' instruction at offset 396_4

    def exitNone(self, ctx: normParser.NoneContext):
        self._push(Constant(ConstantType.NULL, None))

    def exitBool_c(self, ctx: normParser.Bool_cContext):
        self._push(Constant(ConstantType.BOOL, ctx.getText().lower() == 'true'))

    def exitInteger_c(self, ctx: normParser.Integer_cContext):
        self._push(Constant(ConstantType.INT, int(ctx.getText())))

    def exitFloat_c(self, ctx: normParser.Float_cContext):
        self._push(Constant(ConstantType.FLT, float(ctx.getText())))

    def exitString_c(self, ctx: normParser.String_cContext):
        self._push(Constant(ConstantType.STR, str(ctx.getText()[1:-1])))

    def exitPattern(self, ctx: normParser.PatternContext):
        try:
            self._push(Constant(ConstantType.PTN, re.compile(str(ctx.getText()[2:-1]))))
        except:
            raise ParseError('Pattern constant {} is in wrong format, should be Python regex pattern'.format(ctx.getText()))

    def exitUuid(self, ctx: normParser.UuidContext):
        self._push(Constant(ConstantType.UID, str(ctx.getText()[2:-1])))

    def exitUrl(self, ctx: normParser.UrlContext):
        self._push(Constant(ConstantType.URL, str(ctx.getText()[2:-1])))

    def exitDatetime(self, ctx: normParser.DatetimeContext):
        self._push(Constant(ConstantType.DTM, dateparser.parse((ctx.getText()[2:-1]), fuzzy=True)))

    def exitConstant(self, ctx: normParser.ConstantContext):
        if ctx.LSBR():
            constants = list(reversed([self._pop() for ch in ctx.children if isinstance(ch, normParser.ConstantContext)]))
            types = set((constant.type_ for constant in constants))
            if len(types) > 1:
                type_ = ConstantType.ANY
            else:
                type_ = types.pop()
            self._push(ListConstant(type_, [constant.value for constant in constants]))

    def exitQueryProjection(self, ctx: normParser.QueryProjectionContext):
        variables = list(reversed([self._pop() for ch in ctx.children if isinstance(ch, normParser.VariableContext)]))
        to_evaluate = True if ctx.LCBR() else False
        self._push(Projection(variables, to_evaluate))

    def exitComments(self, ctx: normParser.CommentsContext):
        spaces = ' \r\n\t'
        cmt = ctx.getText()
        if ctx.MULTILINE():
            cmt = cmt.strip(spaces)[2:-2].strip(spaces)
        elif ctx.SINGLELINE():
            cmt = '\n'.join((cmt_line.strip(spaces)[2:].strip(spaces) for cmt_line in cmt.split('\n')))
        self._push(cmt)

    def exitImports(self, ctx: normParser.ImportsContext):
        type_ = self._pop() if ctx.typeName() else None
        namespace = [str(v) for v in ctx.VARNAME()]
        variable = namespace.pop() if ctx.AS() else None
        self._push(Import('.'.join(namespace), type_, variable).compile(self))

    def exitExports(self, ctx: normParser.ExportsContext):
        type_ = self._pop()
        namespace = [str(v) for v in ctx.VARNAME()]
        variable = namespace.pop() if ctx.AS() else None
        self._push(Export('.'.join(namespace), type_, variable).compile(self))

    def exitCommands(self, ctx: normParser.CommandsContext):
        type_ = self._pop()
        op = MOP(ctx.SPACED_COMMAND().getText().strip().lower())
        self._push(Command(op, type_).compile(self))

    def exitArgumentDeclaration(self, ctx: normParser.ArgumentDeclarationContext):
        variable_property = ctx.argumentProperty().getText() if ctx.argumentProperty() else None
        optional = variable_property is not None and variable_property.lower().find('optional') > 0
        type_name = self._pop()
        variable_name = self._pop()
        self._push(ArgumentDeclaration(variable_name, type_name, optional))

    def enterArgumentDeclarations(self, ctx: normParser.ArgumentDeclarationsContext):
        type_name = self._peek()
        if type_name is not None:
            if isinstance(type_name, TypeName):
                if type_name.lam is not None:
                    self.scopes.append((type_name.lam, 'argument_declarations'))

    def exitArgumentDeclarations(self, ctx: normParser.ArgumentDeclarationsContext):
        args = list(reversed([self._pop() for ch in ctx.children if isinstance(ch, normParser.ArgumentDeclarationContext)]))
        self._push(args)
        if self.scope_lex == 'argument_declarations':
            self.scopes.pop()

    def exitRename(self, ctx: normParser.RenameContext):
        new_name = self._pop()
        original_name = self._pop()
        self._push(RenameArgument(original_name.name, new_name.name))

    def exitRenames(self, ctx: normParser.RenamesContext):
        args = list(reversed([self._pop() for ch in ctx.children if isinstance(ch, normParser.RenameContext)]))
        self._push(args)
        if self.scope_lex == 'renames':
            self.scopes.pop()

    def enterRenames(self, ctx: normParser.RenamesContext):
        type_name = self._peek()
        if type_name is not None:
            if isinstance(type_name, TypeName):
                if type_name.lam is not None:
                    self.scopes.append((type_name.lam, 'renames'))

    def exitTypeDeclaration(self, ctx: normParser.TypeDeclarationContext):
        output_type_name = self._pop() if ctx.typeName(1) else None
        args = self._pop() if ctx.argumentDeclarations() else None
        type_name = self._pop()
        self._push(TypeDeclaration(type_name, args, output_type_name).compile(self))

    def exitTypeName(self, ctx: normParser.TypeNameContext):
        typename = ctx.VARNAME()
        if typename:
            version = ctx.version().getText() if ctx.version() else None
            self._push(TypeName(str(typename), version).compile(self))
        elif ctx.LSBR():
            intern = self._pop()
            self._push(ListType(intern).compile(self))
        else:
            raise ParseError('Not a valid type name definition')

    def exitVariable(self, ctx: normParser.VariableContext):
        name = ''
        if ctx.VARNAME():
            name = ctx.VARNAME().getText()
        elif ctx.COMMAND():
            name = ctx.COMMAND().getText()
        elif ctx.ARGOPT():
            name = ctx.ARGOPT().getText()
        scope = self._pop() if ctx.variable() else None
        self._push(VariableName(scope, name).compile(self))

    def exitArgumentExpression(self, ctx: normParser.ArgumentExpressionContext):
        if isinstance(self._peek(), ArgumentExpr):
            return
        projection = self._pop() if ctx.queryProjection() else None
        expr = self._pop() if ctx.arithmeticExpression() else None
        op = COP(ctx.spacedConditionOperator().conditionOperator().getText().lower()) if ctx.spacedConditionOperator() else None
        variable = self._pop() if ctx.variable() else None
        if variable is None and projection is None and op is None and expr is not None and isinstance(expr, EvaluationExpr) and isinstance(expr.variable, ColumnVariable) and len(expr.args) == 0 and expr.projection is not None:
            self._push(ArgumentExprexpr.variableopNoneexpr.projection.compile(self))
        else:
            self._push(ArgumentExprvariableopexprprojection.compile(self))

    def enterArgumentExpressions(self, ctx: normParser.ArgumentExpressionsContext):
        expr = self._peek()
        if expr is not None:
            if isinstance(expr, (VariableName, EvaluationExpr)):
                if expr.lam is not None:
                    self.scopes.append((expr.lam, 'argument_expressions'))

    def exitArgumentExpressions(self, ctx: normParser.ArgumentExpressionsContext):
        args = list(reversed([self._pop() for ch in ctx.children if isinstance(ch, normParser.ArgumentExpressionContext)]))
        self._push(args)
        if self.scope_lex == 'argument_expressions':
            self.scopes.pop()

    def enterMultiLineExpression(self, ctx: normParser.MultiLineExpressionContext):
        type_declaration = self._peek()
        if type_declaration is not None:
            if isinstance(type_declaration, TypeDeclaration):
                if type_declaration.lam is not None:
                    self.scopes.append((type_declaration.lam, 'multiline'))

    def exitContext(self, ctx: normParser.ContextContext):
        type_name = self._pop()
        self.scopes.append((type_name.lam, 'multiline'))

    def exitMultiLineExpression(self, ctx: normParser.MultiLineExpressionContext):
        if ctx.newlineLogicalOperator():
            expr2 = self._pop()
            expr1 = self._pop()
            op = LOP.parse(ctx.newlineLogicalOperator().logicalOperator().getText())
            self._push(QueryExpr(op, expr1, expr2).compile(self))
        if self.scope_lex == 'multiline':
            self.scopes.pop()

    def enterSpacedLogicalOperator(self, ctx: normParser.SpacedLogicalOperatorContext):
        expr = self._peek()
        self.scopes.append((expr.lam, 'lop'))

    def exitOneLineExpression(self, ctx: normParser.OneLineExpressionContext):
        if ctx.queryProjection():
            projection = self._pop()
            expr = self._peek()
            expr.projection = projection
            expr.compile(self)
        elif ctx.NOT():
            expr = self._pop()
            self._push(NegatedQueryExpr(expr).compile(self))
        elif ctx.spacedLogicalOperator():
            expr2 = self._pop()
            expr1 = self._pop()
            op = LOP.parse(ctx.spacedLogicalOperator().logicalOperator().getText())
            self._push(QueryExpr(op, expr1, expr2).compile(self))
            if self.scope_lex == 'lop':
                self.scopes.pop()

    def exitConditionExpression(self, ctx: normParser.ConditionExpressionContext):
        if ctx.spacedConditionOperator():
            qexpr = self._pop()
            aexpr = self._pop()
            cop = COP(ctx.spacedConditionOperator().conditionOperator().getText().lower())
            self._push(ConditionExpr(cop, aexpr, qexpr).compile(self))

    def exitArithmeticExpression(self, ctx: normParser.ArithmeticExpressionContext):
        if ctx.slicedExpression():
            return
        else:
            op = None
            if ctx.MOD():
                op = AOP.MOD
            elif ctx.EXP():
                op = AOP.EXP
            elif ctx.TIMES():
                op = AOP.MUL
            elif ctx.DIVIDE():
                op = AOP.DIV
            elif ctx.PLUS():
                op = AOP.ADD
            elif ctx.MINUS():
                op = AOP.SUB
        if op is not None:
            expr2 = self._pop()
            if isinstance(expr2, ArgumentExpr):
                expr2 = expr2.variable
            expr1 = self._pop() if ctx.arithmeticExpression(1) else None
            if isinstance(expr1, AddDataEvaluationExpr):
                expr1 = list(expr1.data.values())[0]
                assert isinstance(expr1, ArithmeticExpr)
            self._push(ArithmeticExpr(op, expr1, expr2).compile(self))

    def exitSlicedExpression(self, ctx: normParser.SlicedExpressionContext):
        if ctx.LSBR():
            if ctx.evaluationExpression(1):
                expr_range = self._pop()
                expr = self._pop()
                self._push(EvaluatedSliceExpr(expr, expr_range).compile(self))
            else:
                end = self._pop() if ctx.integer_c(1) else None
                start = self._pop() if ctx.integer_c(0) else None
                expr = self._pop()
                start_value = start.value
                if end is not None:
                    end_value = end.value
                elif ctx.COLON():
                    colon_before_number = True
                    for ch in ctx.children:
                        if ch == ctx.COLON():
                            break

                    if colon_before_number:
                        end_value = start_value
                        start_value = 0
                    else:
                        end_value = None
                else:
                    end_value = start_value + 1
                self._push(SliceExpr(expr, start_value, end_value).compile(self))

    def exitEvaluationExpression(self, ctx: normParser.EvaluationExpressionContext):
        if ctx.DOT():
            rexpr = self._pop()
            lexpr = self._pop()
            self._push(ChainedEvaluationExpr(lexpr, rexpr).compile(self))
        elif ctx.argumentExpressions() or ctx.queryProjection():
            projection = self._pop() if ctx.queryProjection() else None
            args = self._pop() if ctx.argumentExpressions() else []
            variable = self._pop() if ctx.variable() else None
            self._push(EvaluationExpr(args, variable, projection).compile(self))

    def exitCodeExpression(self, ctx: normParser.CodeExpressionContext):
        self._push(ctx.code().getText())