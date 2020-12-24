# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/src/metrics/live_account.py
# Compiled at: 2013-02-04 10:13:22
__author__ = 'Ryan Faulkner'
__email__ = 'rfaulkner@wikimedia.org'
__date__ = 'January 6th, 2013'
__license__ = 'GPL (version 2 or later)'
import user_metric as um, src.utils.multiprocessing_wrapper as mpw
from src.etl.data_loader import Connector
from collections import namedtuple
from config import logging
from os import getpid
from dateutil.parser import parse as date_parse
from src.etl.aggregator import decorator_builder, boolean_rate
from query_calls import live_account_query
LiveAccountArgsClass = namedtuple('LiveAccountArgs', 'project namespace log date_start date_end t')

class LiveAccount(um.UserMetric):
    """
        Skeleton class for "live account" metric:

            `https://meta.wikimedia.org/wiki/Research:Metrics/live_account`

        As a UserMetric type this class utilizes the process() function
        attribute to produce an internal list of metrics by user handle
        (typically ID but user names may also be specified). The execution
        of process() produces a nested list that
        stores in each element:

            * user ID
            * boolean value indicating whether the account is considered
                "live" given the parameters

        For example to produce the above datapoint for a user id one could
        call: ::

            >>> from src.metrics.live_account import LiveAccount
            >>> users = ['17792132', '17797320', '17792130', '17792131',
                        '17792136', 13234584, 156171]
            >>> la = LiveAccount(date_start='20110101000000')
            >>> for r in r.process(users,log=True): print r
            ('17792130', -1)
            ('17792131', -1)
            ('17792132', -1)
            ('17797320', -1)
            ('156171', -1)
            ('17792136', 1)
            ('13234584', -1)

        Here the follow outcomes may follow: ::

            -1  - The edit button was not clicked after registration
            0   - The edit button was clicked more than `t` minutes
                    after registration
            1   - The edit button was clicked `t` minutes within registration
    """
    _param_types = {'init': {'t': [
                    'int', 'The time in minutes until the threshold.', 60]}, 
       'process': {'log': [
                         'bool', 'Enable logging for processing.', False], 
                   'num_threads': [
                                 'int', 'Number of worker processes over users.', 1]}}
    _data_model_meta = {'id_fields': [
                   0], 
       'date_fields': [], 'float_fields': [], 'integer_fields': [], 'boolean_fields': [
                        1]}
    _agg_indices = {}

    @um.pre_metrics_init
    def __init__(self, **kwargs):
        um.UserMetric.__init__(self, **kwargs)
        self._t_ = int(kwargs['t']) if 't' in kwargs else self._param_types['init']['t'][2]

    @staticmethod
    def header():
        return [
         'user_id', 'is_active_account']

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
         self._project_, self._namespace_, log, self._start_ts_,
         self._end_ts_, self._t_]
        self._results = mpw.build_thread_pool(user_handle, _process_help, k, args)
        return self


def _process_help(args):
    state = args[1]
    thread_args = LiveAccountArgsClass(state[0], state[1], state[2], state[3], state[4], state[5])
    user_data = args[0]
    conn = Connector(instance='slave')
    if thread_args.log:
        logging.info(__name__ + '::Computing live account. (PID = %s)' % getpid())
        logging.info(__name__ + '::From %s to %s. (PID = %s)' % (
         str(thread_args.date_start), str(thread_args.date_end), getpid()))
    la_query = live_account_query(user_data, thread_args.namespace, thread_args.project)
    conn._cur_.execute(la_query)
    results = {long(user):-1 for user in user_data}
    for row in conn._cur_:
        try:
            diff = (date_parse(row[2]) - date_parse(row[1])).total_seconds()
            diff /= 60
        except Exception:
            continue

        if diff <= thread_args.t:
            results[row[0]] = 1
        else:
            results[row[0]] = 0

    return [ (str(key), results[key]) for key in results ]


@decorator_builder(LiveAccount.header())
def live_accounts_agg--- This code section failed: ---

 L. 158         0  LOAD_CONST               0
                3  STORE_FAST            1  'total'

 L. 159         6  LOAD_CONST               0
                9  STORE_FAST            2  'pos'

 L. 160        12  SETUP_LOOP           99  'to 114'
               15  LOAD_FAST             0  'metric'
               18  LOAD_ATTR             0  '__iter__'
               21  CALL_FUNCTION_0       0  None
               24  GET_ITER         
               25  FOR_ITER             85  'to 113'
               28  STORE_FAST            3  'r'

 L. 161        31  SETUP_EXCEPT         37  'to 71'

 L. 162        34  LOAD_FAST             3  'r'
               37  LOAD_CONST               1
               40  BINARY_SUBSCR    
               41  POP_JUMP_IF_FALSE    57  'to 57'
               44  LOAD_FAST             2  'pos'
               47  LOAD_CONST               1
               50  INPLACE_ADD      
               51  STORE_FAST            2  'pos'
               54  JUMP_FORWARD          0  'to 57'
             57_0  COME_FROM            54  '54'

 L. 163        57  LOAD_FAST             1  'total'
               60  LOAD_CONST               1
               63  INPLACE_ADD      
               64  STORE_FAST            1  'total'
               67  POP_BLOCK        
               68  JUMP_BACK            25  'to 25'
             71_0  COME_FROM            31  '31'

 L. 164        71  DUP_TOP          
               72  LOAD_GLOBAL           1  'IndexError'
               75  COMPARE_OP           10  exception-match
               78  POP_JUMP_IF_FALSE    90  'to 90'
               81  POP_TOP          
               82  POP_TOP          
               83  POP_TOP          
               84  JUMP_BACK            25  'to 25'
               87  JUMP_BACK            25  'to 25'

 L. 165        90  DUP_TOP          
               91  LOAD_GLOBAL           2  'TypeError'
               94  COMPARE_OP           10  exception-match
               97  POP_JUMP_IF_FALSE   109  'to 109'
              100  POP_TOP          
              101  POP_TOP          
              102  POP_TOP          
              103  CONTINUE             25  'to 25'
              106  JUMP_BACK            25  'to 25'
              109  END_FINALLY      
            110_0  COME_FROM           109  '109'
              110  JUMP_BACK            25  'to 25'
              113  POP_BLOCK        
            114_0  COME_FROM            12  '12'

 L. 166       114  LOAD_FAST             1  'total'
              117  POP_JUMP_IF_FALSE   143  'to 143'

 L. 167       120  LOAD_FAST             1  'total'
              123  LOAD_FAST             2  'pos'
              126  LOAD_GLOBAL           3  'float'
              129  LOAD_FAST             2  'pos'
              132  CALL_FUNCTION_1       1  None
              135  LOAD_FAST             1  'total'
              138  BINARY_DIVIDE    
              139  BUILD_LIST_3          3 
              142  RETURN_END_IF    
            143_0  COME_FROM           117  '117'

 L. 169       143  LOAD_FAST             1  'total'
              146  LOAD_FAST             2  'pos'
              149  LOAD_CONST               0.0
              152  BUILD_LIST_3          3 
              155  RETURN_VALUE     

Parse error at or near `JUMP_BACK' instruction at offset 87


live_accounts_agg = boolean_rate
live_accounts_agg = decorator_builder(LiveAccount.header())(live_accounts_agg)
setattr(live_accounts_agg, um.METRIC_AGG_METHOD_FLAG, True)
setattr(live_accounts_agg, um.METRIC_AGG_METHOD_NAME, 'live_accounts_agg')
setattr(live_accounts_agg, um.METRIC_AGG_METHOD_HEAD, ['total_users',
 'is_live', 'rate'])
setattr(live_accounts_agg, um.METRIC_AGG_METHOD_KWARGS, {'val_idx': 1})
if __name__ == '__main__':
    users = [
     '17792132', '17797320', '17792130', '17792131', '17792136',
     13234584, 156171]
    la = LiveAccount()
    for r in la.process(users, log=True):
        print r