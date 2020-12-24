# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/dispatch/resource/dispatch.py
# Compiled at: 2019-06-10 13:47:41
# Size of source mod 2**32: 2794 bytes
import warnings
from collections import deque
from functools import partial
from inspect import isclass, ismethod
from .exc import InvalidMethod
log = __import__('logging').getLogger(__name__)

def invalid_method(*args, **kw):
    raise InvalidMethod()


class ResourceDispatch:
    __slots__ = ()

    def __repr__(self):
        return 'ResourceDispatch(0x{id})'.format(id=(id(self)), self=self)

    def __call__--- This code section failed: ---

 L.  26         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'context'
                4  LOAD_STR                 'environ'
                6  LOAD_FAST                'context'
                8  CALL_FUNCTION_3       3  '3 positional arguments'
               10  LOAD_STR                 'REQUEST_METHOD'
               12  BINARY_SUBSCR    
               14  LOAD_METHOD              lower
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  STORE_FAST               'verb'

 L.  29        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'path'
               24  LOAD_GLOBAL              deque
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  POP_JUMP_IF_TRUE    106  'to 106'

 L.  30        30  LOAD_GLOBAL              warnings
               32  LOAD_ATTR                warn

 L.  31        34  LOAD_STR                 'Your code is not providing the path as a deque; this will be cast in development butwill explode gloriously if run in a production environment.'

 L.  33        36  LOAD_GLOBAL              RuntimeWarning
               38  LOAD_CONST               1
               40  LOAD_CONST               ('stacklevel',)
               42  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               44  POP_TOP          

 L.  36        46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'path'
               50  LOAD_GLOBAL              str
               52  CALL_FUNCTION_2       2  '2 positional arguments'
               54  POP_JUMP_IF_FALSE    98  'to 98'

 L.  37        56  LOAD_GLOBAL              deque
               58  LOAD_FAST                'path'
               60  LOAD_METHOD              split
               62  LOAD_STR                 '/'
               64  CALL_METHOD_1         1  '1 positional argument'
               66  LOAD_FAST                'path'
               68  POP_JUMP_IF_FALSE    80  'to 80'
               70  LOAD_FAST                'path'
               72  LOAD_METHOD              startswith
               74  LOAD_STR                 '/'
               76  CALL_METHOD_1         1  '1 positional argument'
               78  POP_JUMP_IF_FALSE    84  'to 84'
             80_0  COME_FROM            68  '68'
               80  LOAD_CONST               1
               82  JUMP_FORWARD         86  'to 86'
             84_0  COME_FROM            78  '78'
               84  LOAD_CONST               0
             86_0  COME_FROM            82  '82'
               86  LOAD_CONST               None
               88  BUILD_SLICE_2         2 
               90  BINARY_SUBSCR    
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  STORE_FAST               'path'
               96  JUMP_FORWARD        106  'to 106'
             98_0  COME_FROM            54  '54'

 L.  39        98  LOAD_GLOBAL              deque
              100  LOAD_FAST                'path'
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  STORE_FAST               'path'
            106_0  COME_FROM            96  '96'
            106_1  COME_FROM            28  '28'

 L.  41       106  LOAD_GLOBAL              log
              108  LOAD_ATTR                debug
              110  LOAD_STR                 'Preparing resource dispatch. '
              112  LOAD_GLOBAL              repr
              114  LOAD_DEREF               'obj'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  BINARY_ADD       
              120  LOAD_GLOBAL              dict

 L.  42       122  LOAD_GLOBAL              repr
              124  LOAD_FAST                'self'
              126  CALL_FUNCTION_1       1  '1 positional argument'

 L.  43       128  LOAD_GLOBAL              repr
              130  LOAD_FAST                'context'
              132  CALL_FUNCTION_1       1  '1 positional argument'

 L.  44       134  LOAD_GLOBAL              repr
              136  LOAD_DEREF               'obj'
              138  CALL_FUNCTION_1       1  '1 positional argument'

 L.  45       140  LOAD_GLOBAL              list
              142  LOAD_FAST                'path'
              144  CALL_FUNCTION_1       1  '1 positional argument'

 L.  46       146  LOAD_FAST                'verb'
              148  LOAD_CONST               ('dispatcher', 'context', 'obj', 'path', 'verb')
              150  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              152  LOAD_CONST               ('extra',)
              154  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              156  POP_TOP          

 L.  49       158  LOAD_GLOBAL              isclass
              160  LOAD_DEREF               'obj'
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  POP_JUMP_IF_FALSE   190  'to 190'

 L.  50       166  LOAD_DEREF               'obj'
              168  LOAD_FAST                'context'
              170  LOAD_CONST               None
              172  LOAD_CONST               None
              174  CALL_FUNCTION_3       3  '3 positional arguments'
              176  STORE_DEREF              'obj'

 L.  51       178  LOAD_CONST               None
              180  LOAD_DEREF               'obj'
              182  LOAD_CONST               False
              184  BUILD_TUPLE_3         3 
              186  YIELD_VALUE      
              188  POP_TOP          
            190_0  COME_FROM           164  '164'

 L.  53       190  LOAD_DEREF               'obj'
              192  LOAD_FAST                'context'
              194  STORE_ATTR               resource

 L.  54       196  LOAD_CONST               None
              198  STORE_FAST               'consumed'

 L.  55       200  LOAD_GLOBAL              getattr
              202  LOAD_DEREF               'obj'
              204  LOAD_STR                 '__resource__'
              206  LOAD_CONST               None
              208  CALL_FUNCTION_3       3  '3 positional arguments'
              210  STORE_FAST               'Resource'

 L.  56       212  LOAD_SETCOMP             '<code_object <setcomp>>'
              214  LOAD_STR                 'ResourceDispatch.__call__.<locals>.<setcomp>'
              216  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              218  LOAD_GLOBAL              dir
              220  LOAD_DEREF               'obj'
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  GET_ITER         
              226  CALL_FUNCTION_1       1  '1 positional argument'
              228  LOAD_STR                 'options'
              230  BUILD_SET_1           1 
              232  BINARY_OR        
              234  STORE_FAST               'safe'

 L.  57       236  LOAD_STR                 'get'
              238  LOAD_FAST                'safe'
              240  COMPARE_OP               in
              242  POP_JUMP_IF_FALSE   254  'to 254'

 L.  57       244  LOAD_FAST                'safe'
              246  LOAD_METHOD              add
              248  LOAD_STR                 'head'
              250  CALL_METHOD_1         1  '1 positional argument'
              252  POP_TOP          
            254_0  COME_FROM           242  '242'

 L.  59       254  LOAD_STR                 'collection'
              256  LOAD_FAST                'context'
              258  COMPARE_OP               not-in
          260_262  POP_JUMP_IF_FALSE   270  'to 270'

 L.  60       264  LOAD_CONST               None
              266  LOAD_FAST                'context'
              268  STORE_ATTR               collection
            270_0  COME_FROM           260  '260'

 L.  62       270  LOAD_STR                 'response'
              272  LOAD_FAST                'context'
              274  COMPARE_OP               in
          276_278  POP_JUMP_IF_FALSE   302  'to 302'

 L.  63       280  LOAD_CLOSURE             'obj'
              282  BUILD_TUPLE_1         1 
              284  LOAD_SETCOMP             '<code_object <setcomp>>'
              286  LOAD_STR                 'ResourceDispatch.__call__.<locals>.<setcomp>'
              288  MAKE_FUNCTION_8          'closure'
              290  LOAD_FAST                'safe'
              292  GET_ITER         
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  LOAD_FAST                'context'
              298  LOAD_ATTR                response
              300  STORE_ATTR               allow
            302_0  COME_FROM           276  '276'

 L.  65       302  LOAD_FAST                'path'
          304_306  POP_JUMP_IF_FALSE   428  'to 428'
              308  LOAD_FAST                'path'
              310  LOAD_CONST               0
              312  BINARY_SUBSCR    
              314  LOAD_FAST                'safe'
              316  COMPARE_OP               in
          318_320  POP_JUMP_IF_FALSE   428  'to 428'

 L.  66       322  LOAD_FAST                'path'
              324  LOAD_METHOD              popleft
              326  CALL_METHOD_0         0  '0 positional arguments'
              328  DUP_TOP          
              330  STORE_FAST               'consumed'
              332  STORE_FAST               'attr'

 L.  67       334  LOAD_GLOBAL              getattr
              336  LOAD_DEREF               'obj'
              338  LOAD_FAST                'attr'
              340  LOAD_CONST               None
              342  CALL_FUNCTION_3       3  '3 positional arguments'
              344  STORE_FAST               'attr'

 L.  68       346  LOAD_FAST                'attr'
          348_350  POP_JUMP_IF_TRUE    378  'to 378'
              352  LOAD_FAST                'consumed'
              354  LOAD_CONST               {'head', 'options'}
              356  COMPARE_OP               in
          358_360  POP_JUMP_IF_FALSE   378  'to 378'

 L.  69       362  LOAD_GLOBAL              partial
              364  LOAD_GLOBAL              getattr
              366  LOAD_FAST                'self'
              368  LOAD_FAST                'consumed'
              370  CALL_FUNCTION_2       2  '2 positional arguments'
              372  LOAD_DEREF               'obj'
              374  CALL_FUNCTION_2       2  '2 positional arguments'
              376  STORE_FAST               'attr'
            378_0  COME_FROM           358  '358'
            378_1  COME_FROM           348  '348'

 L.  71       378  LOAD_GLOBAL              isclass
              380  LOAD_FAST                'attr'
              382  CALL_FUNCTION_1       1  '1 positional argument'
          384_386  POP_JUMP_IF_FALSE   412  'to 412'

 L.  72       388  LOAD_FAST                'consumed'
              390  LOAD_FAST                'attr'
              392  LOAD_FAST                'context'
              394  LOAD_DEREF               'obj'
              396  LOAD_CONST               None
              398  CALL_FUNCTION_3       3  '3 positional arguments'
              400  LOAD_CONST               False
              402  BUILD_TUPLE_3         3 
              404  YIELD_VALUE      
              406  POP_TOP          

 L.  73       408  LOAD_CONST               None
              410  RETURN_VALUE     
            412_0  COME_FROM           384  '384'

 L.  75       412  LOAD_FAST                'consumed'
              414  LOAD_FAST                'attr'
              416  LOAD_CONST               True
              418  BUILD_TUPLE_3         3 
              420  YIELD_VALUE      
              422  POP_TOP          

 L.  76       424  LOAD_CONST               None
              426  RETURN_VALUE     
            428_0  COME_FROM           318  '318'
            428_1  COME_FROM           304  '304'

 L.  78       428  LOAD_FAST                'path'
          430_432  POP_JUMP_IF_FALSE   514  'to 514'
              434  LOAD_FAST                'Resource'
          436_438  POP_JUMP_IF_FALSE   514  'to 514'

 L.  79       440  LOAD_DEREF               'obj'
              442  LOAD_FAST                'context'
              444  STORE_ATTR               collection

 L.  81       446  SETUP_EXCEPT        472  'to 472'

 L.  82       448  LOAD_FAST                'Resource'
              450  LOAD_FAST                'context'
              452  LOAD_DEREF               'obj'
              454  LOAD_DEREF               'obj'
              456  LOAD_FAST                'path'
              458  LOAD_CONST               0
              460  BINARY_SUBSCR    
              462  BINARY_SUBSCR    
              464  CALL_FUNCTION_3       3  '3 positional arguments'
              466  STORE_DEREF              'obj'
              468  POP_BLOCK        
              470  JUMP_FORWARD        494  'to 494'
            472_0  COME_FROM_EXCEPT    446  '446'

 L.  83       472  DUP_TOP          
              474  LOAD_GLOBAL              KeyError
              476  COMPARE_OP               exception-match
          478_480  POP_JUMP_IF_FALSE   492  'to 492'
              482  POP_TOP          
              484  POP_TOP          
              486  POP_TOP          

 L.  84       488  POP_EXCEPT       
              490  JUMP_FORWARD        510  'to 510'
            492_0  COME_FROM           478  '478'
              492  END_FINALLY      
            494_0  COME_FROM           470  '470'

 L.  86       494  LOAD_FAST                'path'
              496  LOAD_METHOD              popleft
              498  CALL_METHOD_0         0  '0 positional arguments'
              500  LOAD_DEREF               'obj'
              502  LOAD_CONST               False
              504  BUILD_TUPLE_3         3 
              506  YIELD_VALUE      
              508  POP_TOP          
            510_0  COME_FROM           490  '490'

 L.  88       510  LOAD_CONST               None
              512  RETURN_VALUE     
            514_0  COME_FROM           436  '436'
            514_1  COME_FROM           430  '430'

 L.  90       514  LOAD_FAST                'verb'
          516_518  POP_JUMP_IF_FALSE   590  'to 590'
              520  LOAD_FAST                'verb'
              522  LOAD_FAST                'safe'
              524  COMPARE_OP               in
          526_528  POP_JUMP_IF_FALSE   590  'to 590'

 L.  91       530  LOAD_GLOBAL              getattr
              532  LOAD_DEREF               'obj'
              534  LOAD_FAST                'verb'
              536  LOAD_CONST               None
              538  CALL_FUNCTION_3       3  '3 positional arguments'
              540  STORE_DEREF              'obj'

 L.  92       542  LOAD_DEREF               'obj'
          544_546  POP_JUMP_IF_TRUE    574  'to 574'
              548  LOAD_FAST                'verb'
              550  LOAD_CONST               {'head', 'options'}
              552  COMPARE_OP               in
          554_556  POP_JUMP_IF_FALSE   574  'to 574'

 L.  93       558  LOAD_GLOBAL              partial
              560  LOAD_GLOBAL              getattr
              562  LOAD_FAST                'self'
              564  LOAD_FAST                'verb'
              566  CALL_FUNCTION_2       2  '2 positional arguments'
              568  LOAD_DEREF               'obj'
              570  CALL_FUNCTION_2       2  '2 positional arguments'
              572  STORE_DEREF              'obj'
            574_0  COME_FROM           554  '554'
            574_1  COME_FROM           544  '544'

 L.  94       574  LOAD_CONST               None
              576  LOAD_DEREF               'obj'
              578  LOAD_CONST               True
              580  BUILD_TUPLE_3         3 
              582  YIELD_VALUE      
              584  POP_TOP          

 L.  95       586  LOAD_CONST               None
              588  RETURN_VALUE     
            590_0  COME_FROM           526  '526'
            590_1  COME_FROM           516  '516'

 L.  97       590  LOAD_CONST               None
              592  LOAD_GLOBAL              invalid_method
              594  LOAD_CONST               True
              596  BUILD_TUPLE_3         3 
              598  YIELD_VALUE      
              600  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 80_0

    def head(self, obj, *args, **kw):
        """Allow the get method to set headers, but return no content.
                
                This performs an internal GET and strips the body from the response.
                """
        (obj.get)(*args, **kw)

    def options(self, obj, *args, **kw):
        """The allowed methods are present in the returned headers."""
        pass