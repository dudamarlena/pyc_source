# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/generated/PyNestMLParserVisitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 5755 bytes
from antlr4 import *

class PyNestMLParserVisitor(ParseTreeVisitor):

    def visitDataType(self, ctx):
        return self.visitChildren(ctx)

    def visitUnitType(self, ctx):
        return self.visitChildren(ctx)

    def visitUnitTypeExponent(self, ctx):
        return self.visitChildren(ctx)

    def visitExpression(self, ctx):
        return self.visitChildren(ctx)

    def visitSimpleExpression(self, ctx):
        return self.visitChildren(ctx)

    def visitUnaryOperator(self, ctx):
        return self.visitChildren(ctx)

    def visitBitOperator(self, ctx):
        return self.visitChildren(ctx)

    def visitComparisonOperator(self, ctx):
        return self.visitChildren(ctx)

    def visitLogicalOperator(self, ctx):
        return self.visitChildren(ctx)

    def visitVariable(self, ctx):
        return self.visitChildren(ctx)

    def visitFunctionCall(self, ctx):
        return self.visitChildren(ctx)

    def visitOdeFunction(self, ctx):
        return self.visitChildren(ctx)

    def visitOdeEquation(self, ctx):
        return self.visitChildren(ctx)

    def visitOdeShape(self, ctx):
        return self.visitChildren(ctx)

    def visitBlock(self, ctx):
        return self.visitChildren(ctx)

    def visitStmt(self, ctx):
        return self.visitChildren(ctx)

    def visitCompoundStmt(self, ctx):
        return self.visitChildren(ctx)

    def visitSmallStmt(self, ctx):
        return self.visitChildren(ctx)

    def visitAssignment(self, ctx):
        return self.visitChildren(ctx)

    def visitDeclaration(self, ctx):
        return self.visitChildren(ctx)

    def visitReturnStmt(self, ctx):
        return self.visitChildren(ctx)

    def visitIfStmt(self, ctx):
        return self.visitChildren(ctx)

    def visitIfClause(self, ctx):
        return self.visitChildren(ctx)

    def visitElifClause(self, ctx):
        return self.visitChildren(ctx)

    def visitElseClause(self, ctx):
        return self.visitChildren(ctx)

    def visitForStmt(self, ctx):
        return self.visitChildren(ctx)

    def visitWhileStmt(self, ctx):
        return self.visitChildren(ctx)

    def visitNestMLCompilationUnit(self, ctx):
        return self.visitChildren(ctx)

    def visitNeuron(self, ctx):
        return self.visitChildren(ctx)

    def visitBody(self, ctx):
        return self.visitChildren(ctx)

    def visitBlockWithVariables(self, ctx):
        return self.visitChildren(ctx)

    def visitUpdateBlock(self, ctx):
        return self.visitChildren(ctx)

    def visitEquationsBlock(self, ctx):
        return self.visitChildren(ctx)

    def visitInputBlock(self, ctx):
        return self.visitChildren(ctx)

    def visitInputPort(self, ctx):
        return self.visitChildren(ctx)

    def visitInputQualifier(self, ctx):
        return self.visitChildren(ctx)

    def visitOutputBlock(self, ctx):
        return self.visitChildren(ctx)

    def visitFunction(self, ctx):
        return self.visitChildren(ctx)

    def visitParameter(self, ctx):
        return self.visitChildren(ctx)