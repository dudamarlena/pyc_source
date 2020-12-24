# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/multiprocess/remoteproxy.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 48018 bytes
import os, time, sys, traceback, weakref, numpy as np, threading
try:
    import __builtin__ as builtins, cPickle as pickle
except ImportError:
    import builtins, pickle

from ..util import cprint

class ClosedError(Exception):
    __doc__ = 'Raised when an event handler receives a request to close the connection\n    or discovers that the connection has been closed.'


class NoResultError(Exception):
    __doc__ = 'Raised when a request for the return value of a remote call fails\n    because the call has not yet returned.'


class RemoteEventHandler(object):
    __doc__ = '\n    This class handles communication between two processes. One instance is present on \n    each process and listens for communication from the other process. This enables\n    (amongst other things) ObjectProxy instances to look up their attributes and call \n    their methods.\n    \n    This class is responsible for carrying out actions on behalf of the remote process.\n    Each instance holds one end of a Connection which allows python\n    objects to be passed between processes.\n    \n    For the most common operations, see _import(), close(), and transfer()\n    \n    To handle and respond to incoming requests, RemoteEventHandler requires that its\n    processRequests method is called repeatedly (this is usually handled by the Process\n    classes defined in multiprocess.processes).\n    \n    \n    \n    \n    '
    handlers = {}

    def __init__(self, connection, name, pid, debug=False):
        self.debug = debug
        self.conn = connection
        self.name = name
        self.results = {}
        self.resultLock = threading.RLock()
        self.proxies = {}
        self.proxyLock = threading.RLock()
        self.proxyOptions = {'callSync':'sync', 
         'timeout':10, 
         'returnType':'auto', 
         'autoProxy':False, 
         'deferGetattr':False, 
         'noProxyTypes':[
          type(None), str, int, float, tuple, list, dict, LocalObjectProxy, ObjectProxy]}
        self.optsLock = threading.RLock()
        self.nextRequestId = 0
        self.exited = False
        self.processLock = threading.RLock()
        self.sendLock = threading.RLock()
        RemoteEventHandler.handlers[pid] = self

    @classmethod
    def getHandler(cls, pid):
        try:
            return cls.handlers[pid]
        except:
            print(pid, cls.handlers)
            raise

    def debugMsg(self, msg):
        if not self.debug:
            return
        cprint.cout(self.debug, '[%d] %s\n' % (os.getpid(), str(msg)), -1)

    def getProxyOption(self, opt):
        with self.optsLock:
            return self.proxyOptions[opt]

    def setProxyOptions(self, **kwds):
        """
        Set the default behavior options for object proxies.
        See ObjectProxy._setProxyOptions for more info.
        """
        with self.optsLock:
            self.proxyOptions.update(kwds)

    def processRequests(self):
        """Process all pending requests from the pipe, return
        after no more events are immediately available. (non-blocking)
        Returns the number of events processed.
        """
        with self.processLock:
            if self.exited:
                self.debugMsg('  processRequests: exited already; raise ClosedError.')
                raise ClosedError()
            numProcessed = 0
            while self.conn.poll():
                try:
                    self.handleRequest()
                    numProcessed += 1
                except ClosedError:
                    self.debugMsg('processRequests: got ClosedError from handleRequest; setting exited=True.')
                    self.exited = True
                    raise
                except:
                    print('Error in process %s' % self.name)
                    (sys.excepthook)(*sys.exc_info())

            if numProcessed > 0:
                self.debugMsg('processRequests: finished %d requests' % numProcessed)
            return numProcessed

    def handleRequest--- This code section failed: ---

 L. 154         0  LOAD_CONST               None
                2  STORE_FAST               'result'

 L. 155         4  SETUP_LOOP          156  'to 156'

 L. 156         6  SETUP_EXCEPT         32  'to 32'

 L. 158         8  LOAD_FAST                'self'
               10  LOAD_ATTR                conn
               12  LOAD_METHOD              recv
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  UNPACK_SEQUENCE_4     4 
               18  STORE_FAST               'cmd'
               20  STORE_FAST               'reqId'
               22  STORE_FAST               'nByteMsgs'
               24  STORE_FAST               'optStr'

 L. 159        26  BREAK_LOOP       
               28  POP_BLOCK        
               30  JUMP_BACK             6  'to 6'
             32_0  COME_FROM_EXCEPT      6  '6'

 L. 160        32  DUP_TOP          
               34  LOAD_GLOBAL              EOFError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    66  'to 66'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 161        46  LOAD_FAST                'self'
               48  LOAD_METHOD              debugMsg
               50  LOAD_STR                 '  handleRequest: got EOFError from recv; raise ClosedError.'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  POP_TOP          

 L. 163        56  LOAD_GLOBAL              ClosedError
               58  CALL_FUNCTION_0       0  '0 positional arguments'
               60  RAISE_VARARGS_1       1  'exception instance'
               62  POP_EXCEPT       
               64  JUMP_BACK             6  'to 6'
             66_0  COME_FROM            38  '38'

 L. 164        66  DUP_TOP          
               68  LOAD_GLOBAL              IOError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE   150  'to 150'
               74  POP_TOP          
               76  STORE_FAST               'err'
               78  POP_TOP          
               80  SETUP_FINALLY       138  'to 138'

 L. 165        82  LOAD_FAST                'err'
               84  LOAD_ATTR                errno
               86  LOAD_CONST               4
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   106  'to 106'

 L. 166        92  LOAD_FAST                'self'
               94  LOAD_METHOD              debugMsg
               96  LOAD_STR                 '  handleRequest: got IOError 4 from recv; try again.'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  POP_TOP          

 L. 167       102  CONTINUE_LOOP         6  'to 6'
              104  JUMP_FORWARD        134  'to 134'
            106_0  COME_FROM            90  '90'

 L. 169       106  LOAD_FAST                'self'
              108  LOAD_METHOD              debugMsg
              110  LOAD_STR                 '  handleRequest: got IOError %d from recv (%s); raise ClosedError.'
              112  LOAD_FAST                'err'
              114  LOAD_ATTR                errno
              116  LOAD_FAST                'err'
              118  LOAD_ATTR                strerror
              120  BUILD_TUPLE_2         2 
              122  BINARY_MODULO    
              124  CALL_METHOD_1         1  '1 positional argument'
              126  POP_TOP          

 L. 170       128  LOAD_GLOBAL              ClosedError
              130  CALL_FUNCTION_0       0  '0 positional arguments'
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           104  '104'
              134  POP_BLOCK        
              136  LOAD_CONST               None
            138_0  COME_FROM_FINALLY    80  '80'
              138  LOAD_CONST               None
              140  STORE_FAST               'err'
              142  DELETE_FAST              'err'
              144  END_FINALLY      
              146  POP_EXCEPT       
              148  JUMP_BACK             6  'to 6'
            150_0  COME_FROM            72  '72'
              150  END_FINALLY      
              152  JUMP_BACK             6  'to 6'
              154  POP_BLOCK        
            156_0  COME_FROM_LOOP        4  '4'

 L. 172       156  LOAD_FAST                'self'
              158  LOAD_METHOD              debugMsg
              160  LOAD_STR                 '  handleRequest: received %s %s'
              162  LOAD_GLOBAL              str
              164  LOAD_FAST                'cmd'
              166  CALL_FUNCTION_1       1  '1 positional argument'
              168  LOAD_GLOBAL              str
              170  LOAD_FAST                'reqId'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  BUILD_TUPLE_2         2 
              176  BINARY_MODULO    
              178  CALL_METHOD_1         1  '1 positional argument'
              180  POP_TOP          

 L. 175       182  BUILD_LIST_0          0 
              184  STORE_FAST               'byteData'

 L. 176       186  LOAD_FAST                'nByteMsgs'
              188  LOAD_CONST               0
              190  COMPARE_OP               >
              192  POP_JUMP_IF_FALSE   208  'to 208'

 L. 177       194  LOAD_FAST                'self'
              196  LOAD_METHOD              debugMsg
              198  LOAD_STR                 '    handleRequest: reading %d byte messages'
              200  LOAD_FAST                'nByteMsgs'
              202  BINARY_MODULO    
              204  CALL_METHOD_1         1  '1 positional argument'
              206  POP_TOP          
            208_0  COME_FROM           192  '192'

 L. 178       208  SETUP_LOOP          370  'to 370'
              210  LOAD_GLOBAL              range
              212  LOAD_FAST                'nByteMsgs'
              214  CALL_FUNCTION_1       1  '1 positional argument'
              216  GET_ITER         
              218  FOR_ITER            368  'to 368'
              220  STORE_FAST               'i'

 L. 179       222  SETUP_LOOP          366  'to 366'

 L. 180       224  SETUP_EXCEPT        248  'to 248'

 L. 181       226  LOAD_FAST                'byteData'
              228  LOAD_METHOD              append
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                conn
              234  LOAD_METHOD              recv_bytes
              236  CALL_METHOD_0         0  '0 positional arguments'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  POP_TOP          

 L. 182       242  BREAK_LOOP       
              244  POP_BLOCK        
              246  JUMP_BACK           224  'to 224'
            248_0  COME_FROM_EXCEPT    224  '224'

 L. 183       248  DUP_TOP          
              250  LOAD_GLOBAL              EOFError
              252  COMPARE_OP               exception-match
          254_256  POP_JUMP_IF_FALSE   284  'to 284'
              258  POP_TOP          
              260  POP_TOP          
              262  POP_TOP          

 L. 184       264  LOAD_FAST                'self'
              266  LOAD_METHOD              debugMsg
              268  LOAD_STR                 '    handleRequest: got EOF while reading byte messages; raise ClosedError.'
              270  CALL_METHOD_1         1  '1 positional argument'
              272  POP_TOP          

 L. 185       274  LOAD_GLOBAL              ClosedError
              276  CALL_FUNCTION_0       0  '0 positional arguments'
              278  RAISE_VARARGS_1       1  'exception instance'
              280  POP_EXCEPT       
              282  JUMP_BACK           224  'to 224'
            284_0  COME_FROM           254  '254'

 L. 186       284  DUP_TOP          
              286  LOAD_GLOBAL              IOError
              288  COMPARE_OP               exception-match
          290_292  POP_JUMP_IF_FALSE   360  'to 360'
              294  POP_TOP          
              296  STORE_FAST               'err'
              298  POP_TOP          
              300  SETUP_FINALLY       348  'to 348'

 L. 187       302  LOAD_FAST                'err'
              304  LOAD_ATTR                errno
              306  LOAD_CONST               4
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   328  'to 328'

 L. 188       314  LOAD_FAST                'self'
              316  LOAD_METHOD              debugMsg
              318  LOAD_STR                 '    handleRequest: got IOError 4 while reading byte messages; try again.'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  POP_TOP          

 L. 189       324  CONTINUE_LOOP       224  'to 224'
              326  JUMP_FORWARD        344  'to 344'
            328_0  COME_FROM           310  '310'

 L. 191       328  LOAD_FAST                'self'
              330  LOAD_METHOD              debugMsg
              332  LOAD_STR                 '    handleRequest: got IOError while reading byte messages; raise ClosedError.'
              334  CALL_METHOD_1         1  '1 positional argument'
              336  POP_TOP          

 L. 192       338  LOAD_GLOBAL              ClosedError
              340  CALL_FUNCTION_0       0  '0 positional arguments'
              342  RAISE_VARARGS_1       1  'exception instance'
            344_0  COME_FROM           326  '326'
              344  POP_BLOCK        
              346  LOAD_CONST               None
            348_0  COME_FROM_FINALLY   300  '300'
              348  LOAD_CONST               None
              350  STORE_FAST               'err'
              352  DELETE_FAST              'err'
              354  END_FINALLY      
              356  POP_EXCEPT       
              358  JUMP_BACK           224  'to 224'
            360_0  COME_FROM           290  '290'
              360  END_FINALLY      
              362  JUMP_BACK           224  'to 224'
              364  POP_BLOCK        
            366_0  COME_FROM_LOOP      222  '222'
              366  JUMP_BACK           218  'to 218'
              368  POP_BLOCK        
            370_0  COME_FROM_LOOP      208  '208'

 L. 195   370_372  SETUP_EXCEPT       1236  'to 1236'

 L. 196       374  LOAD_FAST                'cmd'
              376  LOAD_STR                 'result'
              378  COMPARE_OP               ==
          380_382  POP_JUMP_IF_TRUE    394  'to 394'
              384  LOAD_FAST                'cmd'
              386  LOAD_STR                 'error'
              388  COMPARE_OP               ==
          390_392  POP_JUMP_IF_FALSE   402  'to 402'
            394_0  COME_FROM           380  '380'

 L. 197       394  LOAD_FAST                'reqId'
              396  STORE_FAST               'resultId'

 L. 198       398  LOAD_CONST               None
              400  STORE_FAST               'reqId'
            402_0  COME_FROM           390  '390'

 L. 201       402  LOAD_GLOBAL              pickle
              404  LOAD_METHOD              loads
              406  LOAD_FAST                'optStr'
              408  CALL_METHOD_1         1  '1 positional argument'
              410  STORE_FAST               'opts'

 L. 202       412  LOAD_FAST                'self'
              414  LOAD_METHOD              debugMsg
              416  LOAD_STR                 '    handleRequest: id=%s opts=%s'
              418  LOAD_GLOBAL              str
              420  LOAD_FAST                'reqId'
              422  CALL_FUNCTION_1       1  '1 positional argument'
              424  LOAD_GLOBAL              str
              426  LOAD_FAST                'opts'
              428  CALL_FUNCTION_1       1  '1 positional argument'
              430  BUILD_TUPLE_2         2 
              432  BINARY_MODULO    
              434  CALL_METHOD_1         1  '1 positional argument'
              436  POP_TOP          

 L. 204       438  LOAD_FAST                'opts'
              440  LOAD_METHOD              get
              442  LOAD_STR                 'returnType'
              444  LOAD_STR                 'auto'
              446  CALL_METHOD_2         2  '2 positional arguments'
              448  STORE_FAST               'returnType'

 L. 206       450  LOAD_FAST                'cmd'
              452  LOAD_STR                 'result'
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   500  'to 500'

 L. 207       460  LOAD_FAST                'self'
              462  LOAD_ATTR                resultLock
              464  SETUP_WITH          490  'to 490'
              466  POP_TOP          

 L. 208       468  LOAD_STR                 'result'
              470  LOAD_FAST                'opts'
              472  LOAD_STR                 'result'
              474  BINARY_SUBSCR    
              476  BUILD_TUPLE_2         2 
              478  LOAD_FAST                'self'
              480  LOAD_ATTR                results
              482  LOAD_FAST                'resultId'
              484  STORE_SUBSCR     
              486  POP_BLOCK        
              488  LOAD_CONST               None
            490_0  COME_FROM_WITH      464  '464'
              490  WITH_CLEANUP_START
              492  WITH_CLEANUP_FINISH
              494  END_FINALLY      
          496_498  JUMP_FORWARD       1228  'to 1228'
            500_0  COME_FROM           456  '456'

 L. 209       500  LOAD_FAST                'cmd'
              502  LOAD_STR                 'error'
              504  COMPARE_OP               ==
          506_508  POP_JUMP_IF_FALSE   558  'to 558'

 L. 210       510  LOAD_FAST                'self'
              512  LOAD_ATTR                resultLock
              514  SETUP_WITH          548  'to 548'
              516  POP_TOP          

 L. 211       518  LOAD_STR                 'error'
              520  LOAD_FAST                'opts'
              522  LOAD_STR                 'exception'
              524  BINARY_SUBSCR    
              526  LOAD_FAST                'opts'
              528  LOAD_STR                 'excString'
              530  BINARY_SUBSCR    
              532  BUILD_TUPLE_2         2 
              534  BUILD_TUPLE_2         2 
              536  LOAD_FAST                'self'
              538  LOAD_ATTR                results
              540  LOAD_FAST                'resultId'
              542  STORE_SUBSCR     
              544  POP_BLOCK        
              546  LOAD_CONST               None
            548_0  COME_FROM_WITH      514  '514'
              548  WITH_CLEANUP_START
              550  WITH_CLEANUP_FINISH
              552  END_FINALLY      
          554_556  JUMP_FORWARD       1228  'to 1228'
            558_0  COME_FROM           506  '506'

 L. 212       558  LOAD_FAST                'cmd'
              560  LOAD_STR                 'getObjAttr'
              562  COMPARE_OP               ==
          564_566  POP_JUMP_IF_FALSE   590  'to 590'

 L. 213       568  LOAD_GLOBAL              getattr
              570  LOAD_FAST                'opts'
              572  LOAD_STR                 'obj'
              574  BINARY_SUBSCR    
              576  LOAD_FAST                'opts'
              578  LOAD_STR                 'attr'
              580  BINARY_SUBSCR    
              582  CALL_FUNCTION_2       2  '2 positional arguments'
              584  STORE_FAST               'result'
          586_588  JUMP_FORWARD       1228  'to 1228'
            590_0  COME_FROM           564  '564'

 L. 214       590  LOAD_FAST                'cmd'
              592  LOAD_STR                 'callObj'
              594  COMPARE_OP               ==
          596_598  POP_JUMP_IF_FALSE   950  'to 950'

 L. 215       600  LOAD_FAST                'opts'
              602  LOAD_STR                 'obj'
              604  BINARY_SUBSCR    
              606  STORE_FAST               'obj'

 L. 216       608  LOAD_FAST                'opts'
              610  LOAD_STR                 'args'
              612  BINARY_SUBSCR    
              614  STORE_FAST               'fnargs'

 L. 217       616  LOAD_FAST                'opts'
              618  LOAD_STR                 'kwds'
              620  BINARY_SUBSCR    
              622  STORE_FAST               'fnkwds'

 L. 221       624  LOAD_GLOBAL              len
              626  LOAD_FAST                'byteData'
              628  CALL_FUNCTION_1       1  '1 positional argument'
              630  LOAD_CONST               0
              632  COMPARE_OP               >
          634_636  POP_JUMP_IF_FALSE   862  'to 862'

 L. 222       638  SETUP_LOOP          750  'to 750'
              640  LOAD_GLOBAL              enumerate
              642  LOAD_FAST                'fnargs'
              644  CALL_FUNCTION_1       1  '1 positional argument'
              646  GET_ITER         
            648_0  COME_FROM           692  '692'
            648_1  COME_FROM           678  '678'
            648_2  COME_FROM           664  '664'
              648  FOR_ITER            748  'to 748'
              650  UNPACK_SEQUENCE_2     2 
              652  STORE_FAST               'i'
              654  STORE_FAST               'arg'

 L. 223       656  LOAD_GLOBAL              isinstance
              658  LOAD_FAST                'arg'
              660  LOAD_GLOBAL              tuple
              662  CALL_FUNCTION_2       2  '2 positional arguments'
          664_666  POP_JUMP_IF_FALSE   648  'to 648'
              668  LOAD_GLOBAL              len
              670  LOAD_FAST                'arg'
              672  CALL_FUNCTION_1       1  '1 positional argument'
              674  LOAD_CONST               0
              676  COMPARE_OP               >
          678_680  POP_JUMP_IF_FALSE   648  'to 648'
              682  LOAD_FAST                'arg'
              684  LOAD_CONST               0
              686  BINARY_SUBSCR    
              688  LOAD_STR                 '__byte_message__'
              690  COMPARE_OP               ==
          692_694  POP_JUMP_IF_FALSE   648  'to 648'

 L. 224       696  LOAD_FAST                'arg'
              698  LOAD_CONST               1
              700  BINARY_SUBSCR    
              702  STORE_FAST               'ind'

 L. 225       704  LOAD_FAST                'arg'
              706  LOAD_CONST               2
              708  BINARY_SUBSCR    
              710  UNPACK_SEQUENCE_2     2 
              712  STORE_FAST               'dtype'
              714  STORE_FAST               'shape'

 L. 226       716  LOAD_GLOBAL              np
              718  LOAD_ATTR                fromstring
              720  LOAD_FAST                'byteData'
              722  LOAD_FAST                'ind'
              724  BINARY_SUBSCR    
              726  LOAD_FAST                'dtype'
              728  LOAD_CONST               ('dtype',)
              730  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              732  LOAD_METHOD              reshape
              734  LOAD_FAST                'shape'
              736  CALL_METHOD_1         1  '1 positional argument'
              738  LOAD_FAST                'fnargs'
              740  LOAD_FAST                'i'
              742  STORE_SUBSCR     
          744_746  JUMP_BACK           648  'to 648'
              748  POP_BLOCK        
            750_0  COME_FROM_LOOP      638  '638'

 L. 227       750  SETUP_LOOP          862  'to 862'
              752  LOAD_FAST                'fnkwds'
              754  LOAD_METHOD              items
              756  CALL_METHOD_0         0  '0 positional arguments'
              758  GET_ITER         
            760_0  COME_FROM           804  '804'
            760_1  COME_FROM           790  '790'
            760_2  COME_FROM           776  '776'
              760  FOR_ITER            860  'to 860'
              762  UNPACK_SEQUENCE_2     2 
              764  STORE_FAST               'k'
              766  STORE_FAST               'arg'

 L. 228       768  LOAD_GLOBAL              isinstance
              770  LOAD_FAST                'arg'
              772  LOAD_GLOBAL              tuple
              774  CALL_FUNCTION_2       2  '2 positional arguments'
          776_778  POP_JUMP_IF_FALSE   760  'to 760'
              780  LOAD_GLOBAL              len
              782  LOAD_FAST                'arg'
              784  CALL_FUNCTION_1       1  '1 positional argument'
              786  LOAD_CONST               0
              788  COMPARE_OP               >
          790_792  POP_JUMP_IF_FALSE   760  'to 760'
              794  LOAD_FAST                'arg'
              796  LOAD_CONST               0
              798  BINARY_SUBSCR    
              800  LOAD_STR                 '__byte_message__'
              802  COMPARE_OP               ==
          804_806  POP_JUMP_IF_FALSE   760  'to 760'

 L. 229       808  LOAD_FAST                'arg'
              810  LOAD_CONST               1
              812  BINARY_SUBSCR    
              814  STORE_FAST               'ind'

 L. 230       816  LOAD_FAST                'arg'
              818  LOAD_CONST               2
              820  BINARY_SUBSCR    
              822  UNPACK_SEQUENCE_2     2 
              824  STORE_FAST               'dtype'
              826  STORE_FAST               'shape'

 L. 231       828  LOAD_GLOBAL              np
              830  LOAD_ATTR                fromstring
              832  LOAD_FAST                'byteData'
              834  LOAD_FAST                'ind'
              836  BINARY_SUBSCR    
              838  LOAD_FAST                'dtype'
              840  LOAD_CONST               ('dtype',)
              842  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              844  LOAD_METHOD              reshape
              846  LOAD_FAST                'shape'
              848  CALL_METHOD_1         1  '1 positional argument'
              850  LOAD_FAST                'fnkwds'
              852  LOAD_FAST                'k'
              854  STORE_SUBSCR     
          856_858  JUMP_BACK           760  'to 760'
              860  POP_BLOCK        
            862_0  COME_FROM_LOOP      750  '750'
            862_1  COME_FROM           634  '634'

 L. 233       862  LOAD_GLOBAL              len
              864  LOAD_FAST                'fnkwds'
              866  CALL_FUNCTION_1       1  '1 positional argument'
              868  LOAD_CONST               0
              870  COMPARE_OP               ==
          872_874  POP_JUMP_IF_FALSE   936  'to 936'

 L. 234       876  SETUP_EXCEPT        890  'to 890'

 L. 235       878  LOAD_FAST                'obj'
              880  LOAD_FAST                'fnargs'
              882  CALL_FUNCTION_EX      0  'positional arguments only'
              884  STORE_FAST               'result'
              886  POP_BLOCK        
              888  JUMP_FORWARD        934  'to 934'
            890_0  COME_FROM_EXCEPT    876  '876'

 L. 236       890  POP_TOP          
              892  POP_TOP          
              894  POP_TOP          

 L. 237       896  LOAD_GLOBAL              print
              898  LOAD_STR                 'Failed to call object %s: %d, %s'
              900  LOAD_FAST                'obj'
              902  LOAD_GLOBAL              len
              904  LOAD_FAST                'fnargs'
              906  CALL_FUNCTION_1       1  '1 positional argument'
              908  LOAD_FAST                'fnargs'
              910  LOAD_CONST               1
              912  LOAD_CONST               None
              914  BUILD_SLICE_2         2 
              916  BINARY_SUBSCR    
              918  BUILD_TUPLE_3         3 
              920  BINARY_MODULO    
              922  CALL_FUNCTION_1       1  '1 positional argument'
              924  POP_TOP          

 L. 238       926  RAISE_VARARGS_0       0  'reraise'
              928  POP_EXCEPT       
              930  JUMP_FORWARD        934  'to 934'
              932  END_FINALLY      
            934_0  COME_FROM           930  '930'
            934_1  COME_FROM           888  '888'
              934  JUMP_FORWARD       1228  'to 1228'
            936_0  COME_FROM           872  '872'

 L. 240       936  LOAD_FAST                'obj'
              938  LOAD_FAST                'fnargs'
              940  LOAD_FAST                'fnkwds'
              942  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              944  STORE_FAST               'result'
          946_948  JUMP_FORWARD       1228  'to 1228'
            950_0  COME_FROM           596  '596'

 L. 242       950  LOAD_FAST                'cmd'
              952  LOAD_STR                 'getObjValue'
              954  COMPARE_OP               ==
          956_958  POP_JUMP_IF_FALSE   974  'to 974'

 L. 243       960  LOAD_FAST                'opts'
              962  LOAD_STR                 'obj'
              964  BINARY_SUBSCR    
              966  STORE_FAST               'result'

 L. 244       968  LOAD_STR                 'value'
              970  STORE_FAST               'returnType'
              972  JUMP_FORWARD       1228  'to 1228'
            974_0  COME_FROM           956  '956'

 L. 245       974  LOAD_FAST                'cmd'
              976  LOAD_STR                 'transfer'
              978  COMPARE_OP               ==
          980_982  POP_JUMP_IF_FALSE   998  'to 998'

 L. 246       984  LOAD_FAST                'opts'
              986  LOAD_STR                 'obj'
              988  BINARY_SUBSCR    
              990  STORE_FAST               'result'

 L. 247       992  LOAD_STR                 'proxy'
              994  STORE_FAST               'returnType'
              996  JUMP_FORWARD       1228  'to 1228'
            998_0  COME_FROM           980  '980'

 L. 248       998  LOAD_FAST                'cmd'
             1000  LOAD_STR                 'transferArray'
             1002  COMPARE_OP               ==
         1004_1006  POP_JUMP_IF_FALSE  1046  'to 1046'

 L. 250      1008  LOAD_GLOBAL              np
             1010  LOAD_ATTR                fromstring
             1012  LOAD_FAST                'byteData'
             1014  LOAD_CONST               0
             1016  BINARY_SUBSCR    
             1018  LOAD_FAST                'opts'
             1020  LOAD_STR                 'dtype'
             1022  BINARY_SUBSCR    
             1024  LOAD_CONST               ('dtype',)
             1026  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1028  LOAD_METHOD              reshape
             1030  LOAD_FAST                'opts'
             1032  LOAD_STR                 'shape'
             1034  BINARY_SUBSCR    
             1036  CALL_METHOD_1         1  '1 positional argument'
             1038  STORE_FAST               'result'

 L. 251      1040  LOAD_STR                 'proxy'
             1042  STORE_FAST               'returnType'
             1044  JUMP_FORWARD       1228  'to 1228'
           1046_0  COME_FROM          1004  '1004'

 L. 252      1046  LOAD_FAST                'cmd'
             1048  LOAD_STR                 'import'
             1050  COMPARE_OP               ==
         1052_1054  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 253      1056  LOAD_FAST                'opts'
             1058  LOAD_STR                 'module'
             1060  BINARY_SUBSCR    
             1062  STORE_FAST               'name'

 L. 254      1064  LOAD_FAST                'opts'
             1066  LOAD_METHOD              get
             1068  LOAD_STR                 'fromlist'
             1070  BUILD_LIST_0          0 
             1072  CALL_METHOD_2         2  '2 positional arguments'
             1074  STORE_FAST               'fromlist'

 L. 255      1076  LOAD_GLOBAL              builtins
             1078  LOAD_ATTR                __import__
             1080  LOAD_FAST                'name'
             1082  LOAD_FAST                'fromlist'
             1084  LOAD_CONST               ('fromlist',)
             1086  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1088  STORE_FAST               'mod'

 L. 257      1090  LOAD_GLOBAL              len
             1092  LOAD_FAST                'fromlist'
             1094  CALL_FUNCTION_1       1  '1 positional argument'
             1096  LOAD_CONST               0
             1098  COMPARE_OP               ==
         1100_1102  POP_JUMP_IF_FALSE  1160  'to 1160'

 L. 258      1104  LOAD_FAST                'name'
             1106  LOAD_METHOD              lstrip
             1108  LOAD_STR                 '.'
             1110  CALL_METHOD_1         1  '1 positional argument'
             1112  LOAD_METHOD              split
             1114  LOAD_STR                 '.'
             1116  CALL_METHOD_1         1  '1 positional argument'
             1118  STORE_FAST               'parts'

 L. 259      1120  LOAD_FAST                'mod'
             1122  STORE_FAST               'result'

 L. 260      1124  SETUP_LOOP         1172  'to 1172'
             1126  LOAD_FAST                'parts'
             1128  LOAD_CONST               1
             1130  LOAD_CONST               None
             1132  BUILD_SLICE_2         2 
             1134  BINARY_SUBSCR    
             1136  GET_ITER         
             1138  FOR_ITER           1156  'to 1156'
             1140  STORE_FAST               'part'

 L. 261      1142  LOAD_GLOBAL              getattr
             1144  LOAD_FAST                'result'
             1146  LOAD_FAST                'part'
             1148  CALL_FUNCTION_2       2  '2 positional arguments'
             1150  STORE_FAST               'result'
         1152_1154  JUMP_BACK          1138  'to 1138'
             1156  POP_BLOCK        
             1158  JUMP_FORWARD       1172  'to 1172'
           1160_0  COME_FROM          1100  '1100'

 L. 263      1160  LOAD_GLOBAL              map
             1162  LOAD_FAST                'mod'
             1164  LOAD_ATTR                __getattr__
             1166  LOAD_FAST                'fromlist'
             1168  CALL_FUNCTION_2       2  '2 positional arguments'
             1170  STORE_FAST               'result'
           1172_0  COME_FROM          1158  '1158'
           1172_1  COME_FROM_LOOP     1124  '1124'
             1172  JUMP_FORWARD       1228  'to 1228'
           1174_0  COME_FROM          1052  '1052'

 L. 265      1174  LOAD_FAST                'cmd'
             1176  LOAD_STR                 'del'
             1178  COMPARE_OP               ==
         1180_1182  POP_JUMP_IF_FALSE  1200  'to 1200'

 L. 266      1184  LOAD_GLOBAL              LocalObjectProxy
             1186  LOAD_METHOD              releaseProxyId
             1188  LOAD_FAST                'opts'
             1190  LOAD_STR                 'proxyId'
             1192  BINARY_SUBSCR    
             1194  CALL_METHOD_1         1  '1 positional argument'
             1196  POP_TOP          
             1198  JUMP_FORWARD       1228  'to 1228'
           1200_0  COME_FROM          1180  '1180'

 L. 269      1200  LOAD_FAST                'cmd'
             1202  LOAD_STR                 'close'
             1204  COMPARE_OP               ==
         1206_1208  POP_JUMP_IF_FALSE  1228  'to 1228'

 L. 270      1210  LOAD_FAST                'reqId'
             1212  LOAD_CONST               None
           1214_0  COME_FROM           934  '934'
             1214  COMPARE_OP               is-not
         1216_1218  POP_JUMP_IF_FALSE  1228  'to 1228'

 L. 271      1220  LOAD_CONST               True
             1222  STORE_FAST               'result'

 L. 272      1224  LOAD_STR                 'value'
             1226  STORE_FAST               'returnType'
           1228_0  COME_FROM          1216  '1216'
           1228_1  COME_FROM          1206  '1206'
           1228_2  COME_FROM          1198  '1198'
           1228_3  COME_FROM          1172  '1172'
           1228_4  COME_FROM          1044  '1044'
           1228_5  COME_FROM           996  '996'
           1228_6  COME_FROM           972  '972'
           1228_7  COME_FROM           946  '946'
           1228_8  COME_FROM           586  '586'
           1228_9  COME_FROM           554  '554'
          1228_10  COME_FROM           496  '496'

 L. 274      1228  LOAD_CONST               None
             1230  STORE_FAST               'exc'
             1232  POP_BLOCK        
             1234  JUMP_FORWARD       1256  'to 1256'
           1236_0  COME_FROM_EXCEPT    370  '370'

 L. 275      1236  POP_TOP          
             1238  POP_TOP          
             1240  POP_TOP          

 L. 276      1242  LOAD_GLOBAL              sys
             1244  LOAD_METHOD              exc_info
             1246  CALL_METHOD_0         0  '0 positional arguments'
             1248  STORE_FAST               'exc'
             1250  POP_EXCEPT       
             1252  JUMP_FORWARD       1256  'to 1256'
             1254  END_FINALLY      
           1256_0  COME_FROM          1252  '1252'
           1256_1  COME_FROM          1234  '1234'

 L. 280      1256  LOAD_FAST                'reqId'
             1258  LOAD_CONST               None
             1260  COMPARE_OP               is-not
         1262_1264  POP_JUMP_IF_FALSE  1466  'to 1466'

 L. 281      1266  LOAD_FAST                'exc'
             1268  LOAD_CONST               None
             1270  COMPARE_OP               is
         1272_1274  POP_JUMP_IF_FALSE  1434  'to 1434'

 L. 282      1276  LOAD_FAST                'self'
             1278  LOAD_METHOD              debugMsg
             1280  LOAD_STR                 '    handleRequest: sending return value for %d: %s'
             1282  LOAD_FAST                'reqId'
             1284  LOAD_GLOBAL              str
             1286  LOAD_FAST                'result'
             1288  CALL_FUNCTION_1       1  '1 positional argument'
             1290  BUILD_TUPLE_2         2 
             1292  BINARY_MODULO    
             1294  CALL_METHOD_1         1  '1 positional argument'
             1296  POP_TOP          

 L. 284      1298  LOAD_FAST                'returnType'
             1300  LOAD_STR                 'auto'
             1302  COMPARE_OP               ==
         1304_1306  POP_JUMP_IF_FALSE  1350  'to 1350'

 L. 285      1308  LOAD_FAST                'self'
             1310  LOAD_ATTR                optsLock
             1312  SETUP_WITH         1330  'to 1330'
             1314  POP_TOP          

 L. 286      1316  LOAD_FAST                'self'
             1318  LOAD_ATTR                proxyOptions
             1320  LOAD_STR                 'noProxyTypes'
             1322  BINARY_SUBSCR    
             1324  STORE_FAST               'noProxyTypes'
             1326  POP_BLOCK        
             1328  LOAD_CONST               None
           1330_0  COME_FROM_WITH     1312  '1312'
             1330  WITH_CLEANUP_START
             1332  WITH_CLEANUP_FINISH
             1334  END_FINALLY      

 L. 287      1336  LOAD_FAST                'self'
             1338  LOAD_METHOD              autoProxy
             1340  LOAD_FAST                'result'
             1342  LOAD_FAST                'noProxyTypes'
             1344  CALL_METHOD_2         2  '2 positional arguments'
             1346  STORE_FAST               'result'
             1348  JUMP_FORWARD       1368  'to 1368'
           1350_0  COME_FROM          1304  '1304'

 L. 288      1350  LOAD_FAST                'returnType'
             1352  LOAD_STR                 'proxy'
             1354  COMPARE_OP               ==
         1356_1358  POP_JUMP_IF_FALSE  1368  'to 1368'

 L. 289      1360  LOAD_GLOBAL              LocalObjectProxy
             1362  LOAD_FAST                'result'
             1364  CALL_FUNCTION_1       1  '1 positional argument'
             1366  STORE_FAST               'result'
           1368_0  COME_FROM          1356  '1356'
           1368_1  COME_FROM          1348  '1348'

 L. 291      1368  SETUP_EXCEPT       1386  'to 1386'

 L. 292      1370  LOAD_FAST                'self'
             1372  LOAD_METHOD              replyResult
             1374  LOAD_FAST                'reqId'
             1376  LOAD_FAST                'result'
             1378  CALL_METHOD_2         2  '2 positional arguments'
             1380  POP_TOP          
             1382  POP_BLOCK        
             1384  JUMP_FORWARD       1432  'to 1432'
           1386_0  COME_FROM_EXCEPT   1368  '1368'

 L. 293      1386  POP_TOP          
             1388  POP_TOP          
             1390  POP_TOP          

 L. 294      1392  LOAD_GLOBAL              sys
             1394  LOAD_ATTR                excepthook
             1396  LOAD_GLOBAL              sys
             1398  LOAD_METHOD              exc_info
             1400  CALL_METHOD_0         0  '0 positional arguments'
             1402  CALL_FUNCTION_EX      0  'positional arguments only'
             1404  POP_TOP          

 L. 295      1406  LOAD_FAST                'self'
             1408  LOAD_ATTR                replyError
             1410  LOAD_FAST                'reqId'
             1412  BUILD_TUPLE_1         1 
             1414  LOAD_GLOBAL              sys
             1416  LOAD_METHOD              exc_info
             1418  CALL_METHOD_0         0  '0 positional arguments'
             1420  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
             1422  CALL_FUNCTION_EX      0  'positional arguments only'
             1424  POP_TOP          
             1426  POP_EXCEPT       
             1428  JUMP_FORWARD       1432  'to 1432'
             1430  END_FINALLY      
           1432_0  COME_FROM          1428  '1428'
           1432_1  COME_FROM          1384  '1384'
             1432  JUMP_FORWARD       1464  'to 1464'
           1434_0  COME_FROM          1272  '1272'

 L. 297      1434  LOAD_FAST                'self'
             1436  LOAD_METHOD              debugMsg
             1438  LOAD_STR                 '    handleRequest: returning exception for %d'
             1440  LOAD_FAST                'reqId'
             1442  BINARY_MODULO    
             1444  CALL_METHOD_1         1  '1 positional argument'
             1446  POP_TOP          

 L. 298      1448  LOAD_FAST                'self'
             1450  LOAD_ATTR                replyError
             1452  LOAD_FAST                'reqId'
             1454  BUILD_TUPLE_1         1 
             1456  LOAD_FAST                'exc'
             1458  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
             1460  CALL_FUNCTION_EX      0  'positional arguments only'
             1462  POP_TOP          
           1464_0  COME_FROM          1432  '1432'
             1464  JUMP_FORWARD       1486  'to 1486'
           1466_0  COME_FROM          1262  '1262'

 L. 300      1466  LOAD_FAST                'exc'
             1468  LOAD_CONST               None
             1470  COMPARE_OP               is-not
         1472_1474  POP_JUMP_IF_FALSE  1486  'to 1486'

 L. 301      1476  LOAD_GLOBAL              sys
             1478  LOAD_ATTR                excepthook
             1480  LOAD_FAST                'exc'
             1482  CALL_FUNCTION_EX      0  'positional arguments only'
             1484  POP_TOP          
           1486_0  COME_FROM          1472  '1472'
           1486_1  COME_FROM          1464  '1464'

 L. 303      1486  LOAD_FAST                'cmd'
             1488  LOAD_STR                 'close'
             1490  COMPARE_OP               ==
         1492_1494  POP_JUMP_IF_FALSE  1532  'to 1532'

 L. 304      1496  LOAD_FAST                'opts'
             1498  LOAD_METHOD              get
             1500  LOAD_STR                 'noCleanup'
             1502  LOAD_CONST               False
             1504  CALL_METHOD_2         2  '2 positional arguments'
             1506  LOAD_CONST               True
             1508  COMPARE_OP               is
         1510_1512  POP_JUMP_IF_FALSE  1526  'to 1526'

 L. 305      1514  LOAD_GLOBAL              os
             1516  LOAD_METHOD              _exit
             1518  LOAD_CONST               0
             1520  CALL_METHOD_1         1  '1 positional argument'
             1522  POP_TOP          
             1524  JUMP_FORWARD       1532  'to 1532'
           1526_0  COME_FROM          1510  '1510'

 L. 309      1526  LOAD_GLOBAL              ClosedError
             1528  CALL_FUNCTION_0       0  '0 positional arguments'
             1530  RAISE_VARARGS_1       1  'exception instance'
           1532_0  COME_FROM          1524  '1524'
           1532_1  COME_FROM          1492  '1492'

Parse error at or near `COME_FROM' instruction at offset 1214_0

    def replyResult(self, reqId, result):
        self.send(request='result', reqId=reqId, callSync='off', opts=dict(result=result))

    def replyError(self, reqId, *exc):
        print('error: %s %s %s' % (self.name, str(reqId), str(exc[1])))
        excStr = (traceback.format_exception)(*exc)
        try:
            self.send(request='error', reqId=reqId, callSync='off', opts=dict(exception=(exc[1]), excString=excStr))
        except:
            self.send(request='error', reqId=reqId, callSync='off', opts=dict(exception=None, excString=excStr))

    def send(self, request, opts=None, reqId=None, callSync='sync', timeout=10, returnType=None, byteData=None, **kwds):
        """Send a request or return packet to the remote process.
        Generally it is not necessary to call this method directly; it is for internal use.
        (The docstring has information that is nevertheless useful to the programmer
        as it describes the internal protocol used to communicate between processes)
        
        ==============  ====================================================================
        **Arguments:**
        request         String describing the type of request being sent (see below)
        reqId           Integer uniquely linking a result back to the request that generated
                        it. (most requests leave this blank)
        callSync        'sync':  return the actual result of the request
                        'async': return a Request object which can be used to look up the
                                result later
                        'off':   return no result
        timeout         Time in seconds to wait for a response when callSync=='sync'
        opts            Extra arguments sent to the remote process that determine the way
                        the request will be handled (see below)
        returnType      'proxy', 'value', or 'auto'
        byteData        If specified, this is a list of objects to be sent as byte messages
                        to the remote process.
                        This is used to send large arrays without the cost of pickling.
        ==============  ====================================================================
        
        Description of request strings and options allowed for each:
        
        =============  =============  ========================================================
        request        option         description
        -------------  -------------  --------------------------------------------------------
        getObjAttr                    Request the remote process return (proxy to) an
                                      attribute of an object.
                       obj            reference to object whose attribute should be 
                                      returned
                       attr           string name of attribute to return
                       returnValue    bool or 'auto' indicating whether to return a proxy or
                                      the actual value. 
                       
        callObj                       Request the remote process call a function or 
                                      method. If a request ID is given, then the call's
                                      return value will be sent back (or information
                                      about the error that occurred while running the
                                      function)
                       obj            the (reference to) object to call
                       args           tuple of arguments to pass to callable
                       kwds           dict of keyword arguments to pass to callable
                       returnValue    bool or 'auto' indicating whether to return a proxy or
                                      the actual value. 
                       
        getObjValue                   Request the remote process return the value of
                                      a proxied object (must be picklable)
                       obj            reference to object whose value should be returned
                       
        transfer                      Copy an object to the remote process and request
                                      it return a proxy for the new object.
                       obj            The object to transfer.
                       
        import                        Request the remote process import new symbols
                                      and return proxy(ies) to the imported objects
                       module         the string name of the module to import
                       fromlist       optional list of string names to import from module
                       
        del                           Inform the remote process that a proxy has been 
                                      released (thus the remote process may be able to 
                                      release the original object)
                       proxyId        id of proxy which is no longer referenced by 
                                      remote host
                                      
        close                         Instruct the remote process to stop its event loop
                                      and exit. Optionally, this request may return a 
                                      confirmation.
            
        result                        Inform the remote process that its request has 
                                      been processed                        
                       result         return value of a request
                       
        error                         Inform the remote process that its request failed
                       exception      the Exception that was raised (or None if the 
                                      exception could not be pickled)
                       excString      string-formatted version of the exception and 
                                      traceback
        =============  =====================================================================
        """
        if self.exited:
            self.debugMsg('  send: exited already; raise ClosedError.')
            raise ClosedError()
        with self.sendLock:
            if opts is None:
                opts = {}
            elif not callSync in ('off', 'sync', 'async'):
                raise AssertionError('callSync must be one of "off", "sync", or "async"')
            else:
                if reqId is None:
                    if callSync != 'off':
                        reqId = self.nextRequestId
                        self.nextRequestId += 1
                elif not request in ('result', 'error'):
                    raise AssertionError
                if returnType is not None:
                    opts['returnType'] = returnType
                try:
                    optStr = pickle.dumps(opts)
                except:
                    print('====  Error pickling this object:  ====')
                    print(opts)
                    print('=======================================')
                    raise

            nByteMsgs = 0
            if byteData is not None:
                nByteMsgs = len(byteData)
            request = (
             request, reqId, nByteMsgs, optStr)
            self.debugMsg('send request: cmd=%s nByteMsgs=%d id=%s opts=%s' % (str(request[0]), nByteMsgs, str(reqId), str(opts)))
            self.conn.send(request)
            if byteData is not None:
                for obj in byteData:
                    self.conn.send_bytes(obj)

                self.debugMsg('  sent %d byte messages' % len(byteData))
            self.debugMsg('  call sync: %s' % callSync)
            if callSync == 'off':
                return
        req = Request(self, reqId, description=(str(request)), timeout=timeout)
        if callSync == 'async':
            return req
        if callSync == 'sync':
            try:
                return req.result()
            except NoResultError:
                return req

    def close(self, callSync='off', noCleanup=False, **kwds):
        try:
            (self.send)(request='close', opts=dict(noCleanup=noCleanup), callSync=callSync, **kwds)
            self.exited = True
        except ClosedError:
            pass

    def getResult(self, reqId):
        with self.resultLock:
            haveResult = reqId in self.results
        if not haveResult:
            try:
                self.processRequests()
            except ClosedError:
                pass

        else:
            with self.resultLock:
                if reqId not in self.results:
                    raise NoResultError()
                status, result = self.results.pop(reqId)
            if status == 'result':
                return result
                if status == 'error':
                    exc, excStr = result
                    if exc is not None:
                        print('===== Remote process raised exception on request: =====')
                        print(''.join(excStr))
                        print('===== Local Traceback to request follows: =====')
                        raise exc
                    else:
                        print(''.join(excStr))
                        raise Exception('Error getting result. See above for exception from remote process.')
            else:
                raise Exception('Internal error.')

    def _import(self, mod, **kwds):
        """
        Request the remote process import a module (or symbols from a module)
        and return the proxied results. Uses built-in __import__() function, but 
        adds a bit more processing:
        
            _import('module')  =>  returns module
            _import('module.submodule')  =>  returns submodule 
                                             (note this differs from behavior of __import__)
            _import('module', fromlist=[name1, name2, ...])  =>  returns [module.name1, module.name2, ...]
                                             (this also differs from behavior of __import__)
            
        """
        return (self.send)(request='import', callSync='sync', opts=dict(module=mod), **kwds)

    def getObjAttr(self, obj, attr, **kwds):
        return (self.send)(request='getObjAttr', opts=dict(obj=obj, attr=attr), **kwds)

    def getObjValue(self, obj, **kwds):
        return (self.send)(request='getObjValue', opts=dict(obj=obj), **kwds)

    def callObj(self, obj, args, kwds, **opts):
        opts = opts.copy()
        args = list(args)
        with self.optsLock:
            noProxyTypes = opts.pop'noProxyTypes'None
            if noProxyTypes is None:
                noProxyTypes = self.proxyOptions['noProxyTypes']
            autoProxy = opts.pop'autoProxy'self.proxyOptions['autoProxy']
        if autoProxy is True:
            args = [self.autoProxyvnoProxyTypes for v in args]
            for k, v in kwds.iteritems():
                opts[k] = self.autoProxyvnoProxyTypes

        byteMsgs = []
        for i, arg in enumerate(args):
            if arg.__class__ == np.ndarray:
                args[i] = (
                 '__byte_message__', len(byteMsgs), (arg.dtype, arg.shape))
                byteMsgs.append(arg)

        for k, v in kwds.items():
            if v.__class__ == np.ndarray:
                kwds[k] = (
                 '__byte_message__', len(byteMsgs), (v.dtype, v.shape))
                byteMsgs.append(v)

        return (self.send)(request='callObj', opts=dict(obj=obj, args=args, kwds=kwds), byteData=byteMsgs, **opts)

    def registerProxy(self, proxy):
        with self.proxyLock:
            ref = weakref.refproxyself.deleteProxy
            self.proxies[ref] = proxy._proxyId

    def deleteProxy(self, ref):
        with self.proxyLock:
            proxyId = self.proxies.pop(ref)
        try:
            self.send(request='del', opts=dict(proxyId=proxyId), callSync='off')
        except IOError:
            pass

    def transfer(self, obj, **kwds):
        """
        Transfer an object by value to the remote host (the object must be picklable) 
        and return a proxy for the new remote object.
        """
        if obj.__class__ is np.ndarray:
            opts = {'dtype':obj.dtype, 
             'shape':obj.shape}
            return (self.send)(request='transferArray', opts=opts, byteData=[obj], **kwds)
        return (self.send)(request='transfer', opts=dict(obj=obj), **kwds)

    def autoProxy(self, obj, noProxyTypes):
        for typ in noProxyTypes:
            if isinstance(obj, typ):
                return obj

        return LocalObjectProxy(obj)


class Request(object):
    __doc__ = '\n    Request objects are returned when calling an ObjectProxy in asynchronous mode\n    or if a synchronous call has timed out. Use hasResult() to ask whether\n    the result of the call has been returned yet. Use result() to get\n    the returned value.\n    '

    def __init__(self, process, reqId, description=None, timeout=10):
        self.proc = process
        self.description = description
        self.reqId = reqId
        self.gotResult = False
        self._result = None
        self.timeout = timeout

    def result(self, block=True, timeout=None):
        """
        Return the result for this request. 
        
        If block is True, wait until the result has arrived or *timeout* seconds passes.
        If the timeout is reached, raise NoResultError. (use timeout=None to disable)
        If block is False, raise NoResultError immediately if the result has not arrived yet.
        
        If the process's connection has closed before the result arrives, raise ClosedError.
        """
        if self.gotResult:
            return self._result
        if timeout is None:
            timeout = self.timeout
        if block:
            start = time.time()
            while not self.hasResult():
                if self.proc.exited:
                    raise ClosedError()
                time.sleep(0.005)
                if timeout >= 0 and time.time() - start > timeout:
                    print('Request timed out: %s' % self.description)
                    import traceback
                    traceback.print_stack()
                    raise NoResultError()

            return self._result
        self._result = self.proc.getResult(self.reqId)
        self.gotResult = True
        return self._result

    def hasResult(self):
        """Returns True if the result for this request has arrived."""
        try:
            self.result(block=False)
        except NoResultError:
            pass

        return self.gotResult


class LocalObjectProxy(object):
    __doc__ = "\n    Used for wrapping local objects to ensure that they are send by proxy to a remote host.\n    Note that 'proxy' is just a shorter alias for LocalObjectProxy.\n    \n    For example::\n    \n        data = [1,2,3,4,5]\n        remotePlot.plot(data)         ## by default, lists are pickled and sent by value\n        remotePlot.plot(proxy(data))  ## force the object to be sent by proxy\n    \n    "
    nextProxyId = 0
    proxiedObjects = {}

    @classmethod
    def registerObject(cls, obj):
        pid = cls.nextProxyId
        cls.nextProxyId += 1
        cls.proxiedObjects[pid] = obj
        return pid

    @classmethod
    def lookupProxyId(cls, pid):
        return cls.proxiedObjects[pid]

    @classmethod
    def releaseProxyId(cls, pid):
        del cls.proxiedObjects[pid]

    def __init__(self, obj, **opts):
        """
        Create a 'local' proxy object that, when sent to a remote host,
        will appear as a normal ObjectProxy to *obj*. 
        Any extra keyword arguments are passed to proxy._setProxyOptions()
        on the remote side.
        """
        self.processId = os.getpid()
        self.typeStr = repr(obj)
        self.obj = obj
        self.opts = opts

    def __reduce__(self):
        pid = LocalObjectProxy.registerObject(self.obj)
        return (unpickleObjectProxy, (self.processId, pid, self.typeStr, None, self.opts))


proxy = LocalObjectProxy

def unpickleObjectProxy(processId, proxyId, typeStr, attributes=None, opts=None):
    if processId == os.getpid():
        obj = LocalObjectProxy.lookupProxyId(proxyId)
        if attributes is not None:
            for attr in attributes:
                obj = getattr(obj, attr)

        return obj
    proxy = ObjectProxy(processId, proxyId=proxyId, typeStr=typeStr)
    if opts is not None:
        (proxy._setProxyOptions)(**opts)
    return proxy


class ObjectProxy(object):
    __doc__ = "\n    Proxy to an object stored by the remote process. Proxies are created\n    by calling Process._import(), Process.transfer(), or by requesting/calling\n    attributes on existing proxy objects.\n    \n    For the most part, this object can be used exactly as if it\n    were a local object::\n    \n        rsys = proc._import('sys')   # returns proxy to sys module on remote process\n        rsys.stdout                  # proxy to remote sys.stdout\n        rsys.stdout.write            # proxy to remote sys.stdout.write\n        rsys.stdout.write('hello')   # calls sys.stdout.write('hello') on remote machine\n                                     # and returns the result (None)\n    \n    When calling a proxy to a remote function, the call can be made synchronous\n    (result of call is returned immediately), asynchronous (result is returned later),\n    or return can be disabled entirely::\n    \n        ros = proc._import('os')\n        \n        ## synchronous call; result is returned immediately\n        pid = ros.getpid()\n        \n        ## asynchronous call\n        request = ros.getpid(_callSync='async')\n        while not request.hasResult():\n            time.sleep(0.01)\n        pid = request.result()\n        \n        ## disable return when we know it isn't needed\n        rsys.stdout.write('hello', _callSync='off')\n    \n    Additionally, values returned from a remote function call are automatically\n    returned either by value (must be picklable) or by proxy. \n    This behavior can be forced::\n    \n        rnp = proc._import('numpy')\n        arrProxy = rnp.array([1,2,3,4], _returnType='proxy')\n        arrValue = rnp.array([1,2,3,4], _returnType='value')\n    \n    The default callSync and returnType behaviors (as well as others) can be set \n    for each proxy individually using ObjectProxy._setProxyOptions() or globally using \n    proc.setProxyOptions(). \n    \n    "

    def __init__(self, processId, proxyId, typeStr='', parent=None):
        object.__init__(self)
        self.__dict__['_processId'] = processId
        self.__dict__['_typeStr'] = typeStr
        self.__dict__['_proxyId'] = proxyId
        self.__dict__['_attributes'] = ()
        self.__dict__['_proxyOptions'] = {'callSync':None, 
         'timeout':None, 
         'returnType':None, 
         'deferGetattr':None, 
         'noProxyTypes':None}
        self.__dict__['_handler'] = RemoteEventHandler.getHandler(processId)
        self.__dict__['_handler'].registerProxy(self)

    def _setProxyOptions(self, **kwds):
        """
        Change the behavior of this proxy. For all options, a value of None
        will cause the proxy to instead use the default behavior defined
        by its parent Process.
        
        Options are:
        
        =============  =============================================================
        callSync       'sync', 'async', 'off', or None. 
                       If 'async', then calling methods will return a Request object
                       which can be used to inquire later about the result of the 
                       method call.
                       If 'sync', then calling a method
                       will block until the remote process has returned its result
                       or the timeout has elapsed (in this case, a Request object
                       is returned instead).
                       If 'off', then the remote process is instructed _not_ to 
                       reply and the method call will return None immediately.
        returnType     'auto', 'proxy', 'value', or None. 
                       If 'proxy', then the value returned when calling a method
                       will be a proxy to the object on the remote process.
                       If 'value', then attempt to pickle the returned object and
                       send it back.
                       If 'auto', then the decision is made by consulting the
                       'noProxyTypes' option.
        autoProxy      bool or None. If True, arguments to __call__ are 
                       automatically converted to proxy unless their type is 
                       listed in noProxyTypes (see below). If False, arguments
                       are left untouched. Use proxy(obj) to manually convert
                       arguments before sending. 
        timeout        float or None. Length of time to wait during synchronous 
                       requests before returning a Request object instead.
        deferGetattr   True, False, or None. 
                       If False, all attribute requests will be sent to the remote 
                       process immediately and will block until a response is
                       received (or timeout has elapsed).
                       If True, requesting an attribute from the proxy returns a
                       new proxy immediately. The remote process is _not_ contacted
                       to make this request. This is faster, but it is possible to 
                       request an attribute that does not exist on the proxied
                       object. In this case, AttributeError will not be raised
                       until an attempt is made to look up the attribute on the
                       remote process.
        noProxyTypes   List of object types that should _not_ be proxied when
                       sent to the remote process.
        =============  =============================================================
        """
        self._proxyOptions.update(kwds)

    def _getValue(self):
        """
        Return the value of the proxied object
        (the remote object must be picklable)
        """
        return self._handler.getObjValue(self)

    def _getProxyOption(self, opt):
        val = self._proxyOptions[opt]
        if val is None:
            return self._handler.getProxyOption(opt)
        return val

    def _getProxyOptions(self):
        return dict([(k, self._getProxyOption(k)) for k in self._proxyOptions])

    def __reduce__(self):
        return (
         unpickleObjectProxy, (self._processId, self._proxyId, self._typeStr, self._attributes))

    def __repr__(self):
        return '<ObjectProxy for process %d, object 0x%x: %s >' % (self._processId, self._proxyId, self._typeStr)

    def __getattr__(self, attr, **kwds):
        """
        Calls __getattr__ on the remote object and returns the attribute
        by value or by proxy depending on the options set (see
        ObjectProxy._setProxyOptions and RemoteEventHandler.setProxyOptions)
        
        If the option 'deferGetattr' is True for this proxy, then a new proxy object
        is returned _without_ asking the remote object whether the named attribute exists.
        This can save time when making multiple chained attribute requests,
        but may also defer a possible AttributeError until later, making
        them more difficult to debug.
        """
        opts = self._getProxyOptions()
        for k in opts:
            if '_' + k in kwds:
                opts[k] = kwds.pop('_' + k)

        if opts['deferGetattr'] is True:
            return self._deferredAttr(attr)
        return (self._handler.getObjAttr)(self, attr, **opts)

    def _deferredAttr(self, attr):
        return DeferredObjectProxy(self, attr)

    def __call__(self, *args, **kwds):
        """
        Attempts to call the proxied object from the remote process.
        Accepts extra keyword arguments:
        
            _callSync    'off', 'sync', or 'async'
            _returnType   'value', 'proxy', or 'auto'
        
        If the remote call raises an exception on the remote process,
        it will be re-raised on the local process.
        
        """
        opts = self._getProxyOptions()
        for k in opts:
            if '_' + k in kwds:
                opts[k] = kwds.pop('_' + k)

        return (self._handler.callObj)(obj=self, args=args, kwds=kwds, **opts)

    def _getSpecialAttr(self, attr):
        return self._deferredAttr(attr)

    def __getitem__(self, *args):
        return (self._getSpecialAttr('__getitem__'))(*args)

    def __setitem__(self, *args):
        return (self._getSpecialAttr('__setitem__'))(*args, **{'_callSync': 'off'})

    def __setattr__(self, *args):
        return (self._getSpecialAttr('__setattr__'))(*args, **{'_callSync': 'off'})

    def __str__(self, *args):
        return (self._getSpecialAttr('__str__'))(*args, **{'_returnType': 'value'})

    def __len__(self, *args):
        return (self._getSpecialAttr('__len__'))(*args)

    def __add__(self, *args):
        return (self._getSpecialAttr('__add__'))(*args)

    def __sub__(self, *args):
        return (self._getSpecialAttr('__sub__'))(*args)

    def __div__(self, *args):
        return (self._getSpecialAttr('__div__'))(*args)

    def __truediv__(self, *args):
        return (self._getSpecialAttr('__truediv__'))(*args)

    def __floordiv__(self, *args):
        return (self._getSpecialAttr('__floordiv__'))(*args)

    def __mul__(self, *args):
        return (self._getSpecialAttr('__mul__'))(*args)

    def __pow__(self, *args):
        return (self._getSpecialAttr('__pow__'))(*args)

    def __iadd__(self, *args):
        return (self._getSpecialAttr('__iadd__'))(*args, **{'_callSync': 'off'})

    def __isub__(self, *args):
        return (self._getSpecialAttr('__isub__'))(*args, **{'_callSync': 'off'})

    def __idiv__(self, *args):
        return (self._getSpecialAttr('__idiv__'))(*args, **{'_callSync': 'off'})

    def __itruediv__(self, *args):
        return (self._getSpecialAttr('__itruediv__'))(*args, **{'_callSync': 'off'})

    def __ifloordiv__(self, *args):
        return (self._getSpecialAttr('__ifloordiv__'))(*args, **{'_callSync': 'off'})

    def __imul__(self, *args):
        return (self._getSpecialAttr('__imul__'))(*args, **{'_callSync': 'off'})

    def __ipow__(self, *args):
        return (self._getSpecialAttr('__ipow__'))(*args, **{'_callSync': 'off'})

    def __rshift__(self, *args):
        return (self._getSpecialAttr('__rshift__'))(*args)

    def __lshift__(self, *args):
        return (self._getSpecialAttr('__lshift__'))(*args)

    def __irshift__(self, *args):
        return (self._getSpecialAttr('__irshift__'))(*args, **{'_callSync': 'off'})

    def __ilshift__(self, *args):
        return (self._getSpecialAttr('__ilshift__'))(*args, **{'_callSync': 'off'})

    def __eq__(self, *args):
        return (self._getSpecialAttr('__eq__'))(*args)

    def __ne__(self, *args):
        return (self._getSpecialAttr('__ne__'))(*args)

    def __lt__(self, *args):
        return (self._getSpecialAttr('__lt__'))(*args)

    def __gt__(self, *args):
        return (self._getSpecialAttr('__gt__'))(*args)

    def __le__(self, *args):
        return (self._getSpecialAttr('__le__'))(*args)

    def __ge__(self, *args):
        return (self._getSpecialAttr('__ge__'))(*args)

    def __and__(self, *args):
        return (self._getSpecialAttr('__and__'))(*args)

    def __or__(self, *args):
        return (self._getSpecialAttr('__or__'))(*args)

    def __xor__(self, *args):
        return (self._getSpecialAttr('__xor__'))(*args)

    def __iand__(self, *args):
        return (self._getSpecialAttr('__iand__'))(*args, **{'_callSync': 'off'})

    def __ior__(self, *args):
        return (self._getSpecialAttr('__ior__'))(*args, **{'_callSync': 'off'})

    def __ixor__(self, *args):
        return (self._getSpecialAttr('__ixor__'))(*args, **{'_callSync': 'off'})

    def __mod__(self, *args):
        return (self._getSpecialAttr('__mod__'))(*args)

    def __radd__(self, *args):
        return (self._getSpecialAttr('__radd__'))(*args)

    def __rsub__(self, *args):
        return (self._getSpecialAttr('__rsub__'))(*args)

    def __rdiv__(self, *args):
        return (self._getSpecialAttr('__rdiv__'))(*args)

    def __rfloordiv__(self, *args):
        return (self._getSpecialAttr('__rfloordiv__'))(*args)

    def __rtruediv__(self, *args):
        return (self._getSpecialAttr('__rtruediv__'))(*args)

    def __rmul__(self, *args):
        return (self._getSpecialAttr('__rmul__'))(*args)

    def __rpow__(self, *args):
        return (self._getSpecialAttr('__rpow__'))(*args)

    def __rrshift__(self, *args):
        return (self._getSpecialAttr('__rrshift__'))(*args)

    def __rlshift__(self, *args):
        return (self._getSpecialAttr('__rlshift__'))(*args)

    def __rand__(self, *args):
        return (self._getSpecialAttr('__rand__'))(*args)

    def __ror__(self, *args):
        return (self._getSpecialAttr('__ror__'))(*args)

    def __rxor__(self, *args):
        return (self._getSpecialAttr('__ror__'))(*args)

    def __rmod__(self, *args):
        return (self._getSpecialAttr('__rmod__'))(*args)

    def __hash__(self):
        return id(self)


class DeferredObjectProxy(ObjectProxy):
    __doc__ = "\n    This class represents an attribute (or sub-attribute) of a proxied object.\n    It is used to speed up attribute requests. Take the following scenario::\n    \n        rsys = proc._import('sys')\n        rsys.stdout.write('hello')\n        \n    For this simple example, a total of 4 synchronous requests are made to \n    the remote process: \n    \n    1) import sys\n    2) getattr(sys, 'stdout')\n    3) getattr(stdout, 'write')\n    4) write('hello')\n    \n    This takes a lot longer than running the equivalent code locally. To\n    speed things up, we can 'defer' the two attribute lookups so they are\n    only carried out when neccessary::\n    \n        rsys = proc._import('sys')\n        rsys._setProxyOptions(deferGetattr=True)\n        rsys.stdout.write('hello')\n        \n    This example only makes two requests to the remote process; the two \n    attribute lookups immediately return DeferredObjectProxy instances \n    immediately without contacting the remote process. When the call \n    to write() is made, all attribute requests are processed at the same time.\n    \n    Note that if the attributes requested do not exist on the remote object, \n    making the call to write() will raise an AttributeError.\n    "

    def __init__(self, parentProxy, attribute):
        for k in ('_processId', '_typeStr', '_proxyId', '_handler'):
            self.__dict__[k] = getattr(parentProxy, k)

        self.__dict__['_parent'] = parentProxy
        self.__dict__['_attributes'] = parentProxy._attributes + (attribute,)
        self.__dict__['_proxyOptions'] = parentProxy._proxyOptions.copy()

    def __repr__(self):
        return ObjectProxy.__repr__(self) + '.' + '.'.join(self._attributes)

    def _undefer(self):
        """
        Return a non-deferred ObjectProxy referencing the same object
        """
        return self._parent.__getattr__((self._attributes[(-1)]), _deferGetattr=False)