# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/khalikov/projects/processing/src/processing/../env/m3_consolequery/helpers.py
# Compiled at: 2013-09-30 08:42:40
"""
Created on 14.12.2010

@author: Камилла
"""
from django.db import connections
from django.db import transaction
from models import CustomQueries
import urllib

@transaction.commit_manually
def query_result_list(sql):
    u"""
    Выполняет полученный запрос sql
    Возращает: в случае удачного выполнения результат запроса и пустую ошибку
                в случае неудачи пустой результат запроса и ошибку 
    
    """
    try:
        cursor = connections['readonly'].cursor()
        cursor.execute(sql)
    except Exception, e:
        transaction.rollback()
        return (None, e.args[0], None)

    transaction.commit()
    return (cursor.fetchall(), None, cursor.description)
    return


def new_query_save(name, sql):
    sql = urllib.unquote_plus(sql)
    if CustomQueries.objects.filter(name=name):
        old_query = CustomQueries.objects.get(name=name)
        old_query.query = sql
        old_query.save()
    else:
        nqs = CustomQueries(name=name, query=sql)
        nqs.save()
        return
    return


def load_query(query_id, arg):
    u"""
    Запрашивает запрос из модели по query_id
    """
    query_text = CustomQueries.objects.get(id=query_id)
    if arg == False:
        return query_text.query
    else:
        return query_text.name