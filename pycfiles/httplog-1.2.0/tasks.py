# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\cd2\env\lib\site-packages\httplog\tasks.py
# Compiled at: 2016-11-29 02:34:15
from __future__ import absolute_import
import json
from datetime import date
from .services import is_log_to_db, is_log_to_es, save_httplog_data, get_es_log_data, get_request_user, set_es_url
from elasticsearch import Elasticsearch
from celery import shared_task

def datetime_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    raise TypeError


@shared_task(serializer='json')
def task_http_log(http_log_config, http_log_data, request):
    if is_log_to_db(http_log_config):
        save_httplog_data(http_log_data, request)
    if is_log_to_es(http_log_config):
        es_log_data = get_es_log_data(http_log_data, get_request_user(request))
        body = json.dumps(es_log_data, default=datetime_handler)
        es = Elasticsearch(set_es_url())
        es.index(index=('cd_http_log_{}').format(date.today()), doc_type='log', body=body)