# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/logging_config.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3836 bytes
import logging, warnings
from logging.config import dictConfig
from airflow import configuration as conf
from airflow.exceptions import AirflowConfigException
from airflow.utils.module_loading import import_string
log = logging.getLogger(__name__)

def configure_logging():
    logging_class_path = ''
    try:
        logging_class_path = conf.get('core', 'logging_config_class')
    except AirflowConfigException:
        log.debug('Could not find key logging_config_class in config')

    if logging_class_path:
        try:
            logging_config = import_string(logging_class_path)
            assert isinstance(logging_config, dict)
            log.info('Successfully imported user-defined logging config from %s', logging_class_path)
        except Exception as err:
            raise ImportError('Unable to load custom logging from {} due to {}'.format(logging_class_path, err))

    else:
        logging_class_path = 'airflow.config_templates.airflow_local_settings.DEFAULT_LOGGING_CONFIG'
        logging_config = import_string(logging_class_path)
        log.debug('Unable to load custom logging, using default config instead')
    try:
        dictConfig(logging_config)
    except ValueError as e:
        log.warning('Unable to load the config, contains a configuration error.')
        raise e

    validate_logging_config(logging_config)
    return logging_class_path


def validate_logging_config(logging_config):
    task_log_reader = conf.get('core', 'task_log_reader')
    logger = logging.getLogger('airflow.task')

    def _get_handler(name):
        return next((h for h in logger.handlers if h.name == name), None)

    if _get_handler(task_log_reader) is None:
        if task_log_reader == 'file.task':
            if _get_handler('task'):
                warnings.warn('task_log_reader setting in [core] has a deprecated value of {!r}, but no handler with this name was found. Please update your config to use {!r}. Running config has been adjusted to match'.format(task_log_reader, 'task'), DeprecationWarning)
                conf.set('core', 'task_log_reader', 'task')
        else:
            raise AirflowConfigException("Configured task_log_reader {!r} was not a handler of the 'airflow.task' logger.".format(task_log_reader))