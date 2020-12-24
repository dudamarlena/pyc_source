# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/src/metrics/namespace_of_edits.py
# Compiled at: 2013-01-30 13:44:04
__author__ = 'Ryan Faulkner'
__email__ = 'rfaulkner@wikimedia.org'
__date__ = 'January 6th, 2013'
__license__ = 'GPL (version 2 or later)'
import user_metric as um, src.utils.multiprocessing_wrapper as mpw
from src.etl.data_loader import Connector, DataLoader
from collections import namedtuple, OrderedDict
from src.etl.aggregator import decorator_builder
from config import logging
from os import getpid
NamespaceEditsArgsClass = namedtuple('NamespaceEditsArgs', 'project log date_start date_end')

class NamespaceEdits(um.UserMetric):
    """
        Skeleton class for "namespace of edits" metric:

            `https://meta.wikimedia.org/wiki/Research:Metrics/revert_rate`

        As a UserMetric type this class utilizes the process() function attribute to produce an internal list of metrics by
        user handle (typically ID but user names may also be specified). The execution of process() produces a nested list that
        stores in each element:

            * User ID
            * Dictionary of namespace edit counts

        For example to produce the above datapoint for a user id one could call: ::

            >>> from src.metrics.namespace_of_edits import NamespaceEdits
            >>> users = ['17792132', '17797320', '17792130', '17792131', '17792136', 13234584, 156171]
            >>> n = NamespaceEdits(date_start='20110101000000')
            >>> for r in r.process(users, log=True): print r
            Jan-15 15:25:29 INFO     __main__::parameters = {'num_threads': 1, 'log': True}
            Jan-15 15:25:30 INFO     __main__::Computing namespace edits. (PID = 20102)
            Jan-15 15:25:30 INFO     __main__::From 20110101000000 to 20130115152529. (PID = 20102)
            ['namespace_edits_sum', OrderedDict([('-1', 0), ('-2', 0), ('0', 227), ('1', 11), ('2', 158), ('3', 38),
            ('4', 578), ('5', 27), ('6', 1), ('7', 0), ('8', 0), ('9', 0), ('10', 13), ('11', 8), ('12', 0), ('13', 0),
            ('14', 5), ('15', 0), ('100', 1), ('101', 2), ('108', 0), ('109', 0)])]

    """
    VALID_NAMESPACES = [
     -1, -2] + range(16) + [100, 101, 108, 109]
    _param_types = {'init': {}, 'process': {'log': [
                         'bool', 'Enable logging for processing.', False], 
                   'num_threads': [
                                 'int', 'Number of worker processes over users.', 1]}}
    _data_model_meta = {'id_fields': [
                   0], 
       'date_fields': [], 'float_fields': [
                      1], 
       'integer_fields': [
                        2], 
       'boolean_fields': []}
    _agg_indices = {'namespace_edits_sum': _data_model_meta['integer_fields'] + _data_model_meta['float_fields']}

    @um.pre_metrics_init
    def __init__(self, **kwargs):
        um.UserMetric.__init__(self, **kwargs)

    @staticmethod
    def header():
        return [
         'user_id', 'revision_data_by_namespace']

    @um.UserMetric.pre_process_users
    def process(self, user_handle, **kwargs):
        self.apply_default_kwargs(kwargs, 'process')
        if not hasattr(user_handle, '__iter__'):
            user_handle = [user_handle]
        k = int(kwargs['num_threads'])
        log = bool(kwargs['log'])
        if log:
            logging.info(__name__ + '::parameters = ' + str(kwargs))
        args = [
         self._project_, log, self._start_ts_, self._end_ts_]
        self._results = mpw.build_thread_pool(user_handle, _process_help, k, args)
        return self


def _process_help(args):
    state = args[1]
    thread_args = NamespaceEditsArgsClass(state[0], state[1], state[2], state[3])
    user_data = args[0]
    conn = Connector(instance='slave')
    to_string = DataLoader().cast_elems_to_string
    to_csv_str = DataLoader().format_comma_separated_list
    user_cond = 'rev_user in (' + to_csv_str(to_string(user_data)) + ')'
    ts_cond = 'rev_timestamp >= %s and rev_timestamp < %s' % (thread_args.date_start, thread_args.date_end)
    if thread_args.log:
        logging.info(__name__ + '::Computing namespace edits. (PID = %s)' % getpid())
        logging.info(__name__ + '::From %s to %s. (PID = %s)' % (
         str(thread_args.date_start), str(thread_args.date_end), getpid()))
    sql = '\n            SELECT\n                r.rev_user,\n                p.page_namespace,\n                count(*) AS revs\n            FROM %(project)s.revision AS r JOIN %(project)s.page AS p\n                ON r.rev_page = p.page_id\n            WHERE %(user_cond)s AND %(ts_cond)s\n            GROUP BY 1,2\n        ' % {'user_cond': user_cond, 
       'ts_cond': ts_cond, 
       'project': thread_args.project}
    conn._cur_.execute((' ').join(sql.split('\n')))
    results = dict()
    for user in user_data:
        results[str(user)] = OrderedDict()
        for ns in NamespaceEdits.VALID_NAMESPACES:
            results[str(user)][str(ns)] = 0

    for row in conn._cur_:
        try:
            if row[1] in NamespaceEdits.VALID_NAMESPACES:
                results[str(row[0])][str(row[1])] = int(row[2])
        except KeyError:
            logging.error(__name__ + '::Could not process row: %s' % str(row))
        except IndexError:
            logging.error(__name__ + '::Could not process row: %s' % str(row))

    del conn
    return [ (user, results[user]) for user in results ]


@decorator_builder(NamespaceEdits.header())
def namespace_edits_sum--- This code section failed: ---

 L. 153         0  LOAD_CONST               'namespace_edits_sum'
                3  LOAD_GLOBAL           0  'OrderedDict'
                6  CALL_FUNCTION_0       0  None
                9  BUILD_LIST_2          2 
               12  STORE_FAST            1  'summed_results'

 L. 154        15  SETUP_LOOP           37  'to 55'
               18  LOAD_GLOBAL           1  'NamespaceEdits'
               21  LOAD_ATTR             2  'VALID_NAMESPACES'
               24  GET_ITER         
               25  FOR_ITER             26  'to 54'
               28  STORE_FAST            2  'ns'

 L. 155        31  LOAD_CONST               0
               34  LOAD_FAST             1  'summed_results'
               37  LOAD_CONST               1
               40  BINARY_SUBSCR    
               41  LOAD_GLOBAL           3  'str'
               44  LOAD_FAST             2  'ns'
               47  CALL_FUNCTION_1       1  None
               50  STORE_SUBSCR     
               51  JUMP_BACK            25  'to 25'
               54  POP_BLOCK        
             55_0  COME_FROM            15  '15'

 L. 156        55  SETUP_LOOP          126  'to 184'
               58  LOAD_FAST             0  'metric'
               61  LOAD_ATTR             4  '__iter__'
               64  CALL_FUNCTION_0       0  None
               67  GET_ITER         
               68  FOR_ITER            112  'to 183'
               71  STORE_FAST            3  'r'

 L. 157        74  SETUP_EXCEPT         64  'to 141'

 L. 158        77  SETUP_LOOP           57  'to 137'
               80  LOAD_GLOBAL           1  'NamespaceEdits'
               83  LOAD_ATTR             2  'VALID_NAMESPACES'
               86  GET_ITER         
               87  FOR_ITER             46  'to 136'
               90  STORE_FAST            2  'ns'

 L. 159        93  LOAD_FAST             1  'summed_results'
               96  LOAD_CONST               1
               99  BINARY_SUBSCR    
              100  LOAD_GLOBAL           3  'str'
              103  LOAD_FAST             2  'ns'
              106  CALL_FUNCTION_1       1  None
              109  DUP_TOPX_2            2  None
              112  BINARY_SUBSCR    
              113  LOAD_FAST             3  'r'
              116  LOAD_CONST               1
              119  BINARY_SUBSCR    
              120  LOAD_GLOBAL           3  'str'
              123  LOAD_FAST             2  'ns'
              126  CALL_FUNCTION_1       1  None
              129  BINARY_SUBSCR    
              130  INPLACE_ADD      
              131  ROT_THREE        
              132  STORE_SUBSCR     
              133  JUMP_BACK            87  'to 87'
              136  POP_BLOCK        
            137_0  COME_FROM            77  '77'
              137  POP_BLOCK        
              138  JUMP_BACK            68  'to 68'
            141_0  COME_FROM            74  '74'

 L. 160       141  DUP_TOP          
              142  LOAD_GLOBAL           5  'IndexError'
              145  COMPARE_OP           10  exception-match
              148  POP_JUMP_IF_FALSE   160  'to 160'
              151  POP_TOP          
              152  POP_TOP          
              153  POP_TOP          
              154  JUMP_BACK            68  'to 68'
              157  JUMP_BACK            68  'to 68'

 L. 161       160  DUP_TOP          
              161  LOAD_GLOBAL           6  'TypeError'
              164  COMPARE_OP           10  exception-match
              167  POP_JUMP_IF_FALSE   179  'to 179'
              170  POP_TOP          
              171  POP_TOP          
              172  POP_TOP          
              173  CONTINUE             68  'to 68'
              176  JUMP_BACK            68  'to 68'
              179  END_FINALLY      
            180_0  COME_FROM           179  '179'
              180  JUMP_BACK            68  'to 68'
              183  POP_BLOCK        
            184_0  COME_FROM            55  '55'

 L. 162       184  LOAD_FAST             1  'summed_results'
              187  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 157


setattr(namespace_edits_sum, um.METRIC_AGG_METHOD_FLAG, True)
setattr(namespace_edits_sum, um.METRIC_AGG_METHOD_NAME, 'namespace_edits_aggregates')
setattr(namespace_edits_sum, um.METRIC_AGG_METHOD_HEAD, ['type', 'total_revs',
 'weighted_rate', 'total_editors', 'reverted_editors'])
if __name__ == '__main__':
    users = [
     '17792132', '17797320', '17792130', '17792131', '17792136', 13234584, 156171]
    m = NamespaceEdits(date_start='20110101000000')
    m.process(users, log=True)
    print namespace_edits_sum(m)