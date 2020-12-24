# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/grammar/normListener.py
# Compiled at: 2019-05-09 11:45:25
# Size of source mod 2**32: 12469 bytes
from antlr4 import *
if __name__ is not None:
    if '.' in __name__:
        from .normParser import normParser
else:
    from normParser import normParser

class normListener(ParseTreeListener):

    def enterScript(self, ctx: normParser.ScriptContext):
        pass

    def exitScript(self, ctx: normParser.ScriptContext):
        pass

    def enterStatement(self, ctx: normParser.StatementContext):
        pass

    def exitStatement(self, ctx: normParser.StatementContext):
        pass

    def enterComments(self, ctx: normParser.CommentsContext):
        pass

    def exitComments(self, ctx: normParser.CommentsContext):
        pass

    def enterExports(self, ctx: normParser.ExportsContext):
        pass

    def exitExports(self, ctx: normParser.ExportsContext):
        pass

    def enterImports(self, ctx: normParser.ImportsContext):
        pass

    def exitImports(self, ctx: normParser.ImportsContext):
        pass

    def enterCommands(self, ctx: normParser.CommandsContext):
        pass

    def exitCommands(self, ctx: normParser.CommandsContext):
        pass

    def enterContext(self, ctx: normParser.ContextContext):
        pass

    def exitContext(self, ctx: normParser.ContextContext):
        pass

    def enterTypeName(self, ctx: normParser.TypeNameContext):
        pass

    def exitTypeName(self, ctx: normParser.TypeNameContext):
        pass

    def enterVariable(self, ctx: normParser.VariableContext):
        pass

    def exitVariable(self, ctx: normParser.VariableContext):
        pass

    def enterArgumentProperty(self, ctx: normParser.ArgumentPropertyContext):
        pass

    def exitArgumentProperty(self, ctx: normParser.ArgumentPropertyContext):
        pass

    def enterArgumentDeclaration(self, ctx: normParser.ArgumentDeclarationContext):
        pass

    def exitArgumentDeclaration(self, ctx: normParser.ArgumentDeclarationContext):
        pass

    def enterArgumentDeclarations(self, ctx: normParser.ArgumentDeclarationsContext):
        pass

    def exitArgumentDeclarations(self, ctx: normParser.ArgumentDeclarationsContext):
        pass

    def enterRename(self, ctx: normParser.RenameContext):
        pass

    def exitRename(self, ctx: normParser.RenameContext):
        pass

    def enterRenames(self, ctx: normParser.RenamesContext):
        pass

    def exitRenames(self, ctx: normParser.RenamesContext):
        pass

    def enterTypeDeclaration(self, ctx: normParser.TypeDeclarationContext):
        pass

    def exitTypeDeclaration(self, ctx: normParser.TypeDeclarationContext):
        pass

    def enterVersion(self, ctx: normParser.VersionContext):
        pass

    def exitVersion(self, ctx: normParser.VersionContext):
        pass

    def enterQueryProjection(self, ctx: normParser.QueryProjectionContext):
        pass

    def exitQueryProjection(self, ctx: normParser.QueryProjectionContext):
        pass

    def enterConstant(self, ctx: normParser.ConstantContext):
        pass

    def exitConstant(self, ctx: normParser.ConstantContext):
        pass

    def enterCode(self, ctx: normParser.CodeContext):
        pass

    def exitCode(self, ctx: normParser.CodeContext):
        pass

    def enterCodeExpression(self, ctx: normParser.CodeExpressionContext):
        pass

    def exitCodeExpression(self, ctx: normParser.CodeExpressionContext):
        pass

    def enterArgumentExpression(self, ctx: normParser.ArgumentExpressionContext):
        pass

    def exitArgumentExpression(self, ctx: normParser.ArgumentExpressionContext):
        pass

    def enterArgumentExpressions(self, ctx: normParser.ArgumentExpressionsContext):
        pass

    def exitArgumentExpressions(self, ctx: normParser.ArgumentExpressionsContext):
        pass

    def enterEvaluationExpression(self, ctx: normParser.EvaluationExpressionContext):
        pass

    def exitEvaluationExpression(self, ctx: normParser.EvaluationExpressionContext):
        pass

    def enterSlicedExpression(self, ctx: normParser.SlicedExpressionContext):
        pass

    def exitSlicedExpression(self, ctx: normParser.SlicedExpressionContext):
        pass

    def enterArithmeticExpression(self, ctx: normParser.ArithmeticExpressionContext):
        pass

    def exitArithmeticExpression(self, ctx: normParser.ArithmeticExpressionContext):
        pass

    def enterConditionExpression(self, ctx: normParser.ConditionExpressionContext):
        pass

    def exitConditionExpression(self, ctx: normParser.ConditionExpressionContext):
        pass

    def enterOneLineExpression(self, ctx: normParser.OneLineExpressionContext):
        pass

    def exitOneLineExpression(self, ctx: normParser.OneLineExpressionContext):
        pass

    def enterMultiLineExpression(self, ctx: normParser.MultiLineExpressionContext):
        pass

    def exitMultiLineExpression(self, ctx: normParser.MultiLineExpressionContext):
        pass

    def enterNone(self, ctx: normParser.NoneContext):
        pass

    def exitNone(self, ctx: normParser.NoneContext):
        pass

    def enterBool_c(self, ctx: normParser.Bool_cContext):
        pass

    def exitBool_c(self, ctx: normParser.Bool_cContext):
        pass

    def enterInteger_c(self, ctx: normParser.Integer_cContext):
        pass

    def exitInteger_c(self, ctx: normParser.Integer_cContext):
        pass

    def enterFloat_c(self, ctx: normParser.Float_cContext):
        pass

    def exitFloat_c(self, ctx: normParser.Float_cContext):
        pass

    def enterString_c(self, ctx: normParser.String_cContext):
        pass

    def exitString_c(self, ctx: normParser.String_cContext):
        pass

    def enterPattern(self, ctx: normParser.PatternContext):
        pass

    def exitPattern(self, ctx: normParser.PatternContext):
        pass

    def enterUuid(self, ctx: normParser.UuidContext):
        pass

    def exitUuid(self, ctx: normParser.UuidContext):
        pass

    def enterUrl(self, ctx: normParser.UrlContext):
        pass

    def exitUrl(self, ctx: normParser.UrlContext):
        pass

    def enterDatetime(self, ctx: normParser.DatetimeContext):
        pass

    def exitDatetime(self, ctx: normParser.DatetimeContext):
        pass

    def enterLogicalOperator(self, ctx: normParser.LogicalOperatorContext):
        pass

    def exitLogicalOperator(self, ctx: normParser.LogicalOperatorContext):
        pass

    def enterSpacedLogicalOperator(self, ctx: normParser.SpacedLogicalOperatorContext):
        pass

    def exitSpacedLogicalOperator(self, ctx: normParser.SpacedLogicalOperatorContext):
        pass

    def enterNewlineLogicalOperator(self, ctx: normParser.NewlineLogicalOperatorContext):
        pass

    def exitNewlineLogicalOperator(self, ctx: normParser.NewlineLogicalOperatorContext):
        pass

    def enterConditionOperator(self, ctx: normParser.ConditionOperatorContext):
        pass

    def exitConditionOperator(self, ctx: normParser.ConditionOperatorContext):
        pass

    def enterSpacedConditionOperator(self, ctx: normParser.SpacedConditionOperatorContext):
        pass

    def exitSpacedConditionOperator(self, ctx: normParser.SpacedConditionOperatorContext):
        pass