# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/components/adapters/reordering/reordering.py
# Compiled at: 2011-01-05 09:31:32
from pyf.componentized.components.adapter import BaseAdapter
from pyf.dataflow import component
from pyf.transport import Packet
from pyjon.utils import get_secure_filename
import decimal, datetime
from pyf.componentized.configuration.keys import SimpleKey, RepeatedKey, CompoundKey, BooleanKey
from pyf.componentized.configuration.fields import InputField, SingleSelectField
import operator
from pyf.dataflow.reordering import reorder_flow

class FlowReorder(BaseAdapter):
    """
    This plugin will reorder reorder the flow by serializing it to temp files
    and replaying it in an ordered fashion.
    
    There are two serializers available:
    
        - "packet_marshal": Packet marshal (only for Packet objects, faster than pickle)
        - "pickle": Pickle (using latest version of pickle protocol)
    """
    display_name = 'Flow Reorderer'
    description = 'Reorders the flow by serializing it to temp files and replaying it in an ordered fashion.\n    There are two serializers available:\n    - "packet_marshal": Packet marshal (only for Packet objects, faster than pickle)\n    - "pickle": Pickle (using latest version of pickle protocol)'
    name = 'reorder'
    configuration = [
     CompoundKey('ordering', text_value='key', label='Ordering', attributes={'type': 'type'}, fields=[
      SingleSelectField('type', label='Type', default='attribute', values=[
       'attribute',
       'item',
       'eval']),
      InputField('key', label='Key', help_text='Key to order by (attribute name, eval code...)')]),
     SimpleKey('serializer', label='Serializer', field=SingleSelectField('serializer', label='Serializer', default='pickle', values=[
      'packet_marshal',
      'pickle']))]

    def __init__(self, config_node, name):
        super(FlowReorder, self).__init__(config_node, name)

    def get_comparator(self):
        info_dict = self.get_config_key('ordering', {'type': 'attribute', 'key': 'id'})
        if info_dict['type'] == 'attribute':
            return operator.attrgetter(info_dict['key'])
        if info_dict['type'] == 'item':
            return operator.itemgetter(info_dict['key'])
        if info_dict['type'] == 'eval':
            getter_code = compile(info_dict['key'], '<component "%s" comparator>' % self.node_name, 'eval')
            get_config_key = self.get_config_key
            get_config_key_node = self.get_config_key_node

            def getter(item, eval_code=getter_code):
                return eval(eval_code)

            return getter
        raise ValueError, 'Ordering key type "%s" not supported' % info_dict['type']

    def get_serializer(self):
        serializer_type = self.get_config_key('serializer', 'pickle')
        if serializer_type == 'pickle':
            try:
                import cPickle as pickle
            except ImportError:
                import pickle

            apickle = type('pickler', (), {})()
            apickle.loads = pickle.loads
            apickle.dumps = lambda v: pickle.dumps(v, -1)
            return apickle
        if serializer_type == 'packet_marshal':
            import marshal
            packet_marshal = type('pickler', (), {})()
            packet_marshal.loads = lambda v: Packet(marshal.loads(v), data_type='serialized')
            packet_marshal.dumps = lambda v: marshal.dumps(v.serialized)
            return packet_marshal
        raise ValueError, 'Serializer type "%s" not supported' % serializer_type

    @component('IN', 'OUT')
    def launch(self, values, out):
        key_comp = self.get_comparator()
        serializer = self.get_serializer()
        for item in reorder_flow(values, key_comp, continue_val=Ellipsis, serializer=serializer):
            yield item