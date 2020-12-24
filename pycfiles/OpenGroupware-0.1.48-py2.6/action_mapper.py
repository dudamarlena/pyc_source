# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/action_mapper.py
# Compiled at: 2012-10-12 07:02:39
import glob, inspect, logging
from coils.foundation import Backend, ServerDefaultsManager
from coils.core import ActionCommand, MacroCommand

class ActionMapper:

    @staticmethod
    def list_commands():
        if not hasattr(ActionMapper, '_action_dict'):
            ActionMapper.log = logging.getLogger('actions')
            ActionMapper.load_actions()
        return ActionMapper._action_dict.keys()

    @staticmethod
    def list_macros():
        if not hasattr(ActionMapper, '_macro_dict'):
            ActionMapper.log = logging.getLogger('actions')
            ActionMapper.load_actions()
        return ActionMapper._macro_dict.keys()

    @staticmethod
    def scan_bundle--- This code section failed: ---

 L.  44         0  LOAD_GLOBAL           0  'ServerDefaultsManager'
                3  CALL_FUNCTION_0       0  None
                6  STORE_FAST            1  'sd'

 L.  45         9  SETUP_LOOP          269  'to 281'
               12  LOAD_GLOBAL           1  'inspect'
               15  LOAD_ATTR             2  'getmembers'
               18  LOAD_FAST             0  'bundle'
               21  LOAD_GLOBAL           1  'inspect'
               24  LOAD_ATTR             3  'isclass'
               27  CALL_FUNCTION_2       2  None
               30  GET_ITER         
               31  FOR_ITER            246  'to 280'
               34  UNPACK_SEQUENCE_2     2 
               37  STORE_FAST            2  'name'
               40  STORE_FAST            3  'data'

 L.  47        43  LOAD_FAST             3  'data'
               46  LOAD_ATTR             4  '__module__'
               49  LOAD_GLOBAL           5  'len'
               52  LOAD_FAST             0  'bundle'
               55  LOAD_ATTR             6  '__name__'
               58  CALL_FUNCTION_1       1  None
               61  SLICE+2          
               62  LOAD_FAST             0  'bundle'
               65  LOAD_ATTR             6  '__name__'
               68  COMPARE_OP            2  ==
               71  JUMP_IF_FALSE       202  'to 276'
               74  POP_TOP          

 L.  48        75  LOAD_GLOBAL           7  'issubclass'
               78  LOAD_FAST             3  'data'
               81  LOAD_GLOBAL           8  'ActionCommand'
               84  CALL_FUNCTION_2       2  None
               87  JUMP_IF_FALSE       104  'to 194'
               90  POP_TOP          

 L.  49        91  LOAD_GLOBAL           9  'hasattr'
               94  LOAD_FAST             3  'data'
               97  LOAD_CONST               '__aliases__'
              100  CALL_FUNCTION_2       2  None
              103  JUMP_IF_FALSE        59  'to 165'
              106  POP_TOP          

 L.  50       107  LOAD_CONST               '%s::%s'
              110  LOAD_FAST             3  'data'
              113  LOAD_ATTR            10  '__domain__'
              116  LOAD_FAST             3  'data'
              119  LOAD_ATTR            11  '__operation__'
              122  BUILD_TUPLE_2         2 
              125  BINARY_MODULO    
              126  STORE_FAST            4  'command'

 L.  52       129  SETUP_LOOP           59  'to 191'
              132  LOAD_FAST             3  'data'
              135  LOAD_ATTR            12  '__aliases__'
              138  GET_ITER         
              139  FOR_ITER             19  'to 161'
              142  STORE_FAST            5  'alias'

 L.  54       145  LOAD_FAST             4  'command'
              148  LOAD_GLOBAL          13  'ActionMapper'
              151  LOAD_ATTR            14  '_action_dict'
              154  LOAD_FAST             5  'alias'
              157  STORE_SUBSCR     
              158  JUMP_BACK           139  'to 139'
              161  POP_BLOCK        
              162  JUMP_ABSOLUTE       273  'to 273'
            165_0  COME_FROM           103  '103'
              165  POP_TOP          

 L.  56       166  LOAD_GLOBAL          13  'ActionMapper'
              169  LOAD_ATTR            15  'log'
              172  LOAD_ATTR            16  'warn'
              175  LOAD_CONST               'Found ActionCommand {0} with no aliases.'
              178  LOAD_ATTR            17  'format'
              181  LOAD_FAST             3  'data'
              184  CALL_FUNCTION_1       1  None
              187  CALL_FUNCTION_1       1  None
              190  POP_TOP          
            191_0  COME_FROM           129  '129'
              191  JUMP_ABSOLUTE       277  'to 277'
            194_0  COME_FROM            87  '87'
              194  POP_TOP          

 L.  57       195  LOAD_GLOBAL           7  'issubclass'
              198  LOAD_FAST             3  'data'
              201  LOAD_GLOBAL          18  'MacroCommand'
              204  CALL_FUNCTION_2       2  None
              207  JUMP_IF_FALSE        62  'to 272'
              210  POP_TOP          

 L.  58       211  LOAD_GLOBAL           9  'hasattr'
              214  LOAD_FAST             3  'data'
              217  LOAD_CONST               '__operation__'
              220  CALL_FUNCTION_2       2  None
              223  JUMP_IF_FALSE        42  'to 268'
              226  POP_TOP          

 L.  59       227  LOAD_CONST               '%s::%s'
              230  LOAD_FAST             3  'data'
              233  LOAD_ATTR            10  '__domain__'
              236  LOAD_FAST             3  'data'
              239  LOAD_ATTR            11  '__operation__'
              242  BUILD_TUPLE_2         2 
              245  BINARY_MODULO    
              246  STORE_FAST            4  'command'

 L.  61       249  LOAD_FAST             4  'command'
              252  LOAD_GLOBAL          13  'ActionMapper'
              255  LOAD_ATTR            19  '_macro_dict'
              258  LOAD_FAST             3  'data'
              261  LOAD_ATTR            11  '__operation__'
              264  STORE_SUBSCR     
              265  JUMP_ABSOLUTE       273  'to 273'
            268_0  COME_FROM           223  '223'
              268  POP_TOP          
              269  JUMP_ABSOLUTE       277  'to 277'
            272_0  COME_FROM           207  '207'
              272  POP_TOP          
              273  JUMP_BACK            31  'to 31'
            276_0  COME_FROM            71  '71'
              276  POP_TOP          
              277  JUMP_BACK            31  'to 31'
              280  POP_BLOCK        
            281_0  COME_FROM             9  '9'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 191

    @staticmethod
    def load_actions():
        ActionMapper._action_dict = {}
        ActionMapper._macro_dict = {}
        for bundle_name in Backend.get_logic_bundle_names():
            bundle = None
            try:
                bundle = __import__(bundle_name, fromlist=['*'])
            except:
                ActionMapper.log.debug(('Failed to import bundle {0}').format(bundle_name))
            else:
                ActionMapper.scan_bundle(bundle)

        msg = 'Loaded actions:'
        for k in ActionMapper._action_dict.keys():
            msg = '%s [%s=%s]' % (msg, k, ActionMapper._action_dict[k])

        msg = 'Loaded macros:'
        for k in ActionMapper._macro_dict.keys():
            msg = '%s [%s=%s]' % (msg, k, ActionMapper._macro_dict[k])

        return

    @staticmethod
    def get_action(name):
        if not hasattr(ActionMapper, '_action_dict'):
            ActionMapper.log = logging.getLogger('actions')
            ActionMapper.load_actions()
        if name in ActionMapper._action_dict:
            action = ActionMapper._action_dict.get(name, None)
            ActionMapper.log.debug(('Returning action {0} for alias {1}').format(action, name))
        else:
            action = None
            ActionMapper.log.warn(('No command has an alias of {0}').format(name))
        return action

    @staticmethod
    def get_macro(name):
        if not hasattr(ActionMapper, '_macro_dict'):
            ActionMapper.log = logging.getLogger('actions')
            ActionMapper.load_actions()
        if name in ActionMapper._macro_dict:
            action = ActionMapper._macro_dict.get(name, None)
            ActionMapper.log.debug(('Returning macro {0} for alias {1}').format(action, name))
        else:
            action = None
            ActionMapper.log.warn(('No command has an alias of {0}').format(name))
        return action