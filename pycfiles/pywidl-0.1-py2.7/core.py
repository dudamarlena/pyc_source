# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywidl/core.py
# Compiled at: 2012-03-21 11:41:42


class IPyWIdlObject(object):

    @classmethod
    def attributes(cls):
        for attr in dir(cls):
            if not attr:
                continue
            if attr[0] == '_':
                continue
            yield (
             attr, getattr(cls, attr))


class PyWIdlObject(object):
    iface = None

    def __init__--- This code section failed: ---

 L.  19         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'iface'
                6  POP_JUMP_IF_TRUE     28  'to 28'
                9  LOAD_ASSERT              AssertionError
               12  LOAD_CONST               '%s.iface must be defined'
               15  LOAD_FAST             0  'self'
               18  LOAD_ATTR             2  '__class__'
               21  LOAD_ATTR             3  '__name__'
               24  BINARY_MODULO    
               25  RAISE_VARARGS_2       2  None

 L.  21        28  SETUP_LOOP          108  'to 139'
               31  LOAD_FAST             0  'self'
               34  LOAD_ATTR             0  'iface'
               37  LOAD_ATTR             4  'attributes'
               40  CALL_FUNCTION_0       0  None
               43  GET_ITER         
               44  FOR_ITER             91  'to 138'
               47  UNPACK_SEQUENCE_2     2 
               50  STORE_FAST            2  'attr'
               53  STORE_FAST            3  'default_value'

 L.  22        56  LOAD_GLOBAL           5  'hasattr'
               59  LOAD_FAST             0  'self'
               62  LOAD_FAST             2  'attr'
               65  CALL_FUNCTION_2       2  None
               68  POP_JUMP_IF_FALSE    77  'to 77'
               71  CONTINUE             44  'to 44'
               74  JUMP_FORWARD          0  'to 77'
             77_0  COME_FROM            74  '74'

 L.  23        77  LOAD_GLOBAL           5  'hasattr'
               80  LOAD_FAST             0  'self'
               83  LOAD_ATTR             2  '__class__'
               86  LOAD_FAST             2  'attr'
               89  CALL_FUNCTION_2       2  None
               92  POP_JUMP_IF_FALSE   101  'to 101'
               95  CONTINUE             44  'to 44'
               98  JUMP_FORWARD          0  'to 101'
            101_0  COME_FROM            98  '98'

 L.  24       101  LOAD_FAST             1  'kwargs'
              104  LOAD_ATTR             6  'get'
              107  LOAD_FAST             2  'attr'
              110  LOAD_FAST             3  'default_value'
              113  CALL_FUNCTION_2       2  None
              116  STORE_FAST            4  'value'

 L.  25       119  LOAD_GLOBAL           7  'setattr'
              122  LOAD_FAST             0  'self'
              125  LOAD_FAST             2  'attr'
              128  LOAD_FAST             4  'value'
              131  CALL_FUNCTION_3       3  None
              134  POP_TOP          
              135  JUMP_BACK            44  'to 44'
              138  POP_BLOCK        
            139_0  COME_FROM            28  '28'

Parse error at or near `POP_BLOCK' instruction at offset 138