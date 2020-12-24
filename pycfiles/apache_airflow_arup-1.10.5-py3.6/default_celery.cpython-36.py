# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/config_templates/default_celery.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4104 bytes
import ssl
from airflow import configuration
from airflow.exceptions import AirflowConfigException, AirflowException
from airflow.utils.log.logging_mixin import LoggingMixin

def _broker_supports_visibility_timeout(url):
    return url.startswith('redis://') or url.startswith('sqs://')


log = LoggingMixin().log
broker_url = configuration.conf.get('celery', 'BROKER_URL')
broker_transport_options = configuration.conf.getsection('celery_broker_transport_options')
if 'visibility_timeout' not in broker_transport_options:
    if _broker_supports_visibility_timeout(broker_url):
        broker_transport_options['visibility_timeout'] = 21600
DEFAULT_CELERY_CONFIG = {'accept_content':['json', 'pickle'],  'event_serializer':'json', 
 'worker_prefetch_multiplier':1, 
 'task_acks_late':True, 
 'task_default_queue':configuration.conf.get('celery', 'DEFAULT_QUEUE'), 
 'task_default_exchange':configuration.conf.get('celery', 'DEFAULT_QUEUE'), 
 'broker_url':broker_url, 
 'broker_transport_options':broker_transport_options, 
 'result_backend':configuration.conf.get('celery', 'RESULT_BACKEND'), 
 'worker_concurrency':configuration.conf.getint('celery', 'WORKER_CONCURRENCY')}
celery_ssl_active = False
try:
    celery_ssl_active = configuration.conf.getboolean('celery', 'SSL_ACTIVE')
except AirflowConfigException:
    log.warning('Celery Executor will run without SSL')

try:
    if celery_ssl_active:
        if 'amqp://' in broker_url:
            broker_use_ssl = {'keyfile':configuration.conf.get('celery', 'SSL_KEY'), 
             'certfile':configuration.conf.get('celery', 'SSL_CERT'), 
             'ca_certs':configuration.conf.get('celery', 'SSL_CACERT'), 
             'cert_reqs':ssl.CERT_REQUIRED}
        else:
            if 'redis://' in broker_url:
                broker_use_ssl = {'ssl_keyfile':configuration.conf.get('celery', 'SSL_KEY'), 
                 'ssl_certfile':configuration.conf.get('celery', 'SSL_CERT'), 
                 'ssl_ca_certs':configuration.conf.get('celery', 'SSL_CACERT'), 
                 'ssl_cert_reqs':ssl.CERT_REQUIRED}
            else:
                raise AirflowException('The broker you configured does not support SSL_ACTIVE to be True. Please use RabbitMQ or Redis if you would like to use SSL for broker.')
        DEFAULT_CELERY_CONFIG['broker_use_ssl'] = broker_use_ssl
except AirflowConfigException:
    raise AirflowException('AirflowConfigException: SSL_ACTIVE is True, please ensure SSL_KEY, SSL_CERT and SSL_CACERT are set')
except Exception as e:
    raise AirflowException('Exception: There was an unknown Celery SSL Error. Please ensure you want to use SSL and/or have all necessary certs and key ({}).'.format(e))

result_backend = DEFAULT_CELERY_CONFIG['result_backend']
if 'amqp://' in result_backend or 'redis://' in result_backend or 'rpc://' in result_backend:
    log.warning('You have configured a result_backend of %s, it is highly recommended to use an alternative result_backend (i.e. a database).', result_backend)