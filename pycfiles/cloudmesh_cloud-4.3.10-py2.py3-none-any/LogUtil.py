# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/LogUtil.py
# Compiled at: 2017-04-23 10:30:41
import inspect, logging
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.util import path_expand
from cloudmesh_client.default import Default
LOGGER = logging.getLogger('LogUtil')

class LogUtil(object):
    FORMAT = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(funcName)s() %(message)s'
    LOG_LEVEL_KEY = 'log_level'
    DEFAULT_LOG_LEVEL = 'ERROR'
    category = 'general'

    @staticmethod
    def save():
        """
        save the loglevel for a cloud to the cloudmesh.yaml file
        """
        log_level = Default.get(name=LogUtil.LOG_LEVEL_KEY, category=LogUtil.category) or LogUtil.DEFAULT_LOG_LEVEL
        config = ConfigDict('cloudmesh.yaml')
        config['cloudmesh']['logging']['level'] = log_level
        config.save()

    @staticmethod
    def set_level(log_level):
        """
        sets th eloglevel in the database and the loglevel file from
        cloudmesh.yaml
        :param log_level: the loglevel
        :return:
        """
        level = log_level.upper()
        Default.set(key=LogUtil.LOG_LEVEL_KEY, value=log_level, category=LogUtil.category)
        log_level_obj = LogUtil.get_level_obj(log_level)
        config = ConfigDict('cloudmesh.yaml')
        log_file = config['cloudmesh']['logging']['file']
        logging.basicConfig(format=LogUtil.FORMAT, level=log_level_obj, filename=path_expand(log_file))
        LOGGER.info('Set log level to: ' + log_level)
        return 'Ok.'

    @staticmethod
    def get_level():
        """
        get the log level from database
        :param cloudname: The name of the cloud
        :return: the log level
        """
        log_level = Default.get(name=LogUtil.LOG_LEVEL_KEY, category=LogUtil.category)
        LOGGER.info('Returning Log Level: ' + log_level)
        return log_level

    @staticmethod
    def initialize_logging():
        """
        reads the log level from the cloudmesh.yaml file from
        cloudmesh.logging.level. If the value is not set the logging will be
        set to the default which is "ERROR"
        :return: the loglevel
        """
        config = ConfigDict('cloudmesh.yaml')
        log_level = config['cloudmesh']['logging']['level'] or LogUtil.DEFAULT_LOG_LEVEL
        print (
         'PPPP', log_level)
        LogUtil.set_level(log_level)

    @staticmethod
    def get_logger():
        """
        get caller file name
        :return: file name based on the context where the logger is caller
        """
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        the_class = module.__name__
        return logging.getLogger(the_class)

    @staticmethod
    def get_level_obj(log_level):
        """
        gets the log level when passing a string
        :param log_level: case insensitive string. Valid values are debug,
                          info, warning, critical, error
        :return: a logging level
        """
        level = log_level.lower()
        if level == 'debug':
            log_level = logging.DEBUG
        elif level == 'info':
            level = logging.INFO
        elif level == 'warning':
            level = logging.WARNING
        elif level == 'critical':
            level = logging.CRITICAL
        elif level == 'error':
            level = logging.ERROR
        else:
            level = logging.DEBUG
        return level