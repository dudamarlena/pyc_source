# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/src/metrics/bytes_added.py
# Compiled at: 2013-01-30 17:49:01
__author__ = 'Ryan Faulkner'
__date__ = 'July 27th, 2012'
__license__ = 'GPL (version 2 or later)'
import collections, user_metric as um, os, src.etl.aggregator as agg, src.utils.multiprocessing_wrapper as mpw
from config import logging

class BytesAdded(um.UserMetric):
    """
        Produces a float value that reflects the rate of edit behaviour:

            `https://meta.wikimedia.org/wiki/Research:Metrics/edit_rate`

        As a UserMetric type this class utilizes the process() function
        attribute to produce an internal list of metrics by user handle
        (typically ID but user names may also be specified). The execution of
        process() produces a nested list that stores in each element:

            * User ID
            * Net bytes contributed over the period of measurement
            * Absolute bytes contributed over the period of measurement
            * Bytes added over the period of measurement
            * Bytes removed over the period of measurement
            * Total edit count over the period of measurement

            usage e.g.: ::

                >>> import src.,metrics.bytes_added as ba
                >>> for r in ba.BytesAdded(date_start='2012-07-30 00:00:00').
                    process([13234584], num_threads=0).__iter__(): r
                ['13234584', 2, 2, 2, 0, 1]
                >>> ba.BytesAdded.header()
                ['user_id', 'bytes_added_net', 'bytes_added_absolute',
                    'bytes_added_pos', 'bytes_added_neg', 'edit_count']

        This metric forks a separate query on the revision table for each user
        specified in the call to process().  In order to optimize the
        execution of this implementation the call allows the caller to specify
        the number of threads as a keyword argument, `num_threads`, to the
        process() method.
    """
    _param_types = {'init': {}, 'process': {'log_progress': [
                                  'bool', 'Enable logging for processing.', False], 
                   'log_frequency': [
                                   'int', 'Revision frequency on which to log (ie. log every n revisions)',
                                   1000], 
                   'num_threads': [
                                 'int', 'Number of worker processes.', 1]}}
    _data_model_meta = {'id_fields': [
                   0], 
       'date_fields': [], 'float_fields': [], 'integer_fields': [
                        1, 2, 3, 4, 5], 
       'boolean_fields': []}
    _agg_indices = {'list_sum_indices': _data_model_meta['integer_fields'] + _data_model_meta['float_fields']}

    @um.pre_metrics_init
    def __init__(self, **kwargs):
        um.UserMetric.__init__(self, **kwargs)

    @staticmethod
    def header():
        return [
         'user_id', 'bytes_added_net', 'bytes_added_absolute',
         'bytes_added_pos', 'bytes_added_neg', 'edit_count']

    @um.UserMetric.pre_process_users
    def process(self, user_handle, **kwargs):
        """ Setup metrics gathering using multiprocessing """
        self.apply_default_kwargs(kwargs, 'process')
        k = kwargs['num_threads']
        log_progress = bool(kwargs['log_progress'])
        log_frequency = int(kwargs['log_frequency'])
        if user_handle:
            if not hasattr(user_handle, '__iter__'):
                user_handle = [
                 user_handle]
        if not user_handle:
            sql = 'SELECT distinct rev_user FROM enwiki.revision WHERE rev_timestamp >= "%s" AND rev_timestamp < "%s"'
            sql = sql % (self._start_ts_, self._end_ts_)
            if log_progress:
                logging.info(__name__ + '::Getting all distinct users: " %s "' % sql)
            user_handle = [ str(row[0]) for row in self._data_source_.execute_SQL(sql) ]
            if log_progress:
                logging.info(__name__ + '::Retrieved %s users.' % len(user_handle))
        args = [log_progress, self._start_ts_,
         self._end_ts_, self._project_, self._namespace_]
        revs = mpw.build_thread_pool(user_handle, _get_revisions, k, args)
        args = [
         log_progress, log_frequency, self._project_]
        self._results = agg.list_sum_by_group(mpw.build_thread_pool(revs, _process_help, k, args), 0)
        tallied_users = set([ str(r[0]) for r in self._results ])
        for user in user_handle:
            if not tallied_users.__contains__(str(user)):
                self._results.append([user, 0, 0, 0, 0, 0])

        return self


def _get_revisions(args):
    MethodArgsClass = collections.namedtuple('MethodArg', 'log start end project namespace')
    users = args[0]
    state = args[1]
    arg_obj = MethodArgsClass(state[0], state[1], state[2], state[3], state[4])
    conn = um.dl.Connector(instance='slave')
    if arg_obj.log:
        logging.info('Computing revisions, PID = %s' % os.getpid())
    ts_condition = 'rev_timestamp >= "%s" and rev_timestamp < "%s"' % (
     arg_obj.start, arg_obj.end)
    users = um.UserMetric._escape_var(users)
    if not hasattr(users, '__iter__'):
        users = [users]
    user_set = um.dl.DataLoader().format_comma_separated_list(users, include_quotes=False)
    where_clause = 'rev_user in (%(user_set)s) and %(ts_condition)s' % {'user_set': user_set, 
       'ts_condition': ts_condition}
    ns_cond = um.UserMetric._format_namespace(arg_obj.namespace)
    if ns_cond:
        ns_cond += ' and'
    sql = '\n            select\n                rev_user,\n                rev_len,\n                rev_parent_id\n            from %(project)s.revision\n                join %(project)s.page\n                on page.page_id = revision.rev_page\n            where %(namespace)s %(where_clause)s\n        ' % {'where_clause': where_clause, 
       'project': arg_obj.project, 
       'namespace': ns_cond}
    sql = (' ').join(sql.strip().split())
    if arg_obj.log:
        logging.info(__name__ + '::Querying revisions for %(count)s users (project = %(project)s, namespace = %(namespace)s)... ' % {'count': len(users), 
           'project': arg_obj.project, 
           'namespace': arg_obj.namespace})
    try:
        return list(conn.execute_SQL(sql))
    except um.MySQLdb.ProgrammingError:
        raise um.UserMetric.UserMetricError(message=str(BytesAdded) + '::Could not get revisions for specified users(s) - Query Failed.')


def _process_help(args):
    """
        Determine the bytes added over a number of revisions for user(s).  The
        parameter *user_handle* can be either a string or an integer or a list
        of these types.  When the *user_handle* type is integer it is
        interpreted as a user id, and as a user_name for string input.  If a
        list of users is passed to the *process* method then a dict object
        with edit rates keyed by user handles is returned.

        The flow of the request is as follows:

            #. Get all revisions for the specified users in the given
                timeframe
            #. For each parent revision get its length
            #. Compute the difference in length between each revision and its
                parent
            #. Record edit count, raw bytes added (with sign and absolute),
                amount of positive bytes added, amount of negative bytes added

        - Parameters:
            - **user_handle** - String or Integer (optionally lists).  Value
                or list of values representing user handle(s).
        - Return:
            - Dictionary. key(string): user handle, value(Float): edit counts
    """
    BytesAddedArgsClass = collections.namedtuple('BytesAddedArgs', 'is_log freq project')
    revs = args[0]
    state = args[1]
    thread_args = BytesAddedArgsClass(state[0], state[1], state[2])
    conn = um.dl.Connector(instance='slave')
    bytes_added = dict()
    row_count = 1
    missed_records = 0
    total_rows = len(revs)
    if thread_args.is_log:
        logging.info(__name__ + '::Processing revision data (%s rows) by user... (PID = %s)' % (
         total_rows, os.getpid()))
    for row in revs:
        try:
            user = str(row[0])
            rev_len_total = int(row[1])
            parent_rev_id = row[2]
        except IndexError:
            missed_records += 1
            continue
        except TypeError:
            missed_records += 1
            continue

        if parent_rev_id == 0:
            parent_rev_len = 0
        else:
            sql = '\n                    SELECT rev_len\n                    FROM %(project)s.revision\n                    WHERE rev_id = %(parent_rev_id)s\n                ' % {'project': thread_args.project, 
               'parent_rev_id': parent_rev_id}
            try:
                parent_rev_len = conn.execute_SQL(sql)[0][0]
            except IndexError:
                missed_records += 1
                continue
            except TypeError:
                missed_records += 1
                continue
            except um.MySQLdb.ProgrammingError:
                raise um.UserMetric.UserMetricError(message=str(BytesAdded) + '::Could not produce rev diff for %s on rev_id %s.' % (
                 user, str(parent_rev_id)))

            try:
                bytes_added_bit = int(rev_len_total) - int(parent_rev_len)
            except TypeError:
                missed_records += 1
                continue

            try:
                bytes_added[user][0] += bytes_added_bit
            except KeyError:
                bytes_added[user] = [
                 0] * 5
                bytes_added[user][0] += bytes_added_bit

        bytes_added[user][1] += abs(bytes_added_bit)
        if bytes_added_bit > 0:
            bytes_added[user][2] += bytes_added_bit
        else:
            bytes_added[user][3] += bytes_added_bit
        bytes_added[user][4] += 1
        if thread_args.freq and row_count % thread_args.freq == 0 and thread_args.is_log:
            logging.info(__name__ + '::Processed %s of %s records. (PID = %s)' % (
             row_count, total_rows, os.getpid()))
        row_count += 1

    results = [ [user] + bytes_added[user] for user in bytes_added ]
    if thread_args.is_log:
        logging.info(__name__ + '::Processed %s out of %s records. (PID = %s)' % (
         total_rows - missed_records, total_rows, os.getpid()))
    return results


if __name__ == '__main__':
    for r in BytesAdded().process(user_handle=['156171', '13234584'], num_threads=10, log_progress=True):
        print r