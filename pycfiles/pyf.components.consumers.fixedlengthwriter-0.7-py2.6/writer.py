# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/components/consumers/fixedlengthwriter/writer.py
# Compiled at: 2010-08-26 10:52:59
from pyf.componentized.error import MissingConfigEntryError
from pyf.componentized.components.multiwriter import MultipleFileWriter
from pyf.componentized.configuration.keys import RepeatedKey, SimpleKey, CompoundKey
from pyf.componentized.configuration.fields import InputField
import logging
logger = logging.getLogger()
from any2fixed import Any2Fixed

class FixedLengthWriter(MultipleFileWriter):
    name = 'fixedlengthwriter'
    configuration = [
     SimpleKey('encoding', default='UTF-8'),
     SimpleKey('target_filename', label='Target filename', default='filename.csv'),
     RepeatedKey('columns', 'column', content=CompoundKey('column', text_value='title', attributes={'attribute': 'attribute', 'renderer': 'renderer', 
        'length': 'length'}, fields=[
      InputField('title', label='Title', help_text='Column title'),
      InputField('attribute', label='Attribute', help_text='Source object attribute'),
      InputField('length', label='Length', help_text='Attribute length'),
      InputField('renderer', label='Renderer', help_text='Renderer eval (optionnal)')]))]

    def __init__(self, config_node, component_id):
        """Initialize a new FixedLengthWriter
        @param config: SafeConfigParser
        @type config: SafeConfigParser instance

        @param process_name: The process name to use
        @type process_name: String
        """
        self.config_node = config_node
        self.id = component_id
        self.columns = self.get_config_key('columns')
        if len(self.columns) == 0:
            raise MissingConfigEntryError
        self.column_definitions = list()
        self.__retrieve_columns_definition()

    def __retrieve_columns_definition(self):
        for column_def in self.columns:
            self.column_definitions.append(dict(attr=column_def.get('attribute') or column_def.get('title'), fieldname=column_def.get('title'), renderer=self.__get_renderer(column_def)))

    def __get_renderer(self, node):
        length = int(node.get('length'))
        if node.get('renderer'):
            renderer_sourcecode = node.get('renderer')
            co = compile(renderer_sourcecode, '<pyf.components.plugins.consumers.fixedlengthwriter' + ' node "%s", field "%s">' % (self.id,
             node.get('attribute') or node.get('title')), 'eval')
            renderer_func = lambda value, bytecode=co, length=length: eval(bytecode)
            return renderer_func
        else:
            logger.debug('return lambda value, length=length: str(value)[:%s].ljust(%s)' % (length, length))
            return lambda value, length=length: unicode(value)[:length].ljust(length)

    def __get_column_attributes(self):
        return [ col_def['attr'] for col_def in self.column_definitions ]

    def get_column_names(self):
        return [ col_def['fieldname'] for col_def in self.column_definitions ]

    def write(self, values, key, output_filename, target_filename):
        line_separator = eval(self.get_config_key('line_separator', 'u"\\r\\n"'))
        encoding = self.get_config_key('encoding')
        writer = Any2Fixed(target_filename=output_filename, field_mappings=self.column_definitions, linesep=line_separator, encoding=encoding)
        for data in values:
            writer.writeline(data)
            yield True

        writer.finalize()
        yield True