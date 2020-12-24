# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/webapptitude/dnsquery.py
# Compiled at: 2016-08-31 16:32:16
import dnsq, re
from dnsq import query_dns, mx_hosts_for, ptr_record_for, spf_record_for, get_primary_nameserver
RECORD_TYPES = ('A', 'AAAA', 'CNAME', 'MX', 'PTR', 'SOA', 'TXT')
DNS_SERVER = None

def default_opts():
    return dict(ns_server=DNS_SERVER)


def validation(domain, find_value, _type='TXT'):
    """Look for a specific record in the DNS records of a specific domain."""
    values = dnsq.query_dns(domain, _type, **default_opts())
    return find_value in values


def extract(domain, pattern, _type='TXT', match_full=True):
    """Find all matching records per a regular expression."""
    values = dnsq.query_dns(domain, _type, **default_opts())
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern)
    for val in values:
        if match_full:
            match = pattern.match(val)
            if match is not None:
                yield match
        else:
            for m in pattern.finditer(val):
                yield m

    return


def query_all(domain, _types=RECORD_TYPES):
    """Generate a list of all records for a domain."""
    for a in _types:
        values = dnsq.query_dns(domain, a, **default_opts())
        for val in values or []:
            yield (
             a, val)