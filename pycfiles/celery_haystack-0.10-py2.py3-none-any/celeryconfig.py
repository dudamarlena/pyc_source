# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/brent/coding/englue/fba/celery-geolocator/build/lib/examples/strait_celery/celeryconfig.py
# Compiled at: 2014-08-09 13:41:56
__author__ = 'brent'
BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'amqp://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RDB_PORT = '6902'
CELERY_ROUTES = {'celery_geolocator.tasks.geocode': {'queue': 'geocode', 'routing_key': 'geocode'}}
CELERY_CREATE_MISSING_QUEUES = True