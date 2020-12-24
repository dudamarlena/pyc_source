# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_vendor/html5lib/filters/lint.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 3643 bytes
from __future__ import absolute_import, division, unicode_literals
from pip._vendor.six import text_type
from . import base
from ..constants import namespaces, voidElements
from ..constants import spaceCharacters
spaceCharacters = ''.join(spaceCharacters)

class Filter(base.Filter):
    __doc__ = "Lints the token stream for errors\n\n    If it finds any errors, it'll raise an ``AssertionError``.\n\n    "

    def __init__(self, source, require_matching_tags=True):
        """Creates a Filter

        :arg source: the source token stream

        :arg require_matching_tags: whether or not to require matching tags

        """
        super(Filter, self).__init__(source)
        self.require_matching_tags = require_matching_tags

    def __iter__--- This code section failed: ---

 L.  30         0  BUILD_LIST_0          0 
                2  STORE_FAST               'open_elements'

 L.  31       4_6  SETUP_LOOP          842  'to 842'
                8  LOAD_GLOBAL              base
               10  LOAD_ATTR                Filter
               12  LOAD_METHOD              __iter__
               14  LOAD_FAST                'self'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  GET_ITER         
            20_22  FOR_ITER            840  'to 840'
               24  STORE_FAST               'token'

 L.  32        26  LOAD_FAST                'token'
               28  LOAD_STR                 'type'
               30  BINARY_SUBSCR    
               32  STORE_FAST               'type'

 L.  33        34  LOAD_FAST                'type'
               36  LOAD_CONST               ('StartTag', 'EmptyTag')
               38  COMPARE_OP               in
            40_42  POP_JUMP_IF_FALSE   334  'to 334'

 L.  34        44  LOAD_FAST                'token'
               46  LOAD_STR                 'namespace'
               48  BINARY_SUBSCR    
               50  STORE_FAST               'namespace'

 L.  35        52  LOAD_FAST                'token'
               54  LOAD_STR                 'name'
               56  BINARY_SUBSCR    
               58  STORE_FAST               'name'

 L.  36        60  LOAD_FAST                'namespace'
               62  LOAD_CONST               None
               64  COMPARE_OP               is
               66  POP_JUMP_IF_TRUE     82  'to 82'
               68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'namespace'
               72  LOAD_GLOBAL              text_type
               74  CALL_FUNCTION_2       2  '2 positional arguments'
               76  POP_JUMP_IF_TRUE     82  'to 82'
               78  LOAD_ASSERT              AssertionError
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            76  '76'
             82_1  COME_FROM            66  '66'

 L.  37        82  LOAD_FAST                'namespace'
               84  LOAD_STR                 ''
               86  COMPARE_OP               !=
               88  POP_JUMP_IF_TRUE     94  'to 94'
               90  LOAD_ASSERT              AssertionError
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            88  '88'

 L.  38        94  LOAD_GLOBAL              isinstance
               96  LOAD_FAST                'name'
               98  LOAD_GLOBAL              text_type
              100  CALL_FUNCTION_2       2  '2 positional arguments'
              102  POP_JUMP_IF_TRUE    108  'to 108'
              104  LOAD_ASSERT              AssertionError
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM           102  '102'

 L.  39       108  LOAD_FAST                'name'
              110  LOAD_STR                 ''
              112  COMPARE_OP               !=
              114  POP_JUMP_IF_TRUE    120  'to 120'
              116  LOAD_ASSERT              AssertionError
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM           114  '114'

 L.  40       120  LOAD_GLOBAL              isinstance
              122  LOAD_FAST                'token'
              124  LOAD_STR                 'data'
              126  BINARY_SUBSCR    
              128  LOAD_GLOBAL              dict
              130  CALL_FUNCTION_2       2  '2 positional arguments'
              132  POP_JUMP_IF_TRUE    138  'to 138'
              134  LOAD_ASSERT              AssertionError
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           132  '132'

 L.  41       138  LOAD_FAST                'namespace'
              140  POP_JUMP_IF_FALSE   154  'to 154'
              142  LOAD_FAST                'namespace'
              144  LOAD_GLOBAL              namespaces
              146  LOAD_STR                 'html'
              148  BINARY_SUBSCR    
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   176  'to 176'
            154_0  COME_FROM           140  '140'
              154  LOAD_FAST                'name'
              156  LOAD_GLOBAL              voidElements
              158  COMPARE_OP               in
              160  POP_JUMP_IF_FALSE   176  'to 176'

 L.  42       162  LOAD_FAST                'type'
              164  LOAD_STR                 'EmptyTag'
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_TRUE    188  'to 188'
              170  LOAD_ASSERT              AssertionError
              172  RAISE_VARARGS_1       1  'exception instance'
              174  JUMP_FORWARD        188  'to 188'
            176_0  COME_FROM           160  '160'
            176_1  COME_FROM           152  '152'

 L.  44       176  LOAD_FAST                'type'
              178  LOAD_STR                 'StartTag'
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_TRUE    188  'to 188'
              184  LOAD_ASSERT              AssertionError
              186  RAISE_VARARGS_1       1  'exception instance'
            188_0  COME_FROM           182  '182'
            188_1  COME_FROM           174  '174'
            188_2  COME_FROM           168  '168'

 L.  45       188  LOAD_FAST                'type'
              190  LOAD_STR                 'StartTag'
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   216  'to 216'
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                require_matching_tags
              200  POP_JUMP_IF_FALSE   216  'to 216'

 L.  46       202  LOAD_FAST                'open_elements'
              204  LOAD_METHOD              append
              206  LOAD_FAST                'namespace'
              208  LOAD_FAST                'name'
              210  BUILD_TUPLE_2         2 
              212  CALL_METHOD_1         1  '1 positional argument'
              214  POP_TOP          
            216_0  COME_FROM           200  '200'
            216_1  COME_FROM           194  '194'

 L.  47       216  SETUP_LOOP          330  'to 330'
              218  LOAD_FAST                'token'
              220  LOAD_STR                 'data'
              222  BINARY_SUBSCR    
              224  LOAD_METHOD              items
              226  CALL_METHOD_0         0  '0 positional arguments'
              228  GET_ITER         
            230_0  COME_FROM           320  '320'
              230  FOR_ITER            328  'to 328'
              232  UNPACK_SEQUENCE_2     2 
              234  UNPACK_SEQUENCE_2     2 
              236  STORE_FAST               'namespace'
              238  STORE_FAST               'name'
              240  STORE_FAST               'value'

 L.  48       242  LOAD_FAST                'namespace'
              244  LOAD_CONST               None
              246  COMPARE_OP               is
          248_250  POP_JUMP_IF_TRUE    268  'to 268'
              252  LOAD_GLOBAL              isinstance
              254  LOAD_FAST                'namespace'
              256  LOAD_GLOBAL              text_type
              258  CALL_FUNCTION_2       2  '2 positional arguments'
          260_262  POP_JUMP_IF_TRUE    268  'to 268'
              264  LOAD_ASSERT              AssertionError
              266  RAISE_VARARGS_1       1  'exception instance'
            268_0  COME_FROM           260  '260'
            268_1  COME_FROM           248  '248'

 L.  49       268  LOAD_FAST                'namespace'
              270  LOAD_STR                 ''
              272  COMPARE_OP               !=
          274_276  POP_JUMP_IF_TRUE    282  'to 282'
              278  LOAD_ASSERT              AssertionError
              280  RAISE_VARARGS_1       1  'exception instance'
            282_0  COME_FROM           274  '274'

 L.  50       282  LOAD_GLOBAL              isinstance
              284  LOAD_FAST                'name'
              286  LOAD_GLOBAL              text_type
              288  CALL_FUNCTION_2       2  '2 positional arguments'
          290_292  POP_JUMP_IF_TRUE    298  'to 298'
              294  LOAD_ASSERT              AssertionError
              296  RAISE_VARARGS_1       1  'exception instance'
            298_0  COME_FROM           290  '290'

 L.  51       298  LOAD_FAST                'name'
              300  LOAD_STR                 ''
              302  COMPARE_OP               !=
          304_306  POP_JUMP_IF_TRUE    312  'to 312'
              308  LOAD_ASSERT              AssertionError
              310  RAISE_VARARGS_1       1  'exception instance'
            312_0  COME_FROM           304  '304'

 L.  52       312  LOAD_GLOBAL              isinstance
              314  LOAD_FAST                'value'
              316  LOAD_GLOBAL              text_type
              318  CALL_FUNCTION_2       2  '2 positional arguments'
              320  POP_JUMP_IF_TRUE    230  'to 230'
              322  LOAD_GLOBAL              AssertionError
              324  RAISE_VARARGS_1       1  'exception instance'
              326  JUMP_BACK           230  'to 230'
              328  POP_BLOCK        
            330_0  COME_FROM_LOOP      216  '216'
          330_332  JUMP_FORWARD        832  'to 832'
            334_0  COME_FROM            40  '40'

 L.  54       334  LOAD_FAST                'type'
              336  LOAD_STR                 'EndTag'
              338  COMPARE_OP               ==
          340_342  POP_JUMP_IF_FALSE   522  'to 522'

 L.  55       344  LOAD_FAST                'token'
              346  LOAD_STR                 'namespace'
              348  BINARY_SUBSCR    
              350  STORE_FAST               'namespace'

 L.  56       352  LOAD_FAST                'token'
              354  LOAD_STR                 'name'
              356  BINARY_SUBSCR    
              358  STORE_FAST               'name'

 L.  57       360  LOAD_FAST                'namespace'
              362  LOAD_CONST               None
              364  COMPARE_OP               is
          366_368  POP_JUMP_IF_TRUE    386  'to 386'
              370  LOAD_GLOBAL              isinstance
              372  LOAD_FAST                'namespace'
              374  LOAD_GLOBAL              text_type
              376  CALL_FUNCTION_2       2  '2 positional arguments'
          378_380  POP_JUMP_IF_TRUE    386  'to 386'
              382  LOAD_ASSERT              AssertionError
              384  RAISE_VARARGS_1       1  'exception instance'
            386_0  COME_FROM           378  '378'
            386_1  COME_FROM           366  '366'

 L.  58       386  LOAD_FAST                'namespace'
              388  LOAD_STR                 ''
              390  COMPARE_OP               !=
          392_394  POP_JUMP_IF_TRUE    400  'to 400'
              396  LOAD_ASSERT              AssertionError
              398  RAISE_VARARGS_1       1  'exception instance'
            400_0  COME_FROM           392  '392'

 L.  59       400  LOAD_GLOBAL              isinstance
              402  LOAD_FAST                'name'
              404  LOAD_GLOBAL              text_type
              406  CALL_FUNCTION_2       2  '2 positional arguments'
          408_410  POP_JUMP_IF_TRUE    416  'to 416'
              412  LOAD_ASSERT              AssertionError
              414  RAISE_VARARGS_1       1  'exception instance'
            416_0  COME_FROM           408  '408'

 L.  60       416  LOAD_FAST                'name'
              418  LOAD_STR                 ''
              420  COMPARE_OP               !=
          422_424  POP_JUMP_IF_TRUE    430  'to 430'
              426  LOAD_ASSERT              AssertionError
              428  RAISE_VARARGS_1       1  'exception instance'
            430_0  COME_FROM           422  '422'

 L.  61       430  LOAD_FAST                'namespace'
          432_434  POP_JUMP_IF_FALSE   450  'to 450'
              436  LOAD_FAST                'namespace'
              438  LOAD_GLOBAL              namespaces
              440  LOAD_STR                 'html'
              442  BINARY_SUBSCR    
              444  COMPARE_OP               ==
          446_448  POP_JUMP_IF_FALSE   484  'to 484'
            450_0  COME_FROM           432  '432'
              450  LOAD_FAST                'name'
              452  LOAD_GLOBAL              voidElements
              454  COMPARE_OP               in
          456_458  POP_JUMP_IF_FALSE   484  'to 484'

 L.  62       460  LOAD_CONST               False
          462_464  POP_JUMP_IF_TRUE    518  'to 518'
              466  LOAD_ASSERT              AssertionError
              468  LOAD_STR                 'Void element reported as EndTag token: %(tag)s'
              470  LOAD_STR                 'tag'
              472  LOAD_FAST                'name'
              474  BUILD_MAP_1           1 
              476  BINARY_MODULO    
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  RAISE_VARARGS_1       1  'exception instance'
              482  JUMP_FORWARD        832  'to 832'
            484_0  COME_FROM           456  '456'
            484_1  COME_FROM           446  '446'

 L.  63       484  LOAD_FAST                'self'
              486  LOAD_ATTR                require_matching_tags
          488_490  POP_JUMP_IF_FALSE   832  'to 832'

 L.  64       492  LOAD_FAST                'open_elements'
              494  LOAD_METHOD              pop
              496  CALL_METHOD_0         0  '0 positional arguments'
              498  STORE_FAST               'start'

 L.  65       500  LOAD_FAST                'start'
              502  LOAD_FAST                'namespace'
              504  LOAD_FAST                'name'
              506  BUILD_TUPLE_2         2 
              508  COMPARE_OP               ==
          510_512  POP_JUMP_IF_TRUE    832  'to 832'
              514  LOAD_ASSERT              AssertionError
              516  RAISE_VARARGS_1       1  'exception instance'
            518_0  COME_FROM           462  '462'
          518_520  JUMP_FORWARD        832  'to 832'
            522_0  COME_FROM           340  '340'

 L.  67       522  LOAD_FAST                'type'
              524  LOAD_STR                 'Comment'
              526  COMPARE_OP               ==
          528_530  POP_JUMP_IF_FALSE   560  'to 560'

 L.  68       532  LOAD_FAST                'token'
              534  LOAD_STR                 'data'
              536  BINARY_SUBSCR    
              538  STORE_FAST               'data'

 L.  69       540  LOAD_GLOBAL              isinstance
              542  LOAD_FAST                'data'
              544  LOAD_GLOBAL              text_type
              546  CALL_FUNCTION_2       2  '2 positional arguments'
          548_550  POP_JUMP_IF_TRUE    832  'to 832'
              552  LOAD_ASSERT              AssertionError
              554  RAISE_VARARGS_1       1  'exception instance'
          556_558  JUMP_FORWARD        832  'to 832'
            560_0  COME_FROM           528  '528'

 L.  71       560  LOAD_FAST                'type'
              562  LOAD_CONST               ('Characters', 'SpaceCharacters')
              564  COMPARE_OP               in
          566_568  POP_JUMP_IF_FALSE   640  'to 640'

 L.  72       570  LOAD_FAST                'token'
              572  LOAD_STR                 'data'
              574  BINARY_SUBSCR    
              576  STORE_FAST               'data'

 L.  73       578  LOAD_GLOBAL              isinstance
              580  LOAD_FAST                'data'
              582  LOAD_GLOBAL              text_type
              584  CALL_FUNCTION_2       2  '2 positional arguments'
          586_588  POP_JUMP_IF_TRUE    594  'to 594'
              590  LOAD_ASSERT              AssertionError
              592  RAISE_VARARGS_1       1  'exception instance'
            594_0  COME_FROM           586  '586'

 L.  74       594  LOAD_FAST                'data'
              596  LOAD_STR                 ''
              598  COMPARE_OP               !=
          600_602  POP_JUMP_IF_TRUE    608  'to 608'
              604  LOAD_ASSERT              AssertionError
              606  RAISE_VARARGS_1       1  'exception instance'
            608_0  COME_FROM           600  '600'

 L.  75       608  LOAD_FAST                'type'
              610  LOAD_STR                 'SpaceCharacters'
              612  COMPARE_OP               ==
          614_616  POP_JUMP_IF_FALSE   832  'to 832'

 L.  76       618  LOAD_FAST                'data'
              620  LOAD_METHOD              strip
              622  LOAD_GLOBAL              spaceCharacters
              624  CALL_METHOD_1         1  '1 positional argument'
              626  LOAD_STR                 ''
              628  COMPARE_OP               ==
          630_632  POP_JUMP_IF_TRUE    832  'to 832'
              634  LOAD_ASSERT              AssertionError
              636  RAISE_VARARGS_1       1  'exception instance'
              638  JUMP_FORWARD        832  'to 832'
            640_0  COME_FROM           566  '566'

 L.  78       640  LOAD_FAST                'type'
              642  LOAD_STR                 'Doctype'
              644  COMPARE_OP               ==
          646_648  POP_JUMP_IF_FALSE   746  'to 746'

 L.  79       650  LOAD_FAST                'token'
              652  LOAD_STR                 'name'
              654  BINARY_SUBSCR    
              656  STORE_FAST               'name'

 L.  80       658  LOAD_FAST                'name'
              660  LOAD_CONST               None
              662  COMPARE_OP               is
          664_666  POP_JUMP_IF_TRUE    684  'to 684'
              668  LOAD_GLOBAL              isinstance
              670  LOAD_FAST                'name'
              672  LOAD_GLOBAL              text_type
              674  CALL_FUNCTION_2       2  '2 positional arguments'
          676_678  POP_JUMP_IF_TRUE    684  'to 684'
              680  LOAD_ASSERT              AssertionError
              682  RAISE_VARARGS_1       1  'exception instance'
            684_0  COME_FROM           676  '676'
            684_1  COME_FROM           664  '664'

 L.  81       684  LOAD_FAST                'token'
              686  LOAD_STR                 'publicId'
              688  BINARY_SUBSCR    
              690  LOAD_CONST               None
              692  COMPARE_OP               is
          694_696  POP_JUMP_IF_TRUE    714  'to 714'
              698  LOAD_GLOBAL              isinstance
              700  LOAD_FAST                'name'
              702  LOAD_GLOBAL              text_type
              704  CALL_FUNCTION_2       2  '2 positional arguments'
          706_708  POP_JUMP_IF_TRUE    714  'to 714'
              710  LOAD_ASSERT              AssertionError
              712  RAISE_VARARGS_1       1  'exception instance'
            714_0  COME_FROM           706  '706'
            714_1  COME_FROM           694  '694'

 L.  82       714  LOAD_FAST                'token'
              716  LOAD_STR                 'systemId'
              718  BINARY_SUBSCR    
              720  LOAD_CONST               None
              722  COMPARE_OP               is
          724_726  POP_JUMP_IF_TRUE    832  'to 832'
              728  LOAD_GLOBAL              isinstance
              730  LOAD_FAST                'name'
              732  LOAD_GLOBAL              text_type
              734  CALL_FUNCTION_2       2  '2 positional arguments'
          736_738  POP_JUMP_IF_TRUE    832  'to 832'
              740  LOAD_ASSERT              AssertionError
              742  RAISE_VARARGS_1       1  'exception instance'
              744  JUMP_FORWARD        832  'to 832'
            746_0  COME_FROM           646  '646'

 L.  84       746  LOAD_FAST                'type'
              748  LOAD_STR                 'Entity'
              750  COMPARE_OP               ==
          752_754  POP_JUMP_IF_FALSE   778  'to 778'

 L.  85       756  LOAD_GLOBAL              isinstance
              758  LOAD_FAST                'token'
              760  LOAD_STR                 'name'
              762  BINARY_SUBSCR    
              764  LOAD_GLOBAL              text_type
              766  CALL_FUNCTION_2       2  '2 positional arguments'
          768_770  POP_JUMP_IF_TRUE    832  'to 832'
              772  LOAD_ASSERT              AssertionError
              774  RAISE_VARARGS_1       1  'exception instance'
              776  JUMP_FORWARD        832  'to 832'
            778_0  COME_FROM           752  '752'

 L.  87       778  LOAD_FAST                'type'
              780  LOAD_STR                 'SerializerError'
              782  COMPARE_OP               ==
          784_786  POP_JUMP_IF_FALSE   810  'to 810'

 L.  88       788  LOAD_GLOBAL              isinstance
              790  LOAD_FAST                'token'
              792  LOAD_STR                 'data'
            794_0  COME_FROM           482  '482'
              794  BINARY_SUBSCR    
              796  LOAD_GLOBAL              text_type
              798  CALL_FUNCTION_2       2  '2 positional arguments'
          800_802  POP_JUMP_IF_TRUE    832  'to 832'
              804  LOAD_ASSERT              AssertionError
              806  RAISE_VARARGS_1       1  'exception instance'
              808  JUMP_FORWARD        832  'to 832'
            810_0  COME_FROM           784  '784'

 L.  91       810  LOAD_CONST               False
          812_814  POP_JUMP_IF_TRUE    832  'to 832'
              816  LOAD_ASSERT              AssertionError
              818  LOAD_STR                 'Unknown token type: %(type)s'
              820  LOAD_STR                 'type'
              822  LOAD_FAST                'type'
              824  BUILD_MAP_1           1 
              826  BINARY_MODULO    
              828  CALL_FUNCTION_1       1  '1 positional argument'
              830  RAISE_VARARGS_1       1  'exception instance'
            832_0  COME_FROM           812  '812'
            832_1  COME_FROM           808  '808'
            832_2  COME_FROM           800  '800'
            832_3  COME_FROM           776  '776'
            832_4  COME_FROM           768  '768'
            832_5  COME_FROM           744  '744'
            832_6  COME_FROM           736  '736'
            832_7  COME_FROM           724  '724'
            832_8  COME_FROM           638  '638'
            832_9  COME_FROM           630  '630'
           832_10  COME_FROM           614  '614'
           832_11  COME_FROM           556  '556'
           832_12  COME_FROM           548  '548'
           832_13  COME_FROM           518  '518'
           832_14  COME_FROM           510  '510'
           832_15  COME_FROM           488  '488'
           832_16  COME_FROM           330  '330'

 L.  93       832  LOAD_FAST                'token'
              834  YIELD_VALUE      
              836  POP_TOP          
              838  JUMP_BACK            20  'to 20'
              840  POP_BLOCK        
            842_0  COME_FROM_LOOP        4  '4'

Parse error at or near `COME_FROM' instruction at offset 794_0