# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\XPathExtensions.py
# Compiled at: 2005-04-06 18:05:47


class RtfExpr:
    __module__ = __name__

    def __init__(self, nodes):
        self.nodes = nodes

    def evaluate(self, context):
        processor = context.processor
        processor.pushResultTree(context.currentInstruction.baseUri)
        try:
            for child in self.nodes:
                child.instantiate(context, processor)

            result = processor.popResult()
        finally:
            pass
        return result

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<RtfExpr at %x: %s>' % (id(self), str(self.nodes))


class SortedExpression:
    __module__ = __name__

    def __init__(self, expression, sortKeys):
        self.expression = expression
        self.sortKeys = sortKeys or []
        return

    def __str__(self):
        return '<SortedExpr at 0x%x: %s>' % (id(self), repr(self.expression))

    def compare(self, (node1, keys1), (node2, keys2)):
        for i in xrange(len(self.cmps)):
            diff = self.cmps[i](keys1[i], keys2[i])
            if diff:
                return diff

        return cmp(node1, node2)

    def evaluate(self, context):
        if self.expression is None:
            base = context.node.childNodes
        else:
            base = self.expression.evaluate(context)
            if type(base) is not type([]):
                raise TypeError('expected nodeset, %s found' % type(base).__name__)
        state = context.copy()
        size = len(base)
        nodekeys = [None] * size
        pos = 1
        for node in base:
            (context.node, context.position, context.size) = (
             node, pos, size)
            context.currentNode = node
            keys = map(lambda sk, c=context: sk.evaluate(c), self.sortKeys)
            nodekeys[pos - 1] = (node, keys)
            pos += 1

        context.set(state)
        self.cmps = map(lambda sk, c=context: sk.getComparer(c), self.sortKeys)
        nodekeys.sort(self.compare)
        return map(lambda nk: nk[0], nodekeys)
        return