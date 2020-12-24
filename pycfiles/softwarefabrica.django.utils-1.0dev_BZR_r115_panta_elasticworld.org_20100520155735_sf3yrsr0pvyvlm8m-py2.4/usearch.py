# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/usearch.py
# Compiled at: 2009-01-08 04:02:17
import re
from django.db.models import Q

def normalize_query(query_string, findterms=re.compile('"([^"]+)"|(\\S+)').findall, normspace=re.compile('\\s{2,}').sub):
    """ Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    """
    return [ normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string) ]


def get_query(query_string, search_fields):
    """ Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    """
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{'%s__icontains' % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q

        if query is None:
            query = or_query
        else:
            query = query & or_query

    return query