# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taco/ref_count_manager/ref_count_table_creation_config.py
# Compiled at: 2019-09-05 09:49:59
from taco.aws_wrappers.dynamodb_wrapper import table_creation_config, consts as dynamodb_consts
import taco.ref_count_manager.consts as ref_count_manager_consts

class RefCountTableCreation(table_creation_config.TableCreationConfig):

    def __init__(self, table_name=ref_count_manager_consts.REF_COUNT_DEFAULT_TABLE_NAME):
        super().__init__(table_name, [
         dynamodb_consts.property_schema(ref_count_manager_consts.RefCountTableConfig.routing_id.value, dynamodb_consts.PrimaryKeyTypes.hash_type.value)], [
         dynamodb_consts.property_schema(ref_count_manager_consts.RefCountTableConfig.routing_id.value, dynamodb_consts.AttributeTypes.string_type.value)])