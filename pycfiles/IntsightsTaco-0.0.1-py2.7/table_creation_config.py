# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taco/aws_wrappers/dynamodb_wrapper/table_creation_config.py
# Compiled at: 2019-09-05 09:49:59
from .consts import SCALABLE_DIMENSION

class TableCreationConfig(object):

    def __init__(self, table_name, primary_keys, attribute_definitions):
        self.table_name = table_name
        self.primary_keys = primary_keys
        self.attribute_definitions = attribute_definitions

    @property
    def resource_id(self):
        return ('table/{table_name}').format(table_name=self.table_name)

    @property
    def scalable_dimension(self):
        return SCALABLE_DIMENSION