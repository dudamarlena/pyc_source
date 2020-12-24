# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\ValidateXbrlCalcs.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 30697 bytes
"""
Created on Oct 17, 2010

@author: Mark V Systems Limited
(c) Copyright 2010 Mark V Systems Limited, All rights reserved.
"""
from collections import defaultdict
from math import log10, isnan, isinf, fabs, trunc, fmod, floor, pow
import decimal
try:
    from regex import compile as re_compile
except ImportError:
    from re import compile as re_compile

import hashlib
from arelle import Locale, XbrlConst, XbrlUtil
from arelle.ModelObject import ObjectPropertyViewWrapper
from arelle.XmlValidate import UNVALIDATED, VALID
numberPattern = re_compile('[-+]?[0]*([1-9]?[0-9]*)([.])?(0*)([1-9]?[0-9]*)?([eE])?([-+]?[0-9]*)?')
ZERO = decimal.Decimal(0)
ONE = decimal.Decimal(1)
NaN = decimal.Decimal('NaN')
floatNaN = float('NaN')
floatINF = float('INF')

def validate(modelXbrl, inferDecimals=False, deDuplicate=False):
    ValidateXbrlCalcs(modelXbrl, inferDecimals, deDuplicate).validate()


class ValidateXbrlCalcs:

    def __init__(self, modelXbrl, inferDecimals=False, deDuplicate=False):
        self.modelXbrl = modelXbrl
        self.inferDecimals = inferDecimals
        self.deDuplicate = deDuplicate
        self.mapContext = {}
        self.mapUnit = {}
        self.sumFacts = defaultdict(list)
        self.sumConceptBindKeys = defaultdict(set)
        self.itemFacts = defaultdict(list)
        self.itemConceptBindKeys = defaultdict(set)
        self.duplicateKeyFacts = {}
        self.duplicatedFacts = set()
        self.consistentDupFacts = set()
        self.esAlFacts = defaultdict(list)
        self.esAlConceptBindKeys = defaultdict(set)
        self.conceptsInEssencesAlias = set()
        self.requiresElementFacts = defaultdict(list)
        self.conceptsInRequiresElement = set()

    def validate--- This code section failed: ---

 L.  50         0  LOAD_FAST                'self'
                2  LOAD_ATTR                modelXbrl
                4  LOAD_ATTR                contexts
                6  UNARY_NOT        
                8  POP_JUMP_IF_FALSE    24  'to 24'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                modelXbrl
               14  LOAD_ATTR                facts
               16  UNARY_NOT        
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L.  51        20  LOAD_CONST               None
               22  RETURN_END_IF    
             24_0  COME_FROM            18  '18'
             24_1  COME_FROM             8  '8'

 L.  53        24  LOAD_FAST                'self'
               26  LOAD_ATTR                inferDecimals
               28  POP_JUMP_IF_TRUE     44  'to 44'

 L.  54        30  LOAD_FAST                'self'
               32  LOAD_ATTR                modelXbrl
               34  LOAD_ATTR                info
               36  LOAD_STR                 'xbrl.5.2.5.2:inferringPrecision'
               38  LOAD_STR                 'Validating calculations inferring precision.'
               40  CALL_FUNCTION_2       2  '2 positional arguments'
               42  POP_TOP          
             44_0  COME_FROM            28  '28'

 L.  57        44  LOAD_FAST                'self'
               46  LOAD_ATTR                modelXbrl
               48  LOAD_ATTR                profileActivity
               50  CALL_FUNCTION_0       0  '0 positional arguments'
               52  POP_TOP          

 L.  58        54  BUILD_MAP_0           0 
               56  STORE_FAST               'uniqueContextHashes'

 L.  59        58  SETUP_LOOP          132  'to 132'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelXbrl
               64  LOAD_ATTR                contexts
               66  LOAD_ATTR                values
               68  CALL_FUNCTION_0       0  '0 positional arguments'
               70  GET_ITER         
               72  FOR_ITER            130  'to 130'
               74  STORE_FAST               'context'

 L.  60        76  LOAD_FAST                'context'
               78  LOAD_ATTR                contextDimAwareHash
               80  STORE_FAST               'h'

 L.  61        82  LOAD_FAST                'h'
               84  LOAD_FAST                'uniqueContextHashes'
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE   120  'to 120'

 L.  62        90  LOAD_FAST                'context'
               92  LOAD_ATTR                isEqualTo
               94  LOAD_FAST                'uniqueContextHashes'
               96  LOAD_FAST                'h'
               98  BINARY_SUBSCR    
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  POP_JUMP_IF_FALSE   128  'to 128'

 L.  63       104  LOAD_FAST                'uniqueContextHashes'
              106  LOAD_FAST                'h'
              108  BINARY_SUBSCR    
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                mapContext
              114  LOAD_FAST                'context'
              116  STORE_SUBSCR     
              118  JUMP_BACK            72  'to 72'
              120  ELSE                     '128'

 L.  65       120  LOAD_FAST                'context'
              122  LOAD_FAST                'uniqueContextHashes'
              124  LOAD_FAST                'h'
              126  STORE_SUBSCR     
            128_0  COME_FROM           102  '102'
              128  JUMP_BACK            72  'to 72'
              130  POP_BLOCK        
            132_0  COME_FROM_LOOP       58  '58'

 L.  66       132  DELETE_FAST              'uniqueContextHashes'

 L.  67       134  LOAD_FAST                'self'
              136  LOAD_ATTR                modelXbrl
              138  LOAD_ATTR                profileActivity
              140  LOAD_STR                 '... identify equal contexts'
              142  LOAD_CONST               1.0
              144  LOAD_CONST               ('minTimeToShow',)
              146  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              148  POP_TOP          

 L.  70       150  BUILD_MAP_0           0 
              152  STORE_FAST               'uniqueUnitHashes'

 L.  71       154  SETUP_LOOP          228  'to 228'
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                modelXbrl
              160  LOAD_ATTR                units
              162  LOAD_ATTR                values
              164  CALL_FUNCTION_0       0  '0 positional arguments'
              166  GET_ITER         
              168  FOR_ITER            226  'to 226'
              170  STORE_FAST               'unit'

 L.  72       172  LOAD_FAST                'unit'
              174  LOAD_ATTR                hash
              176  STORE_FAST               'h'

 L.  73       178  LOAD_FAST                'h'
              180  LOAD_FAST                'uniqueUnitHashes'
              182  COMPARE_OP               in
              184  POP_JUMP_IF_FALSE   216  'to 216'

 L.  74       186  LOAD_FAST                'unit'
              188  LOAD_ATTR                isEqualTo
              190  LOAD_FAST                'uniqueUnitHashes'
              192  LOAD_FAST                'h'
              194  BINARY_SUBSCR    
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  POP_JUMP_IF_FALSE   224  'to 224'

 L.  75       200  LOAD_FAST                'uniqueUnitHashes'
              202  LOAD_FAST                'h'
              204  BINARY_SUBSCR    
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                mapUnit
              210  LOAD_FAST                'unit'
              212  STORE_SUBSCR     
              214  JUMP_BACK           168  'to 168'
              216  ELSE                     '224'

 L.  77       216  LOAD_FAST                'unit'
              218  LOAD_FAST                'uniqueUnitHashes'
              220  LOAD_FAST                'h'
              222  STORE_SUBSCR     
            224_0  COME_FROM           198  '198'
              224  JUMP_BACK           168  'to 168'
              226  POP_BLOCK        
            228_0  COME_FROM_LOOP      154  '154'

 L.  78       228  LOAD_FAST                'self'
              230  LOAD_ATTR                modelXbrl
              232  LOAD_ATTR                profileActivity
              234  LOAD_STR                 '... identify equal units'
              236  LOAD_CONST               1.0
              238  LOAD_CONST               ('minTimeToShow',)
              240  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              242  POP_TOP          

 L.  82       244  SETUP_LOOP          428  'to 428'
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                modelXbrl
              250  LOAD_ATTR                baseSets
              252  LOAD_ATTR                keys
              254  CALL_FUNCTION_0       0  '0 positional arguments'
              256  GET_ITER         
              258  FOR_ITER            426  'to 426'
              260  STORE_FAST               'baseSetKey'

 L.  83       262  LOAD_FAST                'baseSetKey'
              264  UNPACK_SEQUENCE_4     4 
              266  STORE_FAST               'arcrole'
              268  STORE_FAST               'ELR'
              270  STORE_FAST               'linkqname'
              272  STORE_FAST               'arcqname'

 L.  84       274  LOAD_FAST                'ELR'
              276  POP_JUMP_IF_FALSE   258  'to 258'
              280  LOAD_FAST                'linkqname'
              282  POP_JUMP_IF_FALSE   258  'to 258'
              286  LOAD_FAST                'arcqname'
              288  POP_JUMP_IF_FALSE   258  'to 258'

 L.  85       292  LOAD_FAST                'arcrole'
              294  LOAD_GLOBAL              XbrlConst
              296  LOAD_ATTR                essenceAlias
              298  LOAD_GLOBAL              XbrlConst
              300  LOAD_ATTR                requiresElement
              302  BUILD_TUPLE_2         2 
              304  COMPARE_OP               in
              306  POP_JUMP_IF_FALSE   258  'to 258'

 L.  86       310  LOAD_GLOBAL              XbrlConst
              312  LOAD_ATTR                essenceAlias
              314  LOAD_FAST                'self'
              316  LOAD_ATTR                conceptsInEssencesAlias

 L.  87       318  LOAD_GLOBAL              XbrlConst
              320  LOAD_ATTR                requiresElement
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                conceptsInRequiresElement
              326  BUILD_MAP_2           2 
              328  LOAD_FAST                'arcrole'
              330  BINARY_SUBSCR    
              332  STORE_FAST               'conceptsSet'

 L.  88       334  SETUP_LOOP          422  'to 422'
              336  LOAD_FAST                'self'
              338  LOAD_ATTR                modelXbrl
              340  LOAD_ATTR                relationshipSet
              342  LOAD_FAST                'arcrole'
              344  LOAD_FAST                'ELR'
              346  LOAD_FAST                'linkqname'
              348  LOAD_FAST                'arcqname'
              350  CALL_FUNCTION_4       4  '4 positional arguments'
              352  LOAD_ATTR                modelRelationships
              354  GET_ITER         
              356  FOR_ITER            420  'to 420'
              358  STORE_FAST               'modelRel'

 L.  89       360  SETUP_LOOP          416  'to 416'
              362  LOAD_FAST                'modelRel'
              364  LOAD_ATTR                fromModelObject
              366  LOAD_FAST                'modelRel'
              368  LOAD_ATTR                toModelObject
              370  BUILD_TUPLE_2         2 
              372  GET_ITER         
              374  FOR_ITER            414  'to 414'
              376  STORE_FAST               'concept'

 L.  90       378  LOAD_FAST                'concept'
              380  LOAD_CONST               None
              382  COMPARE_OP               is-not
              384  POP_JUMP_IF_FALSE   374  'to 374'
              388  LOAD_FAST                'concept'
              390  LOAD_ATTR                qname
              392  LOAD_CONST               None
              394  COMPARE_OP               is-not
              396  POP_JUMP_IF_FALSE   374  'to 374'

 L.  91       400  LOAD_FAST                'conceptsSet'
              402  LOAD_ATTR                add
              404  LOAD_FAST                'concept'
              406  CALL_FUNCTION_1       1  '1 positional argument'
              408  POP_TOP          
              410  JUMP_BACK           374  'to 374'
              414  POP_BLOCK        
            416_0  COME_FROM_LOOP      360  '360'
              416  JUMP_BACK           356  'to 356'
              420  POP_BLOCK        
            422_0  COME_FROM_LOOP      334  '334'
              422  JUMP_BACK           258  'to 258'
              426  POP_BLOCK        
            428_0  COME_FROM_LOOP      244  '244'

 L.  92       428  LOAD_FAST                'self'
              430  LOAD_ATTR                modelXbrl
              432  LOAD_ATTR                profileActivity
              434  LOAD_STR                 '... identify requires-element and esseance-aliased concepts'
              436  LOAD_CONST               1.0
              438  LOAD_CONST               ('minTimeToShow',)
              440  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              442  POP_TOP          

 L.  94       444  LOAD_FAST                'self'
              446  LOAD_ATTR                bindFacts
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                modelXbrl
              452  LOAD_ATTR                facts
              454  LOAD_FAST                'self'
              456  LOAD_ATTR                modelXbrl
              458  LOAD_ATTR                modelDocument
              460  LOAD_ATTR                xmlRootElement
              462  BUILD_LIST_1          1 
              464  CALL_FUNCTION_2       2  '2 positional arguments'
              466  POP_TOP          

 L.  95       468  LOAD_FAST                'self'
              470  LOAD_ATTR                modelXbrl
              472  LOAD_ATTR                profileActivity
              474  LOAD_STR                 '... bind facts'
              476  LOAD_CONST               1.0
              478  LOAD_CONST               ('minTimeToShow',)
              480  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              482  POP_TOP          

 L.  98       484  SETUP_LOOP         1844  'to 1844'
              488  LOAD_FAST                'self'
              490  LOAD_ATTR                modelXbrl
              492  LOAD_ATTR                baseSets
              494  LOAD_ATTR                keys
              496  CALL_FUNCTION_0       0  '0 positional arguments'
              498  GET_ITER         
              500  FOR_ITER           1842  'to 1842'
              504  STORE_FAST               'baseSetKey'

 L.  99       506  LOAD_FAST                'baseSetKey'
              508  UNPACK_SEQUENCE_4     4 
              510  STORE_FAST               'arcrole'
              512  STORE_FAST               'ELR'
              514  STORE_FAST               'linkqname'
              516  STORE_FAST               'arcqname'

 L. 100       518  LOAD_FAST                'ELR'
              520  POP_JUMP_IF_FALSE   500  'to 500'
              524  LOAD_FAST                'linkqname'
              526  POP_JUMP_IF_FALSE   500  'to 500'
              530  LOAD_FAST                'arcqname'
              532  POP_JUMP_IF_FALSE   500  'to 500'

 L. 101       536  LOAD_FAST                'arcrole'
              538  LOAD_GLOBAL              XbrlConst
              540  LOAD_ATTR                summationItem
              542  LOAD_GLOBAL              XbrlConst
              544  LOAD_ATTR                essenceAlias
              546  LOAD_GLOBAL              XbrlConst
              548  LOAD_ATTR                requiresElement
              550  BUILD_TUPLE_3         3 
              552  COMPARE_OP               in
              554  POP_JUMP_IF_FALSE   500  'to 500'

 L. 102       558  LOAD_FAST                'self'
              560  LOAD_ATTR                modelXbrl
              562  LOAD_ATTR                relationshipSet
              564  LOAD_FAST                'arcrole'
              566  LOAD_FAST                'ELR'
              568  LOAD_FAST                'linkqname'
              570  LOAD_FAST                'arcqname'
              572  CALL_FUNCTION_4       4  '4 positional arguments'
              574  STORE_FAST               'relsSet'

 L. 103       576  LOAD_FAST                'arcrole'
              578  LOAD_GLOBAL              XbrlConst
              580  LOAD_ATTR                summationItem
              582  COMPARE_OP               ==
              584  POP_JUMP_IF_FALSE  1368  'to 1368'

 L. 104       588  LOAD_FAST                'relsSet'
              590  LOAD_ATTR                fromModelObjects
              592  CALL_FUNCTION_0       0  '0 positional arguments'
              594  STORE_FAST               'fromRelationships'

 L. 105       596  SETUP_LOOP         1838  'to 1838'
              600  LOAD_FAST                'fromRelationships'
              602  LOAD_ATTR                items
              604  CALL_FUNCTION_0       0  '0 positional arguments'
              606  GET_ITER         
              608  FOR_ITER           1362  'to 1362'
              612  UNPACK_SEQUENCE_2     2 
              614  STORE_FAST               'sumConcept'
              616  STORE_FAST               'modelRels'

 L. 106       618  LOAD_FAST                'self'
              620  LOAD_ATTR                sumConceptBindKeys
              622  LOAD_FAST                'sumConcept'
              624  BINARY_SUBSCR    
              626  STORE_FAST               'sumBindingKeys'

 L. 107       628  LOAD_GLOBAL              set
              630  CALL_FUNCTION_0       0  '0 positional arguments'
              632  STORE_FAST               'dupBindingKeys'

 L. 108       634  LOAD_GLOBAL              set
              636  CALL_FUNCTION_0       0  '0 positional arguments'
              638  STORE_FAST               'boundSumKeys'

 L. 110       640  SETUP_LOOP          706  'to 706'
              642  LOAD_FAST                'modelRels'
              644  GET_ITER         
              646  FOR_ITER            704  'to 704'
              648  STORE_FAST               'modelRel'

 L. 111       650  LOAD_FAST                'modelRel'
              652  LOAD_ATTR                toModelObject
              654  STORE_FAST               'itemConcept'

 L. 112       656  LOAD_FAST                'itemConcept'
              658  LOAD_CONST               None
              660  COMPARE_OP               is-not
              662  POP_JUMP_IF_FALSE   646  'to 646'
              666  LOAD_FAST                'itemConcept'
              668  LOAD_ATTR                qname
              670  LOAD_CONST               None
              672  COMPARE_OP               is-not
              674  POP_JUMP_IF_FALSE   646  'to 646'

 L. 113       678  LOAD_FAST                'self'
              680  LOAD_ATTR                itemConceptBindKeys
              682  LOAD_FAST                'itemConcept'
              684  BINARY_SUBSCR    
              686  STORE_FAST               'itemBindingKeys'

 L. 114       688  LOAD_FAST                'boundSumKeys'
              690  LOAD_FAST                'sumBindingKeys'
              692  LOAD_FAST                'itemBindingKeys'
              694  BINARY_AND       
              696  INPLACE_OR       
              698  STORE_FAST               'boundSumKeys'
              700  JUMP_BACK           646  'to 646'
              704  POP_BLOCK        
            706_0  COME_FROM_LOOP      640  '640'

 L. 116       706  LOAD_GLOBAL              defaultdict
              708  LOAD_GLOBAL              decimal
              710  LOAD_ATTR                Decimal
              712  CALL_FUNCTION_1       1  '1 positional argument'
              714  STORE_FAST               'boundSums'

 L. 117       716  LOAD_GLOBAL              defaultdict
              718  LOAD_GLOBAL              list
              720  CALL_FUNCTION_1       1  '1 positional argument'
              722  STORE_FAST               'boundSummationItems'

 L. 118       724  SETUP_LOOP          924  'to 924'
              726  LOAD_FAST                'modelRels'
              728  GET_ITER         
              730  FOR_ITER            922  'to 922'
              732  STORE_FAST               'modelRel'

 L. 119       734  LOAD_FAST                'modelRel'
              736  LOAD_ATTR                weightDecimal
              738  STORE_FAST               'weight'

 L. 120       740  LOAD_FAST                'modelRel'
              742  LOAD_ATTR                toModelObject
              744  STORE_FAST               'itemConcept'

 L. 121       746  LOAD_FAST                'itemConcept'
              748  LOAD_CONST               None
              750  COMPARE_OP               is-not
              752  POP_JUMP_IF_FALSE   730  'to 730'

 L. 122       756  SETUP_LOOP          918  'to 918'
              758  LOAD_FAST                'boundSumKeys'
              760  GET_ITER         
              762  FOR_ITER            916  'to 916'
              764  STORE_FAST               'itemBindKey'

 L. 123       766  LOAD_FAST                'itemBindKey'
              768  UNPACK_SEQUENCE_3     3 
              770  STORE_FAST               'ancestor'
              772  STORE_FAST               'contextHash'
              774  STORE_FAST               'unit'

 L. 124       776  LOAD_FAST                'itemConcept'
              778  LOAD_FAST                'ancestor'
              780  LOAD_FAST                'contextHash'
              782  LOAD_FAST                'unit'
              784  BUILD_TUPLE_4         4 
              786  STORE_FAST               'factKey'

 L. 125       788  LOAD_FAST                'factKey'
              790  LOAD_FAST                'self'
              792  LOAD_ATTR                itemFacts
              794  COMPARE_OP               in
              796  POP_JUMP_IF_FALSE   762  'to 762'

 L. 126       800  SETUP_LOOP          912  'to 912'
              802  LOAD_FAST                'self'
              804  LOAD_ATTR                itemFacts
              806  LOAD_FAST                'factKey'
              808  BINARY_SUBSCR    
              810  GET_ITER         
              812  FOR_ITER            910  'to 910'
              814  STORE_FAST               'fact'

 L. 127       816  LOAD_FAST                'fact'
              818  LOAD_FAST                'self'
              820  LOAD_ATTR                duplicatedFacts
              822  COMPARE_OP               in
              824  POP_JUMP_IF_FALSE   840  'to 840'

 L. 128       828  LOAD_FAST                'dupBindingKeys'
              830  LOAD_ATTR                add
              832  LOAD_FAST                'itemBindKey'
              834  CALL_FUNCTION_1       1  '1 positional argument'
              836  POP_TOP          
              838  JUMP_FORWARD        906  'to 906'
              840  ELSE                     '906'

 L. 129       840  LOAD_FAST                'fact'
              842  LOAD_FAST                'self'
              844  LOAD_ATTR                consistentDupFacts
              846  COMPARE_OP               not-in
              848  POP_JUMP_IF_FALSE   812  'to 812'

 L. 130       852  LOAD_GLOBAL              roundFact
              854  LOAD_FAST                'fact'
              856  LOAD_FAST                'self'
              858  LOAD_ATTR                inferDecimals
              860  CALL_FUNCTION_2       2  '2 positional arguments'
              862  STORE_FAST               'roundedValue'

 L. 131       864  LOAD_FAST                'boundSums'
              866  LOAD_FAST                'itemBindKey'
              868  DUP_TOP_TWO      
              870  BINARY_SUBSCR    
              872  LOAD_FAST                'roundedValue'
              874  LOAD_FAST                'weight'
              876  BINARY_MULTIPLY  
              878  INPLACE_ADD      
              880  ROT_THREE        
              882  STORE_SUBSCR     

 L. 132       884  LOAD_FAST                'boundSummationItems'
              886  LOAD_FAST                'itemBindKey'
              888  BINARY_SUBSCR    
              890  LOAD_ATTR                append
              892  LOAD_GLOBAL              wrappedFactWithWeight
              894  LOAD_FAST                'fact'
              896  LOAD_FAST                'weight'
              898  LOAD_FAST                'roundedValue'
              900  CALL_FUNCTION_3       3  '3 positional arguments'
              902  CALL_FUNCTION_1       1  '1 positional argument'
              904  POP_TOP          
            906_0  COME_FROM           838  '838'
              906  JUMP_BACK           812  'to 812'
              910  POP_BLOCK        
            912_0  COME_FROM_LOOP      800  '800'
              912  JUMP_BACK           762  'to 762'
              916  POP_BLOCK        
            918_0  COME_FROM_LOOP      756  '756'
              918  JUMP_BACK           730  'to 730'
              922  POP_BLOCK        
            924_0  COME_FROM_LOOP      724  '724'

 L. 133       924  SETUP_LOOP         1350  'to 1350'
              928  LOAD_FAST                'boundSumKeys'
              930  GET_ITER         
              932  FOR_ITER           1348  'to 1348'
              936  STORE_FAST               'sumBindKey'

 L. 134       938  LOAD_FAST                'sumBindKey'
              940  UNPACK_SEQUENCE_3     3 
              942  STORE_FAST               'ancestor'
              944  STORE_FAST               'contextHash'
              946  STORE_FAST               'unit'

 L. 135       948  LOAD_FAST                'sumConcept'
              950  LOAD_FAST                'ancestor'
              952  LOAD_FAST                'contextHash'
              954  LOAD_FAST                'unit'
              956  BUILD_TUPLE_4         4 
              958  STORE_FAST               'factKey'

 L. 136       960  LOAD_FAST                'factKey'
              962  LOAD_FAST                'self'
              964  LOAD_ATTR                sumFacts
              966  COMPARE_OP               in
              968  POP_JUMP_IF_FALSE   932  'to 932'

 L. 137       972  LOAD_FAST                'self'
              974  LOAD_ATTR                sumFacts
              976  LOAD_FAST                'factKey'
              978  BINARY_SUBSCR    
              980  STORE_FAST               'sumFacts'

 L. 138       982  SETUP_LOOP         1344  'to 1344'
              986  LOAD_FAST                'sumFacts'
              988  GET_ITER         
              990  FOR_ITER           1342  'to 1342'
              994  STORE_FAST               'fact'

 L. 139       996  LOAD_FAST                'fact'
              998  LOAD_FAST                'self'
             1000  LOAD_ATTR                duplicatedFacts
             1002  COMPARE_OP               in
             1004  POP_JUMP_IF_FALSE  1022  'to 1022'

 L. 140      1008  LOAD_FAST                'dupBindingKeys'
             1010  LOAD_ATTR                add
             1012  LOAD_FAST                'sumBindKey'
             1014  CALL_FUNCTION_1       1  '1 positional argument'
             1016  POP_TOP          
             1018  JUMP_BACK           990  'to 990'
             1022  ELSE                     '1340'

 L. 141      1022  LOAD_FAST                'sumBindKey'
             1024  LOAD_FAST                'dupBindingKeys'
             1026  COMPARE_OP               not-in
             1028  POP_JUMP_IF_FALSE   990  'to 990'
             1032  LOAD_FAST                'fact'
             1034  LOAD_FAST                'self'
             1036  LOAD_ATTR                consistentDupFacts
             1038  COMPARE_OP               not-in
             1040  POP_JUMP_IF_FALSE   990  'to 990'

 L. 142      1044  LOAD_GLOBAL              roundFact
             1046  LOAD_FAST                'fact'
             1048  LOAD_FAST                'self'
             1050  LOAD_ATTR                inferDecimals
             1052  CALL_FUNCTION_2       2  '2 positional arguments'
             1054  STORE_FAST               'roundedSum'

 L. 143      1056  LOAD_GLOBAL              roundFact
             1058  LOAD_FAST                'fact'
             1060  LOAD_FAST                'self'
             1062  LOAD_ATTR                inferDecimals
             1064  LOAD_FAST                'boundSums'
             1066  LOAD_FAST                'sumBindKey'
             1068  BINARY_SUBSCR    
             1070  LOAD_CONST               ('vDecimal',)
             1072  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1074  STORE_FAST               'roundedItemsSum'

 L. 144      1076  LOAD_FAST                'roundedItemsSum'
             1078  LOAD_GLOBAL              roundFact
             1080  LOAD_FAST                'fact'
             1082  LOAD_FAST                'self'
             1084  LOAD_ATTR                inferDecimals
             1086  CALL_FUNCTION_2       2  '2 positional arguments'
             1088  COMPARE_OP               !=
             1090  POP_JUMP_IF_FALSE   990  'to 990'

 L. 145      1094  LOAD_GLOBAL              inferredDecimals
             1096  LOAD_FAST                'fact'
             1098  CALL_FUNCTION_1       1  '1 positional argument'
             1100  STORE_FAST               'd'

 L. 146      1102  LOAD_GLOBAL              isnan
             1104  LOAD_FAST                'd'
             1106  CALL_FUNCTION_1       1  '1 positional argument'
             1108  POP_JUMP_IF_TRUE   1122  'to 1122'
             1112  LOAD_GLOBAL              isinf
             1114  LOAD_FAST                'd'
             1116  CALL_FUNCTION_1       1  '1 positional argument'
           1118_0  COME_FROM          1108  '1108'
             1118  POP_JUMP_IF_FALSE  1126  'to 1126'

 L. 146      1122  LOAD_CONST               4
             1124  STORE_FAST               'd'
           1126_0  COME_FROM          1118  '1118'

 L. 147      1126  LOAD_FAST                'boundSummationItems'
             1128  LOAD_FAST                'sumBindKey'
             1130  BINARY_SUBSCR    
             1132  STORE_FAST               '_boundSummationItems'

 L. 148      1134  BUILD_LIST_0          0 
             1136  STORE_FAST               'unreportedContribingItemQnames'

 L. 149      1138  SETUP_LOOP         1206  'to 1206'
             1140  LOAD_FAST                'modelRels'
             1142  GET_ITER         
             1144  FOR_ITER           1204  'to 1204'
             1146  STORE_FAST               'modelRel'

 L. 150      1148  LOAD_FAST                'modelRel'
             1150  LOAD_ATTR                toModelObject
             1152  STORE_FAST               'itemConcept'

 L. 151      1154  LOAD_FAST                'itemConcept'
             1156  LOAD_CONST               None
             1158  COMPARE_OP               is-not
             1160  POP_JUMP_IF_FALSE  1144  'to 1144'

 L. 152      1164  LOAD_FAST                'itemConcept'
             1166  LOAD_FAST                'ancestor'
             1168  LOAD_FAST                'contextHash'
             1170  LOAD_FAST                'unit'
             1172  BUILD_TUPLE_4         4 
             1174  LOAD_FAST                'self'
             1176  LOAD_ATTR                itemFacts
             1178  COMPARE_OP               not-in
             1180  POP_JUMP_IF_FALSE  1144  'to 1144'

 L. 153      1184  LOAD_FAST                'unreportedContribingItemQnames'
             1186  LOAD_ATTR                append
             1188  LOAD_GLOBAL              str
             1190  LOAD_FAST                'itemConcept'
             1192  LOAD_ATTR                qname
             1194  CALL_FUNCTION_1       1  '1 positional argument'
             1196  CALL_FUNCTION_1       1  '1 positional argument'
             1198  POP_TOP          
             1200  JUMP_BACK          1144  'to 1144'
             1204  POP_BLOCK        
           1206_0  COME_FROM_LOOP     1138  '1138'

 L. 154      1206  LOAD_FAST                'self'
             1208  LOAD_ATTR                modelXbrl
             1210  LOAD_ATTR                log
             1212  LOAD_STR                 'INCONSISTENCY'
             1214  LOAD_STR                 'xbrl.5.2.5.2:calcInconsistency'

 L. 155      1216  LOAD_GLOBAL              _
             1218  LOAD_STR                 'Calculation inconsistent from %(concept)s in link role %(linkrole)s reported sum %(reportedSum)s computed sum %(computedSum)s context %(contextID)s unit %(unitID)s unreportedContributingItems %(unreportedContributors)s'
             1220  CALL_FUNCTION_1       1  '1 positional argument'

 L. 156      1222  LOAD_GLOBAL              wrappedSummationAndItems
             1224  LOAD_FAST                'fact'
             1226  LOAD_FAST                'roundedSum'
             1228  LOAD_FAST                '_boundSummationItems'
             1230  CALL_FUNCTION_3       3  '3 positional arguments'

 L. 157      1232  LOAD_FAST                'sumConcept'
             1234  LOAD_ATTR                qname
             1236  LOAD_FAST                'ELR'

 L. 158      1238  LOAD_FAST                'self'
             1240  LOAD_ATTR                modelXbrl
             1242  LOAD_ATTR                roleTypeDefinition
             1244  LOAD_FAST                'ELR'
             1246  CALL_FUNCTION_1       1  '1 positional argument'

 L. 159      1248  LOAD_GLOBAL              Locale
             1250  LOAD_ATTR                format_decimal
             1252  LOAD_FAST                'self'
             1254  LOAD_ATTR                modelXbrl
             1256  LOAD_ATTR                locale
             1258  LOAD_FAST                'roundedSum'
             1260  LOAD_CONST               1
             1262  LOAD_GLOBAL              max
             1264  LOAD_FAST                'd'
             1266  LOAD_CONST               0
             1268  CALL_FUNCTION_2       2  '2 positional arguments'
             1270  CALL_FUNCTION_4       4  '4 positional arguments'

 L. 160      1272  LOAD_GLOBAL              Locale
             1274  LOAD_ATTR                format_decimal
             1276  LOAD_FAST                'self'
             1278  LOAD_ATTR                modelXbrl
             1280  LOAD_ATTR                locale
             1282  LOAD_FAST                'roundedItemsSum'
             1284  LOAD_CONST               1
             1286  LOAD_GLOBAL              max
             1288  LOAD_FAST                'd'
             1290  LOAD_CONST               0
             1292  CALL_FUNCTION_2       2  '2 positional arguments'
             1294  CALL_FUNCTION_4       4  '4 positional arguments'

 L. 161      1296  LOAD_FAST                'fact'
             1298  LOAD_ATTR                context
             1300  LOAD_ATTR                id
             1302  LOAD_FAST                'fact'
             1304  LOAD_ATTR                unit
             1306  LOAD_ATTR                id

 L. 162      1308  LOAD_STR                 ', '
             1310  LOAD_ATTR                join
             1312  LOAD_FAST                'unreportedContribingItemQnames'
             1314  CALL_FUNCTION_1       1  '1 positional argument'
             1316  JUMP_IF_TRUE_OR_POP  1322  'to 1322'
             1320  LOAD_STR                 'none'
           1322_0  COME_FROM          1316  '1316'
             1322  LOAD_CONST               ('modelObject', 'concept', 'linkrole', 'linkroleDefinition', 'reportedSum', 'computedSum', 'contextID', 'unitID', 'unreportedContributors')
             1324  CALL_FUNCTION_KW_12    12  '12 total positional and keyword args'
             1326  POP_TOP          

 L. 163      1328  LOAD_FAST                'unreportedContribingItemQnames'
             1330  LOAD_CONST               None
             1332  LOAD_CONST               None
             1334  BUILD_SLICE_2         2 
             1336  DELETE_SUBSCR    
             1338  JUMP_BACK           990  'to 990'
             1342  POP_BLOCK        
           1344_0  COME_FROM_LOOP      982  '982'
             1344  JUMP_BACK           932  'to 932'
             1348  POP_BLOCK        
           1350_0  COME_FROM_LOOP      924  '924'

 L. 164      1350  LOAD_FAST                'boundSummationItems'
             1352  LOAD_ATTR                clear
             1354  CALL_FUNCTION_0       0  '0 positional arguments'
             1356  POP_TOP          
             1358  JUMP_BACK           608  'to 608'
             1362  POP_BLOCK        
             1364  JUMP_BACK           500  'to 500'
             1368  ELSE                     '1840'

 L. 165      1368  LOAD_FAST                'arcrole'
             1370  LOAD_GLOBAL              XbrlConst
             1372  LOAD_ATTR                essenceAlias
             1374  COMPARE_OP               ==
             1376  POP_JUMP_IF_FALSE  1728  'to 1728'

 L. 166      1380  SETUP_LOOP         1838  'to 1838'
             1384  LOAD_FAST                'relsSet'
             1386  LOAD_ATTR                modelRelationships
             1388  GET_ITER         
             1390  FOR_ITER           1724  'to 1724'
             1394  STORE_FAST               'modelRel'

 L. 167      1396  LOAD_FAST                'modelRel'
             1398  LOAD_ATTR                fromModelObject
             1400  STORE_FAST               'essenceConcept'

 L. 168      1402  LOAD_FAST                'modelRel'
             1404  LOAD_ATTR                toModelObject
             1406  STORE_FAST               'aliasConcept'

 L. 169      1408  LOAD_FAST                'self'
             1410  LOAD_ATTR                esAlConceptBindKeys
             1412  LOAD_FAST                'essenceConcept'
             1414  BINARY_SUBSCR    
             1416  STORE_FAST               'essenceBindingKeys'

 L. 170      1418  LOAD_FAST                'self'
             1420  LOAD_ATTR                esAlConceptBindKeys
             1422  LOAD_FAST                'aliasConcept'
             1424  BINARY_SUBSCR    
             1426  STORE_FAST               'aliasBindingKeys'

 L. 171      1428  SETUP_LOOP         1720  'to 1720'
             1432  LOAD_FAST                'essenceBindingKeys'
             1434  LOAD_FAST                'aliasBindingKeys'
             1436  BINARY_AND       
             1438  GET_ITER         
             1440  FOR_ITER           1718  'to 1718'
             1444  STORE_FAST               'esAlBindKey'

 L. 172      1446  LOAD_FAST                'esAlBindKey'
             1448  UNPACK_SEQUENCE_2     2 
             1450  STORE_FAST               'ancestor'
             1452  STORE_FAST               'contextHash'

 L. 173      1454  LOAD_FAST                'essenceConcept'
             1456  LOAD_FAST                'ancestor'
             1458  LOAD_FAST                'contextHash'
             1460  BUILD_TUPLE_3         3 
             1462  STORE_FAST               'essenceFactsKey'

 L. 174      1464  LOAD_FAST                'aliasConcept'
             1466  LOAD_FAST                'ancestor'
             1468  LOAD_FAST                'contextHash'
             1470  BUILD_TUPLE_3         3 
             1472  STORE_FAST               'aliasFactsKey'

 L. 175      1474  LOAD_FAST                'essenceFactsKey'
             1476  LOAD_FAST                'self'
             1478  LOAD_ATTR                esAlFacts
             1480  COMPARE_OP               in
             1482  POP_JUMP_IF_FALSE  1440  'to 1440'
             1486  LOAD_FAST                'aliasFactsKey'
             1488  LOAD_FAST                'self'
             1490  LOAD_ATTR                esAlFacts
             1492  COMPARE_OP               in
             1494  POP_JUMP_IF_FALSE  1440  'to 1440'

 L. 176      1498  SETUP_LOOP         1714  'to 1714'
             1500  LOAD_FAST                'self'
             1502  LOAD_ATTR                esAlFacts
             1504  LOAD_FAST                'essenceFactsKey'
             1506  BINARY_SUBSCR    
             1508  GET_ITER         
             1510  FOR_ITER           1712  'to 1712'
             1512  STORE_FAST               'eF'

 L. 177      1514  SETUP_LOOP         1708  'to 1708'
             1516  LOAD_FAST                'self'
             1518  LOAD_ATTR                esAlFacts
             1520  LOAD_FAST                'aliasFactsKey'
             1522  BINARY_SUBSCR    
             1524  GET_ITER         
             1526  FOR_ITER           1706  'to 1706'
             1528  STORE_FAST               'aF'

 L. 178      1530  LOAD_FAST                'self'
             1532  LOAD_ATTR                mapUnit
             1534  LOAD_ATTR                get
             1536  LOAD_FAST                'eF'
             1538  LOAD_ATTR                unit
             1540  LOAD_FAST                'eF'
             1542  LOAD_ATTR                unit
             1544  CALL_FUNCTION_2       2  '2 positional arguments'
             1546  STORE_FAST               'essenceUnit'

 L. 179      1548  LOAD_FAST                'self'
             1550  LOAD_ATTR                mapUnit
             1552  LOAD_ATTR                get
             1554  LOAD_FAST                'aF'
             1556  LOAD_ATTR                unit
             1558  LOAD_FAST                'aF'
             1560  LOAD_ATTR                unit
             1562  CALL_FUNCTION_2       2  '2 positional arguments'
             1564  STORE_FAST               'aliasUnit'

 L. 180      1566  LOAD_FAST                'essenceUnit'
             1568  LOAD_FAST                'aliasUnit'
             1570  COMPARE_OP               !=
             1572  POP_JUMP_IF_FALSE  1632  'to 1632'

 L. 181      1576  LOAD_FAST                'self'
             1578  LOAD_ATTR                modelXbrl
             1580  LOAD_ATTR                log
             1582  LOAD_STR                 'INCONSISTENCY'
             1584  LOAD_STR                 'xbrl.5.2.6.2.2:essenceAliasUnitsInconsistency'

 L. 182      1586  LOAD_GLOBAL              _
             1588  LOAD_STR                 'Essence-Alias inconsistent units from %(essenceConcept)s to %(aliasConcept)s in link role %(linkrole)s context %(contextID)s'
             1590  CALL_FUNCTION_1       1  '1 positional argument'

 L. 183      1592  LOAD_FAST                'modelRel'
             1594  LOAD_FAST                'eF'
             1596  LOAD_FAST                'aF'
             1598  BUILD_TUPLE_3         3 

 L. 184      1600  LOAD_FAST                'essenceConcept'
             1602  LOAD_ATTR                qname
             1604  LOAD_FAST                'aliasConcept'
             1606  LOAD_ATTR                qname

 L. 185      1608  LOAD_FAST                'ELR'

 L. 186      1610  LOAD_FAST                'self'
             1612  LOAD_ATTR                modelXbrl
             1614  LOAD_ATTR                roleTypeDefinition
             1616  LOAD_FAST                'ELR'
             1618  CALL_FUNCTION_1       1  '1 positional argument'

 L. 187      1620  LOAD_FAST                'eF'
             1622  LOAD_ATTR                context
             1624  LOAD_ATTR                id
             1626  LOAD_CONST               ('modelObject', 'essenceConcept', 'aliasConcept', 'linkrole', 'linkroleDefinition', 'contextID')
             1628  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
             1630  POP_TOP          
           1632_0  COME_FROM          1572  '1572'

 L. 188      1632  LOAD_GLOBAL              XbrlUtil
             1634  LOAD_ATTR                vEqual
             1636  LOAD_FAST                'eF'
             1638  LOAD_FAST                'aF'
             1640  CALL_FUNCTION_2       2  '2 positional arguments'
             1642  POP_JUMP_IF_TRUE   1526  'to 1526'

 L. 189      1646  LOAD_FAST                'self'
             1648  LOAD_ATTR                modelXbrl
             1650  LOAD_ATTR                log
             1652  LOAD_STR                 'INCONSISTENCY'
             1654  LOAD_STR                 'xbrl.5.2.6.2.2:essenceAliasUnitsInconsistency'

 L. 190      1656  LOAD_GLOBAL              _
             1658  LOAD_STR                 'Essence-Alias inconsistent value from %(essenceConcept)s to %(aliasConcept)s in link role %(linkrole)s context %(contextID)s'
             1660  CALL_FUNCTION_1       1  '1 positional argument'

 L. 191      1662  LOAD_FAST                'modelRel'
             1664  LOAD_FAST                'eF'
             1666  LOAD_FAST                'aF'
             1668  BUILD_TUPLE_3         3 

 L. 192      1670  LOAD_FAST                'essenceConcept'
             1672  LOAD_ATTR                qname
             1674  LOAD_FAST                'aliasConcept'
             1676  LOAD_ATTR                qname

 L. 193      1678  LOAD_FAST                'ELR'

 L. 194      1680  LOAD_FAST                'self'
             1682  LOAD_ATTR                modelXbrl
             1684  LOAD_ATTR                roleTypeDefinition
             1686  LOAD_FAST                'ELR'
             1688  CALL_FUNCTION_1       1  '1 positional argument'

 L. 195      1690  LOAD_FAST                'eF'
             1692  LOAD_ATTR                context
             1694  LOAD_ATTR                id
             1696  LOAD_CONST               ('modelObject', 'essenceConcept', 'aliasConcept', 'linkrole', 'linkroleDefinition', 'contextID')
             1698  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
             1700  POP_TOP          
             1702  JUMP_BACK          1526  'to 1526'
             1706  POP_BLOCK        
           1708_0  COME_FROM_LOOP     1514  '1514'
             1708  JUMP_BACK          1510  'to 1510'
             1712  POP_BLOCK        
           1714_0  COME_FROM_LOOP     1498  '1498'
             1714  JUMP_BACK          1440  'to 1440'
             1718  POP_BLOCK        
           1720_0  COME_FROM_LOOP     1428  '1428'
             1720  JUMP_BACK          1390  'to 1390'
             1724  POP_BLOCK        
           1726_0  COME_FROM_LOOP     1380  '1380'
             1726  JUMP_FORWARD       1838  'to 1838'
             1728  ELSE                     '1838'

 L. 196      1728  LOAD_FAST                'arcrole'
             1730  LOAD_GLOBAL              XbrlConst
             1732  LOAD_ATTR                requiresElement
             1734  COMPARE_OP               ==
             1736  POP_JUMP_IF_FALSE   500  'to 500'

 L. 197      1740  SETUP_LOOP         1838  'to 1838'
             1742  LOAD_FAST                'relsSet'
             1744  LOAD_ATTR                modelRelationships
             1746  GET_ITER         
             1748  FOR_ITER           1836  'to 1836'
             1750  STORE_FAST               'modelRel'

 L. 198      1752  LOAD_FAST                'modelRel'
             1754  LOAD_ATTR                fromModelObject
             1756  STORE_FAST               'sourceConcept'

 L. 199      1758  LOAD_FAST                'modelRel'
             1760  LOAD_ATTR                toModelObject
             1762  STORE_FAST               'requiredConcept'

 L. 200      1764  LOAD_FAST                'sourceConcept'
             1766  LOAD_FAST                'self'
             1768  LOAD_ATTR                requiresElementFacts
             1770  COMPARE_OP               in
             1772  POP_JUMP_IF_FALSE  1748  'to 1748'

 L. 201      1776  LOAD_FAST                'requiredConcept'
             1778  LOAD_FAST                'self'
             1780  LOAD_ATTR                requiresElementFacts
             1782  COMPARE_OP               not-in
             1784  POP_JUMP_IF_FALSE  1748  'to 1748'

 L. 202      1788  LOAD_FAST                'self'
             1790  LOAD_ATTR                modelXbrl
             1792  LOAD_ATTR                log
             1794  LOAD_STR                 'INCONSISTENCY'
             1796  LOAD_STR                 'xbrl.5.2.6.2.4:requiresElementInconsistency'

 L. 203      1798  LOAD_GLOBAL              _
             1800  LOAD_STR                 'Requires-Element %(requiringConcept)s missing required fact for %(requiredConcept)s in link role %(linkrole)s'
             1802  CALL_FUNCTION_1       1  '1 positional argument'

 L. 204      1804  LOAD_FAST                'sourceConcept'

 L. 205      1806  LOAD_FAST                'sourceConcept'
             1808  LOAD_ATTR                qname
             1810  LOAD_FAST                'requiredConcept'
             1812  LOAD_ATTR                qname

 L. 206      1814  LOAD_FAST                'ELR'

 L. 207      1816  LOAD_FAST                'self'
             1818  LOAD_ATTR                modelXbrl
             1820  LOAD_ATTR                roleTypeDefinition
             1822  LOAD_FAST                'ELR'
             1824  CALL_FUNCTION_1       1  '1 positional argument'
             1826  LOAD_CONST               ('modelObject', 'requiringConcept', 'requiredConcept', 'linkrole', 'linkroleDefinition')
             1828  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
             1830  POP_TOP          
             1832  JUMP_BACK          1748  'to 1748'
             1836  POP_BLOCK        
           1838_0  COME_FROM_LOOP     1740  '1740'
           1838_1  COME_FROM          1726  '1726'
             1838  JUMP_BACK           500  'to 500'
             1842  POP_BLOCK        
           1844_0  COME_FROM_LOOP      484  '484'

 L. 208      1844  LOAD_FAST                'self'
             1846  LOAD_ATTR                modelXbrl
             1848  LOAD_ATTR                profileActivity
             1850  LOAD_STR                 '... find inconsistencies'
             1852  LOAD_CONST               1.0
             1854  LOAD_CONST               ('minTimeToShow',)
             1856  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1858  POP_TOP          

 L. 209      1860  LOAD_FAST                'self'
             1862  LOAD_ATTR                modelXbrl
             1864  LOAD_ATTR                profileActivity
             1866  CALL_FUNCTION_0       0  '0 positional arguments'
             1868  POP_TOP          

Parse error at or near `JUMP_BACK' instruction at offset 1364

    def bindFacts(self, facts, ancestors):
        for f in facts:
            concept = f.concept
            if concept is not None:
                if concept.isNumeric:
                    for ancestor in ancestors:
                        context = self.mapContext.get(f.context, f.context)
                        contextHash = context.contextNonDimAwareHash if context is not None else hash(None)
                        unit = self.mapUnit.get(f.unit, f.unit)
                        calcKey = (concept, ancestor, contextHash, unit)
                        if not f.isNil:
                            self.itemFacts[calcKey].append(f)
                            bindKey = (ancestor, contextHash, unit)
                            self.itemConceptBindKeys[concept].add(bindKey)

                    if not f.isNil:
                        self.sumFacts[calcKey].append(f)
                        self.sumConceptBindKeys[concept].add(bindKey)
                    if calcKey in self.duplicateKeyFacts:
                        fDup = self.duplicateKeyFacts[calcKey]
                        if self.deDuplicate:
                            if self.inferDecimals:
                                d = inferredDecimals(f)
                                dDup = inferredDecimals(fDup)
                                dMin = min((d, dDup))
                                pMin = None
                                hasAccuracy = not isnan(d) and not isnan(dDup)
                                fIsMorePrecise = d > dDup
                            else:
                                p = inferredPrecision(f)
                                pDup = inferredPrecision(fDup)
                                dMin = None
                                pMin = min((p, pDup))
                                hasAccuracy = p != 0
                                fIsMorePrecise = p > pDup
                        elif hasAccuracy and roundValue((f.value), precision=pMin, decimals=dMin) == roundValue((fDup.value), precision=pMin, decimals=dMin):
                            if fIsMorePrecise:
                                self.duplicateKeyFacts[calcKey] = f
                                self.consistentDupFacts.add(fDup)
                            else:
                                self.consistentDupFacts.add(f)
                        else:
                            self.duplicatedFacts.add(f)
                            self.duplicatedFacts.add(fDup)
                    else:
                        self.duplicatedFacts.add(f)
                        self.duplicatedFacts.add(fDup)
                else:
                    self.duplicateKeyFacts[calcKey] = f
            else:
                if concept.isTuple:
                    self.bindFacts(f.modelTupleFacts, ancestors + [f])
                if concept in self.conceptsInEssencesAlias:
                    if not f.isNil:
                        ancestor = ancestors[(-1)]
                        context = self.mapContext.get(f.context, f.context)
                        contextHash = context.contextNonDimAwareHash if context is not None else hash(None)
                        esAlKey = (concept, ancestor, contextHash)
                        self.esAlFacts[esAlKey].append(f)
                        bindKey = (ancestor, contextHash)
                        self.esAlConceptBindKeys[concept].add(bindKey)
                    if concept in self.conceptsInRequiresElement:
                        self.requiresElementFacts[concept].append(f)


def roundFact(fact, inferDecimals=False, vDecimal=None):
    if vDecimal is None:
        vStr = fact.value
        try:
            vDecimal = decimal.Decimal(vStr)
            vFloatFact = float(vStr)
        except (decimal.InvalidOperation, ValueError):
            vDecimal = NaN
            vFloatFact = floatNaN

    else:
        if vDecimal.is_nan():
            return vDecimal
        else:
            vStr = None
            try:
                vFloatFact = float(fact.value)
            except ValueError:
                vFloatFact = floatNaN

            dStr = fact.decimals
            pStr = fact.precision
            if dStr == 'INF' or pStr == 'INF':
                vRounded = vDecimal
            else:
                if inferDecimals:
                    if pStr:
                        p = int(pStr)
                        if p == 0:
                            vRounded = NaN
                        else:
                            if vDecimal == 0:
                                vRounded = ZERO
                            else:
                                vAbs = fabs(vFloatFact)
                                d = p - int(floor(log10(vAbs))) - 1
                                vRounded = decimalRound(vDecimal, d, decimal.ROUND_HALF_EVEN)
                    else:
                        if dStr:
                            d = int(dStr)
                            vRounded = decimalRound(vDecimal, d, decimal.ROUND_HALF_EVEN)
                        else:
                            vRounded = vDecimal
                else:
                    if dStr:
                        match = numberPattern.match(vStr if vStr else str(vDecimal))
                        if match:
                            nonZeroInt, period, zeroDec, nonZeroDec, e, exp = match.groups()
                            p = len(nonZeroInt) if (nonZeroInt and len(nonZeroInt) > 0) else (-len(zeroDec)) + int(exp) if (exp and len(exp) > 0) else 0 + int(dStr)
                        else:
                            p = 0
                    else:
                        if pStr:
                            p = int(pStr)
                        else:
                            p = None
                        if p == 0:
                            vRounded = NaN
                        else:
                            if vDecimal == 0:
                                vRounded = vDecimal
                            else:
                                if p is not None:
                                    vAbs = vDecimal.copy_abs()
                                    log = vAbs.log10()
                                    d = p - int(log) - (1 if vAbs >= 1 else 0)
                                    vRounded = decimalRound(vDecimal, d, decimal.ROUND_HALF_UP)
                                else:
                                    vRounded = vDecimal
            return vRounded


def decimalRound(x, d, rounding):
    if x.is_normal() and -28 <= d <= 28:
        if d >= 0:
            return x.quantize(ONE.scaleb(-d), rounding)
        return x.scaleb(d).quantize(ONE, rounding).scaleb(-d)
    else:
        return x


def inferredPrecision--- This code section failed: ---

 L. 364         0  LOAD_FAST                'fact'
                2  LOAD_ATTR                value
                4  STORE_FAST               'vStr'

 L. 365         6  LOAD_FAST                'fact'
                8  LOAD_ATTR                decimals
               10  STORE_FAST               'dStr'

 L. 366        12  LOAD_FAST                'fact'
               14  LOAD_ATTR                precision
               16  STORE_FAST               'pStr'

 L. 367        18  LOAD_FAST                'dStr'
               20  LOAD_STR                 'INF'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_TRUE     34  'to 34'
               26  LOAD_FAST                'pStr'
               28  LOAD_STR                 'INF'
               30  COMPARE_OP               ==
             32_0  COME_FROM            24  '24'
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 368        34  LOAD_GLOBAL              floatINF
               36  RETURN_END_IF    
             38_0  COME_FROM            32  '32'

 L. 369        38  SETUP_EXCEPT        184  'to 184'

 L. 370        40  LOAD_GLOBAL              float
               42  LOAD_FAST                'vStr'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  STORE_FAST               'vFloat'

 L. 371        48  LOAD_FAST                'dStr'
               50  POP_JUMP_IF_FALSE   172  'to 172'

 L. 372        52  LOAD_GLOBAL              numberPattern
               54  LOAD_ATTR                match
               56  LOAD_FAST                'vStr'
               58  POP_JUMP_IF_FALSE    64  'to 64'
               60  LOAD_FAST                'vStr'
               62  JUMP_FORWARD         70  'to 70'
               64  ELSE                     '70'
               64  LOAD_GLOBAL              str
               66  LOAD_FAST                'vFloat'
               68  CALL_FUNCTION_1       1  '1 positional argument'
             70_0  COME_FROM            62  '62'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  STORE_FAST               'match'

 L. 373        74  LOAD_FAST                'match'
               76  POP_JUMP_IF_FALSE   166  'to 166'

 L. 374        78  LOAD_FAST                'match'
               80  LOAD_ATTR                groups
               82  CALL_FUNCTION_0       0  '0 positional arguments'
               84  UNPACK_SEQUENCE_6     6 
               86  STORE_FAST               'nonZeroInt'
               88  STORE_FAST               'period'
               90  STORE_FAST               'zeroDec'
               92  STORE_FAST               'nonZeroDec'
               94  STORE_FAST               'e'
               96  STORE_FAST               'exp'

 L. 376        98  LOAD_FAST                'nonZeroInt'
              100  POP_JUMP_IF_FALSE   110  'to 110'
              102  LOAD_GLOBAL              len
              104  LOAD_FAST                'nonZeroInt'
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  JUMP_FORWARD        126  'to 126'
              110  ELSE                     '126'
              110  LOAD_FAST                'nonZeroDec'
              112  POP_JUMP_IF_FALSE   124  'to 124'
              114  LOAD_GLOBAL              len
              116  LOAD_FAST                'zeroDec'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  UNARY_NEGATIVE   
              122  JUMP_FORWARD        126  'to 126'
              124  ELSE                     '126'
              124  LOAD_CONST               0
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM           108  '108'
              126  LOAD_FAST                'exp'
              128  POP_JUMP_IF_FALSE   138  'to 138'
              130  LOAD_GLOBAL              int
              132  LOAD_FAST                'exp'
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  JUMP_FORWARD        140  'to 140'
              138  ELSE                     '140'
              138  LOAD_CONST               0
            140_0  COME_FROM           136  '136'
              140  BINARY_ADD       

 L. 377       142  LOAD_GLOBAL              int
              144  LOAD_FAST                'dStr'
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  BINARY_ADD       
              150  STORE_FAST               'p'

 L. 378       152  LOAD_FAST                'p'
              154  LOAD_CONST               0
              156  COMPARE_OP               <
              158  POP_JUMP_IF_FALSE   170  'to 170'

 L. 379       160  LOAD_CONST               0
              162  STORE_FAST               'p'
              164  JUMP_ABSOLUTE       180  'to 180'
              166  ELSE                     '170'

 L. 381       166  LOAD_CONST               0
              168  STORE_FAST               'p'
            170_0  COME_FROM           158  '158'
              170  JUMP_FORWARD        180  'to 180'
              172  ELSE                     '180'

 L. 383       172  LOAD_GLOBAL              int
              174  LOAD_FAST                'pStr'
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  RETURN_VALUE     
            180_0  COME_FROM           170  '170'
              180  POP_BLOCK        
              182  JUMP_FORWARD        204  'to 204'
            184_0  COME_FROM_EXCEPT     38  '38'

 L. 384       184  DUP_TOP          
              186  LOAD_GLOBAL              ValueError
              188  COMPARE_OP               exception-match
              190  POP_JUMP_IF_FALSE   202  'to 202'
              192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          

 L. 385       198  LOAD_GLOBAL              floatNaN
              200  RETURN_VALUE     
            202_0  COME_FROM           190  '190'
              202  END_FINALLY      
            204_0  COME_FROM           182  '182'

 L. 386       204  LOAD_FAST                'p'
              206  LOAD_CONST               0
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   216  'to 216'

 L. 387       212  LOAD_CONST               0
              214  RETURN_END_IF    
            216_0  COME_FROM           210  '210'

 L. 388       216  LOAD_FAST                'vFloat'
              218  LOAD_CONST               0
              220  COMPARE_OP               ==
              222  POP_JUMP_IF_FALSE   228  'to 228'

 L. 389       224  LOAD_CONST               0
              226  RETURN_END_IF    
            228_0  COME_FROM           222  '222'

 L. 391       228  LOAD_FAST                'p'
              230  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 180


def inferredDecimals(fact):
    vStr = fact.value
    dStr = fact.decimals
    pStr = fact.precision
    if dStr == 'INF' or pStr == 'INF':
        return floatINF
    else:
        try:
            if pStr:
                p = int(pStr)
                if p == 0:
                    return floatNaN
                else:
                    vFloat = float(vStr)
                    if vFloat == 0:
                        return floatINF
                    vAbs = fabs(vFloat)
                    return p - int(floor(log10(vAbs))) - 1
            else:
                if dStr:
                    return int(dStr)
        except ValueError:
            pass

        return floatNaN


def roundValue(value, precision=None, decimals=None, scale=None):
    try:
        vDecimal = decimal.Decimal(value)
        if scale:
            iScale = int(scale)
            vDecimal = vDecimal.scaleb(iScale)
        if precision is not None:
            vFloat = float(value)
            if scale:
                vFloat = pow(vFloat, iScale)
    except (decimal.InvalidOperation, ValueError):
        return NaN
    else:
        if precision is not None:
            if isinstance(precision, (int, float)) or precision == 'INF':
                precision = floatINF
            else:
                try:
                    precision = int(precision)
                except ValueError:
                    precision = floatNaN

                if isinf(precision):
                    vRounded = vDecimal
                else:
                    if precision == 0 or isnan(precision):
                        vRounded = NaN
                    else:
                        if vFloat == 0:
                            vRounded = ZERO
                        else:
                            vAbs = fabs(vFloat)
                            log = log10(vAbs)
                            d = precision - int(log) - (1 if vAbs >= 1 else 0)
                            vRounded = decimalRound(vDecimal, d, decimal.ROUND_HALF_UP)
        else:
            if decimals is not None:
                if isinstance(decimals, (int, float)) or decimals == 'INF':
                    decimals = floatINF
                else:
                    try:
                        decimals = int(decimals)
                    except ValueError:
                        decimals = floatNaN

                    if isinf(decimals):
                        vRounded = vDecimal
                    else:
                        if isnan(decimals):
                            vRounded = NaN
                        else:
                            vRounded = decimalRound(vDecimal, decimals, decimal.ROUND_HALF_EVEN)
            else:
                vRounded = vDecimal
            return vRounded


def insignificantDigits(value, precision=None, decimals=None, scale=None):
    try:
        vDecimal = decimal.Decimal(value)
        if scale:
            iScale = int(scale)
            vDecimal = vDecimal.scaleb(iScale)
        if precision is not None:
            vFloat = float(value)
            if scale:
                vFloat = pow(vFloat, iScale)
    except (decimal.InvalidOperation, ValueError):
        return
    else:
        if precision is not None:
            if not isinstance(precision, (int, float)):
                if precision == 'INF':
                    return
                try:
                    precision = int(precision)
                except ValueError:
                    return

            if isinf(precision) or precision == 0 or isnan(precision) or vFloat == 0:
                return
            vAbs = fabs(vFloat)
            log = log10(vAbs)
            decimals = precision - int(log) - (1 if vAbs >= 1 else 0)
        else:
            if decimals is not None:
                if not isinstance(decimals, (int, float)):
                    if decimals == 'INF':
                        return
                    try:
                        decimals = int(decimals)
                    except ValueError:
                        return

                    if isinf(decimals) or isnan(decimals):
                        return
            else:
                return
        if vDecimal.is_normal():
            if -28 <= decimals <= 28:
                if decimals > 0:
                    divisor = ONE.scaleb(-decimals)
                else:
                    divisor = ONE.scaleb(-decimals).quantize(ONE, decimal.ROUND_HALF_UP)
                insignificantDigits = abs(vDecimal) % divisor
                if insignificantDigits:
                    return (
                     vDecimal // divisor * divisor,
                     insignificantDigits)


def wrappedFactWithWeight(fact, weight, roundedValue):
    return ObjectPropertyViewWrapper(fact, (('weight', weight), ('roundedValue', roundedValue)))


def wrappedSummationAndItems(fact, roundedSum, boundSummationItems):
    """ ARELLE-281, replace: faster python-based hash (replace with hashlib for fewer collisions)
    itemValuesHash = hash( tuple(( hash(b.modelObject.qname), hash(b.extraProperties[1][1]) )
                                 # sort by qname so we don't care about reordering of summation terms
                                 for b in sorted(boundSummationItems,
                                                       key=lambda b: b.modelObject.qname)) )
    sumValueHash = hash( (hash(fact.qname), hash(roundedSum)) )
    """
    sha256 = hashlib.sha256()
    for b in sorted(boundSummationItems, key=(lambda b: b.modelObject.qname)):
        sha256.update(b.modelObject.qname.namespaceURI.encode('utf-8', 'replace'))
        sha256.update(b.modelObject.qname.localName.encode('utf-8', 'replace'))
        sha256.update(str(b.extraProperties[1][1]).encode('utf-8', 'replace'))

    itemValuesHash = sha256.hexdigest()
    sha256 = hashlib.sha256()
    sha256.update(fact.qname.namespaceURI.encode('utf-8', 'replace'))
    sha256.update(fact.qname.localName.encode('utf-8', 'replace'))
    sha256.update(str(roundedSum).encode('utf-8', 'replace'))
    sumValueHash = sha256.hexdigest()
    return [
     ObjectPropertyViewWrapper(fact, (
      (
       'sumValueHash', sumValueHash),
      (
       'itemValuesHash', itemValuesHash),
      (
       'roundedSum', roundedSum)))] + boundSummationItems