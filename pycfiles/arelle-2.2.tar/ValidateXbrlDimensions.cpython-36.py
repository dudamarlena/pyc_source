# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\ValidateXbrlDimensions.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 38907 bytes
"""
Created on Oct 17, 2010

@author: Mark V Systems Limited
(c) Copyright 2010 Mark V Systems Limited, All rights reserved.
"""
import os, sys
from collections import defaultdict
from arelle import UrlUtil, XbrlConst
from arelle.ModelObject import ModelObject
from arelle.ModelDtsObject import ModelConcept
from arelle.PrototypeInstanceObject import ContextPrototype, DimValuePrototype
NONDEFAULT = sys.intern(_STR_8BIT('non-default'))

def loadDimensionDefaults(val):
    val.modelXbrl.dimensionDefaultConcepts = {}
    val.modelXbrl.qnameDimensionDefaults = {}
    val.modelXbrl.qnameDimensionContextElement = {}
    for baseSetKey in val.modelXbrl.baseSets.keys():
        arcrole, ELR, linkqname, arcqname = baseSetKey
        if ELR and linkqname and arcqname and arcrole in (XbrlConst.all, XbrlConst.dimensionDefault):
            checkBaseSet(val, arcrole, ELR, val.modelXbrl.relationshipSet(arcrole, ELR, linkqname, arcqname))

    val.modelXbrl.isDimensionsValidated = True


def checkBaseSet--- This code section failed: ---

 L.  29         0  LOAD_FAST                'arcrole'
                2  LOAD_GLOBAL              XbrlConst
                4  LOAD_ATTR                hypercubeDimension
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE   162  'to 162'

 L.  30        10  SETUP_LOOP          158  'to 158'
               12  LOAD_FAST                'relsSet'
               14  LOAD_ATTR                modelRelationships
               16  GET_ITER         
               18  FOR_ITER            156  'to 156'
               20  STORE_FAST               'modelRel'

 L.  31        22  LOAD_FAST                'modelRel'
               24  LOAD_ATTR                fromModelObject
               26  STORE_FAST               'fromConcept'

 L.  32        28  LOAD_FAST                'modelRel'
               30  LOAD_ATTR                toModelObject
               32  STORE_FAST               'toConcept'

 L.  33        34  LOAD_FAST                'fromConcept'
               36  LOAD_CONST               None
               38  COMPARE_OP               is-not
               40  POP_JUMP_IF_FALSE    18  'to 18'
               42  LOAD_FAST                'toConcept'
               44  LOAD_CONST               None
               46  COMPARE_OP               is-not
               48  POP_JUMP_IF_FALSE    18  'to 18'

 L.  34        50  LOAD_GLOBAL              isinstance
               52  LOAD_FAST                'fromConcept'
               54  LOAD_GLOBAL              ModelConcept
               56  CALL_FUNCTION_2       2  '2 positional arguments'
               58  UNARY_NOT        
               60  POP_JUMP_IF_TRUE     70  'to 70'
               62  LOAD_FAST                'fromConcept'
               64  LOAD_ATTR                isHypercubeItem
               66  UNARY_NOT        
             68_0  COME_FROM            60  '60'
               68  POP_JUMP_IF_FALSE   102  'to 102'

 L.  35        70  LOAD_FAST                'val'
               72  LOAD_ATTR                modelXbrl
               74  LOAD_ATTR                error
               76  LOAD_STR                 'xbrldte:HypercubeDimensionSourceError'

 L.  36        78  LOAD_GLOBAL              _
               80  LOAD_STR                 'Hypercube-dimension relationship from %(source)s to %(target)s in link role %(linkrole)s must have a hypercube declaration source'
               82  CALL_FUNCTION_1       1  '1 positional argument'

 L.  37        84  LOAD_FAST                'modelRel'
               86  LOAD_FAST                'fromConcept'
               88  LOAD_ATTR                qname
               90  LOAD_FAST                'toConcept'
               92  LOAD_ATTR                qname
               94  LOAD_FAST                'ELR'
               96  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
               98  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              100  POP_TOP          
            102_0  COME_FROM            68  '68'

 L.  38       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'toConcept'
              106  LOAD_GLOBAL              ModelConcept
              108  CALL_FUNCTION_2       2  '2 positional arguments'
              110  UNARY_NOT        
              112  POP_JUMP_IF_TRUE    122  'to 122'
              114  LOAD_FAST                'toConcept'
              116  LOAD_ATTR                isDimensionItem
              118  UNARY_NOT        
            120_0  COME_FROM           112  '112'
              120  POP_JUMP_IF_FALSE    18  'to 18'

 L.  39       122  LOAD_FAST                'val'
              124  LOAD_ATTR                modelXbrl
              126  LOAD_ATTR                error
              128  LOAD_STR                 'xbrldte:HypercubeDimensionTargetError'

 L.  40       130  LOAD_GLOBAL              _
              132  LOAD_STR                 'Hypercube-dimension relationship from %(source)s to %(target)s in link role %(linkrole)s must have a dimension declaration target'
              134  CALL_FUNCTION_1       1  '1 positional argument'

 L.  41       136  LOAD_FAST                'modelRel'
              138  LOAD_FAST                'fromConcept'
              140  LOAD_ATTR                qname
              142  LOAD_FAST                'toConcept'
              144  LOAD_ATTR                qname
              146  LOAD_FAST                'ELR'
              148  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
              150  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              152  POP_TOP          
              154  JUMP_BACK            18  'to 18'
              156  POP_BLOCK        
            158_0  COME_FROM_LOOP       10  '10'
              158  JUMP_FORWARD       1624  'to 1624'
              162  ELSE                     '1624'

 L.  43       162  LOAD_FAST                'arcrole'
              164  LOAD_GLOBAL              XbrlConst
              166  LOAD_ATTR                all
              168  LOAD_GLOBAL              XbrlConst
              170  LOAD_ATTR                notAll
              172  BUILD_TUPLE_2         2 
              174  COMPARE_OP               in
              176  POP_JUMP_IF_FALSE   878  'to 878'

 L.  44       180  LOAD_FAST                'relsSet'
              182  LOAD_ATTR                fromModelObjects
              184  CALL_FUNCTION_0       0  '0 positional arguments'
              186  STORE_FAST               'fromRelationships'

 L.  45       188  SETUP_LOOP         1624  'to 1624'
              192  LOAD_FAST                'fromRelationships'
              194  LOAD_ATTR                items
              196  CALL_FUNCTION_0       0  '0 positional arguments'
              198  GET_ITER         
              200  FOR_ITER            872  'to 872'
              204  UNPACK_SEQUENCE_2     2 
              206  STORE_FAST               'priItemConcept'
              208  STORE_FAST               'hcRels'

 L.  46       210  SETUP_LOOP          870  'to 870'
              214  LOAD_FAST                'hcRels'
              216  GET_ITER         
              218  FOR_ITER            868  'to 868'
              222  STORE_FAST               'hasHcRel'

 L.  47       224  LOAD_FAST                'hasHcRel'
              226  LOAD_ATTR                toModelObject
              228  STORE_FAST               'hcConcept'

 L.  48       230  LOAD_FAST                'priItemConcept'
              232  LOAD_CONST               None
              234  COMPARE_OP               is-not
              236  JUMP_IF_FALSE_OR_POP   244  'to 244'
              238  LOAD_FAST                'hcConcept'
              240  LOAD_CONST               None
              242  COMPARE_OP               is-not
            244_0  COME_FROM           236  '236'
              244  POP_JUMP_IF_FALSE   218  'to 218'

 L.  49       246  LOAD_GLOBAL              isinstance
              248  LOAD_FAST                'priItemConcept'
              250  LOAD_GLOBAL              ModelConcept
              252  CALL_FUNCTION_2       2  '2 positional arguments'
              254  UNARY_NOT        
              256  POP_JUMP_IF_TRUE    270  'to 270'
              260  LOAD_FAST                'priItemConcept'
              262  LOAD_ATTR                isPrimaryItem
              264  UNARY_NOT        
            266_0  COME_FROM           256  '256'
              266  POP_JUMP_IF_FALSE   312  'to 312'

 L.  50       270  LOAD_FAST                'val'
              272  LOAD_ATTR                modelXbrl
              274  LOAD_ATTR                error
              276  LOAD_STR                 'xbrldte:HasHypercubeSourceError'

 L.  51       278  LOAD_GLOBAL              _
              280  LOAD_STR                 'HasHypercube %(arcroleType)s relationship from %(source)s to %(target)s in link role %(linkrole)s must have a primary item source'
              282  CALL_FUNCTION_1       1  '1 positional argument'

 L.  52       284  LOAD_FAST                'hasHcRel'
              286  LOAD_GLOBAL              os
              288  LOAD_ATTR                path
              290  LOAD_ATTR                basename
              292  LOAD_FAST                'arcrole'
              294  CALL_FUNCTION_1       1  '1 positional argument'

 L.  53       296  LOAD_FAST                'priItemConcept'
              298  LOAD_ATTR                qname
              300  LOAD_FAST                'hcConcept'
              302  LOAD_ATTR                qname
              304  LOAD_FAST                'ELR'
              306  LOAD_CONST               ('modelObject', 'arcroleType', 'source', 'target', 'linkrole')
              308  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              310  POP_TOP          
            312_0  COME_FROM           266  '266'

 L.  54       312  LOAD_GLOBAL              isinstance
              314  LOAD_FAST                'hcConcept'
              316  LOAD_GLOBAL              ModelConcept
              318  CALL_FUNCTION_2       2  '2 positional arguments'
              320  UNARY_NOT        
              322  POP_JUMP_IF_TRUE    336  'to 336'
              326  LOAD_FAST                'hcConcept'
              328  LOAD_ATTR                isHypercubeItem
              330  UNARY_NOT        
            332_0  COME_FROM           322  '322'
              332  POP_JUMP_IF_FALSE   378  'to 378'

 L.  55       336  LOAD_FAST                'val'
              338  LOAD_ATTR                modelXbrl
              340  LOAD_ATTR                error
              342  LOAD_STR                 'xbrldte:HasHypercubeTargetError'

 L.  56       344  LOAD_GLOBAL              _
              346  LOAD_STR                 'HasHypercube %(arcroleType)s relationship from %(source)s to %(target)s in link role %(linkrole)s must have a hypercube declaration target'
              348  CALL_FUNCTION_1       1  '1 positional argument'

 L.  57       350  LOAD_FAST                'hasHcRel'
              352  LOAD_GLOBAL              os
              354  LOAD_ATTR                path
              356  LOAD_ATTR                basename
              358  LOAD_FAST                'arcrole'
              360  CALL_FUNCTION_1       1  '1 positional argument'

 L.  58       362  LOAD_FAST                'priItemConcept'
              364  LOAD_ATTR                qname
              366  LOAD_FAST                'hcConcept'
              368  LOAD_ATTR                qname
              370  LOAD_FAST                'ELR'
              372  LOAD_CONST               ('modelObject', 'arcroleType', 'source', 'target', 'linkrole')
              374  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              376  POP_TOP          
            378_0  COME_FROM           332  '332'

 L.  59       378  LOAD_FAST                'hasHcRel'
              380  LOAD_ATTR                contextElement
              382  STORE_FAST               'hcContextElement'

 L.  60       384  LOAD_FAST                'hcContextElement'
              386  LOAD_CONST               ('segment', 'scenario')
              388  COMPARE_OP               not-in
              390  POP_JUMP_IF_FALSE   436  'to 436'

 L.  61       394  LOAD_FAST                'val'
              396  LOAD_ATTR                modelXbrl
              398  LOAD_ATTR                error
              400  LOAD_STR                 'xbrldte:HasHypercubeMissingContextElementAttributeError'

 L.  62       402  LOAD_GLOBAL              _
              404  LOAD_STR                 'HasHypercube %(arcroleType)s relationship from %(source)s to %(target)s in link role %(linkrole)s must have a context element'
              406  CALL_FUNCTION_1       1  '1 positional argument'

 L.  63       408  LOAD_FAST                'hasHcRel'
              410  LOAD_GLOBAL              os
              412  LOAD_ATTR                path
              414  LOAD_ATTR                basename
              416  LOAD_FAST                'arcrole'
              418  CALL_FUNCTION_1       1  '1 positional argument'

 L.  64       420  LOAD_FAST                'priItemConcept'
              422  LOAD_ATTR                qname
              424  LOAD_FAST                'hcConcept'
              426  LOAD_ATTR                qname
              428  LOAD_FAST                'ELR'
              430  LOAD_CONST               ('modelObject', 'arcroleType', 'source', 'target', 'linkrole')
              432  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              434  POP_TOP          
            436_0  COME_FROM           390  '390'

 L.  67       436  LOAD_FAST                'hasHcRel'
              438  LOAD_ATTR                targetRole
              440  STORE_FAST               'dimELR'

 L.  68       442  LOAD_FAST                'dimELR'
              444  POP_JUMP_IF_TRUE    452  'to 452'

 L.  69       448  LOAD_FAST                'ELR'
              450  STORE_FAST               'dimELR'
            452_0  COME_FROM           444  '444'

 L.  70       452  LOAD_FAST                'val'
              454  LOAD_ATTR                modelXbrl
              456  LOAD_ATTR                relationshipSet

 L.  71       458  LOAD_GLOBAL              XbrlConst
              460  LOAD_ATTR                hypercubeDimension
              462  LOAD_FAST                'dimELR'
              464  CALL_FUNCTION_2       2  '2 positional arguments'
              466  LOAD_ATTR                fromModelObject
              468  LOAD_FAST                'hcConcept'
              470  CALL_FUNCTION_1       1  '1 positional argument'
              472  STORE_FAST               'hcDimRels'

 L.  72       474  SETUP_LOOP          866  'to 866'
              478  LOAD_FAST                'hcDimRels'
              480  GET_ITER         
              482  FOR_ITER            864  'to 864'
              486  STORE_FAST               'hcDimRel'

 L.  73       488  LOAD_FAST                'hcDimRel'
              490  LOAD_ATTR                toModelObject
              492  STORE_FAST               'dimConcept'

 L.  74       494  LOAD_FAST                'dimConcept'
              496  LOAD_CONST               None
              498  COMPARE_OP               is-not
              500  POP_JUMP_IF_FALSE   482  'to 482'

 L.  75       504  LOAD_FAST                'arcrole'
              506  LOAD_GLOBAL              XbrlConst
              508  LOAD_ATTR                all
              510  COMPARE_OP               ==
              512  POP_JUMP_IF_FALSE   558  'to 558'

 L.  76       516  LOAD_FAST                'val'
              518  LOAD_ATTR                modelXbrl
              520  LOAD_ATTR                qnameDimensionContextElement
              522  LOAD_ATTR                setdefault
              524  LOAD_FAST                'dimConcept'
              526  LOAD_ATTR                qname
              528  LOAD_FAST                'hcContextElement'
              530  CALL_FUNCTION_2       2  '2 positional arguments'
              532  STORE_FAST               'cntxElt'

 L.  77       534  LOAD_FAST                'cntxElt'
              536  LOAD_FAST                'hcContextElement'
              538  COMPARE_OP               !=
              540  POP_JUMP_IF_FALSE   558  'to 558'

 L.  78       544  LOAD_STR                 'ambiguous'
              546  LOAD_FAST                'val'
              548  LOAD_ATTR                modelXbrl
              550  LOAD_ATTR                qnameDimensionContextElement
              552  LOAD_FAST                'dimConcept'
              554  LOAD_ATTR                qname
              556  STORE_SUBSCR     
            558_0  COME_FROM           540  '540'
            558_1  COME_FROM           512  '512'

 L.  79       558  LOAD_FAST                'hcDimRel'
              560  LOAD_ATTR                targetRole
              562  STORE_FAST               'domELR'

 L.  80       564  LOAD_FAST                'domELR'
              566  POP_JUMP_IF_TRUE    574  'to 574'

 L.  81       570  LOAD_FAST                'dimELR'
              572  STORE_FAST               'domELR'
            574_0  COME_FROM           566  '566'

 L.  82       574  LOAD_FAST                'val'
              576  LOAD_ATTR                modelXbrl
              578  LOAD_ATTR                relationshipSet

 L.  83       580  LOAD_GLOBAL              XbrlConst
              582  LOAD_ATTR                dimensionDomain
              584  LOAD_FAST                'domELR'
              586  CALL_FUNCTION_2       2  '2 positional arguments'
              588  LOAD_ATTR                fromModelObject
              590  LOAD_FAST                'dimConcept'
              592  CALL_FUNCTION_1       1  '1 positional argument'
              594  STORE_FAST               'dimDomRels'

 L.  84       596  LOAD_GLOBAL              xdtCycle
              598  LOAD_FAST                'val'
              600  LOAD_GLOBAL              domainTargetRoles
              602  LOAD_FAST                'val'
              604  LOAD_FAST                'domELR'
              606  LOAD_FAST                'dimDomRels'
              608  CALL_FUNCTION_3       3  '3 positional arguments'
              610  LOAD_FAST                'dimDomRels'
              612  LOAD_FAST                'hcConcept'
              614  LOAD_FAST                'dimConcept'
              616  BUILD_SET_2           2 
              618  CALL_FUNCTION_4       4  '4 positional arguments'
              620  STORE_FAST               'cycle'

 L.  85       622  LOAD_FAST                'cycle'
              624  LOAD_CONST               None
              626  COMPARE_OP               is-not
              628  POP_JUMP_IF_FALSE   730  'to 730'

 L.  86       632  LOAD_FAST                'cycle'
              634  LOAD_CONST               None
              636  COMPARE_OP               is-not
              638  POP_JUMP_IF_FALSE   690  'to 690'

 L.  87       642  LOAD_FAST                'cycle'
              644  LOAD_ATTR                append
              646  LOAD_FAST                'hcDimRel'
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  POP_TOP          

 L.  88       652  LOAD_GLOBAL              str
              654  LOAD_FAST                'hcConcept'
              656  LOAD_ATTR                qname
              658  CALL_FUNCTION_1       1  '1 positional argument'
              660  LOAD_STR                 ' '
              662  BINARY_ADD       
              664  LOAD_STR                 ' - '
              666  LOAD_ATTR                join

 L.  89       668  LOAD_GENEXPR             '<code_object <genexpr>>'
              670  LOAD_STR                 'checkBaseSet.<locals>.<genexpr>'
              672  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  90       674  LOAD_GLOBAL              reversed
              676  LOAD_FAST                'cycle'
              678  CALL_FUNCTION_1       1  '1 positional argument'
              680  GET_ITER         
              682  CALL_FUNCTION_1       1  '1 positional argument'
              684  CALL_FUNCTION_1       1  '1 positional argument'
              686  BINARY_ADD       
              688  STORE_FAST               'path'
            690_0  COME_FROM           638  '638'

 L.  91       690  LOAD_FAST                'val'
              692  LOAD_ATTR                modelXbrl
              694  LOAD_ATTR                error
              696  LOAD_STR                 'xbrldte:DRSDirectedCycleError'

 L.  92       698  LOAD_GLOBAL              _
              700  LOAD_STR                 'Dimension relationships have a directed cycle in DRS role %(linkrole)s \nstarting from hypercube %(hypercube)s, \ndimension %(dimension)s, \npath %(path)s'
              702  CALL_FUNCTION_1       1  '1 positional argument'

 L.  93       704  LOAD_FAST                'hcConcept'
              706  BUILD_LIST_1          1 
              708  LOAD_FAST                'cycle'
              710  BINARY_ADD       
              712  LOAD_FAST                'hcConcept'
              714  LOAD_ATTR                qname
              716  LOAD_FAST                'dimConcept'
              718  LOAD_ATTR                qname
              720  LOAD_FAST                'ELR'
              722  LOAD_FAST                'path'
              724  LOAD_CONST               ('modelObject', 'hypercube', 'dimension', 'linkrole', 'path')
              726  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              728  POP_TOP          
            730_0  COME_FROM           628  '628'

 L.  94       730  LOAD_GLOBAL              drsPolymorphism
              732  LOAD_FAST                'val'
              734  LOAD_FAST                'domELR'
              736  LOAD_FAST                'dimDomRels'
              738  LOAD_GLOBAL              drsPriItems
              740  LOAD_FAST                'val'
              742  LOAD_FAST                'ELR'
              744  LOAD_FAST                'priItemConcept'
              746  CALL_FUNCTION_3       3  '3 positional arguments'
              748  CALL_FUNCTION_4       4  '4 positional arguments'
              750  STORE_FAST               'cycle'

 L.  95       752  LOAD_FAST                'cycle'
              754  LOAD_CONST               None
              756  COMPARE_OP               is-not
              758  POP_JUMP_IF_FALSE   482  'to 482'

 L.  96       762  LOAD_FAST                'cycle'
              764  LOAD_CONST               None
              766  COMPARE_OP               is-not
              768  POP_JUMP_IF_FALSE   820  'to 820'

 L.  97       772  LOAD_FAST                'cycle'
              774  LOAD_ATTR                append
              776  LOAD_FAST                'hcDimRel'
              778  CALL_FUNCTION_1       1  '1 positional argument'
              780  POP_TOP          

 L.  98       782  LOAD_GLOBAL              str
              784  LOAD_FAST                'priItemConcept'
              786  LOAD_ATTR                qname
              788  CALL_FUNCTION_1       1  '1 positional argument'
              790  LOAD_STR                 ' '
              792  BINARY_ADD       
              794  LOAD_STR                 ' - '
              796  LOAD_ATTR                join

 L.  99       798  LOAD_GENEXPR             '<code_object <genexpr>>'
              800  LOAD_STR                 'checkBaseSet.<locals>.<genexpr>'
              802  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 100       804  LOAD_GLOBAL              reversed
              806  LOAD_FAST                'cycle'
              808  CALL_FUNCTION_1       1  '1 positional argument'
              810  GET_ITER         
              812  CALL_FUNCTION_1       1  '1 positional argument'
              814  CALL_FUNCTION_1       1  '1 positional argument'
              816  BINARY_ADD       
              818  STORE_FAST               'path'
            820_0  COME_FROM           768  '768'

 L. 101       820  LOAD_FAST                'val'
              822  LOAD_ATTR                modelXbrl
              824  LOAD_ATTR                error
              826  LOAD_STR                 'xbrldte:PrimaryItemPolymorphismError'

 L. 102       828  LOAD_GLOBAL              _
              830  LOAD_STR                 'Dimension relationships have a polymorphism cycle in DRS role %(linkrole)s \nstarting from hypercube %(hypercube)s, \ndimension %(dimension)s, \npath %(path)s'
              832  CALL_FUNCTION_1       1  '1 positional argument'

 L. 103       834  LOAD_FAST                'hcConcept'
              836  BUILD_LIST_1          1 
              838  LOAD_FAST                'cycle'
              840  BINARY_ADD       
              842  LOAD_FAST                'hcConcept'
              844  LOAD_ATTR                qname
              846  LOAD_FAST                'dimConcept'
              848  LOAD_ATTR                qname
              850  LOAD_FAST                'ELR'
              852  LOAD_FAST                'path'
              854  LOAD_CONST               ('modelObject', 'hypercube', 'dimension', 'linkrole', 'path')
              856  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              858  POP_TOP          
              860  JUMP_BACK           482  'to 482'
              864  POP_BLOCK        
            866_0  COME_FROM_LOOP      474  '474'
              866  JUMP_BACK           218  'to 218'
              868  POP_BLOCK        
            870_0  COME_FROM_LOOP      210  '210'
              870  JUMP_BACK           200  'to 200'
              872  POP_BLOCK        
              874  JUMP_FORWARD       1624  'to 1624'
              878  ELSE                     '1624'

 L. 105       878  LOAD_FAST                'arcrole'
              880  LOAD_GLOBAL              XbrlConst
              882  LOAD_ATTR                dimensionDomain
              884  COMPARE_OP               ==
              886  POP_JUMP_IF_FALSE  1106  'to 1106'

 L. 106       890  SETUP_LOOP         1102  'to 1102'
              892  LOAD_FAST                'relsSet'
              894  LOAD_ATTR                modelRelationships
              896  GET_ITER         
              898  FOR_ITER           1100  'to 1100'
              900  STORE_FAST               'modelRel'

 L. 107       902  LOAD_FAST                'modelRel'
              904  LOAD_ATTR                fromModelObject
              906  STORE_FAST               'fromConcept'

 L. 108       908  LOAD_FAST                'modelRel'
              910  LOAD_ATTR                toModelObject
              912  STORE_FAST               'toConcept'

 L. 109       914  LOAD_FAST                'fromConcept'
              916  LOAD_CONST               None
              918  COMPARE_OP               is-not
              920  POP_JUMP_IF_FALSE   898  'to 898'
              924  LOAD_FAST                'toConcept'
              926  LOAD_CONST               None
              928  COMPARE_OP               is-not
              930  POP_JUMP_IF_FALSE   898  'to 898'

 L. 110       934  LOAD_GLOBAL              isinstance
              936  LOAD_FAST                'fromConcept'
              938  LOAD_GLOBAL              ModelConcept
              940  CALL_FUNCTION_2       2  '2 positional arguments'
              942  UNARY_NOT        
              944  POP_JUMP_IF_TRUE    958  'to 958'
              948  LOAD_FAST                'fromConcept'
              950  LOAD_ATTR                isDimensionItem
              952  UNARY_NOT        
            954_0  COME_FROM           944  '944'
              954  POP_JUMP_IF_FALSE   992  'to 992'

 L. 111       958  LOAD_FAST                'val'
              960  LOAD_ATTR                modelXbrl
              962  LOAD_ATTR                error
              964  LOAD_STR                 'xbrldte:DimensionDomainSourceError'

 L. 112       966  LOAD_GLOBAL              _
              968  LOAD_STR                 'Dimension-domain relationship from %(source)s to %(target)s in link role %(linkrole)s must have a dimension declaration source'
              970  CALL_FUNCTION_1       1  '1 positional argument'

 L. 113       972  LOAD_FAST                'modelRel'
              974  LOAD_FAST                'fromConcept'
              976  LOAD_ATTR                qname
              978  LOAD_FAST                'toConcept'
              980  LOAD_ATTR                qname
              982  LOAD_FAST                'ELR'
              984  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
              986  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              988  POP_TOP          
              990  JUMP_FORWARD       1040  'to 1040'
              992  ELSE                     '1040'

 L. 114       992  LOAD_FAST                'fromConcept'
              994  LOAD_ATTR                get
              996  LOAD_STR                 '{http://xbrl.org/2005/xbrldt}typedDomainRef'
              998  CALL_FUNCTION_1       1  '1 positional argument'
             1000  LOAD_CONST               None
             1002  COMPARE_OP               is-not
             1004  POP_JUMP_IF_FALSE  1040  'to 1040'

 L. 115      1008  LOAD_FAST                'val'
             1010  LOAD_ATTR                modelXbrl
             1012  LOAD_ATTR                error
             1014  LOAD_STR                 'xbrldte:DimensionDomainSourceError'

 L. 116      1016  LOAD_GLOBAL              _
             1018  LOAD_STR                 'Dimension-domain relationship from %(source)s to %(target)s in link role %(linkrole)s has a typed dimension source'
             1020  CALL_FUNCTION_1       1  '1 positional argument'

 L. 117      1022  LOAD_FAST                'modelRel'
             1024  LOAD_FAST                'fromConcept'
             1026  LOAD_ATTR                qname
             1028  LOAD_FAST                'toConcept'
             1030  LOAD_ATTR                qname
             1032  LOAD_FAST                'ELR'
             1034  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
             1036  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1038  POP_TOP          
           1040_0  COME_FROM          1004  '1004'
           1040_1  COME_FROM           990  '990'

 L. 118      1040  LOAD_GLOBAL              isinstance
             1042  LOAD_FAST                'toConcept'
             1044  LOAD_GLOBAL              ModelConcept
             1046  CALL_FUNCTION_2       2  '2 positional arguments'
             1048  UNARY_NOT        
             1050  POP_JUMP_IF_TRUE   1064  'to 1064'
             1054  LOAD_FAST                'toConcept'
             1056  LOAD_ATTR                isDomainMember
             1058  UNARY_NOT        
           1060_0  COME_FROM          1050  '1050'
             1060  POP_JUMP_IF_FALSE   898  'to 898'

 L. 119      1064  LOAD_FAST                'val'
             1066  LOAD_ATTR                modelXbrl
             1068  LOAD_ATTR                error
             1070  LOAD_STR                 'xbrldte:DimensionDomainTargetError'

 L. 120      1072  LOAD_GLOBAL              _
             1074  LOAD_STR                 'Dimension-domain relationship from %(source)s to %(target)s in link role %(linkrole)s must have a domain member target'
             1076  CALL_FUNCTION_1       1  '1 positional argument'

 L. 121      1078  LOAD_FAST                'modelRel'
             1080  LOAD_FAST                'fromConcept'
             1082  LOAD_ATTR                qname
             1084  LOAD_FAST                'toConcept'
             1086  LOAD_ATTR                qname
             1088  LOAD_FAST                'ELR'
             1090  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
             1092  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1094  POP_TOP          
             1096  JUMP_BACK           898  'to 898'
             1100  POP_BLOCK        
           1102_0  COME_FROM_LOOP      890  '890'
             1102  JUMP_FORWARD       1624  'to 1624'
             1106  ELSE                     '1624'

 L. 123      1106  LOAD_FAST                'arcrole'
             1108  LOAD_GLOBAL              XbrlConst
             1110  LOAD_ATTR                dimensionDefault
             1112  COMPARE_OP               ==
             1114  POP_JUMP_IF_FALSE  1436  'to 1436'

 L. 124      1118  SETUP_LOOP         1624  'to 1624'
             1122  LOAD_FAST                'relsSet'
             1124  LOAD_ATTR                modelRelationships
             1126  GET_ITER         
             1128  FOR_ITER           1432  'to 1432'
             1132  STORE_FAST               'modelRel'

 L. 125      1134  LOAD_FAST                'modelRel'
             1136  LOAD_ATTR                fromModelObject
             1138  STORE_FAST               'fromConcept'

 L. 126      1140  LOAD_FAST                'modelRel'
             1142  LOAD_ATTR                toModelObject
             1144  STORE_FAST               'toConcept'

 L. 127      1146  LOAD_FAST                'fromConcept'
             1148  LOAD_CONST               None
             1150  COMPARE_OP               is-not
             1152  POP_JUMP_IF_FALSE  1128  'to 1128'
             1156  LOAD_FAST                'toConcept'
             1158  LOAD_CONST               None
             1160  COMPARE_OP               is-not
             1162  POP_JUMP_IF_FALSE  1128  'to 1128'

 L. 128      1166  LOAD_GLOBAL              isinstance
             1168  LOAD_FAST                'fromConcept'
             1170  LOAD_GLOBAL              ModelConcept
             1172  CALL_FUNCTION_2       2  '2 positional arguments'
             1174  UNARY_NOT        
             1176  POP_JUMP_IF_TRUE   1190  'to 1190'
             1180  LOAD_FAST                'fromConcept'
             1182  LOAD_ATTR                isDimensionItem
             1184  UNARY_NOT        
           1186_0  COME_FROM          1176  '1176'
             1186  POP_JUMP_IF_FALSE  1224  'to 1224'

 L. 129      1190  LOAD_FAST                'val'
             1192  LOAD_ATTR                modelXbrl
             1194  LOAD_ATTR                error
             1196  LOAD_STR                 'xbrldte:DimensionDefaultSourceError'

 L. 130      1198  LOAD_GLOBAL              _
             1200  LOAD_STR                 'Dimension-default relationship from %(source)s to %(target)s in link role %(linkrole)s must have a dimension declaration source'
             1202  CALL_FUNCTION_1       1  '1 positional argument'

 L. 131      1204  LOAD_FAST                'modelRel'
             1206  LOAD_FAST                'fromConcept'
             1208  LOAD_ATTR                qname
             1210  LOAD_FAST                'toConcept'
             1212  LOAD_ATTR                qname
             1214  LOAD_FAST                'ELR'
             1216  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
             1218  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1220  POP_TOP          
             1222  JUMP_FORWARD       1268  'to 1268'
             1224  ELSE                     '1268'

 L. 132      1224  LOAD_FAST                'fromConcept'
             1226  LOAD_ATTR                get
             1228  LOAD_STR                 '{http://xbrl.org/2005/xbrldt}typedDomainRef'
             1230  CALL_FUNCTION_1       1  '1 positional argument'
             1232  POP_JUMP_IF_FALSE  1268  'to 1268'

 L. 133      1236  LOAD_FAST                'val'
             1238  LOAD_ATTR                modelXbrl
             1240  LOAD_ATTR                error
             1242  LOAD_STR                 'xbrldte:DimensionDefaultSourceError'

 L. 134      1244  LOAD_GLOBAL              _
             1246  LOAD_STR                 'Dimension-default relationship from %(source)s to %(target)s in link role %(linkrole)s has a typed dimension source'
             1248  CALL_FUNCTION_1       1  '1 positional argument'

 L. 135      1250  LOAD_FAST                'modelRel'
             1252  LOAD_FAST                'fromConcept'
             1254  LOAD_ATTR                qname
             1256  LOAD_FAST                'toConcept'
             1258  LOAD_ATTR                qname
             1260  LOAD_FAST                'ELR'
             1262  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
             1264  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1266  POP_TOP          
           1268_0  COME_FROM          1232  '1232'
           1268_1  COME_FROM          1222  '1222'

 L. 136      1268  LOAD_GLOBAL              isinstance
             1270  LOAD_FAST                'toConcept'
             1272  LOAD_GLOBAL              ModelConcept
             1274  CALL_FUNCTION_2       2  '2 positional arguments'
             1276  UNARY_NOT        
             1278  POP_JUMP_IF_TRUE   1292  'to 1292'
             1282  LOAD_FAST                'toConcept'
             1284  LOAD_ATTR                isDomainMember
             1286  UNARY_NOT        
           1288_0  COME_FROM          1278  '1278'
             1288  POP_JUMP_IF_FALSE  1324  'to 1324'

 L. 137      1292  LOAD_FAST                'val'
             1294  LOAD_ATTR                modelXbrl
             1296  LOAD_ATTR                error
             1298  LOAD_STR                 'xbrldte:DimensionDefaultTargetError'

 L. 138      1300  LOAD_GLOBAL              _
             1302  LOAD_STR                 'Dimension-default relationship from %(source)s to %(target)s in link role %(linkrole)s must have a domain member target'
             1304  CALL_FUNCTION_1       1  '1 positional argument'

 L. 139      1306  LOAD_FAST                'modelRel'
             1308  LOAD_FAST                'fromConcept'
             1310  LOAD_ATTR                qname
             1312  LOAD_FAST                'toConcept'
             1314  LOAD_ATTR                qname
             1316  LOAD_FAST                'ELR'
             1318  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
             1320  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1322  POP_TOP          
           1324_0  COME_FROM          1288  '1288'

 L. 140      1324  LOAD_FAST                'fromConcept'
             1326  LOAD_FAST                'val'
             1328  LOAD_ATTR                modelXbrl
             1330  LOAD_ATTR                dimensionDefaultConcepts
             1332  COMPARE_OP               in
             1334  POP_JUMP_IF_FALSE  1400  'to 1400'
             1338  LOAD_FAST                'toConcept'
             1340  LOAD_FAST                'val'
             1342  LOAD_ATTR                modelXbrl
             1344  LOAD_ATTR                dimensionDefaultConcepts
             1346  LOAD_FAST                'fromConcept'
             1348  BINARY_SUBSCR    
             1350  COMPARE_OP               !=
             1352  POP_JUMP_IF_FALSE  1400  'to 1400'

 L. 141      1356  LOAD_FAST                'val'
             1358  LOAD_ATTR                modelXbrl
             1360  LOAD_ATTR                error
             1362  LOAD_STR                 'xbrldte:TooManyDefaultMembersError'

 L. 142      1364  LOAD_GLOBAL              _
             1366  LOAD_STR                 'Dimension %(source)s has multiple defaults %(target)s and %(target2)s'
             1368  CALL_FUNCTION_1       1  '1 positional argument'

 L. 143      1370  LOAD_FAST                'modelRel'
             1372  LOAD_FAST                'fromConcept'
             1374  LOAD_ATTR                qname
             1376  LOAD_FAST                'toConcept'
             1378  LOAD_ATTR                qname

 L. 144      1380  LOAD_FAST                'val'
             1382  LOAD_ATTR                modelXbrl
             1384  LOAD_ATTR                dimensionDefaultConcepts
             1386  LOAD_FAST                'fromConcept'
             1388  BINARY_SUBSCR    
             1390  LOAD_ATTR                qname
             1392  LOAD_CONST               ('modelObject', 'source', 'target', 'target2')
             1394  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1396  POP_TOP          
             1398  JUMP_FORWARD       1428  'to 1428'
           1400_0  COME_FROM          1334  '1334'

 L. 146      1400  LOAD_FAST                'toConcept'
             1402  LOAD_FAST                'val'
             1404  LOAD_ATTR                modelXbrl
             1406  LOAD_ATTR                dimensionDefaultConcepts
             1408  LOAD_FAST                'fromConcept'
             1410  STORE_SUBSCR     

 L. 147      1412  LOAD_FAST                'toConcept'
             1414  LOAD_ATTR                qname
             1416  LOAD_FAST                'val'
             1418  LOAD_ATTR                modelXbrl
             1420  LOAD_ATTR                qnameDimensionDefaults
             1422  LOAD_FAST                'fromConcept'
             1424  LOAD_ATTR                qname
             1426  STORE_SUBSCR     
           1428_0  COME_FROM          1398  '1398'
             1428  JUMP_BACK          1128  'to 1128'
             1432  POP_BLOCK        
           1434_0  COME_FROM_LOOP     1118  '1118'
             1434  JUMP_FORWARD       1624  'to 1624'
             1436  ELSE                     '1624'

 L. 150      1436  LOAD_FAST                'arcrole'
             1438  LOAD_GLOBAL              XbrlConst
             1440  LOAD_ATTR                domainMember
             1442  COMPARE_OP               ==
             1444  POP_JUMP_IF_FALSE  1624  'to 1624'

 L. 151      1448  LOAD_FAST                'relsSet'
             1450  LOAD_ATTR                fromModelObjects
             1452  CALL_FUNCTION_0       0  '0 positional arguments'
             1454  STORE_FAST               'fromRelationships'

 L. 152      1456  SETUP_LOOP         1624  'to 1624'
             1458  LOAD_FAST                'fromRelationships'
             1460  LOAD_ATTR                items
             1462  CALL_FUNCTION_0       0  '0 positional arguments'
             1464  GET_ITER         
             1466  FOR_ITER           1622  'to 1622'
             1468  UNPACK_SEQUENCE_2     2 
             1470  STORE_FAST               'priItemConcept'
             1472  STORE_FAST               'rels'

 L. 153      1474  SETUP_LOOP         1618  'to 1618'
             1476  LOAD_FAST                'rels'
             1478  GET_ITER         
             1480  FOR_ITER           1616  'to 1616'
             1482  STORE_FAST               'domMbrRel'

 L. 154      1484  LOAD_FAST                'domMbrRel'
             1486  LOAD_ATTR                toModelObject
             1488  STORE_FAST               'toConcept'

 L. 155      1490  LOAD_FAST                'toConcept'
             1492  LOAD_CONST               None
             1494  COMPARE_OP               is-not
             1496  POP_JUMP_IF_FALSE  1480  'to 1480'

 L. 156      1500  LOAD_GLOBAL              isinstance
             1502  LOAD_FAST                'priItemConcept'
             1504  LOAD_GLOBAL              ModelConcept
             1506  CALL_FUNCTION_2       2  '2 positional arguments'
             1508  UNARY_NOT        
             1510  POP_JUMP_IF_TRUE   1524  'to 1524'
             1514  LOAD_FAST                'priItemConcept'
             1516  LOAD_ATTR                isDomainMember
             1518  UNARY_NOT        
           1520_0  COME_FROM          1510  '1510'
             1520  POP_JUMP_IF_FALSE  1556  'to 1556'

 L. 157      1524  LOAD_FAST                'val'
             1526  LOAD_ATTR                modelXbrl
             1528  LOAD_ATTR                error
             1530  LOAD_STR                 'xbrldte:DomainMemberSourceError'

 L. 158      1532  LOAD_GLOBAL              _
             1534  LOAD_STR                 'Domain-Member relationship from %(source)s to %(target)s in link role %(linkrole)s must have a domain primary item or domain member source'
             1536  CALL_FUNCTION_1       1  '1 positional argument'

 L. 159      1538  LOAD_FAST                'domMbrRel'
             1540  LOAD_FAST                'priItemConcept'
             1542  LOAD_ATTR                qname
             1544  LOAD_FAST                'toConcept'
             1546  LOAD_ATTR                qname
             1548  LOAD_FAST                'ELR'
             1550  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
             1552  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1554  POP_TOP          
           1556_0  COME_FROM          1520  '1520'

 L. 160      1556  LOAD_GLOBAL              isinstance
             1558  LOAD_FAST                'toConcept'
             1560  LOAD_GLOBAL              ModelConcept
             1562  CALL_FUNCTION_2       2  '2 positional arguments'
             1564  UNARY_NOT        
             1566  POP_JUMP_IF_TRUE   1580  'to 1580'
             1570  LOAD_FAST                'toConcept'
             1572  LOAD_ATTR                isDomainMember
             1574  UNARY_NOT        
           1576_0  COME_FROM          1566  '1566'
             1576  POP_JUMP_IF_FALSE  1480  'to 1480'

 L. 161      1580  LOAD_FAST                'val'
             1582  LOAD_ATTR                modelXbrl
             1584  LOAD_ATTR                error
             1586  LOAD_STR                 'xbrldte:DomainMemberTargetError'

 L. 162      1588  LOAD_GLOBAL              _
             1590  LOAD_STR                 'Domain-Member relationship from %(source)s to %(target)s in link role %(linkrole)s must have a domain primary item or domain member target'
             1592  CALL_FUNCTION_1       1  '1 positional argument'

 L. 163      1594  LOAD_FAST                'domMbrRel'
             1596  LOAD_FAST                'priItemConcept'
             1598  LOAD_ATTR                qname
             1600  LOAD_FAST                'toConcept'
             1602  LOAD_ATTR                qname
             1604  LOAD_FAST                'ELR'
             1606  LOAD_CONST               ('modelObject', 'source', 'target', 'linkrole')
             1608  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1610  POP_TOP          
             1612  JUMP_BACK          1480  'to 1480'
             1616  POP_BLOCK        
           1618_0  COME_FROM_LOOP     1474  '1474'
             1618  JUMP_BACK          1466  'to 1466'
             1622  POP_BLOCK        
           1624_0  COME_FROM_LOOP     1456  '1456'
           1624_1  COME_FROM          1444  '1444'
           1624_2  COME_FROM          1434  '1434'
           1624_3  COME_FROM          1102  '1102'
           1624_4  COME_FROM           874  '874'
           1624_5  COME_FROM           158  '158'

Parse error at or near `JUMP_FORWARD' instruction at offset 874


def domainTargetRoles(val, fromELR, rels, fromConcepts=None, ELRs=None):
    if fromConcepts is None:
        fromConcepts = set()
    if not ELRs:
        ELRs = {
         fromELR}
    for rel in rels:
        relTo = rel.toModelObject
        if relTo not in fromConcepts:
            fromConcepts.add(relTo)
            toELR = rel.targetRole
            if toELR:
                ELRs.add(toELR)
            else:
                toELR = fromELR
            domMbrRels = val.modelXbrl.relationshipSetXbrlConst.domainMembertoELR.fromModelObject(relTo)
            domainTargetRoles(val, toELR, domMbrRels, fromConcepts, ELRs)
            fromConcepts.discard(relTo)

    return ELRs


def xdtCycle(val, ELRs, rels, fromConcepts):
    for rel in rels:
        relTo = rel.toModelObject
        if rel.isUsable:
            if relTo in fromConcepts:
                return [
                 rel]
        fromConcepts.add(relTo)
        for ELR in ELRs:
            domMbrRels = val.modelXbrl.relationshipSetXbrlConst.domainMemberELR.fromModelObject(relTo)
            foundCycle = xdtCycle(val, ELRs, domMbrRels, fromConcepts)
            if foundCycle is not None:
                foundCycle.append(rel)
                return foundCycle

        fromConcepts.discard(relTo)


def drsPriItems(val, fromELR, fromPriItem, priItems=None):
    if priItems is None:
        priItems = {
         fromPriItem}
    for rel in val.modelXbrl.relationshipSetXbrlConst.domainMemberfromELR.fromModelObject(fromPriItem):
        toPriItem = rel.toModelObject
        if toPriItem not in priItems:
            if rel.isUsable:
                priItems.add(toPriItem)
            toELR = rel.targetRole
            drsPriItems(val, toELR if toELR else fromELR, toPriItem, priItems)

    return priItems


def drsPolymorphism(val, fromELR, rels, priItems, visitedMbrs=None):
    if visitedMbrs is None:
        visitedMbrs = set()
    for rel in rels:
        relTo = rel.toModelObject
        toELR = rel.targetRole
        if not toELR:
            toELR = fromELR
        if rel.isUsable:
            if relTo in priItems:
                return [
                 rel]
        if relTo not in visitedMbrs:
            visitedMbrs.add(relTo)
            domMbrRels = val.modelXbrl.relationshipSetXbrlConst.domainMembertoELR.fromModelObject(relTo)
            foundCycle = drsPolymorphism(val, toELR, domMbrRels, priItems, visitedMbrs)
            if foundCycle is not None:
                foundCycle.append(rel)
                return foundCycle
            visitedMbrs.discard(relTo)


def checkConcept(val, concept):
    if concept.get('{http://xbrl.org/2005/xbrldt}typedDomainRef'):
        if concept.isDimensionItem:
            typedDomainElement = concept.typedDomainElement
            if typedDomainElement is None:
                url, id = UrlUtil.splitDecodeFragment(concept.get('{http://xbrl.org/2005/xbrldt}typedDomainRef'))
                if len(id) == 0:
                    val.modelXbrl.error('xbrldte:TypedDimensionURIError', (_('Concept %(concept)s typedDomainRef has no fragment identifier')),
                      modelObject=concept,
                      concept=(concept.qname))
                else:
                    val.modelXbrl.error('xbrldte:OutOfDTSSchemaError', (_('Concept %(concept)s typedDomainRef is not resolved')),
                      modelObject=concept,
                      concept=(concept.qname))
            elif not isinstancetypedDomainElementModelConcept or not typedDomainElement.isGlobalDeclaration or typedDomainElement.abstract == 'true':
                val.modelXbrl.error('xbrldte:TypedDimensionError', (_('Concept %(concept)s typedDomainRef must identify a non-abstract element')),
                  modelObject=concept,
                  concept=(concept.qname))
        else:
            val.modelXbrl.error('xbrldte:TypedDomainRefError', (_('Concept %(concept)s is not a dimension item but has a typedDomainRef')),
              modelObject=concept,
              concept=(concept.qname))


def checkContext(val, cntx):

    def logDimAndFacts(modelDimValue):
        dimAndFacts = [
         modelDimValue]
        for f in val.modelXbrl.facts:
            if f.context == cntx:
                dimAndFacts.append(f)
                if len(dimAndFacts) > 10:
                    break

        return dimAndFacts

    for modelDimValues in (cntx.segDimValues.values(), cntx.scenDimValues.values(), cntx.errorDimValues):
        for modelDimValue in modelDimValues:
            dimensionConcept = modelDimValue.dimension
            if dimensionConcept is None or not dimensionConcept.isDimensionItem or modelDimValue.isTyped != (dimensionConcept.get('{http://xbrl.org/2005/xbrldt}typedDomainRef') is not None):
                val.modelXbrl.error(('xbrldie:TypedMemberNotTypedDimensionError' if modelDimValue.isTyped else 'xbrldie:ExplicitMemberNotExplicitDimensionError'), (_('Context %(contextID)s %(dimension)s %(value)s is not an appropriate dimension item')),
                  modelObject=(logDimAndFacts(modelDimValue)),
                  contextID=(cntx.id),
                  dimension=(modelDimValue.prefixedName),
                  value=(modelDimValue.dimensionQname),
                  messageCodes=('xbrldie:TypedMemberNotTypedDimensionError', 'xbrldie:ExplicitMemberNotExplicitDimensionError'))
            else:
                if modelDimValue.isTyped:
                    typedDomainConcept = dimensionConcept.typedDomainElement
                    problem = _('missing content')
                    for element in modelDimValue:
                        if isinstanceelementModelObject:
                            if problem is None:
                                problem = _('multiple contents')
                            else:
                                if typedDomainConcept is None:
                                    problem = _('Missing domain element schema definition for {0}').format(dimensionConcept.typedDomainRef)
                                else:
                                    if element.localName != typedDomainConcept.name or element.namespaceURI != typedDomainConcept.modelDocument.targetNamespace:
                                        problem = _('wrong content {0}').format(element.prefixedName)
                                    else:
                                        problem = None
                                        if val.validateEnum:
                                            if typedDomainConcept.isEnumeration:
                                                if getattrelement'xValid'0 == 4:
                                                    if element.get('{http://www.w3.org/2001/XMLSchema-instance}nil') not in ('true',
                                                                                                                             '1'):
                                                        qnEnums = element.xValue
                                                        if not isinstanceqnEnumslist:
                                                            qnEnums = (
                                                             qnEnums,)
                                                        if not all(enumerationMemberUsablevaltypedDomainConceptval.modelXbrl.qnameConcepts.get(qnEnum) for qnEnum in qnEnums):
                                                            val.modelXbrl.error('enum2ie:InvalidDimensionSetValue', (_('Dimension value %(dimensionMember)s context %(contextID)s enumeration %(value)s is not in the domain of %(concept)s')),
                                                              modelObject=element,
                                                              dimensionMember=(element.qname),
                                                              contextID=(cntx.id),
                                                              value=(element.xValue),
                                                              concept=(element.qname))
                                                        if len(qnEnums) > len(set(qnEnums)):
                                                            val.modelXbrl.error('enum2ie:RepeatedDimensionSetValue', (_('Dimension value %(dimensionMember)s context %(contextID)s enumeration has non-unique values %(value)s')),
                                                              modelObject=element,
                                                              dimensionMember=(element.qname),
                                                              contextID=(cntx.id),
                                                              value=(element.xValue),
                                                              concept=(element.qname))
                                            if any(qnEnum < qnEnums[i] for i, qnEnum in enumerate(qnEnums[1:])):
                                                val.modelXbrl.error('enum2ie:InvalidDimensionSetOrder', (_('Dimension value %(dimensionMember) context %(contextID)s enumeration is not in lexicographical order %(value)s')),
                                                  modelObject=element,
                                                  dimensionMember=(element.qname),
                                                  contextID=(cntx.id),
                                                  value=(element.xValue),
                                                  concept=(element.qname))

                    if problem:
                        val.modelXbrl.error('xbrldie:IllegalTypedDimensionContentError', (_('Context %(contextID)s typed dimension %(dimension)s has %(error)s')),
                          modelObject=(logDimAndFacts(modelDimValue)),
                          contextID=(cntx.id),
                          dimension=(modelDimValue.dimensionQname),
                          error=problem)
            if modelDimValue.isExplicit:
                memberConcept = modelDimValue.member
                if memberConcept is None or not memberConcept.isGlobalDeclaration:
                    val.modelXbrl.error('xbrldie:ExplicitMemberUndefinedQNameError', (_('Context %(contextID)s explicit dimension %(dimension)s member %(value)s is not a global member item')),
                      modelObject=(logDimAndFacts(modelDimValue)),
                      contextID=(cntx.id),
                      dimension=(modelDimValue.dimensionQname),
                      value=(modelDimValue.memberQname))
                elif val.modelXbrl.dimensionDefaultConcepts.get(dimensionConcept) == memberConcept:
                    val.modelXbrl.error('xbrldie:DefaultValueUsedInInstanceError', (_('Context %(contextID)s explicit dimension %(dimension)s member %(value)s is a default member item')),
                      modelObject=(logDimAndFacts(modelDimValue)),
                      contextID=(cntx.id),
                      dimension=(modelDimValue.dimensionQname),
                      value=(modelDimValue.memberQname))

    for modelDimValue in cntx.errorDimValues:
        dimensionConcept = modelDimValue.dimension
        if dimensionConcept is not None and (dimensionConcept in cntx.segDimValues or dimensionConcept in cntx.scenDimValues):
            val.modelXbrl.error('xbrldie:RepeatedDimensionInInstanceError', (_('Context %(contextID)s dimension %(dimension)s is a repeated dimension value')),
              modelObject=(logDimAndFacts(modelDimValue)),
              contextID=(cntx.id),
              dimension=(modelDimValue.dimensionQname))

    for modelDimValue in cntx.segDimValues.values():
        dimensionConcept = modelDimValue.dimension
        if dimensionConcept is not None and dimensionConcept in cntx.scenDimValues:
            val.modelXbrl.error('xbrldie:RepeatedDimensionInInstanceError', (_('Context %(contextID)s dimension %(dimension)s is a repeated dimension value')),
              modelObject=(logDimAndFacts(modelDimValue)),
              contextID=(cntx.id),
              dimension=(modelDimValue.dimensionQname))


def checkFact(val, f, otherFacts=None):
    if not isFactDimensionallyValidvalfotherFacts:
        val.modelXbrl.error('xbrldie:PrimaryItemDimensionallyInvalidError', (_('Fact %(fact)s context %(contextID)s dimensionally not valid')),
          modelObject=f,
          fact=(f.qname),
          contextID=(f.context.id))


def isFactDimensionallyValid(val, f, setPrototypeContextElements=False, otherFacts=None):
    hasElrHc = False
    for ELR, hcRels in priItemElrHcRelsvalf.concept.items():
        hasElrHc = True
        if checkFactElrHcs(val, f, ELR, hcRels, setPrototypeContextElements):
            return True

    if hasElrHc:
        return False
    else:
        return True


def priItemElrHcRels(val, priItem, ELR=None):
    key = (priItem, ELR)
    try:
        priItemElrHcRels = val.priItemElrHcRels
    except AttributeError:
        priItemElrHcRels = val.priItemElrHcRels = {}

    try:
        return priItemElrHcRels[key]
    except KeyError:
        rels = priItemElrHcRels[key] = findPriItemElrHcRelsvalpriItemELR
        return rels


def findPriItemElrHcRels(val, priItem, ELR=None, elrHcRels=None):
    if elrHcRels is None:
        elrHcRels = defaultdict(list)
    for arcrole in (XbrlConst.all, XbrlConst.notAll):
        for hasHcRel in val.modelXbrl.relationshipSetarcroleELR.fromModelObject(priItem):
            elrHcRels[hasHcRel.linkrole].append(hasHcRel)

    for domMbrRel in val.modelXbrl.relationshipSet(XbrlConst.domainMember).toModelObject(priItem):
        relLinkrole = domMbrRel.linkrole
        toELR = domMbrRel.targetRole or relLinkrole
        if ELR is None or ELR == toELR:
            findPriItemElrHcRels(val, domMbrRel.fromModelObject, relLinkrole, elrHcRels)

    return elrHcRels


def priItemsOfElrHc(val, priItem, hcELR, relELR, priItems=None):
    if priItems is None:
        priItems = set(priItem)
    for domMbrRel in val.modelXbrl.relationshipSetXbrlConst.domainMemberrelELR.fromModelObject(priItem):
        toPriItem = domMbrRel.toModelObject
        linkrole = domMbrRel.consecutiveLinkrole
        if linkrole == hcELR:
            priItems.add(toPriItem)
        priItemsOfElrHc(val, toPriItem, hcELR, linkrole, priItems)

    return priItems


NOT_FOUND = 0
MEMBER_USABLE = 1
MEMBER_NOT_USABLE = 2

def checkFactElrHcs(val, f, ELR, hcRels, setPrototypeContextElements=False):
    context = f.context
    elrValid = True
    for hasHcRel in hcRels:
        hcConcept = hasHcRel.toModelObject
        hcIsClosed = hasHcRel.isClosed
        hcContextElement = hasHcRel.contextElement
        hcNegating = hasHcRel.arcrole == XbrlConst.notAll
        modelDimValues = context.dimValues(hcContextElement)
        if setPrototypeContextElements:
            if isinstancecontextContextPrototype:
                oppositeContextDimValues = context.dimValues(hcContextElement, oppositeContextElement=True)
        else:
            contextElementDimSet = set(modelDimValues.keys())
            modelNonDimValues = context.nonDimValues(hcContextElement)
            hcValid = True
            if hcIsClosed and len(modelNonDimValues) > 0:
                hcValid = False
            else:
                dimELR = hasHcRel.targetRole or ELR
                for hcDimRel in val.modelXbrl.relationshipSetXbrlConst.hypercubeDimensiondimELR.fromModelObject(hcConcept):
                    dimConcept = hcDimRel.toModelObject
                    if isinstancedimConceptModelConcept:
                        domELR = hcDimRel.targetRole or dimELR
                        if dimConcept in modelDimValues:
                            memModelDimension = modelDimValues[dimConcept]
                            contextElementDimSet.discard(dimConcept)
                            memConcept = memModelDimension.member
                        else:
                            if dimConcept in val.modelXbrl.dimensionDefaultConcepts:
                                memConcept = val.modelXbrl.dimensionDefaultConcepts[dimConcept]
                                memModelDimension = None
                            elif setPrototypeContextElements:
                                if isinstancecontextContextPrototype:
                                    if dimConcept in oppositeContextDimValues:
                                        memModelDimension = oppositeContextDimValues[dimConcept]
                                        memConcept = memModelDimension.member
                            else:
                                hcValid = False
                                continue
                    if not dimConcept.isTypedDimension:
                        if not dimensionMemberUsable(val, dimConcept, memConcept, domELR):
                            hcValid = False
                        if hcValid and setPrototypeContextElements and isinstancememModelDimensionDimValuePrototype and not hcNegating:
                            memModelDimension.contextElement = hcContextElement

        if hcIsClosed:
            if len(contextElementDimSet) > 0:
                hcValid = False
            elif setPrototypeContextElements:
                if isinstancecontextContextPrototype:
                    if hcValid:
                        if not hcNegating:
                            for memModelDimension in modelDimValues.values():
                                if memModelDimension.contextElement != hcContextElement:
                                    memModelDimension.contextElement = hcContextElement

                            if len(oppositeContextDimValues) > 0:
                                for memModelDimension in oppositeContextDimValues.values():
                                    if memModelDimension.contextElement != hcContextElement:
                                        memModelDimension.contextElement = hcContextElement

            if hcNegating:
                hcValid = not hcValid
            if not hcValid:
                elrValid = False

    return elrValid


def dimensionMemberUsable(val, dimConcept, memConcept, domELR):
    try:
        dimensionMembersUsable = val.dimensionMembersUsable
    except AttributeError:
        dimensionMembersUsable = val.dimensionMembersUsable = {}

    key = (
     dimConcept, domELR)
    try:
        return memConcept in dimensionMembersUsable[key]
    except KeyError:
        usableMembers = set()
        unusableMembers = set()
        dimensionMembersUsable[key] = usableMembers
        findUsableMembersInDomainELR(val, val.modelXbrl.relationshipSetXbrlConst.dimensionDomaindomELR.fromModelObject(dimConcept), domELR, usableMembers, unusableMembers, defaultdict(set))
        usableMembers -= unusableMembers
        return memConcept in usableMembers


def findUsableMembersInDomainELR(val, rels, ELR, usableMembers, unusableMembers, toConceptELRs):
    for rel in rels:
        toConcept = rel.toModelObject
        if rel.isUsable:
            usableMembers.add(toConcept)
        else:
            unusableMembers.add(toConcept)
        toELR = rel.targetRole or ELR
        toELRs = toConceptELRs[toConcept]
        if toELR not in toELRs:
            toELRs.add(toELR)
            domMbrRels = val.modelXbrl.relationshipSetXbrlConst.domainMembertoELR.fromModelObject(toConcept)
            findUsableMembersInDomainELR(val, domMbrRels, toELR, usableMembers, unusableMembers, toConceptELRs)
            toELRs.discard(toELR)


def usableEnumerationMembers(val, enumConcept):
    if enumConcept is None:
        return set()
    try:
        enumerationMembersUsable = val.enumerationMembersUsable
    except AttributeError:
        enumerationMembersUsable = val.enumerationMembersUsable = {}

    try:
        return enumerationMembersUsable[enumConcept]
    except KeyError:
        domConcept = enumConcept.enumDomain
        usableMembers = set()
        unusableMembers = set()
        enumerationMembersUsable[enumConcept] = usableMembers
        if domConcept is None:
            usableMembers = set()
            return usableMembers
        if enumConcept.isEnumDomainUsable:
            usableMembers.add(domConcept)
        domELR = enumConcept.enumLinkrole
        findUsableMembersInDomainELR(val, val.modelXbrl.relationshipSetXbrlConst.domainMemberdomELR.fromModelObject(domConcept), domELR, usableMembers, unusableMembers, defaultdict(set))
        usableMembers -= unusableMembers
        return usableMembers


def enumerationMemberUsable(val, enumConcept, memConcept):
    if enumConcept is None or memConcept is None:
        return False
    else:
        return memConcept in usableEnumerationMembersvalenumConcept