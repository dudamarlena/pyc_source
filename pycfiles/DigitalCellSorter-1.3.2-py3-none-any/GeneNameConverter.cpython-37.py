# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\A_DCS\VS\DigitalCellSorter\DigitalCellSorter\GeneNameConverter.py
# Compiled at: 2019-10-25 14:33:06
# Size of source mod 2**32: 11141 bytes
"""
Spyder Editor

This is a temporary script file.
"""
import mygene, pickle

class GeneNameConverter:

    def __init__(self, dictDir=None, jumpStart=True):
        if dictDir is None:
            self.dictDir = 'pickledGeneConverterDict/ensembl_hugo_entrez_alias_dict.pythdat'
        else:
            self.dictDir = dictDir
        try:
            self.conversionDict = self.Load(self.dictDir)
        except IOError:
            self.conversionDict = {'hugo':{'entrez':{},  'ensembl':{},  'alias':{}},  'entrez':{'hugo':{},  'ensembl':{},  'retired':{}},  'ensembl':{'entrez':{},  'hugo':{}},  'alias':{'hugo':{},  'entrez':{},  'ensembl':{}},  'retired':{'entrez': {}}}
            for sourceType in ('hugo', 'alias', 'entrez', 'ensembl', 'retired'):
                self.conversionDict[sourceType]['known'] = set()
                self.conversionDict[sourceType]['unknown'] = set()

            if jumpStart:
                try:
                    self.JumpStart()
                except IOError:
                    pass

            else:
                self.Save(self.conversionDict, self.dictDir)

    def JumpStart(self):
        import pandas as pd
        self.Convert(pd.read_csv('seedGenes/genes_ensembl.txt').values.flatten().tolist(), 'ensembl', 'entrez')
        self.Convert(pd.read_csv('seedGenes/genes_entrez.txt').values.flatten().tolist(), 'retired', 'entrez')
        self.Convert(pd.read_csv('seedGenes/genes_hugo.txt').values.flatten().tolist(), 'alias', 'entrez')

    def Convert--- This code section failed: ---

 L.  62         0  LOAD_BUILD_CLASS 
                2  LOAD_CODE                <code_object MyTypeError>
                4  LOAD_STR                 'MyTypeError'
                6  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                8  LOAD_STR                 'MyTypeError'
               10  LOAD_GLOBAL              Exception
               12  CALL_FUNCTION_3       3  '3 positional arguments'
               14  STORE_FAST               'MyTypeError'

 L.  63        16  LOAD_CONST               False
               18  STORE_FAST               'returnFlatFlag'

 L.  64        20  LOAD_GLOBAL              type
               22  LOAD_FAST                'genes'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  LOAD_GLOBAL              list
               28  COMPARE_OP               is-not
               30  POP_JUMP_IF_FALSE   112  'to 112'
               32  LOAD_GLOBAL              type
               34  LOAD_FAST                'genes'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  LOAD_GLOBAL              tuple
               40  COMPARE_OP               is-not
               42  POP_JUMP_IF_FALSE   112  'to 112'

 L.  65        44  LOAD_GLOBAL              type
               46  LOAD_FAST                'genes'
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  LOAD_GLOBAL              int
               52  COMPARE_OP               is
               54  POP_JUMP_IF_TRUE     92  'to 92'
               56  LOAD_GLOBAL              type
               58  LOAD_FAST                'genes'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  LOAD_GLOBAL              long
               64  COMPARE_OP               is
               66  POP_JUMP_IF_TRUE     92  'to 92'
               68  LOAD_GLOBAL              type
               70  LOAD_FAST                'genes'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  LOAD_GLOBAL              str
               76  COMPARE_OP               is
               78  POP_JUMP_IF_TRUE     92  'to 92'
               80  LOAD_GLOBAL              type
               82  LOAD_FAST                'genes'
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  LOAD_GLOBAL              unicode
               88  COMPARE_OP               is
               90  POP_JUMP_IF_FALSE   104  'to 104'
             92_0  COME_FROM            78  '78'
             92_1  COME_FROM            66  '66'
             92_2  COME_FROM            54  '54'

 L.  66        92  LOAD_FAST                'genes'
               94  BUILD_LIST_1          1 
               96  STORE_FAST               'genes'

 L.  67        98  LOAD_CONST               True
              100  STORE_FAST               'returnFlatFlag'
              102  JUMP_FORWARD        112  'to 112'
            104_0  COME_FROM            90  '90'

 L.  69       104  LOAD_FAST                'MyTypeError'
              106  LOAD_STR                 'The only currently supported input types for "genes" are list, tuple, int, long, string, and unicode'
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM           102  '102'
            112_1  COME_FROM            42  '42'
            112_2  COME_FROM            30  '30'

 L.  71       112  LOAD_FAST                'onlineSearch'
              114  POP_JUMP_IF_FALSE   200  'to 200'

 L.  72       116  LOAD_GLOBAL              set
              118  LOAD_FAST                'genes'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  LOAD_METHOD              difference
              124  LOAD_DEREF               'self'
              126  LOAD_ATTR                conversionDict
              128  LOAD_DEREF               'sourceType'
              130  BINARY_SUBSCR    
              132  LOAD_DEREF               'targetType'
              134  BINARY_SUBSCR    
              136  LOAD_METHOD              keys
              138  CALL_METHOD_0         0  '0 positional arguments'
              140  CALL_METHOD_1         1  '1 positional argument'
              142  STORE_FAST               'genesToFetch'

 L.  73       144  LOAD_FAST                'aggressiveSearch'
              146  LOAD_CONST               False
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   172  'to 172'

 L.  74       152  LOAD_FAST                'genesToFetch'
              154  LOAD_METHOD              difference
              156  LOAD_DEREF               'self'
              158  LOAD_ATTR                conversionDict
              160  LOAD_DEREF               'sourceType'
              162  BINARY_SUBSCR    
              164  LOAD_STR                 'unknown'
              166  BINARY_SUBSCR    
              168  CALL_METHOD_1         1  '1 positional argument'
              170  STORE_FAST               'genesToFetch'
            172_0  COME_FROM           150  '150'

 L.  75       172  LOAD_GLOBAL              len
              174  LOAD_FAST                'genesToFetch'
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  LOAD_CONST               0
              180  COMPARE_OP               >
              182  POP_JUMP_IF_FALSE   200  'to 200'

 L.  76       184  LOAD_DEREF               'self'
              186  LOAD_METHOD              Fetch
              188  LOAD_GLOBAL              list
              190  LOAD_FAST                'genesToFetch'
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  LOAD_DEREF               'sourceType'
              196  CALL_METHOD_2         2  '2 positional arguments'
              198  POP_TOP          
            200_0  COME_FROM           182  '182'
            200_1  COME_FROM           114  '114'

 L.  78       200  LOAD_GLOBAL              set
              202  LOAD_DEREF               'self'
              204  LOAD_ATTR                conversionDict
              206  LOAD_DEREF               'sourceType'
              208  BINARY_SUBSCR    
              210  LOAD_DEREF               'targetType'
              212  BINARY_SUBSCR    
              214  LOAD_METHOD              keys
              216  CALL_METHOD_0         0  '0 positional arguments'
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  STORE_DEREF              'geneSet'

 L.  80       222  LOAD_FAST                'returnUnknownString'
              224  POP_JUMP_IF_FALSE   252  'to 252'

 L.  81       226  LOAD_CLOSURE             'geneSet'
              228  LOAD_CLOSURE             'self'
              230  LOAD_CLOSURE             'sourceType'
              232  LOAD_CLOSURE             'targetType'
              234  BUILD_TUPLE_4         4 
              236  LOAD_LISTCOMP            '<code_object <listcomp>>'
              238  LOAD_STR                 'GeneNameConverter.Convert.<locals>.<listcomp>'
              240  MAKE_FUNCTION_8          'closure'

 L.  84       242  LOAD_FAST                'genes'
              244  GET_ITER         
              246  CALL_FUNCTION_1       1  '1 positional argument'
              248  STORE_FAST               'genes_converted'
              250  JUMP_FORWARD        276  'to 276'
            252_0  COME_FROM           224  '224'

 L.  86       252  LOAD_CLOSURE             'geneSet'
              254  LOAD_CLOSURE             'self'
              256  LOAD_CLOSURE             'sourceType'
              258  LOAD_CLOSURE             'targetType'
              260  BUILD_TUPLE_4         4 
              262  LOAD_LISTCOMP            '<code_object <listcomp>>'
              264  LOAD_STR                 'GeneNameConverter.Convert.<locals>.<listcomp>'
              266  MAKE_FUNCTION_8          'closure'

 L.  89       268  LOAD_FAST                'genes'
              270  GET_ITER         
              272  CALL_FUNCTION_1       1  '1 positional argument'
              274  STORE_FAST               'genes_converted'
            276_0  COME_FROM           250  '250'

 L.  91       276  LOAD_FAST                'returnFlatFlag'
          278_280  POP_JUMP_IF_FALSE   290  'to 290'

 L.  91       282  LOAD_FAST                'genes_converted'
              284  LOAD_CONST               0
              286  BINARY_SUBSCR    
              288  RETURN_VALUE     
            290_0  COME_FROM           278  '278'

 L.  92       290  LOAD_FAST                'genes_converted'
              292  RETURN_VALUE     

Parse error at or near `JUMP_FORWARD' instruction at offset 102

    def Fetch--- This code section failed: ---

 L.  99         0  LOAD_STR                 'human'
                2  LOAD_STR                 'ensembl.gene'
                4  LOAD_STR                 'entrezgene'
                6  LOAD_STR                 'symbol'
                8  LOAD_STR                 'alias'
               10  LOAD_STR                 'retired'
               12  BUILD_LIST_5          5 
               14  LOAD_CONST               ('species', 'fields')
               16  BUILD_CONST_KEY_MAP_2     2 
               18  STORE_FAST               'kwargs'

 L. 100        20  LOAD_FAST                'sourceType'
               22  LOAD_STR                 'entrez'
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_TRUE     36  'to 36'
               28  LOAD_FAST                'sourceType'
               30  LOAD_STR                 'retired'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    88  'to 88'
             36_0  COME_FROM            26  '26'

 L. 101        36  LOAD_CONST               ('entrezgene', 'retired')
               38  LOAD_FAST                'kwargs'
               40  LOAD_STR                 'scopes'
               42  STORE_SUBSCR     

 L. 102        44  SETUP_LOOP          230  'to 230'
               46  LOAD_FAST                'genes'
               48  GET_ITER         
             50_0  COME_FROM            76  '76'
             50_1  COME_FROM            64  '64'
               50  FOR_ITER             84  'to 84'
               52  STORE_FAST               'gene'

 L. 103        54  LOAD_GLOBAL              type
               56  LOAD_FAST                'gene'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  LOAD_GLOBAL              int
               62  COMPARE_OP               is
               64  POP_JUMP_IF_TRUE     50  'to 50'
               66  LOAD_GLOBAL              type
               68  LOAD_FAST                'gene'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  LOAD_GLOBAL              long
               74  COMPARE_OP               is
               76  POP_JUMP_IF_TRUE     50  'to 50'
               78  LOAD_GLOBAL              AssertionError
               80  RAISE_VARARGS_1       1  'exception instance'
               82  JUMP_BACK            50  'to 50'
               84  POP_BLOCK        
               86  JUMP_FORWARD        230  'to 230'
             88_0  COME_FROM            34  '34'

 L. 104        88  LOAD_FAST                'sourceType'
               90  LOAD_STR                 'ensembl'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   156  'to 156'

 L. 105        96  LOAD_STR                 'ensembl.gene'
               98  LOAD_FAST                'kwargs'
              100  LOAD_STR                 'scopes'
              102  STORE_SUBSCR     

 L. 106       104  SETUP_LOOP          230  'to 230'
              106  LOAD_FAST                'genes'
              108  GET_ITER         
            110_0  COME_FROM           144  '144'
              110  FOR_ITER            152  'to 152'
              112  STORE_FAST               'gene'

 L. 107       114  LOAD_GLOBAL              type
              116  LOAD_FAST                'gene'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  LOAD_GLOBAL              str
              122  COMPARE_OP               is
              124  POP_JUMP_IF_TRUE    130  'to 130'
              126  LOAD_ASSERT              AssertionError
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM           124  '124'

 L. 108       130  LOAD_FAST                'gene'
              132  LOAD_CONST               None
              134  LOAD_CONST               4
              136  BUILD_SLICE_2         2 
              138  BINARY_SUBSCR    
              140  LOAD_STR                 'ENSG'
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_TRUE    110  'to 110'
              146  LOAD_GLOBAL              AssertionError
              148  RAISE_VARARGS_1       1  'exception instance'
              150  JUMP_BACK           110  'to 110'
              152  POP_BLOCK        
              154  JUMP_FORWARD        230  'to 230'
            156_0  COME_FROM            94  '94'

 L. 109       156  LOAD_FAST                'sourceType'
              158  LOAD_STR                 'hugo'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_TRUE    172  'to 172'
              164  LOAD_FAST                'sourceType'
              166  LOAD_STR                 'alias'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   230  'to 230'
            172_0  COME_FROM           162  '162'

 L. 110       172  LOAD_CONST               ('symbol', 'alias')
              174  LOAD_FAST                'kwargs'
              176  LOAD_STR                 'scopes'
              178  STORE_SUBSCR     

 L. 111       180  SETUP_LOOP          230  'to 230'
              182  LOAD_FAST                'genes'
              184  GET_ITER         
            186_0  COME_FROM           220  '220'
              186  FOR_ITER            228  'to 228'
              188  STORE_FAST               'gene'

 L. 112       190  LOAD_GLOBAL              type
              192  LOAD_FAST                'gene'
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  LOAD_GLOBAL              str
              198  COMPARE_OP               is
              200  POP_JUMP_IF_TRUE    206  'to 206'
              202  LOAD_ASSERT              AssertionError
              204  RAISE_VARARGS_1       1  'exception instance'
            206_0  COME_FROM           200  '200'

 L. 113       206  LOAD_FAST                'gene'
              208  LOAD_CONST               None
              210  LOAD_CONST               4
              212  BUILD_SLICE_2         2 
              214  BINARY_SUBSCR    
              216  LOAD_STR                 'ENSG'
              218  COMPARE_OP               !=
              220  POP_JUMP_IF_TRUE    186  'to 186'
              222  LOAD_GLOBAL              AssertionError
              224  RAISE_VARARGS_1       1  'exception instance'
              226  JUMP_BACK           186  'to 186'
              228  POP_BLOCK        
            230_0  COME_FROM_LOOP      180  '180'
            230_1  COME_FROM           170  '170'
            230_2  COME_FROM           154  '154'
            230_3  COME_FROM_LOOP      104  '104'
            230_4  COME_FROM            86  '86'
            230_5  COME_FROM_LOOP       44  '44'

 L. 115       230  LOAD_GLOBAL              set
              232  LOAD_FAST                'genes'
              234  CALL_FUNCTION_1       1  '1 positional argument'
              236  STORE_FAST               'genesSet'

 L. 116       238  LOAD_GLOBAL              mygene
              240  LOAD_METHOD              MyGeneInfo
              242  CALL_METHOD_0         0  '0 positional arguments'
              244  LOAD_ATTR                querymany
              246  LOAD_FAST                'genes'
              248  BUILD_TUPLE_1         1 
              250  LOAD_FAST                'kwargs'
              252  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              254  STORE_FAST               'queryList'

 L. 119   256_258  SETUP_LOOP         1300  'to 1300'
              260  LOAD_GLOBAL              zip
              262  LOAD_FAST                'queryList'
              264  LOAD_FAST                'genes'
              266  CALL_FUNCTION_2       2  '2 positional arguments'
              268  GET_ITER         
            270_0  COME_FROM          1178  '1178'
          270_272  FOR_ITER           1298  'to 1298'
              274  UNPACK_SEQUENCE_2     2 
              276  STORE_FAST               'q'
              278  STORE_FAST               'gene'

 L. 121       280  LOAD_STR                 'notfound'
              282  LOAD_FAST                'q'
              284  LOAD_METHOD              keys
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  COMPARE_OP               in
          290_292  POP_JUMP_IF_FALSE   318  'to 318'

 L. 122       294  LOAD_FAST                'self'
              296  LOAD_ATTR                conversionDict
              298  LOAD_FAST                'sourceType'
              300  BINARY_SUBSCR    
              302  LOAD_STR                 'unknown'
              304  BINARY_SUBSCR    
              306  LOAD_METHOD              add
              308  LOAD_FAST                'gene'
              310  CALL_METHOD_1         1  '1 positional argument'
              312  POP_TOP          
          314_316  JUMP_BACK           270  'to 270'
            318_0  COME_FROM           290  '290'

 L. 126       318  SETUP_EXCEPT        414  'to 414'

 L. 127       320  LOAD_FAST                'q'
              322  LOAD_STR                 'entrezgene'
              324  BINARY_SUBSCR    
              326  STORE_FAST               'entrez'

 L. 128       328  SETUP_EXCEPT        382  'to 382'

 L. 129       330  LOAD_FAST                'q'
              332  LOAD_STR                 'retired'
              334  BINARY_SUBSCR    
              336  STORE_FAST               'retireds'

 L. 130       338  LOAD_GLOBAL              type
              340  LOAD_FAST                'retireds'
              342  CALL_FUNCTION_1       1  '1 positional argument'
              344  LOAD_GLOBAL              int
              346  COMPARE_OP               is
          348_350  POP_JUMP_IF_FALSE   360  'to 360'

 L. 131       352  LOAD_FAST                'retireds'
              354  BUILD_LIST_1          1 
              356  STORE_FAST               'retireds'
              358  JUMP_FORWARD        368  'to 368'
            360_0  COME_FROM           348  '348'

 L. 133       360  LOAD_GLOBAL              list
              362  LOAD_FAST                'retireds'
              364  CALL_FUNCTION_1       1  '1 positional argument'
              366  STORE_FAST               'retireds'
            368_0  COME_FROM           358  '358'

 L. 134       368  LOAD_FAST                'retireds'
              370  LOAD_METHOD              append
              372  LOAD_FAST                'entrez'
              374  CALL_METHOD_1         1  '1 positional argument'
              376  POP_TOP          
              378  POP_BLOCK        
              380  JUMP_FORWARD        410  'to 410'
            382_0  COME_FROM_EXCEPT    328  '328'

 L. 135       382  DUP_TOP          
              384  LOAD_GLOBAL              KeyError
              386  COMPARE_OP               exception-match
          388_390  POP_JUMP_IF_FALSE   408  'to 408'
              392  POP_TOP          
              394  POP_TOP          
              396  POP_TOP          

 L. 136       398  LOAD_FAST                'entrez'
              400  BUILD_LIST_1          1 
              402  STORE_FAST               'retireds'
              404  POP_EXCEPT       
              406  JUMP_FORWARD        410  'to 410'
            408_0  COME_FROM           388  '388'
              408  END_FINALLY      
            410_0  COME_FROM           406  '406'
            410_1  COME_FROM           380  '380'
              410  POP_BLOCK        
              412  JUMP_FORWARD        444  'to 444'
            414_0  COME_FROM_EXCEPT    318  '318'

 L. 137       414  DUP_TOP          
              416  LOAD_GLOBAL              KeyError
              418  COMPARE_OP               exception-match
          420_422  POP_JUMP_IF_FALSE   442  'to 442'
              424  POP_TOP          
              426  POP_TOP          
              428  POP_TOP          

 L. 138       430  LOAD_CONST               None
              432  STORE_FAST               'entrez'

 L. 139       434  BUILD_LIST_0          0 
              436  STORE_FAST               'retireds'
              438  POP_EXCEPT       
              440  JUMP_FORWARD        444  'to 444'
            442_0  COME_FROM           420  '420'
              442  END_FINALLY      
            444_0  COME_FROM           440  '440'
            444_1  COME_FROM           412  '412'

 L. 140       444  SETUP_EXCEPT        458  'to 458'

 L. 140       446  LOAD_FAST                'q'
              448  LOAD_STR                 'symbol'
              450  BINARY_SUBSCR    
              452  STORE_FAST               'hugo'
              454  POP_BLOCK        
              456  JUMP_FORWARD        484  'to 484'
            458_0  COME_FROM_EXCEPT    444  '444'

 L. 141       458  DUP_TOP          
              460  LOAD_GLOBAL              KeyError
              462  COMPARE_OP               exception-match
          464_466  POP_JUMP_IF_FALSE   482  'to 482'
              468  POP_TOP          
              470  POP_TOP          
              472  POP_TOP          

 L. 141       474  LOAD_CONST               None
              476  STORE_FAST               'hugo'
              478  POP_EXCEPT       
              480  JUMP_FORWARD        484  'to 484'
            482_0  COME_FROM           464  '464'
              482  END_FINALLY      
            484_0  COME_FROM           480  '480'
            484_1  COME_FROM           456  '456'

 L. 142       484  LOAD_GLOBAL              str
              486  LOAD_FAST                'q'
              488  LOAD_STR                 'query'
              490  BINARY_SUBSCR    
              492  CALL_FUNCTION_1       1  '1 positional argument'
              494  LOAD_CONST               None
              496  LOAD_CONST               4
              498  BUILD_SLICE_2         2 
              500  BINARY_SUBSCR    
              502  LOAD_STR                 'ENSG'
              504  COMPARE_OP               ==
          506_508  POP_JUMP_IF_FALSE   526  'to 526'

 L. 143       510  LOAD_FAST                'q'
              512  LOAD_STR                 'query'
              514  BINARY_SUBSCR    
              516  STORE_FAST               'ensembl'

 L. 144       518  LOAD_FAST                'ensembl'
              520  BUILD_TUPLE_1         1 
              522  STORE_FAST               'ensembl_list'
              524  JUMP_FORWARD        634  'to 634'
            526_0  COME_FROM           506  '506'

 L. 146       526  SETUP_EXCEPT        604  'to 604'

 L. 147       528  LOAD_FAST                'q'
              530  LOAD_STR                 'ensembl'
              532  BINARY_SUBSCR    
              534  STORE_FAST               'ensembl'

 L. 148       536  LOAD_GLOBAL              type
              538  LOAD_FAST                'ensembl'
              540  CALL_FUNCTION_1       1  '1 positional argument'
              542  LOAD_GLOBAL              dict
              544  COMPARE_OP               ==
          546_548  POP_JUMP_IF_FALSE   558  'to 558'

 L. 149       550  LOAD_FAST                'ensembl'
              552  LOAD_STR                 'gene'
              554  BINARY_SUBSCR    
              556  STORE_FAST               'ensembl'
            558_0  COME_FROM           546  '546'

 L. 150       558  LOAD_GLOBAL              type
              560  LOAD_FAST                'ensembl'
              562  CALL_FUNCTION_1       1  '1 positional argument'
              564  LOAD_GLOBAL              list
              566  COMPARE_OP               ==
          568_570  POP_JUMP_IF_FALSE   596  'to 596'

 L. 151       572  LOAD_LISTCOMP            '<code_object <listcomp>>'
              574  LOAD_STR                 'GeneNameConverter.Fetch.<locals>.<listcomp>'
              576  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              578  LOAD_FAST                'ensembl'
              580  GET_ITER         
              582  CALL_FUNCTION_1       1  '1 positional argument'
              584  STORE_FAST               'ensembl_list'

 L. 152       586  LOAD_FAST                'ensembl_list'
              588  LOAD_CONST               0
              590  BINARY_SUBSCR    
              592  STORE_FAST               'ensembl'
              594  JUMP_FORWARD        600  'to 600'
            596_0  COME_FROM           568  '568'

 L. 154       596  LOAD_CONST               ()
              598  STORE_FAST               'ensembl_list'
            600_0  COME_FROM           594  '594'
              600  POP_BLOCK        
              602  JUMP_FORWARD        634  'to 634'
            604_0  COME_FROM_EXCEPT    526  '526'

 L. 156       604  DUP_TOP          
              606  LOAD_GLOBAL              KeyError
              608  COMPARE_OP               exception-match
          610_612  POP_JUMP_IF_FALSE   632  'to 632'
              614  POP_TOP          
              616  POP_TOP          
              618  POP_TOP          

 L. 157       620  LOAD_CONST               None
              622  STORE_FAST               'ensembl'

 L. 158       624  LOAD_CONST               ()
              626  STORE_FAST               'ensembl_list'
              628  POP_EXCEPT       
              630  JUMP_FORWARD        634  'to 634'
            632_0  COME_FROM           610  '610'
              632  END_FINALLY      
            634_0  COME_FROM           630  '630'
            634_1  COME_FROM           602  '602'
            634_2  COME_FROM           524  '524'

 L. 159       634  SETUP_EXCEPT        690  'to 690'

 L. 160       636  LOAD_FAST                'q'
              638  LOAD_STR                 'alias'
              640  BINARY_SUBSCR    
              642  STORE_FAST               'aliases'

 L. 161       644  LOAD_GLOBAL              type
              646  LOAD_FAST                'aliases'
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  LOAD_GLOBAL              list
              652  COMPARE_OP               !=
          654_656  POP_JUMP_IF_FALSE   664  'to 664'

 L. 161       658  LOAD_FAST                'aliases'
              660  BUILD_LIST_1          1 
              662  STORE_FAST               'aliases'
            664_0  COME_FROM           654  '654'

 L. 162       664  LOAD_FAST                'aliases'
              666  LOAD_METHOD              append
              668  LOAD_FAST                'hugo'
              670  CALL_METHOD_1         1  '1 positional argument'
              672  POP_TOP          

 L. 163       674  LOAD_GLOBAL              tuple
              676  LOAD_GLOBAL              set
              678  LOAD_FAST                'aliases'
              680  CALL_FUNCTION_1       1  '1 positional argument'
              682  CALL_FUNCTION_1       1  '1 positional argument'
              684  STORE_FAST               'aliases'
              686  POP_BLOCK        
              688  JUMP_FORWARD        716  'to 716'
            690_0  COME_FROM_EXCEPT    634  '634'

 L. 164       690  DUP_TOP          
              692  LOAD_GLOBAL              KeyError
              694  COMPARE_OP               exception-match
          696_698  POP_JUMP_IF_FALSE   714  'to 714'
              700  POP_TOP          
              702  POP_TOP          
              704  POP_TOP          

 L. 164       706  LOAD_CONST               ()
              708  STORE_FAST               'aliases'
              710  POP_EXCEPT       
              712  JUMP_FORWARD        716  'to 716'
            714_0  COME_FROM           696  '696'
              714  END_FINALLY      
            716_0  COME_FROM           712  '712'
            716_1  COME_FROM           688  '688'

 L. 167       716  SETUP_LOOP          910  'to 910'
              718  LOAD_GLOBAL              zip
              720  LOAD_STR                 'entrez'
              722  LOAD_STR                 'hugo'
              724  LOAD_STR                 'ensembl'
              726  BUILD_LIST_3          3 
              728  LOAD_FAST                'entrez'
              730  LOAD_FAST                'hugo'
              732  LOAD_FAST                'ensembl'
              734  BUILD_LIST_3          3 
              736  CALL_FUNCTION_2       2  '2 positional arguments'
              738  GET_ITER         
              740  FOR_ITER            908  'to 908'
              742  UNPACK_SEQUENCE_2     2 
              744  STORE_FAST               'source'
              746  STORE_FAST               'sourceGene'

 L. 168       748  SETUP_LOOP          904  'to 904'
              750  LOAD_GLOBAL              zip
              752  LOAD_STR                 'entrez'
              754  LOAD_STR                 'hugo'
              756  LOAD_STR                 'ensembl'
              758  BUILD_LIST_3          3 
              760  LOAD_FAST                'entrez'
              762  LOAD_FAST                'hugo'
              764  LOAD_FAST                'ensembl'
              766  BUILD_LIST_3          3 
              768  CALL_FUNCTION_2       2  '2 positional arguments'
              770  GET_ITER         
            772_0  COME_FROM           876  '876'
            772_1  COME_FROM           866  '866'
            772_2  COME_FROM           856  '856'
              772  FOR_ITER            902  'to 902'
              774  UNPACK_SEQUENCE_2     2 
              776  STORE_FAST               'target'
              778  STORE_FAST               'targetGene'

 L. 169       780  LOAD_FAST                'source'
              782  LOAD_CONST               None
              784  COMPARE_OP               is-not
          786_788  POP_JUMP_IF_FALSE   850  'to 850'

 L. 170       790  LOAD_FAST                'self'
              792  LOAD_ATTR                conversionDict
              794  LOAD_FAST                'source'
              796  BINARY_SUBSCR    
              798  LOAD_STR                 'known'
              800  BINARY_SUBSCR    
              802  LOAD_METHOD              add
              804  LOAD_FAST                'sourceGene'
              806  CALL_METHOD_1         1  '1 positional argument'
              808  POP_TOP          

 L. 171       810  LOAD_FAST                'sourceGene'
              812  LOAD_FAST                'self'
              814  LOAD_ATTR                conversionDict
              816  LOAD_FAST                'source'
              818  BINARY_SUBSCR    
              820  LOAD_STR                 'unknown'
              822  BINARY_SUBSCR    
              824  COMPARE_OP               in
          826_828  POP_JUMP_IF_FALSE   850  'to 850'

 L. 172       830  LOAD_FAST                'self'
              832  LOAD_ATTR                conversionDict
              834  LOAD_FAST                'source'
              836  BINARY_SUBSCR    
              838  LOAD_STR                 'unknown'
              840  BINARY_SUBSCR    
              842  LOAD_METHOD              remove
              844  LOAD_FAST                'sourceGene'
              846  CALL_METHOD_1         1  '1 positional argument'
              848  POP_TOP          
            850_0  COME_FROM           826  '826'
            850_1  COME_FROM           786  '786'

 L. 173       850  LOAD_FAST                'source'
              852  LOAD_FAST                'target'
              854  COMPARE_OP               !=
          856_858  POP_JUMP_IF_FALSE   772  'to 772'
              860  LOAD_FAST                'sourceGene'
              862  LOAD_CONST               None
              864  COMPARE_OP               is-not
          866_868  POP_JUMP_IF_FALSE   772  'to 772'
              870  LOAD_FAST                'targetGene'
              872  LOAD_CONST               None
              874  COMPARE_OP               is-not
          876_878  POP_JUMP_IF_FALSE   772  'to 772'

 L. 174       880  LOAD_FAST                'targetGene'
              882  LOAD_FAST                'self'
              884  LOAD_ATTR                conversionDict
              886  LOAD_FAST                'source'
              888  BINARY_SUBSCR    
              890  LOAD_FAST                'target'
              892  BINARY_SUBSCR    
              894  LOAD_FAST                'sourceGene'
              896  STORE_SUBSCR     
          898_900  JUMP_BACK           772  'to 772'
              902  POP_BLOCK        
            904_0  COME_FROM_LOOP      748  '748'
          904_906  JUMP_BACK           740  'to 740'
              908  POP_BLOCK        
            910_0  COME_FROM_LOOP      716  '716'

 L. 177       910  SETUP_LOOP          988  'to 988'
              912  LOAD_GLOBAL              set
              914  LOAD_FAST                'ensembl_list'
              916  CALL_FUNCTION_1       1  '1 positional argument'
              918  LOAD_METHOD              difference
              920  LOAD_FAST                'genesSet'
              922  CALL_METHOD_1         1  '1 positional argument'
              924  GET_ITER         
              926  FOR_ITER            986  'to 986'
              928  STORE_FAST               'ensembl_list_item'

 L. 178       930  SETUP_LOOP          982  'to 982'
              932  LOAD_GLOBAL              zip
              934  LOAD_STR                 'entrez'
              936  LOAD_STR                 'hugo'
              938  BUILD_LIST_2          2 
              940  LOAD_FAST                'entrez'
              942  LOAD_FAST                'hugo'
              944  BUILD_LIST_2          2 
              946  CALL_FUNCTION_2       2  '2 positional arguments'
              948  GET_ITER         
              950  FOR_ITER            980  'to 980'
              952  UNPACK_SEQUENCE_2     2 
              954  STORE_FAST               'target'
              956  STORE_FAST               'targetGene'

 L. 179       958  LOAD_FAST                'targetGene'
              960  LOAD_FAST                'self'
              962  LOAD_ATTR                conversionDict
              964  LOAD_STR                 'ensembl'
              966  BINARY_SUBSCR    
              968  LOAD_FAST                'target'
              970  BINARY_SUBSCR    
              972  LOAD_FAST                'ensembl_list_item'
              974  STORE_SUBSCR     
          976_978  JUMP_BACK           950  'to 950'
              980  POP_BLOCK        
            982_0  COME_FROM_LOOP      930  '930'
          982_984  JUMP_BACK           926  'to 926'
              986  POP_BLOCK        
            988_0  COME_FROM_LOOP      910  '910'

 L. 182       988  SETUP_LOOP         1130  'to 1130'
              990  LOAD_FAST                'aliases'
              992  GET_ITER         
              994  FOR_ITER           1128  'to 1128'
              996  STORE_FAST               'alias'

 L. 183       998  LOAD_FAST                'self'
             1000  LOAD_ATTR                conversionDict
             1002  LOAD_STR                 'alias'
             1004  BINARY_SUBSCR    
             1006  LOAD_STR                 'known'
             1008  BINARY_SUBSCR    
             1010  LOAD_METHOD              add
             1012  LOAD_FAST                'alias'
             1014  CALL_METHOD_1         1  '1 positional argument'
             1016  POP_TOP          

 L. 184      1018  LOAD_FAST                'alias'
             1020  LOAD_FAST                'self'
             1022  LOAD_ATTR                conversionDict
             1024  LOAD_STR                 'alias'
             1026  BINARY_SUBSCR    
             1028  LOAD_STR                 'unknown'
             1030  BINARY_SUBSCR    
             1032  COMPARE_OP               in
         1034_1036  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 185      1038  LOAD_FAST                'self'
             1040  LOAD_ATTR                conversionDict
             1042  LOAD_STR                 'alias'
             1044  BINARY_SUBSCR    
             1046  LOAD_STR                 'unknown'
             1048  BINARY_SUBSCR    
             1050  LOAD_METHOD              remove
             1052  LOAD_FAST                'alias'
             1054  CALL_METHOD_1         1  '1 positional argument'
             1056  POP_TOP          
           1058_0  COME_FROM          1034  '1034'

 L. 186      1058  SETUP_LOOP         1124  'to 1124'
             1060  LOAD_GLOBAL              zip
             1062  LOAD_STR                 'entrez'
             1064  LOAD_STR                 'hugo'
             1066  LOAD_STR                 'ensembl'
             1068  BUILD_LIST_3          3 
             1070  LOAD_FAST                'entrez'
             1072  LOAD_FAST                'hugo'
             1074  LOAD_FAST                'ensembl'
             1076  BUILD_LIST_3          3 
             1078  CALL_FUNCTION_2       2  '2 positional arguments'
             1080  GET_ITER         
           1082_0  COME_FROM          1096  '1096'
             1082  FOR_ITER           1122  'to 1122'
             1084  UNPACK_SEQUENCE_2     2 
             1086  STORE_FAST               'target'
             1088  STORE_FAST               'targetGene'

 L. 187      1090  LOAD_FAST                'targetGene'
             1092  LOAD_CONST               None
             1094  COMPARE_OP               is-not
         1096_1098  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 188      1100  LOAD_FAST                'targetGene'
             1102  LOAD_FAST                'self'
             1104  LOAD_ATTR                conversionDict
             1106  LOAD_STR                 'alias'
             1108  BINARY_SUBSCR    
             1110  LOAD_FAST                'target'
             1112  BINARY_SUBSCR    
             1114  LOAD_FAST                'alias'
             1116  STORE_SUBSCR     
         1118_1120  JUMP_BACK          1082  'to 1082'
             1122  POP_BLOCK        
           1124_0  COME_FROM_LOOP     1058  '1058'
         1124_1126  JUMP_BACK           994  'to 994'
             1128  POP_BLOCK        
           1130_0  COME_FROM_LOOP      988  '988'

 L. 191      1130  LOAD_FAST                'hugo'
             1132  LOAD_CONST               None
             1134  COMPARE_OP               is-not
         1136_1138  POP_JUMP_IF_FALSE  1172  'to 1172'
             1140  LOAD_GLOBAL              len
             1142  LOAD_FAST                'aliases'
             1144  CALL_FUNCTION_1       1  '1 positional argument'
             1146  LOAD_CONST               0
             1148  COMPARE_OP               >
         1150_1152  POP_JUMP_IF_FALSE  1172  'to 1172'

 L. 192      1154  LOAD_FAST                'aliases'
             1156  LOAD_FAST                'self'
             1158  LOAD_ATTR                conversionDict
             1160  LOAD_STR                 'hugo'
             1162  BINARY_SUBSCR    
             1164  LOAD_STR                 'alias'
             1166  BINARY_SUBSCR    
             1168  LOAD_FAST                'hugo'
             1170  STORE_SUBSCR     
           1172_0  COME_FROM          1150  '1150'
           1172_1  COME_FROM          1136  '1136'

 L. 195      1172  LOAD_FAST                'entrez'
             1174  LOAD_CONST               None
             1176  COMPARE_OP               is-not
         1178_1180  POP_JUMP_IF_FALSE   270  'to 270'

 L. 196      1182  LOAD_FAST                'retireds'
             1184  LOAD_FAST                'self'
             1186  LOAD_ATTR                conversionDict
             1188  LOAD_STR                 'entrez'
             1190  BINARY_SUBSCR    
             1192  LOAD_STR                 'retired'
             1194  BINARY_SUBSCR    
             1196  LOAD_FAST                'entrez'
             1198  STORE_SUBSCR     

 L. 197      1200  SETUP_LOOP         1294  'to 1294'
             1202  LOAD_FAST                'retireds'
             1204  GET_ITER         
           1206_0  COME_FROM          1264  '1264'
             1206  FOR_ITER           1292  'to 1292'
             1208  STORE_FAST               'retired'

 L. 198      1210  LOAD_FAST                'entrez'
             1212  LOAD_FAST                'self'
             1214  LOAD_ATTR                conversionDict
             1216  LOAD_STR                 'retired'
             1218  BINARY_SUBSCR    
             1220  LOAD_STR                 'entrez'
             1222  BINARY_SUBSCR    
             1224  LOAD_FAST                'retired'
             1226  STORE_SUBSCR     

 L. 199      1228  LOAD_FAST                'self'
             1230  LOAD_ATTR                conversionDict
             1232  LOAD_STR                 'retired'
             1234  BINARY_SUBSCR    
             1236  LOAD_STR                 'known'
             1238  BINARY_SUBSCR    
             1240  LOAD_METHOD              add
             1242  LOAD_FAST                'retired'
             1244  CALL_METHOD_1         1  '1 positional argument'
             1246  POP_TOP          

 L. 200      1248  LOAD_FAST                'retired'
             1250  LOAD_FAST                'self'
             1252  LOAD_ATTR                conversionDict
             1254  LOAD_STR                 'retired'
             1256  BINARY_SUBSCR    
             1258  LOAD_STR                 'unknown'
             1260  BINARY_SUBSCR    
             1262  COMPARE_OP               in
         1264_1266  POP_JUMP_IF_FALSE  1206  'to 1206'

 L. 201      1268  LOAD_FAST                'self'
             1270  LOAD_ATTR                conversionDict
             1272  LOAD_STR                 'retired'
             1274  BINARY_SUBSCR    
             1276  LOAD_STR                 'unknown'
             1278  BINARY_SUBSCR    
             1280  LOAD_METHOD              remove
             1282  LOAD_FAST                'retired'
             1284  CALL_METHOD_1         1  '1 positional argument'
             1286  POP_TOP          
         1288_1290  JUMP_BACK          1206  'to 1206'
             1292  POP_BLOCK        
           1294_0  COME_FROM_LOOP     1200  '1200'
         1294_1296  JUMP_BACK           270  'to 270'
             1298  POP_BLOCK        
           1300_0  COME_FROM_LOOP      256  '256'

 L. 216      1300  SETUP_LOOP         1544  'to 1544'

 L. 217      1302  LOAD_GLOBAL              list
             1304  LOAD_FAST                'self'
             1306  LOAD_ATTR                conversionDict
             1308  LOAD_STR                 'hugo'
             1310  BINARY_SUBSCR    
             1312  LOAD_STR                 'entrez'
             1314  BINARY_SUBSCR    
             1316  LOAD_METHOD              keys
             1318  CALL_METHOD_0         0  '0 positional arguments'
             1320  CALL_FUNCTION_1       1  '1 positional argument'
             1322  LOAD_GLOBAL              list
             1324  LOAD_FAST                'self'
             1326  LOAD_ATTR                conversionDict
             1328  LOAD_STR                 'hugo'
             1330  BINARY_SUBSCR    
             1332  LOAD_STR                 'ensembl'
             1334  BINARY_SUBSCR    
             1336  LOAD_METHOD              keys
             1338  CALL_METHOD_0         0  '0 positional arguments'
             1340  CALL_FUNCTION_1       1  '1 positional argument'
             1342  BINARY_ADD       

 L. 218      1344  LOAD_GLOBAL              list
             1346  LOAD_FAST                'self'
             1348  LOAD_ATTR                conversionDict
             1350  LOAD_STR                 'hugo'
             1352  BINARY_SUBSCR    
             1354  LOAD_STR                 'alias'
             1356  BINARY_SUBSCR    
             1358  LOAD_METHOD              keys
             1360  CALL_METHOD_0         0  '0 positional arguments'
             1362  CALL_FUNCTION_1       1  '1 positional argument'
             1364  BINARY_ADD       
             1366  GET_ITER         
             1368  FOR_ITER           1542  'to 1542'
             1370  STORE_FAST               'hugo'

 L. 219      1372  SETUP_EXCEPT       1396  'to 1396'

 L. 219      1374  LOAD_FAST                'self'
             1376  LOAD_ATTR                conversionDict
             1378  LOAD_STR                 'hugo'
             1380  BINARY_SUBSCR    
             1382  LOAD_STR                 'entrez'
             1384  BINARY_SUBSCR    
             1386  LOAD_FAST                'hugo'
             1388  BINARY_SUBSCR    
             1390  STORE_FAST               'entrez'
             1392  POP_BLOCK        
             1394  JUMP_FORWARD       1422  'to 1422'
           1396_0  COME_FROM_EXCEPT   1372  '1372'

 L. 220      1396  DUP_TOP          
             1398  LOAD_GLOBAL              KeyError
             1400  COMPARE_OP               exception-match
         1402_1404  POP_JUMP_IF_FALSE  1420  'to 1420'
             1406  POP_TOP          
             1408  POP_TOP          
             1410  POP_TOP          

 L. 220      1412  LOAD_CONST               None
             1414  STORE_FAST               'entrez'
             1416  POP_EXCEPT       
             1418  JUMP_FORWARD       1422  'to 1422'
           1420_0  COME_FROM          1402  '1402'
             1420  END_FINALLY      
           1422_0  COME_FROM          1418  '1418'
           1422_1  COME_FROM          1394  '1394'

 L. 221      1422  SETUP_EXCEPT       1446  'to 1446'

 L. 221      1424  LOAD_FAST                'self'
             1426  LOAD_ATTR                conversionDict
             1428  LOAD_STR                 'hugo'
             1430  BINARY_SUBSCR    
             1432  LOAD_STR                 'ensembl'
             1434  BINARY_SUBSCR    
             1436  LOAD_FAST                'hugo'
             1438  BINARY_SUBSCR    
             1440  STORE_FAST               'ensembl'
             1442  POP_BLOCK        
             1444  JUMP_FORWARD       1472  'to 1472'
           1446_0  COME_FROM_EXCEPT   1422  '1422'

 L. 222      1446  DUP_TOP          
             1448  LOAD_GLOBAL              KeyError
             1450  COMPARE_OP               exception-match
         1452_1454  POP_JUMP_IF_FALSE  1470  'to 1470'
             1456  POP_TOP          
             1458  POP_TOP          
             1460  POP_TOP          

 L. 222      1462  LOAD_CONST               None
             1464  STORE_FAST               'ensembl'
             1466  POP_EXCEPT       
             1468  JUMP_FORWARD       1472  'to 1472'
           1470_0  COME_FROM          1452  '1452'
             1470  END_FINALLY      
           1472_0  COME_FROM          1468  '1468'
           1472_1  COME_FROM          1444  '1444'

 L. 223      1472  SETUP_LOOP         1538  'to 1538'
             1474  LOAD_GLOBAL              zip
             1476  LOAD_STR                 'entrez'
             1478  LOAD_STR                 'hugo'
             1480  LOAD_STR                 'ensembl'
             1482  BUILD_LIST_3          3 
             1484  LOAD_FAST                'entrez'
             1486  LOAD_FAST                'hugo'
             1488  LOAD_FAST                'ensembl'
             1490  BUILD_LIST_3          3 
             1492  CALL_FUNCTION_2       2  '2 positional arguments'
             1494  GET_ITER         
           1496_0  COME_FROM          1510  '1510'
             1496  FOR_ITER           1536  'to 1536'
             1498  UNPACK_SEQUENCE_2     2 
             1500  STORE_FAST               'target'
             1502  STORE_FAST               'targetGene'

 L. 224      1504  LOAD_FAST                'targetGene'
             1506  LOAD_CONST               None
             1508  COMPARE_OP               is-not
         1510_1512  POP_JUMP_IF_FALSE  1496  'to 1496'

 L. 225      1514  LOAD_FAST                'targetGene'
             1516  LOAD_FAST                'self'
             1518  LOAD_ATTR                conversionDict
             1520  LOAD_STR                 'alias'
             1522  BINARY_SUBSCR    
             1524  LOAD_FAST                'target'
             1526  BINARY_SUBSCR    
             1528  LOAD_FAST                'hugo'
             1530  STORE_SUBSCR     
         1532_1534  JUMP_BACK          1496  'to 1496'
             1536  POP_BLOCK        
           1538_0  COME_FROM_LOOP     1472  '1472'
         1538_1540  JUMP_BACK          1368  'to 1368'
             1542  POP_BLOCK        
           1544_0  COME_FROM_LOOP     1300  '1300'

 L. 227      1544  LOAD_FAST                'self'
             1546  LOAD_METHOD              Save
             1548  LOAD_FAST                'self'
             1550  LOAD_ATTR                conversionDict
             1552  LOAD_FAST                'self'
             1554  LOAD_ATTR                dictDir
             1556  CALL_METHOD_2         2  '2 positional arguments'
             1558  POP_TOP          

Parse error at or near `LOAD_GLOBAL' instruction at offset 230

    def Save(self, x, pathToFile):
        with open(pathToFile, 'wb') as (f):
            pickle.dump(x, f)

    def Load(self, pathToFile):
        with open(pathToFile, 'rb') as (f):
            return pickle.load(f)