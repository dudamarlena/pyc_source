# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lambadalib/functionproxy.py
# Compiled at: 2017-04-25 15:30:45
# Size of source mod 2**32: 1920 bytes
import json, types
from lambadalib import netproxy

def color(s):
    return '\x1b[94m' + s + '\x1b[0m'


class Proxy:

    def __new__(cls, classname, proxy=True):
        print(color('[functionproxy new] {} {} {}'.format(cls, classname, proxy)))
        if proxy:
            return lambda : Proxy(classname, False)
        else:
            return object.__new__(cls)

    def __init__(self, classname, ignoreproxy):
        print(color('[functionproxy init] {}'.format(classname)))
        self.classname = classname
        self.__remote__init__()

    def __getattr__(self, name):
        print(color('[functionproxy remote call] {} {}'.format(self.classname, name)))

        def method(*args):
            cn = self.classname
            _d = json.dumps(self.__dict__)
            _dc = json.loads(_d)
            del _dc['classname']
            _d = json.dumps(_dc)
            print(color('[functionproxy] >> {} {}'.format(args, _d)))
            _d, *args = netproxy.Netproxy(_d, self.classname, name, args)
            print(color('[functionproxy] << {} {}'.format(args, _d)))
            self.__dict__ = json.loads(_d)
            self.__dict__['classname'] = cn
            return args

        return method


def scanclass(mod, modname, cname):
    print(color('[scan] class {} -> proxy'.format(cname)))
    if mod and modname:
        setattr(mod, cname, Proxy('{}.{}'.format(modname, cname)))
    else:
        globals()[cname] = Proxy('{}'.format(cname))


def scan--- This code section failed: ---

 L.  53         0  SETUP_LOOP          190  'to 190'
                3  LOAD_FAST                'globalnames'
                6  GET_ITER         
                7  FOR_ITER            189  'to 189'
               10  STORE_FAST               'modname'

 L.  54        13  LOAD_GLOBAL              type
               16  LOAD_FAST                'globalnames'
               19  LOAD_FAST                'modname'
               22  BINARY_SUBSCR    
               23  CALL_FUNCTION_1       1  '1 positional, 0 named'
               26  LOAD_GLOBAL              types
               29  LOAD_ATTR                ModuleType
               32  COMPARE_OP               ==
               35  POP_JUMP_IF_FALSE   167  'to 167'

 L.  55        38  LOAD_CONST               ('json', 'sys', 'functionproxy')
               41  STORE_FAST               'blacklist'

 L.  56        44  LOAD_FAST                'modname'
               47  LOAD_STR                 '__builtins__'
               50  LOAD_GLOBAL              __name__
               53  BUILD_TUPLE_2         2 
               56  LOAD_FAST                'blacklist'
               59  BINARY_ADD       
               60  COMPARE_OP               not-in
               63  POP_JUMP_IF_FALSE   186  'to 186'

 L.  57        66  LOAD_GLOBAL              print
               69  LOAD_GLOBAL              color
               72  LOAD_STR                 '[scan] module {}'
               75  LOAD_ATTR                format
               78  LOAD_FAST                'modname'
               81  CALL_FUNCTION_1       1  '1 positional, 0 named'
               84  CALL_FUNCTION_1       1  '1 positional, 0 named'
               87  CALL_FUNCTION_1       1  '1 positional, 0 named'
               90  POP_TOP          

 L.  58        91  LOAD_FAST                'globalnames'
               94  LOAD_FAST                'modname'
               97  BINARY_SUBSCR    
               98  STORE_FAST               'mod'

 L.  59       101  SETUP_LOOP          186  'to 186'
              104  LOAD_GLOBAL              dir
              107  LOAD_FAST                'mod'
              110  CALL_FUNCTION_1       1  '1 positional, 0 named'
              113  GET_ITER         
              114  FOR_ITER            163  'to 163'
              117  STORE_FAST               'cname'

 L.  60       120  LOAD_GLOBAL              getattr
              123  LOAD_FAST                'mod'
              126  LOAD_FAST                'cname'
              129  CALL_FUNCTION_2       2  '2 positional, 0 named'
              132  LOAD_ATTR                __class__
              135  LOAD_GLOBAL              type
              138  COMPARE_OP               ==
              141  POP_JUMP_IF_FALSE   114  'to 114'

 L.  61       144  LOAD_GLOBAL              scanclass
              147  LOAD_FAST                'mod'
              150  LOAD_FAST                'modname'
              153  LOAD_FAST                'cname'
              156  CALL_FUNCTION_3       3  '3 positional, 0 named'
              159  POP_TOP          
            160_0  COME_FROM           141  '141'
              160  JUMP_BACK           114  'to 114'
              163  POP_BLOCK        
            164_0  COME_FROM_LOOP      101  '101'
              164  JUMP_BACK             7  'to 7'
              167  ELSE                     '186'

 L.  62       167  LOAD_FAST                'globalnames'
              170  LOAD_FAST                'modname'
              173  BINARY_SUBSCR    
              174  LOAD_ATTR                __class__
              177  LOAD_GLOBAL              type
              180  COMPARE_OP               ==
            183_0  COME_FROM            63  '63'
              183  POP_JUMP_IF_FALSE     7  'to 7'
            186_0  COME_FROM           183  '183'

 L.  63       186  JUMP_BACK             7  'to 7'
              189  POP_BLOCK        
            190_0  COME_FROM_LOOP        0  '0'

Parse error at or near `COME_FROM' instruction at offset 183_0