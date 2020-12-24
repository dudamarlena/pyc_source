# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/logger.py
# Compiled at: 2017-04-23 10:30:41
import logging, os
from cloudmesh_client.common.util import grep
from cloudmesh_client.locations import config_file

def LOGGER(filename):
    """creates a logger with the given name.

    You can use it as follows::

       log = cloudmesh.util.LOGGER(__file__)
       log.error("this is an error")
       log.info("this is an info")
       log.warning("this is a warning")

    """
    pwd = os.getcwd()
    name = filename.replace(pwd, '$PWD')
    try:
        first, name = name.split('site-packages')
        name += '... site'
    except:
        pass

    loglevel = logging.CRITICAL
    try:
        level = grep('loglevel:', config_file('/cloudmesh_debug.yaml')).strip().split(':')[1].strip().lower()
        if level.upper() == 'DEBUG':
            loglevel = logging.DEBUG
        elif level.upper() == 'INFO':
            loglevel = logging.INFO
        elif level.upper() == 'WARNING':
            loglevel = logging.WARNING
        elif level.upper() == 'ERROR':
            loglevel = logging.ERROR
        else:
            level = logging.CRITICAL
    except:
        loglevel = logging.DEBUG

    log = logging.getLogger(name)
    log.setLevel(loglevel)
    formatter = logging.Formatter(('CM {0:>50}:%(lineno)s: %(levelname)6s - %(message)s').format(name))
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


def LOGGING_ON(log):
    """
    Switches logging on
    :param log: the logger for which we switch logging on 
    """
    try:
        log.setLevel(logging.DEBUG)
        return True
    except:
        return False


def LOGGING_OFF(log):
    """
    Switches logging off
    :param log: the logger for which we switch logging off
    """
    try:
        log.setLevel(logging.CRITICAL)
        return True
    except:
        return False