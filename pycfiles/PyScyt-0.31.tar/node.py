# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/scxml/node.py
# Compiled at: 2011-11-01 16:07:24
__doc__ = '\nCreated on Nov 7, 2009\n\n@author: Johan Roxendal\n\nThis file is part of pyscxml.\n\n    pyscxml is free software: you can redistribute it and/or modify\n    it under the terms of the GNU Lesser General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    pyscxml is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU Lesser General Public License for more details.\n\n    You should have received a copy of the GNU Lesser General Public License\n    along with pyscxml.  If not, see <http://www.gnu.org/licenses/>.\n'

class SCXMLNode(object):

    def __init__(self, id, parent, n):
        self.transition = []
        self.state = []
        self.final = []
        self.history = []
        self.onentry = []
        self.onexit = []
        self.invoke = []
        self.id = id
        self.parent = parent
        self.n = n
        self.initial = []
        self.isFirstEntry = True
        self.initDatamodel = lambda : None

    def addChild(self, child):
        self.state.append(child)

    def addHistory(self, child):
        self.history.append(child)

    def addFinal(self, child):
        self.final.append(child)

    def addTransition(self, trans):
        self.transition.append(trans)

    def addInvoke(self, entry):
        self.invoke.append(entry)

    def addOnentry(self, entry):
        self.onentry.append(entry)

    def addOnexit(self, exit):
        self.onexit.append(exit)

    def getChildren(self):
        return self.state + self.final

    def __repr__(self):
        return str(self)

    def __iter__(self):
        stack = [
         self]
        while len(stack) > 0:
            item = stack.pop()
            if hasattr(item, 'getChildren'):
                children = item.getChildren()
                children.reverse()
                stack.extend(children)
            yield item


class Executable(object):

    def __init__(self):
        self.exe = None
        return


class State(SCXMLNode):

    def __str__(self):
        return '<State id="%s">' % self.id


class Parallel(SCXMLNode):

    def __str__(self):
        return '<Parallel id="%s">' % self.id


class Initial(list, Executable):

    def __init__(self, iterable):
        list.__init__(self, iterable)
        Executable.__init__(self)


class History(object):

    def __init__(self, id, parent, type, n):
        self.id = id
        self.parent = parent
        if not type or type not in ('deep', 'shallow'):
            type = 'shallow'
        self.type = type
        self.n = n
        self.transition = []

    def addTransition(self, t):
        self.transition.append(t)

    def __str__(self):
        return '<History id="%s" type="%s">' % (self.id, self.type)


class Transition(Executable):

    def __init__(self, source):
        Executable.__init__(self)
        self.source = source
        self.target = []
        self.event = []
        self.cond = None
        self.type = 'external'
        return

    def __str__(self):
        attrs = 'source="%s" ' % self.source.id
        if self.target:
            attrs += 'target="%s" ' % (' ').join(self.target)
        if self.event:
            attrs += 'event="%s">' % self.event
        return '<Transition ' + attrs

    def __repr__(self):
        return str(self)


class Final(SCXMLNode):

    def __init__(self, id, parent, n):
        SCXMLNode.__init__(self, id, parent, n)
        self.donedata = None
        return

    def __str__(self):
        return '<Final id="%s">' % self.id


class Onentry(Executable):

    def __str__(self):
        return '<Onentry>'


class Onexit(Executable):

    def __str__(self):
        return '<Onexit>'


class SCXMLDocument(object):

    def __init__(self):
        self.initial = None
        self.stateDict = {}
        self._rootState = None
        self.name = ''
        self.binding = None
        return

    def setRoot(self, state):
        self._rootState = state
        self.addNode(state)

    def getRoot(self):
        return self._rootState

    rootState = property(getRoot, setRoot)

    def addNode(self, node):
        assert hasattr(node, 'id') and node.id
        self.stateDict[node.id] = node

    def getState(self, id):
        return self.stateDict.get(id)

    def __str__(self):

        def getDepth(state):
            if type(state) == Transition:
                return getDepth(state.source) + 1
            else:
                if not hasattr(state, 'parent') or not state.parent:
                    return 0
                return getDepth(state.parent) + 1

        output = ''
        for item in self:
            output += getDepth(item) * '    ' + str(item) + '\n'

        return output

    def __iter__(self):
        return iter(self.rootState)


__all__ = [
 'Final', 'History', 'Initial', 'Onentry', 'Onexit', 'Parallel', 'SCXMLDocument', 'State', 'Transition', 'SCXMLNode']