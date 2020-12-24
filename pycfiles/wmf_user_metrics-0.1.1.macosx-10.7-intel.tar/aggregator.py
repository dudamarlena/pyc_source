# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/src/etl/aggregator.py
# Compiled at: 2013-01-30 18:14:09
"""
    This module contains methods that provide functionality for aggregating
    metrics data.
"""
__author__ = 'ryan faulkner'
__date__ = '12/12/2012'
__license__ = 'GPL (version 2 or later)'
from itertools import izip
from numpy import array

def decorator_builder(header):
    """
        Decorator method to annotate aggregation methods to ensure the correct
        data model is exposed by.
    """

    def eval_data_model(f):

        def wrapper(metric, **kwargs):
            if hasattr(metric, 'header'):
                header_arg = metric.header()
                if all(header_arg[i] == header[i] for i in range(len(header) - 1)):
                    return f(metric, **kwargs)
            else:
                raise AggregatorException('This aggregator (%s) does not operate on this ' + 'data type.' % f.__name__)

        return wrapper

    return eval_data_model


def identity(x):
    """ The identity aggregator - returns whatever was put in """
    return x


def list_sum_indices(l, indices):
    """
        Sums the elements of list indicated by numeric list `indices`.  The
        elements must be summable (i.e. e1 + e2 is allowed for all e1 and e2).

        Returns: <list of summed elements>

        e.g.
        >>> l = [['1',1,50],['2',4,1],['3',2,6]]
        >>> list_sum_indices(l,[1,2])
        [7, 57]
    """
    return list(reduce(lambda x, y: x + y, [ array([ elem.__getitem__(i) for i in indices ]) for elem in l ]))


def list_sum_by_group(l, group_index):
    """
        Sums the elements of list keyed on `key_index`. The elements must be
        summable (i.e. e1 + e2 is allowed for all e1 and e2).  All elements
        outside of key are summed on matching keys.

        Returns: <list of summed and keyed elements>

        e.g.
        >>> l = [[2,1],[1,4],[2,2]]
        >>> list_sum_by_group(l,0)
        [[1,4], [2,3]]
    """
    d = dict()
    for i in l:
        summables = i[:group_index] + i[group_index + 1:]
        if d.has_key(i[group_index]):
            d[i[group_index]] = map(sum, izip(summables, d[i[group_index]]))
        else:
            d[i[group_index]] = summables

    return [ d[k][:group_index] + [k] + d[k][group_index:] for k in d ]


def list_average_by_group(l, group_index):
    """
        Computes the average of the elements of list keyed on `key_index`.
        The elements must be summable (i.e. e1 + e2 is allowed for all e1 and
        e2).  All elements outside of key are summed on matching keys. This
        duplicates the code of `list_sum_by_group` since it needs to compute
        counts in the loop also.

        Returns: <list of averaged and keyed elements>

        e.g.
        >>> l = [[2,1],[1,4],[2,2]]
        >>> list_average(l,0)
        [[1, 4.0], [2, 1.5]]
    """
    d = dict()
    counts = dict()
    for i in l:
        summables = i[:group_index] + i[group_index + 1:]
        if d.has_key(i[group_index]):
            d[i[group_index]] = map(sum, izip(summables, d[i[group_index]]))
            counts[i[group_index]] += 1
        else:
            d[i[group_index]] = summables
            counts[i[group_index]] = 1

    for k in counts:
        d[k] = list(array(d[k]) / float(counts[k]))

    return [ d[k][:group_index] + [k] + d[k][group_index:] for k in d ]


def cmp_method_default(x):
    return x > 0


def boolean_rate--- This code section failed: ---

 L. 117         0  LOAD_CONST               'val_idx'
                3  LOAD_FAST             1  'kwargs'
                6  COMPARE_OP            6  in
                9  POP_JUMP_IF_FALSE    22  'to 22'
               12  LOAD_FAST             1  'kwargs'
               15  LOAD_CONST               'val_idx'
               18  BINARY_SUBSCR    
               19  JUMP_FORWARD          3  'to 25'
               22  LOAD_CONST               1
             25_0  COME_FROM            19  '19'
               25  STORE_FAST            2  'val_idx'

 L. 118        28  LOAD_CONST               'cmp_method'
               31  LOAD_FAST             1  'kwargs'
               34  COMPARE_OP            6  in
               37  POP_JUMP_IF_FALSE    50  'to 50'
               40  LOAD_FAST             1  'kwargs'
               43  LOAD_CONST               'cmp_method'
               46  BINARY_SUBSCR    
               47  JUMP_FORWARD          3  'to 53'
               50  LOAD_GLOBAL           0  'cmp_method_default'
             53_0  COME_FROM            47  '47'
               53  STORE_FAST            3  'cmp_method'

 L. 120        56  LOAD_CONST               0
               59  STORE_FAST            4  'total'

 L. 121        62  LOAD_CONST               0
               65  STORE_FAST            5  'pos'

 L. 122        68  SETUP_LOOP          105  'to 176'
               71  LOAD_FAST             0  'iter'
               74  LOAD_ATTR             1  '__iter__'
               77  CALL_FUNCTION_0       0  None
               80  GET_ITER         
               81  FOR_ITER             91  'to 175'
               84  STORE_FAST            6  'r'

 L. 123        87  SETUP_EXCEPT         43  'to 133'

 L. 124        90  LOAD_FAST             3  'cmp_method'
               93  LOAD_FAST             6  'r'
               96  LOAD_FAST             2  'val_idx'
               99  BINARY_SUBSCR    
              100  CALL_FUNCTION_1       1  None
              103  POP_JUMP_IF_FALSE   119  'to 119'
              106  LOAD_FAST             5  'pos'
              109  LOAD_CONST               1
              112  INPLACE_ADD      
              113  STORE_FAST            5  'pos'
              116  JUMP_FORWARD          0  'to 119'
            119_0  COME_FROM           116  '116'

 L. 125       119  LOAD_FAST             4  'total'
              122  LOAD_CONST               1
              125  INPLACE_ADD      
              126  STORE_FAST            4  'total'
              129  POP_BLOCK        
              130  JUMP_BACK            81  'to 81'
            133_0  COME_FROM            87  '87'

 L. 126       133  DUP_TOP          
              134  LOAD_GLOBAL           2  'IndexError'
              137  COMPARE_OP           10  exception-match
              140  POP_JUMP_IF_FALSE   152  'to 152'
              143  POP_TOP          
              144  POP_TOP          
              145  POP_TOP          
              146  JUMP_BACK            81  'to 81'
              149  JUMP_BACK            81  'to 81'

 L. 127       152  DUP_TOP          
              153  LOAD_GLOBAL           3  'TypeError'
              156  COMPARE_OP           10  exception-match
              159  POP_JUMP_IF_FALSE   171  'to 171'
              162  POP_TOP          
              163  POP_TOP          
              164  POP_TOP          
              165  CONTINUE             81  'to 81'
              168  JUMP_BACK            81  'to 81'
              171  END_FINALLY      
            172_0  COME_FROM           171  '171'
              172  JUMP_BACK            81  'to 81'
              175  POP_BLOCK        
            176_0  COME_FROM            68  '68'

 L. 128       176  LOAD_FAST             4  'total'
              179  POP_JUMP_IF_FALSE   205  'to 205'

 L. 129       182  LOAD_FAST             4  'total'
              185  LOAD_FAST             5  'pos'
              188  LOAD_GLOBAL           4  'float'
              191  LOAD_FAST             5  'pos'
              194  CALL_FUNCTION_1       1  None
              197  LOAD_FAST             4  'total'
              200  BINARY_DIVIDE    
              201  BUILD_LIST_3          3 
              204  RETURN_END_IF    
            205_0  COME_FROM           179  '179'

 L. 131       205  LOAD_FAST             4  'total'
              208  LOAD_FAST             5  'pos'
              211  LOAD_CONST               0.0
              214  BUILD_LIST_3          3 
              217  RETURN_VALUE     

Parse error at or near `JUMP_BACK' instruction at offset 149


def weight_method_default(x):
    return 1


def weighted_rate--- This code section failed: ---

 L. 138         0  LOAD_CONST               'weight_idx'
                3  LOAD_FAST             1  'kwargs'
                6  COMPARE_OP            6  in
                9  POP_JUMP_IF_FALSE    22  'to 22'
               12  LOAD_FAST             1  'kwargs'
               15  LOAD_CONST               'weight_idx'
               18  BINARY_SUBSCR    
               19  JUMP_FORWARD          3  'to 25'
               22  LOAD_CONST               1
             25_0  COME_FROM            19  '19'
               25  STORE_FAST            2  'weight_idx'

 L. 139        28  LOAD_CONST               'val_idx'
               31  LOAD_FAST             1  'kwargs'
               34  COMPARE_OP            6  in
               37  POP_JUMP_IF_FALSE    50  'to 50'
               40  LOAD_FAST             1  'kwargs'
               43  LOAD_CONST               'val_idx'
               46  BINARY_SUBSCR    
               47  JUMP_FORWARD          3  'to 53'
               50  LOAD_CONST               1
             53_0  COME_FROM            47  '47'
               53  STORE_FAST            3  'val_idx'

 L. 140        56  LOAD_CONST               'cmp_method'
               59  LOAD_FAST             1  'kwargs'
               62  COMPARE_OP            6  in
               65  POP_JUMP_IF_FALSE    78  'to 78'
               68  LOAD_FAST             1  'kwargs'
               71  LOAD_CONST               'weight_method'
               74  BINARY_SUBSCR    
               75  JUMP_FORWARD          3  'to 81'
               78  LOAD_GLOBAL           0  'weight_method_default'
             81_0  COME_FROM            75  '75'
               81  STORE_FAST            4  'weight_method'

 L. 142        84  LOAD_CONST               0
               87  STORE_FAST            5  'count'

 L. 143        90  LOAD_CONST               0.0
               93  STORE_FAST            6  'total_weight'

 L. 144        96  LOAD_CONST               0.0
               99  STORE_FAST            7  'weighted_sum'

 L. 145       102  SETUP_LOOP          124  'to 229'
              105  LOAD_FAST             0  'iter'
              108  LOAD_ATTR             1  '__iter__'
              111  CALL_FUNCTION_0       0  None
              114  GET_ITER         
              115  FOR_ITER            110  'to 228'
              118  STORE_FAST            8  'r'

 L. 146       121  SETUP_EXCEPT         62  'to 186'

 L. 147       124  LOAD_FAST             5  'count'
              127  LOAD_CONST               1
              130  INPLACE_ADD      
              131  STORE_FAST            5  'count'

 L. 148       134  LOAD_FAST             4  'weight_method'
              137  LOAD_FAST             8  'r'
              140  LOAD_FAST             2  'weight_idx'
              143  BINARY_SUBSCR    
              144  CALL_FUNCTION_1       1  None
              147  STORE_FAST            9  'weight'

 L. 149       150  LOAD_FAST             6  'total_weight'
              153  LOAD_FAST             8  'r'
              156  LOAD_FAST             2  'weight_idx'
              159  BINARY_SUBSCR    
              160  INPLACE_ADD      
              161  STORE_FAST            6  'total_weight'

 L. 150       164  LOAD_FAST             7  'weighted_sum'
              167  LOAD_FAST             9  'weight'
              170  LOAD_FAST             8  'r'
              173  LOAD_FAST             3  'val_idx'
              176  BINARY_SUBSCR    
              177  BINARY_MULTIPLY  
              178  INPLACE_ADD      
              179  STORE_FAST            7  'weighted_sum'
              182  POP_BLOCK        
              183  JUMP_BACK           115  'to 115'
            186_0  COME_FROM           121  '121'

 L. 151       186  DUP_TOP          
              187  LOAD_GLOBAL           2  'IndexError'
              190  COMPARE_OP           10  exception-match
              193  POP_JUMP_IF_FALSE   205  'to 205'
              196  POP_TOP          
              197  POP_TOP          
              198  POP_TOP          
              199  JUMP_BACK           115  'to 115'
              202  JUMP_BACK           115  'to 115'

 L. 152       205  DUP_TOP          
              206  LOAD_GLOBAL           3  'TypeError'
              209  COMPARE_OP           10  exception-match
              212  POP_JUMP_IF_FALSE   224  'to 224'
              215  POP_TOP          
              216  POP_TOP          
              217  POP_TOP          
              218  CONTINUE            115  'to 115'
              221  JUMP_BACK           115  'to 115'
              224  END_FINALLY      
            225_0  COME_FROM           224  '224'
              225  JUMP_BACK           115  'to 115'
              228  POP_BLOCK        
            229_0  COME_FROM           102  '102'

 L. 153       229  LOAD_FAST             5  'count'
              232  POP_JUMP_IF_FALSE   252  'to 252'

 L. 154       235  LOAD_FAST             5  'count'
              238  LOAD_FAST             6  'total_weight'
              241  LOAD_FAST             7  'weighted_sum'
              244  LOAD_FAST             5  'count'
              247  BINARY_DIVIDE    
              248  BUILD_LIST_3          3 
              251  RETURN_END_IF    
            252_0  COME_FROM           232  '232'

 L. 156       252  LOAD_FAST             5  'count'
              255  LOAD_FAST             6  'total_weight'
              258  LOAD_CONST               0.0
              261  BUILD_LIST_3          3 
              264  RETURN_VALUE     

Parse error at or near `JUMP_BACK' instruction at offset 202


class AggregatorException(Exception):
    pass