# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/adoc.py
# Compiled at: 2006-03-02 13:59:00
"""agile documentation (doctest) utilities
"""
from xix.utils.comp.interface import implements
from xix.utils.interfaces import IDocTestElement, IDocTestUnit
from xix.utils.interfaces import IDocTestLineup, IInterpreterSession
__author__ = 'Drew Smathers'
__contact__ = 'drew.smathers@gmail.com'
__license__ = 'MIT'
__revision__ = '$Revision$'

class DocTestElement:
    """DocTestElement provides the IDocTestElement

    >>> IDocTestElement.providedBy(DocTestElement)
    """
    __module__ = __name__
    implements(IDocTestElement)


class InterpreterLine(DocTestElement):
    __module__ = __name__


class InterpreterInput(InterpreterLine):
    __module__ = __name__

    def __init__(self, input):
        self.input = input


class InterpreterOutput(InterpreterLine):
    __module__ = __name__

    def __init__(self, output):
        self.output = output


class DocTestUnit:
    __module__ = __name__
    implements(IDocTestUnit)
    lines = []


class DocTestLineup(DocTestUnit):
    __module__ = __name__


class InterpreterLineup(DocTestLineup):
    __module__ = __name__
    implements(IInterpreterSession)
    interpreter = None


class PydocElement(DocTestElement):
    __module__ = __name__


class PydocMetatag(PydocElement):
    __module__ = __name__

    def __init__(self, tag, name=None, desc=None):
        self.tag = tag
        self.name = name or ''
        self.desc = desc or ''