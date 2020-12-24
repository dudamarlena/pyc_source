# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pysolarized/__init__.py
# Compiled at: 2014-05-26 16:45:17
from .solr import Solr, SolrException, SolrResults
from datetime import datetime
__all__ = ['Solr', 'SolrException', 'SolrResults']

def to_solr_date(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')


def from_solr_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')