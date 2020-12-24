# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/pushworkflow/scheme/scheme.py
# Compiled at: 2019-09-23 10:35:46
# Size of source mod 2**32: 12099 bytes
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '17/12/2018'
from xml.etree.ElementTree import TreeBuilder, Element, ElementTree
from collections import defaultdict
from itertools import count, chain
import json, pprint, base64, pickle, logging
from .node import Node
from ..workflow import ActorFactory, StartActor, StopActor, JoinUntilStopSignal
_logger = logging.getLogger(__name__)

class Scheme(object):
    __doc__ = '\n    class to define a workflow scheme from nodes and links\n\n    :param list nodes:\n    :param list links:\n    '

    def __init__(self, nodes=None, links=None):
        self.title = ''
        self.description = ''
        self.links = {}
        if links is not None:
            for link in links:
                self.links[link.id] = link

        else:
            self.nodes = nodes or []
            self.nodes_dict = {}
            for node in self.nodes:
                self.nodes_dict[node.id] = node

            if links is not None:
                self._update_nodes_from_links()
            self._actor_factory = {}
            for node in self.nodes:
                self._actor_factory[node] = ActorFactory(node)

            for node in self.nodes:
                actor_factory = self._actor_factory[node]
                for downstream_node in node.downstream_nodes:
                    downstream_actor_factory = self._actor_factory[downstream_node]
                    actor_factory.connect(downstream_actor_factory)

            self._start_actor = StartActor()
            for node in self.start_nodes():
                actor_factory = self._actor_factory[node]
                self._start_actor.connect(actor_factory)

            def connect_finals_nodes(actor):
                for node in self.finalsNodes():
                    actor_factory = self._actor_factory[node]
                    actor_factory.connect(actor)

            self._end_actor = StopActor()
            if self.has_final_join():
                self._join_actor = JoinUntilStopSignal('stop join')
                connect_finals_nodes(self._join_actor)
                self._join_actor.connect(self._end_actor)
            else:
                connect_finals_nodes(self._end_actor)

    def finalsNodes(self):
        """

        :return: list of final nodes (with no output) and which hasn't any
                 control node upstream
        """
        res = []
        for node in self.nodes:
            assert isinstance(node, Node)
            if node.isfinal():
                res.append(node)

        return res

    def start_nodes(self):
        res = []
        for node in self.nodes:
            assert isinstance(node, Node)
            if node.isstart():
                res.append(node)

        return res

    def endlessNodes(self):
        res = []
        for node in self.nodes:
            assert isinstance(node, Node)
            if node.endless is True:
                res.append(node)

        return res

    def save_to(self, output_file):
        """
        Save the scheme as an xml formated file to `stream`
        """
        tree = self.scheme_to_etree(data_format='literal')
        indent(tree.getroot(), 0)
        tree.write(output_file)

    def scheme_to_etree(self, data_format='literal', pickle_fallback=False):
        """
        Return an `xml.etree.ElementTree` representation of the `scheme.
        """
        builder = TreeBuilder(element_factory=Element)
        builder.start('scheme', {'version':'2.0',  'title':self.title or '', 
         'description':self.description or ''})
        node_ids = defaultdict(count().__next__)
        builder.start('nodes', {})
        for node in self.nodes:
            attrs = {'id':node.id, 
             'qualified_name':node._qualified_name}
            if type(node) is not Node:
                attrs['scheme_node_type'] = '%s.%s' % (type(node).__name__,
                 type(node).__module__)
            builder.start('node', attrs)
            builder.end('node')

        builder.end('nodes')
        link_ids = defaultdict(count().__next__)
        builder.start('links', {})
        for link in self.links:
            source = link.source_node_id
            sink = link.sink_node_id
            source_id = node_ids[source]
            sink_id = node_ids[sink]
            attrs = {'id':str(link_ids[link]),  'source_node_id':str(source_id), 
             'sink_node_id':str(sink_id), 
             'source_channel':link.source_channel, 
             'sink_channel':link.sink_channel, 
             'enabled':'true' if link.enabled else 'false'}
            builder.start('link', attrs)
            builder.end('link')

        builder.end('links')
        annotation_ids = defaultdict(count().__next__)
        builder.start('thumbnail', {})
        builder.end('thumbnail')
        builder.start('node_properties', {})
        for node in self.nodes:
            data = None
            if node.properties:
                try:
                    data, format = dumps((node.properties), format=data_format, pickle_fallback=pickle_fallback)
                except Exception:
                    _logger.error('Error serializing properties for node %r', (node.title),
                      exc_info=True)

                if data is not None:
                    builder.start('properties', {'node_id':str(node_ids[node]), 
                     'format':format})
                    builder.data(data)
                    builder.end('properties')

        builder.end('node_properties')
        builder.end('scheme')
        root = builder.close()
        tree = ElementTree(root)
        return tree

    def _update_nodes_from_links(self):
        """
        Update upstream and downstream nodes from links definition
        """
        self._clear_nodes_connections()
        for link_id, link in self.links.items():
            source_node = self.nodes_dict[link.source_node_id]
            sink_node = self.nodes_dict[link.sink_node_id]
            source_node.downstream_nodes.add(self.nodes_dict[link.sink_node_id])
            sink_node.upstream_nodes.add(self.nodes_dict[link.source_node_id])

    def _clear_nodes_connections(self):
        """
        clear for all nodes downstream and upstream nodes
        """
        for node in self.nodes:
            assert isinstance(node, Node)
            node.downstream_nodes = set()
            node.upstream_nodes = set()

    def has_final_join(self):
        """True if we need to send a 'end' signal before closing the workflow
        This is needed for DataList and DataWatcher
        """
        for node in self.nodes:
            if node.need_stop_join:
                return True

        return False


def contains_control_nodes(nodes_list):
    for _node in nodes_list:
        if _node.endless or contains_control_nodes(_node.upstream_nodes):
            return True

    return False


def indent(element, level=0, indent='\t'):
    """
    Indent an instance of a :class:`Element`. Based on
    (http://effbot.org/zone/element-lib.htm#prettyprint).

    """

    def empty(text):
        return not text or not text.strip()

    def indent_--- This code section failed: ---

 L. 267         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'element'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'child_count'

 L. 269         8  LOAD_FAST                'child_count'
               10  POP_JUMP_IF_FALSE   124  'to 124'

 L. 270        12  LOAD_DEREF               'empty'
               14  LOAD_FAST                'element'
               16  LOAD_ATTR                text
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  POP_JUMP_IF_FALSE    40  'to 40'

 L. 271        22  LOAD_STR                 '\n'
               24  LOAD_DEREF               'indent'
               26  LOAD_FAST                'level'
               28  LOAD_CONST               1
               30  BINARY_ADD       
               32  BINARY_MULTIPLY  
               34  BINARY_ADD       
               36  LOAD_FAST                'element'
               38  STORE_ATTR               text
             40_0  COME_FROM            20  '20'

 L. 273        40  LOAD_DEREF               'empty'
               42  LOAD_FAST                'element'
               44  LOAD_ATTR                tail
               46  CALL_FUNCTION_1       1  '1 positional argument'
               48  POP_JUMP_IF_FALSE    76  'to 76'

 L. 274        50  LOAD_STR                 '\n'
               52  LOAD_DEREF               'indent'
               54  LOAD_FAST                'level'
               56  LOAD_FAST                'last'
               58  POP_JUMP_IF_FALSE    64  'to 64'
               60  LOAD_CONST               -1
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            58  '58'
               64  LOAD_CONST               0
             66_0  COME_FROM            62  '62'
               66  BINARY_ADD       
               68  BINARY_MULTIPLY  
               70  BINARY_ADD       
               72  LOAD_FAST                'element'
               74  STORE_ATTR               tail
             76_0  COME_FROM            48  '48'

 L. 276        76  SETUP_LOOP          160  'to 160'
               78  LOAD_GLOBAL              enumerate
               80  LOAD_FAST                'element'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  GET_ITER         
               86  FOR_ITER            120  'to 120'
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'i'
               92  STORE_FAST               'child'

 L. 277        94  LOAD_DEREF               'indent_'
               96  LOAD_FAST                'child'
               98  LOAD_FAST                'level'
              100  LOAD_CONST               1
              102  BINARY_ADD       
              104  LOAD_FAST                'i'
              106  LOAD_FAST                'child_count'
              108  LOAD_CONST               1
              110  BINARY_SUBTRACT  
              112  COMPARE_OP               ==
              114  CALL_FUNCTION_3       3  '3 positional arguments'
              116  POP_TOP          
              118  JUMP_BACK            86  'to 86'
              120  POP_BLOCK        
              122  JUMP_FORWARD        160  'to 160'
            124_0  COME_FROM            10  '10'

 L. 280       124  LOAD_DEREF               'empty'
              126  LOAD_FAST                'element'
              128  LOAD_ATTR                tail
              130  CALL_FUNCTION_1       1  '1 positional argument'
              132  POP_JUMP_IF_FALSE   160  'to 160'

 L. 281       134  LOAD_STR                 '\n'
              136  LOAD_DEREF               'indent'
              138  LOAD_FAST                'level'
              140  LOAD_FAST                'last'
              142  POP_JUMP_IF_FALSE   148  'to 148'
              144  LOAD_CONST               -1
              146  JUMP_FORWARD        150  'to 150'
            148_0  COME_FROM           142  '142'
              148  LOAD_CONST               0
            150_0  COME_FROM           146  '146'
              150  BINARY_ADD       
              152  BINARY_MULTIPLY  
              154  BINARY_ADD       
              156  LOAD_FAST                'element'
              158  STORE_ATTR               tail
            160_0  COME_FROM           132  '132'
            160_1  COME_FROM           122  '122'
            160_2  COME_FROM_LOOP       76  '76'

Parse error at or near `COME_FROM' instruction at offset 160_1

    return indent_(element, level, True)


def dumps(obj, format='literal', prettyprint=False, pickle_fallback=False):
    """
    Serialize `obj` using `format` ('json' or 'literal') and return its
    string representation and the used serialization format ('literal',
    'json' or 'pickle').

    If `pickle_fallback` is True and the serialization with `format`
    fails object's pickle representation will be returned

    """
    if format == 'literal':
        try:
            return (
             literal_dumps(obj, prettyprint=prettyprint, indent=1),
             'literal')
        except (ValueError, TypeError) as ex:
            try:
                if not pickle_fallback:
                    raise
                _logger.debug('Could not serialize to a literal string')
            finally:
                ex = None
                del ex

    else:
        if format == 'json':
            try:
                return (
                 json.dumps(obj, indent=(1 if prettyprint else None)),
                 'json')
            except (ValueError, TypeError):
                if not pickle_fallback:
                    raise
                _logger.debug('Could not serialize to a json string')

        else:
            if format == 'pickle':
                return (
                 base64.encodebytes(pickle.dumps(obj)).decode('ascii'), 'pickle')
            raise ValueError('Unsupported format %r' % format)
    if pickle_fallback:
        _logger.warning('Using pickle fallback')
        return (base64.encodebytes(pickle.dumps(obj)).decode('ascii'), 'pickle')
    raise Exception('Something strange happened.')


def literal_dumps(obj, prettyprint=False, indent=4):
    """
    Write obj into a string as a python literal.
    """
    memo = {}
    NoneType = type(None)

    def check(obj):
        if type(obj) in [int, float, bool, NoneType, str, bytes]:
            return True
        if id(obj) in memo:
            raise ValueError('{0} is a recursive structure'.format(obj))
        memo[id(obj)] = obj
        if type(obj) in [list, tuple]:
            return all(map(check, obj))
        if type(obj) is dict:
            return all(map(check, chain(iter(obj.keys()), iter(obj.values()))))
        raise TypeError('{0} can not be serialized as a python literal'.format(type(obj)))

    check(obj)
    if prettyprint:
        return pprint.pformat(obj, indent=indent)
    return repr(obj)