# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/crawlers_manager.py
# Compiled at: 2011-09-28 13:50:09
import Queue, time
from concurrent_tree_crawler.crawler_thread import CrawlerThread

class CrawlersManagerException(Exception):
    pass


class CrawlersManager:
    """Starts and stops different crawler threads"""

    def __init__(self, tree, navigators):
        """
                @param tree: L{TreeAccessor} object to be used by all of the threads
                @type tree: L{TreeAccessor}
                @param navigators: navigators to be used by the threads. Each thread
                        obtains a single navigator. Number of threads created is the same
                        as the number of navigators.
                @type navigators: list of L{NavigatorTreeWrapper}s
                """
        self.__tree = tree
        self.__navigators = navigators
        self.__status_queue = None
        self.__threads = None
        return

    def start--- This code section failed: ---

 L.  29         0  LOAD_GLOBAL           0  'len'
                3  LOAD_FAST             0  'self'
                6  LOAD_ATTR             1  '__navigators'
                9  CALL_FUNCTION_1       1  None
               12  LOAD_CONST               0
               15  COMPARE_OP            4  >
               18  POP_JUMP_IF_TRUE     30  'to 30'
               21  LOAD_ASSERT              AssertionError
               24  LOAD_CONST               'No navigators available'
               27  RAISE_VARARGS_2       2  None

 L.  30        30  LOAD_GLOBAL           3  'Queue'
               33  LOAD_ATTR             3  'Queue'
               36  CALL_FUNCTION_0       0  None
               39  LOAD_FAST             0  'self'
               42  STORE_ATTR            4  '__status_queue'

 L.  31        45  BUILD_LIST_0          0 
               48  LOAD_FAST             0  'self'
               51  STORE_ATTR            5  '__threads'

 L.  32        54  SETUP_LOOP           57  'to 114'
               57  LOAD_FAST             0  'self'
               60  LOAD_ATTR             1  '__navigators'
               63  GET_ITER         
               64  FOR_ITER             46  'to 113'
               67  STORE_FAST            1  'navigator'

 L.  33        70  LOAD_GLOBAL           6  'CrawlerThread'
               73  LOAD_FAST             1  'navigator'
               76  LOAD_FAST             0  'self'
               79  LOAD_ATTR             7  '__tree'
               82  LOAD_FAST             0  'self'
               85  LOAD_ATTR             4  '__status_queue'
               88  CALL_FUNCTION_3       3  None
               91  STORE_FAST            2  'crawler'

 L.  34        94  LOAD_FAST             0  'self'
               97  LOAD_ATTR             5  '__threads'
              100  LOAD_ATTR             8  'append'
              103  LOAD_FAST             2  'crawler'
              106  CALL_FUNCTION_1       1  None
              109  POP_TOP          
              110  JUMP_BACK            64  'to 64'
              113  POP_BLOCK        
            114_0  COME_FROM            54  '54'

 L.  35       114  SETUP_LOOP           36  'to 153'
              117  LOAD_FAST             0  'self'
              120  LOAD_ATTR             5  '__threads'
              123  GET_ITER         
              124  FOR_ITER             25  'to 152'
              127  STORE_FAST            3  't'

 L.  36       130  LOAD_GLOBAL           9  'True'
              133  LOAD_FAST             3  't'
              136  STORE_ATTR           10  'daemon'

 L.  37       139  LOAD_FAST             3  't'
              142  LOAD_ATTR            11  'start'
              145  CALL_FUNCTION_0       0  None
              148  POP_TOP          
              149  JUMP_BACK           124  'to 124'
              152  POP_BLOCK        
            153_0  COME_FROM           114  '114'

Parse error at or near `POP_BLOCK' instruction at offset 152

    def stop(self):
        for t in self.__threads:
            t.stop_activity()

        self.wait_until_finish()

    def wait_until_finish(self, timeout=None):
        """
                Wait until all threads finished their jobs and then get rid of them. If
                C{timeout} seconds pass before the threads are finished, they are 
                stopped.
                
                @param timeout: if the value is not C{None}, the method 
                        blocks at most for C{timeout} number of seconds, otherwise 
                        the method blocks until all threads are finished.
                @return: C{False} iff the wait ended because of the timeout 
                """
        try:
            try:
                for _ in xrange(len(self.__threads)):
                    wait_start = time.time()
                    ex_info = self.__status_queue.get(timeout=timeout)
                    wait_end = time.time()
                    if ex_info is not None:
                        raise CrawlersManagerException(ex_info[1])
                    if timeout is not None:
                        timeout = timeout - (wait_end - wait_start)
                        if timeout <= 0:
                            raise Queue.Empty

                return True
            except Queue.Empty as _:
                for t in self.__threads:
                    t.stop_activity()

                for t in self.__threads:
                    t.join()

                return False

        finally:
            del self.__threads[:]

        return