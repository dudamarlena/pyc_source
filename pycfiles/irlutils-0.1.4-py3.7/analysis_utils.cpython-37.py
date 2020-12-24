# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/url/crawl/analysis_utils.py
# Compiled at: 2019-11-16 18:33:01
# Size of source mod 2**32: 5877 bytes
from __future__ import absolute_import
from __future__ import print_function
import os, sys, json, pandas as pd
from datetime import datetime

def get_set_of_script_hosts_from_call_stack(call_stack):
    """Return the urls of the scripts involved in the call stack."""
    script_urls = set()
    if not call_stack:
        return ''
    stack_frames = call_stack.strip().split('\n')
    for stack_frame in stack_frames:
        script_url = stack_frame.rsplit(':', 2)[0].split('@')[(-1)].split(' line')[0]
        script_urls.add(get_host_from_url(script_url))

    return ', '.join(script_urls)


def get_host_from_url(url):
    return strip_scheme_www_and_query(url).split('/', 1)[0]


def strip_scheme_www_and_query(url):
    """Remove the scheme and query section of a URL."""
    if url:
        return url.split('//')[(-1)].split('?')[0].lstrip('www.')
    return ''


def get_initiator_from_call_stack(call_stack):
    """Return the bottom element of the call stack."""
    if call_stack:
        if type(call_stack) == str:
            return call_stack.strip().split('\n')[(-1)]
    return ''


def get_initiator_from_req_call_stack(req_call_stack):
    """Return the bottom element of a request call stack.
    Request call stacks have an extra field (async_cause) at the end.
    """
    return get_initiator_from_call_stack(req_call_stack).split(';')[0]


def get_func_and_script_url_from_initiator(initiator):
    """Remove line number and column number from the initiator."""
    if initiator:
        return initiator.rsplit(':', 2)[0].split(' line')[0]
    return ''


def get_script_url_from_initiator(initiator):
    """Remove the scheme and query section of a URL."""
    if initiator:
        return initiator.rsplit(':', 2)[0].split('@')[(-1)].split(' line')[0]
    return ''


def get_set_of_script_urls_from_call_stack(call_stack):
    """Return the urls of the scripts involved in the call stack as a
    string."""
    if not call_stack:
        return ''
    return ', '.join(get_script_urls_from_call_stack_as_set(call_stack))


def get_script_urls_from_call_stack_as_set(call_stack):
    """Return the urls of the scripts involved in the call stack as a set."""
    script_urls = set()
    if not call_stack:
        return script_urls
    stack_frames = call_stack.strip().split('\n')
    for stack_frame in stack_frames:
        script_url = stack_frame.rsplit(':', 2)[0].split('@')[(-1)].split(' line')[0]
        script_urls.add(script_url)

    return script_urls


def add_col_bare_script_url(js_df):
    """Add a col for script URL without scheme, www and query."""
    js_df['bare_script_url'] = js_df['script_url'].map(strip_scheme_www_and_query)


def add_col_set_of_script_urls_from_call_stack(js_df):
    js_df['stack_scripts'] = js_df['call_stack'].map(get_set_of_script_urls_from_call_stack)


def add_col_unix_timestamp(df):
    df['unix_time_stamp'] = df['time_stamp'].map(datetime_from_iso)


def datetime_from_iso(iso_date):
    """Convert from ISO."""
    iso_date = iso_date.rstrip('Z')
    if iso_date[(-3)] == '.':
        rest, ms = iso_date.split('.')
        iso_date = rest + '.0' + ms
    else:
        if iso_date[(-2)] == '.':
            rest, ms = iso_date.split('.')
            iso_date = rest + '.00' + ms
    try:
        return datetime.strptime(iso_date, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        return datetime.strptime(iso_date.rstrip('+0000'), '%Y-%m-%dT%H:%M:%S')


def get_cookie(headers):
    for item in headers:
        if item[0] == 'Cookie':
            return item[1]

    return ''


def parse_headers(header):
    kv = {}
    for item in json.loads(header):
        k = item[0]
        v = item[1]
        kv[k] = v

    return kv


def get_set_cookie(header):
    for item in json.loads(header):
        if item[0] == 'Set-Cookie':
            return item[1]

    return ''


def get_responses_from_visits(con, visit_ids):
    visit_ids_str = '(%s)' % ','.join((str(x) for x in visit_ids))
    qry = 'SELECT r.id, r.crawl_id, r.visit_id, r.url,\n                sv.site_url, sv.first_party, sv.site_rank,\n                r.method, r.referrer, r.headers, r.response_status, r.location,\n                r.time_stamp FROM http_responses as r\n            LEFT JOIN site_visits as sv\n            ON r.visit_id = sv.visit_id\n            WHERE r.visit_id in %s;' % visit_ids_str
    return pd.read_sql_query(qry, con)


def get_requests_from_visits(con, visit_ids):
    visit_ids_str = '(%s)' % ','.join((str(x) for x in visit_ids))
    qry = 'SELECT r.id, r.crawl_id, r.visit_id, r.url, r.top_level_url,\n            sv.site_url, sv.first_party, sv.site_rank,\n            r.method, r.referrer, r.headers, r.loading_href, r.req_call_stack,\n            r.content_policy_type, r.post_body, r.time_stamp\n            FROM http_requests as r\n            LEFT JOIN site_visits as sv\n            ON r.visit_id = sv.visit_id\n            WHERE r.visit_id in %s;' % visit_ids_str
    return pd.read_sql_query(qry, con)


def get_set_of_script_ps1s_from_call_stack(script_urls, du):
    if len(script_urls):
        return ', '.join(set((du.get_ps_plus_1(x) or '' for x in script_urls.split(', '))))
    return ''


def add_col_set_of_script_ps1s_from_call_stack(js_df):
    js_df['stack_script_ps1s'] = js_df['stack_scripts'].map(get_set_of_script_ps1s_from_call_stack)


if __name__ == '__main__':
    pass