# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/pod/actions.py
# Compiled at: 2009-09-30 05:37:25
from appy.pod import PodError
from appy.pod.elements import *
EVAL_ERROR = 'Error while evaluating expression "%s".'
FROM_EVAL_ERROR = 'Error while evaluating the expression "%s" defined in the "from" part of a statement.'
WRONG_SEQ_TYPE = 'Expression "%s" is not iterable.'
TABLE_NOT_ONE_CELL = "The table you wanted to populate with '%s' can't be dumped with the '-' option because it has more than one cell in it."

class BufferAction:
    """Abstract class representing a action (=statement) that must be performed
       on the content of a buffer (if, for...)."""
    __module__ = __name__

    def __init__(self, name, buffer, expr, elem, minus, source, fromExpr):
        self.name = name
        self.buffer = buffer
        self.expr = expr
        self.elem = elem
        self.minus = minus
        self.result = self.buffer.getFileBuffer()
        self.source = source
        self.fromExpr = fromExpr
        self.exprResult = None
        self.fromExprResult = None
        return

    def writeError(self, errorMessage, dumpTb=True):
        self.buffer.__init__(self.buffer.env, self.buffer.parent)
        PodError.dump(self.buffer, errorMessage, withinElement=self.elem, dumpTb=dumpTb)
        self.buffer.evaluate()

    def execute(self):
        if self.minus and isinstance(self.elem, Table) and not self.elem.tableInfo.isOneCell():
            self.writeError(TABLE_NOT_ONE_CELL % self.expr)
        else:
            errorOccurred = False
            if self.expr:
                try:
                    self.exprResult = eval(self.expr, self.buffer.env.context)
                except:
                    self.exprResult = None
                    self.writeError(EVAL_ERROR % self.expr)
                    errorOccurred = True

            if not errorOccurred:
                self.do()
        return

    def evaluateBuffer(self):
        if self.source == 'buffer':
            self.buffer.evaluate(removeMainElems=self.minus)
        else:
            self.fromExprResult = None
            errorOccurred = False
            try:
                self.fromExprResult = eval(self.fromExpr, self.buffer.env.context)
            except PodError, pe:
                self.writeError(FROM_EVAL_ERROR % self.fromExpr + ' ' + str(pe), dumpTb=False)
                errorOccurred = True
            except:
                self.writeError(FROM_EVAL_ERROR % self.fromExpr)
                errorOccurred = True

            if not errorOccurred:
                self.result.write(self.fromExprResult)
        return


class IfAction(BufferAction):
    """Action that determines if we must include the content of the buffer in
    the result or not."""
    __module__ = __name__

    def do(self):
        if self.exprResult:
            self.evaluateBuffer()
        elif self.buffer.isMainElement(Cell.OD):
            self.result.dumpElement(Cell.OD.elem)


class ElseAction(IfAction):
    """Action that is linked to a previous "if" action. In fact, an "else"
       action works exactly like an "if" action, excepted that instead of
       defining a conditional expression, it is based on the negation of the
       conditional expression of the last defined "if" action."""
    __module__ = __name__

    def __init__(self, name, buffer, expr, elem, minus, source, fromExpr, ifAction):
        IfAction.__init__(self, name, buffer, None, elem, minus, source, fromExpr)
        self.ifAction = ifAction
        return

    def do(self):
        self.exprResult = not self.ifAction.exprResult
        IfAction.do(self)


class ForAction(BufferAction):
    """Actions that will include the content of the buffer as many times as
    specified by the action parameters."""
    __module__ = __name__

    def __init__(self, name, buffer, expr, elem, minus, iter, source, fromExpr):
        BufferAction.__init__(self, name, buffer, expr, elem, minus, source, fromExpr)
        self.iter = iter

    def do(self):
        context = self.buffer.env.context
        try:
            iter(self.exprResult)
        except TypeError:
            self.writeError(WRONG_SEQ_TYPE % self.expr)
            return

        hasHiddenVariable = False
        if context.has_key(self.iter):
            hiddenVariable = context[self.iter]
            hasHiddenVariable = True
        isCell = False
        if isinstance(self.elem, Cell):
            isCell = True
            nbOfColumns = self.elem.tableInfo.nbOfColumns
            initialColIndex = self.elem.tableInfo.curColIndex
            currentColIndex = initialColIndex
            rowAttributes = self.elem.tableInfo.curRowAttrs
            if not self.exprResult:
                self.result.dumpElement(Cell.OD.elem)
        for item in self.exprResult:
            context[self.iter] = item
            if isCell and currentColIndex == nbOfColumns:
                self.result.dumpEndElement(Row.OD.elem)
                self.result.dumpStartElement(Row.OD.elem, rowAttributes)
                currentColIndex = 0
            self.evaluateBuffer()
            if isCell:
                currentColIndex += 1

        if isCell and self.exprResult:
            wrongNbOfCells = currentColIndex - 1 - initialColIndex
            if wrongNbOfCells < 0:
                for i in range(abs(wrongNbOfCells)):
                    context[self.iter] = ''
                    self.buffer.evaluate(subElements=False)

            elif wrongNbOfCells > 0:
                nbOfMissingCells = 0
                if currentColIndex < nbOfColumns:
                    nbOfMissingCells = nbOfColumns - currentColIndex
                    context[self.iter] = ''
                    for i in range(nbOfMissingCells):
                        self.buffer.evaluate(subElements=False)

                self.result.dumpEndElement(Row.OD.elem)
                self.result.dumpStartElement(Row.OD.elem, rowAttributes)
                nbOfRemainingCells = wrongNbOfCells + nbOfMissingCells
                nbOfMissingCellsLastLine = nbOfColumns - nbOfRemainingCells
                context[self.iter] = ''
                for i in range(nbOfMissingCellsLastLine):
                    self.buffer.evaluate(subElements=False)

        if hasHiddenVariable:
            context[self.iter] = hiddenVariable
        elif self.exprResult:
            del context[self.iter]


class NullAction(BufferAction):
    """Action that does nothing. Used in conjunction with a "from" clause, it
       allows to insert in a buffer arbitrary odt content."""
    __module__ = __name__

    def do(self):
        self.evaluateBuffer()