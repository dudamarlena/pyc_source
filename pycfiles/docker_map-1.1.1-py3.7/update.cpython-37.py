# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/map/action/update.py
# Compiled at: 2020-04-02 07:00:31
# Size of source mod 2**32: 7021 bytes
from __future__ import unicode_literals
import logging, six
from ..input import ItemType
from ..state import State, StateFlags
from . import ItemAction, Action, ContainerUtilAction, VolumeUtilAction, NetworkUtilAction, ImageAction, DerivedAction
from .base import AbstractActionGenerator
log = logging.getLogger(__name__)

class UpdateActionGenerator(AbstractActionGenerator):
    pull_before_update = False
    pull_insecure_registry = False
    policy_options = ['pull_before_update', 'pull_insecure_registry']

    def get_state_actions--- This code section failed: ---

 L.  37         0  LOAD_FAST                'state'
                2  LOAD_ATTR                config_id
                4  STORE_FAST               'config_id'

 L.  38         6  LOAD_FAST                'config_id'
                8  LOAD_ATTR                config_type
               10  STORE_FAST               'config_type'

 L.  39        12  LOAD_FAST                'config_type'
               14  LOAD_GLOBAL              ItemType
               16  LOAD_ATTR                NETWORK
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE   184  'to 184'

 L.  40        22  LOAD_FAST                'state'
               24  LOAD_ATTR                base_state
               26  LOAD_GLOBAL              State
               28  LOAD_ATTR                ABSENT
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.  41        34  LOAD_GLOBAL              log
               36  LOAD_METHOD              debug
               38  LOAD_STR                 'Not found - creating network %s.'
               40  LOAD_FAST                'config_id'
               42  CALL_METHOD_2         2  '2 positional arguments'
               44  POP_TOP          

 L.  42        46  LOAD_GLOBAL              ItemAction
               48  LOAD_FAST                'state'
               50  LOAD_GLOBAL              Action
               52  LOAD_ATTR                CREATE
               54  CALL_FUNCTION_2       2  '2 positional arguments'
               56  BUILD_LIST_1          1 
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'

 L.  43        60  LOAD_FAST                'state'
               62  LOAD_ATTR                state_flags
               64  LOAD_GLOBAL              StateFlags
               66  LOAD_ATTR                NEEDS_RESET
               68  BINARY_AND       
               70  POP_JUMP_IF_FALSE   180  'to 180'

 L.  44        72  LOAD_GLOBAL              log
               74  LOAD_METHOD              debug
               76  LOAD_STR                 'Found to be outdated - resetting %s.'
               78  LOAD_FAST                'config_id'
               80  CALL_METHOD_2         2  '2 positional arguments'
               82  POP_TOP          

 L.  45        84  LOAD_FAST                'state'
               86  LOAD_ATTR                extra_data
               88  LOAD_METHOD              get
               90  LOAD_STR                 'containers'
               92  CALL_METHOD_1         1  '1 positional argument'
               94  STORE_FAST               'connected_containers'

 L.  46        96  LOAD_FAST                'connected_containers'
               98  POP_JUMP_IF_FALSE   154  'to 154'

 L.  47       100  LOAD_LISTCOMP            '<code_object <listcomp>>'
              102  LOAD_STR                 'UpdateActionGenerator.get_state_actions.<locals>.<listcomp>'
              104  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              106  LOAD_GLOBAL              six
              108  LOAD_METHOD              iteritems
              110  LOAD_FAST                'connected_containers'
              112  CALL_METHOD_1         1  '1 positional argument'
              114  GET_ITER         
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  STORE_FAST               'cc_names'

 L.  48       120  LOAD_GLOBAL              log
              122  LOAD_METHOD              debug
              124  LOAD_STR                 'Disconnecting containers from %s: %s.'
              126  LOAD_FAST                'config_id'
              128  LOAD_FAST                'cc_names'
              130  CALL_METHOD_3         3  '3 positional arguments'
              132  POP_TOP          

 L.  49       134  LOAD_GLOBAL              ItemAction
              136  LOAD_FAST                'state'
              138  LOAD_GLOBAL              NetworkUtilAction
              140  LOAD_ATTR                DISCONNECT_ALL
              142  LOAD_FAST                'cc_names'
              144  LOAD_CONST               ('containers',)
              146  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              148  BUILD_LIST_1          1 
              150  STORE_FAST               'actions'
              152  JUMP_FORWARD        158  'to 158'
            154_0  COME_FROM            98  '98'

 L.  51       154  BUILD_LIST_0          0 
              156  STORE_FAST               'actions'
            158_0  COME_FROM           152  '152'

 L.  52       158  LOAD_FAST                'actions'
              160  LOAD_METHOD              append
              162  LOAD_GLOBAL              ItemAction
              164  LOAD_FAST                'state'
              166  LOAD_GLOBAL              DerivedAction
              168  LOAD_ATTR                RESET_NETWORK
              170  CALL_FUNCTION_2       2  '2 positional arguments'
              172  CALL_METHOD_1         1  '1 positional argument'
              174  POP_TOP          

 L.  53       176  LOAD_FAST                'actions'
              178  RETURN_VALUE     
            180_0  COME_FROM            70  '70'
          180_182  JUMP_FORWARD        982  'to 982'
            184_0  COME_FROM            20  '20'

 L.  54       184  LOAD_FAST                'config_type'
              186  LOAD_GLOBAL              ItemType
              188  LOAD_ATTR                IMAGE
              190  COMPARE_OP               ==
          192_194  POP_JUMP_IF_FALSE   256  'to 256'

 L.  55       196  BUILD_MAP_0           0 
              198  STORE_FAST               'pull_kwargs'

 L.  56       200  LOAD_FAST                'self'
              202  LOAD_ATTR                pull_insecure_registry
              204  POP_JUMP_IF_FALSE   216  'to 216'

 L.  57       206  LOAD_FAST                'self'
              208  LOAD_ATTR                pull_insecure_registry
              210  LOAD_FAST                'pull_kwargs'
              212  LOAD_STR                 'insecure_registry'
              214  STORE_SUBSCR     
            216_0  COME_FROM           204  '204'

 L.  58       216  LOAD_FAST                'state'
              218  LOAD_ATTR                base_state
              220  LOAD_GLOBAL              State
              222  LOAD_ATTR                ABSENT
              224  COMPARE_OP               ==
              226  POP_JUMP_IF_TRUE    234  'to 234'
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                pull_before_update
              232  POP_JUMP_IF_FALSE   252  'to 252'
            234_0  COME_FROM           226  '226'

 L.  59       234  LOAD_GLOBAL              ItemAction
              236  LOAD_FAST                'state'
              238  LOAD_GLOBAL              ImageAction
              240  LOAD_ATTR                PULL
              242  BUILD_TUPLE_2         2 
              244  LOAD_FAST                'pull_kwargs'
              246  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              248  BUILD_LIST_1          1 
              250  RETURN_VALUE     
            252_0  COME_FROM           232  '232'
          252_254  JUMP_FORWARD        982  'to 982'
            256_0  COME_FROM           192  '192'

 L.  60       256  LOAD_FAST                'config_type'
              258  LOAD_GLOBAL              ItemType
              260  LOAD_ATTR                VOLUME
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   396  'to 396'

 L.  61       268  LOAD_FAST                'state'
              270  LOAD_ATTR                base_state
              272  LOAD_GLOBAL              State
              274  LOAD_ATTR                ABSENT
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   302  'to 302'

 L.  62       282  LOAD_GLOBAL              log
              284  LOAD_METHOD              debug
              286  LOAD_STR                 'Not found - creating attached volume %s.'
              288  LOAD_FAST                'config_id'
              290  CALL_METHOD_2         2  '2 positional arguments'
              292  POP_TOP          

 L.  63       294  LOAD_GLOBAL              Action
              296  LOAD_ATTR                CREATE
              298  STORE_FAST               'action_type'
              300  JUMP_FORWARD        374  'to 374'
            302_0  COME_FROM           278  '278'

 L.  64       302  LOAD_FAST                'state'
              304  LOAD_ATTR                state_flags
              306  LOAD_GLOBAL              StateFlags
              308  LOAD_ATTR                NEEDS_RESET
              310  BINARY_AND       
          312_314  POP_JUMP_IF_FALSE   336  'to 336'

 L.  65       316  LOAD_GLOBAL              log
              318  LOAD_METHOD              debug
              320  LOAD_STR                 'Found to be outdated or non-recoverable - resetting %s.'
              322  LOAD_FAST                'config_id'
              324  CALL_METHOD_2         2  '2 positional arguments'
              326  POP_TOP          

 L.  66       328  LOAD_GLOBAL              DerivedAction
              330  LOAD_ATTR                RESET_VOLUME
              332  STORE_FAST               'action_type'
              334  JUMP_FORWARD        374  'to 374'
            336_0  COME_FROM           312  '312'

 L.  67       336  LOAD_FAST                'state'
              338  LOAD_ATTR                state_flags
              340  LOAD_GLOBAL              StateFlags
              342  LOAD_ATTR                INITIAL
              344  BINARY_AND       
          346_348  POP_JUMP_IF_FALSE   370  'to 370'

 L.  68       350  LOAD_GLOBAL              log
              352  LOAD_METHOD              debug
              354  LOAD_STR                 'Container for attached volume found but initial, starting %s.'
              356  LOAD_FAST                'config_id'
              358  CALL_METHOD_2         2  '2 positional arguments'
              360  POP_TOP          

 L.  69       362  LOAD_GLOBAL              Action
              364  LOAD_ATTR                START
              366  STORE_FAST               'action_type'
              368  JUMP_FORWARD        374  'to 374'
            370_0  COME_FROM           346  '346'

 L.  71       370  LOAD_CONST               None
              372  RETURN_VALUE     
            374_0  COME_FROM           368  '368'
            374_1  COME_FROM           334  '334'
            374_2  COME_FROM           300  '300'

 L.  73       374  LOAD_GLOBAL              ItemAction
              376  LOAD_FAST                'state'
              378  LOAD_FAST                'action_type'
              380  CALL_FUNCTION_2       2  '2 positional arguments'

 L.  74       382  LOAD_GLOBAL              ItemAction
              384  LOAD_FAST                'state'
              386  LOAD_GLOBAL              VolumeUtilAction
              388  LOAD_ATTR                PREPARE
              390  CALL_FUNCTION_2       2  '2 positional arguments'
              392  BUILD_LIST_2          2 
              394  RETURN_VALUE     
            396_0  COME_FROM           264  '264'

 L.  76       396  LOAD_FAST                'config_type'
              398  LOAD_GLOBAL              ItemType
              400  LOAD_ATTR                CONTAINER
              402  COMPARE_OP               ==
          404_406  POP_JUMP_IF_FALSE   982  'to 982'

 L.  77       408  LOAD_FAST                'state'
              410  LOAD_ATTR                state_flags
              412  LOAD_GLOBAL              StateFlags
              414  LOAD_ATTR                INITIAL
              416  BINARY_AND       
              418  STORE_FAST               'ci_initial'

 L.  78       420  LOAD_FAST                'state'
              422  LOAD_ATTR                base_state
              424  LOAD_GLOBAL              State
              426  LOAD_ATTR                ABSENT
              428  COMPARE_OP               ==
          430_432  POP_JUMP_IF_FALSE   456  'to 456'

 L.  79       434  LOAD_GLOBAL              log
              436  LOAD_METHOD              debug
              438  LOAD_STR                 'Not found - creating and starting instance container %s.'
              440  LOAD_FAST                'config_id'
              442  CALL_METHOD_2         2  '2 positional arguments'
              444  POP_TOP          

 L.  80       446  LOAD_GLOBAL              DerivedAction
              448  LOAD_ATTR                STARTUP_CONTAINER
              450  STORE_FAST               'action_type'
          452_454  JUMP_FORWARD        960  'to 960'
            456_0  COME_FROM           430  '430'

 L.  81       456  LOAD_FAST                'state'
              458  LOAD_ATTR                state_flags
              460  LOAD_GLOBAL              StateFlags
              462  LOAD_ATTR                NEEDS_RESET
              464  BINARY_AND       
          466_468  POP_JUMP_IF_FALSE   540  'to 540'

 L.  82       470  LOAD_FAST                'state'
              472  LOAD_ATTR                base_state
              474  LOAD_GLOBAL              State
              476  LOAD_ATTR                RUNNING
              478  COMPARE_OP               ==
          480_482  POP_JUMP_IF_TRUE    498  'to 498'
              484  LOAD_FAST                'state'
              486  LOAD_ATTR                state_flags
              488  LOAD_GLOBAL              StateFlags
              490  LOAD_ATTR                RESTARTING
              492  BINARY_AND       
          494_496  POP_JUMP_IF_FALSE   518  'to 518'
            498_0  COME_FROM           480  '480'

 L.  83       498  LOAD_GLOBAL              log
              500  LOAD_METHOD              debug
              502  LOAD_STR                 'Found to be outdated or non-recoverable - resetting %s.'
              504  LOAD_FAST                'config_id'
              506  CALL_METHOD_2         2  '2 positional arguments'
              508  POP_TOP          

 L.  84       510  LOAD_GLOBAL              DerivedAction
              512  LOAD_ATTR                RESET_CONTAINER
              514  STORE_FAST               'action_type'
              516  JUMP_FORWARD        960  'to 960'
            518_0  COME_FROM           494  '494'

 L.  86       518  LOAD_GLOBAL              log
              520  LOAD_METHOD              debug
              522  LOAD_STR                 'Found to be outdated or non-recoverable - relaunching %s.'
              524  LOAD_FAST                'config_id'
              526  CALL_METHOD_2         2  '2 positional arguments'
              528  POP_TOP          

 L.  87       530  LOAD_GLOBAL              DerivedAction
              532  LOAD_ATTR                RELAUNCH_CONTAINER
              534  STORE_FAST               'action_type'
          536_538  JUMP_FORWARD        960  'to 960'
            540_0  COME_FROM           466  '466'

 L.  89       540  BUILD_LIST_0          0 
              542  STORE_FAST               'actions'

 L.  90       544  LOAD_FAST                'state'
              546  LOAD_ATTR                state_flags
              548  LOAD_GLOBAL              StateFlags
              550  LOAD_ATTR                NETWORK_DISCONNECTED
              552  BINARY_AND       
          554_556  POP_JUMP_IF_FALSE   602  'to 602'

 L.  91       558  LOAD_FAST                'state'
              560  LOAD_ATTR                extra_data
              562  LOAD_STR                 'disconnected'
              564  BINARY_SUBSCR    
              566  STORE_FAST               'dn'

 L.  92       568  LOAD_GLOBAL              log
              570  LOAD_METHOD              debug
              572  LOAD_STR                 'Container is connecting to the following networks: %s.'
              574  LOAD_FAST                'dn'
              576  CALL_METHOD_2         2  '2 positional arguments'
              578  POP_TOP          

 L.  93       580  LOAD_FAST                'actions'
              582  LOAD_METHOD              append
              584  LOAD_GLOBAL              ItemAction
              586  LOAD_FAST                'state'
              588  LOAD_GLOBAL              Action
              590  LOAD_ATTR                CONNECT
              592  LOAD_FAST                'dn'
              594  LOAD_CONST               ('endpoints',)
              596  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              598  CALL_METHOD_1         1  '1 positional argument'
              600  POP_TOP          
            602_0  COME_FROM           554  '554'

 L.  94       602  LOAD_FAST                'state'
              604  LOAD_ATTR                state_flags
              606  LOAD_GLOBAL              StateFlags
              608  LOAD_ATTR                NETWORK_MISMATCH
              610  BINARY_AND       
          612_614  POP_JUMP_IF_FALSE   688  'to 688'

 L.  95       616  LOAD_FAST                'state'
              618  LOAD_ATTR                extra_data
              620  LOAD_STR                 'reconnect'
              622  BINARY_SUBSCR    
              624  STORE_FAST               'rn'

 L.  96       626  LOAD_GLOBAL              zip
              628  LOAD_FAST                'rn'
              630  CALL_FUNCTION_EX      0  'positional arguments only'
              632  UNPACK_SEQUENCE_2     2 
              634  STORE_FAST               'n_names'
              636  STORE_FAST               'n_ep'

 L.  97       638  LOAD_GLOBAL              log
              640  LOAD_METHOD              debug
              642  LOAD_STR                 'Container is reconnecting to the following networks: %s.'
              644  LOAD_FAST                'n_names'
              646  CALL_METHOD_2         2  '2 positional arguments'
              648  POP_TOP          

 L.  98       650  LOAD_FAST                'actions'
              652  LOAD_METHOD              extend

 L.  99       654  LOAD_GLOBAL              ItemAction
              656  LOAD_FAST                'state'
              658  LOAD_GLOBAL              Action
              660  LOAD_ATTR                DISCONNECT
              662  LOAD_FAST                'n_names'
              664  LOAD_CONST               ('networks',)
              666  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 100       668  LOAD_GLOBAL              ItemAction
              670  LOAD_FAST                'state'
              672  LOAD_GLOBAL              Action
              674  LOAD_ATTR                CONNECT
              676  LOAD_FAST                'n_ep'
              678  LOAD_CONST               ('endpoints',)
              680  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              682  BUILD_LIST_2          2 
              684  CALL_METHOD_1         1  '1 positional argument'
              686  POP_TOP          
            688_0  COME_FROM           612  '612'

 L. 102       688  LOAD_FAST                'state'
              690  LOAD_ATTR                state_flags
              692  LOAD_GLOBAL              StateFlags
              694  LOAD_ATTR                NETWORK_LEFT
              696  BINARY_AND       
          698_700  POP_JUMP_IF_FALSE   746  'to 746'

 L. 103       702  LOAD_FAST                'state'
              704  LOAD_ATTR                extra_data
              706  LOAD_STR                 'left'
              708  BINARY_SUBSCR    
              710  STORE_FAST               'ln'

 L. 104       712  LOAD_GLOBAL              log
              714  LOAD_METHOD              debug
              716  LOAD_STR                 'Container is disconnecting from the following networks: %s.'
              718  LOAD_FAST                'ln'
              720  CALL_METHOD_2         2  '2 positional arguments'
              722  POP_TOP          

 L. 105       724  LOAD_FAST                'actions'
              726  LOAD_METHOD              append
              728  LOAD_GLOBAL              ItemAction
              730  LOAD_FAST                'state'
              732  LOAD_GLOBAL              Action
              734  LOAD_ATTR                DISCONNECT
              736  LOAD_FAST                'ln'
              738  LOAD_CONST               ('networks',)
              740  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              742  CALL_METHOD_1         1  '1 positional argument'
              744  POP_TOP          
            746_0  COME_FROM           698  '698'

 L. 106       746  LOAD_FAST                'state'
              748  LOAD_ATTR                base_state
              750  LOAD_GLOBAL              State
              752  LOAD_ATTR                RUNNING
              754  COMPARE_OP               !=
          756_758  POP_JUMP_IF_FALSE   824  'to 824'

 L. 107       760  LOAD_FAST                'ci_initial'
          762_764  POP_JUMP_IF_TRUE    780  'to 780'
              766  LOAD_FAST                'state'
              768  LOAD_ATTR                state_flags
              770  LOAD_GLOBAL              StateFlags
              772  LOAD_ATTR                PERSISTENT
              774  BINARY_AND       
          776_778  POP_JUMP_IF_TRUE    824  'to 824'
            780_0  COME_FROM           762  '762'

 L. 108       780  LOAD_GLOBAL              log
              782  LOAD_METHOD              debug
              784  LOAD_STR                 'Container found but not running, starting %s.'
              786  LOAD_FAST                'config_id'
              788  CALL_METHOD_2         2  '2 positional arguments'
              790  POP_TOP          

 L. 109       792  LOAD_FAST                'actions'
              794  LOAD_METHOD              extend

 L. 110       796  LOAD_GLOBAL              ItemAction
              798  LOAD_FAST                'state'
              800  LOAD_GLOBAL              Action
              802  LOAD_ATTR                START
              804  CALL_FUNCTION_2       2  '2 positional arguments'

 L. 111       806  LOAD_GLOBAL              ItemAction
              808  LOAD_FAST                'state'
              810  LOAD_GLOBAL              ContainerUtilAction
              812  LOAD_ATTR                EXEC_ALL
              814  CALL_FUNCTION_2       2  '2 positional arguments'
              816  BUILD_LIST_2          2 
              818  CALL_METHOD_1         1  '1 positional argument'
              820  POP_TOP          
              822  JUMP_FORWARD        956  'to 956'
            824_0  COME_FROM           776  '776'
            824_1  COME_FROM           756  '756'

 L. 114       824  LOAD_FAST                'state'
              826  LOAD_ATTR                state_flags
              828  LOAD_GLOBAL              StateFlags
              830  LOAD_ATTR                HOST_CONFIG_UPDATE
              832  BINARY_AND       
          834_836  POP_JUMP_IF_FALSE   890  'to 890'

 L. 115       838  LOAD_FAST                'state'
              840  LOAD_ATTR                extra_data
              842  LOAD_STR                 'update_container'
              844  BINARY_SUBSCR    
              846  STORE_FAST               'update_args'

 L. 116       848  LOAD_FAST                'update_args'
          850_852  POP_JUMP_IF_FALSE   890  'to 890'

 L. 117       854  LOAD_GLOBAL              log
              856  LOAD_METHOD              debug
              858  LOAD_STR                 'Container %s with updated host config: %s.'
              860  LOAD_FAST                'config_id'
              862  LOAD_FAST                'update_args'
              864  CALL_METHOD_3         3  '3 positional arguments'
              866  POP_TOP          

 L. 118       868  LOAD_FAST                'actions'
              870  LOAD_METHOD              append
              872  LOAD_GLOBAL              ItemAction
              874  LOAD_FAST                'state'
              876  LOAD_GLOBAL              Action
              878  LOAD_ATTR                UPDATE
              880  LOAD_FAST                'update_args'
              882  LOAD_CONST               ('update_values',)
              884  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              886  CALL_METHOD_1         1  '1 positional argument'
              888  POP_TOP          
            890_0  COME_FROM           850  '850'
            890_1  COME_FROM           834  '834'

 L. 119       890  LOAD_FAST                'state'
              892  LOAD_ATTR                state_flags
              894  LOAD_GLOBAL              StateFlags
              896  LOAD_ATTR                EXEC_COMMANDS
              898  BINARY_AND       
          900_902  POP_JUMP_IF_FALSE   956  'to 956'

 L. 120       904  LOAD_FAST                'state'
              906  LOAD_ATTR                extra_data
              908  LOAD_STR                 'exec_commands'
              910  BINARY_SUBSCR    
              912  STORE_FAST               'run_cmds'

 L. 121       914  LOAD_FAST                'run_cmds'
          916_918  POP_JUMP_IF_FALSE   956  'to 956'

 L. 122       920  LOAD_GLOBAL              log
              922  LOAD_METHOD              debug
              924  LOAD_STR                 'Container %s up-to-date, but with missing commands %s.'
              926  LOAD_FAST                'config_id'
              928  LOAD_FAST                'run_cmds'
              930  CALL_METHOD_3         3  '3 positional arguments'
              932  POP_TOP          

 L. 123       934  LOAD_FAST                'actions'
              936  LOAD_METHOD              append
            938_0  COME_FROM           516  '516'
              938  LOAD_GLOBAL              ItemAction
              940  LOAD_FAST                'state'
              942  LOAD_GLOBAL              ContainerUtilAction
              944  LOAD_ATTR                EXEC_COMMANDS
              946  LOAD_FAST                'run_cmds'
              948  LOAD_CONST               ('run_cmds',)
              950  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              952  CALL_METHOD_1         1  '1 positional argument'
              954  POP_TOP          
            956_0  COME_FROM           916  '916'
            956_1  COME_FROM           900  '900'
            956_2  COME_FROM           822  '822'

 L. 124       956  LOAD_FAST                'actions'
              958  RETURN_VALUE     
            960_0  COME_FROM           536  '536'
            960_1  COME_FROM           452  '452'

 L. 126       960  LOAD_GLOBAL              ItemAction
              962  LOAD_FAST                'state'
              964  LOAD_FAST                'action_type'
              966  CALL_FUNCTION_2       2  '2 positional arguments'

 L. 127       968  LOAD_GLOBAL              ItemAction
              970  LOAD_FAST                'state'
              972  LOAD_GLOBAL              ContainerUtilAction
              974  LOAD_ATTR                EXEC_ALL
              976  CALL_FUNCTION_2       2  '2 positional arguments'
              978  BUILD_LIST_2          2 
              980  RETURN_VALUE     
            982_0  COME_FROM           404  '404'
            982_1  COME_FROM           252  '252'
            982_2  COME_FROM           180  '180'

Parse error at or near `COME_FROM' instruction at offset 938_0