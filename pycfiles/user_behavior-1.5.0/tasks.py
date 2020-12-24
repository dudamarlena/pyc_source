# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Leslie/workspace/ctrip/cdportal/cdportal/venv/lib/python2.7/site-packages/user_behavior/tasks.py
# Compiled at: 2016-11-18 01:16:13
from __future__ import absolute_import
import json
from datetime import date
from django.forms import model_to_dict
from .services import set_es_url
from elasticsearch import Elasticsearch
from celery import shared_task

@shared_task(serializer='json')
def task_user_behavior(es_log_data):
    es = Elasticsearch(set_es_url())
    try:
        body = json.dumps(model_to_dict(es_log_data))
        es.index(index=('cd_event_log_{}').format(date.today()), doc_type='log', body=body)
    except:
        pass