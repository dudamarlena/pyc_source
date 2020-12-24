# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/src/opentea/noob/validation.py
# Compiled at: 2020-03-04 10:05:22
# Size of source mod 2**32: 12531 bytes
"""Module to operate a trplie layer of validation"""
import json
from opentea.noob.noob import nob_find, nob_node_exist, nob_get, nob_set, nob_pprint
from opentea.noob.schema import clean_schema_addresses
from opentea.noob.inferdefault import nob_complete
import opentea.noob.validate_light as validate_light

class OpenteaSchemaError(Exception):
    __doc__ = 'Error in OptenTea schema structure'


def opentea_clean_data(nobj):
    """Check if data is opentea proof"""
    return rec_validate_opentea_data(nobj)


def rec_validate_opentea_data--- This code section failed: ---

 L.  31         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'nobj'
                4  LOAD_GLOBAL              dict
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    48  'to 48'

 L.  32        10  LOAD_GLOBAL              dict
               12  CALL_FUNCTION_0       0  '0 positional arguments'
               14  STORE_FAST               'out'

 L.  33        16  SETUP_LOOP          148  'to 148'
               18  LOAD_FAST                'nobj'
               20  GET_ITER         
               22  FOR_ITER             44  'to 44'
               24  STORE_FAST               'dict_key'

 L.  34        26  LOAD_GLOBAL              rec_validate_opentea_data
               28  LOAD_FAST                'nobj'
               30  LOAD_FAST                'dict_key'
               32  BINARY_SUBSCR    
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  LOAD_FAST                'out'
               38  LOAD_FAST                'dict_key'
               40  STORE_SUBSCR     
               42  JUMP_BACK            22  'to 22'
               44  POP_BLOCK        
               46  JUMP_FORWARD        148  'to 148'
             48_0  COME_FROM             8  '8'

 L.  35        48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'nobj'
               52  LOAD_GLOBAL              list
               54  CALL_FUNCTION_2       2  '2 positional arguments'
               56  POP_JUMP_IF_FALSE   144  'to 144'

 L.  36        58  LOAD_GLOBAL              isinstance
               60  LOAD_FAST                'nobj'
               62  LOAD_CONST               0
               64  BINARY_SUBSCR    
               66  LOAD_GLOBAL              dict
               68  CALL_FUNCTION_2       2  '2 positional arguments'
               70  POP_JUMP_IF_FALSE   138  'to 138'

 L.  37        72  LOAD_GLOBAL              list
               74  CALL_FUNCTION_0       0  '0 positional arguments'
               76  STORE_FAST               'out'

 L.  38        78  LOAD_GLOBAL              list
               80  CALL_FUNCTION_0       0  '0 positional arguments'
               82  STORE_FAST               'existing_names'

 L.  39        84  SETUP_LOOP          142  'to 142'
               86  LOAD_FAST                'nobj'
               88  GET_ITER         
               90  FOR_ITER            134  'to 134'
               92  STORE_FAST               'list_item'

 L.  40        94  LOAD_GLOBAL              clean_opentea_list_item
               96  LOAD_FAST                'list_item'

 L.  41        98  LOAD_FAST                'existing_names'
              100  CALL_FUNCTION_2       2  '2 positional arguments'
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'out_name'
              106  STORE_FAST               'clean_item'

 L.  42       108  LOAD_FAST                'existing_names'
              110  LOAD_METHOD              append
              112  LOAD_FAST                'out_name'
              114  CALL_METHOD_1         1  '1 positional argument'
              116  POP_TOP          

 L.  43       118  LOAD_FAST                'out'
              120  LOAD_METHOD              append
              122  LOAD_GLOBAL              rec_validate_opentea_data
              124  LOAD_FAST                'clean_item'
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  CALL_METHOD_1         1  '1 positional argument'
              130  POP_TOP          
              132  JUMP_BACK            90  'to 90'
              134  POP_BLOCK        
              136  JUMP_ABSOLUTE       148  'to 148'
            138_0  COME_FROM            70  '70'

 L.  45       138  LOAD_FAST                'nobj'
              140  STORE_FAST               'out'
            142_0  COME_FROM_LOOP       84  '84'
              142  JUMP_FORWARD        148  'to 148'
            144_0  COME_FROM            56  '56'

 L.  47       144  LOAD_FAST                'nobj'
              146  STORE_FAST               'out'
            148_0  COME_FROM           142  '142'
            148_1  COME_FROM            46  '46'
            148_2  COME_FROM_LOOP       16  '16'

 L.  48       148  LOAD_FAST                'out'
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 142_0


def clean_opentea_list_item(item_in, existing_names):
    """Add # to list elements to avoid duplication."""
    out_name = item_in['name']
    item_out = item_in.copy()
    if out_name == '':
        out_name = '#'
    if out_name in existing_names:
        while out_name in existing_names:
            out_name += '#'

    item_out['name'] = out_name
    return (out_name, item_out)


def validate_opentea_schema(schema):
    """Check if schema is OpenTEA-proof.

    - named items in arrays of dicts,
    - required optin in xors
    - existif and require defined
    """
    rec_validate_schema(schema)


def rec_validate_schema--- This code section failed: ---

 L.  78         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'schema'
                4  LOAD_GLOBAL              dict
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    82  'to 82'

 L.  80        10  LOAD_STR                 'type'
               12  LOAD_FAST                'schema'
               14  COMPARE_OP               in
               16  POP_JUMP_IF_FALSE    38  'to 38'

 L.  81        18  LOAD_FAST                'schema'
               20  LOAD_STR                 'type'
               22  BINARY_SUBSCR    
               24  LOAD_STR                 'array'
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L.  82        30  LOAD_GLOBAL              validate_array
               32  LOAD_FAST                'schema'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  POP_TOP          
             38_0  COME_FROM            28  '28'
             38_1  COME_FROM            16  '16'

 L.  84        38  LOAD_STR                 'oneOf'
               40  LOAD_FAST                'schema'
               42  COMPARE_OP               in
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L.  85        46  LOAD_GLOBAL              validate_oneof
               48  LOAD_FAST                'schema'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  POP_TOP          
             54_0  COME_FROM            44  '44'

 L.  87        54  SETUP_LOOP          116  'to 116'
               56  LOAD_FAST                'schema'
               58  GET_ITER         
               60  FOR_ITER             78  'to 78'
               62  STORE_FAST               'child_name'

 L.  88        64  LOAD_GLOBAL              rec_validate_schema
               66  LOAD_FAST                'schema'
               68  LOAD_FAST                'child_name'
               70  BINARY_SUBSCR    
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  POP_TOP          
               76  JUMP_BACK            60  'to 60'
               78  POP_BLOCK        
               80  JUMP_FORWARD        116  'to 116'
             82_0  COME_FROM             8  '8'

 L.  90        82  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'schema'
               86  LOAD_GLOBAL              list
               88  CALL_FUNCTION_2       2  '2 positional arguments'
               90  POP_JUMP_IF_FALSE   116  'to 116'

 L.  91        92  SETUP_LOOP          116  'to 116'
               94  LOAD_FAST                'schema'
               96  GET_ITER         
               98  FOR_ITER            112  'to 112'
              100  STORE_FAST               'child'

 L.  92       102  LOAD_GLOBAL              rec_validate_schema
              104  LOAD_FAST                'child'
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  POP_TOP          
              110  JUMP_BACK            98  'to 98'
              112  POP_BLOCK        
              114  JUMP_FORWARD        116  'to 116'
            116_0  COME_FROM           114  '114'
            116_1  COME_FROM_LOOP       92  '92'
            116_2  COME_FROM            90  '90'
            116_3  COME_FROM            80  '80'
            116_4  COME_FROM_LOOP       54  '54'

Parse error at or near `COME_FROM' instruction at offset 116_3


def validate_array(schema):
    """Validate an opentea multiple structure."""
    context = '\n\nMULTIPLE ERROR\n'
    context += nob_pprint(schema, max_lvl=4)
    if 'items' not in schema:
        context += '\n -items- is missing... '
        raise OpenteaSchemaError(context)
    elif 'type' not in schema['items']:
        context += '\n -items/type- is missing... '
        raise OpenteaSchemaError(context)
    elif schema['items']['type'] == 'object':
        if 'properties' not in schema['items']:
            context += '\n -items/type- is missing...'
            raise OpenteaSchemaError(context)
        if 'name' not in schema['items']['properties']:
            context += '\n -items/properties/name- is missing...'
            raise OpenteaSchemaError(context)
    elif schema['items']['type'] not in ('integer', 'number', 'string'):
        context += 'Type ' + schema['items']['type'] + ' unsupported in arrays'
        raise OpenteaSchemaError(context)


def validate_oneof(schema):
    """Validate an opentea multiple structure."""
    for oneof_item in schema['oneOf']:
        context = '\n\nXOR ERROR\n'
        context += nob_pprint(oneof_item, max_lvl=4)
        if not isinstance(oneof_item, dict):
            context += '\n oneOf item must be dicts '
            raise OpenteaSchemaError(context)
        if 'properties' not in oneof_item:
            context += '\n oneOf item need a -properties- item '
            raise OpenteaSchemaError(context)
        if 'required' not in oneof_item:
            context += '\n oneOf item need a -required- list item'
            raise OpenteaSchemaError(context)
        if len(oneof_item['required']) != 1:
            context += '\n oneOf item need a -required- list item with a single element '
            raise OpenteaSchemaError(context)
        if not isinstance(oneof_item['properties'], dict):
            context += '\n oneOf item need a dict in their properties'
            raise OpenteaSchemaError(context)
        if oneof_item['required'] != list(oneof_item['properties'].keys()):
            context += '\n all oneOf item need matching -required- and -properties keys- '
            context += '\n ' + str(oneof_item['required']) + ' <> ' + str(list(oneof_item['properties'].keys()))
            raise OpenteaSchemaError(context)
        real_shape = oneof_item['properties'][oneof_item['required'][0]]
        if not isinstance(real_shape, dict):
            context += '\n all oneOf item must have a dict in the -properties-'
            raise OpenteaSchemaError(context)


class ErrorExistIf(Exception):
    __doc__ = 'Errors on exist if elements.'


def opentea_resolve_existif(data, schema):
    """Validate existif dependencies.

    if an item existence depends on the value of one other item

    Parameters :
    -----------
    data : a nested dict to validate
    schema : the schema to validate against (jsonschema grammar)

    Return:
    -------
    data_out : a nested dict to synchronize
    data with require updated"""
    for sch_address in nob_find(schema, 'existif'):
        condition = nob_get(schema, *sch_address)
        dat_address = clean_schema_addresses(sch_address[:-1])
        if nob_node_exist(data, *dat_address):
            if not nob_node_exist(data, condition['node']):
                msgerr = 'node -' + '/'.join(dat_address) + '- Existif cannot be solved if a condition node -' + condition['node'] + '- is missing.'
                raise ErrorExistIf(msgerr)
            else:
                outcome = None
                value = nob_get(data, condition['node'])
                if isinstance(value, (int, float)):
                    if condition['operator'] == '==':
                        outcome = value == condition['value']
                    else:
                        if condition['operator'] == '>=':
                            outcome = value >= condition['value']
                        else:
                            if condition['operator'] == '<=':
                                outcome = value <= condition['value']
                            else:
                                if condition['operator'] == '>':
                                    outcome = value > condition['value']
                                else:
                                    if condition['operator'] == '<':
                                        outcome = value < condition['value']
                                    else:
                                        if condition['operator'] != '!=':
                                            outcome = value != condition['value']
                                        else:
                                            raise NotImplementedError('operator :' + condition['operator'])
                if isinstance(value, bool):
                    if condition['operator'] == '==':
                        outcome = value is condition['value']
                    else:
                        if condition['operator'] == '!=':
                            outcome = value is not condition['value']
                        else:
                            raise NotImplementedError('operator :' + condition['operator'])
            if outcome is False:
                msgerr = 'node ' + '/'.join(dat_address) + 'do no pass test :' + condition['node'] + str(condition['operator']) + str(condition['value'])
                raise ErrorExistIf(msgerr)


class ErrorRequire(Exception):
    __doc__ = 'Errors on require elements.'


def opentea_resolve_require(data, schema, verbose=False):
    """Validate require dependencies.

    if  children of an item depends of the value of one other item.
    -tgt- is the node to update
    -src- is the information used to update

    Parameters :
    -----------
    data : a nested dict to synchronize
    schema : the schema to validate against (jsonschema grammar)

    Return:
    -------
    data_out : a nested dict to synchronize
    data with require updated"""
    log = '## Resolve require log'
    data_out = data.copy()
    for tgt_schema_address in nob_find(schema, 'ot_require'):
        tgt_schema = nob_get(schema, *tgt_schema_address[:-1])
        src_nodename = nob_get(schema, *tgt_schema_address)
        multiple_fill = False
        if tgt_schema['type'] == 'array':
            if tgt_schema['items']['type'] == 'object':
                multiple_fill = True
        tgt_data_address = clean_schema_addresses(tgt_schema_address[:-1])
        log += 'ot_require : ' + '/'.join(tgt_schema_address)
        log += '  depending from ' + src_nodename + ')\n'
        log += '( Multiple mode :' + str(multiple_fill) + ')\n'
        if nob_node_exist(data, *tgt_data_address):
            log += _require_update_data(data, src_nodename, tgt_data_address, tgt_schema, data_out, multiple_fill)

    if verbose:
        print(log)
    return data_out


def _require_update_data(data, src_nodename, tgt_data_address, tgt_schema, data_out, multiple_fill):
    """Update data due to opentea require.

    Input :
    -------
    data : the nested dict to synchronize
    src_nodename : the name of the source
    tgt_data_address : the address of the target
    tgt_schema : the schema description of the targed
    InOut :
    --------
    data_out : the nested dict synchronized
    NOT STATELESS!
    """
    log = ''
    if not nob_node_exist(data, src_nodename):
        msgerr = 'node children -' + '/'.join(tgt_data_address) + '- ot_require cannot be solved if ' + 'the required node -' + src_nodename + '- is missing.'
        raise ErrorRequire(msgerr)
    else:
        data_to_paste = nob_get(data, src_nodename)
        current_names = nob_get(data_out, *tgt_data_address)
        if multiple_fill:
            current_names = list
            current_data = dict
            for items in nob_get(data_out, *tgt_data_address):
                current_names.append(items['name'])
                current_data[items['name']] = items

        else:
            current_names = nob_get(data_out, *tgt_data_address)
        if data_to_paste != current_names:
            log = 'Update is needed:\n'
            log += 'former data : ' + str(current_names) + '\n'
            log += 'new data.   : ' + str(data_to_paste) + '\n'
            if not multiple_fill:
                nob_set(data_out, data_to_paste, *tgt_data_address)
            else:
                multiple_paste = list
                for name in data_to_paste:
                    if name in current_names:
                        item_content = current_data[name]
                    else:
                        item_content = nob_complete(tgt_schema['items'], {'name': name})
                    multiple_paste.append(item_content)

                log += 'Setting to:\n' + nob_pprint(multiple_paste, max_lvl=3)
                nob_set(data_out, multiple_paste, *tgt_data_address)
    return log


def main_validate(data, schema):
    """Main validation procedure.

    Parameters:
    -----------
    data : a nested dict to validate
    schema : the schema to validate agains (jsonschema grammar)

    Return:
    -------
    Only exceptions are returned if any problem"""
    validate_light(data, schema)


if __name__ == '__main__':
    with open('./schema.json', 'r') as (fin):
        SCH = json.load(fin)
    with open('./test.json', 'r') as (fin):
        DAT = json.load(fin)
    main_validate(DAT, SCH)