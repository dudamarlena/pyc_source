# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/pod/elements.py
# Compiled at: 2009-09-30 05:37:25
from appy.shared.xml_parser import XmlElement
from appy.pod.odf_parser import OdfEnvironment as ns
from appy.pod import PodError

class PodElement:
    __module__ = __name__
    OD_TO_POD = {'p': 'Text', 'h': 'Title', 'section': 'Section', 'table': 'Table', 'table-row': 'Row', 'table-cell': 'Cell', None: 'Expression'}
    POD_ELEMS = ('text', 'title', 'section', 'table', 'row', 'cell')
    MINUS_ELEMS = ('section', 'table')

    def create(elem):
        """Used to create any POD elem that has a equivalent OD element. Not
           for creating expressions, for example."""
        return eval(PodElement.OD_TO_POD[elem])()

    create = staticmethod(create)


class Text(PodElement):
    __module__ = __name__
    OD = XmlElement('p', nsUri=ns.NS_TEXT)
    subTags = []


class Title(PodElement):
    __module__ = __name__
    OD = XmlElement('h', nsUri=ns.NS_TEXT)
    subTags = []


class Section(PodElement):
    __module__ = __name__
    OD = XmlElement('section', nsUri=ns.NS_TEXT)
    subTags = [Text.OD]
    DEEPEST_TO_REMOVE = OD


class Cell(PodElement):
    __module__ = __name__
    OD = XmlElement('table-cell', nsUri=ns.NS_TABLE)
    subTags = [Text.OD]

    def __init__(self):
        self.tableInfo = None
        return


class Row(PodElement):
    __module__ = __name__
    OD = XmlElement('table-row', nsUri=ns.NS_TABLE)
    subTags = [Cell.OD, Text.OD]


class Table(PodElement):
    __module__ = __name__
    OD = XmlElement('table', nsUri=ns.NS_TABLE)
    subTags = [Row.OD, Cell.OD, Text.OD]
    DEEPEST_TO_REMOVE = Cell.OD

    def __init__(self):
        self.tableInfo = None
        return


class Expression(PodElement):
    __module__ = __name__
    OD = None

    def __init__(self, pyExpr):
        self.expr = pyExpr

    def evaluate(self, context):
        res = eval(self.expr, context)
        if res == None:
            res = ''
        elif isinstance(res, str):
            res = unicode(res.decode('utf-8'))
        elif isinstance(res, unicode):
            pass
        else:
            res = unicode(res)
        return res