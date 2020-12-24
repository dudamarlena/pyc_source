# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/crawler_thread.py
# Compiled at: 2011-09-28 13:50:09
import threading, logging
from concurrent_tree_crawler.common.threads.ex_thread import ExThread
from concurrent_tree_crawler.abstract_tree_navigator import NavigationException
from concurrent_tree_crawler.abstract_tree_accessor import NodeAction

class CrawlerThread(ExThread):

    def __init__(self, navigator, tree, status_queue=None):
        """
                @type navigator: L{NavigatorTreeWrapper}
                @type tree: L{AbstractTreeAccessor}
                @type status_queue: L{Queue.Queue}
                """
        ExThread.__init__(self, status_queue)
        self.__nav = navigator
        self.__tree = tree
        self.__should_stop = False

    def run_with_exception(self):
        while not self.__should_stop:
            self.__nav.start_in_sentinel()
            try:
                while not self.__should_stop:
                    ret = self.__analyze_children_and_move_to_next_node()
                    if ret == True:
                        self.__log('Exiting')
                        return

            except NavigationException as _:
                pass

    def stop_activity(self):
        self.__should_stop = True

    def __analyze_children_and_move_to_next_node--- This code section failed: ---

 L.  39         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '__nav'
                6  LOAD_ATTR             1  'get_possible_children'
                9  CALL_FUNCTION_0       0  None
               12  STORE_FAST            1  'possible_children_names'

 L.  40        15  LOAD_FAST             0  'self'
               18  LOAD_ATTR             2  '__tree'
               21  LOAD_ATTR             3  'update_and_get_child'

 L.  41        24  LOAD_FAST             0  'self'
               27  LOAD_ATTR             0  '__nav'
               30  LOAD_ATTR             4  'get_current_node'
               33  CALL_FUNCTION_0       0  None
               36  LOAD_FAST             1  'possible_children_names'
               39  CALL_FUNCTION_2       2  None
               42  STORE_FAST            2  'node_info'

 L.  42        45  LOAD_FAST             2  'node_info'
               48  LOAD_CONST               None
               51  COMPARE_OP            8  is
               54  POP_JUMP_IF_FALSE    83  'to 83'

 L.  43        57  LOAD_FAST             0  'self'
               60  LOAD_ATTR             6  '__log'
               63  LOAD_CONST               'No traversable children available'
               66  CALL_FUNCTION_1       1  None
               69  POP_TOP          

 L.  44        70  LOAD_FAST             0  'self'
               73  LOAD_ATTR             0  '__nav'
               76  LOAD_ATTR             7  'move_to_parent'
               79  CALL_FUNCTION_0       0  None
               82  RETURN_END_IF    
             83_0  COME_FROM            54  '54'

 L.  46        83  LOAD_FAST             2  'node_info'
               86  UNPACK_SEQUENCE_2     2 
               89  STORE_FAST            3  'child'
               92  STORE_FAST            4  'action'

 L.  47        95  LOAD_FAST             0  'self'
               98  LOAD_ATTR             6  '__log'
              101  LOAD_CONST               'Obtained child "{}" with action {}'
              104  LOAD_ATTR             8  'format'

 L.  48       107  LOAD_FAST             3  'child'
              110  LOAD_ATTR             9  'get_name'
              113  CALL_FUNCTION_0       0  None
              116  LOAD_GLOBAL          10  'NodeAction'
              119  LOAD_ATTR            11  'to_str'
              122  LOAD_FAST             4  'action'
              125  CALL_FUNCTION_1       1  None
              128  CALL_FUNCTION_2       2  None
              131  CALL_FUNCTION_1       1  None
              134  POP_TOP          

 L.  49       135  LOAD_FAST             0  'self'
              138  LOAD_ATTR             0  '__nav'
              141  LOAD_ATTR            12  'move_to_child'
              144  LOAD_FAST             3  'child'
              147  CALL_FUNCTION_1       1  None
              150  POP_TOP          

 L.  50       151  LOAD_FAST             4  'action'
              154  LOAD_GLOBAL          10  'NodeAction'
              157  LOAD_ATTR            13  'TO_PROCESS'
              160  COMPARE_OP            2  ==
              163  POP_JUMP_IF_FALSE   226  'to 226'

 L.  51       166  LOAD_FAST             0  'self'
              169  LOAD_ATTR             0  '__nav'
              172  LOAD_ATTR            14  'process_node_and_check_if_is_leaf'
              175  CALL_FUNCTION_0       0  None
              178  STORE_FAST            5  'is_leaf'

 L.  52       181  LOAD_FAST             0  'self'
              184  LOAD_ATTR             2  '__tree'
              187  LOAD_ATTR            15  'set_node_type'
              190  LOAD_FAST             3  'child'
              193  LOAD_FAST             5  'is_leaf'
              196  CALL_FUNCTION_2       2  None
              199  POP_TOP          

 L.  53       200  LOAD_FAST             5  'is_leaf'
              203  POP_JUMP_IF_FALSE   219  'to 219'

 L.  54       206  LOAD_FAST             0  'self'
              209  LOAD_ATTR             0  '__nav'
              212  LOAD_ATTR             7  'move_to_parent'
              215  CALL_FUNCTION_0       0  None
              218  RETURN_END_IF    
            219_0  COME_FROM           203  '203'

 L.  56       219  LOAD_GLOBAL          16  'False'
              222  RETURN_VALUE     
              223  JUMP_FORWARD         34  'to 260'

 L.  57       226  LOAD_FAST             4  'action'
              229  LOAD_GLOBAL          10  'NodeAction'
              232  LOAD_ATTR            17  'TO_VISIT'
              235  COMPARE_OP            2  ==
              238  POP_JUMP_IF_FALSE   245  'to 245'

 L.  58       241  LOAD_GLOBAL          16  'False'
              244  RETURN_END_IF    
            245_0  COME_FROM           238  '238'

 L.  60       245  LOAD_GLOBAL          16  'False'
              248  POP_JUMP_IF_TRUE    260  'to 260'
              251  LOAD_ASSERT              AssertionError
              254  LOAD_CONST               'Unknown action type'
              257  RAISE_VARARGS_2       2  None
            260_0  COME_FROM           223  '223'
              260  LOAD_CONST               None
              263  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 260_0

    def __log(self, message):
        """
                @type message: string
                """
        node = self.__nav.get_current_node()
        path_str = '/' + ('/').join(self.__tree.get_path(node))
        logging.debug(('thread="{}", node="{}": {}').format(threading.current_thread().name, path_str, message))