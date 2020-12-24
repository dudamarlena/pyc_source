# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fourtytwo/bqtools/conversions.py
# Compiled at: 2019-10-22 02:13:37
# Size of source mod 2**32: 11370 bytes
import decimal, math, datetime, logging, json, dateutil, pandas as pd
NoneType = type(None)

def convert--- This code section failed: ---

 L.  13         0  LOAD_FAST                'field_type'
                2  LOAD_METHOD              upper
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'field_type'

 L.  14         8  LOAD_DEREF               'mode'
               10  LOAD_METHOD              upper
               12  CALL_METHOD_0         0  ''
               14  STORE_DEREF              'mode'

 L.  16        16  LOAD_FAST                'field_type'
               18  LOAD_STR                 'INTEGER'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    48  'to 48'

 L.  18        24  LOAD_CLOSURE             'infer_required'
               26  LOAD_CLOSURE             'mode'
               28  BUILD_TUPLE_2         2 
               30  LOAD_LISTCOMP            '<code_object <listcomp>>'
               32  LOAD_STR                 'convert.<locals>.<listcomp>'
               34  MAKE_FUNCTION_8          'closure'
               36  LOAD_FAST                'column'
               38  GET_ITER         
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'converted_column'
            44_46  JUMP_FORWARD        674  'to 674'
             48_0  COME_FROM            22  '22'

 L.  20        48  LOAD_FAST                'field_type'
               50  LOAD_STR                 'STRING'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    80  'to 80'

 L.  22        56  LOAD_CLOSURE             'infer_required'
               58  LOAD_CLOSURE             'mode'
               60  BUILD_TUPLE_2         2 
               62  LOAD_LISTCOMP            '<code_object <listcomp>>'
               64  LOAD_STR                 'convert.<locals>.<listcomp>'
               66  MAKE_FUNCTION_8          'closure'
               68  LOAD_FAST                'column'
               70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'converted_column'
            76_78  JUMP_FORWARD        674  'to 674'
             80_0  COME_FROM            54  '54'

 L.  24        80  LOAD_FAST                'field_type'
               82  LOAD_STR                 'NUMERIC'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   112  'to 112'

 L.  26        88  LOAD_CLOSURE             'infer_required'
               90  LOAD_CLOSURE             'mode'
               92  BUILD_TUPLE_2         2 
               94  LOAD_LISTCOMP            '<code_object <listcomp>>'
               96  LOAD_STR                 'convert.<locals>.<listcomp>'
               98  MAKE_FUNCTION_8          'closure'
              100  LOAD_FAST                'column'
              102  GET_ITER         
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'converted_column'
          108_110  JUMP_FORWARD        674  'to 674'
            112_0  COME_FROM            86  '86'

 L.  28       112  LOAD_FAST                'field_type'
              114  LOAD_STR                 'FLOAT'
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   144  'to 144'

 L.  30       120  LOAD_CLOSURE             'infer_required'
              122  LOAD_CLOSURE             'mode'
              124  BUILD_TUPLE_2         2 
              126  LOAD_LISTCOMP            '<code_object <listcomp>>'
              128  LOAD_STR                 'convert.<locals>.<listcomp>'
              130  MAKE_FUNCTION_8          'closure'
              132  LOAD_FAST                'column'
              134  GET_ITER         
              136  CALL_FUNCTION_1       1  ''
              138  STORE_FAST               'converted_column'
          140_142  JUMP_FORWARD        674  'to 674'
            144_0  COME_FROM           118  '118'

 L.  32       144  LOAD_FAST                'field_type'
              146  LOAD_STR                 'BOOLEAN'
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   176  'to 176'

 L.  34       152  LOAD_CLOSURE             'infer_required'
              154  LOAD_CLOSURE             'mode'
              156  BUILD_TUPLE_2         2 
              158  LOAD_LISTCOMP            '<code_object <listcomp>>'
              160  LOAD_STR                 'convert.<locals>.<listcomp>'
              162  MAKE_FUNCTION_8          'closure'
              164  LOAD_FAST                'column'
              166  GET_ITER         
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'converted_column'
          172_174  JUMP_FORWARD        674  'to 674'
            176_0  COME_FROM           150  '150'

 L.  36       176  LOAD_FAST                'field_type'
              178  LOAD_STR                 'BYTES'
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   208  'to 208'

 L.  38       184  LOAD_CLOSURE             'infer_required'
              186  LOAD_CLOSURE             'mode'
              188  BUILD_TUPLE_2         2 
              190  LOAD_LISTCOMP            '<code_object <listcomp>>'
              192  LOAD_STR                 'convert.<locals>.<listcomp>'
              194  MAKE_FUNCTION_8          'closure'
              196  LOAD_FAST                'column'
              198  GET_ITER         
              200  CALL_FUNCTION_1       1  ''
              202  STORE_FAST               'converted_column'
          204_206  JUMP_FORWARD        674  'to 674'
            208_0  COME_FROM           182  '182'

 L.  40       208  LOAD_FAST                'field_type'
              210  LOAD_STR                 'DATETIME'
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   240  'to 240'

 L.  42       216  LOAD_CLOSURE             'infer_required'
              218  LOAD_CLOSURE             'mode'
              220  BUILD_TUPLE_2         2 
              222  LOAD_LISTCOMP            '<code_object <listcomp>>'
              224  LOAD_STR                 'convert.<locals>.<listcomp>'
              226  MAKE_FUNCTION_8          'closure'
              228  LOAD_FAST                'column'
              230  GET_ITER         
              232  CALL_FUNCTION_1       1  ''
              234  STORE_FAST               'converted_column'
          236_238  JUMP_FORWARD        674  'to 674'
            240_0  COME_FROM           214  '214'

 L.  44       240  LOAD_FAST                'field_type'
              242  LOAD_STR                 'DATE'
              244  COMPARE_OP               ==
          246_248  POP_JUMP_IF_FALSE   274  'to 274'

 L.  46       250  LOAD_CLOSURE             'infer_required'
              252  LOAD_CLOSURE             'mode'
              254  BUILD_TUPLE_2         2 
              256  LOAD_LISTCOMP            '<code_object <listcomp>>'
              258  LOAD_STR                 'convert.<locals>.<listcomp>'
              260  MAKE_FUNCTION_8          'closure'
              262  LOAD_FAST                'column'
              264  GET_ITER         
              266  CALL_FUNCTION_1       1  ''
              268  STORE_FAST               'converted_column'
          270_272  JUMP_FORWARD        674  'to 674'
            274_0  COME_FROM           246  '246'

 L.  48       274  LOAD_FAST                'field_type'
              276  LOAD_STR                 'TIME'
              278  COMPARE_OP               ==
          280_282  POP_JUMP_IF_FALSE   308  'to 308'

 L.  50       284  LOAD_CLOSURE             'infer_required'
              286  LOAD_CLOSURE             'mode'
              288  BUILD_TUPLE_2         2 
              290  LOAD_LISTCOMP            '<code_object <listcomp>>'
              292  LOAD_STR                 'convert.<locals>.<listcomp>'
              294  MAKE_FUNCTION_8          'closure'
              296  LOAD_FAST                'column'
              298  GET_ITER         
              300  CALL_FUNCTION_1       1  ''
              302  STORE_FAST               'converted_column'
          304_306  JUMP_FORWARD        674  'to 674'
            308_0  COME_FROM           280  '280'

 L.  52       308  LOAD_FAST                'field_type'
              310  LOAD_STR                 'TIMESTAMP'
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   342  'to 342'

 L.  54       318  LOAD_CLOSURE             'infer_required'
              320  LOAD_CLOSURE             'mode'
              322  BUILD_TUPLE_2         2 
              324  LOAD_LISTCOMP            '<code_object <listcomp>>'
              326  LOAD_STR                 'convert.<locals>.<listcomp>'
              328  MAKE_FUNCTION_8          'closure'
              330  LOAD_FAST                'column'
              332  GET_ITER         
              334  CALL_FUNCTION_1       1  ''
              336  STORE_FAST               'converted_column'
          338_340  JUMP_FORWARD        674  'to 674'
            342_0  COME_FROM           314  '314'

 L.  56       342  LOAD_FAST                'field_type'
              344  LOAD_CONST               ('STRUCT', 'RECORD')
              346  COMPARE_OP               in
          348_350  POP_JUMP_IF_FALSE   640  'to 640'

 L.  57       352  LOAD_FAST                'fields'
          354_356  POP_JUMP_IF_TRUE    366  'to 366'

 L.  58       358  LOAD_GLOBAL              ValueError
              360  LOAD_STR                 'Fields must be provided for STRUCT/RECORD'
              362  CALL_FUNCTION_1       1  ''
              364  RAISE_VARARGS_1       1  ''
            366_0  COME_FROM           354  '354'

 L.  59       366  LOAD_DEREF               'mode'
              368  LOAD_STR                 'REPEATED'
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   516  'to 516'

 L.  60       376  LOAD_GLOBAL              isinstance
              378  LOAD_FAST                'column'
              380  LOAD_CONST               0
              382  BINARY_SUBSCR    
              384  LOAD_GLOBAL              list
              386  CALL_FUNCTION_2       2  ''
          388_390  POP_JUMP_IF_TRUE    400  'to 400'

 L.  61       392  LOAD_GLOBAL              ValueError
              394  LOAD_STR                 'For REPEATED mode in STRUCT/RECORD a list of dicts must be provided for each row'
              396  CALL_FUNCTION_1       1  ''
              398  RAISE_VARARGS_1       1  ''
            400_0  COME_FROM           388  '388'

 L.  62       400  BUILD_LIST_0          0 
              402  STORE_FAST               'converted_column'

 L.  63       404  SETUP_LOOP          638  'to 638'
              406  LOAD_FAST                'column'
              408  GET_ITER         
              410  FOR_ITER            512  'to 512'
              412  STORE_FAST               'r'

 L.  64       414  LOAD_GLOBAL              pd
              416  LOAD_METHOD              DataFrame
              418  LOAD_FAST                'r'
              420  CALL_METHOD_1         1  ''
              422  LOAD_METHOD              to_dict
              424  LOAD_STR                 'list'
              426  CALL_METHOD_1         1  ''
              428  STORE_FAST               'columns'

 L.  65       430  BUILD_MAP_0           0 
              432  STORE_FAST               'output'

 L.  66       434  SETUP_LOOP          486  'to 486'
              436  LOAD_FAST                'fields'
              438  GET_ITER         
              440  FOR_ITER            484  'to 484'
              442  STORE_FAST               'f'

 L.  67       444  LOAD_GLOBAL              convert
              446  LOAD_FAST                'columns'
              448  LOAD_METHOD              get
              450  LOAD_FAST                'f'
              452  LOAD_ATTR                name
              454  BUILD_LIST_0          0 
              456  CALL_METHOD_2         2  ''
              458  LOAD_FAST                'f'
              460  LOAD_ATTR                field_type
              462  LOAD_FAST                'f'
              464  LOAD_ATTR                mode
              466  LOAD_FAST                'f'
              468  LOAD_ATTR                fields
              470  CALL_FUNCTION_4       4  ''
              472  LOAD_FAST                'output'
              474  LOAD_FAST                'f'
              476  LOAD_ATTR                name
              478  STORE_SUBSCR     
          480_482  JUMP_BACK           440  'to 440'
              484  POP_BLOCK        
            486_0  COME_FROM_LOOP      434  '434'

 L.  68       486  LOAD_FAST                'converted_column'
              488  LOAD_METHOD              append
              490  LOAD_GLOBAL              pd
              492  LOAD_METHOD              DataFrame
              494  LOAD_FAST                'output'
              496  CALL_METHOD_1         1  ''
              498  LOAD_METHOD              to_dict
              500  LOAD_STR                 'records'
              502  CALL_METHOD_1         1  ''
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          
          508_510  JUMP_BACK           410  'to 410'
              512  POP_BLOCK        
              514  JUMP_FORWARD        638  'to 638'
            516_0  COME_FROM           372  '372'

 L.  69       516  LOAD_DEREF               'mode'
              518  LOAD_STR                 'NULLABLE'
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_FALSE   674  'to 674'

 L.  70       526  LOAD_GLOBAL              isinstance
              528  LOAD_FAST                'column'
              530  LOAD_CONST               0
              532  BINARY_SUBSCR    
              534  LOAD_GLOBAL              dict
              536  CALL_FUNCTION_2       2  ''
          538_540  POP_JUMP_IF_TRUE    550  'to 550'

 L.  71       542  LOAD_GLOBAL              ValueError
              544  LOAD_STR                 'For NULLABLE mode in STRUCT/RECORD only one dict is accepted per row'
              546  CALL_FUNCTION_1       1  ''
              548  RAISE_VARARGS_1       1  ''
            550_0  COME_FROM           538  '538'

 L.  72       550  LOAD_GLOBAL              pd
              552  LOAD_METHOD              DataFrame
              554  LOAD_FAST                'column'
              556  CALL_METHOD_1         1  ''
              558  LOAD_METHOD              to_dict
              560  LOAD_STR                 'list'
              562  CALL_METHOD_1         1  ''
              564  STORE_FAST               'columns'

 L.  73       566  BUILD_MAP_0           0 
              568  STORE_FAST               'output'

 L.  74       570  SETUP_LOOP          622  'to 622'
              572  LOAD_FAST                'fields'
              574  GET_ITER         
              576  FOR_ITER            620  'to 620'
              578  STORE_FAST               'f'

 L.  75       580  LOAD_GLOBAL              convert
              582  LOAD_FAST                'columns'
              584  LOAD_METHOD              get
              586  LOAD_FAST                'f'
              588  LOAD_ATTR                name
              590  BUILD_LIST_0          0 
              592  CALL_METHOD_2         2  ''
              594  LOAD_FAST                'f'
              596  LOAD_ATTR                field_type
              598  LOAD_FAST                'f'
              600  LOAD_ATTR                mode
              602  LOAD_FAST                'f'
              604  LOAD_ATTR                fields
              606  CALL_FUNCTION_4       4  ''
              608  LOAD_FAST                'output'
              610  LOAD_FAST                'f'
              612  LOAD_ATTR                name
              614  STORE_SUBSCR     
          616_618  JUMP_BACK           576  'to 576'
              620  POP_BLOCK        
            622_0  COME_FROM_LOOP      570  '570'

 L.  76       622  LOAD_GLOBAL              pd
              624  LOAD_METHOD              DataFrame
              626  LOAD_FAST                'output'
              628  CALL_METHOD_1         1  ''
              630  LOAD_METHOD              to_dict
              632  LOAD_STR                 'records'
              634  CALL_METHOD_1         1  ''
              636  STORE_FAST               'converted_column'
            638_0  COME_FROM           514  '514'
            638_1  COME_FROM_LOOP      404  '404'
              638  JUMP_FORWARD        674  'to 674'
            640_0  COME_FROM           348  '348'

 L.  78       640  LOAD_FAST                'field_type'
              642  LOAD_CONST               ('ARRAY', 'GEOGRAPHY')
              644  COMPARE_OP               in
          646_648  POP_JUMP_IF_FALSE   660  'to 660'

 L.  79       650  LOAD_GLOBAL              NotImplementedError
              652  LOAD_STR                 'Types ARRAY and GEOGRAPHY are not yet implemented.'
              654  CALL_FUNCTION_1       1  ''
              656  RAISE_VARARGS_1       1  ''
              658  JUMP_FORWARD        674  'to 674'
            660_0  COME_FROM           646  '646'

 L.  81       660  LOAD_GLOBAL              ValueError
              662  LOAD_STR                 '{} not a valid field_type.'
              664  LOAD_METHOD              format
              666  LOAD_FAST                'field_type'
              668  CALL_METHOD_1         1  ''
              670  CALL_FUNCTION_1       1  ''
              672  RAISE_VARARGS_1       1  ''
            674_0  COME_FROM           658  '658'
            674_1  COME_FROM           638  '638'
            674_2  COME_FROM           522  '522'
            674_3  COME_FROM           338  '338'
            674_4  COME_FROM           304  '304'
            674_5  COME_FROM           270  '270'
            674_6  COME_FROM           236  '236'
            674_7  COME_FROM           204  '204'
            674_8  COME_FROM           172  '172'
            674_9  COME_FROM           140  '140'
           674_10  COME_FROM           108  '108'
           674_11  COME_FROM            76  '76'
           674_12  COME_FROM            44  '44'

 L.  82       674  LOAD_FAST                'converted_column'
              676  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 638_1


def to_integer(value, mode='NULLABLE', infer_required=False):

    def handle_none():
        if mode == 'REQUIRED':
            if infer_required:
                return 0
            raise ValueError('None is not allowed.')
        else:
            return

    if isinstancevalueNoneType:
        int_value = handle_none()
    elif isinstancevaluefloat and math.isnanvalue:
        int_value = handle_none()
    elif isinstancevaluebytes:
        int_value = value.from_bytes(value, byteorder='big', signed=False)
    elif isinstancevaluestr:
        if value.isnumeric:
            int_value = int(value)
        elif value == 'False':
            int_value = 0
        elif value in ('', 'None', 'nan'):
            int_value = handle_none()
        else:
            f = float(value)
            if f.is_integer:
                int_value = int(f)
            elif math.isnanf:
                int_value = handle_none()
            else:
                logging.warning'Converting Float to Int with loss.'
                int_value = int(f)
    else:
        int_value = int(value)
    return int_value


def to_float(value, mode='NULLABLE', infer_required=False):

    def handle_none():
        if mode == 'REQUIRED':
            if infer_required:
                return 0.0
            raise ValueError('None is not allowed.')
        else:
            return float('nan')

    if isinstancevalueNoneType:
        float_value = handle_none()
    elif isinstancevaluestr:
        if value == 'False':
            float_value = 0.0
        elif value in ('', 'None', 'nan'):
            float_value = handle_none()
        else:
            float_value = float(value)
    else:
        float_value = float(value)
    return float_value


def to_string(value, mode='NULLABLE', infer_required=False):

    def handle_none():
        if mode == 'REQUIRED':
            if infer_required:
                return ''
            raise ValueError('None is not allowed.')
        else:
            return

    if isinstancevalueNoneType:
        str_value = handle_none()
    elif isinstancevaluefloat and math.isnanvalue:
        str_value = handle_none()
    elif isinstancevaluebytes:
        str_value = value.decode(encoding='utf8', errors='strict')
    elif isinstancevaluestr:
        if value in ('', 'None', 'nan'):
            str_value = handle_none()
        else:
            return value.replace'\n'' '
    else:
        str_value = str(value)
    return str_value


def to_numeric(value, mode='NULLABLE', infer_required=False):

    def handle_none():
        if mode == 'REQUIRED':
            if infer_required:
                return decimal.Decimal'0.0'
            raise ValueError('None is not allowed.')
        else:
            return

    if isinstancevalueNoneType:
        numeric_value = handle_none()
    elif isinstancevaluefloat and math.isnanvalue:
        numeric_value = handle_none()
    elif isinstancevaluestr:
        if value == '':
            numeric_value = decimal.Decimal'0.0'
        elif value in ('', 'None', 'nan'):
            numeric_value = handle_none()
        else:
            numeric_value = decimal.Decimalvalue
    else:
        numeric_value = decimal.Decimalvalue
    return numeric_value


def to_boolean(value, mode='NULLABLE', infer_required=False):

    def handle_none():
        if mode == 'REQUIRED':
            if infer_required:
                return False
            raise ValueError('None is not allowed.')
        else:
            return

    if isinstancevalueNoneType:
        bool_value = handle_none()
    elif isinstancevaluefloat and math.isnanvalue:
        bool_value = handle_none()
    elif isinstancevaluestr:
        if value in ('', '0', '0.0', 'False'):
            bool_value = False
        elif value in ('None', 'nan'):
            bool_value = handle_none()
        else:
            bool_value = True
    else:
        bool_value = bool(value)
    return bool_value


def to_bytes(value, mode='NULLABLE', infer_required=False):

    def handle_none():
        if mode == 'REQUIRED':
            if infer_required:
                return ''
            raise ValueError('None is not allowed.')
        else:
            return

    if isinstancevalueNoneType:
        bytes_value = handle_none()
    elif isinstancevaluefloat and math.isnanvalue:
        bytes_value = handle_none()
    elif isinstancevaluestr:
        if value == 'False':
            bytes_value = ''
        elif value in ('', 'None', 'nan'):
            bytes_value = handle_none()
        else:
            bytes_value = value.encode(encoding='utf8', errors='strict')
    elif isinstancevalueint:
        bytes_value = value.to_bytes(length=4, byteorder='big', signed=False)
    else:
        bytes_value = bytes(value)
    return bytes_value


def to_date(value, mode='NULLABLE', infer_required=False):
    if isinstancevaluedatetime.datetime:
        return value.date
    if isinstancevaluedatetime.date:
        return value
    dt_value = to_datetime(value, mode=mode, infer_required=infer_required)
    if dt_value is None:
        return dt_value
    return dt_value.date


def to_datetime(value, mode='NULLABLE', infer_required=False):

    def handle_none():
        if mode == 'REQUIRED':
            if infer_required:
                return datetime.datetime.min
            raise ValueError('None is not allowed.')
        else:
            return

    if isinstancevalueNoneType:
        dt_value = handle_none()
    elif isinstancevaluefloat and math.isnanvalue:
        dt_value = handle_none()
    elif isinstancevaluestr:
        if value in ('', 'None', 'nan', 'False'):
            dt_value = handle_none()
        else:
            dt_value = dateutil.parser.parsevalue
    elif isinstancevalue(int, float):
        dt_value = datetime.datetime.fromtimestampvalue
    elif isinstancevalue(tuple, list):
        dt_value = (datetime.datetime)(*value)
    elif isinstancevaluedict:
        dt_value = (datetime.datetime)(**value)
    elif isinstancevaluedatetime.datetime:
        dt_value = value
    else:
        raise NotImplementedError('Cannot convert {} to Datetime'.formattype(value))
    return dt_value


def to_time(value, mode='NULLABLE', infer_required=False):

    def handle_none():
        if mode == 'REQUIRED':
            if infer_required:
                return datetime.time.min
            raise ValueError('None is not allowed.')
        else:
            return

    if isinstancevalueNoneType:
        time_value = handle_none()
    elif isinstancevaluefloat and math.isnanvalue:
        time_value = handle_none()
    elif isinstancevaluestr:
        if value in ('', 'None', 'nan', 'False'):
            time_value = handle_none()
        else:
            time_value = to_datetime(value, mode=mode, infer_required=infer_required).time
    elif isinstancevalue(tuple, list):
        time_value = (datetime.time)(*value)
    else:
        time_value = to_datetime(value, mode=mode, infer_required=infer_required).time
    return time_value


def to_timestamp(value, mode='NULLABLE', infer_required=False):
    if isinstancevalue(int, float):
        ts_value = math.isnanvalue or float(value)
    else:
        ts_value = to_datetime(value, mode=mode, infer_required=infer_required).timestamp
    return ts_value


def to_struct(value, mode='NULLABLE', infer_required=False):
    raise NotImplementedError('Conversion to STRUCT is not implemented yet.')


def to_array(value, mode='NULLABLE', infer_required=False):
    raise NotImplementedError('Conversion to ARRAY is not implemented yet.')


def to_geograpy(value, mode='NULLABLE', infer_required=False):
    raise NotImplementedError('Conversion to GEOGRAPHY is not implemented yet.')