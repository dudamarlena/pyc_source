# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/src/opentea/noob/inferdefault.py
# Compiled at: 2020-03-11 12:20:40
# Size of source mod 2**32: 6891 bytes
"""Infer a nested object from a schema."""
from opentea.noob.noob import nob_pprint, str_address
import opentea.noob.validate_light as validate_light

def nob_complete(schema, update_data=None):
    """Infer a nested object from a schema.

    Input :
    -------
    schema :  a schema object
    update_data : nested object, providing known
        parts of the object to infer

    Output :
    --------
    nob_out : nested object
    """
    out = recursive_infer(schema, path=None,
      update_data=update_data)
    validate_light(out, schema)
    return out


def recursive_infer--- This code section failed: ---

 L.  40         0  LOAD_FAST                'path'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  41         8  LOAD_GLOBAL              list
               10  CALL_FUNCTION_0       0  '0 positional arguments'
               12  STORE_FAST               'path'
             14_0  COME_FROM             6  '6'

 L.  43        14  LOAD_CONST               None
               16  STORE_FAST               'out'

 L.  44        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'schema'
               22  LOAD_GLOBAL              dict
               24  CALL_FUNCTION_2       2  '2 positional arguments'
               26  POP_JUMP_IF_FALSE   214  'to 214'

 L.  45        28  LOAD_STR                 'type'
               30  LOAD_FAST                'schema'
               32  COMPARE_OP               in
               34  POP_JUMP_IF_FALSE   180  'to 180'

 L.  46        36  LOAD_FAST                'schema'
               38  LOAD_STR                 'type'
               40  BINARY_SUBSCR    
               42  LOAD_STR                 'object'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE   130  'to 130'

 L.  47        48  LOAD_STR                 'properties'
               50  LOAD_FAST                'schema'
               52  COMPARE_OP               in
               54  POP_JUMP_IF_FALSE    74  'to 74'

 L.  48        56  LOAD_GLOBAL              recursive_infer_properties

 L.  49        58  LOAD_FAST                'schema'
               60  LOAD_STR                 'properties'
               62  BINARY_SUBSCR    

 L.  50        64  LOAD_FAST                'path'

 L.  51        66  LOAD_FAST                'update_data'
               68  CALL_FUNCTION_3       3  '3 positional arguments'
               70  STORE_FAST               'out'
               72  JUMP_ABSOLUTE       178  'to 178'
             74_0  COME_FROM            54  '54'

 L.  52        74  LOAD_STR                 'oneOf'
               76  LOAD_FAST                'schema'
               78  COMPARE_OP               in
               80  POP_JUMP_IF_FALSE    96  'to 96'

 L.  53        82  LOAD_GLOBAL              recursive_infer_oneof
               84  LOAD_FAST                'schema'
               86  LOAD_FAST                'path'
               88  LOAD_FAST                'update_data'
               90  CALL_FUNCTION_3       3  '3 positional arguments'
               92  STORE_FAST               'out'
               94  JUMP_ABSOLUTE       178  'to 178'
             96_0  COME_FROM            80  '80'

 L.  55        96  LOAD_GLOBAL              RuntimeError

 L.  58        98  LOAD_STR                 'Cannot infer objects without properties or  oneOf\n At path : '
              100  LOAD_GLOBAL              str_address
              102  LOAD_FAST                'path'
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  BINARY_ADD       
              108  LOAD_STR                 '\n'
              110  BINARY_ADD       
              112  LOAD_GLOBAL              nob_pprint
              114  LOAD_FAST                'schema'
              116  LOAD_CONST               2
              118  LOAD_CONST               ('max_lvl',)
              120  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              122  BINARY_ADD       
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  RAISE_VARARGS_1       1  'exception instance'
              128  JUMP_ABSOLUTE       212  'to 212'
            130_0  COME_FROM            46  '46'

 L.  59       130  LOAD_FAST                'schema'
              132  LOAD_STR                 'type'
              134  BINARY_SUBSCR    
              136  LOAD_CONST               ('string', 'integer', 'number', 'boolean')
              138  COMPARE_OP               in
              140  POP_JUMP_IF_FALSE   154  'to 154'

 L.  63       142  LOAD_GLOBAL              recursive_infer_leafs
              144  LOAD_FAST                'schema'
              146  LOAD_FAST                'update_data'
              148  CALL_FUNCTION_2       2  '2 positional arguments'
              150  STORE_FAST               'out'
              152  JUMP_ABSOLUTE       212  'to 212'
            154_0  COME_FROM           140  '140'

 L.  64       154  LOAD_FAST                'schema'
              156  LOAD_STR                 'type'
              158  BINARY_SUBSCR    
              160  LOAD_STR                 'array'
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_FALSE   212  'to 212'

 L.  65       166  LOAD_GLOBAL              recursive_infer_array
              168  LOAD_FAST                'schema'
              170  LOAD_FAST                'path'
              172  LOAD_FAST                'update_data'
              174  CALL_FUNCTION_3       3  '3 positional arguments'
              176  STORE_FAST               'out'
              178  JUMP_ABSOLUTE       246  'to 246'
            180_0  COME_FROM            34  '34'

 L.  68       180  LOAD_GLOBAL              RuntimeError

 L.  71       182  LOAD_STR                 'Dead end. No type provided...\n At path : '
              184  LOAD_GLOBAL              str_address
              186  LOAD_FAST                'path'
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  BINARY_ADD       
              192  LOAD_STR                 '\n'
              194  BINARY_ADD       
              196  LOAD_GLOBAL              nob_pprint
              198  LOAD_FAST                'schema'
              200  LOAD_CONST               2
              202  LOAD_CONST               ('max_lvl',)
              204  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              206  BINARY_ADD       
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  RAISE_VARARGS_1       1  'exception instance'
            212_0  COME_FROM           164  '164'
              212  JUMP_FORWARD        246  'to 246'
            214_0  COME_FROM            26  '26'

 L.  73       214  LOAD_GLOBAL              RuntimeError

 L.  76       216  LOAD_STR                 'Dead end.\n At path : '
              218  LOAD_GLOBAL              str_address
              220  LOAD_FAST                'path'
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  BINARY_ADD       
              226  LOAD_STR                 '\n'
              228  BINARY_ADD       
              230  LOAD_GLOBAL              nob_pprint
              232  LOAD_FAST                'schema'
              234  LOAD_CONST               2
              236  LOAD_CONST               ('max_lvl',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  BINARY_ADD       
              242  CALL_FUNCTION_1       1  '1 positional argument'
              244  RAISE_VARARGS_1       1  'exception instance'
            246_0  COME_FROM           212  '212'

 L.  78       246  LOAD_FAST                'out'
              248  LOAD_CONST               None
              250  COMPARE_OP               is
          252_254  POP_JUMP_IF_FALSE   288  'to 288'

 L.  79       256  LOAD_GLOBAL              NotImplementedError

 L.  82       258  LOAD_STR                 'Could not infer schema\n At path : '
              260  LOAD_GLOBAL              str_address
              262  LOAD_FAST                'path'
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  BINARY_ADD       
              268  LOAD_STR                 '\n'
              270  BINARY_ADD       
              272  LOAD_GLOBAL              nob_pprint
              274  LOAD_FAST                'schema'
              276  LOAD_CONST               2
              278  LOAD_CONST               ('max_lvl',)
              280  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              282  BINARY_ADD       
              284  CALL_FUNCTION_1       1  '1 positional argument'
              286  RAISE_VARARGS_1       1  'exception instance'
            288_0  COME_FROM           252  '252'

 L.  84       288  LOAD_FAST                'out'
              290  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 290


def recursive_infer_leafs(schema, update_data=None):
    """Recursive inference specific to leafs."""
    out = None
    if 'enum' in schema:
        out = schema['enum'][0]
    else:
        if 'default' in schema:
            out = schema['default']
        if out is None:
            if schema['type'] == 'string':
                out = ''
            else:
                if schema['type'] in ('integer', 'number'):
                    out = infer_number(schema)
                else:
                    if schema['type'] == 'boolean':
                        out = False
                    else:
                        out = None
    if update_data is not None:
        out = update_data
    return out


def infer_number(schema):
    """Return default number if not provided by schema"""
    out = 0.0
    if schema['type'] == 'integer':
        out = 0
    elif 'maximum' in schema:
        out = schema['maximum']
        if 'exclusiveMaximum' in schema and schema['exclusiveMaximum']:
            if isinstance(out, float):
                out *= 0.9
    elif isinstance(out, int):
        out -= 1
    elif 'minimum' in schema:
        out = schema['minimum']
        if 'exclusiveMinimum' in schema and schema['exclusiveMinimum']:
            if isinstance(out, float):
                out *= 1.1
            else:
                if isinstance(out, int):
                    out += 1
    return out


def recursive_infer_oneof(schema, path, update_data=None):
    """Recursive inference specific to oneOfs."""
    key = schema['oneOf'][0]['required'][0]
    option_schema = schema['oneOf'][0]['properties']
    option_data = None
    if isinstance(update_data, dict):
        if update_data != {}:
            for update_key in update_data.keys():
                key = update_key
                break

            for option in schema['oneOf']:
                if option['required'][0] == key:
                    option_data = update_data[key]
                    option_schema = option['properties']

    out = dict
    out[key] = recursive_inferoption_schema[key][*path, key]option_data
    return out


def recursive_infer_array(schema, path, update_data=None):
    """Recursive inference specific to arrays."""
    out = list
    default_len = 1
    if 'maxItems' in schema:
        default_len = min(default_len, schema['maxItems'])
    elif 'minItems' in schema:
        default_len = max(default_len, schema['minItems'])
    else:
        if 'items' in schema:
            if isinstance(update_data, list):
                for i, item_data in enumerate(update_data):
                    out.append(recursive_inferschema['items'][
                     *path, i]item_data)

        else:
            for i in range(default_len):
                out.append(recursive_infer(schema['items'], [
                 *path, i]))

        if schema['items']['type'] == 'string':
            out = avoid_string_duplication(out)
        else:
            for index in range(default_len):
                out.append('item_#' + str(index))

    return out


def avoid_string_duplication(list_str):
    """Individualize repated string items."""
    new_list = list
    for item in list_str:
        new_item = item
        while new_item in new_list:
            new_item += '#'

        new_list.append(new_item)

    return new_list


def recursive_infer_properties(schema, path, update_data=None):
    """Recursive inference specific to properties."""
    out = dict
    for key in schema:
        if isinstance(update_data, dict):
            option_data = None
            if key in update_data:
                option_data = update_data[key]
            out[key] = recursive_inferschema[key][*path, key]option_data
        elif update_data is None:
            out[key] = recursive_infer(schema[key], [*path, key])
        else:
            raise RuntimeError('Path ' + str_address([*path, key]) + ': update_data is not a dict')

    return out