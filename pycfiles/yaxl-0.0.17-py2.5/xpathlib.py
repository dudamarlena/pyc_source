# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\yaxl\xpathlib.py
# Compiled at: 2006-10-30 07:00:41
"""Yet Another (Pythonic) XML Library - XPath support

YAXL is Copyright (C) 2005 by Iain Lowe and is released under the MIT License.
Visit http://www.ilowe.net/software/yaxl for the latest version.
"""
import yaxl

class XPathMixin:

    def __getRootElement(self):
        if self.parent:
            return self.parent.__getRootElement()
        else:
            return self

    def __assertPredicate(self, node, predicate):
        operators = {'!=': lambda x, y, r: r and str(r) != str(y), 
           '>=': lambda x, y, r: int(r) >= int(y), 
           '<=': lambda x, y, r: int(r) <= int(y), 
           '=': lambda x, y, r: '1', 
           '<': lambda x, y, r: str(r) < str(y), 
           '>': lambda x, y, r: int(r) > int(y)}
        for operator in operators.keys():
            if operator in predicate:
                (x, y) = predicate.split(operator)
                if y == 'last()':
                    y = str(len(node.parent.children))
                else:
                    y = eval(y)
                if x == 'position()':
                    x = node.parent.children.index(node) + 1
                else:
                    x = node(x)
                r = x
                if isinstance(r, yaxl.Element):
                    r = str(r)
                if operator == '=':
                    if isinstance(r, tuple):
                        return True
                    else:
                        return str(r) == str(y)
                else:
                    return operators[operator](x, y, r)
        else:
            return node(predicate) is not None

        return

    def __applyPredicates(self, nodeset, predicates):
        if not isinstance(nodeset, tuple):
            return self.__applyPredicates((nodeset,), predicates)
        for predicate in predicates:
            nodeset = [ x for x in nodeset if self.__assertPredicate(x, predicate) ]

        return self.__formatRetval(nodeset)

    def __formatRetval(self, retval):
        if len(retval) == 1:
            return retval[0]
        elif len(retval) > 1:
            return tuple(retval)
        else:
            return
        return

    def __selectAlongChildAxis(self, nodeTest):
        if nodeTest == '*':
            return self.__formatRetval([ x for x in self.children ])
        elif nodeTest == 'text()' or nodeTest == 'node()':
            return self.__formatRetval([ x for x in self.children ])
        else:
            x = self.__formatRetval([ x for x in self.children if type(x) not in (str, unicode) if x.qname == nodeTest ])
            return x

    def __selectAlongAttributeAxis(self, nodeTest):
        if nodeTest == '*':
            return self.attributes.values()
        if self.attributes.has_key(nodeTest):
            return self[nodeTest]

    def __selectAlongDescendantAxis(self, nodeTest):
        dlist = []

        def findMatchingNodes(x):
            for y in [ i for i in x.children if type(i) not in (str, unicode) ]:
                if y.qname == nodeTest:
                    dlist.append(y)
                findMatchingNodes(y)

        findMatchingNodes(self)
        return self.__formatRetval(dlist)

    def __selectAlongDescendantOrSelfAxis(self, nodeTest):
        dlist = []

        def findMatchingNodes(x):
            for y in [ i for i in x.children if type(i) not in (str, unicode) ]:
                if nodeTest in ('*', y.qname):
                    dlist.append(y)
                findMatchingNodes(y)

        findMatchingNodes(self)
        if nodeTest == self.qname:
            dlist.append(self)
        return self.__formatRetval(dlist)

    def __select(self, xpath):
        if 'count' in xpath:

            def countit(x):
                r = self.__select(x.group(1))
                if isinstance(r, tuple):
                    return str(len(r))
                elif isinstance(r, yaxl.Element):
                    return '1'
                else:
                    return '0'

            import re
            xpath = re.sub('count\\((.+?)\\)', countit, xpath)
        try:
            return int(xpath)
        except:
            pass

        xpath = xpath.replace('//', '/descendant::')
        if xpath == '/':
            return self.__getRootElement()
        elif xpath.startswith('/'):
            return self.__getRootElement().__select(xpath[1:])
        locationStep = None
        rest = None
        result = None
        predicates = []
        if '/' in xpath:
            xpathParts = xpath.split('/')
            locationStep, rest = xpathParts[0], ('/').join(xpathParts[1:])
        else:
            locationStep = xpath
        if '[' in locationStep:
            lStepParts = locationStep.split('[')
            predicates = [ x[:-1] for x in lStepParts[1:] ]
            locationStep = lStepParts[0]
        if '::' in locationStep:
            lsParts = locationStep.split('::')
            axis = lsParts[0]
            nodeTest = lsParts[1]
            if axis == 'child':
                result = self.__selectAlongChildAxis(nodeTest)
            elif axis == 'descendant':
                result = self.__selectAlongDescendantAxis(nodeTest)
            elif axis in ('parent', 'ancestor'):
                if self.parent and nodeTest in ('*', self.parent.qname):
                    result = self.parent
            elif axis == 'attribute':
                result = self.__selectAlongAttributeAxis(nodeTest)
            elif axis == 'self':
                if nodeTest in ('*', self.qname):
                    result = self
                else:
                    result = self.__selectAlongChildAxis(nodeTest)
            elif axis == 'descendant-or-self':
                result = self.__selectAlongDescendantOrSelfAxis(nodeTest)
            elif axis == 'ancestor-or-self':
                dlist = []

                def findMatchingNodes(x):
                    if x.qname == nodeTest:
                        dlist.append(x)
                    if x.parent:
                        findMatchingNodes(x.parent)

                findMatchingNodes(self)
                result = self.__formatRetval(dlist)
        elif locationStep[0] == '@':
            result = self.__selectAlongAttributeAxis(locationStep[1:])
        elif locationStep == '..':
            result = self.parent
        elif locationStep == '.':
            result = self
        elif locationStep == 'last()':
            result = len(self.children)
        elif locationStep == 'position()':
            result = self.parent.children.index(self) + 1
        else:
            result = self.__selectAlongChildAxis(locationStep)
        if result:
            result = self.__applyPredicates(result, predicates)
        if result and rest:
            r = []
            if isinstance(result, tuple):
                for n in result:
                    xx = n(rest)
                    if isinstance(xx, tuple):
                        for x in xx:
                            r.append(x)

                    elif xx:
                        r.append(xx)

            if isinstance(result, yaxl.Element):
                return result(rest)
            return self.__formatRetval(r)
        else:
            return result
        return

    def __call__(self, xpath_expression, return_nodelist=False):
        """Evaluates the supplied XPath expression using this element as the context.
        
        The `return_nodelist` parameter, if True, forces this query to return
        a node list that has zero or more elements. If False, the return value of
        the query is either a nodelist or a single `Element` object.
        """
        v = self.__select(xpath_expression)
        if return_nodelist and not isinstance(v, tuple):
            return tuple([v])
        else:
            return v