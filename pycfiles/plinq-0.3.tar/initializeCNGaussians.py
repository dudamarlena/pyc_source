# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/initializeCNGaussians.py
# Compiled at: 2010-07-13 12:32:47
__doc__ = '\nusage: %prog [options] <CNsummaries> <CNclusters>\n\nRead CN summaries file, and write CN clusters.\n'
import fileinput, math, optparse, sys
from mpgutils import utils
iMIN_SAMPLES1 = 4
iMIN_SAMPLES2 = 10

def mean(values):
    x = 0
    for i in values:
        x += i

    return x / len(values)


def trimmean(values, pct=0.8):
    n = len(values)
    x = 0
    leaveout = int((1 - pct) / 2 * n)
    for i in values[leaveout:n - leaveout]:
        x += i

    return x / (n - 2 * leaveout)


def var(values):
    avg = mean(values)
    x = 0
    for i in values:
        x += (i - avg) ** 2

    return x / len(values)


def robustvar(values):
    leaveout = int(0.25 * len(values))
    return (0.7413 * (values[leaveout] - values[(len(values) - leaveout - 1)])) ** 2


def parseExclusions(strExclusions, bIncludeSNPs=True, bIncludeCNs=True):
    assert bIncludeSNPs or bIncludeCNs
    fIn = fileinput.FileInput([strExclusions])
    for strLine in fIn:
        if strLine.startswith('probeset_id'):
            break

    dctRet = {}
    for strLine in fIn:
        lstFields = strLine.split()
        if len(lstFields) != 2:
            utils.raiseExceptionWithFileInput(fIn, 'Exclusions file', 'Wrong number of fields')
        strProbe = lstFields[0]
        if not bIncludeCNs and strProbe.startswith('CN'):
            continue
        if not bIncludeSNPs and not strProbe.startswith('CN'):
            continue
        lstExclusions = [ int(strVal) for strVal in lstFields[1].split(',') ]
        dctRet[strProbe] = lstExclusions

    return dctRet


def doIt--- This code section failed: ---

 L.  66         0  SETUP_EXCEPT         19  'to 22'

 L.  67         3  LOAD_GLOBAL           0  'open'
                6  LOAD_FAST             0  'strCNSummaries'
                9  LOAD_CONST               'r'
               12  CALL_FUNCTION_2       2  None
               15  STORE_FAST            5  'infile'
               18  POP_BLOCK        
               19  JUMP_FORWARD         37  'to 59'
             22_0  COME_FROM             0  '0'

 L.  68        22  DUP_TOP          
               23  LOAD_GLOBAL           1  'IOError'
               26  COMPARE_OP           10  exception-match
               29  JUMP_IF_FALSE        25  'to 57'
               32  POP_TOP          
               33  POP_TOP          
               34  POP_TOP          
               35  POP_TOP          

 L.  69        36  LOAD_CONST               "Can't open file for reading."
               39  PRINT_ITEM       
               40  PRINT_NEWLINE_CONT

 L.  70        41  LOAD_GLOBAL           2  'sys'
               44  LOAD_ATTR             3  'exit'
               47  LOAD_CONST               0
               50  CALL_FUNCTION_1       1  None
               53  POP_TOP          
               54  JUMP_FORWARD          2  'to 59'
               57  POP_TOP          
               58  END_FINALLY      
             59_0  COME_FROM            54  '54'
             59_1  COME_FROM            19  '19'

 L.  72        59  LOAD_FAST             4  'lstSampleIndices'
               62  LOAD_CONST               None
               65  COMPARE_OP            8  is
               68  JUMP_IF_FALSE        10  'to 81'
             71_0  THEN                     82
               71  POP_TOP          

 L.  73        72  BUILD_LIST_0          0 
               75  STORE_FAST            4  'lstSampleIndices'
               78  JUMP_FORWARD          1  'to 82'
             81_0  COME_FROM            68  '68'
               81  POP_TOP          
             82_0  COME_FROM            78  '78'

 L.  75        82  SETUP_EXCEPT         19  'to 104'

 L.  76        85  LOAD_GLOBAL           0  'open'
               88  LOAD_FAST             1  'strCNClusters'
               91  LOAD_CONST               'w'
               94  CALL_FUNCTION_2       2  None
               97  STORE_FAST            6  'outfile'
              100  POP_BLOCK        
              101  JUMP_FORWARD         47  'to 151'
            104_0  COME_FROM            82  '82'

 L.  77       104  DUP_TOP          
              105  LOAD_GLOBAL           1  'IOError'
              108  COMPARE_OP           10  exception-match
              111  JUMP_IF_FALSE        35  'to 149'
              114  POP_TOP          
              115  POP_TOP          
              116  POP_TOP          
              117  POP_TOP          

 L.  78       118  LOAD_CONST               "Can't open file for writing."
              121  PRINT_ITEM       
              122  PRINT_NEWLINE_CONT

 L.  79       123  LOAD_FAST             5  'infile'
              126  LOAD_ATTR             5  'close'
              129  CALL_FUNCTION_0       0  None
              132  POP_TOP          

 L.  80       133  LOAD_GLOBAL           2  'sys'
              136  LOAD_ATTR             3  'exit'
              139  LOAD_CONST               0
              142  CALL_FUNCTION_1       1  None
              145  POP_TOP          
              146  JUMP_FORWARD          2  'to 151'
              149  POP_TOP          
              150  END_FINALLY      
            151_0  COME_FROM           146  '146'
            151_1  COME_FROM           101  '101'

 L.  82       151  LOAD_FAST             2  'bExpectHeader'
              154  JUMP_IF_FALSE        42  'to 199'
            157_0  THEN                     200
              157  POP_TOP          

 L.  84       158  SETUP_LOOP           39  'to 200'
              161  LOAD_FAST             5  'infile'
              164  GET_ITER         
              165  FOR_ITER             27  'to 195'
              168  STORE_FAST            7  'strLine'

 L.  85       171  LOAD_FAST             7  'strLine'
              174  LOAD_ATTR             6  'startswith'
              177  LOAD_CONST               'probeset_id'
              180  CALL_FUNCTION_1       1  None
              183  JUMP_IF_FALSE         5  'to 191'
              186  POP_TOP          

 L.  86       187  BREAK_LOOP       
              188  JUMP_BACK           165  'to 165'
            191_0  COME_FROM           183  '183'
              191  POP_TOP          
              192  JUMP_BACK           165  'to 165'
              195  POP_BLOCK        
              196  JUMP_FORWARD          1  'to 200'
            199_0  COME_FROM           154  '154'
              199  POP_TOP          
            200_0  COME_FROM           158  '158'

 L.  87       200  SETUP_LOOP          755  'to 958'
              203  LOAD_FAST             5  'infile'
              206  GET_ITER         
              207  FOR_ITER            747  'to 957'
              210  STORE_FAST            8  'line'

 L.  88       213  LOAD_FAST             8  'line'
              216  LOAD_ATTR             7  'split'
              219  CALL_FUNCTION_0       0  None
              222  STORE_FAST            9  'values'

 L.  89       225  LOAD_FAST             9  'values'
              228  LOAD_CONST               0
              231  BINARY_SUBSCR    
              232  STORE_FAST           10  'strProbe'

 L.  90       235  LOAD_GLOBAL           8  'len'
              238  LOAD_FAST             4  'lstSampleIndices'
              241  CALL_FUNCTION_1       1  None
              244  LOAD_CONST               0
              247  COMPARE_OP            2  ==
              250  JUMP_IF_TRUE         68  'to 321'
              253  POP_TOP          
              254  LOAD_FAST             9  'values'
              257  LOAD_CONST               1
              260  BINARY_SUBSCR    
              261  LOAD_CONST               'X'
              264  COMPARE_OP            3  !=
              267  JUMP_IF_FALSE       205  'to 475'
              270  POP_TOP          
              271  LOAD_FAST             9  'values'
              274  LOAD_CONST               1
              277  BINARY_SUBSCR    
              278  LOAD_CONST               '23'
              281  COMPARE_OP            3  !=
              284  JUMP_IF_FALSE       188  'to 475'
              287  POP_TOP          
              288  LOAD_FAST             9  'values'
              291  LOAD_CONST               1
              294  BINARY_SUBSCR    
              295  LOAD_CONST               'Y'
              298  COMPARE_OP            3  !=
              301  JUMP_IF_FALSE       171  'to 475'
              304  POP_TOP          
              305  LOAD_FAST             9  'values'
              308  LOAD_CONST               1
              311  BINARY_SUBSCR    
              312  LOAD_CONST               '24'
              315  COMPARE_OP            3  !=
            318_0  COME_FROM           301  '301'
            318_1  COME_FROM           284  '284'
            318_2  COME_FROM           267  '267'
            318_3  COME_FROM           250  '250'
              318  JUMP_IF_FALSE       154  'to 475'
              321  POP_TOP          

 L.  91       322  LOAD_FAST             9  'values'
              325  LOAD_CONST               4
              328  SLICE+1          
              329  STORE_FAST           11  'values2'

 L.  92       332  LOAD_FAST             3  'dctExclusions'
              335  LOAD_CONST               None
              338  COMPARE_OP            9  is-not
              341  JUMP_IF_FALSE       127  'to 471'
              344  POP_TOP          

 L.  93       345  LOAD_FAST            10  'strProbe'
              348  LOAD_FAST             3  'dctExclusions'
              351  COMPARE_OP            6  in
              354  JUMP_IF_FALSE       110  'to 467'
              357  POP_TOP          

 L.  94       358  LOAD_FAST             3  'dctExclusions'
              361  LOAD_FAST            10  'strProbe'
              364  BINARY_SUBSCR    
              365  STORE_FAST           12  'lstExclusions'

 L.  95       368  LOAD_GLOBAL           8  'len'
              371  LOAD_FAST            12  'lstExclusions'
              374  CALL_FUNCTION_1       1  None
              377  LOAD_GLOBAL           8  'len'
              380  LOAD_FAST            11  'values2'
              383  CALL_FUNCTION_1       1  None
              386  COMPARE_OP            0  <
              389  JUMP_IF_FALSE        54  'to 446'
              392  POP_TOP          

 L.  98       393  SETUP_LOOP           68  'to 464'
              396  LOAD_GLOBAL           9  'xrange'
              399  LOAD_GLOBAL           8  'len'
              402  LOAD_FAST            12  'lstExclusions'
              405  CALL_FUNCTION_1       1  None
              408  LOAD_CONST               1
              411  BINARY_SUBTRACT  
              412  LOAD_CONST               -1
              415  LOAD_CONST               -1
              418  CALL_FUNCTION_3       3  None
              421  GET_ITER         
              422  FOR_ITER             17  'to 442'
              425  STORE_FAST           13  'i'

 L.  99       428  LOAD_FAST            11  'values2'
              431  LOAD_FAST            12  'lstExclusions'
              434  LOAD_FAST            13  'i'
              437  BINARY_SUBSCR    
              438  DELETE_SUBSCR    
              439  JUMP_BACK           422  'to 422'
              442  POP_BLOCK        
              443  JUMP_ABSOLUTE       468  'to 468'
            446_0  COME_FROM           389  '389'
              446  POP_TOP          

 L. 102       447  LOAD_FAST             6  'outfile'
              450  DUP_TOP          
              451  LOAD_FAST            10  'strProbe'
              454  LOAD_CONST               ';1 1;1 1;1 1'
              457  BINARY_ADD       
              458  ROT_TWO          
              459  PRINT_ITEM_TO    
              460  PRINT_NEWLINE_TO 

 L. 103       461  CONTINUE            207  'to 207'
            464_0  COME_FROM           393  '393'
              464  JUMP_ABSOLUTE       472  'to 472'
            467_0  COME_FROM           354  '354'
              467  POP_TOP          
              468  JUMP_ABSOLUTE       520  'to 520'
            471_0  COME_FROM           341  '341'
              471  POP_TOP          
              472  JUMP_FORWARD         45  'to 520'
            475_0  COME_FROM           318  '318'
              475  POP_TOP          

 L. 105       476  BUILD_LIST_0          0 
              479  STORE_FAST           11  'values2'

 L. 106       482  SETUP_LOOP           35  'to 520'
              485  LOAD_FAST             4  'lstSampleIndices'
              488  GET_ITER         
              489  FOR_ITER             27  'to 519'
              492  STORE_FAST           13  'i'

 L. 107       495  LOAD_FAST            11  'values2'
              498  LOAD_ATTR            10  'append'
              501  LOAD_FAST             9  'values'
              504  LOAD_FAST            13  'i'
              507  LOAD_CONST               4
              510  BINARY_ADD       
              511  BINARY_SUBSCR    
              512  CALL_FUNCTION_1       1  None
              515  POP_TOP          
              516  JUMP_BACK           489  'to 489'
              519  POP_BLOCK        
            520_0  COME_FROM           482  '482'
            520_1  COME_FROM           472  '472'

 L. 108       520  SETUP_LOOP           46  'to 569'
              523  LOAD_GLOBAL          11  'range'
              526  LOAD_GLOBAL           8  'len'
              529  LOAD_FAST            11  'values2'
              532  CALL_FUNCTION_1       1  None
              535  CALL_FUNCTION_1       1  None
              538  GET_ITER         
              539  FOR_ITER             26  'to 568'
              542  STORE_FAST           13  'i'

 L. 109       545  LOAD_GLOBAL          12  'float'
              548  LOAD_FAST            11  'values2'
              551  LOAD_FAST            13  'i'
              554  BINARY_SUBSCR    
              555  CALL_FUNCTION_1       1  None
              558  LOAD_FAST            11  'values2'
              561  LOAD_FAST            13  'i'
              564  STORE_SUBSCR     
              565  JUMP_BACK           539  'to 539'
              568  POP_BLOCK        
            569_0  COME_FROM           520  '520'

 L. 110       569  LOAD_FAST            11  'values2'
              572  LOAD_ATTR            13  'sort'
              575  CALL_FUNCTION_0       0  None
              578  POP_TOP          

 L. 111       579  LOAD_GLOBAL          14  'trimmean'
              582  LOAD_FAST            11  'values2'
              585  CALL_FUNCTION_1       1  None
              588  STORE_FAST           14  'mean2'

 L. 112       591  LOAD_GLOBAL           8  'len'
              594  LOAD_FAST            11  'values2'
              597  CALL_FUNCTION_1       1  None
              600  LOAD_GLOBAL          15  'iMIN_SAMPLES2'
              603  COMPARE_OP            5  >=
              606  JUMP_IF_FALSE        16  'to 625'
              609  POP_TOP          

 L. 113       610  LOAD_GLOBAL          16  'robustvar'
              613  LOAD_FAST            11  'values2'
              616  CALL_FUNCTION_1       1  None
              619  STORE_FAST           15  'var2'
              622  JUMP_FORWARD         62  'to 687'
            625_0  COME_FROM           606  '606'
              625  POP_TOP          

 L. 114       626  LOAD_GLOBAL           8  'len'
              629  LOAD_FAST            11  'values2'
              632  CALL_FUNCTION_1       1  None
              635  LOAD_GLOBAL          17  'iMIN_SAMPLES1'
              638  COMPARE_OP            5  >=
              641  JUMP_IF_FALSE        16  'to 660'
              644  POP_TOP          

 L. 115       645  LOAD_GLOBAL          18  'var'
              648  LOAD_FAST            11  'values2'
              651  CALL_FUNCTION_1       1  None
              654  STORE_FAST           15  'var2'
              657  JUMP_FORWARD         27  'to 687'
            660_0  COME_FROM           641  '641'
              660  POP_TOP          

 L. 117       661  LOAD_GLOBAL          19  'math'
              664  LOAD_ATTR            20  'pow'
              667  LOAD_CONST               31
              670  LOAD_CONST               0.075
              673  LOAD_FAST            14  'mean2'
              676  BINARY_MULTIPLY  
              677  BINARY_ADD       
              678  LOAD_CONST               2
              681  CALL_FUNCTION_2       2  None
              684  STORE_FAST           15  'var2'
            687_0  COME_FROM           657  '657'
            687_1  COME_FROM           622  '622'

 L. 118       687  LOAD_FAST             9  'values'
              690  LOAD_CONST               1
              693  BINARY_SUBSCR    
              694  LOAD_CONST               'Y'
              697  COMPARE_OP            2  ==
              700  JUMP_IF_TRUE         17  'to 720'
              703  POP_TOP          
              704  LOAD_FAST             9  'values'
              707  LOAD_CONST               1
              710  BINARY_SUBSCR    
              711  LOAD_CONST               '24'
              714  COMPARE_OP            2  ==
            717_0  COME_FROM           700  '700'
              717  JUMP_IF_FALSE        72  'to 792'
              720  POP_TOP          

 L. 119       721  LOAD_FAST            14  'mean2'
              724  STORE_FAST           16  'mean1'

 L. 120       727  LOAD_FAST            15  'var2'
              730  STORE_FAST           17  'var1'

 L. 121       733  LOAD_FAST            16  'mean1'
              736  LOAD_CONST               41.5529
              739  BINARY_SUBTRACT  
              740  LOAD_CONST               0.646
              743  BINARY_DIVIDE    
              744  STORE_FAST           14  'mean2'

 L. 122       747  LOAD_FAST            17  'var1'
              750  LOAD_CONST               0.9
              753  BINARY_DIVIDE    
              754  STORE_FAST           15  'var2'

 L. 123       757  LOAD_FAST            16  'mean1'
              760  LOAD_CONST               0.354
              763  LOAD_FAST            14  'mean2'
              766  BINARY_MULTIPLY  
              767  LOAD_CONST               41.5529
              770  BINARY_SUBTRACT  
              771  LOAD_CONST               0.75
              774  BINARY_DIVIDE    
              775  BINARY_SUBTRACT  
              776  STORE_FAST           18  'mean0'

 L. 124       779  LOAD_FAST            17  'var1'
              782  LOAD_CONST               0.9
              785  BINARY_MULTIPLY  
              786  STORE_FAST           19  'var0'
              789  JUMP_FORWARD         61  'to 853'
            792_0  COME_FROM           717  '717'
              792  POP_TOP          

 L. 126       793  LOAD_FAST            14  'mean2'
              796  LOAD_CONST               0.354
              799  LOAD_FAST            14  'mean2'
              802  BINARY_MULTIPLY  
              803  LOAD_CONST               41.5529
              806  BINARY_SUBTRACT  
              807  BINARY_SUBTRACT  
              808  STORE_FAST           16  'mean1'

 L. 127       811  LOAD_FAST            16  'mean1'
              814  LOAD_CONST               0.354
              817  LOAD_FAST            14  'mean2'
              820  BINARY_MULTIPLY  
              821  LOAD_CONST               41.5529
              824  BINARY_SUBTRACT  
              825  LOAD_CONST               0.75
              828  BINARY_DIVIDE    
              829  BINARY_SUBTRACT  
              830  STORE_FAST           18  'mean0'

 L. 128       833  LOAD_FAST            15  'var2'
              836  LOAD_CONST               0.9
              839  BINARY_MULTIPLY  
              840  STORE_FAST           17  'var1'

 L. 129       843  LOAD_FAST            17  'var1'
              846  LOAD_CONST               0.9
              849  BINARY_MULTIPLY  
              850  STORE_FAST           19  'var0'
            853_0  COME_FROM           789  '789'

 L. 130       853  LOAD_FAST             6  'outfile'
              856  LOAD_ATTR            21  'write'
              859  LOAD_FAST            10  'strProbe'
              862  LOAD_CONST               ';'
              865  BINARY_ADD       
              866  LOAD_GLOBAL          22  'str'
              869  LOAD_FAST            18  'mean0'
              872  CALL_FUNCTION_1       1  None
              875  BINARY_ADD       
              876  LOAD_CONST               ' '
              879  BINARY_ADD       
              880  LOAD_GLOBAL          22  'str'
              883  LOAD_FAST            19  'var0'
              886  CALL_FUNCTION_1       1  None
              889  BINARY_ADD       
              890  LOAD_CONST               ';'
              893  BINARY_ADD       
              894  LOAD_GLOBAL          22  'str'
              897  LOAD_FAST            16  'mean1'
              900  CALL_FUNCTION_1       1  None
              903  BINARY_ADD       
              904  LOAD_CONST               ' '
              907  BINARY_ADD       
              908  LOAD_GLOBAL          22  'str'
              911  LOAD_FAST            17  'var1'
              914  CALL_FUNCTION_1       1  None
              917  BINARY_ADD       
              918  LOAD_CONST               ';'
              921  BINARY_ADD       
              922  LOAD_GLOBAL          22  'str'
              925  LOAD_FAST            14  'mean2'
              928  CALL_FUNCTION_1       1  None
              931  BINARY_ADD       
              932  LOAD_CONST               ' '
              935  BINARY_ADD       
              936  LOAD_GLOBAL          22  'str'
              939  LOAD_FAST            15  'var2'
              942  CALL_FUNCTION_1       1  None
              945  BINARY_ADD       
              946  LOAD_CONST               '\n'
              949  BINARY_ADD       
              950  CALL_FUNCTION_1       1  None
              953  POP_TOP          
              954  JUMP_BACK           207  'to 207'
              957  POP_BLOCK        
            958_0  COME_FROM           200  '200'

 L. 132       958  LOAD_FAST             5  'infile'
              961  LOAD_ATTR             5  'close'
              964  CALL_FUNCTION_0       0  None
              967  POP_TOP          

 L. 133       968  LOAD_FAST             6  'outfile'
              971  LOAD_ATTR             5  'close'
              974  CALL_FUNCTION_0       0  None
              977  POP_TOP          
              978  LOAD_CONST               None
              981  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 464


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('--header', default=False, action='store_true', help='Expected a header line in CN summary file.  Default: %default')
    parser.add_option('--exclusions', help='File containing CN/sample pairs that should not be included in CN cluster creation.')
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if len(lstArgs) > 3:
        strSamples = lstArgs[3]
    else:
        strSamples = None
    if dctOptions.exclusions is not None:
        dctExclusions = parseExclusions(dctOptions.exclusions, bIncludeSNPs=False)
    else:
        dctExclusions = None
    doIt(lstArgs[1], lstArgs[2], strSamples=strSamples, bExpectHeader=dctOptions.header, dctExclusions=dctExclusions)
    return


if __name__ == '__main__':
    sys.exit(main())