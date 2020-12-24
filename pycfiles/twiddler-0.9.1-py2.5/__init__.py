# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/__init__.py
# Compiled at: 2008-07-24 14:48:01
from copy import copy, deepcopy
from cPickle import dumps, loads
from elementtree.ElementTree import _escape_attrib as html_quote
from elementtree.ElementTree import _raise_serialization_error
from elementtree.ElementTree import Comment
from elementtree.ElementTree import fixtag
from elementtree.ElementTree import ProcessingInstruction
from elementtree.ElementTree import QName
from new import function
from twiddler.input.default import Default as DefaultImport
from twiddler.interfaces import ITwiddler, IElement, IRepeater
from twiddler.output.default import Default as DefaultOutput
from zope.interface import implements

class TwiddlerSearcher:

    def getBy(self, **kw):
        """
        specify at most one index to get by
        """
        if len(kw) != 1:
            raise ValueError('One and only one keyword parameter should be passed to getBy')
        return TwiddlerElement(self.node.findByAttribute(*kw.items()[0]), self.twiddler)

    def __getitem__(self, value):
        """
        try each indexed thing in order until at least one thing is returned
        """
        return TwiddlerElement(self.node.search(value), self.twiddler)


class Twiddler(TwiddlerSearcher):
    implements(ITwiddler)
    executor = None

    def __init__(self, source, input=DefaultImport, output=DefaultOutput, executor=None, filters=(
 html_quote,), indexes=('id', 'name')):
        """Create a twiddler from a string"""
        self.indexes = indexes
        self.input = input
        self.executor = executor
        self.setSource(source)
        self.output = output
        self.filters = filters
        self.twiddler = self

    def setSource(self, source):
        (self.node, executor) = self.input(source, self.indexes)
        if executor is False:
            del self.executor
        elif executor is not None:
            self.executor = executor
        return

    def setFilters(self, *filters):
        all_filters = []
        for filter in filters:
            if filter is True:
                all_filters.extend(self.filters)
            else:
                all_filters.append(filter)

        self.filters = all_filters

    def clone(self):
        """Returns a clone of this Twiddler in its current state"""
        return loads(dumps(self))

    def execute(self, *args, **kw):
        """Calls the executor in this Twiddler if one is defined"""
        if self.executor is not None:
            t = self.executor(*((self,) + args), **kw)
            del self.executor
            if t is not None:
                return t
        return self

    def render(self, *args, **kw):
        """Renders this Twiddler"""
        t = self.execute(*args, **kw)
        return t.output(t.node, *args, **kw)


class TwiddlerRepeater:
    implements(IRepeater)

    def __init__(self, twiddler, parent, node, index):
        self.twiddler = twiddler
        self.parent = parent
        self.node = node
        self.index = index

    def repeat(self, *args, **kw):
        """Used to repeat specific Twiddler elements."""
        node = deepcopy(self.node)
        element = TwiddlerElement(node, self.twiddler)
        self.parent.insert(self.index, node)
        self.index += 1
        if args or kw:
            element.replace(*args, **kw)
        return element


class TwiddlerElement(TwiddlerSearcher):
    implements(IElement)
    index = None

    def __init__(self, node, twiddler):
        self.node = node
        self.twiddler = twiddler

    def _filter(self, value, filters):
        for filter in filters:
            value = filter(value)

        return value

    def replace(self, content=True, tag=True, filters=True, attributes=None, **kwattributes):
        """Replace the specified parts of this element"""
        if attributes:
            kwattributes.update(attributes)
        if filters is False:
            all_filters = ()
        elif filters is True:
            all_filters = self.twiddler.filters
        else:
            all_filters = []
            try:
                for filter in filters:
                    if filter is True:
                        all_filters.extend(self.twiddler.filters)
                    else:
                        all_filters.append(filter)

            except TypeError:
                all_filters = (
                 filters,)

        node = self.node
        if IElement.providedBy(content):
            parent = node.parent
            index = parent.index(node)
            parent.remove(node)
            node = content.node
            if node._tree is not None:
                node = loads(dumps(content.node))
            parent.insert(index, node)
            self.node = node
        elif content is not True:
            for child in copy(node.getchildren()):
                node.remove(child)

            if content is False:
                node.text = None
            else:
                node.text = self._filter(unicode(content), all_filters)
        if tag is not True:
            node.tag = tag
        for (key, value) in kwattributes.items():
            if value is True:
                continue
            if value is False:
                node.delete(key)
            else:
                node.set(key, self._filter(unicode(value), all_filters))

        return

    def repeater(self):
        """Remove this element from the tree do it can be used for repeating"""
        parent = self.node.parent
        index = parent.index(self.node)
        self.node.parent.remove(self.node)
        return TwiddlerRepeater(self.twiddler, parent, self.node, index)

    def clone(self):
        """Creates a copy of this element that belongs to no Twiddler"""
        node = loads(dumps(self.node))
        node.parent = None
        node._tree = None
        return TwiddlerElement(node, self.twiddler)

    def remove(self):
        """Remove this node and all its children."""
        self.node.parent.remove(self.node)