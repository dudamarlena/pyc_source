# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/config_templates/airflow_local_settings.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 8143 bytes
import os
from typing import Dict, Any
import six
from airflow import configuration as conf
from airflow.utils.file import mkdirs
LOG_LEVEL = conf.get('core', 'LOGGING_LEVEL').upper()
FAB_LOG_LEVEL = conf.get('core', 'FAB_LOGGING_LEVEL').upper()
LOG_FORMAT = conf.get('core', 'LOG_FORMAT')
COLORED_LOG_FORMAT = conf.get('core', 'COLORED_LOG_FORMAT')
COLORED_LOG = conf.getboolean('core', 'COLORED_CONSOLE_LOG')
COLORED_FORMATTER_CLASS = conf.get('core', 'COLORED_FORMATTER_CLASS')
BASE_LOG_FOLDER = conf.get('core', 'BASE_LOG_FOLDER')
PROCESSOR_LOG_FOLDER = conf.get('scheduler', 'CHILD_PROCESS_LOG_DIRECTORY')
DAG_PROCESSOR_MANAGER_LOG_LOCATION = conf.get('core', 'DAG_PROCESSOR_MANAGER_LOG_LOCATION')
FILENAME_TEMPLATE = conf.get('core', 'LOG_FILENAME_TEMPLATE')
PROCESSOR_FILENAME_TEMPLATE = conf.get('core', 'LOG_PROCESSOR_FILENAME_TEMPLATE')
REMOTE_BASE_LOG_FOLDER = conf.get('core', 'REMOTE_BASE_LOG_FOLDER')
ELASTICSEARCH_HOST = conf.get('elasticsearch', 'HOST')
ELASTICSEARCH_LOG_ID_TEMPLATE = conf.get('elasticsearch', 'LOG_ID_TEMPLATE')
ELASTICSEARCH_END_OF_LOG_MARK = conf.get('elasticsearch', 'END_OF_LOG_MARK')
ELASTICSEARCH_WRITE_STDOUT = conf.get('elasticsearch', 'WRITE_STDOUT')
ELASTICSEARCH_JSON_FORMAT = conf.get('elasticsearch', 'JSON_FORMAT')
ELASTICSEARCH_JSON_FIELDS = conf.get('elasticsearch', 'JSON_FIELDS')
FORMATTER_CLASS_KEY = '()' if six.PY2 else 'class'
DEFAULT_LOGGING_CONFIG = {'version':1, 
 'disable_existing_loggers':False, 
 'formatters':{'airflow':{'format': LOG_FORMAT}, 
  'airflow_coloured':{'format': COLORED_LOG_FORMAT if COLORED_LOG else LOG_FORMAT, 
   FORMATTER_CLASS_KEY: COLORED_FORMATTER_CLASS if COLORED_LOG else 'logging.Formatter'}}, 
 'handlers':{'console':{'class':'airflow.utils.log.logging_mixin.RedirectStdHandler', 
   'formatter':'airflow_coloured', 
   'stream':'sys.stdout'}, 
  'task':{'class':'airflow.utils.log.file_task_handler.FileTaskHandler', 
   'formatter':'airflow', 
   'base_log_folder':os.path.expanduser(BASE_LOG_FOLDER), 
   'filename_template':FILENAME_TEMPLATE}, 
  'processor':{'class':'airflow.utils.log.file_processor_handler.FileProcessorHandler', 
   'formatter':'airflow', 
   'base_log_folder':os.path.expanduser(PROCESSOR_LOG_FOLDER), 
   'filename_template':PROCESSOR_FILENAME_TEMPLATE}}, 
 'loggers':{'airflow.processor':{'handlers':[
    'processor'], 
   'level':LOG_LEVEL, 
   'propagate':False}, 
  'airflow.task':{'handlers':[
    'task'], 
   'level':LOG_LEVEL, 
   'propagate':False}, 
  'flask_appbuilder':{'handler':[
    'console'], 
   'level':FAB_LOG_LEVEL, 
   'propagate':True}}, 
 'root':{'handlers':[
   'console'], 
  'level':LOG_LEVEL}}
DEFAULT_DAG_PARSING_LOGGING_CONFIG = {'handlers':{'processor_manager': {'class':'logging.handlers.RotatingFileHandler', 
                        'formatter':'airflow', 
                        'filename':DAG_PROCESSOR_MANAGER_LOG_LOCATION, 
                        'mode':'a', 
                        'maxBytes':104857600, 
                        'backupCount':5}}, 
 'loggers':{'airflow.processor_manager': {'handlers':[
                                 'processor_manager'], 
                                'level':LOG_LEVEL, 
                                'propagate':False}}}
REMOTE_HANDLERS = {'s3':{'task': {'class':'airflow.utils.log.s3_task_handler.S3TaskHandler', 
           'formatter':'airflow', 
           'base_log_folder':os.path.expanduser(BASE_LOG_FOLDER), 
           's3_log_folder':REMOTE_BASE_LOG_FOLDER, 
           'filename_template':FILENAME_TEMPLATE}}, 
 'gcs':{'task': {'class':'airflow.utils.log.gcs_task_handler.GCSTaskHandler', 
           'formatter':'airflow', 
           'base_log_folder':os.path.expanduser(BASE_LOG_FOLDER), 
           'gcs_log_folder':REMOTE_BASE_LOG_FOLDER, 
           'filename_template':FILENAME_TEMPLATE}}, 
 'wasb':{'task': {'class':'airflow.utils.log.wasb_task_handler.WasbTaskHandler', 
           'formatter':'airflow', 
           'base_log_folder':os.path.expanduser(BASE_LOG_FOLDER), 
           'wasb_log_folder':REMOTE_BASE_LOG_FOLDER, 
           'wasb_container':'airflow-logs', 
           'filename_template':FILENAME_TEMPLATE, 
           'delete_local_copy':False}}, 
 'elasticsearch':{'task': {'class':'airflow.utils.log.es_task_handler.ElasticsearchTaskHandler', 
           'formatter':'airflow', 
           'base_log_folder':os.path.expanduser(BASE_LOG_FOLDER), 
           'log_id_template':ELASTICSEARCH_LOG_ID_TEMPLATE, 
           'filename_template':FILENAME_TEMPLATE, 
           'end_of_log_mark':ELASTICSEARCH_END_OF_LOG_MARK, 
           'host':ELASTICSEARCH_HOST, 
           'write_stdout':ELASTICSEARCH_WRITE_STDOUT, 
           'json_format':ELASTICSEARCH_JSON_FORMAT, 
           'json_fields':ELASTICSEARCH_JSON_FIELDS}}}
REMOTE_LOGGING = conf.getboolean('core', 'remote_logging')
if os.environ.get('CONFIG_PROCESSOR_MANAGER_LOGGER') == 'True':
    DEFAULT_LOGGING_CONFIG['handlers'].update(DEFAULT_DAG_PARSING_LOGGING_CONFIG['handlers'])
    DEFAULT_LOGGING_CONFIG['loggers'].update(DEFAULT_DAG_PARSING_LOGGING_CONFIG['loggers'])
    processor_manager_handler_config = DEFAULT_DAG_PARSING_LOGGING_CONFIG['handlers']['processor_manager']
    directory = os.path.dirname(processor_manager_handler_config['filename'])
    mkdirs(directory, 493)
if REMOTE_LOGGING:
    if REMOTE_BASE_LOG_FOLDER.startswith('s3://'):
        DEFAULT_LOGGING_CONFIG['handlers'].update(REMOTE_HANDLERS['s3'])
if REMOTE_LOGGING and REMOTE_BASE_LOG_FOLDER.startswith('gs://'):
    DEFAULT_LOGGING_CONFIG['handlers'].update(REMOTE_HANDLERS['gcs'])
elif REMOTE_LOGGING and REMOTE_BASE_LOG_FOLDER.startswith('wasb'):
    DEFAULT_LOGGING_CONFIG['handlers'].update(REMOTE_HANDLERS['wasb'])
elif REMOTE_LOGGING:
    if ELASTICSEARCH_HOST:
        DEFAULT_LOGGING_CONFIG['handlers'].update(REMOTE_HANDLERS['elasticsearch'])