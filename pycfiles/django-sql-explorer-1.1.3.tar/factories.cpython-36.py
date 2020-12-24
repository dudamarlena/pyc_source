# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/tests/factories.py
# Compiled at: 2019-07-02 16:47:10
# Size of source mod 2**32: 496 bytes
import factory
from explorer import models

class SimpleQueryFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Query

    title = factory.Sequence(lambda n: 'My siple query %s' % n)
    sql = 'SELECT 1+1 AS TWO'
    description = "Doin' math"
    connection = 'default'
    created_by_user_id = 1


class QueryLogFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.QueryLog

    sql = 'SELECT 2+2 AS FOUR'