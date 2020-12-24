# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/utils/conversion.py
# Compiled at: 2019-08-01 15:53:35
# Size of source mod 2**32: 3095 bytes
"""
Conversion utilities for btrdb
"""
import uuid, json, pytz
from datetime import datetime
try:
    import numpy as np
except ImportError:
    np = None
else:
    RFC3339 = '%Y-%m-%d %H:%M:%S.%f%z'

    class AnnotationEncoder(json.JSONEncoder):
        __doc__ = 'Default JSON encoder class for saving stream annotations'

        def default(self, obj):
            """Handle complex and user-specific types"""
            if isinstance(obj, uuid.UUID):
                return str(obj)
            else:
                if isinstance(obj, datetime):
                    return obj.strftime(RFC3339)
                if np is not None and isinstance(obj, np.datetime64):
                    return pytz.utc.localize(obj.astype(datetime)).strftime(RFC3339)
            return json.JSONEncoder.default(self, obj)

        def encode(self, obj):
            serialized = super(AnnotationEncoder, self).encode(obj)
            if serialized.startswith('"'):
                if serialized.endswith('"'):
                    serialized = serialized.strip('"')
            return serialized


    class AnnotationDecoder(json.JSONDecoder):
        __doc__ = 'Default JSON decoder class for deserializing stream annotations'

        def decode--- This code section failed: ---

 L.  76         0  SETUP_FINALLY        20  'to 20'

 L.  77         2  LOAD_GLOBAL              super
                4  LOAD_GLOBAL              AnnotationDecoder
                6  LOAD_FAST                'self'
                8  CALL_FUNCTION_2       2  ''
               10  LOAD_METHOD              decode
               12  LOAD_FAST                's'
               14  CALL_METHOD_1         1  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  78        20  DUP_TOP          
               22  LOAD_GLOBAL              json
               24  LOAD_ATTR                JSONDecodeError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    44  'to 44'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.  79        36  LOAD_FAST                's'
               38  ROT_FOUR         
               40  POP_EXCEPT       
               42  RETURN_VALUE     
             44_0  COME_FROM            28  '28'
               44  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 32


    def to_uuid(obj):
        """
    Converts argument to UUID

    @param obj: object to be converted to UUID
    @return: returns instance of uuid.UUID
    @raise TypeError: raised if obj is of unsupported class
    """
        if isinstance(obj, uuid.UUID):
            return obj
        if isinstance(obj, bytes):
            obj = obj.decode('UTF-8')
        if isinstance(obj, str):
            return uuid.UUID(obj)
        raise TypeError('Cannot convert object to UUID ({})'.format(obj.__class__.__name__))