# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/content/search.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 264 bytes
from elasticsearch_dsl import function, query

def randomize_es(es_queryset):
    """Randomize an elasticsearch queryset."""
    return es_queryset.query(query.FunctionScore(functions=[
     function.RandomScore()])).sort('-_score')