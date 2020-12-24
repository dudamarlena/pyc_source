# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/management/classmgr/Type.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 4058 bytes
""" Class description goes here. """
from dataclay.util.MgrObject import ManagementObject

class Type(ManagementObject):
    _fields = [
     'id',
     'descriptor',
     'signature',
     'typeName',
     'includes']
    _internal_fields = [
     'languageDepInfos']

    @staticmethod
    def build_from_type(type_instance):
        """Build a Type from a type instance (of a decorator, typically).
        :param type_instance: The instance passed to the decorator. Note that
        this may be a real type (like int, str, a custom DataClayObject class...)
        or it may be a string like 'list<storageobject>'.
        :return: A Type instance.
        """
        from .Utils import instance_types
        from dataclay import DataClayObject
        try:
            return instance_types[type_instance]
        except KeyError:
            pass

        if isinstance(type_instance, str):
            return Type.build_from_docstring(type_instance)
        if issubclass(type_instance, DataClayObject):
            full_name = type_instance.get_class_extradata().full_name
            namespace = type_instance.get_class_extradata().namespace
            from .UserType import UserType
            return UserType(namespace=namespace, typeName=full_name,
              signature=(('L%s;' % full_name).replace('.', '/')),
              includes=[])
        raise RuntimeError('Using a type instance is only supported for language primitives and DataClayObjects')

    @staticmethod
    def build_from_docstring--- This code section failed: ---

 L.  63         0  LOAD_CONST               1
                2  LOAD_CONST               ('NATIVE_PACKAGES', 'docstring_types')
                4  IMPORT_NAME              Utils
                6  IMPORT_FROM              NATIVE_PACKAGES
                8  STORE_FAST               'NATIVE_PACKAGES'
               10  IMPORT_FROM              docstring_types
               12  STORE_FAST               'docstring_types'
               14  POP_TOP          

 L.  64        16  SETUP_EXCEPT         26  'to 26'

 L.  65        18  LOAD_FAST                'docstring_types'
               20  LOAD_FAST                'type_str'
               22  BINARY_SUBSCR    
               24  RETURN_VALUE     
             26_0  COME_FROM_EXCEPT     16  '16'

 L.  66        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    44  'to 44'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  67        40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            32  '32'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'

 L.  69        46  LOAD_FAST                'type_str'
               48  LOAD_METHOD              startswith
               50  LOAD_STR                 'list'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  POP_JUMP_IF_TRUE     94  'to 94'

 L.  70        56  LOAD_FAST                'type_str'
               58  LOAD_METHOD              startswith
               60  LOAD_STR                 'tuple'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  POP_JUMP_IF_TRUE     94  'to 94'

 L.  71        66  LOAD_FAST                'type_str'
               68  LOAD_METHOD              startswith
               70  LOAD_STR                 'set'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  POP_JUMP_IF_TRUE     94  'to 94'

 L.  72        76  LOAD_FAST                'type_str'
               78  LOAD_METHOD              startswith
               80  LOAD_STR                 'dict'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  POP_JUMP_IF_TRUE     94  'to 94'

 L.  73        86  LOAD_FAST                'type_str'
               88  LOAD_STR                 'str'
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   126  'to 126'
             94_0  COME_FROM            84  '84'
             94_1  COME_FROM            74  '74'
             94_2  COME_FROM            64  '64'
             94_3  COME_FROM            54  '54'

 L.  77        94  LOAD_GLOBAL              Type
               96  LOAD_STR                 'python.%s'
               98  LOAD_FAST                'type_str'
              100  LOAD_METHOD              replace
              102  LOAD_STR                 '<'
              104  LOAD_STR                 '['
              106  CALL_METHOD_2         2  '2 positional arguments'
              108  LOAD_METHOD              replace
              110  LOAD_STR                 '>'
              112  LOAD_STR                 ']'
              114  CALL_METHOD_2         2  '2 positional arguments'
              116  BINARY_MODULO    

 L.  78       118  BUILD_LIST_0          0 
              120  LOAD_CONST               ('signature', 'includes')
              122  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              124  RETURN_VALUE     
            126_0  COME_FROM            92  '92'

 L.  80       126  LOAD_FAST                'type_str'
              128  LOAD_STR                 'anything'
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_TRUE    142  'to 142'
              134  LOAD_FAST                'type_str'
              136  LOAD_STR                 'storageobject'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   154  'to 154'
            142_0  COME_FROM           132  '132'

 L.  81       142  LOAD_GLOBAL              Type
              144  LOAD_FAST                'type_str'

 L.  82       146  BUILD_LIST_0          0 
              148  LOAD_CONST               ('signature', 'includes')
              150  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              152  RETURN_VALUE     
            154_0  COME_FROM           140  '140'

 L.  84       154  SETUP_EXCEPT        176  'to 176'

 L.  85       156  LOAD_FAST                'type_str'
              158  LOAD_METHOD              split
              160  LOAD_STR                 '.'
              162  LOAD_CONST               1
              164  CALL_METHOD_2         2  '2 positional arguments'
              166  UNPACK_SEQUENCE_2     2 
              168  STORE_FAST               'namespace'
              170  STORE_FAST               'full_name'
              172  POP_BLOCK        
              174  JUMP_FORWARD        208  'to 208'
            176_0  COME_FROM_EXCEPT    154  '154'

 L.  86       176  DUP_TOP          
              178  LOAD_GLOBAL              ValueError
              180  COMPARE_OP               exception-match
              182  POP_JUMP_IF_FALSE   206  'to 206'
              184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          

 L.  87       190  LOAD_GLOBAL              ValueError
              192  LOAD_STR                 'Could not split namespace and full_name from %s'
              194  LOAD_FAST                'type_str'
              196  BINARY_MODULO    
              198  CALL_FUNCTION_1       1  '1 positional argument'
              200  RAISE_VARARGS_1       1  'exception instance'
              202  POP_EXCEPT       
              204  JUMP_FORWARD        208  'to 208'
            206_0  COME_FROM           182  '182'
              206  END_FINALLY      
            208_0  COME_FROM           204  '204'
            208_1  COME_FROM           174  '174'

 L.  89       208  LOAD_FAST                'namespace'
              210  LOAD_FAST                'NATIVE_PACKAGES'
              212  COMPARE_OP               in
              214  POP_JUMP_IF_FALSE   228  'to 228'

 L.  90       216  LOAD_GLOBAL              Type
              218  LOAD_FAST                'type_str'

 L.  91       220  BUILD_LIST_0          0 
              222  LOAD_CONST               ('signature', 'includes')
              224  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              226  RETURN_VALUE     
            228_0  COME_FROM           214  '214'

 L.  93       228  LOAD_CONST               1
              230  LOAD_CONST               ('UserType',)
              232  IMPORT_NAME              UserType
              234  IMPORT_FROM              UserType
              236  STORE_FAST               'UserType'
              238  POP_TOP          

 L.  94       240  LOAD_FAST                'UserType'
              242  LOAD_FAST                'namespace'

 L.  95       244  LOAD_FAST                'full_name'

 L.  96       246  LOAD_STR                 'L%s;'
              248  LOAD_FAST                'full_name'
              250  BINARY_MODULO    
              252  LOAD_METHOD              replace
              254  LOAD_STR                 '.'
              256  LOAD_STR                 '/'
              258  CALL_METHOD_2         2  '2 positional arguments'

 L.  97       260  BUILD_LIST_0          0 
              262  LOAD_CONST               ('namespace', 'typeName', 'signature', 'includes')
              264  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              266  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_KW_4' instruction at offset 264