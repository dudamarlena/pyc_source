# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/bundlemanager.py
# Compiled at: 2012-10-12 07:02:39
import os, sys, glob, inspect, logging
from coils.foundation import Backend, ServerDefaultsManager
from entityaccessmanager import EntityAccessManager
from command import Command
from service import Service
from threadedservice import ThreadedService
from content_plugin import ContentPlugin

class BundleManager(object):
    __slots__ = ()
    _command_dict = None
    _service_dict = None
    _manager_dict = None
    _plugin_dict = None

    @staticmethod
    def scan_bundle--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL           0  'ServerDefaultsManager'
                3  CALL_FUNCTION_0       0  None
                6  STORE_FAST            1  'sd'

 L.  39         9  SETUP_LOOP          528  'to 540'
               12  LOAD_GLOBAL           1  'inspect'
               15  LOAD_ATTR             2  'getmembers'
               18  LOAD_FAST             0  'bundle'
               21  LOAD_GLOBAL           1  'inspect'
               24  LOAD_ATTR             3  'isclass'
               27  CALL_FUNCTION_2       2  None
               30  GET_ITER         
               31  FOR_ITER            505  'to 539'
               34  UNPACK_SEQUENCE_2     2 
               37  STORE_FAST            2  'name'
               40  STORE_FAST            3  'data'

 L.  41        43  LOAD_FAST             3  'data'
               46  LOAD_ATTR             4  '__module__'
               49  LOAD_GLOBAL           5  'len'
               52  LOAD_FAST             0  'bundle'
               55  LOAD_ATTR             6  '__name__'
               58  CALL_FUNCTION_1       1  None
               61  SLICE+2          
               62  LOAD_FAST             0  'bundle'
               65  LOAD_ATTR             6  '__name__'
               68  COMPARE_OP            2  ==
               71  JUMP_IF_FALSE       461  'to 535'
               74  POP_TOP          

 L.  42        75  LOAD_GLOBAL           7  'issubclass'
               78  LOAD_FAST             3  'data'
               81  LOAD_GLOBAL           8  'Command'
               84  CALL_FUNCTION_2       2  None
               87  JUMP_IF_FALSE        39  'to 129'
               90  POP_TOP          

 L.  46        91  LOAD_CONST               '%s::%s'
               94  LOAD_FAST             3  'data'
               97  LOAD_ATTR             9  '__domain__'
              100  LOAD_FAST             3  'data'
              103  LOAD_ATTR            10  '__operation__'
              106  BUILD_TUPLE_2         2 
              109  BINARY_MODULO    
              110  STORE_FAST            4  'x'

 L.  47       113  LOAD_FAST             3  'data'
              116  LOAD_GLOBAL          11  'BundleManager'
              119  LOAD_ATTR            12  '_command_dict'
              122  LOAD_FAST             4  'x'
              125  STORE_SUBSCR     
              126  JUMP_ABSOLUTE       536  'to 536'
            129_0  COME_FROM            87  '87'
              129  POP_TOP          

 L.  48       130  LOAD_GLOBAL           7  'issubclass'
              133  LOAD_FAST             3  'data'
              136  LOAD_GLOBAL          13  'Service'
              139  CALL_FUNCTION_2       2  None
              142  JUMP_IF_TRUE         16  'to 161'
              145  POP_TOP          
              146  LOAD_GLOBAL           7  'issubclass'
              149  LOAD_FAST             3  'data'
              152  LOAD_GLOBAL          14  'ThreadedService'
              155  CALL_FUNCTION_2       2  None
            158_0  COME_FROM           142  '142'
              158  JUMP_IF_FALSE        32  'to 193'
              161  POP_TOP          

 L.  52       162  LOAD_GLOBAL          15  'str'
              165  LOAD_FAST             3  'data'
              168  LOAD_ATTR            16  '__service__'
              171  CALL_FUNCTION_1       1  None
              174  STORE_FAST            4  'x'

 L.  53       177  LOAD_FAST             3  'data'
              180  LOAD_GLOBAL          11  'BundleManager'
              183  LOAD_ATTR            17  '_service_dict'
              186  LOAD_FAST             4  'x'
              189  STORE_SUBSCR     
              190  JUMP_ABSOLUTE       536  'to 536'
            193_0  COME_FROM           158  '158'
              193  POP_TOP          

 L.  54       194  LOAD_GLOBAL           7  'issubclass'
              197  LOAD_FAST             3  'data'
              200  LOAD_GLOBAL          18  'EntityAccessManager'
              203  CALL_FUNCTION_2       2  None
              206  JUMP_IF_FALSE       108  'to 317'
              209  POP_TOP          

 L.  58       210  LOAD_GLOBAL          19  'hasattr'
              213  LOAD_FAST             3  'data'
              216  LOAD_CONST               '__entity__'
              219  CALL_FUNCTION_2       2  None
              222  JUMP_IF_FALSE        88  'to 313'
              225  POP_TOP          

 L.  59       226  LOAD_GLOBAL          19  'hasattr'
              229  LOAD_FAST             3  'data'
              232  LOAD_ATTR            20  '__entity__'
              235  LOAD_CONST               '__iter__'
              238  CALL_FUNCTION_2       2  None
              241  JUMP_IF_FALSE        43  'to 287'
              244  POP_TOP          

 L.  60       245  SETUP_LOOP           62  'to 310'
              248  LOAD_FAST             3  'data'
              251  LOAD_ATTR            20  '__entity__'
              254  GET_ITER         
              255  FOR_ITER             25  'to 283'
              258  STORE_FAST            5  'entity'

 L.  61       261  LOAD_FAST             3  'data'
              264  LOAD_GLOBAL          11  'BundleManager'
              267  LOAD_ATTR            21  '_manager_dict'
              270  LOAD_FAST             5  'entity'
              273  LOAD_ATTR            22  'lower'
              276  CALL_FUNCTION_0       0  None
              279  STORE_SUBSCR     
              280  JUMP_BACK           255  'to 255'
              283  POP_BLOCK        
              284  JUMP_ABSOLUTE       314  'to 314'
            287_0  COME_FROM           241  '241'
              287  POP_TOP          

 L.  63       288  LOAD_FAST             3  'data'
              291  LOAD_GLOBAL          11  'BundleManager'
              294  LOAD_ATTR            21  '_manager_dict'
              297  LOAD_FAST             3  'data'
              300  LOAD_ATTR            20  '__entity__'
              303  LOAD_ATTR            22  'lower'
              306  CALL_FUNCTION_0       0  None
              309  STORE_SUBSCR     
            310_0  COME_FROM           245  '245'
              310  JUMP_ABSOLUTE       532  'to 532'
            313_0  COME_FROM           222  '222'
              313  POP_TOP          
              314  JUMP_ABSOLUTE       536  'to 536'
            317_0  COME_FROM           206  '206'
              317  POP_TOP          

 L.  64       318  LOAD_GLOBAL           7  'issubclass'
              321  LOAD_FAST             3  'data'
              324  LOAD_GLOBAL          23  'ContentPlugin'
              327  CALL_FUNCTION_2       2  None
              330  JUMP_IF_FALSE       198  'to 531'
              333  POP_TOP          

 L.  68       334  LOAD_GLOBAL          19  'hasattr'
              337  LOAD_FAST             3  'data'
              340  LOAD_ATTR            20  '__entity__'
              343  LOAD_CONST               '__iter__'
              346  CALL_FUNCTION_2       2  None
              349  JUMP_IF_FALSE        98  'to 450'
              352  POP_TOP          

 L.  70       353  SETUP_LOOP          172  'to 528'
              356  LOAD_FAST             3  'data'
              359  LOAD_ATTR            20  '__entity__'
              362  GET_ITER         
              363  FOR_ITER             80  'to 446'
              366  STORE_FAST            5  'entity'

 L.  71       369  LOAD_FAST             5  'entity'
              372  LOAD_ATTR            22  'lower'
              375  CALL_FUNCTION_0       0  None
              378  LOAD_GLOBAL          11  'BundleManager'
              381  LOAD_ATTR            24  '_plugin_dict'
              384  COMPARE_OP            6  in
              387  JUMP_IF_FALSE        30  'to 420'
              390  POP_TOP          

 L.  72       391  LOAD_GLOBAL          11  'BundleManager'
              394  LOAD_ATTR            24  '_plugin_dict'
              397  LOAD_FAST             5  'entity'
              400  LOAD_ATTR            22  'lower'
              403  CALL_FUNCTION_0       0  None
              406  BINARY_SUBSCR    
              407  LOAD_ATTR            25  'append'
              410  LOAD_FAST             3  'data'
              413  CALL_FUNCTION_1       1  None
              416  POP_TOP          
              417  JUMP_BACK           363  'to 363'
            420_0  COME_FROM           387  '387'
              420  POP_TOP          

 L.  74       421  LOAD_FAST             3  'data'
              424  BUILD_LIST_1          1 
              427  LOAD_GLOBAL          11  'BundleManager'
              430  LOAD_ATTR            24  '_plugin_dict'
              433  LOAD_FAST             5  'entity'
              436  LOAD_ATTR            22  'lower'
              439  CALL_FUNCTION_0       0  None
              442  STORE_SUBSCR     
              443  JUMP_BACK           363  'to 363'
              446  POP_BLOCK        
              447  JUMP_ABSOLUTE       532  'to 532'
            450_0  COME_FROM           349  '349'
              450  POP_TOP          

 L.  76       451  LOAD_FAST             3  'data'
              454  LOAD_ATTR            20  '__entity__'
              457  LOAD_ATTR            22  'lower'
              460  CALL_FUNCTION_0       0  None
              463  LOAD_GLOBAL          11  'BundleManager'
              466  LOAD_ATTR            24  '_plugin_dict'
              469  COMPARE_OP            6  in
              472  JUMP_IF_FALSE        30  'to 505'
              475  POP_TOP          

 L.  77       476  LOAD_GLOBAL          11  'BundleManager'
              479  LOAD_ATTR            24  '_plugin_dict'
              482  LOAD_FAST             5  'entity'
              485  LOAD_ATTR            22  'lower'
              488  CALL_FUNCTION_0       0  None
              491  BINARY_SUBSCR    
              492  LOAD_ATTR            25  'append'
              495  LOAD_FAST             3  'data'
              498  CALL_FUNCTION_1       1  None
              501  POP_TOP          
              502  JUMP_ABSOLUTE       532  'to 532'
            505_0  COME_FROM           472  '472'
              505  POP_TOP          

 L.  79       506  LOAD_FAST             3  'data'
              509  BUILD_LIST_1          1 
              512  LOAD_GLOBAL          11  'BundleManager'
              515  LOAD_ATTR            24  '_plugin_dict'
              518  LOAD_FAST             5  'entity'
              521  LOAD_ATTR            22  'lower'
              524  CALL_FUNCTION_0       0  None
              527  STORE_SUBSCR     
            528_0  COME_FROM           353  '353'
              528  JUMP_ABSOLUTE       536  'to 536'
            531_0  COME_FROM           330  '330'
              531  POP_TOP          
              532  JUMP_BACK            31  'to 31'
            535_0  COME_FROM            71  '71'
              535  POP_TOP          
              536  JUMP_BACK            31  'to 31'
              539  POP_BLOCK        
            540_0  COME_FROM             9  '9'

 L.  81       540  LOAD_GLOBAL          19  'hasattr'
              543  LOAD_FAST             0  'bundle'
              546  LOAD_CONST               'COILS_DEFAULT_DEFAULTS'
              549  CALL_FUNCTION_2       2  None
              552  JUMP_IF_FALSE        56  'to 611'
            555_0  THEN                     612
              555  POP_TOP          

 L.  82       556  LOAD_GLOBAL          26  'getattr'
              559  LOAD_FAST             0  'bundle'
              562  LOAD_CONST               'COILS_DEFAULT_DEFAULTS'
              565  CALL_FUNCTION_2       2  None
              568  STORE_FAST            4  'x'

 L.  83       571  SETUP_LOOP           38  'to 612'
              574  LOAD_FAST             4  'x'
              577  GET_ITER         
              578  FOR_ITER             26  'to 607'
              581  STORE_FAST            6  'key'

 L.  84       584  LOAD_FAST             1  'sd'
              587  LOAD_ATTR            27  'add_server_default'
              590  LOAD_FAST             6  'key'
              593  LOAD_FAST             4  'x'
              596  LOAD_FAST             6  'key'
              599  BINARY_SUBSCR    
              600  CALL_FUNCTION_2       2  None
              603  POP_TOP          
              604  JUMP_BACK           578  'to 578'
              607  POP_BLOCK        
              608  JUMP_FORWARD          1  'to 612'
            611_0  COME_FROM           552  '552'
              611  POP_TOP          
            612_0  COME_FROM           571  '571'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 310

    @staticmethod
    def load_bundles():
        BundleManager.log = logging.getLogger('bundle')
        BundleManager._command_dict = {}
        BundleManager._service_dict = {}
        BundleManager._manager_dict = {}
        BundleManager._plugin_dict = {}
        for bundle_name in Backend.get_logic_bundle_names():
            bundle = None
            try:
                bundle = __import__(bundle_name, fromlist=['*'])
                BundleManager.log.info(('Loaded bundle {0}').format(bundle_name))
            except:
                BundleManager.log.error(('Failed to load bundle {0}').format(bundle_name))
            else:
                BundleManager.scan_bundle(bundle)

        msg = 'Loaded commands:'
        for k in BundleManager._command_dict.keys():
            msg = '%s [%s=%s]' % (msg, k, BundleManager._command_dict[k])

        BundleManager.log.debug(msg)
        msg = 'Loaded services:'
        for k in BundleManager._service_dict.keys():
            msg = '%s [%s=%s]' % (msg, k, BundleManager._service_dict[k])

        BundleManager.log.debug(msg)
        msg = 'Loaded plugins:'
        for k in BundleManager._plugin_dict.keys():
            msg = '%s [%s=%s]' % (msg, k, BundleManager._plugin_dict[k])

        BundleManager.log.debug(msg)
        msg = 'Loaded managers:'
        for k in BundleManager._manager_dict:
            msg = '%s [%s=%s]' % (msg, k, BundleManager._manager_dict[k])

        BundleManager.log.debug(msg)
        return

    @staticmethod
    def list_commands():
        if BundleManager._command_dict is None:
            BundleManager.load_bundles()
        return BundleManager._command_dict.keys()

    @staticmethod
    def get_command(name):
        if BundleManager._command_dict is None:
            BundleManager.load_bundles()
        if name in BundleManager._command_dict:
            return BundleManager._command_dict[name]()
        else:
            return

    @staticmethod
    def has_command(name):
        if name in BundleManager._command_dict:
            return True
        return False

    @staticmethod
    def list_services():
        if BundleManager._service_dict is None:
            BundleManager.load_bundles()
        return BundleManager._service_dict.keys()

    @staticmethod
    def get_service(name):
        if BundleManager._service_dict is None:
            BundleManager.load_bundles()
        if name in BundleManager._service_dict:
            x = BundleManager._service_dict[name]()
            return x
        else:
            return

    @staticmethod
    def has_service(name):
        if name in BundleManager._service_dict:
            return True
        return False

    @staticmethod
    def list_access_managers():
        if BundleManager._manager_dict is None:
            BundleManager.load_bundles()
        return BundleManager._manager_dict.keys()

    @staticmethod
    def get_access_manager(kind, ctx):
        kind = kind.lower()
        if BundleManager._manager_dict is None:
            BundleManager.load_bundles()
        if kind in BundleManager._manager_dict:
            return BundleManager._manager_dict[kind](ctx)
        else:
            return EntityAccessManager(ctx)

    @staticmethod
    def get_content_plugins(kind, ctx):
        kind = kind.lower()
        if BundleManager._plugin_dict is None:
            BundleManager.load_bundles()
        if kind in BundleManager._plugin_dict:
            result = []
            for plugin in BundleManager._plugin_dict[kind]:
                result.append(plugin(ctx))

            return result
        else:
            return []