# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cuteSV/cuteSV_resolveDUP.py
# Compiled at: 2020-04-29 04:13:06
# Size of source mod 2**32: 8951 bytes
import sys, numpy as np
from collections import Counter
from cuteSV.cuteSV_genotype import cal_GL, threshold_ref_count, count_coverage

def resolution_DUP--- This code section failed: ---

 L.  19         0  LOAD_GLOBAL              list
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'semi_dup_cluster'

 L.  20         6  LOAD_FAST                'semi_dup_cluster'
                8  LOAD_METHOD              append
               10  LOAD_CONST               0
               12  LOAD_CONST               0
               14  LOAD_STR                 ''
               16  BUILD_LIST_3          3 
               18  CALL_METHOD_1         1  '1 positional argument'
               20  POP_TOP          

 L.  21        22  LOAD_GLOBAL              list
               24  CALL_FUNCTION_0       0  '0 positional arguments'
               26  STORE_FAST               'candidate_single_SV'

 L.  23        28  LOAD_GLOBAL              open
               30  LOAD_FAST                'path'
               32  LOAD_STR                 'r'
               34  CALL_FUNCTION_2       2  '2 positional arguments'
               36  STORE_FAST               'file'

 L.  24        38  SETUP_LOOP          272  'to 272'
               40  LOAD_FAST                'file'
               42  GET_ITER         
               44  FOR_ITER            270  'to 270'
               46  STORE_FAST               'line'

 L.  25        48  LOAD_FAST                'line'
               50  LOAD_METHOD              strip
               52  LOAD_STR                 '\n'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  LOAD_METHOD              split
               58  LOAD_STR                 '\t'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  STORE_FAST               'seq'

 L.  26        64  LOAD_FAST                'seq'
               66  LOAD_CONST               1
               68  BINARY_SUBSCR    
               70  LOAD_FAST                'chr'
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE    78  'to 78'

 L.  27        76  CONTINUE             44  'to 44'
             78_0  COME_FROM            74  '74'

 L.  29        78  LOAD_GLOBAL              int
               80  LOAD_FAST                'seq'
               82  LOAD_CONST               2
               84  BINARY_SUBSCR    
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  STORE_FAST               'pos_1'

 L.  30        90  LOAD_GLOBAL              int
               92  LOAD_FAST                'seq'
               94  LOAD_CONST               3
               96  BINARY_SUBSCR    
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  STORE_FAST               'pos_2'

 L.  31       102  LOAD_FAST                'seq'
              104  LOAD_CONST               4
              106  BINARY_SUBSCR    
              108  STORE_FAST               'read_id'

 L.  33       110  LOAD_FAST                'pos_1'
              112  LOAD_FAST                'semi_dup_cluster'
              114  LOAD_CONST               -1
              116  BINARY_SUBSCR    
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  BINARY_SUBTRACT  
              124  LOAD_FAST                'max_cluster_bias'
              126  COMPARE_OP               >
              128  POP_JUMP_IF_TRUE    150  'to 150'
              130  LOAD_FAST                'pos_2'
              132  LOAD_FAST                'semi_dup_cluster'
              134  LOAD_CONST               -1
              136  BINARY_SUBSCR    
              138  LOAD_CONST               1
              140  BINARY_SUBSCR    
              142  BINARY_SUBTRACT  
              144  LOAD_FAST                'max_cluster_bias'
              146  COMPARE_OP               >
              148  POP_JUMP_IF_FALSE   252  'to 252'
            150_0  COME_FROM           128  '128'

 L.  34       150  LOAD_GLOBAL              len
              152  LOAD_FAST                'semi_dup_cluster'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  LOAD_FAST                'read_count'
              158  COMPARE_OP               >=
              160  POP_JUMP_IF_FALSE   230  'to 230'

 L.  35       162  LOAD_FAST                'semi_dup_cluster'
              164  LOAD_CONST               -1
              166  BINARY_SUBSCR    
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  LOAD_FAST                'semi_dup_cluster'
              174  LOAD_CONST               -1
              176  BINARY_SUBSCR    
              178  LOAD_CONST               1
              180  BINARY_SUBSCR    
              182  DUP_TOP          
              184  ROT_THREE        
              186  COMPARE_OP               ==
              188  POP_JUMP_IF_FALSE   198  'to 198'
              190  LOAD_CONST               0
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   204  'to 204'
              196  JUMP_ABSOLUTE       230  'to 230'
            198_0  COME_FROM           188  '188'
              198  POP_TOP          
              200  JUMP_FORWARD        204  'to 204'

 L.  36       202  JUMP_FORWARD        230  'to 230'
            204_0  COME_FROM           200  '200'
            204_1  COME_FROM           194  '194'

 L.  42       204  LOAD_GLOBAL              generate_dup_cluster
              206  LOAD_FAST                'semi_dup_cluster'

 L.  43       208  LOAD_FAST                'chr'

 L.  44       210  LOAD_FAST                'read_count'

 L.  45       212  LOAD_FAST                'max_cluster_bias'

 L.  46       214  LOAD_FAST                'sv_size'

 L.  47       216  LOAD_FAST                'candidate_single_SV'

 L.  48       218  LOAD_FAST                'bam_path'

 L.  49       220  LOAD_FAST                'action'

 L.  50       222  LOAD_FAST                'MaxSize'

 L.  51       224  LOAD_FAST                'gt_round'
              226  CALL_FUNCTION_10     10  '10 positional arguments'
              228  POP_TOP          
            230_0  COME_FROM           202  '202'
            230_1  COME_FROM           160  '160'

 L.  52       230  BUILD_LIST_0          0 
              232  STORE_FAST               'semi_dup_cluster'

 L.  53       234  LOAD_FAST                'semi_dup_cluster'
              236  LOAD_METHOD              append
              238  LOAD_FAST                'pos_1'
              240  LOAD_FAST                'pos_2'
              242  LOAD_FAST                'read_id'
              244  BUILD_LIST_3          3 
              246  CALL_METHOD_1         1  '1 positional argument'
              248  POP_TOP          
              250  JUMP_BACK            44  'to 44'
            252_0  COME_FROM           148  '148'

 L.  55       252  LOAD_FAST                'semi_dup_cluster'
              254  LOAD_METHOD              append
              256  LOAD_FAST                'pos_1'
              258  LOAD_FAST                'pos_2'
              260  LOAD_FAST                'read_id'
              262  BUILD_LIST_3          3 
              264  CALL_METHOD_1         1  '1 positional argument'
              266  POP_TOP          
              268  JUMP_BACK            44  'to 44'
              270  POP_BLOCK        
            272_0  COME_FROM_LOOP       38  '38'

 L.  57       272  LOAD_GLOBAL              len
              274  LOAD_FAST                'semi_dup_cluster'
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  LOAD_FAST                'read_count'
              280  COMPARE_OP               >=
          282_284  POP_JUMP_IF_FALSE   358  'to 358'

 L.  58       286  LOAD_FAST                'semi_dup_cluster'
              288  LOAD_CONST               -1
              290  BINARY_SUBSCR    
              292  LOAD_CONST               0
              294  BINARY_SUBSCR    
              296  LOAD_FAST                'semi_dup_cluster'
              298  LOAD_CONST               -1
              300  BINARY_SUBSCR    
              302  LOAD_CONST               1
              304  BINARY_SUBSCR    
              306  DUP_TOP          
              308  ROT_THREE        
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   326  'to 326'
              316  LOAD_CONST               0
              318  COMPARE_OP               ==
          320_322  POP_JUMP_IF_FALSE   332  'to 332'
              324  JUMP_FORWARD        330  'to 330'
            326_0  COME_FROM           312  '312'
              326  POP_TOP          
              328  JUMP_FORWARD        332  'to 332'
            330_0  COME_FROM           324  '324'

 L.  59       330  JUMP_FORWARD        358  'to 358'
            332_0  COME_FROM           328  '328'
            332_1  COME_FROM           320  '320'

 L.  65       332  LOAD_GLOBAL              generate_dup_cluster
              334  LOAD_FAST                'semi_dup_cluster'

 L.  66       336  LOAD_FAST                'chr'

 L.  67       338  LOAD_FAST                'read_count'

 L.  68       340  LOAD_FAST                'max_cluster_bias'

 L.  69       342  LOAD_FAST                'sv_size'

 L.  70       344  LOAD_FAST                'candidate_single_SV'

 L.  71       346  LOAD_FAST                'bam_path'

 L.  72       348  LOAD_FAST                'action'

 L.  73       350  LOAD_FAST                'MaxSize'

 L.  74       352  LOAD_FAST                'gt_round'
              354  CALL_FUNCTION_10     10  '10 positional arguments'
              356  POP_TOP          
            358_0  COME_FROM           330  '330'
            358_1  COME_FROM           282  '282'

 L.  75       358  LOAD_FAST                'file'
              360  LOAD_METHOD              close
              362  CALL_METHOD_0         0  '0 positional arguments'
              364  POP_TOP          

 L.  76       366  LOAD_FAST                'candidate_single_SV'
              368  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 198


def generate_dup_cluster(semi_dup_cluster, chr, read_count, max_cluster_bias, sv_size, candidate_single_SV, bam_path, action, MaxSize, gt_round):
    support_read = list(set([i[2] for i in semi_dup_cluster]))
    if len(support_read) < read_count:
        return
    else:
        low_b = int(len(semi_dup_cluster) * 0.4)
        up_b = int(len(semi_dup_cluster) * 0.6)
        if low_b == up_b:
            breakpoint_1 = semi_dup_cluster[low_b][0]
            breakpoint_2 = semi_dup_cluster[low_b][1]
        else:
            breakpoint_1 = [i[0] for i in semi_dup_cluster[low_b:up_b]]
            breakpoint_2 = [i[1] for i in semi_dup_cluster[low_b:up_b]]
            breakpoint_1 = int(sum(breakpoint_1) / len(semi_dup_cluster[low_b:up_b]))
            breakpoint_2 = int(sum(breakpoint_2) / len(semi_dup_cluster[low_b:up_b]))
        if sv_size <= breakpoint_2 - breakpoint_1 <= MaxSize:
            if action:
                import time
                DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, breakpoint_1, breakpoint_2, chr, support_read, minmax_cluster_bias(breakpoint_2 - breakpoint_1), gt_round)
            else:
                DR = '.'
                GT = './.'
                GL = '.,.,.'
                GQ = '.'
                QUAL = '.'
            candidate_single_SV.append[chr,
             'DUP',
             str(breakpoint_1),
             str(breakpoint_2 - breakpoint_1),
             str(len(support_read)),
             str(DR),
             str(GT),
             str(GL),
             str(GQ),
             str(QUAL)]


def run_dup(args):
    return resolution_DUP(*args)


def call_gt(bam_path, pos_1, pos_2, chr, read_id_list, max_cluster_bias, gt_round):
    import pysam
    bamfile = pysam.AlignmentFilebam_path
    querydata = set
    search_start = maxint(pos_1 - max_cluster_bias / 2)0
    search_end = minint(pos_1 + max_cluster_bias / 2)bamfile.get_reference_lengthchr
    up_bound = threshold_ref_count(len(read_id_list))
    status = count_coverage(chr, search_start, search_end, bamfile, querydata, up_bound, gt_round)
    if status == -1:
        DR = '.'
        GT = './.'
        GL = '.,.,.'
        GQ = '.'
        QUAL = '.'
    else:
        if status == 1:
            DR = 0
            for query in querydata:
                if query not in read_id_list:
                    DR += 1

            GT, GL, GQ, QUAL = cal_GLDRlen(read_id_list)
        else:
            search_start = maxint(pos_2 - max_cluster_bias / 2)0
            search_end = minint(pos_2 + max_cluster_bias / 2)bamfile.get_reference_lengthchr
            status_2 = count_coverage(chr, search_start, search_end, bamfile, querydata, up_bound, gt_round)
            DR = 0
            for query in querydata:
                if query not in read_id_list:
                    DR += 1

            GT, GL, GQ, QUAL = cal_GLDRlen(read_id_list)
    bamfile.close
    return (len(read_id_list), DR, GT, GL, GQ, QUAL)