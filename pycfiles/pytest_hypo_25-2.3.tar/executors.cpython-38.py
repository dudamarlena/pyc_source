# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\executors.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 2036 bytes


def default_executor(function):
    raise NotImplementedError()


def setup_teardown_executor(setup, teardown):
    setup = setup or (lambda : None)
    teardown = teardown or (lambda ex: None)

    def execute--- This code section failed: ---

 L.  26         0  LOAD_CONST               None
                2  STORE_FAST               'token'

 L.  27         4  SETUP_FINALLY        22  'to 22'

 L.  28         6  LOAD_DEREF               'setup'
                8  CALL_FUNCTION_0       0  ''
               10  STORE_FAST               'token'

 L.  29        12  LOAD_FAST                'function'
               14  CALL_FUNCTION_0       0  ''
               16  POP_BLOCK        
               18  CALL_FINALLY         22  'to 22'
               20  RETURN_VALUE     
             22_0  COME_FROM            18  '18'
             22_1  COME_FROM_FINALLY     4  '4'

 L.  31        22  LOAD_DEREF               'teardown'
               24  LOAD_FAST                'token'
               26  CALL_FUNCTION_1       1  ''
               28  POP_TOP          
               30  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 18

    return execute


def executor--- This code section failed: ---

 L.  37         0  SETUP_FINALLY        10  'to 10'

 L.  38         2  LOAD_FAST                'runner'
                4  LOAD_ATTR                execute_example
                6  POP_BLOCK        
                8  RETURN_VALUE     
             10_0  COME_FROM_FINALLY     0  '0'

 L.  39        10  DUP_TOP          
               12  LOAD_GLOBAL              AttributeError
               14  COMPARE_OP               exception-match
               16  POP_JUMP_IF_FALSE    28  'to 28'
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L.  40        24  POP_EXCEPT       
               26  JUMP_FORWARD         30  'to 30'
             28_0  COME_FROM            16  '16'
               28  END_FINALLY      
             30_0  COME_FROM            26  '26'

 L.  42        30  LOAD_GLOBAL              hasattr
               32  LOAD_FAST                'runner'
               34  LOAD_STR                 'setup_example'
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_TRUE     50  'to 50'
               40  LOAD_GLOBAL              hasattr
               42  LOAD_FAST                'runner'
               44  LOAD_STR                 'teardown_example'
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_FALSE    76  'to 76'
             50_0  COME_FROM            38  '38'

 L.  43        50  LOAD_GLOBAL              setup_teardown_executor

 L.  44        52  LOAD_GLOBAL              getattr
               54  LOAD_FAST                'runner'
               56  LOAD_STR                 'setup_example'
               58  LOAD_CONST               None
               60  CALL_FUNCTION_3       3  ''

 L.  45        62  LOAD_GLOBAL              getattr
               64  LOAD_FAST                'runner'
               66  LOAD_STR                 'teardown_example'
               68  LOAD_CONST               None
               70  CALL_FUNCTION_3       3  ''

 L.  43        72  CALL_FUNCTION_2       2  ''
               74  RETURN_VALUE     
             76_0  COME_FROM            48  '48'

 L.  48        76  LOAD_GLOBAL              default_executor
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 20


def default_new_style_executor(data, function):
    return function(data)


class ConjectureRunner:

    def hypothesis_execute_example_with_data(self, data, function):
        return function(data)


def new_style_executor(runner):
    if runner is None:
        return default_new_style_executor
    if isinstance(runner, ConjectureRunner):
        return runner.hypothesis_execute_example_with_data
    old_school = executor(runner)
    if old_school is default_executor:
        return default_new_style_executor
    return lambda data, function: old_school(lambda : function(data))