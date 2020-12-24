# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/grnhse/util.py
# Compiled at: 2018-11-09 23:39:01
"""
    Utilities for interacting with the Greenhouse APIs
"""
import datetime, re
DT_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

def extract_header_links(link_header):
    rels = {}
    if link_header is not None:
        links = [ l.strip() for l in link_header.split(',') ]
        pattern = '<(?P<url>.*)>;\\s*rel="(?P<rel>.*)"'
        for link in links:
            group_dict = re.match(pattern, link).groupdict()
            rels[group_dict['rel']] = group_dict['url']

    return rels


def strf_dt(dt):
    return dt.strftime(DT_FORMAT)


def strp_dt(sdt):
    return datetime.datetime.strptime(sdt, DT_FORMAT)