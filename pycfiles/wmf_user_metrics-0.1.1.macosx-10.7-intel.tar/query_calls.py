# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/src/metrics/query_calls.py
# Compiled at: 2013-02-04 10:15:59
"""
    Store the query calls for UserMetric classes
"""
__author__ = 'Ryan Faulkner'
__email__ = 'rfaulkner@wikimedia.org'
__date__ = 'january 30th, 2013'
__license__ = 'GPL (version 2 or later)'
from src.etl.data_loader import DataLoader
from copy import deepcopy

def format_namespace(namespace):
    """ Format the namespace condition in queries and returns the string.

        Expects a list of numeric namespace keys.  Otherwise returns
        an empty condition string
    """
    ns_cond = ''
    if hasattr(namespace, '__iter__'):
        if len(namespace) == 1:
            ns_cond = 'page_namespace = ' + str(namespace.pop())
        else:
            ns_cond = 'page_namespace in (' + (',').join(DataLoader().cast_elems_to_string(list(namespace))) + ')'
    return ns_cond


def threshold_reg_query(users, project):
    """ Get registered users for Threshold metric objects """
    uid_str = DataLoader().format_comma_separated_list(DataLoader().cast_elems_to_string(users), include_quotes=False)
    sql = query_store[threshold_reg_query.__name__] % {'project': project, 
       'uid_str': uid_str}
    return (' ').join(sql.strip().split('\n'))


def threshold_rev_query(uid, is_survival, namespace, project, restrict, start_time, end_time, threshold_ts):
    """ Get revisions associated with a UID for Threshold metrics """
    if is_survival:
        timestamp_cond = ' and rev_timestamp > %(ts)s'
    else:
        timestamp_cond = ' and rev_timestamp <= "%(ts)s"'
    ns_cond = format_namespace(deepcopy(namespace))
    if restrict:
        timestamp_cond += (' and rev_timestamp > "{0}" and rev_timestamp <= "{1}"').format(start_time, end_time)
    sql = query_store[threshold_rev_query.__name__] + timestamp_cond
    sql = sql % {'project': project, 'ts': threshold_ts, 
       'ns': ns_cond, 
       'uid': uid}
    return (' ').join(sql.strip().split('\n'))


def live_account_query(users, namespace, project):
    """ Format query for live_account metric """
    user_cond = DataLoader().format_condition_in('ept_user', users)
    ns_cond = format_namespace(namespace)
    where_clause = 'log_action = "create"'
    if user_cond:
        where_clause += ' AND ' + user_cond
    if ns_cond:
        where_clause += ' AND ' + ns_cond
    from_clause = '%(project)s.edit_page_tracking AS e RIGHT JOIN %(project)s.logging AS l ON e.ept_user = l.log_user'
    from_clause = from_clause % {'project': project}
    if ns_cond:
        from_clause += ' LEFT JOIN %(project)s.page as p ON e.ept_title = p.page_title' % {'project': project}
    sql = '\n            SELECT\n                e.ept_user,\n                MIN(l.log_timestamp) as registration,\n                MIN(e.ept_timestamp) as first_click\n            FROM %(from_clause)s\n            WHERE %(where_clause)s\n            GROUP BY 1\n        ' % {'from_clause': from_clause, 
       'where_clause': where_clause}
    return (' ').join(sql.split('\n'))


query_store = {threshold_reg_query.__name__: "\n                                SELECT\n                                    log_user,\n                                    log_timestamp\n                                FROM %(project)s.logging\n                                WHERE log_action = 'create' AND\n                                    log_type='newusers'\n                                        and log_user in (%(uid_str)s)\n                            ", 
   threshold_rev_query.__name__: '\n                                SELECT\n                                    count(*) as revs\n                                FROM %(project)s.revision as r\n                                    JOIN %(project)s.page as p\n                                        ON  r.rev_page = p.page_id\n                                WHERE %(ns)s AND rev_user = %(uid)s\n                            ', 
   live_account_query.__name__: '\n                                SELECT\n                                    e.ept_user,\n                                    MIN(l.log_timestamp) as registration,\n                                    MIN(e.ept_timestamp) as first_click\n                                FROM %(from_clause)s\n                                WHERE %(where_clause)s\n                                GROUP BY 1\n                            '}