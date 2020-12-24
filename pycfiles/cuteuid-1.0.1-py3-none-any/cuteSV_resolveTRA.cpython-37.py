# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cuteSV/cuteSV_resolveTRA.py
# Compiled at: 2020-04-29 04:13:07
# Size of source mod 2**32: 8217 bytes
import sys, numpy as np
from cuteSV.cuteSV_genotype import cal_GL, threshold_ref_count, count_coverage

def resolution_TRA--- This code section failed: ---

 L.  30         0  LOAD_GLOBAL              list
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'semi_tra_cluster'

 L.  31         6  LOAD_FAST                'semi_tra_cluster'
                8  LOAD_METHOD              append
               10  LOAD_CONST               0
               12  LOAD_CONST               0
               14  LOAD_STR                 ''
               16  LOAD_STR                 'N'
               18  BUILD_LIST_4          4 
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L.  32        24  LOAD_GLOBAL              list
               26  CALL_FUNCTION_0       0  ''
               28  STORE_FAST               'candidate_single_SV'

 L.  34        30  LOAD_GLOBAL              open
               32  LOAD_FAST                'path'
               34  LOAD_STR                 'r'
               36  CALL_FUNCTION_2       2  ''
               38  STORE_FAST               'file'

 L.  35     40_42  SETUP_LOOP          300  'to 300'
               44  LOAD_FAST                'file'
               46  GET_ITER         
               48  FOR_ITER            298  'to 298'
               50  STORE_FAST               'line'

 L.  36        52  LOAD_FAST                'line'
               54  LOAD_METHOD              strip
               56  LOAD_STR                 '\n'
               58  CALL_METHOD_1         1  ''
               60  LOAD_METHOD              split
               62  LOAD_STR                 '\t'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'seq'

 L.  37        68  LOAD_FAST                'seq'
               70  LOAD_CONST               1
               72  BINARY_SUBSCR    
               74  LOAD_FAST                'chr_1'
               76  COMPARE_OP               !=
               78  POP_JUMP_IF_FALSE    82  'to 82'

 L.  38        80  CONTINUE             48  'to 48'
             82_0  COME_FROM            78  '78'

 L.  39        82  LOAD_FAST                'seq'
               84  LOAD_CONST               4
               86  BINARY_SUBSCR    
               88  LOAD_FAST                'chr_2'
               90  COMPARE_OP               !=
               92  POP_JUMP_IF_FALSE    96  'to 96'

 L.  40        94  CONTINUE             48  'to 48'
             96_0  COME_FROM            92  '92'

 L.  42        96  LOAD_GLOBAL              int
               98  LOAD_FAST                'seq'
              100  LOAD_CONST               3
              102  BINARY_SUBSCR    
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'pos_1'

 L.  43       108  LOAD_GLOBAL              int
              110  LOAD_FAST                'seq'
              112  LOAD_CONST               5
              114  BINARY_SUBSCR    
              116  CALL_FUNCTION_1       1  ''
              118  STORE_FAST               'pos_2'

 L.  44       120  LOAD_FAST                'seq'
              122  LOAD_CONST               6
              124  BINARY_SUBSCR    
              126  STORE_FAST               'read_id'

 L.  45       128  LOAD_FAST                'seq'
              130  LOAD_CONST               2
              132  BINARY_SUBSCR    
              134  STORE_FAST               'BND_type'

 L.  47       136  LOAD_FAST                'pos_1'
              138  LOAD_FAST                'semi_tra_cluster'
              140  LOAD_CONST               -1
              142  BINARY_SUBSCR    
              144  LOAD_CONST               0
              146  BINARY_SUBSCR    
              148  BINARY_SUBTRACT  
              150  LOAD_FAST                'max_cluster_bias'
              152  COMPARE_OP               >
              154  POP_JUMP_IF_TRUE    174  'to 174'
              156  LOAD_FAST                'BND_type'
              158  LOAD_FAST                'semi_tra_cluster'
              160  LOAD_CONST               -1
              162  BINARY_SUBSCR    
              164  LOAD_CONST               3
              166  BINARY_SUBSCR    
              168  COMPARE_OP               !=
          170_172  POP_JUMP_IF_FALSE   278  'to 278'
            174_0  COME_FROM           154  '154'

 L.  48       174  LOAD_GLOBAL              len
              176  LOAD_FAST                'semi_tra_cluster'
              178  CALL_FUNCTION_1       1  ''
              180  LOAD_FAST                'read_count'
              182  COMPARE_OP               >=
              184  POP_JUMP_IF_FALSE   254  'to 254'

 L.  49       186  LOAD_FAST                'semi_tra_cluster'
              188  LOAD_CONST               -1
              190  BINARY_SUBSCR    
              192  LOAD_CONST               0
              194  BINARY_SUBSCR    
              196  LOAD_FAST                'semi_tra_cluster'
              198  LOAD_CONST               -1
              200  BINARY_SUBSCR    
              202  LOAD_CONST               1
              204  BINARY_SUBSCR    
              206  DUP_TOP          
              208  ROT_THREE        
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   222  'to 222'
              214  LOAD_CONST               0
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   228  'to 228'
              220  JUMP_ABSOLUTE       254  'to 254'
            222_0  COME_FROM           212  '212'
              222  POP_TOP          
              224  JUMP_FORWARD        228  'to 228'

 L.  50       226  JUMP_FORWARD        254  'to 254'
            228_0  COME_FROM           224  '224'
            228_1  COME_FROM           218  '218'

 L.  52       228  LOAD_GLOBAL              generate_semi_tra_cluster
              230  LOAD_FAST                'semi_tra_cluster'

 L.  53       232  LOAD_FAST                'chr_1'

 L.  54       234  LOAD_FAST                'chr_2'

 L.  55       236  LOAD_FAST                'read_count'

 L.  56       238  LOAD_FAST                'overlap_size'

 L.  57       240  LOAD_FAST                'max_cluster_bias'

 L.  58       242  LOAD_FAST                'candidate_single_SV'

 L.  59       244  LOAD_FAST                'bam_path'

 L.  60       246  LOAD_FAST                'action'

 L.  61       248  LOAD_FAST                'gt_round'
              250  CALL_FUNCTION_10     10  ''
              252  POP_TOP          
            254_0  COME_FROM           226  '226'
            254_1  COME_FROM           184  '184'

 L.  62       254  BUILD_LIST_0          0 
              256  STORE_FAST               'semi_tra_cluster'

 L.  63       258  LOAD_FAST                'semi_tra_cluster'
              260  LOAD_METHOD              append
              262  LOAD_FAST                'pos_1'
              264  LOAD_FAST                'pos_2'
              266  LOAD_FAST                'read_id'
              268  LOAD_FAST                'BND_type'
              270  BUILD_LIST_4          4 
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
              276  JUMP_BACK            48  'to 48'
            278_0  COME_FROM           170  '170'

 L.  65       278  LOAD_FAST                'semi_tra_cluster'
              280  LOAD_METHOD              append
              282  LOAD_FAST                'pos_1'
              284  LOAD_FAST                'pos_2'
              286  LOAD_FAST                'read_id'
              288  LOAD_FAST                'BND_type'
              290  BUILD_LIST_4          4 
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          
              296  JUMP_BACK            48  'to 48'
              298  POP_BLOCK        
            300_0  COME_FROM_LOOP       40  '40'

 L.  67       300  LOAD_GLOBAL              len
              302  LOAD_FAST                'semi_tra_cluster'
              304  CALL_FUNCTION_1       1  ''
              306  LOAD_FAST                'read_count'
              308  COMPARE_OP               >=
          310_312  POP_JUMP_IF_FALSE   386  'to 386'

 L.  68       314  LOAD_FAST                'semi_tra_cluster'
              316  LOAD_CONST               -1
              318  BINARY_SUBSCR    
              320  LOAD_CONST               0
              322  BINARY_SUBSCR    
              324  LOAD_FAST                'semi_tra_cluster'
              326  LOAD_CONST               -1
              328  BINARY_SUBSCR    
              330  LOAD_CONST               1
              332  BINARY_SUBSCR    
              334  DUP_TOP          
              336  ROT_THREE        
              338  COMPARE_OP               ==
          340_342  POP_JUMP_IF_FALSE   354  'to 354'
              344  LOAD_CONST               0
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_FALSE   360  'to 360'
              352  JUMP_FORWARD        358  'to 358'
            354_0  COME_FROM           340  '340'
              354  POP_TOP          
              356  JUMP_FORWARD        360  'to 360'
            358_0  COME_FROM           352  '352'

 L.  69       358  JUMP_FORWARD        386  'to 386'
            360_0  COME_FROM           356  '356'
            360_1  COME_FROM           348  '348'

 L.  71       360  LOAD_GLOBAL              generate_semi_tra_cluster
              362  LOAD_FAST                'semi_tra_cluster'

 L.  72       364  LOAD_FAST                'chr_1'

 L.  73       366  LOAD_FAST                'chr_2'

 L.  74       368  LOAD_FAST                'read_count'

 L.  75       370  LOAD_FAST                'overlap_size'

 L.  76       372  LOAD_FAST                'max_cluster_bias'

 L.  77       374  LOAD_FAST                'candidate_single_SV'

 L.  78       376  LOAD_FAST                'bam_path'

 L.  79       378  LOAD_FAST                'action'

 L.  80       380  LOAD_FAST                'gt_round'
              382  CALL_FUNCTION_10     10  ''
              384  POP_TOP          
            386_0  COME_FROM           358  '358'
            386_1  COME_FROM           310  '310'

 L.  81       386  LOAD_FAST                'file'
              388  LOAD_METHOD              close
              390  CALL_METHOD_0         0  ''
              392  POP_TOP          

 L.  82       394  LOAD_FAST                'candidate_single_SV'
              396  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 222


def generate_semi_tra_cluster(semi_tra_cluster, chr_1, chr_2, read_count, overlap_size, max_cluster_bias, candidate_single_SV, bam_path, action, gt_round):
    BND_type = semi_tra_cluster[0][3]
    semi_tra_cluster = sorted(semi_tra_cluster, key=(lambda x: x[1]))
    read_tag = dict
    temp = list
    last_len = 0
    temp.append[0, 0, set]
    for element in semi_tra_cluster:
        if element[1] - last_len > max_cluster_bias:
            temp.append[element[0], element[1], {element[2]}]
            last_len = element[1]
        else:
            temp[(-1)][0] += element[0]
            temp[(-1)][1] += element[1]
            temp[(-1)][2].addelement[2]
            last_len = element[1]
        if element[2] not in read_tag:
            read_tag[element[2]] = 0

    if len(read_tag) < read_count:
        return
        temp = sorted(temp, key=(lambda x: -len(x[2])))
        if len(temp[1][2]) >= 0.5 * read_count:
            if len(temp[0][2]) + len(temp[1][2]) >= len(semi_tra_cluster) * overlap_size:
                BND_pos_1 = '%s:%s' % (chr_2, int(temp[0][1] / len(temp[0][2])))
                BND_pos_2 = '%s:%s' % (chr_2, int(temp[1][1] / len(temp[1][2])))
                if BND_type == 'A':
                    TRA_1 = 'N[%s[' % BND_pos_1
                    TRA_2 = 'N[%s[' % BND_pos_2
                elif BND_type == 'B':
                    TRA_1 = 'N]%s]' % BND_pos_1
                    TRA_2 = 'N]%s]' % BND_pos_2
                elif BND_type == 'C':
                    TRA_1 = '[%s[N' % BND_pos_1
                    TRA_2 = '[%s[N' % BND_pos_2
                elif BND_type == 'D':
                    TRA_1 = ']%s]N' % BND_pos_1
                    TRA_2 = ']%s]N' % BND_pos_2
                else:
                    return
                if action:
                    import time
                    DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, int(temp[0][0] / len(temp[0][2])), int(temp[0][1] / len(temp[0][2])), chr_1, chr_2, temp[0][2], max_cluster_bias, gt_round)
                else:
                    DR = '.'
                    GT = './.'
                    GL = '.,.,.'
                    GQ = '.'
                    QUAL = '.'
                candidate_single_SV.append[chr_1,
                 TRA_1,
                 str(int(temp[0][0] / len(temp[0][2]))),
                 chr_2,
                 str(int(temp[0][1] / len(temp[0][2]))),
                 str(len(temp[0][2])),
                 str(DR),
                 str(GT),
                 str(GL),
                 str(GQ),
                 str(QUAL)]
                if action:
                    import time
                    DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, int(temp[1][0] / len(temp[1][2])), int(temp[1][1] / len(temp[1][2])), chr_1, chr_2, temp[1][2], max_cluster_bias, gt_round)
                else:
                    DR = '.'
                    GT = './.'
                    GL = '.,.,.'
                    GQ = '.'
                    QUAL = '.'
                candidate_single_SV.append[chr_1,
                 TRA_2,
                 str(int(temp[1][0] / len(temp[1][2]))),
                 chr_2,
                 str(int(temp[1][1] / len(temp[1][2]))),
                 str(len(temp[1][2])),
                 str(DR),
                 str(GT),
                 str(GL),
                 str(GQ),
                 str(QUAL)]
    elif len(temp[0][2]) >= len(semi_tra_cluster) * overlap_size:
        BND_pos = '%s:%s' % (chr_2, int(temp[0][1] / len(temp[0][2])))
        if BND_type == 'A':
            TRA = 'N[%s[' % BND_pos
        elif BND_type == 'B':
            TRA = 'N]%s]' % BND_pos
        elif BND_type == 'C':
            TRA = '[%s[N' % BND_pos
        elif BND_type == 'D':
            TRA = ']%s]N' % BND_pos
        else:
            return
        if action:
            import time
            DV, DR, GT, GL, GQ, QUAL = call_gt(bam_path, int(temp[0][0] / len(temp[0][2])), int(temp[0][1] / len(temp[0][2])), chr_1, chr_2, temp[0][2], max_cluster_bias, gt_round)
        else:
            DR = '.'
            GT = './.'
            GL = '.,.,.'
            GQ = '.'
            QUAL = '.'
        candidate_single_SV.append[chr_1,
         TRA,
         str(int(temp[0][0] / len(temp[0][2]))),
         chr_2,
         str(int(temp[0][1] / len(temp[0][2]))),
         str(len(temp[0][2])),
         str(DR),
         str(GT),
         str(GL),
         str(GQ),
         str(QUAL)]


def run_tra(args):
    return resolution_TRA(*args)


def call_gt(bam_path, pos_1, pos_2, chr_1, chr_2, read_id_list, max_cluster_bias, gt_round):
    import pysam
    bamfile = pysam.AlignmentFilebam_path
    querydata = set
    search_start = max(int(pos_1) - max_cluster_bias)0
    search_end = min(int(pos_1) + max_cluster_bias)bamfile.get_reference_lengthchr_1
    up_bound = threshold_ref_count(len(read_id_list))
    status = count_coverage(chr_1, search_start, search_end, bamfile, querydata, up_bound, gt_round)
    if status == -1:
        DR = '.'
        GT = './.'
        GL = '.,.,.'
        GQ = '.'
        QUAL = '.'
    elif status == 1:
        DR = 0
        for query in querydata:
            if query not in read_id_list:
                DR += 1

        GT, GL, GQ, QUAL = cal_GLDRlen(read_id_list)
    else:
        search_start = max(int(pos_2) - max_cluster_bias)0
        search_end = min(int(pos_2) + max_cluster_bias)bamfile.get_reference_lengthchr_2
        status_2 = count_coverage(chr_2, search_start, search_end, bamfile, querydata, up_bound, gt_round)
        DR = 0
        for query in querydata:
            if query not in read_id_list:
                DR += 1

        GT, GL, GQ, QUAL = cal_GLDRlen(read_id_list)
    bamfile.close
    return (
     len(read_id_list), DR, GT, GL, GQ, QUAL)