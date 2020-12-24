# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\ValidateXbrl.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 68760 bytes
"""
Created on Oct 17, 2010

@author: Mark V Systems Limited
(c) Copyright 2010 Mark V Systems Limited, All rights reserved.
"""
try:
    import regex as re
except ImportError:
    import re

from arelle import ModelDocument, XmlUtil, XbrlUtil, XbrlConst, ValidateXbrlCalcs, ValidateXbrlDimensions, ValidateXbrlDTS, ValidateFormula, ValidateUtr
from arelle import FunctionIxt
from arelle.ModelObject import ModelObject
from arelle.ModelDtsObject import ModelConcept
from arelle.ModelInstanceObject import ModelInlineFact
from arelle.ModelValue import qname
from arelle.PluginManager import pluginClassMethods
from arelle.XbrlConst import ixbrlAll
from arelle.XhtmlValidate import ixMsgCode
from arelle.XmlValidate import VALID
from collections import defaultdict
validateUniqueParticleAttribution = None
arcNamesTo21Resource = {
 'labelArc', 'referenceArc'}
xlinkTypeValues = {None, 'simple', 'extended', 'locator', 'arc', 'resource', 'title', 'none'}
xlinkActuateValues = {None, 'onLoad', 'onRequest', 'other', 'none'}
xlinkShowValues = {None, 'new', 'replace', 'embed', 'other', 'none'}
xlinkLabelAttributes = {'{http://www.w3.org/1999/xlink}label', '{http://www.w3.org/1999/xlink}from', '{http://www.w3.org/1999/xlink}to'}
periodTypeValues = {'instant', 'duration'}
balanceValues = {None, 'credit', 'debit'}
baseXbrliTypes = {
 'decimalItemType', 'floatItemType', 'doubleItemType', 'integerItemType',
 'nonPositiveIntegerItemType', 'negativeIntegerItemType', 'longItemType', 'intItemType',
 'shortItemType', 'byteItemType', 'nonNegativeIntegerItemType', 'unsignedLongItemType',
 'unsignedIntItemType', 'unsignedShortItemType', 'unsignedByteItemType',
 'positiveIntegerItemType', 'monetaryItemType', 'sharesItemType', 'pureItemType',
 'fractionItemType', 'stringItemType', 'booleanItemType', 'hexBinaryItemType',
 'base64BinaryItemType', 'anyURIItemType', 'QNameItemType', 'durationItemType',
 'dateTimeItemType', 'timeItemType', 'dateItemType', 'gYearMonthItemType',
 'gYearItemType', 'gMonthDayItemType', 'gDayItemType', 'gMonthItemType',
 'normalizedStringItemType', 'tokenItemType', 'languageItemType', 'NameItemType', 'NCNameItemType'}

class ValidateXbrl:

    def __init__(self, testModelXbrl):
        self.testModelXbrl = testModelXbrl

    def close(self, reusable=True):
        if reusable:
            testModelXbrl = self.testModelXbrl
        self.__dict__.clear()
        if reusable:
            self.testModelXbrl = testModelXbrl

    def validate--- This code section failed: ---

 L.  57         0  LOAD_FAST                'parameters'
                2  LOAD_DEREF               'self'
                4  STORE_ATTR               parameters

 L.  58         6  LOAD_GLOBAL              re
                8  LOAD_ATTR                compile
               10  LOAD_STR                 '^([0-9]+|INF)$'
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  LOAD_DEREF               'self'
               16  STORE_ATTR               precisionPattern

 L.  59        18  LOAD_GLOBAL              re
               20  LOAD_ATTR                compile
               22  LOAD_STR                 '^(-?[0-9]+|INF)$'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  LOAD_DEREF               'self'
               28  STORE_ATTR               decimalsPattern

 L.  60        30  LOAD_GLOBAL              re
               32  LOAD_ATTR                compile
               34  LOAD_STR                 '^[A-Z]{3}$'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  LOAD_DEREF               'self'
               40  STORE_ATTR               isoCurrencyPattern

 L.  61        42  LOAD_FAST                'modelXbrl'
               44  LOAD_DEREF               'self'
               46  STORE_ATTR               modelXbrl

 L.  62        48  LOAD_FAST                'modelXbrl'
               50  LOAD_ATTR                modelManager
               52  LOAD_ATTR                validateDisclosureSystem
               54  LOAD_DEREF               'self'
               56  STORE_ATTR               validateDisclosureSystem

 L.  63        58  LOAD_FAST                'modelXbrl'
               60  LOAD_ATTR                modelManager
               62  LOAD_ATTR                disclosureSystem
               64  LOAD_DEREF               'self'
               66  STORE_ATTR               disclosureSystem

 L.  64        68  LOAD_DEREF               'self'
               70  LOAD_ATTR                validateDisclosureSystem
               72  JUMP_IF_FALSE_OR_POP    80  'to 80'
               74  LOAD_DEREF               'self'
               76  LOAD_ATTR                disclosureSystem
               78  LOAD_ATTR                EFM
             80_0  COME_FROM            72  '72'
               80  LOAD_DEREF               'self'
               82  STORE_ATTR               validateEFM

 L.  65        84  LOAD_DEREF               'self'
               86  LOAD_ATTR                validateDisclosureSystem
               88  JUMP_IF_FALSE_OR_POP    96  'to 96'
               90  LOAD_DEREF               'self'
               92  LOAD_ATTR                disclosureSystem
               94  LOAD_ATTR                GFM
             96_0  COME_FROM            88  '88'
               96  LOAD_DEREF               'self'
               98  STORE_ATTR               validateGFM

 L.  66       100  LOAD_DEREF               'self'
              102  LOAD_ATTR                validateDisclosureSystem
              104  JUMP_IF_FALSE_OR_POP   112  'to 112'
              106  LOAD_DEREF               'self'
              108  LOAD_ATTR                disclosureSystem
              110  LOAD_ATTR                EFMorGFM
            112_0  COME_FROM           104  '104'
              112  LOAD_DEREF               'self'
              114  STORE_ATTR               validateEFMorGFM

 L.  67       116  LOAD_DEREF               'self'
              118  LOAD_ATTR                validateDisclosureSystem
              120  JUMP_IF_FALSE_OR_POP   128  'to 128'
              122  LOAD_DEREF               'self'
              124  LOAD_ATTR                disclosureSystem
              126  LOAD_ATTR                HMRC
            128_0  COME_FROM           120  '120'
              128  LOAD_DEREF               'self'
              130  STORE_ATTR               validateHMRC

 L.  68       132  LOAD_DEREF               'self'
              134  LOAD_ATTR                validateDisclosureSystem
              136  JUMP_IF_FALSE_OR_POP   144  'to 144'
              138  LOAD_DEREF               'self'
              140  LOAD_ATTR                disclosureSystem
              142  LOAD_ATTR                SBRNL
            144_0  COME_FROM           136  '136'
              144  LOAD_DEREF               'self'
              146  STORE_ATTR               validateSBRNL

 L.  69       148  LOAD_DEREF               'self'
              150  LOAD_ATTR                validateEFMorGFM
              152  JUMP_IF_TRUE_OR_POP   158  'to 158'
              154  LOAD_DEREF               'self'
              156  LOAD_ATTR                validateSBRNL
            158_0  COME_FROM           152  '152'
              158  LOAD_DEREF               'self'
              160  STORE_ATTR               validateEFMorGFMorSBRNL

 L.  70       162  LOAD_DEREF               'self'
              164  LOAD_ATTR                validateDisclosureSystem
              166  JUMP_IF_FALSE_OR_POP   174  'to 174'
              168  LOAD_DEREF               'self'
              170  LOAD_ATTR                disclosureSystem
              172  LOAD_ATTR                xmlLangPattern
            174_0  COME_FROM           166  '166'
              174  LOAD_DEREF               'self'
              176  STORE_ATTR               validateXmlLang

 L.  71       178  LOAD_FAST                'modelXbrl'
              180  LOAD_ATTR                modelManager
              182  LOAD_ATTR                validateCalcLB
              184  LOAD_DEREF               'self'
              186  STORE_ATTR               validateCalcLB

 L.  72       188  LOAD_FAST                'modelXbrl'
              190  LOAD_ATTR                modelManager
              192  LOAD_ATTR                validateInferDecimals
              194  LOAD_DEREF               'self'
              196  STORE_ATTR               validateInferDecimals

 L.  73       198  LOAD_FAST                'modelXbrl'
              200  LOAD_ATTR                modelManager
              202  LOAD_ATTR                validateDedupCalcs
              204  LOAD_DEREF               'self'
              206  STORE_ATTR               validateDedupCalcs

 L.  74       208  LOAD_FAST                'modelXbrl'
              210  LOAD_ATTR                modelManager
              212  LOAD_ATTR                validateUtr
              214  JUMP_IF_TRUE_OR_POP   298  'to 298'

 L.  75       218  LOAD_DEREF               'self'
              220  LOAD_ATTR                parameters
              222  POP_JUMP_IF_FALSE   258  'to 258'
              226  LOAD_DEREF               'self'
              228  LOAD_ATTR                parameters
              230  LOAD_ATTR                get
              232  LOAD_GLOBAL              qname
              234  LOAD_STR                 'forceUtrValidation'
              236  LOAD_CONST               True
              238  LOAD_CONST               ('noPrefixIsNoNamespace',)
              240  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              242  LOAD_CONST               (None, 'false')
              244  CALL_FUNCTION_2       2  '2 positional arguments'
              246  LOAD_CONST               1
              248  BINARY_SUBSCR    
              250  LOAD_STR                 'true'
              252  COMPARE_OP               ==
            254_0  COME_FROM           222  '222'
              254  JUMP_IF_TRUE_OR_POP   298  'to 298'

 L.  76       258  LOAD_DEREF               'self'
              260  LOAD_ATTR                validateEFM
              262  JUMP_IF_FALSE_OR_POP   298  'to 298'

 L.  77       266  LOAD_GLOBAL              any
              268  LOAD_CLOSURE             'self'
              270  BUILD_TUPLE_1         1 
              272  LOAD_GENEXPR             '<code_object <genexpr>>'
              274  LOAD_STR                 'ValidateXbrl.validate.<locals>.<genexpr>'
              276  MAKE_FUNCTION_8          'closure'

 L.  78       278  LOAD_DEREF               'self'
              280  LOAD_ATTR                modelXbrl
              282  LOAD_ATTR                nameConcepts
              284  LOAD_ATTR                get
              286  LOAD_STR                 'UTR'
              288  BUILD_TUPLE_0         0 
              290  CALL_FUNCTION_2       2  '2 positional arguments'
              292  GET_ITER         
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  CALL_FUNCTION_1       1  '1 positional argument'
            298_0  COME_FROM           262  '262'
            298_1  COME_FROM           254  '254'
            298_2  COME_FROM           214  '214'
              298  LOAD_DEREF               'self'
              300  STORE_ATTR               validateUTR

 L.  79       302  LOAD_CONST               False
              304  LOAD_DEREF               'self'
              306  STORE_ATTR               validateIXDS

 L.  80       308  LOAD_GLOBAL              bool
              310  LOAD_GLOBAL              XbrlConst
              312  LOAD_ATTR                enums
              314  LOAD_GLOBAL              _DICT_SET
              316  LOAD_FAST                'modelXbrl'
              318  LOAD_ATTR                namespaceDocs
              320  LOAD_ATTR                keys
              322  CALL_FUNCTION_0       0  '0 positional arguments'
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  BINARY_AND       
              328  CALL_FUNCTION_1       1  '1 positional argument'
              330  LOAD_DEREF               'self'
              332  STORE_ATTR               validateEnum

 L.  82       334  SETUP_LOOP          364  'to 364'
              336  LOAD_GLOBAL              pluginClassMethods
              338  LOAD_STR                 'Validate.XBRL.Start'
              340  CALL_FUNCTION_1       1  '1 positional argument'
              342  GET_ITER         
              344  FOR_ITER            362  'to 362'
              346  STORE_FAST               'pluginXbrlMethod'

 L.  83       348  LOAD_FAST                'pluginXbrlMethod'
              350  LOAD_DEREF               'self'
              352  LOAD_FAST                'parameters'
              354  CALL_FUNCTION_2       2  '2 positional arguments'
              356  POP_TOP          
              358  JUMP_BACK           344  'to 344'
              362  POP_BLOCK        
            364_0  COME_FROM_LOOP      334  '334'

 L.  86       364  LOAD_FAST                'modelXbrl'
              366  LOAD_ATTR                profileStat
              368  LOAD_CONST               None
              370  CALL_FUNCTION_1       1  '1 positional argument'
              372  POP_TOP          

 L.  87       374  LOAD_FAST                'modelXbrl'
              376  LOAD_ATTR                modelManager
              378  LOAD_ATTR                showStatus
              380  LOAD_GLOBAL              _
              382  LOAD_STR                 'validating links'
              384  CALL_FUNCTION_1       1  '1 positional argument'
              386  CALL_FUNCTION_1       1  '1 positional argument'
              388  POP_TOP          

 L.  88       390  LOAD_GLOBAL              set
              392  CALL_FUNCTION_0       0  '0 positional arguments'
              394  STORE_FAST               'modelLinks'

 L.  89       396  LOAD_GLOBAL              set
              398  CALL_FUNCTION_0       0  '0 positional arguments'
              400  LOAD_DEREF               'self'
              402  STORE_ATTR               remoteResourceLocElements

 L.  90       404  LOAD_GLOBAL              set
              406  CALL_FUNCTION_0       0  '0 positional arguments'
              408  LOAD_DEREF               'self'
              410  STORE_ATTR               genericArcArcroles

 L.  91       412  SETUP_LOOP          460  'to 460'
              414  LOAD_FAST                'modelXbrl'
              416  LOAD_ATTR                baseSets
              418  LOAD_ATTR                values
              420  CALL_FUNCTION_0       0  '0 positional arguments'
              422  GET_ITER         
              424  FOR_ITER            458  'to 458'
              426  STORE_FAST               'baseSetExtLinks'

 L.  92       428  SETUP_LOOP          454  'to 454'
              430  LOAD_FAST                'baseSetExtLinks'
              432  GET_ITER         
              434  FOR_ITER            452  'to 452'
              436  STORE_FAST               'baseSetExtLink'

 L.  93       438  LOAD_FAST                'modelLinks'
              440  LOAD_ATTR                add
              442  LOAD_FAST                'baseSetExtLink'
              444  CALL_FUNCTION_1       1  '1 positional argument'
              446  POP_TOP          
              448  JUMP_BACK           434  'to 434'
              452  POP_BLOCK        
            454_0  COME_FROM_LOOP      428  '428'
              454  JUMP_BACK           424  'to 424'
              458  POP_BLOCK        
            460_0  COME_FROM_LOOP      412  '412'

 L.  94       460  LOAD_DEREF               'self'
              462  LOAD_ATTR                checkLinks
              464  LOAD_FAST                'modelLinks'
              466  CALL_FUNCTION_1       1  '1 positional argument'
              468  POP_TOP          

 L.  95       470  LOAD_FAST                'modelXbrl'
              472  LOAD_ATTR                profileStat
              474  LOAD_GLOBAL              _
              476  LOAD_STR                 'validateLinks'
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  CALL_FUNCTION_1       1  '1 positional argument'
              482  POP_TOP          

 L.  97       484  BUILD_MAP_0           0 
              486  LOAD_FAST                'modelXbrl'
              488  STORE_ATTR               dimensionDefaultConcepts

 L.  98       490  BUILD_MAP_0           0 
              492  LOAD_FAST                'modelXbrl'
              494  STORE_ATTR               qnameDimensionDefaults

 L.  99       496  BUILD_MAP_0           0 
              498  LOAD_FAST                'modelXbrl'
              500  STORE_ATTR               qnameDimensionContextElement

 L. 101       502  LOAD_FAST                'modelXbrl'
              504  LOAD_ATTR                modelManager
              506  LOAD_ATTR                showStatus
              508  LOAD_GLOBAL              _
              510  LOAD_STR                 'validating relationship sets'
              512  CALL_FUNCTION_1       1  '1 positional argument'
              514  CALL_FUNCTION_1       1  '1 positional argument'
              516  POP_TOP          

 L. 102       518  SETUP_LOOP         1864  'to 1864'
              522  LOAD_FAST                'modelXbrl'
              524  LOAD_ATTR                baseSets
              526  LOAD_ATTR                keys
              528  CALL_FUNCTION_0       0  '0 positional arguments'
              530  GET_ITER         
              532  FOR_ITER           1862  'to 1862'
              536  STORE_FAST               'baseSetKey'

 L. 103       538  LOAD_FAST                'baseSetKey'
              540  UNPACK_SEQUENCE_4     4 
              542  STORE_FAST               'arcrole'
              544  STORE_FAST               'ELR'
              546  STORE_FAST               'linkqname'
              548  STORE_FAST               'arcqname'

 L. 104       550  LOAD_FAST                'arcrole'
              552  LOAD_ATTR                startswith
              554  LOAD_STR                 'XBRL-'
              556  CALL_FUNCTION_1       1  '1 positional argument'
              558  POP_JUMP_IF_TRUE    532  'to 532'
              562  LOAD_FAST                'ELR'
              564  LOAD_CONST               None
              566  COMPARE_OP               is
              568  POP_JUMP_IF_TRUE    532  'to 532'

 L. 105       572  LOAD_FAST                'linkqname'
              574  LOAD_CONST               None
              576  COMPARE_OP               is
              578  POP_JUMP_IF_TRUE    532  'to 532'
              582  LOAD_FAST                'arcqname'
              584  LOAD_CONST               None
              586  COMPARE_OP               is
              588  POP_JUMP_IF_FALSE   598  'to 598'

 L. 106       592  CONTINUE            532  'to 532'
              596  JUMP_FORWARD        712  'to 712'
              598  ELSE                     '712'

 L. 107       598  LOAD_FAST                'arcrole'
              600  LOAD_GLOBAL              XbrlConst
              602  LOAD_ATTR                standardArcroleCyclesAllowed
              604  COMPARE_OP               in
              606  POP_JUMP_IF_FALSE   626  'to 626'

 L. 109       610  LOAD_GLOBAL              XbrlConst
              612  LOAD_ATTR                standardArcroleCyclesAllowed
              614  LOAD_FAST                'arcrole'
              616  BINARY_SUBSCR    
              618  UNPACK_SEQUENCE_2     2 
              620  STORE_FAST               'cyclesAllowed'
              622  STORE_FAST               'specSect'
              624  JUMP_FORWARD        712  'to 712'
              626  ELSE                     '712'

 L. 110       626  LOAD_FAST                'arcrole'
              628  LOAD_DEREF               'self'
              630  LOAD_ATTR                modelXbrl
              632  LOAD_ATTR                arcroleTypes
              634  COMPARE_OP               in
              636  POP_JUMP_IF_FALSE   704  'to 704'
              640  LOAD_GLOBAL              len
              642  LOAD_DEREF               'self'
              644  LOAD_ATTR                modelXbrl
              646  LOAD_ATTR                arcroleTypes
              648  LOAD_FAST                'arcrole'
              650  BINARY_SUBSCR    
              652  CALL_FUNCTION_1       1  '1 positional argument'
              654  LOAD_CONST               0
              656  COMPARE_OP               >
              658  POP_JUMP_IF_FALSE   704  'to 704'

 L. 111       662  LOAD_DEREF               'self'
              664  LOAD_ATTR                modelXbrl
              666  LOAD_ATTR                arcroleTypes
              668  LOAD_FAST                'arcrole'
              670  BINARY_SUBSCR    
              672  LOAD_CONST               0
              674  BINARY_SUBSCR    
              676  LOAD_ATTR                cyclesAllowed
              678  STORE_FAST               'cyclesAllowed'

 L. 112       680  LOAD_FAST                'arcrole'
              682  LOAD_DEREF               'self'
              684  LOAD_ATTR                genericArcArcroles
              686  COMPARE_OP               in
              688  POP_JUMP_IF_FALSE   698  'to 698'

 L. 113       692  LOAD_STR                 'xbrlgene:violatedCyclesConstraint'
              694  STORE_FAST               'specSect'
              696  JUMP_FORWARD        702  'to 702'
              698  ELSE                     '702'

 L. 115       698  LOAD_STR                 'xbrl.5.1.4.3:cycles'
              700  STORE_FAST               'specSect'
            702_0  COME_FROM           696  '696'
              702  JUMP_FORWARD        712  'to 712'
            704_0  COME_FROM           636  '636'

 L. 117       704  LOAD_STR                 'any'
              706  STORE_FAST               'cyclesAllowed'

 L. 118       708  LOAD_CONST               None
              710  STORE_FAST               'specSect'
            712_0  COME_FROM           702  '702'
            712_1  COME_FROM           624  '624'
            712_2  COME_FROM           596  '596'

 L. 119       712  LOAD_FAST                'cyclesAllowed'
              714  LOAD_STR                 'any'
              716  COMPARE_OP               !=
              718  POP_JUMP_IF_TRUE    784  'to 784'
              722  LOAD_FAST                'arcrole'
              724  LOAD_GLOBAL              XbrlConst
              726  LOAD_ATTR                summationItem
              728  BUILD_TUPLE_1         1 
              730  COMPARE_OP               in
              732  POP_JUMP_IF_TRUE    784  'to 784'

 L. 120       736  LOAD_FAST                'arcrole'
              738  LOAD_DEREF               'self'
              740  LOAD_ATTR                genericArcArcroles
              742  COMPARE_OP               in
              744  POP_JUMP_IF_TRUE    784  'to 784'

 L. 121       748  LOAD_FAST                'arcrole'
              750  LOAD_ATTR                startswith
              752  LOAD_GLOBAL              XbrlConst
              754  LOAD_ATTR                formulaStartsWith
              756  CALL_FUNCTION_1       1  '1 positional argument'
              758  POP_JUMP_IF_TRUE    784  'to 784'

 L. 122       762  LOAD_FAST                'modelXbrl'
              764  LOAD_ATTR                hasXDT
              766  POP_JUMP_IF_FALSE   800  'to 800'
              770  LOAD_FAST                'arcrole'
              772  LOAD_ATTR                startswith
              774  LOAD_GLOBAL              XbrlConst
              776  LOAD_ATTR                dimStartsWith
              778  CALL_FUNCTION_1       1  '1 positional argument'
            780_0  COME_FROM           766  '766'
            780_1  COME_FROM           758  '758'
            780_2  COME_FROM           744  '744'
            780_3  COME_FROM           732  '732'
            780_4  COME_FROM           718  '718'
              780  POP_JUMP_IF_FALSE   800  'to 800'

 L. 123       784  LOAD_FAST                'modelXbrl'
              786  LOAD_ATTR                relationshipSet
              788  LOAD_FAST                'arcrole'
              790  LOAD_FAST                'ELR'
              792  LOAD_FAST                'linkqname'
              794  LOAD_FAST                'arcqname'
              796  CALL_FUNCTION_4       4  '4 positional arguments'
              798  STORE_FAST               'relsSet'
            800_0  COME_FROM           780  '780'

 L. 124       800  LOAD_FAST                'cyclesAllowed'
              802  LOAD_STR                 'any'
              804  COMPARE_OP               !=
              806  POP_JUMP_IF_FALSE   834  'to 834'

 L. 125       810  LOAD_GLOBAL              XbrlConst
              812  LOAD_ATTR                isStandardExtLinkQname
              814  LOAD_FAST                'linkqname'
              816  CALL_FUNCTION_1       1  '1 positional argument'
              818  POP_JUMP_IF_FALSE   834  'to 834'
              822  LOAD_GLOBAL              XbrlConst
              824  LOAD_ATTR                isStandardArcQname
              826  LOAD_FAST                'arcqname'
              828  CALL_FUNCTION_1       1  '1 positional argument'
            830_0  COME_FROM           818  '818'
            830_1  COME_FROM           806  '806'
              830  POP_JUMP_IF_TRUE    846  'to 846'

 L. 126       834  LOAD_FAST                'arcrole'
              836  LOAD_DEREF               'self'
              838  LOAD_ATTR                genericArcArcroles
              840  COMPARE_OP               in
            842_0  COME_FROM           830  '830'
              842  POP_JUMP_IF_FALSE  1080  'to 1080'

 L. 127       846  LOAD_FAST                'cyclesAllowed'
              848  LOAD_STR                 'none'
              850  COMPARE_OP               ==
              852  STORE_FAST               'noUndirected'

 L. 128       854  LOAD_FAST                'relsSet'
              856  LOAD_ATTR                fromModelObjects
              858  CALL_FUNCTION_0       0  '0 positional arguments'
              860  STORE_FAST               'fromRelationships'

 L. 129       862  SETUP_LOOP         1080  'to 1080'
              864  LOAD_FAST                'fromRelationships'
              866  LOAD_ATTR                items
              868  CALL_FUNCTION_0       0  '0 positional arguments'
              870  GET_ITER         
              872  FOR_ITER           1078  'to 1078'
              874  UNPACK_SEQUENCE_2     2 
              876  STORE_FAST               'relFrom'
              878  STORE_FAST               'rels'

 L. 130       880  LOAD_DEREF               'self'
              882  LOAD_ATTR                fwdCycle
              884  LOAD_FAST                'relsSet'
              886  LOAD_FAST                'rels'
              888  LOAD_FAST                'noUndirected'
              890  LOAD_FAST                'relFrom'
              892  BUILD_SET_1           1 
              894  CALL_FUNCTION_4       4  '4 positional arguments'
              896  STORE_FAST               'cycleFound'

 L. 131       898  LOAD_FAST                'cycleFound'
              900  LOAD_CONST               None
              902  COMPARE_OP               is-not
              904  POP_JUMP_IF_FALSE   872  'to 872'

 L. 132       908  LOAD_GLOBAL              len
              910  LOAD_FAST                'cycleFound'
              912  CALL_FUNCTION_1       1  '1 positional argument'
              914  STORE_FAST               'pathEndsAt'

 L. 133       916  LOAD_FAST                'cycleFound'
              918  LOAD_CONST               1
              920  BINARY_SUBSCR    
              922  LOAD_ATTR                toModelObject
              924  STORE_FAST               'loopedModelObject'

 L. 134       926  SETUP_LOOP          980  'to 980'
              928  LOAD_GLOBAL              enumerate
              930  LOAD_FAST                'cycleFound'
              932  LOAD_CONST               2
              934  LOAD_CONST               None
              936  BUILD_SLICE_2         2 
              938  BINARY_SUBSCR    
              940  CALL_FUNCTION_1       1  '1 positional argument'
              942  GET_ITER         
              944  FOR_ITER            978  'to 978'
              946  UNPACK_SEQUENCE_2     2 
              948  STORE_FAST               'i'
              950  STORE_FAST               'rel'

 L. 135       952  LOAD_FAST                'rel'
              954  LOAD_ATTR                fromModelObject
              956  LOAD_FAST                'loopedModelObject'
              958  COMPARE_OP               ==
              960  POP_JUMP_IF_FALSE   944  'to 944'

 L. 136       964  LOAD_CONST               3
              966  LOAD_FAST                'i'
              968  BINARY_ADD       
              970  STORE_FAST               'pathEndsAt'

 L. 137       972  BREAK_LOOP       
              974  JUMP_BACK           944  'to 944'
              978  POP_BLOCK        
            980_0  COME_FROM_LOOP      926  '926'

 L. 138       980  LOAD_GLOBAL              str
              982  LOAD_FAST                'loopedModelObject'
              984  LOAD_ATTR                qname
              986  CALL_FUNCTION_1       1  '1 positional argument'
              988  LOAD_STR                 ' '
              990  BINARY_ADD       
              992  LOAD_STR                 ' - '
              994  LOAD_ATTR                join

 L. 139       996  LOAD_GENEXPR             '<code_object <genexpr>>'
              998  LOAD_STR                 'ValidateXbrl.validate.<locals>.<genexpr>'
             1000  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 140      1002  LOAD_GLOBAL              reversed
             1004  LOAD_FAST                'cycleFound'
             1006  LOAD_CONST               1
             1008  LOAD_FAST                'pathEndsAt'
             1010  BUILD_SLICE_2         2 
             1012  BINARY_SUBSCR    
             1014  CALL_FUNCTION_1       1  '1 positional argument'
             1016  GET_ITER         
             1018  CALL_FUNCTION_1       1  '1 positional argument'
             1020  CALL_FUNCTION_1       1  '1 positional argument'
             1022  BINARY_ADD       
             1024  STORE_FAST               'path'

 L. 141      1026  LOAD_FAST                'modelXbrl'
             1028  LOAD_ATTR                error
             1030  LOAD_FAST                'specSect'

 L. 142      1032  LOAD_GLOBAL              _
             1034  LOAD_STR                 'Relationships have a %(cycle)s cycle in arcrole %(arcrole)s \nlink role %(linkrole)s \nlink %(linkname)s, \narc %(arcname)s, \npath %(path)s'
             1036  CALL_FUNCTION_1       1  '1 positional argument'

 L. 143      1038  LOAD_FAST                'cycleFound'
             1040  LOAD_CONST               1
             1042  LOAD_FAST                'pathEndsAt'
             1044  BUILD_SLICE_2         2 
             1046  BINARY_SUBSCR    
             1048  LOAD_FAST                'cycleFound'
             1050  LOAD_CONST               0
             1052  BINARY_SUBSCR    
             1054  LOAD_FAST                'path'

 L. 144      1056  LOAD_FAST                'arcrole'
             1058  LOAD_FAST                'ELR'
             1060  LOAD_FAST                'linkqname'
             1062  LOAD_FAST                'arcqname'

 L. 147      1064  LOAD_CONST               ('xbrlgene:violatedCyclesConstraint', 'xbrl.5.1.4.3:cycles', 'xbrl.5.2.4.2', 'xbrl.5.2.5.2', 'xbrl.5.2.6.2.1', 'xbrl.5.2.6.2.1', 'xbrl.5.2.6.2.3', 'xbrl.5.2.6.2.4')
             1066  LOAD_CONST               ('modelObject', 'cycle', 'path', 'arcrole', 'linkrole', 'linkname', 'arcname', 'messageCodes')
             1068  CALL_FUNCTION_KW_10    10  '10 total positional and keyword args'
             1070  POP_TOP          

 L. 148      1072  BREAK_LOOP       
             1074  JUMP_BACK           872  'to 872'
             1078  POP_BLOCK        
           1080_0  COME_FROM_LOOP      862  '862'
           1080_1  COME_FROM           842  '842'

 L. 151      1080  LOAD_FAST                'arcrole'
             1082  LOAD_GLOBAL              XbrlConst
             1084  LOAD_ATTR                summationItem
             1086  COMPARE_OP               ==
             1088  POP_JUMP_IF_FALSE  1404  'to 1404'

 L. 152      1092  SETUP_LOOP         1858  'to 1858'
             1096  LOAD_FAST                'relsSet'
             1098  LOAD_ATTR                modelRelationships
             1100  GET_ITER         
             1102  FOR_ITER           1398  'to 1398'
             1106  STORE_FAST               'modelRel'

 L. 153      1108  LOAD_FAST                'modelRel'
             1110  LOAD_ATTR                weight
             1112  STORE_FAST               'weight'

 L. 154      1114  LOAD_FAST                'modelRel'
             1116  LOAD_ATTR                fromModelObject
             1118  STORE_FAST               'fromConcept'

 L. 155      1120  LOAD_FAST                'modelRel'
             1122  LOAD_ATTR                toModelObject
             1124  STORE_FAST               'toConcept'

 L. 156      1126  LOAD_FAST                'fromConcept'
             1128  LOAD_CONST               None
             1130  COMPARE_OP               is-not
             1132  POP_JUMP_IF_FALSE  1102  'to 1102'
             1136  LOAD_FAST                'toConcept'
             1138  LOAD_CONST               None
             1140  COMPARE_OP               is-not
             1142  POP_JUMP_IF_FALSE  1102  'to 1102'

 L. 157      1146  LOAD_FAST                'weight'
             1148  LOAD_CONST               0
             1150  COMPARE_OP               ==
             1152  POP_JUMP_IF_FALSE  1188  'to 1188'

 L. 158      1156  LOAD_FAST                'modelXbrl'
             1158  LOAD_ATTR                error
             1160  LOAD_STR                 'xbrl.5.2.5.2.1:zeroWeight'

 L. 159      1162  LOAD_GLOBAL              _
             1164  LOAD_STR                 'Calculation relationship has zero weight from %(source)s to %(target)s in link role %(linkrole)s'
             1166  CALL_FUNCTION_1       1  '1 positional argument'

 L. 160      1168  LOAD_FAST                'modelRel'

 L. 161      1170  LOAD_FAST                'fromConcept'
             1172  LOAD_ATTR                qname
             1174  LOAD_FAST                'toConcept'
             1176  LOAD_ATTR                qname
             1178  LOAD_FAST                'ELR'
             1180  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
             1182  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1184  BUILD_TUPLE_1         1 
             1186  POP_TOP          
           1188_0  COME_FROM          1152  '1152'

 L. 162      1188  LOAD_FAST                'fromConcept'
             1190  LOAD_ATTR                balance
             1192  STORE_FAST               'fromBalance'

 L. 163      1194  LOAD_FAST                'toConcept'
             1196  LOAD_ATTR                balance
             1198  STORE_FAST               'toBalance'

 L. 164      1200  LOAD_FAST                'fromBalance'
             1202  POP_JUMP_IF_FALSE  1308  'to 1308'
             1206  LOAD_FAST                'toBalance'
             1208  POP_JUMP_IF_FALSE  1308  'to 1308'

 L. 165      1212  LOAD_FAST                'fromBalance'
             1214  LOAD_FAST                'toBalance'
             1216  COMPARE_OP               ==
             1218  POP_JUMP_IF_FALSE  1232  'to 1232'
             1222  LOAD_FAST                'weight'
             1224  LOAD_CONST               0
             1226  COMPARE_OP               <
           1228_0  COME_FROM          1218  '1218'
             1228  POP_JUMP_IF_TRUE   1252  'to 1252'

 L. 166      1232  LOAD_FAST                'fromBalance'
             1234  LOAD_FAST                'toBalance'
             1236  COMPARE_OP               !=
             1238  POP_JUMP_IF_FALSE  1308  'to 1308'
             1242  LOAD_FAST                'weight'
             1244  LOAD_CONST               0
             1246  COMPARE_OP               >
           1248_0  COME_FROM          1238  '1238'
           1248_1  COME_FROM          1228  '1228'
             1248  POP_JUMP_IF_FALSE  1308  'to 1308'

 L. 167      1252  LOAD_FAST                'modelXbrl'
             1254  LOAD_ATTR                error
             1256  LOAD_STR                 'xbrl.5.1.1.2:balanceCalcWeightIllegal'

 L. 168      1258  LOAD_FAST                'weight'
             1260  LOAD_CONST               0
             1262  COMPARE_OP               <
             1264  POP_JUMP_IF_FALSE  1272  'to 1272'
             1268  LOAD_STR                 'Negative'
             1270  JUMP_FORWARD       1274  'to 1274'
             1272  ELSE                     '1274'
             1272  LOAD_STR                 'Positive'
           1274_0  COME_FROM          1270  '1270'
             1274  BINARY_ADD       

 L. 169      1276  LOAD_GLOBAL              _
             1278  LOAD_STR                 'Calculation relationship has illegal weight %(weight)s from %(source)s, %(sourceBalance)s, to %(target)s, %(targetBalance)s, in link role %(linkrole)s (per 5.1.1.2 Table 6)'
             1280  CALL_FUNCTION_1       1  '1 positional argument'

 L. 170      1282  LOAD_FAST                'modelRel'
             1284  LOAD_FAST                'weight'

 L. 171      1286  LOAD_FAST                'fromConcept'
             1288  LOAD_ATTR                qname
             1290  LOAD_FAST                'toConcept'
             1292  LOAD_ATTR                qname
             1294  LOAD_FAST                'ELR'

 L. 172      1296  LOAD_FAST                'fromBalance'
             1298  LOAD_FAST                'toBalance'

 L. 173      1300  LOAD_CONST               ('xbrl.5.1.1.2:balanceCalcWeightIllegalNegative', 'xbrl.5.1.1.2:balanceCalcWeightIllegalPositive')
             1302  LOAD_CONST               ('modelObject', 'weight', 'source', 'target', 'linkrole', 'sourceBalance', 'targetBalance', 'messageCodes')
             1304  CALL_FUNCTION_KW_10    10  '10 total positional and keyword args'
             1306  POP_TOP          
           1308_0  COME_FROM          1248  '1248'
           1308_1  COME_FROM          1208  '1208'
           1308_2  COME_FROM          1202  '1202'

 L. 174      1308  LOAD_FAST                'fromConcept'
             1310  LOAD_ATTR                isNumeric
             1312  UNARY_NOT        
             1314  POP_JUMP_IF_TRUE   1328  'to 1328'
             1318  LOAD_FAST                'toConcept'
             1320  LOAD_ATTR                isNumeric
             1322  UNARY_NOT        
           1324_0  COME_FROM          1314  '1314'
             1324  POP_JUMP_IF_FALSE  1102  'to 1102'

 L. 175      1328  LOAD_FAST                'modelXbrl'
             1330  LOAD_ATTR                error
             1332  LOAD_STR                 'xbrl.5.2.5.2:nonNumericCalc'

 L. 176      1334  LOAD_GLOBAL              _
             1336  LOAD_STR                 'Calculation relationship has illegal concept from %(source)s%(sourceNumericDecorator)s to %(target)s%(targetNumericDecorator)s in link role %(linkrole)s'
             1338  CALL_FUNCTION_1       1  '1 positional argument'

 L. 177      1340  LOAD_FAST                'modelRel'

 L. 178      1342  LOAD_FAST                'fromConcept'
             1344  LOAD_ATTR                qname
             1346  LOAD_FAST                'toConcept'
             1348  LOAD_ATTR                qname
             1350  LOAD_FAST                'ELR'

 L. 179      1352  LOAD_FAST                'fromConcept'
             1354  LOAD_ATTR                isNumeric
             1356  POP_JUMP_IF_FALSE  1364  'to 1364'
             1360  LOAD_STR                 ''
             1362  JUMP_FORWARD       1370  'to 1370'
             1364  ELSE                     '1370'
             1364  LOAD_GLOBAL              _
             1366  LOAD_STR                 ' (non-numeric)'
             1368  CALL_FUNCTION_1       1  '1 positional argument'
           1370_0  COME_FROM          1362  '1362'

 L. 180      1370  LOAD_FAST                'toConcept'
             1372  LOAD_ATTR                isNumeric
             1374  POP_JUMP_IF_FALSE  1382  'to 1382'
             1378  LOAD_STR                 ''
             1380  JUMP_FORWARD       1388  'to 1388'
             1382  ELSE                     '1388'
             1382  LOAD_GLOBAL              _
             1384  LOAD_STR                 ' (non-numeric)'
             1386  CALL_FUNCTION_1       1  '1 positional argument'
           1388_0  COME_FROM          1380  '1380'
             1388  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole', 'sourceNumericDecorator', 'targetNumericDecorator')
             1390  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
             1392  POP_TOP          
             1394  JUMP_BACK          1102  'to 1102'
             1398  POP_BLOCK        
             1400  JUMP_BACK           532  'to 532'
           1404_0  COME_FROM          1088  '1088'

 L. 182      1404  LOAD_FAST                'arcrole'
             1406  LOAD_GLOBAL              XbrlConst
             1408  LOAD_ATTR                parentChild
             1410  COMPARE_OP               ==
             1412  POP_JUMP_IF_FALSE  1588  'to 1588'

 L. 183      1416  SETUP_LOOP         1584  'to 1584'
             1418  LOAD_FAST                'relsSet'
             1420  LOAD_ATTR                modelRelationships
             1422  GET_ITER         
             1424  FOR_ITER           1582  'to 1582'
             1426  STORE_FAST               'modelRel'

 L. 184      1428  LOAD_FAST                'modelRel'
             1430  LOAD_ATTR                preferredLabel
             1432  STORE_FAST               'preferredLabel'

 L. 185      1434  LOAD_FAST                'modelRel'
             1436  LOAD_ATTR                fromModelObject
             1438  STORE_FAST               'fromConcept'

 L. 186      1440  LOAD_FAST                'modelRel'
             1442  LOAD_ATTR                toModelObject
             1444  STORE_FAST               'toConcept'

 L. 187      1446  LOAD_FAST                'preferredLabel'
             1448  LOAD_CONST               None
             1450  COMPARE_OP               is-not
             1452  POP_JUMP_IF_FALSE  1424  'to 1424'
             1456  LOAD_GLOBAL              isinstance
             1458  LOAD_FAST                'fromConcept'
             1460  LOAD_GLOBAL              ModelConcept
             1462  CALL_FUNCTION_2       2  '2 positional arguments'
             1464  POP_JUMP_IF_FALSE  1424  'to 1424'
             1468  LOAD_GLOBAL              isinstance
             1470  LOAD_FAST                'toConcept'
             1472  LOAD_GLOBAL              ModelConcept
             1474  CALL_FUNCTION_2       2  '2 positional arguments'
             1476  POP_JUMP_IF_FALSE  1424  'to 1424'

 L. 188      1480  LOAD_FAST                'toConcept'
             1482  LOAD_ATTR                label
             1484  LOAD_FAST                'preferredLabel'
             1486  LOAD_CONST               False
             1488  LOAD_CONST               True
             1490  LOAD_CONST               ('preferredLabel', 'fallbackToQname', 'strip')
             1492  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1494  STORE_FAST               'label'

 L. 189      1496  LOAD_FAST                'label'
             1498  LOAD_CONST               None
             1500  COMPARE_OP               is
             1502  POP_JUMP_IF_FALSE  1540  'to 1540'

 L. 190      1506  LOAD_FAST                'modelXbrl'
             1508  LOAD_ATTR                error
             1510  LOAD_STR                 'xbrl.5.2.4.2.1:preferredLabelMissing'

 L. 191      1512  LOAD_GLOBAL              _
             1514  LOAD_STR                 'Presentation relationship from %(source)s to %(target)s in link role %(linkrole)s missing preferredLabel %(preferredLabel)s'
             1516  CALL_FUNCTION_1       1  '1 positional argument'

 L. 192      1518  LOAD_FAST                'modelRel'

 L. 193      1520  LOAD_FAST                'fromConcept'
             1522  LOAD_ATTR                qname
             1524  LOAD_FAST                'toConcept'
             1526  LOAD_ATTR                qname
             1528  LOAD_FAST                'ELR'

 L. 194      1530  LOAD_FAST                'preferredLabel'
             1532  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole', 'preferredLabel')
             1534  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1536  POP_TOP          
             1538  JUMP_FORWARD       1578  'to 1578'
             1540  ELSE                     '1578'

 L. 195      1540  LOAD_FAST                'label'
             1542  POP_JUMP_IF_TRUE   1424  'to 1424'

 L. 196      1546  LOAD_FAST                'modelXbrl'
             1548  LOAD_ATTR                info
             1550  LOAD_STR                 'arelle:info.preferredLabelEmpty'

 L. 197      1552  LOAD_GLOBAL              _
             1554  LOAD_STR                 '(Info xbrl.5.2.4.2.1) Presentation relationship from %(source)s to %(target)s in link role %(linkrole)s has empty preferredLabel %(preferredLabel)s'
             1556  CALL_FUNCTION_1       1  '1 positional argument'

 L. 198      1558  LOAD_FAST                'modelRel'

 L. 199      1560  LOAD_FAST                'fromConcept'
             1562  LOAD_ATTR                qname
             1564  LOAD_FAST                'toConcept'
             1566  LOAD_ATTR                qname
             1568  LOAD_FAST                'ELR'

 L. 200      1570  LOAD_FAST                'preferredLabel'
             1572  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole', 'preferredLabel')
             1574  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1576  POP_TOP          
           1578_0  COME_FROM          1538  '1538'
             1578  JUMP_BACK          1424  'to 1424'
             1582  POP_BLOCK        
           1584_0  COME_FROM_LOOP     1416  '1416'
             1584  JUMP_BACK           532  'to 532'
           1588_0  COME_FROM          1412  '1412'

 L. 202      1588  LOAD_FAST                'arcrole'
             1590  LOAD_GLOBAL              XbrlConst
             1592  LOAD_ATTR                essenceAlias
             1594  COMPARE_OP               ==
             1596  POP_JUMP_IF_FALSE  1790  'to 1790'

 L. 203      1600  SETUP_LOOP         1788  'to 1788'
             1602  LOAD_FAST                'relsSet'
             1604  LOAD_ATTR                modelRelationships
             1606  GET_ITER         
             1608  FOR_ITER           1786  'to 1786'
             1610  STORE_FAST               'modelRel'

 L. 204      1612  LOAD_FAST                'modelRel'
             1614  LOAD_ATTR                fromModelObject
             1616  STORE_FAST               'fromConcept'

 L. 205      1618  LOAD_FAST                'modelRel'
             1620  LOAD_ATTR                toModelObject
             1622  STORE_FAST               'toConcept'

 L. 206      1624  LOAD_FAST                'fromConcept'
             1626  LOAD_CONST               None
             1628  COMPARE_OP               is-not
             1630  POP_JUMP_IF_FALSE  1608  'to 1608'
             1634  LOAD_FAST                'toConcept'
             1636  LOAD_CONST               None
             1638  COMPARE_OP               is-not
             1640  POP_JUMP_IF_FALSE  1608  'to 1608'

 L. 207      1644  LOAD_FAST                'fromConcept'
             1646  LOAD_ATTR                type
             1648  LOAD_FAST                'toConcept'
             1650  LOAD_ATTR                type
             1652  COMPARE_OP               !=
             1654  POP_JUMP_IF_TRUE   1672  'to 1672'
             1658  LOAD_FAST                'fromConcept'
             1660  LOAD_ATTR                periodType
             1662  LOAD_FAST                'toConcept'
             1664  LOAD_ATTR                periodType
             1666  COMPARE_OP               !=
           1668_0  COME_FROM          1654  '1654'
             1668  POP_JUMP_IF_FALSE  1702  'to 1702'

 L. 208      1672  LOAD_FAST                'modelXbrl'
             1674  LOAD_ATTR                error
             1676  LOAD_STR                 'xbrl.5.2.6.2.2:essenceAliasTypes'

 L. 209      1678  LOAD_GLOBAL              _
             1680  LOAD_STR                 'Essence-alias relationship from %(source)s to %(target)s in link role %(linkrole)s has different types or periodTypes'
             1682  CALL_FUNCTION_1       1  '1 positional argument'

 L. 210      1684  LOAD_FAST                'modelRel'

 L. 211      1686  LOAD_FAST                'fromConcept'
             1688  LOAD_ATTR                qname
             1690  LOAD_FAST                'toConcept'
             1692  LOAD_ATTR                qname
             1694  LOAD_FAST                'ELR'
             1696  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
             1698  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1700  POP_TOP          
           1702_0  COME_FROM          1668  '1668'

 L. 212      1702  LOAD_FAST                'fromConcept'
             1704  LOAD_ATTR                balance
             1706  STORE_FAST               'fromBalance'

 L. 213      1708  LOAD_FAST                'toConcept'
             1710  LOAD_ATTR                balance
             1712  STORE_FAST               'toBalance'

 L. 214      1714  LOAD_FAST                'fromBalance'
             1716  POP_JUMP_IF_FALSE  1608  'to 1608'
             1720  LOAD_FAST                'toBalance'
             1722  POP_JUMP_IF_FALSE  1608  'to 1608'

 L. 215      1726  LOAD_FAST                'fromBalance'
             1728  POP_JUMP_IF_FALSE  1608  'to 1608'
             1732  LOAD_FAST                'toBalance'
             1734  POP_JUMP_IF_FALSE  1608  'to 1608'
             1738  LOAD_FAST                'fromBalance'
             1740  LOAD_FAST                'toBalance'
             1742  COMPARE_OP               !=
             1744  POP_JUMP_IF_FALSE  1608  'to 1608'

 L. 216      1748  LOAD_FAST                'modelXbrl'
             1750  LOAD_ATTR                error
             1752  LOAD_STR                 'xbrl.5.2.6.2.2:essenceAliasBalance'

 L. 217      1754  LOAD_GLOBAL              _
             1756  LOAD_STR                 'Essence-alias relationship from %(source)s to %(target)s in link role %(linkrole)s has different balances'
             1758  CALL_FUNCTION_1       1  '1 positional argument'
             1760  CALL_FUNCTION_2       2  '2 positional arguments'
             1762  LOAD_ATTR                format

 L. 218      1764  LOAD_FAST                'modelRel'

 L. 219      1766  LOAD_FAST                'fromConcept'
             1768  LOAD_ATTR                qname
             1770  LOAD_FAST                'toConcept'
             1772  LOAD_ATTR                qname
             1774  LOAD_FAST                'ELR'
             1776  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
             1778  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1780  POP_TOP          
             1782  JUMP_BACK          1608  'to 1608'
             1786  POP_BLOCK        
           1788_0  COME_FROM_LOOP     1600  '1600'
             1788  JUMP_FORWARD       1858  'to 1858'
             1790  ELSE                     '1858'

 L. 220      1790  LOAD_FAST                'modelXbrl'
             1792  LOAD_ATTR                hasXDT
             1794  POP_JUMP_IF_FALSE  1830  'to 1830'
             1798  LOAD_FAST                'arcrole'
             1800  LOAD_ATTR                startswith
             1802  LOAD_GLOBAL              XbrlConst
             1804  LOAD_ATTR                dimStartsWith
             1806  CALL_FUNCTION_1       1  '1 positional argument'
             1808  POP_JUMP_IF_FALSE  1830  'to 1830'

 L. 221      1812  LOAD_GLOBAL              ValidateXbrlDimensions
             1814  LOAD_ATTR                checkBaseSet
             1816  LOAD_DEREF               'self'
             1818  LOAD_FAST                'arcrole'
             1820  LOAD_FAST                'ELR'
             1822  LOAD_FAST                'relsSet'
             1824  CALL_FUNCTION_4       4  '4 positional arguments'
             1826  POP_TOP          
             1828  JUMP_FORWARD       1858  'to 1858'
           1830_0  COME_FROM          1794  '1794'

 L. 222      1830  LOAD_FAST                'arcrole'
             1832  LOAD_GLOBAL              ValidateFormula
             1834  LOAD_ATTR                arcroleChecks
             1836  COMPARE_OP               in
             1838  POP_JUMP_IF_FALSE   532  'to 532'

 L. 223      1842  LOAD_GLOBAL              ValidateFormula
             1844  LOAD_ATTR                checkBaseSet
             1846  LOAD_DEREF               'self'
             1848  LOAD_FAST                'arcrole'
             1850  LOAD_FAST                'ELR'
             1852  LOAD_FAST                'relsSet'
             1854  CALL_FUNCTION_4       4  '4 positional arguments'
             1856  POP_TOP          
           1858_0  COME_FROM          1828  '1828'
           1858_1  COME_FROM          1788  '1788'
           1858_2  COME_FROM_LOOP     1092  '1092'
             1858  JUMP_BACK           532  'to 532'
             1862  POP_BLOCK        
           1864_0  COME_FROM_LOOP      518  '518'

 L. 224      1864  LOAD_CONST               True
             1866  LOAD_FAST                'modelXbrl'
             1868  STORE_ATTR               isDimensionsValidated

 L. 225      1870  LOAD_FAST                'modelXbrl'
             1872  LOAD_ATTR                profileStat
             1874  LOAD_GLOBAL              _
             1876  LOAD_STR                 'validateRelationships'
             1878  CALL_FUNCTION_1       1  '1 positional argument'
             1880  CALL_FUNCTION_1       1  '1 positional argument'
             1882  POP_TOP          

 L. 228      1884  LOAD_FAST                'modelXbrl'
             1886  LOAD_ATTR                modelManager
             1888  LOAD_ATTR                showStatus
             1890  LOAD_GLOBAL              _
             1892  LOAD_STR                 'validating instance'
             1894  CALL_FUNCTION_1       1  '1 positional argument'
             1896  CALL_FUNCTION_1       1  '1 positional argument'
             1898  POP_TOP          

 L. 229      1900  LOAD_FAST                'modelXbrl'
             1902  LOAD_ATTR                modelDocument
             1904  LOAD_ATTR                type
             1906  LOAD_GLOBAL              ModelDocument
             1908  LOAD_ATTR                Type
             1910  LOAD_ATTR                INSTANCE
             1912  COMPARE_OP               ==
             1914  POP_JUMP_IF_TRUE   1936  'to 1936'

 L. 230      1918  LOAD_FAST                'modelXbrl'
             1920  LOAD_ATTR                modelDocument
             1922  LOAD_ATTR                type
             1924  LOAD_GLOBAL              ModelDocument
             1926  LOAD_ATTR                Type
             1928  LOAD_ATTR                INLINEXBRL
             1930  COMPARE_OP               ==
           1932_0  COME_FROM          1914  '1914'
             1932  POP_JUMP_IF_FALSE  2064  'to 2064'

 L. 231      1936  LOAD_DEREF               'self'
             1938  LOAD_ATTR                checkFacts
             1940  LOAD_FAST                'modelXbrl'
             1942  LOAD_ATTR                facts
             1944  CALL_FUNCTION_1       1  '1 positional argument'
             1946  POP_TOP          

 L. 232      1948  LOAD_DEREF               'self'
             1950  LOAD_ATTR                checkContexts
             1952  LOAD_DEREF               'self'
             1954  LOAD_ATTR                modelXbrl
             1956  LOAD_ATTR                contexts
             1958  LOAD_ATTR                values
             1960  CALL_FUNCTION_0       0  '0 positional arguments'
             1962  CALL_FUNCTION_1       1  '1 positional argument'
             1964  POP_TOP          

 L. 233      1966  LOAD_DEREF               'self'
             1968  LOAD_ATTR                checkUnits
             1970  LOAD_DEREF               'self'
             1972  LOAD_ATTR                modelXbrl
             1974  LOAD_ATTR                units
             1976  LOAD_ATTR                values
             1978  CALL_FUNCTION_0       0  '0 positional arguments'
             1980  CALL_FUNCTION_1       1  '1 positional argument'
             1982  POP_TOP          

 L. 235      1984  LOAD_FAST                'modelXbrl'
             1986  LOAD_ATTR                profileStat
             1988  LOAD_GLOBAL              _
             1990  LOAD_STR                 'validateInstance'
             1992  CALL_FUNCTION_1       1  '1 positional argument'
             1994  CALL_FUNCTION_1       1  '1 positional argument'
             1996  POP_TOP          

 L. 237      1998  LOAD_FAST                'modelXbrl'
             2000  LOAD_ATTR                hasXDT
             2002  POP_JUMP_IF_FALSE  2064  'to 2064'

 L. 238      2006  LOAD_FAST                'modelXbrl'
             2008  LOAD_ATTR                modelManager
             2010  LOAD_ATTR                showStatus
             2012  LOAD_GLOBAL              _
             2014  LOAD_STR                 'validating dimensions'
             2016  CALL_FUNCTION_1       1  '1 positional argument'
             2018  CALL_FUNCTION_1       1  '1 positional argument'
             2020  POP_TOP          

 L. 248      2022  LOAD_DEREF               'self'
             2024  LOAD_ATTR                checkFactsDimensions
             2026  LOAD_FAST                'modelXbrl'
             2028  LOAD_ATTR                facts
             2030  CALL_FUNCTION_1       1  '1 positional argument'
             2032  POP_TOP          

 L. 249      2034  LOAD_DEREF               'self'
             2036  LOAD_ATTR                checkContextsDimensions
             2038  LOAD_FAST                'modelXbrl'
             2040  LOAD_ATTR                contexts
             2042  LOAD_ATTR                values
             2044  CALL_FUNCTION_0       0  '0 positional arguments'
             2046  CALL_FUNCTION_1       1  '1 positional argument'
             2048  POP_TOP          

 L. 250      2050  LOAD_FAST                'modelXbrl'
             2052  LOAD_ATTR                profileStat
             2054  LOAD_GLOBAL              _
             2056  LOAD_STR                 'validateDimensions'
             2058  CALL_FUNCTION_1       1  '1 positional argument'
             2060  CALL_FUNCTION_1       1  '1 positional argument'
             2062  POP_TOP          
           2064_0  COME_FROM          2002  '2002'
           2064_1  COME_FROM          1932  '1932'

 L. 254      2064  LOAD_FAST                'modelXbrl'
             2066  LOAD_ATTR                modelManager
             2068  LOAD_ATTR                showStatus
             2070  LOAD_GLOBAL              _
             2072  LOAD_STR                 'validating concepts'
             2074  CALL_FUNCTION_1       1  '1 positional argument'
             2076  CALL_FUNCTION_1       1  '1 positional argument'
             2078  POP_TOP          

 L. 255      2080  SETUP_LOOP         3152  'to 3152'
             2084  LOAD_FAST                'modelXbrl'
             2086  LOAD_ATTR                qnameConcepts
             2088  LOAD_ATTR                values
             2090  CALL_FUNCTION_0       0  '0 positional arguments'
             2092  GET_ITER         
             2094  FOR_ITER           3150  'to 3150'
             2098  STORE_FAST               'concept'

 L. 256      2100  LOAD_FAST                'concept'
             2102  LOAD_ATTR                type
             2104  STORE_FAST               'conceptType'

 L. 257      2106  LOAD_FAST                'concept'
             2108  LOAD_ATTR                qname
             2110  LOAD_CONST               None
             2112  COMPARE_OP               is
             2114  POP_JUMP_IF_TRUE   2094  'to 2094'

 L. 258      2118  LOAD_GLOBAL              XbrlConst
             2120  LOAD_ATTR                isStandardNamespace
             2122  LOAD_FAST                'concept'
             2124  LOAD_ATTR                qname
             2126  LOAD_ATTR                namespaceURI
             2128  CALL_FUNCTION_1       1  '1 positional argument'
             2130  POP_JUMP_IF_TRUE   2094  'to 2094'

 L. 259      2134  LOAD_FAST                'concept'
             2136  LOAD_ATTR                modelDocument
             2138  LOAD_ATTR                inDTS
             2140  UNARY_NOT        
             2142  POP_JUMP_IF_FALSE  2150  'to 2150'

 L. 260      2146  CONTINUE           2094  'to 2094'
           2150_0  COME_FROM          2142  '2142'

 L. 262      2150  LOAD_FAST                'concept'
             2152  LOAD_ATTR                isTuple
             2154  POP_JUMP_IF_FALSE  2618  'to 2618'

 L. 264      2158  LOAD_FAST                'concept'
             2160  LOAD_ATTR                getparent
             2162  CALL_FUNCTION_0       0  '0 positional arguments'
             2164  LOAD_ATTR                localName
             2166  LOAD_STR                 'schema'
             2168  COMPARE_OP               ==
             2170  POP_JUMP_IF_TRUE   2200  'to 2200'

 L. 265      2174  LOAD_DEREF               'self'
             2176  LOAD_ATTR                modelXbrl
             2178  LOAD_ATTR                error
             2180  LOAD_STR                 'xbrl.4.9:tupleGloballyDeclared'

 L. 266      2182  LOAD_GLOBAL              _
             2184  LOAD_STR                 'Tuple %(concept)s must be declared globally'
             2186  CALL_FUNCTION_1       1  '1 positional argument'

 L. 267      2188  LOAD_FAST                'concept'
             2190  LOAD_FAST                'concept'
             2192  LOAD_ATTR                qname
             2194  LOAD_CONST               ('modelObject', 'concept')
             2196  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2198  POP_TOP          
           2200_0  COME_FROM          2170  '2170'

 L. 268      2200  LOAD_FAST                'concept'
             2202  LOAD_ATTR                periodType
             2204  POP_JUMP_IF_FALSE  2234  'to 2234'

 L. 269      2208  LOAD_DEREF               'self'
             2210  LOAD_ATTR                modelXbrl
             2212  LOAD_ATTR                error
             2214  LOAD_STR                 'xbrl.4.9:tuplePeriodType'

 L. 270      2216  LOAD_GLOBAL              _
             2218  LOAD_STR                 'Tuple %(concept)s must not have periodType'
             2220  CALL_FUNCTION_1       1  '1 positional argument'

 L. 271      2222  LOAD_FAST                'concept'
             2224  LOAD_FAST                'concept'
             2226  LOAD_ATTR                qname
             2228  LOAD_CONST               ('modelObject', 'concept')
             2230  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2232  POP_TOP          
           2234_0  COME_FROM          2204  '2204'

 L. 272      2234  LOAD_FAST                'concept'
             2236  LOAD_ATTR                balance
             2238  POP_JUMP_IF_FALSE  2268  'to 2268'

 L. 273      2242  LOAD_DEREF               'self'
             2244  LOAD_ATTR                modelXbrl
             2246  LOAD_ATTR                error
             2248  LOAD_STR                 'xbrl.4.9:tupleBalance'

 L. 274      2250  LOAD_GLOBAL              _
             2252  LOAD_STR                 'Tuple %(concept)s must not have balance'
             2254  CALL_FUNCTION_1       1  '1 positional argument'

 L. 275      2256  LOAD_FAST                'concept'
             2258  LOAD_FAST                'concept'
             2260  LOAD_ATTR                qname
             2262  LOAD_CONST               ('modelObject', 'concept')
             2264  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2266  POP_TOP          
           2268_0  COME_FROM          2238  '2238'

 L. 276      2268  LOAD_FAST                'conceptType'
             2270  LOAD_CONST               None
             2272  COMPARE_OP               is-not
             2274  POP_JUMP_IF_FALSE  2898  'to 2898'

 L. 278      2278  SETUP_LOOP         2372  'to 2372'
             2280  LOAD_FAST                'conceptType'
             2282  LOAD_ATTR                attributes
             2284  LOAD_ATTR                values
             2286  CALL_FUNCTION_0       0  '0 positional arguments'
             2288  GET_ITER         
             2290  FOR_ITER           2370  'to 2370'
             2292  STORE_FAST               'attribute'

 L. 279      2294  LOAD_FAST                'attribute'
             2296  LOAD_ATTR                qname
             2298  LOAD_CONST               None
             2300  COMPARE_OP               is-not
             2302  POP_JUMP_IF_FALSE  2290  'to 2290'
             2306  LOAD_FAST                'attribute'
             2308  LOAD_ATTR                qname
             2310  LOAD_ATTR                namespaceURI
             2312  LOAD_GLOBAL              XbrlConst
             2314  LOAD_ATTR                xbrli
             2316  LOAD_GLOBAL              XbrlConst
             2318  LOAD_ATTR                link
             2320  LOAD_GLOBAL              XbrlConst
             2322  LOAD_ATTR                xlink
             2324  LOAD_GLOBAL              XbrlConst
             2326  LOAD_ATTR                xl
             2328  BUILD_TUPLE_4         4 
             2330  COMPARE_OP               in
             2332  POP_JUMP_IF_FALSE  2290  'to 2290'

 L. 280      2336  LOAD_DEREF               'self'
             2338  LOAD_ATTR                modelXbrl
             2340  LOAD_ATTR                error
             2342  LOAD_STR                 'xbrl.4.9:tupleAttribute'

 L. 281      2344  LOAD_GLOBAL              _
             2346  LOAD_STR                 'Tuple %(concept)s must not have attribute in this namespace %(attribute)s'
             2348  CALL_FUNCTION_1       1  '1 positional argument'

 L. 282      2350  LOAD_FAST                'concept'
             2352  LOAD_FAST                'concept'
             2354  LOAD_ATTR                qname
             2356  LOAD_FAST                'attribute'
             2358  LOAD_ATTR                qname
             2360  LOAD_CONST               ('modelObject', 'concept', 'attribute')
             2362  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2364  POP_TOP          
             2366  JUMP_BACK          2290  'to 2290'
             2370  POP_BLOCK        
           2372_0  COME_FROM_LOOP     2278  '2278'

 L. 284      2372  LOAD_GLOBAL              XmlUtil
             2374  LOAD_ATTR                descendantAttr
             2376  LOAD_FAST                'conceptType'
             2378  LOAD_GLOBAL              XbrlConst
             2380  LOAD_ATTR                xsd
             2382  LOAD_CONST               ('complexType', 'complexContent')
             2384  LOAD_STR                 'mixed'
             2386  CALL_FUNCTION_4       4  '4 positional arguments'
             2388  LOAD_STR                 'true'
             2390  COMPARE_OP               ==
             2392  POP_JUMP_IF_FALSE  2422  'to 2422'

 L. 285      2396  LOAD_DEREF               'self'
             2398  LOAD_ATTR                modelXbrl
             2400  LOAD_ATTR                error
             2402  LOAD_STR                 'xbrl.4.9:tupleMixedContent'

 L. 286      2404  LOAD_GLOBAL              _
             2406  LOAD_STR                 'Tuple %(concept)s must not have mixed content'
             2408  CALL_FUNCTION_1       1  '1 positional argument'

 L. 287      2410  LOAD_FAST                'concept'
             2412  LOAD_FAST                'concept'
             2414  LOAD_ATTR                qname
             2416  LOAD_CONST               ('modelObject', 'concept')
             2418  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2420  POP_TOP          
           2422_0  COME_FROM          2392  '2392'

 L. 288      2422  LOAD_GLOBAL              XmlUtil
             2424  LOAD_ATTR                descendant
             2426  LOAD_FAST                'conceptType'
             2428  LOAD_GLOBAL              XbrlConst
             2430  LOAD_ATTR                xsd
             2432  LOAD_STR                 'simpleContent'
             2434  CALL_FUNCTION_3       3  '3 positional arguments'
             2436  POP_JUMP_IF_FALSE  2466  'to 2466'

 L. 289      2440  LOAD_DEREF               'self'
             2442  LOAD_ATTR                modelXbrl
             2444  LOAD_ATTR                error
             2446  LOAD_STR                 'xbrl.4.9:tupleSimpleContent'

 L. 290      2448  LOAD_GLOBAL              _
             2450  LOAD_STR                 'Tuple %(concept)s must not have simple content'
             2452  CALL_FUNCTION_1       1  '1 positional argument'

 L. 291      2454  LOAD_FAST                'concept'
             2456  LOAD_FAST                'concept'
             2458  LOAD_ATTR                qname
             2460  LOAD_CONST               ('modelObject', 'concept')
             2462  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2464  POP_TOP          
           2466_0  COME_FROM          2436  '2436'

 L. 293      2466  SETUP_LOOP         2614  'to 2614'
             2468  LOAD_FAST                'conceptType'
             2470  LOAD_ATTR                elements
             2472  GET_ITER         
             2474  FOR_ITER           2612  'to 2612'
             2476  STORE_FAST               'elementQname'

 L. 294      2478  LOAD_DEREF               'self'
             2480  LOAD_ATTR                modelXbrl
             2482  LOAD_ATTR                qnameConcepts
             2484  LOAD_ATTR                get
             2486  LOAD_FAST                'elementQname'
             2488  CALL_FUNCTION_1       1  '1 positional argument'
             2490  STORE_FAST               'childConcept'

 L. 295      2492  LOAD_FAST                'childConcept'
             2494  LOAD_CONST               None
             2496  COMPARE_OP               is
             2498  POP_JUMP_IF_FALSE  2536  'to 2536'

 L. 296      2502  LOAD_DEREF               'self'
             2504  LOAD_ATTR                modelXbrl
             2506  LOAD_ATTR                error
             2508  LOAD_STR                 'xbrl.4.9:tupleElementUndefined'

 L. 297      2510  LOAD_GLOBAL              _
             2512  LOAD_STR                 'Tuple %(concept)s element %(tupleElement)s not defined'
             2514  CALL_FUNCTION_1       1  '1 positional argument'

 L. 298      2516  LOAD_FAST                'concept'
             2518  LOAD_GLOBAL              str
             2520  LOAD_FAST                'concept'
             2522  LOAD_ATTR                qname
             2524  CALL_FUNCTION_1       1  '1 positional argument'
             2526  LOAD_FAST                'elementQname'
             2528  LOAD_CONST               ('modelObject', 'concept', 'tupleElement')
             2530  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2532  POP_TOP          
             2534  JUMP_FORWARD       2608  'to 2608'
             2536  ELSE                     '2608'

 L. 299      2536  LOAD_FAST                'childConcept'
             2538  LOAD_ATTR                isItem
             2540  JUMP_IF_TRUE_OR_POP  2576  'to 2576'
             2544  LOAD_FAST                'childConcept'
             2546  LOAD_ATTR                isTuple
             2548  JUMP_IF_TRUE_OR_POP  2576  'to 2576'

 L. 300      2552  LOAD_FAST                'childConcept'
             2554  LOAD_ATTR                qname
             2556  LOAD_GLOBAL              XbrlConst
             2558  LOAD_ATTR                qnXbrliItem
             2560  COMPARE_OP               ==
             2562  JUMP_IF_TRUE_OR_POP  2576  'to 2576'

 L. 301      2566  LOAD_FAST                'childConcept'
             2568  LOAD_ATTR                qname
             2570  LOAD_GLOBAL              XbrlConst
             2572  LOAD_ATTR                qnXbrliTuple
             2574  COMPARE_OP               ==
           2576_0  COME_FROM          2562  '2562'
           2576_1  COME_FROM          2548  '2548'
           2576_2  COME_FROM          2540  '2540'
             2576  POP_JUMP_IF_TRUE   2474  'to 2474'

 L. 302      2580  LOAD_DEREF               'self'
             2582  LOAD_ATTR                modelXbrl
             2584  LOAD_ATTR                error
             2586  LOAD_STR                 'xbrl.4.9:tupleElementItemOrTuple'

 L. 303      2588  LOAD_GLOBAL              _
             2590  LOAD_STR                 'Tuple %(concept)s must not have element %(tupleElement)s not an item or tuple'
             2592  CALL_FUNCTION_1       1  '1 positional argument'

 L. 304      2594  LOAD_FAST                'concept'
             2596  LOAD_FAST                'concept'
             2598  LOAD_ATTR                qname
             2600  LOAD_FAST                'elementQname'
             2602  LOAD_CONST               ('modelObject', 'concept', 'tupleElement')
             2604  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2606  POP_TOP          
           2608_0  COME_FROM          2534  '2534'
             2608  JUMP_BACK          2474  'to 2474'
             2612  POP_BLOCK        
           2614_0  COME_FROM_LOOP     2466  '2466'
             2614  JUMP_FORWARD       2898  'to 2898'
             2618  ELSE                     '2898'

 L. 305      2618  LOAD_FAST                'concept'
             2620  LOAD_ATTR                isItem
             2622  POP_JUMP_IF_FALSE  2898  'to 2898'

 L. 306      2626  LOAD_FAST                'concept'
             2628  LOAD_ATTR                periodType
             2630  LOAD_GLOBAL              periodTypeValues
             2632  COMPARE_OP               not-in
             2634  POP_JUMP_IF_FALSE  2664  'to 2664'

 L. 307      2638  LOAD_DEREF               'self'
             2640  LOAD_ATTR                modelXbrl
             2642  LOAD_ATTR                error
             2644  LOAD_STR                 'xbrl.5.1.1.1:itemPeriodType'

 L. 308      2646  LOAD_GLOBAL              _
             2648  LOAD_STR                 'Item %(concept)s must have a valid periodType'
             2650  CALL_FUNCTION_1       1  '1 positional argument'

 L. 309      2652  LOAD_FAST                'concept'
             2654  LOAD_FAST                'concept'
             2656  LOAD_ATTR                qname
             2658  LOAD_CONST               ('modelObject', 'concept')
             2660  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2662  POP_TOP          
           2664_0  COME_FROM          2634  '2634'

 L. 310      2664  LOAD_FAST                'concept'
             2666  LOAD_ATTR                isMonetary
             2668  POP_JUMP_IF_FALSE  2716  'to 2716'

 L. 311      2672  LOAD_FAST                'concept'
             2674  LOAD_ATTR                balance
             2676  LOAD_GLOBAL              balanceValues
             2678  COMPARE_OP               not-in
             2680  POP_JUMP_IF_FALSE  2750  'to 2750'

 L. 312      2684  LOAD_DEREF               'self'
             2686  LOAD_ATTR                modelXbrl
             2688  LOAD_ATTR                error
             2690  LOAD_STR                 'xbrl.5.1.1.2:itemBalance'

 L. 313      2692  LOAD_GLOBAL              _
             2694  LOAD_STR                 'Item %(concept)s must have a valid balance %(balance)s'
             2696  CALL_FUNCTION_1       1  '1 positional argument'

 L. 314      2698  LOAD_FAST                'concept'
             2700  LOAD_FAST                'concept'
             2702  LOAD_ATTR                qname
             2704  LOAD_FAST                'concept'
             2706  LOAD_ATTR                balance
             2708  LOAD_CONST               ('modelObject', 'concept', 'balance')
             2710  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2712  POP_TOP          
             2714  JUMP_FORWARD       2750  'to 2750'
             2716  ELSE                     '2750'

 L. 316      2716  LOAD_FAST                'concept'
             2718  LOAD_ATTR                balance
             2720  POP_JUMP_IF_FALSE  2750  'to 2750'

 L. 317      2724  LOAD_DEREF               'self'
             2726  LOAD_ATTR                modelXbrl
             2728  LOAD_ATTR                error
             2730  LOAD_STR                 'xbrl.5.1.1.2:itemBalance'

 L. 318      2732  LOAD_GLOBAL              _
             2734  LOAD_STR                 'Item %(concept)s may not have a balance'
             2736  CALL_FUNCTION_1       1  '1 positional argument'

 L. 319      2738  LOAD_FAST                'concept'
             2740  LOAD_FAST                'concept'
             2742  LOAD_ATTR                qname
             2744  LOAD_CONST               ('modelObject', 'concept')
             2746  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2748  POP_TOP          
           2750_0  COME_FROM          2720  '2720'
           2750_1  COME_FROM          2714  '2714'
           2750_2  COME_FROM          2680  '2680'

 L. 320      2750  LOAD_FAST                'concept'
             2752  LOAD_ATTR                baseXbrliType
             2754  LOAD_GLOBAL              baseXbrliTypes
             2756  COMPARE_OP               not-in
             2758  POP_JUMP_IF_FALSE  2792  'to 2792'

 L. 321      2762  LOAD_DEREF               'self'
             2764  LOAD_ATTR                modelXbrl
             2766  LOAD_ATTR                error
             2768  LOAD_STR                 'xbrl.5.1.1.3:itemType'

 L. 322      2770  LOAD_GLOBAL              _
             2772  LOAD_STR                 'Item %(concept)s type %(itemType)s invalid'
             2774  CALL_FUNCTION_1       1  '1 positional argument'

 L. 323      2776  LOAD_FAST                'concept'
             2778  LOAD_FAST                'concept'
             2780  LOAD_ATTR                qname
             2782  LOAD_FAST                'concept'
             2784  LOAD_ATTR                baseXbrliType
             2786  LOAD_CONST               ('modelObject', 'concept', 'itemType')
             2788  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2790  POP_TOP          
           2792_0  COME_FROM          2758  '2758'

 L. 324      2792  LOAD_FAST                'modelXbrl'
             2794  LOAD_ATTR                hasXDT
             2796  POP_JUMP_IF_FALSE  2898  'to 2898'

 L. 325      2800  LOAD_FAST                'concept'
             2802  LOAD_ATTR                isHypercubeItem
             2804  POP_JUMP_IF_FALSE  2850  'to 2850'
             2808  LOAD_FAST                'concept'
             2810  LOAD_ATTR                abstract
             2812  LOAD_STR                 'true'
             2814  COMPARE_OP               ==
             2816  UNARY_NOT        
             2818  POP_JUMP_IF_FALSE  2850  'to 2850'

 L. 326      2822  LOAD_DEREF               'self'
             2824  LOAD_ATTR                modelXbrl
             2826  LOAD_ATTR                error
             2828  LOAD_STR                 'xbrldte:HypercubeElementIsNotAbstractError'

 L. 327      2830  LOAD_GLOBAL              _
             2832  LOAD_STR                 'Hypercube item %(concept)s must be abstract'
             2834  CALL_FUNCTION_1       1  '1 positional argument'

 L. 328      2836  LOAD_FAST                'concept'
             2838  LOAD_FAST                'concept'
             2840  LOAD_ATTR                qname
             2842  LOAD_CONST               ('modelObject', 'concept')
             2844  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2846  POP_TOP          
             2848  JUMP_FORWARD       2898  'to 2898'
           2850_0  COME_FROM          2804  '2804'

 L. 329      2850  LOAD_FAST                'concept'
             2852  LOAD_ATTR                isDimensionItem
             2854  POP_JUMP_IF_FALSE  2898  'to 2898'
             2858  LOAD_FAST                'concept'
             2860  LOAD_ATTR                abstract
             2862  LOAD_STR                 'true'
             2864  COMPARE_OP               ==
             2866  UNARY_NOT        
             2868  POP_JUMP_IF_FALSE  2898  'to 2898'

 L. 330      2872  LOAD_DEREF               'self'
             2874  LOAD_ATTR                modelXbrl
             2876  LOAD_ATTR                error
             2878  LOAD_STR                 'xbrldte:DimensionElementIsNotAbstractError'

 L. 331      2880  LOAD_GLOBAL              _
             2882  LOAD_STR                 'Dimension item %(concept)s must be abstract'
             2884  CALL_FUNCTION_1       1  '1 positional argument'

 L. 332      2886  LOAD_FAST                'concept'
             2888  LOAD_FAST                'concept'
             2890  LOAD_ATTR                qname
             2892  LOAD_CONST               ('modelObject', 'concept')
             2894  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2896  POP_TOP          
           2898_0  COME_FROM          2868  '2868'
           2898_1  COME_FROM          2854  '2854'
           2898_2  COME_FROM          2848  '2848'
           2898_3  COME_FROM          2796  '2796'
           2898_4  COME_FROM          2622  '2622'
           2898_5  COME_FROM          2614  '2614'

 L. 333      2898  LOAD_DEREF               'self'
             2900  LOAD_ATTR                validateEnum
             2902  POP_JUMP_IF_FALSE  3126  'to 3126'
             2906  LOAD_FAST                'concept'
             2908  LOAD_ATTR                isEnumeration
             2910  POP_JUMP_IF_FALSE  3126  'to 3126'

 L. 334      2914  LOAD_FAST                'concept'
             2916  LOAD_ATTR                enumDomainQname
             2918  POP_JUMP_IF_TRUE   2974  'to 2974'

 L. 335      2922  LOAD_DEREF               'self'
             2924  LOAD_ATTR                modelXbrl
             2926  LOAD_ATTR                error
             2928  LOAD_FAST                'concept'
             2930  LOAD_ATTR                instanceOfType
             2932  LOAD_GLOBAL              XbrlConst
             2934  LOAD_ATTR                qnEnumeration2ItemTypes
             2936  CALL_FUNCTION_1       1  '1 positional argument'
             2938  POP_JUMP_IF_FALSE  2946  'to 2946'
             2942  LOAD_STR                 'enum2te:'
             2944  JUMP_FORWARD       2948  'to 2948'
             2946  ELSE                     '2948'
             2946  LOAD_STR                 'enumte:'
           2948_0  COME_FROM          2944  '2944'

 L. 336      2948  LOAD_STR                 'MissingDomainError'
             2950  BINARY_ADD       

 L. 337      2952  LOAD_GLOBAL              _
             2954  LOAD_STR                 'Item %(concept)s enumeration type must specify a domain.'
             2956  CALL_FUNCTION_1       1  '1 positional argument'

 L. 338      2958  LOAD_FAST                'concept'
             2960  LOAD_FAST                'concept'
             2962  LOAD_ATTR                qname

 L. 339      2964  LOAD_CONST               ('enumte:MissingDomainError', 'enum2te:MissingDomainError')
             2966  LOAD_CONST               ('modelObject', 'concept', 'messageCodes')
             2968  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2970  POP_TOP          
             2972  JUMP_FORWARD       3068  'to 3068'
             2974  ELSE                     '3068'

 L. 340      2974  LOAD_FAST                'concept'
             2976  LOAD_ATTR                enumDomain
             2978  LOAD_CONST               None
             2980  COMPARE_OP               is
             2982  POP_JUMP_IF_TRUE   3018  'to 3018'
             2986  LOAD_FAST                'concept'
             2988  LOAD_ATTR                enumDomain
             2990  LOAD_ATTR                isItem
             2992  UNARY_NOT        
             2994  POP_JUMP_IF_TRUE   3018  'to 3018'
             2998  LOAD_FAST                'concept'
             3000  LOAD_ATTR                enumDomain
             3002  LOAD_ATTR                isHypercubeItem
             3004  POP_JUMP_IF_TRUE   3018  'to 3018'
             3008  LOAD_FAST                'concept'
             3010  LOAD_ATTR                enumDomain
             3012  LOAD_ATTR                isDimensionItem
           3014_0  COME_FROM          3004  '3004'
           3014_1  COME_FROM          2994  '2994'
           3014_2  COME_FROM          2982  '2982'
             3014  POP_JUMP_IF_FALSE  3068  'to 3068'

 L. 341      3018  LOAD_DEREF               'self'
             3020  LOAD_ATTR                modelXbrl
             3022  LOAD_ATTR                error
             3024  LOAD_FAST                'concept'
             3026  LOAD_ATTR                instanceOfType
             3028  LOAD_GLOBAL              XbrlConst
             3030  LOAD_ATTR                qnEnumeration2ItemTypes
             3032  CALL_FUNCTION_1       1  '1 positional argument'
             3034  POP_JUMP_IF_FALSE  3042  'to 3042'
             3038  LOAD_STR                 'enum2te:'
             3040  JUMP_FORWARD       3044  'to 3044'
             3042  ELSE                     '3044'
             3042  LOAD_STR                 'enumte:'
           3044_0  COME_FROM          3040  '3040'

 L. 342      3044  LOAD_STR                 'InvalidDomainError'
             3046  BINARY_ADD       

 L. 343      3048  LOAD_GLOBAL              _
             3050  LOAD_STR                 'Item %(concept)s enumeration type must be a xbrli:item that is neither a hypercube nor dimension.'
             3052  CALL_FUNCTION_1       1  '1 positional argument'

 L. 344      3054  LOAD_FAST                'concept'
             3056  LOAD_FAST                'concept'
             3058  LOAD_ATTR                qname

 L. 345      3060  LOAD_CONST               ('enumte:InvalidDomainError', 'enum2te:InvalidDomainError')
             3062  LOAD_CONST               ('modelObject', 'concept', 'messageCodes')
             3064  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             3066  POP_TOP          
           3068_0  COME_FROM          3014  '3014'
           3068_1  COME_FROM          2972  '2972'

 L. 346      3068  LOAD_FAST                'concept'
             3070  LOAD_ATTR                enumLinkrole
             3072  POP_JUMP_IF_TRUE   3126  'to 3126'

 L. 347      3076  LOAD_DEREF               'self'
             3078  LOAD_ATTR                modelXbrl
             3080  LOAD_ATTR                error
             3082  LOAD_FAST                'concept'
             3084  LOAD_ATTR                instanceOfType
             3086  LOAD_GLOBAL              XbrlConst
             3088  LOAD_ATTR                qnEnumeration2ItemTypes
             3090  CALL_FUNCTION_1       1  '1 positional argument'
             3092  POP_JUMP_IF_FALSE  3100  'to 3100'
             3096  LOAD_STR                 'enum2te:'
             3098  JUMP_FORWARD       3102  'to 3102'
             3100  ELSE                     '3102'
             3100  LOAD_STR                 'enumte:'
           3102_0  COME_FROM          3098  '3098'

 L. 348      3102  LOAD_STR                 'MissingLinkRoleError'
             3104  BINARY_ADD       

 L. 349      3106  LOAD_GLOBAL              _
             3108  LOAD_STR                 'Item %(concept)s enumeration type must specify a linkrole.'
             3110  CALL_FUNCTION_1       1  '1 positional argument'

 L. 350      3112  LOAD_FAST                'concept'
             3114  LOAD_FAST                'concept'
             3116  LOAD_ATTR                qname

 L. 351      3118  LOAD_CONST               ('enumte:MissingLinkRoleError', 'enum2te:MissingLinkRoleError')
             3120  LOAD_CONST               ('modelObject', 'concept', 'messageCodes')
             3122  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             3124  POP_TOP          
           3126_0  COME_FROM          3072  '3072'
           3126_1  COME_FROM          2910  '2910'
           3126_2  COME_FROM          2902  '2902'

 L. 352      3126  LOAD_FAST                'modelXbrl'
             3128  LOAD_ATTR                hasXDT
             3130  POP_JUMP_IF_FALSE  2094  'to 2094'

 L. 353      3134  LOAD_GLOBAL              ValidateXbrlDimensions
             3136  LOAD_ATTR                checkConcept
             3138  LOAD_DEREF               'self'
             3140  LOAD_FAST                'concept'
             3142  CALL_FUNCTION_2       2  '2 positional arguments'
             3144  POP_TOP          
             3146  JUMP_BACK          2094  'to 2094'
             3150  POP_BLOCK        
           3152_0  COME_FROM_LOOP     2080  '2080'

 L. 354      3152  LOAD_FAST                'modelXbrl'
             3154  LOAD_ATTR                profileStat
             3156  LOAD_GLOBAL              _
             3158  LOAD_STR                 'validateConcepts'
             3160  CALL_FUNCTION_1       1  '1 positional argument'
             3162  CALL_FUNCTION_1       1  '1 positional argument'
             3164  POP_TOP          

 L. 356      3166  SETUP_LOOP         3194  'to 3194'
             3168  LOAD_GLOBAL              pluginClassMethods
             3170  LOAD_STR                 'Validate.XBRL.Finally'
             3172  CALL_FUNCTION_1       1  '1 positional argument'
             3174  GET_ITER         
             3176  FOR_ITER           3192  'to 3192'
             3178  STORE_FAST               'pluginXbrlMethod'

 L. 357      3180  LOAD_FAST                'pluginXbrlMethod'
             3182  LOAD_DEREF               'self'
             3184  CALL_FUNCTION_1       1  '1 positional argument'
             3186  POP_TOP          
             3188  JUMP_BACK          3176  'to 3176'
             3192  POP_BLOCK        
           3194_0  COME_FROM_LOOP     3166  '3166'

 L. 359      3194  LOAD_FAST                'modelXbrl'
             3196  LOAD_ATTR                profileStat
             3198  CALL_FUNCTION_0       0  '0 positional arguments'
             3200  POP_TOP          

 L. 361      3202  LOAD_FAST                'modelXbrl'
             3204  LOAD_ATTR                modelManager
             3206  LOAD_ATTR                showStatus
             3208  LOAD_GLOBAL              _
             3210  LOAD_STR                 'validating DTS'
             3212  CALL_FUNCTION_1       1  '1 positional argument'
             3214  CALL_FUNCTION_1       1  '1 positional argument'
             3216  POP_TOP          

 L. 362      3218  BUILD_MAP_0           0 
             3220  LOAD_DEREF               'self'
             3222  STORE_ATTR               DTSreferenceResourceIDs

 L. 363      3224  LOAD_GLOBAL              set
             3226  CALL_FUNCTION_0       0  '0 positional arguments'
             3228  STORE_FAST               'checkedModelDocuments'

 L. 364      3230  LOAD_GLOBAL              ValidateXbrlDTS
             3232  LOAD_ATTR                checkDTS
             3234  LOAD_DEREF               'self'
             3236  LOAD_FAST                'modelXbrl'
             3238  LOAD_ATTR                modelDocument
             3240  LOAD_FAST                'checkedModelDocuments'
             3242  CALL_FUNCTION_3       3  '3 positional arguments'
             3244  POP_TOP          

 L. 366      3246  SETUP_LOOP         3290  'to 3290'
             3248  LOAD_GLOBAL              set
             3250  LOAD_FAST                'modelXbrl'
             3252  LOAD_ATTR                urlDocs
             3254  LOAD_ATTR                values
             3256  CALL_FUNCTION_0       0  '0 positional arguments'
             3258  CALL_FUNCTION_1       1  '1 positional argument'
             3260  LOAD_FAST                'checkedModelDocuments'
             3262  BINARY_SUBTRACT  
             3264  GET_ITER         
             3266  FOR_ITER           3288  'to 3288'
             3268  STORE_FAST               'importedModelDocument'

 L. 367      3270  LOAD_GLOBAL              ValidateXbrlDTS
             3272  LOAD_ATTR                checkDTS
             3274  LOAD_DEREF               'self'
             3276  LOAD_FAST                'importedModelDocument'
             3278  LOAD_FAST                'checkedModelDocuments'
             3280  CALL_FUNCTION_3       3  '3 positional arguments'
             3282  POP_TOP          
             3284  JUMP_BACK          3266  'to 3266'
             3288  POP_BLOCK        
           3290_0  COME_FROM_LOOP     3246  '3246'

 L. 368      3290  DELETE_FAST              'checkedModelDocuments'
             3292  LOAD_DEREF               'self'
             3294  DELETE_ATTR              DTSreferenceResourceIDs

 L. 371      3296  LOAD_GLOBAL              validateUniqueParticleAttribution
             3298  LOAD_CONST               None
             3300  COMPARE_OP               is
             3302  POP_JUMP_IF_FALSE  3318  'to 3318'

 L. 372      3306  LOAD_CONST               0
             3308  LOAD_CONST               ('validateUniqueParticleAttribution',)
             3310  IMPORT_NAME              arelle.XmlValidateParticles
             3312  IMPORT_FROM              validateUniqueParticleAttribution
             3314  STORE_GLOBAL             validateUniqueParticleAttribution
             3316  POP_TOP          
           3318_0  COME_FROM          3302  '3302'

 L. 373      3318  SETUP_LOOP         3354  'to 3354'
             3320  LOAD_FAST                'modelXbrl'
             3322  LOAD_ATTR                qnameTypes
             3324  LOAD_ATTR                values
             3326  CALL_FUNCTION_0       0  '0 positional arguments'
             3328  GET_ITER         
             3330  FOR_ITER           3352  'to 3352'
             3332  STORE_FAST               'modelType'

 L. 374      3334  LOAD_GLOBAL              validateUniqueParticleAttribution
             3336  LOAD_FAST                'modelXbrl'
             3338  LOAD_FAST                'modelType'
             3340  LOAD_ATTR                particlesList
             3342  LOAD_FAST                'modelType'
             3344  CALL_FUNCTION_3       3  '3 positional arguments'
             3346  POP_TOP          
             3348  JUMP_BACK          3330  'to 3330'
             3352  POP_BLOCK        
           3354_0  COME_FROM_LOOP     3318  '3318'

 L. 375      3354  LOAD_FAST                'modelXbrl'
             3356  LOAD_ATTR                profileStat
             3358  LOAD_GLOBAL              _
             3360  LOAD_STR                 'validateDTS'
             3362  CALL_FUNCTION_1       1  '1 positional argument'
             3364  CALL_FUNCTION_1       1  '1 positional argument'
             3366  POP_TOP          

 L. 377      3368  LOAD_DEREF               'self'
             3370  LOAD_ATTR                validateCalcLB
             3372  POP_JUMP_IF_FALSE  3426  'to 3426'

 L. 378      3376  LOAD_FAST                'modelXbrl'
             3378  LOAD_ATTR                modelManager
             3380  LOAD_ATTR                showStatus
             3382  LOAD_GLOBAL              _
             3384  LOAD_STR                 'Validating instance calculations'
             3386  CALL_FUNCTION_1       1  '1 positional argument'
             3388  CALL_FUNCTION_1       1  '1 positional argument'
             3390  POP_TOP          

 L. 379      3392  LOAD_GLOBAL              ValidateXbrlCalcs
             3394  LOAD_ATTR                validate
             3396  LOAD_FAST                'modelXbrl'

 L. 380      3398  LOAD_DEREF               'self'
             3400  LOAD_ATTR                validateInferDecimals

 L. 381      3402  LOAD_DEREF               'self'
             3404  LOAD_ATTR                validateDedupCalcs
             3406  LOAD_CONST               ('inferDecimals', 'deDuplicate')
             3408  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             3410  POP_TOP          

 L. 382      3412  LOAD_FAST                'modelXbrl'
             3414  LOAD_ATTR                profileStat
             3416  LOAD_GLOBAL              _
             3418  LOAD_STR                 'validateCalculations'
             3420  CALL_FUNCTION_1       1  '1 positional argument'
             3422  CALL_FUNCTION_1       1  '1 positional argument'
             3424  POP_TOP          
           3426_0  COME_FROM          3372  '3372'

 L. 384      3426  LOAD_DEREF               'self'
             3428  LOAD_ATTR                validateUTR
             3430  POP_JUMP_IF_FALSE  3458  'to 3458'

 L. 385      3434  LOAD_GLOBAL              ValidateUtr
             3436  LOAD_ATTR                validateFacts
             3438  LOAD_FAST                'modelXbrl'
             3440  CALL_FUNCTION_1       1  '1 positional argument'
             3442  POP_TOP          

 L. 386      3444  LOAD_FAST                'modelXbrl'
             3446  LOAD_ATTR                profileStat
             3448  LOAD_GLOBAL              _
             3450  LOAD_STR                 'validateUTR'
             3452  CALL_FUNCTION_1       1  '1 positional argument'
             3454  CALL_FUNCTION_1       1  '1 positional argument'
             3456  POP_TOP          
           3458_0  COME_FROM          3430  '3430'

 L. 388      3458  LOAD_DEREF               'self'
             3460  LOAD_ATTR                validateIXDS
             3462  POP_JUMP_IF_FALSE  4986  'to 4986'

 L. 389      3466  LOAD_FAST                'modelXbrl'
             3468  LOAD_ATTR                modelManager
             3470  LOAD_ATTR                showStatus
             3472  LOAD_GLOBAL              _
             3474  LOAD_STR                 'Validating inline document set'
             3476  CALL_FUNCTION_1       1  '1 positional argument'
             3478  CALL_FUNCTION_1       1  '1 positional argument'
             3480  POP_TOP          

 L. 390      3482  LOAD_FAST                'modelXbrl'
             3484  LOAD_ATTR                modelDocument
             3486  LOAD_ATTR                ixNS
             3488  STORE_FAST               '_ixNS'

 L. 391      3490  LOAD_GLOBAL              defaultdict
             3492  LOAD_GLOBAL              list
             3494  CALL_FUNCTION_1       1  '1 positional argument'
             3496  STORE_FAST               'ixdsIdObjects'

 L. 392      3498  SETUP_LOOP         3586  'to 3586'
             3500  LOAD_DEREF               'self'
             3502  LOAD_ATTR                ixdsDocs
             3504  GET_ITER         
             3506  FOR_ITER           3584  'to 3584'
             3508  STORE_FAST               'ixdsDoc'

 L. 393      3510  SETUP_LOOP         3580  'to 3580'
             3512  LOAD_FAST                'ixdsDoc'
             3514  LOAD_ATTR                idObjects
             3516  LOAD_ATTR                values
             3518  CALL_FUNCTION_0       0  '0 positional arguments'
             3520  GET_ITER         
             3522  FOR_ITER           3578  'to 3578'
             3524  STORE_FAST               'idObject'

 L. 394      3526  LOAD_FAST                'idObject'
             3528  LOAD_ATTR                namespaceURI
             3530  LOAD_GLOBAL              ixbrlAll
             3532  COMPARE_OP               in
             3534  POP_JUMP_IF_TRUE   3558  'to 3558'
             3538  LOAD_FAST                'idObject'
             3540  LOAD_ATTR                elementQname
             3542  LOAD_GLOBAL              XbrlConst
             3544  LOAD_ATTR                qnXbrliContext
             3546  LOAD_GLOBAL              XbrlConst
             3548  LOAD_ATTR                qnXbrliUnit
             3550  BUILD_TUPLE_2         2 
             3552  COMPARE_OP               in
           3554_0  COME_FROM          3534  '3534'
             3554  POP_JUMP_IF_FALSE  3522  'to 3522'

 L. 395      3558  LOAD_FAST                'ixdsIdObjects'
             3560  LOAD_FAST                'idObject'
             3562  LOAD_ATTR                id
             3564  BINARY_SUBSCR    
             3566  LOAD_ATTR                append
             3568  LOAD_FAST                'idObject'
             3570  CALL_FUNCTION_1       1  '1 positional argument'
             3572  POP_TOP          
             3574  JUMP_BACK          3522  'to 3522'
             3578  POP_BLOCK        
           3580_0  COME_FROM_LOOP     3510  '3510'
             3580  JUMP_BACK          3506  'to 3506'
             3584  POP_BLOCK        
           3586_0  COME_FROM_LOOP     3498  '3498'

 L. 396      3586  SETUP_LOOP         3690  'to 3690'
             3588  LOAD_FAST                'ixdsIdObjects'
             3590  LOAD_ATTR                items
             3592  CALL_FUNCTION_0       0  '0 positional arguments'
             3594  GET_ITER         
             3596  FOR_ITER           3688  'to 3688'
             3598  UNPACK_SEQUENCE_2     2 
             3600  STORE_FAST               '_id'
             3602  STORE_FAST               'objs'

 L. 397      3604  LOAD_GLOBAL              len
             3606  LOAD_FAST                'objs'
             3608  CALL_FUNCTION_1       1  '1 positional argument'
             3610  LOAD_CONST               1
             3612  COMPARE_OP               >
             3614  POP_JUMP_IF_FALSE  3596  'to 3596'

 L. 398      3618  LOAD_FAST                'objs'
             3620  LOAD_CONST               0
             3622  BINARY_SUBSCR    
             3624  STORE_FAST               'idObject'

 L. 399      3626  LOAD_FAST                'modelXbrl'
             3628  LOAD_ATTR                error
             3630  LOAD_GLOBAL              ixMsgCode
             3632  LOAD_STR                 'uniqueIxId'
             3634  LOAD_FAST                'idObject'
             3636  LOAD_STR                 'validation'
             3638  LOAD_CONST               ('sect',)
             3640  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 400      3642  LOAD_GLOBAL              _
             3644  LOAD_STR                 'Inline XBRL id is not unique in the IXDS: %(id)s, for element(s) %(elements)s'
             3646  CALL_FUNCTION_1       1  '1 positional argument'

 L. 401      3648  LOAD_FAST                'objs'
             3650  LOAD_FAST                '_id'
             3652  LOAD_STR                 ','
             3654  LOAD_ATTR                join
             3656  LOAD_GLOBAL              sorted
             3658  LOAD_GLOBAL              set
             3660  LOAD_GENEXPR             '<code_object <genexpr>>'
             3662  LOAD_STR                 'ValidateXbrl.validate.<locals>.<genexpr>'
             3664  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3666  LOAD_FAST                'objs'
             3668  GET_ITER         
             3670  CALL_FUNCTION_1       1  '1 positional argument'
             3672  CALL_FUNCTION_1       1  '1 positional argument'
             3674  CALL_FUNCTION_1       1  '1 positional argument'
             3676  CALL_FUNCTION_1       1  '1 positional argument'
             3678  LOAD_CONST               ('modelObject', 'id', 'elements')
             3680  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             3682  POP_TOP          
             3684  JUMP_BACK          3596  'to 3596'
             3688  POP_BLOCK        
           3690_0  COME_FROM_LOOP     3586  '3586'

 L. 402      3690  BUILD_LIST_0          0 
             3692  LOAD_DEREF               'self'
             3694  STORE_ATTR               factsWithDeprecatedIxNamespace

 L. 403      3696  LOAD_GLOBAL              set
             3698  CALL_FUNCTION_0       0  '0 positional arguments'
             3700  STORE_FAST               'factFootnoteRefs'

 L. 404      3702  BUILD_LIST_0          0 
             3704  STORE_FAST               'undefinedFacts'

 L. 405      3706  SETUP_LOOP         3990  'to 3990'
             3710  LOAD_FAST                'modelXbrl'
             3712  LOAD_ATTR                factsInInstance
             3714  GET_ITER         
             3716  FOR_ITER           3988  'to 3988'
             3720  STORE_FAST               'f'

 L. 406      3722  SETUP_LOOP         3796  'to 3796'
             3724  LOAD_FAST                'f'
             3726  LOAD_ATTR                footnoteRefs
             3728  GET_ITER         
             3730  FOR_ITER           3794  'to 3794'
             3732  STORE_FAST               'footnoteID'

 L. 407      3734  LOAD_FAST                'footnoteID'
             3736  LOAD_DEREF               'self'
             3738  LOAD_ATTR                ixdsFootnotes
             3740  COMPARE_OP               not-in
             3742  POP_JUMP_IF_FALSE  3780  'to 3780'

 L. 408      3746  LOAD_FAST                'modelXbrl'
             3748  LOAD_ATTR                error
             3750  LOAD_GLOBAL              ixMsgCode
             3752  LOAD_STR                 'footnoteRef'
             3754  LOAD_FAST                'f'
             3756  LOAD_STR                 'footnote'
             3758  LOAD_STR                 'validation'
             3760  LOAD_CONST               ('name', 'sect')
             3762  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 409      3764  LOAD_GLOBAL              _
             3766  LOAD_STR                 "Inline XBRL fact's footnoteRef not found: %(id)s"
             3768  CALL_FUNCTION_1       1  '1 positional argument'

 L. 410      3770  LOAD_FAST                'f'
             3772  LOAD_FAST                'footnoteID'
             3774  LOAD_CONST               ('modelObject', 'id')
             3776  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             3778  POP_TOP          
           3780_0  COME_FROM          3742  '3742'

 L. 411      3780  LOAD_FAST                'factFootnoteRefs'
             3782  LOAD_ATTR                add
             3784  LOAD_FAST                'footnoteID'
             3786  CALL_FUNCTION_1       1  '1 positional argument'
             3788  POP_TOP          
             3790  JUMP_BACK          3730  'to 3730'
             3794  POP_BLOCK        
           3796_0  COME_FROM_LOOP     3722  '3722'

 L. 412      3796  LOAD_FAST                'f'
             3798  LOAD_ATTR                concept
             3800  LOAD_CONST               None
             3802  COMPARE_OP               is
             3804  POP_JUMP_IF_FALSE  3818  'to 3818'

 L. 413      3808  LOAD_FAST                'undefinedFacts'
             3810  LOAD_ATTR                append
             3812  LOAD_FAST                'f'
             3814  CALL_FUNCTION_1       1  '1 positional argument'
             3816  POP_TOP          
           3818_0  COME_FROM          3804  '3804'

 L. 414      3818  LOAD_FAST                'f'
             3820  LOAD_ATTR                localName
             3822  LOAD_CONST               frozenset({'nonNumeric', 'nonFraction', 'fraction'})
             3824  COMPARE_OP               in
             3826  POP_JUMP_IF_FALSE  3882  'to 3882'

 L. 415      3830  LOAD_FAST                'f'
             3832  LOAD_ATTR                context
             3834  LOAD_CONST               None
             3836  COMPARE_OP               is
             3838  POP_JUMP_IF_FALSE  3882  'to 3882'

 L. 416      3842  LOAD_DEREF               'self'
             3844  LOAD_ATTR                modelXbrl
             3846  LOAD_ATTR                error
             3848  LOAD_GLOBAL              ixMsgCode
             3850  LOAD_STR                 'contextReference'
             3852  LOAD_FAST                'f'
             3854  LOAD_STR                 'validation'
             3856  LOAD_CONST               ('sect',)
             3858  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 417      3860  LOAD_GLOBAL              _
             3862  LOAD_STR                 'Fact %(fact)s is missing a context for contextRef %(context)s'
             3864  CALL_FUNCTION_1       1  '1 positional argument'

 L. 418      3866  LOAD_FAST                'f'
             3868  LOAD_FAST                'f'
             3870  LOAD_ATTR                qname
             3872  LOAD_FAST                'f'
             3874  LOAD_ATTR                contextID
             3876  LOAD_CONST               ('modelObject', 'fact', 'context')
             3878  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             3880  POP_TOP          
           3882_0  COME_FROM          3838  '3838'
           3882_1  COME_FROM          3826  '3826'

 L. 419      3882  LOAD_FAST                'f'
             3884  LOAD_ATTR                localName
             3886  LOAD_CONST               frozenset({'nonFraction', 'fraction'})
             3888  COMPARE_OP               in
             3890  POP_JUMP_IF_FALSE  3946  'to 3946'

 L. 420      3894  LOAD_FAST                'f'
             3896  LOAD_ATTR                unit
             3898  LOAD_CONST               None
             3900  COMPARE_OP               is
             3902  POP_JUMP_IF_FALSE  3946  'to 3946'

 L. 421      3906  LOAD_DEREF               'self'
             3908  LOAD_ATTR                modelXbrl
             3910  LOAD_ATTR                error
             3912  LOAD_GLOBAL              ixMsgCode
             3914  LOAD_STR                 'unitReference'
             3916  LOAD_FAST                'f'
             3918  LOAD_STR                 'validation'
             3920  LOAD_CONST               ('sect',)
             3922  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 422      3924  LOAD_GLOBAL              _
             3926  LOAD_STR                 'Fact %(fact)s is missing a unit for unitRef %(unit)s'
             3928  CALL_FUNCTION_1       1  '1 positional argument'

 L. 423      3930  LOAD_FAST                'f'
             3932  LOAD_FAST                'f'
             3934  LOAD_ATTR                qname
             3936  LOAD_FAST                'f'
             3938  LOAD_ATTR                unitID
             3940  LOAD_CONST               ('modelObject', 'fact', 'unit')
             3942  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             3944  POP_TOP          
           3946_0  COME_FROM          3902  '3902'
           3946_1  COME_FROM          3890  '3890'

 L. 424      3946  LOAD_FAST                'f'
             3948  LOAD_ATTR                format
             3950  STORE_FAST               'fmt'

 L. 425      3952  LOAD_FAST                'fmt'
             3954  POP_JUMP_IF_FALSE  3716  'to 3716'

 L. 426      3958  LOAD_FAST                'fmt'
             3960  LOAD_ATTR                namespaceURI
             3962  LOAD_GLOBAL              FunctionIxt
             3964  LOAD_ATTR                deprecatedNamespaceURI
             3966  COMPARE_OP               ==
             3968  POP_JUMP_IF_FALSE  3716  'to 3716'

 L. 427      3972  LOAD_DEREF               'self'
             3974  LOAD_ATTR                factsWithDeprecatedIxNamespace
             3976  LOAD_ATTR                append
             3978  LOAD_FAST                'f'
             3980  CALL_FUNCTION_1       1  '1 positional argument'
             3982  POP_TOP          
             3984  JUMP_BACK          3716  'to 3716'
             3988  POP_BLOCK        
           3990_0  COME_FROM_LOOP     3706  '3706'

 L. 428      3990  LOAD_FAST                'undefinedFacts'
             3992  POP_JUMP_IF_FALSE  4044  'to 4044'

 L. 429      3996  LOAD_DEREF               'self'
             3998  LOAD_ATTR                modelXbrl
             4000  LOAD_ATTR                error
             4002  LOAD_STR                 'xbrl:schemaImportMissing'

 L. 430      4004  LOAD_GLOBAL              _
             4006  LOAD_STR                 'Instance facts missing schema concept definition: %(elements)s'
             4008  CALL_FUNCTION_1       1  '1 positional argument'

 L. 431      4010  LOAD_FAST                'undefinedFacts'
             4012  LOAD_STR                 ', '
             4014  LOAD_ATTR                join
             4016  LOAD_GLOBAL              sorted
             4018  LOAD_GLOBAL              set
             4020  LOAD_GENEXPR             '<code_object <genexpr>>'
             4022  LOAD_STR                 'ValidateXbrl.validate.<locals>.<genexpr>'
             4024  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             4026  LOAD_FAST                'undefinedFacts'
             4028  GET_ITER         
             4030  CALL_FUNCTION_1       1  '1 positional argument'
             4032  CALL_FUNCTION_1       1  '1 positional argument'
             4034  CALL_FUNCTION_1       1  '1 positional argument'
             4036  CALL_FUNCTION_1       1  '1 positional argument'
             4038  LOAD_CONST               ('modelObject', 'elements')
             4040  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             4042  POP_TOP          
           4044_0  COME_FROM          3992  '3992'

 L. 432      4044  DELETE_FAST              'undefinedFacts'

 L. 433      4046  SETUP_LOOP         4192  'to 4192'
             4048  LOAD_DEREF               'self'
             4050  LOAD_ATTR                ixdsFootnotes
             4052  LOAD_ATTR                items
             4054  CALL_FUNCTION_0       0  '0 positional arguments'
             4056  GET_ITER         
             4058  FOR_ITER           4190  'to 4190'
             4060  UNPACK_SEQUENCE_2     2 
             4062  STORE_FAST               '_id'
             4064  STORE_FAST               'objs'

 L. 434      4066  LOAD_GLOBAL              len
             4068  LOAD_FAST                'objs'
             4070  CALL_FUNCTION_1       1  '1 positional argument'
             4072  LOAD_CONST               1
             4074  COMPARE_OP               >
             4076  POP_JUMP_IF_FALSE  4116  'to 4116'

 L. 435      4080  LOAD_FAST                'modelXbrl'
             4082  LOAD_ATTR                error
             4084  LOAD_GLOBAL              ixMsgCode
             4086  LOAD_STR                 'uniqueFootnoteId'
             4088  LOAD_FAST                '_ixNS'
             4090  LOAD_STR                 'footnote'
             4092  LOAD_STR                 'validation'
             4094  LOAD_CONST               ('ns', 'name', 'sect')
             4096  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 436      4098  LOAD_GLOBAL              _
             4100  LOAD_STR                 'Inline XBRL footnote id is not unique in the IXDS: %(id)s'
             4102  CALL_FUNCTION_1       1  '1 positional argument'

 L. 437      4104  LOAD_FAST                'objs'
             4106  LOAD_FAST                '_id'
             4108  LOAD_CONST               ('modelObject', 'id')
             4110  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             4112  POP_TOP          
             4114  JUMP_FORWARD       4186  'to 4186'
             4116  ELSE                     '4186'

 L. 439      4116  LOAD_DEREF               'self'
             4118  LOAD_ATTR                validateGFM
             4120  POP_JUMP_IF_FALSE  4058  'to 4058'

 L. 440      4124  LOAD_FAST                'objs'
             4126  LOAD_CONST               0
             4128  BINARY_SUBSCR    
             4130  STORE_FAST               'elt'

 L. 441      4132  LOAD_FAST                'elt'
             4134  LOAD_ATTR                footnoteID
             4136  STORE_FAST               'id'

 L. 442      4138  LOAD_FAST                'id'
             4140  POP_JUMP_IF_FALSE  4058  'to 4058'
             4144  LOAD_FAST                'id'
             4146  LOAD_FAST                'factFootnoteRefs'
             4148  COMPARE_OP               not-in
             4150  POP_JUMP_IF_FALSE  4058  'to 4058'
             4154  LOAD_FAST                'elt'
             4156  LOAD_ATTR                textValue
             4158  POP_JUMP_IF_FALSE  4058  'to 4058'

 L. 443      4162  LOAD_DEREF               'self'
             4164  LOAD_ATTR                modelXbrl
             4166  LOAD_ATTR                error
             4168  LOAD_CONST               ('EFM.N/A', 'GFM:1.10.15')

 L. 444      4170  LOAD_GLOBAL              _
             4172  LOAD_STR                 'Inline XBRL non-empty footnote %(footnoteID)s is not referenced by any fact'
             4174  CALL_FUNCTION_1       1  '1 positional argument'

 L. 445      4176  LOAD_FAST                'elt'
             4178  LOAD_FAST                'id'
             4180  LOAD_CONST               ('modelObject', 'footnoteID')
             4182  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             4184  POP_TOP          
           4186_0  COME_FROM          4114  '4114'
             4186  JUMP_BACK          4058  'to 4058'
             4190  POP_BLOCK        
           4192_0  COME_FROM_LOOP     4046  '4046'

 L. 446      4192  LOAD_DEREF               'self'
             4194  LOAD_ATTR                ixdsHeaderCount
             4196  POP_JUMP_IF_TRUE   4232  'to 4232'

 L. 447      4200  LOAD_FAST                'modelXbrl'
             4202  LOAD_ATTR                error
             4204  LOAD_GLOBAL              ixMsgCode
             4206  LOAD_STR                 'headerMissing'
             4208  LOAD_FAST                '_ixNS'
             4210  LOAD_STR                 'header'
             4212  LOAD_STR                 'validation'
             4214  LOAD_CONST               ('ns', 'name', 'sect')
             4216  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 448      4218  LOAD_GLOBAL              _
             4220  LOAD_STR                 'Inline XBRL document set must have at least one ix:header element'
             4222  CALL_FUNCTION_1       1  '1 positional argument'

 L. 449      4224  LOAD_FAST                'modelXbrl'
             4226  LOAD_CONST               ('modelObject',)
             4228  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4230  POP_TOP          
           4232_0  COME_FROM          4196  '4196'

 L. 450      4232  LOAD_DEREF               'self'
             4234  LOAD_ATTR                factsWithDeprecatedIxNamespace
             4236  POP_JUMP_IF_FALSE  4276  'to 4276'

 L. 451      4240  LOAD_DEREF               'self'
             4242  LOAD_ATTR                modelXbrl
             4244  LOAD_ATTR                info
             4246  LOAD_STR                 'arelle:info'

 L. 452      4248  LOAD_GLOBAL              _
             4250  LOAD_STR                 '%(count)s facts have deprecated transformation namespace %(namespace)s'
             4252  CALL_FUNCTION_1       1  '1 positional argument'

 L. 453      4254  LOAD_DEREF               'self'
             4256  LOAD_ATTR                factsWithDeprecatedIxNamespace

 L. 454      4258  LOAD_GLOBAL              len
             4260  LOAD_DEREF               'self'
             4262  LOAD_ATTR                factsWithDeprecatedIxNamespace
             4264  CALL_FUNCTION_1       1  '1 positional argument'

 L. 455      4266  LOAD_GLOBAL              FunctionIxt
             4268  LOAD_ATTR                deprecatedNamespaceURI
             4270  LOAD_CONST               ('modelObject', 'count', 'namespace')
             4272  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             4274  POP_TOP          
           4276_0  COME_FROM          4236  '4236'

 L. 457      4276  LOAD_DEREF               'self'
             4278  DELETE_ATTR              factsWithDeprecatedIxNamespace

 L. 458      4280  SETUP_LOOP         4532  'to 4532'
             4282  LOAD_DEREF               'self'
             4284  LOAD_ATTR                ixdsReferences
             4286  LOAD_ATTR                items
             4288  CALL_FUNCTION_0       0  '0 positional arguments'
             4290  GET_ITER         
             4292  FOR_ITER           4530  'to 4530'
             4294  UNPACK_SEQUENCE_2     2 
             4296  STORE_FAST               'target'
             4298  STORE_FAST               'ixReferences'

 L. 459      4300  LOAD_CONST               None
             4302  STORE_FAST               'targetDefaultNamespace'

 L. 460      4304  BUILD_MAP_0           0 
             4306  STORE_FAST               'schemaRefUris'

 L. 461      4308  SETUP_LOOP         4526  'to 4526'
             4310  LOAD_GLOBAL              enumerate
             4312  LOAD_FAST                'ixReferences'
             4314  CALL_FUNCTION_1       1  '1 positional argument'
             4316  GET_ITER         
             4318  FOR_ITER           4524  'to 4524'
             4320  UNPACK_SEQUENCE_2     2 
             4322  STORE_FAST               'i'
             4324  STORE_FAST               'ixReference'

 L. 462      4326  LOAD_GLOBAL              XmlUtil
             4328  LOAD_ATTR                xmlns
             4330  LOAD_FAST                'ixReference'
             4332  LOAD_CONST               None
             4334  CALL_FUNCTION_2       2  '2 positional arguments'
             4336  STORE_FAST               'defaultNamepace'

 L. 463      4338  LOAD_FAST                'i'
             4340  LOAD_CONST               0
             4342  COMPARE_OP               ==
             4344  POP_JUMP_IF_FALSE  4354  'to 4354'

 L. 464      4348  LOAD_FAST                'defaultNamepace'
             4350  STORE_FAST               'targetDefaultNamespace'
             4352  JUMP_FORWARD       4396  'to 4396'
             4354  ELSE                     '4396'

 L. 465      4354  LOAD_FAST                'targetDefaultNamespace'
             4356  LOAD_FAST                'defaultNamepace'
             4358  COMPARE_OP               !=
             4360  POP_JUMP_IF_FALSE  4396  'to 4396'

 L. 466      4364  LOAD_FAST                'modelXbrl'
             4366  LOAD_ATTR                error
             4368  LOAD_GLOBAL              ixMsgCode
             4370  LOAD_STR                 'referenceInconsistentDefaultNamespaces'
             4372  LOAD_FAST                '_ixNS'
             4374  LOAD_STR                 'validation'
             4376  LOAD_CONST               ('ns', 'sect')
             4378  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 467      4380  LOAD_GLOBAL              _
             4382  LOAD_STR                 'Inline XBRL document set must have consistent default namespaces for target %(target)s'
             4384  CALL_FUNCTION_1       1  '1 positional argument'

 L. 468      4386  LOAD_FAST                'ixReferences'
             4388  LOAD_FAST                'target'
             4390  LOAD_CONST               ('modelObject', 'target')
             4392  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             4394  POP_TOP          
           4396_0  COME_FROM          4360  '4360'
           4396_1  COME_FROM          4352  '4352'

 L. 469      4396  SETUP_LOOP         4520  'to 4520'
             4398  LOAD_GLOBAL              XmlUtil
             4400  LOAD_ATTR                children
             4402  LOAD_FAST                'ixReference'
             4404  LOAD_GLOBAL              XbrlConst
             4406  LOAD_ATTR                link
             4408  LOAD_STR                 'schemaRef'
             4410  CALL_FUNCTION_3       3  '3 positional arguments'
             4412  GET_ITER         
             4414  FOR_ITER           4518  'to 4518'
             4416  STORE_FAST               'schemaRef'

 L. 470      4418  LOAD_FAST                'schemaRef'
             4420  LOAD_ATTR                get
             4422  LOAD_STR                 '{http://www.w3.org/1999/xlink}href'
             4424  CALL_FUNCTION_1       1  '1 positional argument'
             4426  STORE_FAST               'href'

 L. 471      4428  LOAD_GLOBAL              XmlUtil
             4430  LOAD_ATTR                xmlnsprefix
             4432  LOAD_FAST                'schemaRef'
             4434  LOAD_FAST                'href'
             4436  CALL_FUNCTION_2       2  '2 positional arguments'
             4438  STORE_FAST               'prefix'

 L. 472      4440  LOAD_FAST                'href'
             4442  LOAD_FAST                'schemaRefUris'
             4444  COMPARE_OP               not-in
             4446  POP_JUMP_IF_FALSE  4460  'to 4460'

 L. 473      4450  LOAD_FAST                'prefix'
             4452  LOAD_FAST                'schemaRefUris'
             4454  LOAD_FAST                'href'
             4456  STORE_SUBSCR     
             4458  JUMP_FORWARD       4514  'to 4514'
             4460  ELSE                     '4514'

 L. 474      4460  LOAD_FAST                'schemaRefUris'
             4462  LOAD_FAST                'href'
             4464  BINARY_SUBSCR    
             4466  LOAD_FAST                'prefix'
             4468  COMPARE_OP               !=
             4470  POP_JUMP_IF_FALSE  4414  'to 4414'

 L. 475      4474  LOAD_FAST                'modelXbrl'
             4476  LOAD_ATTR                error
             4478  LOAD_GLOBAL              ixMsgCode
             4480  LOAD_STR                 'referenceNamespacePrefixInconsistency'
             4482  LOAD_FAST                '_ixNS'
             4484  LOAD_STR                 'validation'
             4486  LOAD_CONST               ('ns', 'sect')
             4488  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 476      4490  LOAD_GLOBAL              _
             4492  LOAD_STR                 'Inline XBRL document set must have consistent prefixes for target %(target)s: %(prefix1)s, %(prefix2)s'
             4494  CALL_FUNCTION_1       1  '1 positional argument'

 L. 477      4496  LOAD_FAST                'ixReferences'
             4498  LOAD_FAST                'target'
             4500  LOAD_FAST                'schemaRefUris'
             4502  LOAD_FAST                'href'
             4504  BINARY_SUBSCR    
             4506  LOAD_FAST                'prefix'
             4508  LOAD_CONST               ('modelObject', 'target', 'prefix1', 'prefix2')
             4510  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             4512  POP_TOP          
           4514_0  COME_FROM          4458  '4458'
             4514  JUMP_BACK          4414  'to 4414'
             4518  POP_BLOCK        
           4520_0  COME_FROM_LOOP     4396  '4396'
             4520  JUMP_BACK          4318  'to 4318'
             4524  POP_BLOCK        
           4526_0  COME_FROM_LOOP     4308  '4308'
             4526  JUMP_BACK          4292  'to 4292'
             4530  POP_BLOCK        
           4532_0  COME_FROM_LOOP     4280  '4280'

 L. 478      4532  SETUP_LOOP         4970  'to 4970'
             4536  LOAD_DEREF               'self'
             4538  LOAD_ATTR                ixdsRelationships
             4540  GET_ITER         
             4542  FOR_ITER           4968  'to 4968'
             4546  STORE_FAST               'ixRel'

 L. 479      4548  SETUP_LOOP         4662  'to 4662'
             4550  LOAD_FAST                'ixRel'
             4552  LOAD_ATTR                get
             4554  LOAD_STR                 'fromRefs'
             4556  LOAD_STR                 ''
             4558  CALL_FUNCTION_2       2  '2 positional arguments'
             4560  LOAD_ATTR                split
             4562  CALL_FUNCTION_0       0  '0 positional arguments'
             4564  GET_ITER         
             4566  FOR_ITER           4660  'to 4660'
             4568  STORE_FAST               'fromRef'

 L. 480      4570  LOAD_FAST                'ixdsIdObjects'
             4572  LOAD_ATTR                get
             4574  LOAD_FAST                'fromRef'
             4576  CALL_FUNCTION_1       1  '1 positional argument'
             4578  STORE_FAST               'refs'

 L. 481      4580  LOAD_FAST                'refs'
             4582  LOAD_CONST               None
             4584  COMPARE_OP               is
             4586  POP_JUMP_IF_TRUE   4622  'to 4622'
             4590  LOAD_FAST                'refs'
             4592  LOAD_CONST               0
             4594  BINARY_SUBSCR    
             4596  LOAD_ATTR                namespaceURI
             4598  LOAD_GLOBAL              ixbrlAll
             4600  COMPARE_OP               not-in
             4602  POP_JUMP_IF_TRUE   4622  'to 4622'
             4606  LOAD_FAST                'refs'
             4608  LOAD_CONST               0
             4610  BINARY_SUBSCR    
             4612  LOAD_ATTR                localName
             4614  LOAD_CONST               ('fraction', 'nonFraction', 'nonNumeric', 'tuple')
             4616  COMPARE_OP               not-in
           4618_0  COME_FROM          4602  '4602'
           4618_1  COME_FROM          4586  '4586'
             4618  POP_JUMP_IF_FALSE  4566  'to 4566'

 L. 482      4622  LOAD_FAST                'modelXbrl'
             4624  LOAD_ATTR                error
             4626  LOAD_GLOBAL              ixMsgCode
             4628  LOAD_STR                 'relationshipFromRef'
             4630  LOAD_FAST                '_ixNS'
             4632  LOAD_STR                 'relationship'
             4634  LOAD_STR                 'validation'
             4636  LOAD_CONST               ('ns', 'name', 'sect')
             4638  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 483      4640  LOAD_GLOBAL              _
             4642  LOAD_STR                 'Inline XBRL fromRef %(ref)s is not a fraction, ix:nonFraction, ix:nonNumeric or ix:tuple.'
             4644  CALL_FUNCTION_1       1  '1 positional argument'

 L. 484      4646  LOAD_FAST                'ixRel'
             4648  LOAD_FAST                'fromRef'
             4650  LOAD_CONST               ('modelObject', 'ref')
             4652  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             4654  POP_TOP          
             4656  JUMP_BACK          4566  'to 4566'
             4660  POP_BLOCK        
           4662_0  COME_FROM_LOOP     4548  '4548'

 L. 485      4662  LOAD_CONST               None
             4664  STORE_FAST               'hasFootnoteToRef'

 L. 486      4666  LOAD_CONST               False
             4668  STORE_FAST               'hasToRefMixture'

 L. 487      4670  SETUP_LOOP         4836  'to 4836'
             4672  LOAD_FAST                'ixRel'
             4674  LOAD_ATTR                get
             4676  LOAD_STR                 'toRefs'
             4678  LOAD_STR                 ''
             4680  CALL_FUNCTION_2       2  '2 positional arguments'
             4682  LOAD_ATTR                split
             4684  CALL_FUNCTION_0       0  '0 positional arguments'
             4686  GET_ITER         
             4688  FOR_ITER           4834  'to 4834'
             4690  STORE_FAST               'toRef'

 L. 488      4692  LOAD_FAST                'ixdsIdObjects'
             4694  LOAD_ATTR                get
             4696  LOAD_FAST                'toRef'
             4698  CALL_FUNCTION_1       1  '1 positional argument'
             4700  STORE_FAST               'refs'

 L. 489      4702  LOAD_FAST                'refs'
             4704  LOAD_CONST               None
             4706  COMPARE_OP               is
             4708  POP_JUMP_IF_TRUE   4744  'to 4744'
             4712  LOAD_FAST                'refs'
             4714  LOAD_CONST               0
             4716  BINARY_SUBSCR    
             4718  LOAD_ATTR                namespaceURI
             4720  LOAD_GLOBAL              ixbrlAll
             4722  COMPARE_OP               not-in
             4724  POP_JUMP_IF_TRUE   4744  'to 4744'
             4728  LOAD_FAST                'refs'
             4730  LOAD_CONST               0
             4732  BINARY_SUBSCR    
             4734  LOAD_ATTR                localName
             4736  LOAD_CONST               ('footnote', 'fraction', 'nonFraction', 'nonNumeric', 'tuple')
             4738  COMPARE_OP               not-in
           4740_0  COME_FROM          4724  '4724'
           4740_1  COME_FROM          4708  '4708'
             4740  POP_JUMP_IF_FALSE  4780  'to 4780'

 L. 490      4744  LOAD_FAST                'modelXbrl'
             4746  LOAD_ATTR                error
             4748  LOAD_GLOBAL              ixMsgCode
             4750  LOAD_STR                 'relationshipToRef'
             4752  LOAD_FAST                '_ixNS'
             4754  LOAD_STR                 'relationship'
             4756  LOAD_STR                 'validation'
             4758  LOAD_CONST               ('ns', 'name', 'sect')
             4760  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 491      4762  LOAD_GLOBAL              _
             4764  LOAD_STR                 'Inline XBRL toRef %(ref)s is not a footnote, fraction, ix:nonFraction, ix:nonNumeric or ix:tuple.'
             4766  CALL_FUNCTION_1       1  '1 positional argument'

 L. 492      4768  LOAD_FAST                'ixRel'
             4770  LOAD_FAST                'toRef'
             4772  LOAD_CONST               ('modelObject', 'ref')
             4774  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             4776  POP_TOP          
             4778  JUMP_FORWARD       4830  'to 4830'
             4780  ELSE                     '4830'

 L. 493      4780  LOAD_FAST                'hasFootnoteToRef'
             4782  LOAD_CONST               None
             4784  COMPARE_OP               is
             4786  POP_JUMP_IF_FALSE  4806  'to 4806'

 L. 494      4790  LOAD_FAST                'refs'
             4792  LOAD_CONST               0
             4794  BINARY_SUBSCR    
             4796  LOAD_ATTR                localName
             4798  LOAD_STR                 'footnote'
             4800  COMPARE_OP               ==
             4802  STORE_FAST               'hasFootnoteToRef'
             4804  JUMP_FORWARD       4830  'to 4830'
             4806  ELSE                     '4830'

 L. 495      4806  LOAD_FAST                'hasFootnoteToRef'
             4808  LOAD_FAST                'refs'
             4810  LOAD_CONST               0
             4812  BINARY_SUBSCR    
             4814  LOAD_ATTR                localName
             4816  LOAD_STR                 'footnote'
             4818  COMPARE_OP               ==
             4820  COMPARE_OP               !=
             4822  POP_JUMP_IF_FALSE  4688  'to 4688'

 L. 496      4826  LOAD_CONST               True
             4828  STORE_FAST               'hasToRefMixture'
           4830_0  COME_FROM          4804  '4804'
           4830_1  COME_FROM          4778  '4778'
             4830  JUMP_BACK          4688  'to 4688'
             4834  POP_BLOCK        
           4836_0  COME_FROM_LOOP     4670  '4670'

 L. 497      4836  LOAD_FAST                'hasToRefMixture'
             4838  POP_JUMP_IF_FALSE  4874  'to 4874'

 L. 498      4842  LOAD_FAST                'modelXbrl'
             4844  LOAD_ATTR                error
             4846  LOAD_GLOBAL              ixMsgCode
             4848  LOAD_STR                 'relationshipToRefMix'
             4850  LOAD_FAST                '_ixNS'
             4852  LOAD_STR                 'relationship'
             4854  LOAD_STR                 'validation'
             4856  LOAD_CONST               ('ns', 'name', 'sect')
             4858  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 499      4860  LOAD_GLOBAL              _
             4862  LOAD_STR                 'Inline XBRL fromRef is not only either footnotes, or ix:fraction, ix:nonFraction, ix:nonNumeric or ix:tuple.'
             4864  CALL_FUNCTION_1       1  '1 positional argument'

 L. 500      4866  LOAD_FAST                'ixRel'
             4868  LOAD_CONST               ('modelObject',)
             4870  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4872  POP_TOP          
           4874_0  COME_FROM          4838  '4838'

 L. 501      4874  LOAD_FAST                'ixRel'
             4876  LOAD_ATTR                get
             4878  LOAD_STR                 'linkRole'
             4880  CALL_FUNCTION_1       1  '1 positional argument'
             4882  LOAD_CONST               None
             4884  COMPARE_OP               is-not
             4886  POP_JUMP_IF_FALSE  4920  'to 4920'

 L. 502      4890  LOAD_GLOBAL              ValidateXbrlDTS
             4892  LOAD_ATTR                checkLinkRole
             4894  LOAD_DEREF               'self'
             4896  LOAD_FAST                'ixRel'
             4898  LOAD_GLOBAL              XbrlConst
             4900  LOAD_ATTR                qnLinkFootnoteLink
             4902  LOAD_FAST                'ixRel'
             4904  LOAD_ATTR                get
             4906  LOAD_STR                 'linkRole'
             4908  CALL_FUNCTION_1       1  '1 positional argument'
             4910  LOAD_STR                 'extended'
             4912  LOAD_DEREF               'self'
             4914  LOAD_ATTR                ixdsRoleRefURIs
             4916  CALL_FUNCTION_6       6  '6 positional arguments'
             4918  POP_TOP          
           4920_0  COME_FROM          4886  '4886'

 L. 503      4920  LOAD_FAST                'ixRel'
             4922  LOAD_ATTR                get
             4924  LOAD_STR                 'arcrole'
             4926  CALL_FUNCTION_1       1  '1 positional argument'
             4928  LOAD_CONST               None
             4930  COMPARE_OP               is-not
             4932  POP_JUMP_IF_FALSE  4542  'to 4542'

 L. 504      4936  LOAD_GLOBAL              ValidateXbrlDTS
             4938  LOAD_ATTR                checkArcrole
             4940  LOAD_DEREF               'self'
             4942  LOAD_FAST                'ixRel'
             4944  LOAD_GLOBAL              XbrlConst
             4946  LOAD_ATTR                qnLinkFootnoteArc
             4948  LOAD_FAST                'ixRel'
             4950  LOAD_ATTR                get
             4952  LOAD_STR                 'arcrole'
             4954  CALL_FUNCTION_1       1  '1 positional argument'
             4956  LOAD_DEREF               'self'
             4958  LOAD_ATTR                ixdsArcroleRefURIs
             4960  CALL_FUNCTION_5       5  '5 positional arguments'
             4962  POP_TOP          
             4964  JUMP_BACK          4542  'to 4542'
             4968  POP_BLOCK        
           4970_0  COME_FROM_LOOP     4532  '4532'

 L. 507      4970  DELETE_FAST              'ixdsIdObjects'

 L. 509      4972  LOAD_FAST                'modelXbrl'
             4974  LOAD_ATTR                profileStat
             4976  LOAD_GLOBAL              _
             4978  LOAD_STR                 'validateInline'
             4980  CALL_FUNCTION_1       1  '1 positional argument'
             4982  CALL_FUNCTION_1       1  '1 positional argument'
             4984  POP_TOP          
           4986_0  COME_FROM          3462  '3462'

 L. 511      4986  LOAD_FAST                'modelXbrl'
             4988  LOAD_ATTR                hasFormulae
             4990  POP_JUMP_IF_TRUE   5002  'to 5002'
             4994  LOAD_FAST                'modelXbrl'
             4996  LOAD_ATTR                modelRenderingTables
           4998_0  COME_FROM          4990  '4990'
             4998  POP_JUMP_IF_FALSE  5074  'to 5074'

 L. 512      5002  LOAD_GLOBAL              ValidateFormula
             5004  LOAD_ATTR                validate
             5006  LOAD_DEREF               'self'

 L. 513      5008  LOAD_FAST                'modelXbrl'
             5010  LOAD_ATTR                hasFormulae
             5012  POP_JUMP_IF_FALSE  5032  'to 5032'
             5016  LOAD_FAST                'modelXbrl'
             5018  LOAD_ATTR                modelRenderingTables
             5020  POP_JUMP_IF_FALSE  5032  'to 5032'
             5024  LOAD_GLOBAL              _
             5026  LOAD_STR                 'compiling formulae and rendering tables'
             5028  CALL_FUNCTION_1       1  '1 positional argument'
             5030  JUMP_FORWARD       5054  'to 5054'
           5032_0  COME_FROM          5012  '5012'

 L. 514      5032  LOAD_FAST                'modelXbrl'
             5034  LOAD_ATTR                hasFormulae
             5036  POP_JUMP_IF_FALSE  5048  'to 5048'
             5040  LOAD_GLOBAL              _
             5042  LOAD_STR                 'compiling formulae'
             5044  CALL_FUNCTION_1       1  '1 positional argument'
             5046  JUMP_FORWARD       5054  'to 5054'
             5048  ELSE                     '5054'

 L. 515      5048  LOAD_GLOBAL              _
             5050  LOAD_STR                 'compiling rendering tables'
             5052  CALL_FUNCTION_1       1  '1 positional argument'
           5054_0  COME_FROM          5046  '5046'
           5054_1  COME_FROM          5030  '5030'

 L. 517      5054  LOAD_FAST                'modelXbrl'
             5056  LOAD_ATTR                modelRenderingTables
             5058  JUMP_IF_FALSE_OR_POP  5068  'to 5068'
             5062  LOAD_FAST                'modelXbrl'
             5064  LOAD_ATTR                hasFormulae
             5066  UNARY_NOT        
           5068_0  COME_FROM          5058  '5058'
             5068  LOAD_CONST               ('statusMsg', 'compileOnly')
             5070  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5072  POP_TOP          
           5074_0  COME_FROM          4998  '4998'

 L. 519      5074  SETUP_LOOP         5102  'to 5102'
             5076  LOAD_GLOBAL              pluginClassMethods
             5078  LOAD_STR                 'Validate.Finally'
             5080  CALL_FUNCTION_1       1  '1 positional argument'
             5082  GET_ITER         
             5084  FOR_ITER           5100  'to 5100'
             5086  STORE_FAST               'pluginXbrlMethod'

 L. 520      5088  LOAD_FAST                'pluginXbrlMethod'
             5090  LOAD_DEREF               'self'
             5092  CALL_FUNCTION_1       1  '1 positional argument'
             5094  POP_TOP          
             5096  JUMP_BACK          5084  'to 5084'
             5100  POP_BLOCK        
           5102_0  COME_FROM_LOOP     5074  '5074'

 L. 522      5102  LOAD_FAST                'modelXbrl'
             5104  LOAD_ATTR                modelManager
             5106  LOAD_ATTR                showStatus
             5108  LOAD_GLOBAL              _
             5110  LOAD_STR                 'ready'
             5112  CALL_FUNCTION_1       1  '1 positional argument'
             5114  LOAD_CONST               2000
             5116  CALL_FUNCTION_2       2  '2 positional arguments'
             5118  POP_TOP          

Parse error at or near `JUMP_BACK' instruction at offset 1400

    def checkLinks(self, modelLinks):
        for modelLink in modelLinks:
            fromToArcs = {}
            locLabels = {}
            resourceLabels = {}
            resourceArcTos = []
            for arcElt in modelLink.iterchildren():
                if isinstance(arcElt, ModelObject):
                    xlinkType = arcElt.get'{http://www.w3.org/1999/xlink}type'
                    if xlinkType == 'locator':
                        if arcElt.get'{http://www.w3.org/1999/xlink}href' is None:
                            self.modelXbrl.error('xlink:locatorHref', (_'Xlink locator %(xlinkLabel)s missing href in extended link %(linkrole)s'),
                              modelObject=arcElt,
                              linkrole=(modelLink.role),
                              xlinkLabel=(arcElt.get'{http://www.w3.org/1999/xlink}label'))
                        locLabels[arcElt.get'{http://www.w3.org/1999/xlink}label'] = arcElt
                    else:
                        if xlinkType == 'resource':
                            resourceLabels[arcElt.get'{http://www.w3.org/1999/xlink}label'] = arcElt
                        else:
                            if xlinkType == 'arc':
                                fromLabel = arcElt.get'{http://www.w3.org/1999/xlink}from'
                                toLabel = arcElt.get'{http://www.w3.org/1999/xlink}to'
                                fromTo = (fromLabel, toLabel)
                                if fromTo in fromToArcs:
                                    self.modelXbrl.error('xlink:dupArcs', (_'Duplicate xlink arcs  in extended link %(linkrole)s from %(xlinkLabelFrom)s to %(xlinkLabelTo)s'),
                                      modelObject=arcElt,
                                      linkrole=(modelLink.role),
                                      xlinkLabelFrom=fromLabel,
                                      xlinkLabelTo=toLabel)
                                else:
                                    fromToArcs[fromTo] = arcElt
                                if arcElt.namespaceURI == XbrlConst.link:
                                    if arcElt.localName in arcNamesTo21Resource:
                                        resourceArcTos.append(toLabel, arcElt.get'use', arcElt)
                                elif self.isGenericArcarcElt:
                                    arcrole = arcElt.get'{http://www.w3.org/1999/xlink}arcrole'
                                    self.genericArcArcroles.addarcrole
                                    if arcrole in (XbrlConst.elementLabel, XbrlConst.elementReference):
                                        resourceArcTos.append(toLabel, arcrole, arcElt)
                    if xlinkType not in xlinkTypeValues:
                        self.modelXbrl.error('xlink:type', (_'Xlink type %(xlinkType)s invalid in extended link %(linkrole)s'),
                          modelObject=arcElt,
                          linkrole=(modelLink.role),
                          xlinkType=xlinkType)
                    xlinkActuate = arcElt.get'{http://www.w3.org/1999/xlink}actuate'
                    if xlinkActuate not in xlinkActuateValues:
                        self.modelXbrl.error('xlink:actuate', (_'Actuate %(xlinkActuate)s invalid in extended link %(linkrole)s'),
                          modelObject=arcElt,
                          linkrole=(modelLink.role),
                          xlinkActuate=xlinkActuate)
                    xlinkShow = arcElt.get'{http://www.w3.org/1999/xlink}show'
                    if xlinkShow not in xlinkShowValues:
                        self.modelXbrl.error('xlink:show', (_'Show %(xlinkShow)s invalid in extended link %(linkrole)s'),
                          modelObject=arcElt,
                          linkrole=(modelLink.role),
                          xlinkShow=xlinkShow)

            for fromTo, arcElt in fromToArcs.items():
                fromLabel, toLabel = fromTo
                for name, value, sect in (('from', fromLabel, '3.5.3.9.2'), ('to', toLabel, '3.5.3.9.3')):
                    if value not in locLabels and value not in resourceLabels:
                        self.modelXbrl.error(('xbrl.{0}:arcResource'.formatsect), (_"Arc in extended link %(linkrole)s from %(xlinkLabelFrom)s to %(xlinkLabelTo)s attribute '%(attribute)s' has no matching loc or resource label"),
                          modelObject=arcElt,
                          linkrole=(modelLink.role),
                          xlinkLabelFrom=fromLabel,
                          xlinkLabelTo=toLabel,
                          attribute=name,
                          messageCodes=('xbrl.3.5.3.9.2:arcResource', 'xbrl.3.5.3.9.3:arcResource'))

                if arcElt.localName == 'footnoteArc':
                    if arcElt.namespaceURI == XbrlConst.link:
                        if arcElt.get'{http://www.w3.org/1999/xlink}arcrole' == XbrlConst.factFootnote:
                            if fromLabel not in locLabels:
                                self.modelXbrl.error('xbrl.4.11.1.3.1:factFootnoteArcFrom', (_'Footnote arc in extended link %(linkrole)s from %(xlinkLabelFrom)s to %(xlinkLabelTo)s "from" is not a loc'),
                                  modelObject=arcElt,
                                  linkrole=(modelLink.role),
                                  xlinkLabelFrom=fromLabel,
                                  xlinkLabelTo=toLabel)
                    if not (toLabel in resourceLabels and resourceLabels[toLabel].qname == XbrlConst.qnLinkFootnote or toLabel in locLabels and locLabels[toLabel].dereference().qname == XbrlConst.qnLinkFootnote):
                        self.modelXbrl.error('xbrl.4.11.1.3.1:factFootnoteArcTo', (_'Footnote arc in extended link %(linkrole)s from %(xlinkLabelFrom)s to %(xlinkLabelTo)s "to" is not a footnote resource'),
                          modelObject=arcElt,
                          linkrole=(modelLink.role),
                          xlinkLabelFrom=fromLabel,
                          xlinkLabelTo=toLabel)

            for resourceArcTo in resourceArcTos:
                resourceArcToLabel, resourceArcUse, arcElt = resourceArcTo
                if resourceArcToLabel in locLabels:
                    toLabel = locLabels[resourceArcToLabel]
                    if resourceArcUse == 'prohibited':
                        self.remoteResourceLocElements.addtoLabel
                    else:
                        self.modelXbrl.error('xbrl.5.2.2.3:labelArcRemoteResource', (_'Unprohibited labelArc in extended link %(linkrole)s has illegal remote resource loc labeled %(xlinkLabel)s href %(xlinkHref)s'),
                          modelObject=arcElt,
                          linkrole=(modelLink.role),
                          xlinkLabel=resourceArcToLabel,
                          xlinkHref=(toLabel.get'{http://www.w3.org/1999/xlink}href'))
                else:
                    if resourceArcToLabel in resourceLabels:
                        toResource = resourceLabels[resourceArcToLabel]
                        if resourceArcUse == XbrlConst.elementLabel:
                            if not self.isGenericLabeltoResource:
                                self.modelXbrl.error('xbrlle.2.1.1:genericLabelTarget', (_'Generic label arc in extended link %(linkrole)s to %(xlinkLabel)s must target a generic label'),
                                  modelObject=arcElt,
                                  linkrole=(modelLink.role),
                                  xlinkLabel=resourceArcToLabel)
                        elif resourceArcUse == XbrlConst.elementReference:
                            if not self.isGenericReferencetoResource:
                                self.modelXbrl.error('xbrlre.2.1.1:genericReferenceTarget', (_'Generic reference arc in extended link %(linkrole)s to %(xlinkLabel)s must target a generic reference'),
                                  modelObject=arcElt,
                                  linkrole=(modelLink.role),
                                  xlinkLabel=resourceArcToLabel)

            resourceArcTos = None

    def checkFacts(self, facts, inTuple=None):
        for f in facts:
            concept = f.concept
            if concept is not None:
                if concept.isNumeric:
                    unit = f.unit
                    if f.unitID is None or unit is None:
                        self.modelXbrl.error('xbrl.4.6.2:numericUnit', (_'Fact %(fact)s context %(contextID)s is numeric and must have a unit'),
                          modelObject=f,
                          fact=(f.qname),
                          contextID=(f.contextID))
                    else:
                        if concept.isMonetary:
                            measures = unit.measures
                            if not measures or lenmeasures[0] != 1 or lenmeasures[1] != 0:
                                self.modelXbrl.error('xbrl.4.8.2:monetaryFactUnit-notSingleMeasure', (_'Fact %(fact)s context %(contextID)s must have a single unit measure which is monetary %(unitID)s'),
                                  modelObject=f,
                                  fact=(f.qname),
                                  contextID=(f.contextID),
                                  unitID=(f.unitID))
                            else:
                                if measures[0][0].namespaceURI != XbrlConst.iso4217 or not self.isoCurrencyPattern.matchmeasures[0][0].localName:
                                    self.modelXbrl.error('xbrl.4.8.2:monetaryFactUnit-notMonetaryMeasure', (_'Fact %(fact)s context %(contextID)s must have a monetary unit measure %(unitID)s'),
                                      modelObject=f,
                                      fact=(f.qname),
                                      contextID=(f.contextID),
                                      unitID=(f.unitID))
                        elif concept.isShares:
                            measures = unit.measures
                            if not measures or lenmeasures[0] != 1 or lenmeasures[1] != 0:
                                self.modelXbrl.error('xbrl.4.8.2:sharesFactUnit-notSingleMeasure', (_'Fact %(fact)s context %(contextID)s must have a single xbrli:shares unit %(unitID)s'),
                                  modelObject=f,
                                  fact=(f.qname),
                                  contextID=(f.contextID),
                                  unitID=(f.unitID))
                            else:
                                if measures[0][0] != XbrlConst.qnXbrliShares:
                                    self.modelXbrl.error('xbrl.4.8.2:sharesFactUnit-notSharesMeasure', (_'Fact %(fact)s context %(contextID)s must have a xbrli:shares unit %(unitID)s'),
                                      modelObject=f,
                                      fact=(f.qname),
                                      contextID=(f.contextID),
                                      unitID=(f.unitID))
                            precision = f.precision
                            hasPrecision = precision is not None
                            if hasPrecision:
                                if precision != 'INF':
                                    if not precision.isdigit():
                                        self.modelXbrl.error('xbrl.4.6.4:precision', (_'Fact %(fact)s context %(contextID)s precision %(precision)s is invalid'),
                                          modelObject=f,
                                          fact=(f.qname),
                                          contextID=(f.contextID),
                                          precision=precision)
                            decimals = f.decimals
                            hasDecimals = decimals is not None
                            if hasPrecision:
                                if not self.precisionPattern.matchprecision:
                                    self.modelXbrl.error('xbrl.4.6.4:precision', (_'Fact %(fact)s context %(contextID)s precision %(precision)s is invalid'),
                                      modelObject=f,
                                      fact=(f.qname),
                                      contextID=(f.contextID),
                                      precision=precision)
                            if hasPrecision:
                                if hasDecimals:
                                    self.modelXbrl.error('xbrl.4.6.3:bothPrecisionAndDecimals', (_'Fact %(fact)s context %(contextID)s can not have both precision and decimals'),
                                      modelObject=f,
                                      fact=(f.qname),
                                      contextID=(f.contextID))
                        elif hasDecimals:
                            if not self.decimalsPattern.matchdecimals:
                                self.modelXbrl.error('xbrl.4.6.5:decimals', (_'Fact %(fact)s context %(contextID)s decimals %(decimals)s is invalid'),
                                  modelObject=f,
                                  fact=(f.qname),
                                  contextID=(f.contextID),
                                  decimals=decimals)
                        else:
                            if concept.isItem:
                                context = f.context
                                if context is None:
                                    self.modelXbrl.error('xbrl.4.6.1:itemContextRef', (_'Item %(fact)s must have a context'),
                                      modelObject=f,
                                      fact=(f.qname))
                                else:
                                    periodType = concept.periodType
                                if periodType == 'instant' and not context.isInstantPeriod or periodType == 'duration' and not (context.isStartEndPeriod or context.isForeverPeriod):
                                    self.modelXbrl.error('xbrl.4.7.2:contextPeriodType', (_'Fact %(fact)s context %(contextID)s has period type %(periodType)s conflict with context'),
                                      modelObject=f,
                                      fact=(f.qname),
                                      contextID=(f.contextID),
                                      periodType=periodType)
                                if f.isNil:
                                    if hasPrecision or hasDecimals:
                                        self.modelXbrl.error('xbrl.4.6.3:nilPrecisionDecimals', (_'Fact %(fact)s context %(contextID)s can not be nil and have either precision or decimals'),
                                          modelObject=f,
                                          fact=(f.qname),
                                          contextID=(f.contextID))
                                else:
                                    if concept.isFraction:
                                        if hasPrecision or hasDecimals:
                                            self.modelXbrl.error('xbrl.4.6.3:fractionPrecisionDecimals', (_'Fact %(fact)s context %(contextID)s is a fraction concept and cannot have either precision or decimals'),
                                              modelObject=f,
                                              fact=(f.qname),
                                              contextID=(f.contextID))
                                            numerator, denominator = f.fractionValue
                                            if not (numerator == 'INF' or numerator.isnumeric()):
                                                self.modelXbrl.error('xbrl.5.1.1:fractionPrecisionDecimals', (_'Fact %(fact)s context %(contextID)s is a fraction with invalid numerator %(numerator)s'),
                                                  modelObject=f,
                                                  fact=(f.qname),
                                                  contextID=(f.contextID),
                                                  numerator=numerator)
                                            if not denominator.isnumeric() or _INTdenominator == 0:
                                                self.modelXbrl.error('xbrl.5.1.1:fractionPrecisionDecimals', _'Fact %(fact)s context %(contextID)s is a fraction with invalid denominator %(denominator)').format(modelObject=f,
                                                  fact=(f.qname),
                                                  contextID=(f.contextID),
                                                  denominator=denominator)
                                    else:
                                        if self.modelXbrl.modelDocument.type != ModelDocument.Type.INLINEXBRL:
                                            for child in f.iterchildren():
                                                if isinstance(child, ModelObject):
                                                    self.modelXbrl.error('xbrl.5.1.1:itemMixedContent', (_'Fact %(fact)s context %(contextID)s may not have child elements %(childElementName)s'),
                                                      modelObject=f,
                                                      fact=(f.qname),
                                                      contextID=(f.contextID),
                                                      childElementName=(child.prefixedName))
                                                    break

                                        if concept.isNumeric:
                                            if not hasPrecision:
                                                if not hasDecimals:
                                                    self.modelXbrl.error('xbrl.4.6.3:missingPrecisionDecimals', (_'Fact %(fact)s context %(contextID)s is a numeric concept and must have either precision or decimals'),
                                                      modelObject=f,
                                                      fact=(f.qname),
                                                      contextID=(f.contextID))
                                        else:
                                            if hasPrecision or hasDecimals:
                                                self.modelXbrl.error('xbrl.4.6.3:extraneousPrecisionDecimals', (_'Fact %(fact)s context %(contextID)s is a non-numeric concept and must not have precision or decimals'),
                                                  modelObject=f,
                                                  fact=(f.qname),
                                                  contextID=(f.contextID))
                                if self.validateEnum:
                                    if concept.isEnumeration:
                                        if getattrf'xValid'0 == 4:
                                            if not f.isNil:
                                                qnEnums = f.xValue
                                                if not isinstance(qnEnums, list):
                                                    qnEnums = (
                                                     qnEnums,)
                                                if not all(ValidateXbrlDimensions.enumerationMemberUsableselfconceptself.modelXbrl.qnameConcepts.getqnEnum for qnEnum in qnEnums):
                                                    self.modelXbrl.error((('enum2ie:InvalidEnumerationSetValue' if concept.instanceOfTypeXbrlConst.qnEnumerationSetItemTypes else 'enum2ie:InvalidEnumerationValue') if concept.instanceOfTypeXbrlConst.qnEnumeration2ItemTypes else 'InvalidListFactValue' if concept.instanceOfTypeXbrlConst.qnEnumerationListItemTypes else 'InvalidFactValue'),
                                                      (_'Fact %(fact)s context %(contextID)s enumeration %(value)s is not in the domain of %(concept)s'),
                                                      modelObject=f,
                                                      fact=(f.qname),
                                                      contextID=(f.contextID),
                                                      value=(f.xValue),
                                                      concept=(f.qname),
                                                      messageCodes=('enumie:InvalidFactValue',
                                                                    'enumie:InvalidListFactValue',
                                                                    'enum2ie:InvalidEnumerationValue',
                                                                    'enum2ie:InvalidEnumerationSetValue'))
                                                if concept.instanceOfTypeXbrlConst.qnEnumerationSetItemTypes:
                                                    if lenqnEnums > lensetqnEnums:
                                                        self.modelXbrl.error((('enum2ie:' if concept.instanceOfTypeXbrlConst.qnEnumeration2ItemTypes else 'enumie:') + 'RepeatedEnumerationSetValue'),
                                                          (_'Fact %(fact)s context %(contextID)s enumeration has non-unique values %(value)s'),
                                                          modelObject=f,
                                                          fact=(f.qname),
                                                          contextID=(f.contextID),
                                                          value=(f.xValue),
                                                          concept=(f.qname),
                                                          messageCodes=('enumie:RepeatedEnumerationSetValue',
                                                                        'enum2ie:RepeatedEnumerationSetValue'))
                                                if concept.instanceOfTypeXbrlConst.qnEnumerationSetItemTypes:
                                                    if any(qnEnum < qnEnums[i] for i, qnEnum in enumerateqnEnums[1:]):
                                                        self.modelXbrl.error('enum2ie:InvalidEnumerationSetOrder', (_'Fact %(fact)s context %(contextID)s enumeration is not in lexicographical order %(value)s'),
                                                          modelObject=f,
                                                          fact=(f.qname),
                                                          contextID=(f.contextID),
                                                          value=(f.xValue),
                                                          concept=(f.qname))
                            else:
                                if concept.isTuple:
                                    if f.contextID:
                                        self.modelXbrl.error('xbrl.4.6.1:tupleContextRef', (_'Tuple %(fact)s must not have a context'),
                                          modelObject=f,
                                          fact=(f.qname))
                                    if hasPrecision or hasDecimals:
                                        self.modelXbrl.error('xbrl.4.6.3:tuplePrecisionDecimals', (_'Fact %(fact)s is a tuple and cannot have either precision or decimals'),
                                          modelObject=f,
                                          fact=(f.qname))
                                    for attrQname, attrValue in XbrlUtil.attributes(self.modelXbrl, f):
                                        if attrQname.namespaceURI in (XbrlConst.xbrli, XbrlConst.link, XbrlConst.xlink, XbrlConst.xl):
                                            (
                                             self.modelXbrl.error('xbrl.4.9:tupleAttribute', (_'Fact %(fact)s is a tuple and must not have attribute in this namespace %(attribute)s'),
                                               modelObject=f,
                                               fact=(f.qname),
                                               attribute=attrQname),)

                                else:
                                    self.modelXbrl.error('xbrl.4.6:notItemOrTuple', (_'Fact %(fact)s must be an item or tuple'),
                                      modelObject=f,
                                      fact=(f.qname))
                else:
                    if isinstance(f, ModelInlineFact):
                        if not inTuple:
                            if f.order is not None:
                                self.modelXbrl.error(ixMsgCode('tupleOrder', f, sect='validation'), (_'Fact %(fact)s must not have an order (%(order)s) unless in a tuple'),
                                  modelObject=f,
                                  fact=(f.qname),
                                  order=(f.order))
                        if f.isTuple or f.tupleID:
                            if inTuple is None:
                                inTuple = dict()
                            inTuple[f.qname] = f
                            self.checkIxTupleContent(f, inTuple)
                    if f.modelTupleFacts:
                        self.checkFacts((f.modelTupleFacts), inTuple=inTuple)
                if isinstance(f, ModelInlineFact) and (f.isTuple or f.tupleID):
                    del inTuple[f.qname]

    def checkFactsDimensions(self, facts):
        for f in facts:
            if f.concept is not None and f.concept.isItem and f.context is not None:
                ValidateXbrlDimensions.checkFact(self, f)
            else:
                if f.modelTupleFacts:
                    self.checkFactsDimensionsf.modelTupleFacts

    def checkIxTupleContent(self, tf, parentTuples):
        if tf.isNil:
            if tf.modelTupleFacts:
                self.modelXbrl.error('ix:tupleNilContent', (_'Inline XBRL nil tuple has content'),
                  modelObject=([
                 tf] + tf.modelTupleFacts))
        else:
            if not tf.modelTupleFacts:
                self.modelXbrl.error('ix:tupleContent', (_'Inline XBRL non-nil tuple requires content: ix:fraction, ix:nonFraction, ix:nonNumeric or ix:tuple'),
                  modelObject=tf)
        tfTarget = tf.get'target'
        prevTupleFact = None
        for f in tf.modelTupleFacts:
            if f.qname in parentTuples:
                self.modelXbrl.error('ix:tupleRecursion', (_'Fact %(fact)s is recursively nested in tuple %(tuple)s'),
                  modelObject=(
                 f, parentTuples[f.qname]),
                  fact=(f.qname),
                  tuple=(tf.qname))
            else:
                if f.order is None:
                    self.modelXbrl.error('ix:tupleOrder', (_'Fact %(fact)s missing an order in tuple %(tuple)s'),
                      modelObject=f,
                      fact=(f.qname),
                      tuple=(tf.qname))
                if f.get'target' != tfTarget:
                    self.modelXbrl.error('ix:tupleItemTarget', (_'Fact %(fact)s has different target, %(factTarget)s, than tuple %(tuple)s, %(tupleTarget)s'),
                      modelObject=(
                     tf, f),
                      fact=(f.qname),
                      tuple=(tf.qname),
                      factTarget=(f.get'target'),
                      tupleTarget=tfTarget)
            if prevTupleFact is None:
                prevTupleFact = f
            else:
                if prevTupleFact.order == f.order and XmlUtil.collapseWhitespaceprevTupleFact.textValue == XmlUtil.collapseWhitespacef.textValue:
                    self.modelXbrl.error('ix:tupleContentDuplicate', (_'Inline XBRL at order %(order)s has non-matching content %(value)s'),
                      modelObject=(
                     prevTupleFact, f),
                      order=(f.order),
                      value=(prevTupleFact.textValue.strip()))

    def checkContexts(self, contexts):
        for cntx in contexts:
            if cntx.isStartEndPeriod:
                try:
                    if cntx.endDatetime is not None:
                        if cntx.startDatetime is not None:
                            if cntx.endDatetime <= cntx.startDatetime:
                                self.modelXbrl.error('xbrl.4.7.2:periodStartBeforeEnd', (_'Context %(contextID)s must have startDate less than endDate'),
                                  modelObject=cntx,
                                  contextID=(cntx.id))
                except (TypeError, ValueError) as err:
                    self.modelXbrl.error('xbrl.4.7.2:contextDateError', (_'Context %(contextID) startDate or endDate: %(error)s'),
                      modelObject=cntx,
                      contextID=(cntx.id),
                      error=err)

            else:
                if cntx.isInstantPeriod:
                    try:
                        cntx.instantDatetime
                    except ValueError as err:
                        self.modelXbrl.error('xbrl.4.7.2:contextDateError', (_'Context %(contextID)s instant date: %(error)s'),
                          modelObject=cntx,
                          contextID=(cntx.id),
                          error=err)

                self.segmentScenariocntx.segmentcntx.id'segment''4.7.3.2'
                self.segmentScenariocntx.scenariocntx.id'scenario''4.7.4'

    def checkContextsDimensions(self, contexts):
        for cntx in contexts:
            ValidateXbrlDimensions.checkContext(self, cntx)

    def checkUnits(self, units):
        for unit in units:
            mulDivMeasures = unit.measures
            if mulDivMeasures:
                for measures in mulDivMeasures:
                    for measure in measures:
                        if measure.namespaceURI == XbrlConst.xbrli and measure not in (XbrlConst.qnXbrliPure, XbrlConst.qnXbrliShares):
                            self.modelXbrl.error('xbrl.4.8.2:measureElement', (_'Unit %(unitID)s illegal measure: %(measure)s'),
                              modelObject=unit,
                              unitID=(unit.id),
                              measure=measure)

                for numeratorMeasure in mulDivMeasures[0]:
                    if numeratorMeasure in mulDivMeasures[1]:
                        self.modelXbrl.error('xbrl.4.8.4:measureBothNumDenom', (_'Unit %(unitID)s numerator measure: %(measure)s also appears as denominator measure'),
                          modelObject=unit,
                          unitID=(unit.id),
                          measure=numeratorMeasure)

    def fwdCycle(self, relsSet, rels, noUndirected, fromConcepts, cycleType='directed', revCycleRel=None):
        for rel in rels:
            if revCycleRel is not None:
                if rel.isIdenticalTorevCycleRel:
                    continue
                else:
                    relTo = rel.toModelObject
                    if relTo in fromConcepts:
                        return [
                         cycleType, rel]
                    fromConcepts.addrelTo
                    nextRels = relsSet.fromModelObjectrelTo
                    foundCycle = self.fwdCyclerelsSetnextRelsnoUndirectedfromConcepts
                    if foundCycle is not None:
                        foundCycle.appendrel
                        return foundCycle
                    fromConcepts.discardrelTo
                    if noUndirected:
                        foundCycle = self.revCyclerelsSetrelTorelfromConcepts
                        if foundCycle is not None:
                            foundCycle.appendrel
                            return foundCycle

    def revCycle(self, relsSet, toConcept, turnbackRel, fromConcepts):
        for rel in relsSet.toModelObjecttoConcept:
            if not rel.isIdenticalToturnbackRel:
                relFrom = rel.fromModelObject
                if relFrom in fromConcepts:
                    return [
                     'undirected', rel]
                fromConcepts.addrelFrom
                foundCycle = self.revCyclerelsSetrelFromturnbackRelfromConcepts
                if foundCycle is not None:
                    foundCycle.appendrel
                    return foundCycle
                fwdRels = relsSet.fromModelObjectrelFrom
                foundCycle = self.fwdCycle(relsSet, fwdRels, True, fromConcepts, cycleType='undirected', revCycleRel=rel)
                if foundCycle is not None:
                    foundCycle.appendrel
                    return foundCycle
                fromConcepts.discardrelFrom

    def segmentScenario(self, element, contextId, name, sect, topLevel=True):
        if topLevel:
            if element is None:
                return
        else:
            if element.namespaceURI == XbrlConst.xbrli:
                self.modelXbrl.error(('xbrl.{0}:{1}XbrliElement'.format(sect, name)), (_'Context %(contextID)s %(contextElement)s cannot have xbrli element %(elementName)s'),
                  modelObject=element,
                  contextID=contextId,
                  contextElement=name,
                  elementName=(element.prefixedName),
                  messageCodes=('xbrl.4.7.3.2:segmentXbrliElement', 'xbrl.4.7.4:scenarioXbrliElement'))
            else:
                concept = self.modelXbrl.qnameConcepts.getelement.qname
            if concept is not None:
                if concept.isItem or concept.isTuple:
                    self.modelXbrl.error(('xbrl.{0}:{1}ItemOrTuple'.format(sect, name)), (_'Context %(contextID)s %(contextElement)s cannot have item or tuple element %(elementName)s'),
                      modelObject=element,
                      contextID=contextId,
                      contextElement=name,
                      elementName=(element.prefixedName),
                      messageCodes=('xbrl.4.7.3.2:segmentItemOrTuple', 'xbrl.4.7.4:scenarioItemOrTuple'))
            hasChild = False
            for child in element.iterchildren():
                if isinstance(child, ModelObject):
                    self.segmentScenario(child, contextId, name, sect, topLevel=False)
                    hasChild = True

            if topLevel and not hasChild:
                self.modelXbrl.error(('xbrl.{0}:{1}Empty'.format(sect, name)), (_'Context %(contextID)s %(contextElement)s cannot be empty'),
                  modelObject=element,
                  contextID=contextId,
                  contextElement=name,
                  messageCodes=('xbrl.4.7.3.2:segmentEmpty', 'xbrl.4.7.4:scenarioEmpty'))

    def isGenericObject(self, elt, genQname):
        return self.modelXbrl.isInSubstitutionGroup(elt.qname, genQname)

    def isGenericLink(self, elt):
        return self.isGenericObject(elt, XbrlConst.qnGenLink)

    def isGenericArc(self, elt):
        return self.isGenericObject(elt, XbrlConst.qnGenArc)

    def isGenericResource(self, elt):
        return self.isGenericObject(elt.getparent(), XbrlConst.qnGenLink)

    def isGenericLabel(self, elt):
        return self.isGenericObject(elt, XbrlConst.qnGenLabel)

    def isGenericReference(self, elt):
        return self.isGenericObject(elt, XbrlConst.qnGenReference)

    def executeCallTest(self, modelXbrl, name, callTuple, testTuple):
        self.modelXbrl = modelXbrl
        ValidateFormula.executeCallTestselfnamecallTupletestTuple


# global validateUniqueParticleAttribution ## Warning: Unused global