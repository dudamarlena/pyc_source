# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/chrisr/Code/airflow/airflow/config_templates/airflow_local_settings.py
# Compiled at: 2017-10-03 21:40:48
import os
from airflow import configuration as conf
LOG_LEVEL = conf.get('core', 'LOGGING_LEVEL').upper()
LOG_FORMAT = conf.get('core', 'log_format')
BASE_LOG_FOLDER = conf.get('core', 'BASE_LOG_FOLDER')
FILENAME_TEMPLATE = '{{ ti.dag_id }}/{{ ti.task_id }}/{{ ts }}/{{ try_number }}.log'
DEFAULT_LOGGING_CONFIG = {'version': 1, 
   'disable_existing_loggers': False, 
   'formatters': {'airflow.task': {'format': LOG_FORMAT}}, 
   'handlers': {'console': {'class': 'logging.StreamHandler', 
                            'formatter': 'airflow.task', 
                            'stream': 'ext://sys.stdout'}, 
                'file.task': {'class': 'airflow.utils.log.file_task_handler.FileTaskHandler', 
                              'formatter': 'airflow.task', 
                              'base_log_folder': os.path.expanduser(BASE_LOG_FOLDER), 
                              'filename_template': FILENAME_TEMPLATE}}, 
   'loggers': {'airflow.task': {'handlers': [
                                           'file.task'], 
                                'level': LOG_LEVEL, 
                                'propagate': False}, 
               'airflow.task_runner': {'handlers': [
                                                  'file.task'], 
                                       'level': LOG_LEVEL, 
                                       'propagate': True}, 
               'airflow': {'handlers': [
                                      'console'], 
                           'level': LOG_LEVEL, 
                           'propagate': False}}}