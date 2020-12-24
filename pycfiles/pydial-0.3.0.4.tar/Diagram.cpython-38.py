# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\billingtonm\dropbox\code\pydiagrams\build\lib\pydiagrams\Diagram.py
# Compiled at: 2019-10-20 22:53:53
# Size of source mod 2**32: 9866 bytes
import pydiagrams.baseItems as baseItems
from pydiagrams.helpers.constants import *
import datetime, sys, os.path
from contextlib import contextmanager

class Item(baseItems.BaseItem):

    def __init__(self, label, **attrs):
        (baseItems.BaseItem.__init__)(self, label, **attrs)
        self.is_group = False

    @property
    def Id(self):
        return self.id or 

    @Id.setter
    def Id(self, value):
        self.id = value

    @property
    def Label(self):
        return self.label or 

    @Label.setter
    def Label(self, value):
        self.label = value

    @property
    def Note(self):
        return self.attrs.get('note')

    @Note.setter
    def Note(self, value):
        self.attrs['note'] = value

    def __str__(self):
        return (self.Helper.node)((self.Id), (self.Label), **self.attrs)

    def link(self, i2, label=None, **attrs):
        """ Create a link between this Item and i2 """
        edge_attrs = attrs
        fromItem = self
        if self.is_group:
            edge_attrs.update(ltail=('cluster_' + self.id))
            fromItem = self.get_first_item()
        elif i2.is_group:
            i2 = i2.get_first_item()
            edge_attrs.update(lhead=('cluster_' + i2.Diagram.id))
        else:
            d = self.Diagram
            assert d, 'Uhoh no diagram for {}'.format(self.__repr__())
            while True:
                if d != i2.Diagram and d.level > 0:
                    d = d.parent

        e = Edge(fromItem, i2, label, **attrs)
        d.add_item(e)
        return i2

    def link_edge(self, i2, dir=None):
        if isinstance(i2, baseItems.BaseItem):
            return self.link(i2, dir=dir)
        if isinstance(i2, ItemEdge):
            return (self.link)(i2.item, dir=dir, **i2.attrs)
        raise ValueError('type(i2)=' + str(type(i2)))

    def __rshift__(self, i2):
        """ Override the >> operator to mean to add an edge between this item and the i2 """
        return self.link_edge(i2)

    def __mod__(self, s):
        """ Override the % operator to add attributes to an edge. Used with the >> operator
            eg: Add a label to an edge:
                n1 >> n2 % "my label"
            eg: Add a label and color to an edge:
                n1 >> n2 % {label:'my label', color:'blue'}
        """
        if type(s) == str:
            return ItemEdge(item=self, label=s)
        if type(s) == dict:
            return ItemEdge(item=self, attrs=s)
        raise ValueError


class DiagramBase(Item):

    def __init__(self, helper, filename=None, label=None, **attrs):
        (Item.__init__)(self, label=label, **attrs)
        self.id = 'g'
        self.collection = baseItems.BaseItemCollection(self)
        self.parent = None
        self.helper = helper
        self._user_module_file = os.path.realpath(sys.modules['__main__'].__file__)
        self._filename = filename
        self._pathname = None
        self.level = 0
        self.edge_attrs = {}
        self.node_attrs = {}
        self.passthrough_index = 0
        self.is_group = True

    @property
    def FileName(self):
        if self._filename:
            fn = self._filename
        else:
            fn = os.path.basename(self._user_module_file).replace('.py', '')
        return fn + '.' + self.helper.extension

    @FileName.setter
    def FileName(self, value):
        self._filename = value

    @property
    def PathName(self):
        if self._pathname:
            return self._pathname
        return os.path.dirname(self._user_module_file)

    @PathName.setter
    def PathName(self, value):
        self._pathname = value

    @property
    def OutputFileName(self):
        return os.path.join(self.PathName, self.FileName)

    def add_item(self, item):
        if isinstance(item, Edge):
            base_attrs = item.fromItem.Diagram.edge_attrs.copy()
        elif isinstance(item, Item):
            base_attrs = self.node_attrs.copy()
        else:
            base_attrs = {}
        ia = item.attrs.copy()
        item.attrs = base_attrs
        item.attrs.update(ia)
        if 'label' in item.__dict__:
            if not item.label:
                item.label = base_attrs.get(label)
        return self.collection.add_item(item)

    def __str__(self):
        if self.parent:
            return (self.helper.startSubdiagram)((self.id), (self.label), **self.attrs) + '\n' + '\n'.join([str(v) for v in list(self.collection.values())]) + (self.helper.endSubdiagram)((self.id), (self.label), **self.attrs) + '\n'
        return ('ViewDiagram({id}, "{label}")'.format)(**self.__dict__)

    def render(self):
        yield self.helper.comment('Generated by pydiagrams @ {}').format(datetime.datetime.now())
        yield (self.helper.startDiagram)((self.FileName), (self.label), **self.attrs) + '\n'
        for v in list(self.collection.values()):
            yield str(v) + '\n'

        yield self.helper.endDiagram() + '\n'

    def dump--- This code section failed: ---

 L. 192         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _filename
                4  LOAD_STR                 'stdout'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    34  'to 34'

 L. 193        10  LOAD_FAST                'self'
               12  LOAD_METHOD              render
               14  CALL_METHOD_0         0  ''
               16  GET_ITER         
               18  FOR_ITER             32  'to 32'
               20  STORE_FAST               'l'

 L. 194        22  LOAD_GLOBAL              print
               24  LOAD_FAST                'l'
               26  CALL_FUNCTION_1       1  ''
               28  POP_TOP          
               30  JUMP_BACK            18  'to 18'
               32  JUMP_FORWARD         90  'to 90'
             34_0  COME_FROM             8  '8'

 L. 196        34  LOAD_FAST                'self'
               36  LOAD_ATTR                OutputFileName
               38  STORE_FAST               'output_filename'

 L. 197        40  LOAD_GLOBAL              print
               42  LOAD_STR                 'Creating: {}'
               44  LOAD_METHOD              format
               46  LOAD_FAST                'output_filename'
               48  CALL_METHOD_1         1  ''
               50  CALL_FUNCTION_1       1  ''
               52  POP_TOP          

 L. 198        54  LOAD_GLOBAL              open
               56  LOAD_FAST                'output_filename'
               58  LOAD_STR                 'w'
               60  CALL_FUNCTION_2       2  ''
               62  SETUP_WITH           84  'to 84'
               64  STORE_FAST               'f'

 L. 199        66  LOAD_FAST                'f'
               68  LOAD_METHOD              writelines
               70  LOAD_FAST                'self'
               72  LOAD_METHOD              render
               74  CALL_METHOD_0         0  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_WITH       62  '62'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      
             90_0  COME_FROM            32  '32'

Parse error at or near `BEGIN_FINALLY' instruction at offset 82

    def __getitem__(self, label):
        """ Returns an Item with a label """
        for v in list(self.collection.values()):
            if v.label == label:
                return v
            raise ValueError

    def get_first_item(self):
        for i in list(self.collection.values()):
            if not isinstance(i, DiagramBase):
                return i

    def passthrough(self, line):
        """ Adds a line of native code to the output """
        return self.add_item(PassthroughItem(line))

    @contextmanager
    def Cluster(self, label, **attrs):
        sub = (self.__class__)(helper=self.helper, label=label, **attrs)
        sub.parent = self
        sub.level = self.level + 1
        sub.node_attrs = self.node_attrs.copy()
        sub.edge_attrs = self.edge_attrs.copy()
        sub.id = hash(self)
        self.add_item(sub)
        yield sub
        sub.collection.set_ids()


class Edge(baseItems.BaseItem):

    def __init__(self, fromItem, toItem, label, **attrs):
        (baseItems.BaseItem.__init__)(self, label, **attrs)
        self.fromItem, self.toItem = fromItem, toItem

    def __str__(self):
        a = self.attrs.copy()
        if label in a:
            a.pop(label)
        return (self.Helper.edge)(self.fromItem.Id, self.toItem.Id, label=self.label, **a)


class PassthroughItem(baseItems.BaseItem):

    def __init__(self, line):
        baseItems.BaseItem.__init__(self, label=None)
        self.line = line

    def __str__(self):
        return self.line


class ItemEdge(object):
    """ItemEdge"""

    def __init__(self, item, label='', attrs={}):
        self.item = item
        self.attrs = attrs
        if label != '':
            self.attrs.update(label=label)


class Items(object):
    """Items"""

    def __init__(self, *items):
        self.itemList = []
        for i in items:
            assert isinstance(i, Item), '<{}> is not an instance of a Item'.format(i)
            self.itemList.append(i)

    def __getitem__(self, index):
        return self.itemList[index]

    def __rshift__(self, i2):
        if isinstance(i2, Item) or isinstance(i2, ItemEdge):
            for i in self.itemList:
                i.link_edge(i2)

        else:
            raise ValueError('type of i2 is {}'.format(type(i2)))


class Context(object):
    """Context"""

    def __init__(self, diagram):
        self.diagram = diagram

    def __enter__(self):
        return self.diagram

    def __exit__(self, *args):
        self.diagram.collection.set_ids()
        self.diagram.render()
        self.diagram.dump()