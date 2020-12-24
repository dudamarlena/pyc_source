# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/xml_tree_serialization.py
# Compiled at: 2011-09-28 13:50:09
import xml.parsers.expat
from concurrent_tree_crawler.abstract_node import AbstractNode, NodeState

class XMLTreeWriter:

    def __init__(self, file_):
        self.__f = file_

    def write(self, sentinel):
        """
                @type sentinel: L{AbstractNode}
                """
        root = sentinel.get_child('root')
        self.__print(0, '<?xml version="1.0" encoding="UTF-8"?>')
        self.__print(0, '<tree>')
        self.__print_node(1, root)
        self.__print(0, '</tree>')

    def __print_node(self, level, node):
        prefix_str = ('<node name="{}" state="{}"').format(node.get_name(), NodeState.to_str(node.get_state()))
        children = node.get_children()
        if children:
            self.__print(level, ('{}>').format(prefix_str))
            for child in node.get_children():
                self.__print_node(level + 1, child)

            self.__print(level, '</node>')
        else:
            self.__print(level, ('{}/>').format(prefix_str))

    def __print(self, level, text):
        print >> self.__f, ('{}{}').format('\t' * level, text)


class XMLTreeReader:

    def __init__(self, file_):
        self.__file = file_
        self.__curr_node = None
        self.__parser = xml.parsers.expat.ParserCreate()
        self.__parser.StartElementHandler = self.__start_element
        self.__parser.EndElementHandler = self.__end_element
        self.__parser.CharacterDataHandler = self.__char_data
        return

    def __start_element(self, name, attrs):
        if name == 'tree':
            return
        if name == 'node':
            state = NodeState.from_str(attrs['state'])
            node_name = attrs['name']
            self.__curr_node = self.__curr_node.add_child(node_name, state)

    def __end_element(self, name):
        if name == 'tree':
            return
        if name == 'node':
            self.__curr_node = self.__curr_node.get_parent()

    def __char_data(self, data):
        pass

    def read--- This code section failed: ---

 L.  66         0  LOAD_FAST             1  'sentinel'
                3  LOAD_ATTR             0  'get_children'
                6  CALL_FUNCTION_0       0  None
                9  UNARY_NOT        
               10  POP_JUMP_IF_TRUE     22  'to 22'
               13  LOAD_ASSERT              AssertionError

 L.  67        16  LOAD_CONST               'The sentinel should be a single node, without children'
               19  RAISE_VARARGS_2       2  None

 L.  68        22  LOAD_FAST             1  'sentinel'
               25  LOAD_FAST             0  'self'
               28  STORE_ATTR            2  '__curr_node'

 L.  69        31  LOAD_FAST             0  'self'
               34  LOAD_ATTR             3  '__parser'
               37  LOAD_ATTR             4  'ParseFile'
               40  LOAD_FAST             0  'self'
               43  LOAD_ATTR             5  '__file'
               46  CALL_FUNCTION_1       1  None
               49  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 46