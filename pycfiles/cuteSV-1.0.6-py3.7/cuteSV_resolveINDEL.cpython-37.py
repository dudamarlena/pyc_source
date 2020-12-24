# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cuteSV/cuteSV_resolveINDEL.py
# Compiled at: 2020-04-29 04:13:06
# Size of source mod 2**32: 21162 bytes
import sys, numpy as np
from collections import Counter
from cuteSV.cuteSV_genotype import cal_GL, cal_CIPOS, threshold_ref_count, count_coverage
import time

def resolution_DEL--- This code section failed: ---

 L.  46         0  LOAD_GLOBAL              list
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'semi_del_cluster'

 L.  47         6  LOAD_FAST                'semi_del_cluster'
                8  LOAD_METHOD              append
               10  LOAD_CONST               0
               12  LOAD_CONST               0
               14  LOAD_STR                 ''
               16  BUILD_LIST_3          3 
               18  CALL_METHOD_1         1  '1 positional argument'
               20  POP_TOP          

 L.  48        22  LOAD_GLOBAL              list
               24  CALL_FUNCTION_0       0  '0 positional arguments'
               26  STORE_FAST               'candidate_single_SV'

 L.  50        28  LOAD_GLOBAL              open
               30  LOAD_FAST                'path'
               32  LOAD_STR                 'r'
               34  CALL_FUNCTION_2       2  '2 positional arguments'
               36  STORE_FAST               'file'

 L.  51        38  SETUP_LOOP          256  'to 256'
               40  LOAD_FAST                'file'
               42  GET_ITER         
               44  FOR_ITER            254  'to 254'
               46  STORE_FAST               'line'

 L.  52        48  LOAD_FAST                'line'
               50  LOAD_METHOD              strip
               52  LOAD_STR                 '\n'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  LOAD_METHOD              split
               58  LOAD_STR                 '\t'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  STORE_FAST               'seq'

 L.  53        64  LOAD_FAST                'seq'
               66  LOAD_CONST               1
               68  BINARY_SUBSCR    
               70  LOAD_FAST                'chr'
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE    78  'to 78'

 L.  54        76  CONTINUE             44  'to 44'
             78_0  COME_FROM            74  '74'

 L.  56        78  LOAD_GLOBAL              int
               80  LOAD_FAST                'seq'
               82  LOAD_CONST               2
               84  BINARY_SUBSCR    
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  STORE_FAST               'pos'

 L.  57        90  LOAD_GLOBAL              int
               92  LOAD_FAST                'seq'
               94  LOAD_CONST               3
               96  BINARY_SUBSCR    
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  STORE_FAST               'indel_len'

 L.  58       102  LOAD_FAST                'seq'
              104  LOAD_CONST               4
              106  BINARY_SUBSCR    
              108  STORE_FAST               'read_id'

 L.  60       110  LOAD_FAST                'pos'
              112  LOAD_FAST                'semi_del_cluster'
              114  LOAD_CONST               -1
              116  BINARY_SUBSCR    
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  BINARY_SUBTRACT  
              124  LOAD_FAST                'max_cluster_bias'
              126  COMPARE_OP               >
              128  POP_JUMP_IF_FALSE   236  'to 236'

 L.  61       130  LOAD_GLOBAL              len
              132  LOAD_FAST                'semi_del_cluster'
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  LOAD_FAST                'read_count'
              138  COMPARE_OP               >=
              140  POP_JUMP_IF_FALSE   214  'to 214'

 L.  62       142  LOAD_FAST                'semi_del_cluster'
              144  LOAD_CONST               -1
              146  BINARY_SUBSCR    
              148  LOAD_CONST               0
              150  BINARY_SUBSCR    
              152  LOAD_FAST                'semi_del_cluster'
              154  LOAD_CONST               -1
              156  BINARY_SUBSCR    
              158  LOAD_CONST               1
              160  BINARY_SUBSCR    
              162  DUP_TOP          
              164  ROT_THREE        
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   178  'to 178'
              170  LOAD_CONST               0
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   184  'to 184'
              176  JUMP_ABSOLUTE       214  'to 214'
            178_0  COME_FROM           168  '168'
              178  POP_TOP          
              180  JUMP_FORWARD        184  'to 184'

 L.  63       182  JUMP_FORWARD        214  'to 214'
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           174  '174'

 L.  65       184  LOAD_GLOBAL              generate_del_cluster
              186  LOAD_FAST                'semi_del_cluster'

 L.  66       188  LOAD_FAST                'chr'

 L.  67       190  LOAD_FAST                'svtype'

 L.  68       192  LOAD_FAST                'read_count'

 L.  69       194  LOAD_FAST                'threshold_gloab'

 L.  70       196  LOAD_FAST                'threshold_local'

 L.  71       198  LOAD_FAST                'minimum_support_reads'

 L.  72       200  LOAD_FAST                'candidate_single_SV'

 L.  73       202  LOAD_FAST                'bam_path'

 L.  74       204  LOAD_FAST                'max_cluster_bias'

 L.  75       206  LOAD_FAST                'action'

 L.  76       208  LOAD_FAST                'gt_round'
              210  CALL_FUNCTION_12     12  '12 positional arguments'
              212  POP_TOP          
            214_0  COME_FROM           182  '182'
            214_1  COME_FROM           140  '140'

 L.  77       214  BUILD_LIST_0          0 
              216  STORE_FAST               'semi_del_cluster'

 L.  78       218  LOAD_FAST                'semi_del_cluster'
              220  LOAD_METHOD              append
              222  LOAD_FAST                'pos'
              224  LOAD_FAST                'indel_len'
              226  LOAD_FAST                'read_id'
              228  BUILD_LIST_3          3 
              230  CALL_METHOD_1         1  '1 positional argument'
              232  POP_TOP          
              234  JUMP_BACK            44  'to 44'
            236_0  COME_FROM           128  '128'

 L.  80       236  LOAD_FAST                'semi_del_cluster'
              238  LOAD_METHOD              append
              240  LOAD_FAST                'pos'
              242  LOAD_FAST                'indel_len'
              244  LOAD_FAST                'read_id'
              246  BUILD_LIST_3          3 
              248  CALL_METHOD_1         1  '1 positional argument'
              250  POP_TOP          
              252  JUMP_BACK            44  'to 44'
              254  POP_BLOCK        
            256_0  COME_FROM_LOOP       38  '38'

 L.  82       256  LOAD_GLOBAL              len
              258  LOAD_FAST                'semi_del_cluster'
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  LOAD_FAST                'read_count'
              264  COMPARE_OP               >=
          266_268  POP_JUMP_IF_FALSE   346  'to 346'

 L.  83       270  LOAD_FAST                'semi_del_cluster'
              272  LOAD_CONST               -1
              274  BINARY_SUBSCR    
              276  LOAD_CONST               0
              278  BINARY_SUBSCR    
              280  LOAD_FAST                'semi_del_cluster'
              282  LOAD_CONST               -1
              284  BINARY_SUBSCR    
              286  LOAD_CONST               1
              288  BINARY_SUBSCR    
              290  DUP_TOP          
              292  ROT_THREE        
              294  COMPARE_OP               ==
          296_298  POP_JUMP_IF_FALSE   310  'to 310'
              300  LOAD_CONST               0
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   316  'to 316'
              308  JUMP_FORWARD        314  'to 314'
            310_0  COME_FROM           296  '296'
              310  POP_TOP          
              312  JUMP_FORWARD        316  'to 316'
            314_0  COME_FROM           308  '308'

 L.  84       314  JUMP_FORWARD        346  'to 346'
            316_0  COME_FROM           312  '312'
            316_1  COME_FROM           304  '304'

 L.  86       316  LOAD_GLOBAL              generate_del_cluster
              318  LOAD_FAST                'semi_del_cluster'

 L.  87       320  LOAD_FAST                'chr'

 L.  88       322  LOAD_FAST                'svtype'

 L.  89       324  LOAD_FAST                'read_count'

 L.  90       326  LOAD_FAST                'threshold_gloab'

 L.  91       328  LOAD_FAST                'threshold_local'

 L.  92       330  LOAD_FAST                'minimum_support_reads'

 L.  93       332  LOAD_FAST                'candidate_single_SV'

 L.  94       334  LOAD_FAST                'bam_path'

 L.  95       336  LOAD_FAST                'max_cluster_bias'

 L.  96       338  LOAD_FAST                'action'

 L.  97       340  LOAD_FAST                'gt_round'
              342  CALL_FUNCTION_12     12  '12 positional arguments'
              344  POP_TOP          
            346_0  COME_FROM           314  '314'
            346_1  COME_FROM           266  '266'

 L.  98       346  LOAD_FAST                'file'
              348  LOAD_METHOD              close
              350  CALL_METHOD_0         0  '0 positional arguments'
              352  POP_TOP          

 L.  99       354  LOAD_FAST                'candidate_single_SV'
              356  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 178


def generate_del_cluster(semi_del_cluster, chr, svtype, read_count, threshold_gloab, threshold_local, minimum_support_reads, candidate_single_SV, bam_path, max_cluster_bias, action, gt_round):
    """
        generate deletion
        *************************************************************
        threshold_gloab         threshold_local         minimum_support_reads
        -------------------------------------------------------------
                0.3                                     0.7                                     5               CLR
                0.4                                     0.5                               <=5           CCS
        *************************************************************
        """
    read_tag = dict
    for element in semi_del_cluster:
        if element[2] not in read_tag:
            read_tag[element[2]] = element

    if len(read_tag) < read_count:
        return
        read_tag2SortedList = sorted((list(read_tag.values)), key=(lambda x: x[1]))
        global_len = [i[1] for i in read_tag2SortedList]
        DISCRETE_THRESHOLD_LEN_CLUSTER_DEL_TEMP = threshold_gloab * np.meanglobal_len
        last_len = read_tag2SortedList[0][1]
        alelle_collect = list
        alelle_collect.append[[read_tag2SortedList[0][0]], [read_tag2SortedList[0][1]], [],
         [
          read_tag2SortedList[0][2]]]
        for i in read_tag2SortedList[1:]:
            if i[1] - last_len > DISCRETE_THRESHOLD_LEN_CLUSTER_DEL_TEMP:
                alelle_collect[(-1)][2].appendlen(alelle_collect[(-1)][0])
                alelle_collect.append[[], [], [], []]
            alelle_collect[(-1)][0].appendi[0]
            alelle_collect[(-1)][1].appendi[1]
            alelle_collect[(-1)][3].appendi[2]
            last_len = i[1]

        alelle_collect[(-1)][2].appendlen(alelle_collect[(-1)][0])
        alelle_sort = sorted(alelle_collect, key=(lambda x: x[2]))
        if alelle_sort[(-1)][2][0] >= minimum_support_reads and float(alelle_sort[(-1)][2][0] * 1.0 / len(read_tag)) >= threshold_local:
            breakpointStart = np.meanalelle_sort[(-1)][0]
            CIPOS = cal_CIPOSnp.stdalelle_sort[(-1)][0]len(alelle_sort[(-1)][0])
            search_threshold = np.minalelle_sort[(-1)][0]
            signalLen = np.meanalelle_sort[(-1)][1]
            CILEN = cal_CIPOSnp.stdalelle_sort[(-1)][1]len(alelle_sort[(-1)][1])
            signalLen_STD = np.stdalelle_sort[(-1)][1]
            if action:
                DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, search_threshold, chr, alelle_sort[(-1)][3], max_cluster_bias, gt_round)
    else:
        DR = '.'
        GT = './.'
        GL = '.,.,.'
        GQ = '.'
        QUAL = '.'
    candidate_single_SV.append[chr,
     svtype,
     str(int(breakpointStart)),
     str(int(-signalLen)),
     str(alelle_sort[(-1)][2][0]),
     str(CIPOS),
     str(CILEN),
     str(DR),
     str(GT),
     str(GL),
     str(GQ),
     str(QUAL)]
    if len(alelle_sort) > 1 and alelle_sort[(-2)][2][0] >= minimum_support_reads and alelle_sort[(-2)][2][0] + alelle_sort[(-1)][2][0] >= 0.95 * len(read_tag) and alelle_sort[(-2)][2][0] >= 0.3 * len(read_tag):
        breakpointStart = np.meanalelle_sort[(-2)][0]
        CIPOS = cal_CIPOSnp.stdalelle_sort[(-2)][0]len(alelle_sort[(-2)][0])
        search_threshold = np.minalelle_sort[(-2)][0]
        signalLen = np.meanalelle_sort[(-2)][1]
        last_signalLen_STD = signalLen_STD
        signalLen_STD = np.stdalelle_sort[(-2)][1]
        CILEN = cal_CIPOSnp.stdalelle_sort[(-2)][1]len(alelle_sort[(-2)][1])
        if action:
            DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, search_threshold, chr, alelle_sort[(-2)][3], max_cluster_bias, gt_round)
        else:
            DR = '.'
            GT = './.'
            GL = '.,.,.'
            GQ = '.'
            QUAL = '.'
        candidate_single_SV.append[chr,
         svtype,
         str(int(breakpointStart)),
         str(int(-signalLen)),
         str(alelle_sort[(-2)][2][0]),
         str(CIPOS),
         str(CILEN),
         str(DR),
         str(GT),
         str(GL),
         str(GQ),
         str(QUAL)]
    else:
        if alelle_sort[(-2)][2][0] >= minimum_support_reads:
            if alelle_sort[(-2)][2][0] + alelle_sort[(-1)][2][0] >= 0.95 * len(read_tag):
                if alelle_sort[(-2)][2][0] >= 0.4 * len(read_tag):
                    breakpointStart = np.meanalelle_sort[(-1)][0]
                    CIPOS = cal_CIPOSnp.stdalelle_sort[(-1)][0]len(alelle_sort[(-1)][0])
                    search_threshold = np.minalelle_sort[(-1)][0]
                    signalLen = np.meanalelle_sort[(-1)][1]
                    signalLen_STD = np.stdalelle_sort[(-1)][1]
                    CILEN = cal_CIPOSnp.stdalelle_sort[(-1)][1]len(alelle_sort[(-1)][1])
                    if action:
                        DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, search_threshold, chr, alelle_sort[(-1)][3], max_cluster_bias, gt_round)
                    else:
                        DR = '.'
                        GT = './.'
                        GL = '.,.,.'
                        GQ = '.'
                        QUAL = '.'
                    candidate_single_SV.append[chr,
                     svtype,
                     str(int(breakpointStart)),
                     str(int(-signalLen)),
                     str(alelle_sort[(-1)][2][0]),
                     str(CIPOS),
                     str(CILEN),
                     str(DR),
                     str(GT),
                     str(GL),
                     str(GQ),
                     str(QUAL)]
                    breakpointStart = np.meanalelle_sort[(-2)][0]
                    CIPOS = cal_CIPOSnp.stdalelle_sort[(-2)][0]len(alelle_sort[(-2)][0])
                    search_threshold = np.minalelle_sort[(-2)][0]
                    signalLen = np.meanalelle_sort[(-2)][1]
                    signalLen_STD = np.stdalelle_sort[(-2)][1]
                    CILEN = cal_CIPOSnp.stdalelle_sort[(-2)][1]len(alelle_sort[(-2)][1])
                    if action:
                        DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, search_threshold, chr, alelle_sort[(-2)][3], max_cluster_bias, gt_round)
                    else:
                        DR = '.'
                        GT = './.'
                        GL = '.,.,.'
                        GQ = '.'
                        QUAL = '.'
                    candidate_single_SV.append[chr,
                     svtype,
                     str(int(breakpointStart)),
                     str(int(-signalLen)),
                     str(alelle_sort[(-2)][2][0]),
                     str(CIPOS),
                     str(CILEN),
                     str(DR),
                     str(GT),
                     str(GL),
                     str(GQ),
                     str(QUAL)]


def resolution_INS--- This code section failed: ---

 L. 335         0  LOAD_GLOBAL              list
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'semi_ins_cluster'

 L. 336         6  LOAD_FAST                'semi_ins_cluster'
                8  LOAD_METHOD              append
               10  LOAD_CONST               0
               12  LOAD_CONST               0
               14  LOAD_STR                 ''
               16  BUILD_LIST_3          3 
               18  CALL_METHOD_1         1  '1 positional argument'
               20  POP_TOP          

 L. 337        22  LOAD_GLOBAL              list
               24  CALL_FUNCTION_0       0  '0 positional arguments'
               26  STORE_FAST               'candidate_single_SV'

 L. 339        28  LOAD_GLOBAL              open
               30  LOAD_FAST                'path'
               32  LOAD_STR                 'r'
               34  CALL_FUNCTION_2       2  '2 positional arguments'
               36  STORE_FAST               'file'

 L. 340        38  SETUP_LOOP          256  'to 256'
               40  LOAD_FAST                'file'
               42  GET_ITER         
               44  FOR_ITER            254  'to 254'
               46  STORE_FAST               'line'

 L. 341        48  LOAD_FAST                'line'
               50  LOAD_METHOD              strip
               52  LOAD_STR                 '\n'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  LOAD_METHOD              split
               58  LOAD_STR                 '\t'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  STORE_FAST               'seq'

 L. 342        64  LOAD_FAST                'seq'
               66  LOAD_CONST               1
               68  BINARY_SUBSCR    
               70  LOAD_FAST                'chr'
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE    78  'to 78'

 L. 343        76  CONTINUE             44  'to 44'
             78_0  COME_FROM            74  '74'

 L. 345        78  LOAD_GLOBAL              int
               80  LOAD_FAST                'seq'
               82  LOAD_CONST               2
               84  BINARY_SUBSCR    
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  STORE_FAST               'pos'

 L. 346        90  LOAD_GLOBAL              int
               92  LOAD_FAST                'seq'
               94  LOAD_CONST               3
               96  BINARY_SUBSCR    
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  STORE_FAST               'indel_len'

 L. 347       102  LOAD_FAST                'seq'
              104  LOAD_CONST               4
              106  BINARY_SUBSCR    
              108  STORE_FAST               'read_id'

 L. 349       110  LOAD_FAST                'pos'
              112  LOAD_FAST                'semi_ins_cluster'
              114  LOAD_CONST               -1
              116  BINARY_SUBSCR    
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  BINARY_SUBTRACT  
              124  LOAD_FAST                'max_cluster_bias'
              126  COMPARE_OP               >
              128  POP_JUMP_IF_FALSE   236  'to 236'

 L. 350       130  LOAD_GLOBAL              len
              132  LOAD_FAST                'semi_ins_cluster'
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  LOAD_FAST                'read_count'
              138  COMPARE_OP               >=
              140  POP_JUMP_IF_FALSE   214  'to 214'

 L. 351       142  LOAD_FAST                'semi_ins_cluster'
              144  LOAD_CONST               -1
              146  BINARY_SUBSCR    
              148  LOAD_CONST               0
              150  BINARY_SUBSCR    
              152  LOAD_FAST                'semi_ins_cluster'
              154  LOAD_CONST               -1
              156  BINARY_SUBSCR    
              158  LOAD_CONST               1
              160  BINARY_SUBSCR    
              162  DUP_TOP          
              164  ROT_THREE        
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   178  'to 178'
              170  LOAD_CONST               0
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   184  'to 184'
              176  JUMP_ABSOLUTE       214  'to 214'
            178_0  COME_FROM           168  '168'
              178  POP_TOP          
              180  JUMP_FORWARD        184  'to 184'

 L. 352       182  JUMP_FORWARD        214  'to 214'
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           174  '174'

 L. 354       184  LOAD_GLOBAL              generate_ins_cluster
              186  LOAD_FAST                'semi_ins_cluster'

 L. 355       188  LOAD_FAST                'chr'

 L. 356       190  LOAD_FAST                'svtype'

 L. 357       192  LOAD_FAST                'read_count'

 L. 358       194  LOAD_FAST                'threshold_gloab'

 L. 359       196  LOAD_FAST                'threshold_local'

 L. 360       198  LOAD_FAST                'minimum_support_reads'

 L. 361       200  LOAD_FAST                'candidate_single_SV'

 L. 362       202  LOAD_FAST                'bam_path'

 L. 363       204  LOAD_FAST                'max_cluster_bias'

 L. 364       206  LOAD_FAST                'action'

 L. 365       208  LOAD_FAST                'gt_round'
              210  CALL_FUNCTION_12     12  '12 positional arguments'
              212  POP_TOP          
            214_0  COME_FROM           182  '182'
            214_1  COME_FROM           140  '140'

 L. 366       214  BUILD_LIST_0          0 
              216  STORE_FAST               'semi_ins_cluster'

 L. 367       218  LOAD_FAST                'semi_ins_cluster'
              220  LOAD_METHOD              append
              222  LOAD_FAST                'pos'
              224  LOAD_FAST                'indel_len'
              226  LOAD_FAST                'read_id'
              228  BUILD_LIST_3          3 
              230  CALL_METHOD_1         1  '1 positional argument'
              232  POP_TOP          
              234  JUMP_BACK            44  'to 44'
            236_0  COME_FROM           128  '128'

 L. 369       236  LOAD_FAST                'semi_ins_cluster'
              238  LOAD_METHOD              append
              240  LOAD_FAST                'pos'
              242  LOAD_FAST                'indel_len'
              244  LOAD_FAST                'read_id'
              246  BUILD_LIST_3          3 
              248  CALL_METHOD_1         1  '1 positional argument'
              250  POP_TOP          
              252  JUMP_BACK            44  'to 44'
              254  POP_BLOCK        
            256_0  COME_FROM_LOOP       38  '38'

 L. 371       256  LOAD_GLOBAL              len
              258  LOAD_FAST                'semi_ins_cluster'
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  LOAD_FAST                'read_count'
              264  COMPARE_OP               >=
          266_268  POP_JUMP_IF_FALSE   346  'to 346'

 L. 372       270  LOAD_FAST                'semi_ins_cluster'
              272  LOAD_CONST               -1
              274  BINARY_SUBSCR    
              276  LOAD_CONST               0
              278  BINARY_SUBSCR    
              280  LOAD_FAST                'semi_ins_cluster'
              282  LOAD_CONST               -1
              284  BINARY_SUBSCR    
              286  LOAD_CONST               1
              288  BINARY_SUBSCR    
              290  DUP_TOP          
              292  ROT_THREE        
              294  COMPARE_OP               ==
          296_298  POP_JUMP_IF_FALSE   310  'to 310'
              300  LOAD_CONST               0
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   316  'to 316'
              308  JUMP_FORWARD        314  'to 314'
            310_0  COME_FROM           296  '296'
              310  POP_TOP          
              312  JUMP_FORWARD        316  'to 316'
            314_0  COME_FROM           308  '308'

 L. 373       314  JUMP_FORWARD        346  'to 346'
            316_0  COME_FROM           312  '312'
            316_1  COME_FROM           304  '304'

 L. 375       316  LOAD_GLOBAL              generate_ins_cluster
              318  LOAD_FAST                'semi_ins_cluster'

 L. 376       320  LOAD_FAST                'chr'

 L. 377       322  LOAD_FAST                'svtype'

 L. 378       324  LOAD_FAST                'read_count'

 L. 379       326  LOAD_FAST                'threshold_gloab'

 L. 380       328  LOAD_FAST                'threshold_local'

 L. 381       330  LOAD_FAST                'minimum_support_reads'

 L. 382       332  LOAD_FAST                'candidate_single_SV'

 L. 383       334  LOAD_FAST                'bam_path'

 L. 384       336  LOAD_FAST                'max_cluster_bias'

 L. 385       338  LOAD_FAST                'action'

 L. 386       340  LOAD_FAST                'gt_round'
              342  CALL_FUNCTION_12     12  '12 positional arguments'
              344  POP_TOP          
            346_0  COME_FROM           314  '314'
            346_1  COME_FROM           266  '266'

 L. 387       346  LOAD_FAST                'file'
              348  LOAD_METHOD              close
              350  CALL_METHOD_0         0  '0 positional arguments'
              352  POP_TOP          

 L. 388       354  LOAD_FAST                'candidate_single_SV'
              356  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 178


def generate_ins_cluster(semi_ins_cluster, chr, svtype, read_count, threshold_gloab, threshold_local, minimum_support_reads, candidate_single_SV, bam_path, max_cluster_bias, action, gt_round):
    """
        generate deletion
        *************************************************************
        threshold_gloab         threshold_local         minimum_support_reads
        -------------------------------------------------------------
                0.2                                     0.6                                     5               CLR
                0.65                            0.7                               <=5           CCS
        *************************************************************
        """
    read_tag = dict
    for element in semi_ins_cluster:
        if element[2] not in read_tag:
            read_tag[element[2]] = element

    if len(read_tag) < read_count:
        return
        read_tag2SortedList = sorted((list(read_tag.values)), key=(lambda x: x[1]))
        global_len = [i[1] for i in read_tag2SortedList]
        DISCRETE_THRESHOLD_LEN_CLUSTER_INS_TEMP = threshold_gloab * np.meanglobal_len
        last_len = read_tag2SortedList[0][1]
        alelle_collect = list
        alelle_collect.append[[read_tag2SortedList[0][0]], [read_tag2SortedList[0][1]], [],
         [
          read_tag2SortedList[0][2]]]
        for i in read_tag2SortedList[1:]:
            if i[1] - last_len > DISCRETE_THRESHOLD_LEN_CLUSTER_INS_TEMP:
                alelle_collect[(-1)][2].appendlen(alelle_collect[(-1)][0])
                alelle_collect.append[[], [], [], []]
            alelle_collect[(-1)][0].appendi[0]
            alelle_collect[(-1)][1].appendi[1]
            alelle_collect[(-1)][3].appendi[2]
            last_len = i[1]

        alelle_collect[(-1)][2].appendlen(alelle_collect[(-1)][0])
        alelle_sort = sorted(alelle_collect, key=(lambda x: x[2]))
        if alelle_sort[(-1)][2][0] >= minimum_support_reads and float(alelle_sort[(-1)][2][0] * 1.0 / len(read_tag)) >= threshold_local:
            breakpointStart = np.meanalelle_sort[(-1)][0]
            CIPOS = cal_CIPOSnp.stdalelle_sort[(-1)][0]len(alelle_sort[(-1)][0])
            signalLen = np.meanalelle_sort[(-1)][1]
            signalLen_STD = np.stdalelle_sort[(-1)][1]
            CILEN = cal_CIPOSnp.stdalelle_sort[(-1)][1]len(alelle_sort[(-1)][1])
            if action:
                DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, int(breakpointStart), chr, alelle_sort[(-1)][3], max_cluster_bias, gt_round)
    else:
        DR = '.'
        GT = './.'
        GL = '.,.,.'
        GQ = '.'
        QUAL = '.'
    candidate_single_SV.append[chr,
     svtype,
     str(int(breakpointStart)),
     str(int(signalLen)),
     str(alelle_sort[(-1)][2][0]),
     str(CIPOS),
     str(CILEN),
     str(DR),
     str(GT),
     str(GL),
     str(GQ),
     str(QUAL)]
    if len(alelle_sort) > 1:
        if alelle_sort[(-2)][2][0] >= minimum_support_reads:
            if alelle_sort[(-2)][2][0] + alelle_sort[(-1)][2][0] >= 0.95 * len(read_tag):
                if alelle_sort[(-2)][2][0] >= 0.3 * len(read_tag):
                    breakpointStart = np.meanalelle_sort[(-2)][0]
                    CIPOS = cal_CIPOSnp.stdalelle_sort[(-2)][0]len(alelle_sort[(-2)][0])
                    signalLen = np.meanalelle_sort[(-2)][1]
                    last_signalLen_STD = signalLen_STD
                    signalLen_STD = np.stdalelle_sort[(-2)][1]
                    CILEN = cal_CIPOSnp.stdalelle_sort[(-2)][1]len(alelle_sort[(-2)][1])
                    if signalLen_STD < last_signalLen_STD:
                        if action:
                            DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, int(breakpointStart), chr, alelle_sort[(-2)][3], max_cluster_bias, gt_round)
                        else:
                            DR = '.'
                            GT = './.'
                            GL = '.,.,.'
                            GQ = '.'
                            QUAL = '.'
                        candidate_single_SV.append[chr,
                         svtype,
                         str(int(breakpointStart)),
                         str(int(signalLen)),
                         str(alelle_sort[(-2)][2][0]),
                         str(CIPOS),
                         str(CILEN),
                         str(DR),
                         str(GT),
                         str(GL),
                         str(GQ),
                         str(QUAL)]
                    else:
                        if alelle_sort[(-2)][2][0] >= minimum_support_reads:
                            if alelle_sort[(-2)][2][0] + alelle_sort[(-1)][2][0] >= 0.95 * len(read_tag):
                                if alelle_sort[(-2)][2][0] >= 0.4 * len(read_tag):
                                    breakpointStart = np.meanalelle_sort[(-1)][0]
                                    CIPOS = cal_CIPOSnp.stdalelle_sort[(-1)][0]len(alelle_sort[(-1)][0])
                                    signalLen = np.meanalelle_sort[(-1)][1]
                                    signalLen_STD = np.stdalelle_sort[(-1)][1]
                                    CILEN = cal_CIPOSnp.stdalelle_sort[(-1)][1]len(alelle_sort[(-1)][1])
                                    if action:
                                        DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, int(breakpointStart), chr, alelle_sort[(-1)][3], max_cluster_bias, gt_round)
                                    else:
                                        DR = '.'
                                        GT = './.'
                                        GL = '.,.,.'
                                        GQ = '.'
                                        QUAL = '.'
                                    candidate_single_SV.append[chr,
                                     svtype,
                                     str(int(breakpointStart)),
                                     str(int(signalLen)),
                                     str(alelle_sort[(-1)][2][0]),
                                     str(CIPOS),
                                     str(CILEN),
                                     str(DR),
                                     str(GT),
                                     str(GL),
                                     str(GQ),
                                     str(QUAL)]
                                    breakpointStart = np.meanalelle_sort[(-2)][0]
                                    CIPOS = cal_CIPOSnp.stdalelle_sort[(-2)][0]len(alelle_sort[(-2)][0])
                                    signalLen = np.meanalelle_sort[(-2)][1]
                                    signalLen_STD = np.stdalelle_sort[(-2)][1]
                                    CILEN = cal_CIPOSnp.stdalelle_sort[(-2)][1]len(alelle_sort[(-2)][1])
                                    if action:
                                        DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, int(breakpointStart), chr, alelle_sort[(-2)][3], max_cluster_bias, gt_round)
                                    else:
                                        DR = '.'
                                        GT = './.'
                                        GL = '.,.,.'
                                        GQ = '.'
                                        QUAL = '.'
                                    candidate_single_SV.append[chr,
                                     svtype,
                                     str(int(breakpointStart)),
                                     str(int(signalLen)),
                                     str(alelle_sort[(-2)][2][0]),
                                     str(CIPOS),
                                     str(CILEN),
                                     str(DR),
                                     str(GT),
                                     str(GL),
                                     str(GQ),
                                     str(QUAL)]


def run_del(args):
    return resolution_DEL(*args)


def run_ins(args):
    return resolution_INS(*args)


def call_gt(bam_path, search_threshold, chr, read_id_list, max_cluster_bias, gt_round):
    import pysam
    querydata = set
    bamfile = pysam.AlignmentFilebam_path
    search_start = max(int(search_threshold) - max_cluster_bias)0
    search_end = min(int(search_threshold) + max_cluster_bias)bamfile.get_reference_lengthchr
    up_bound = threshold_ref_count(len(read_id_list))
    status = count_coverage(chr, search_start, search_end, bamfile, querydata, up_bound, gt_round)
    bamfile.close
    if status == -1:
        DR = '.'
        GT = './.'
        GL = '.,.,.'
        GQ = '.'
        QUAL = '.'
    else:
        DR = 0
        for query in querydata:
            if query not in read_id_list:
                DR += 1

        GT, GL, GQ, QUAL = cal_GLDRlen(read_id_list)
    return (
     len(read_id_list), DR, GT, GL, GQ, QUAL)