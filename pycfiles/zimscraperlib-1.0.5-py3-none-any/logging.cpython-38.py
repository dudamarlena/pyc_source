# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/envs/nautilus/lib/python3.8/site-packages/zimscraperlib/logging.py
# Compiled at: 2020-04-21 13:26:44
# Size of source mod 2**32: 2389 bytes
import sys, logging
from logging.handlers import RotatingFileHandler
from .constants import NAME
DEFAULT_FORMAT = '[%(name)s::%(asctime)s] %(levelname)s:%(message)s'
VERBOSE_DEPENDENCIES = ['urllib3', 'PIL', 'boto3', 'botocore', 's3transfer']

def getLogger(name, level=logging.INFO, console=sys.stdout, log_format=DEFAULT_FORMAT, file=False, file_level=None, file_format=None, file_max=1048576, file_nb_backup=1, deps_level=logging.WARNING, additional_deps=[]):
    """ configured logger for most usages

        - name: name of your logger
        - level: console level
        - log_format: format string
        - console: False | True (sys.stdout) | sys.stdout | sys.stderr
        - file: False | pathlib.Path
        - file_level: log level for file or console_level
        - file_format: format string for file or log_format
        - deps_level: log level for idendified verbose dependencies
        - additional_deps: additional modules names of verbose dependencies
            to assign deps_level to """
    logging.Logger(NAME).setLevel(level)
    for logger_name in set(VERBOSE_DEPENDENCIES + additional_deps):
        logging.getLogger(logger_name).setLevel(logging.WARNING)
    else:
        logger = logging.Logger(name)
        logger.setLevel(logging.DEBUG)
        if console:
            console_handler = logging.StreamHandler(console)
            console_handler.setFormatter(logging.Formatter(log_format))
            console_handler.setLevel(level)
            logger.addHandler(console_handler)
        if file:
            file_handler = RotatingFileHandler(file,
              maxBytes=file_max, backupCount=file_nb_backup)
            file_handler.setFormatter(logging.Formatter(file_format or log_format))
            file_handler.setLevel(file_level or level)
            logger.addHandler(file_handler)
        return logger


def nicer_args_join(args):
    """ slightly better concateated list of subprocess args for display """
    nargs = args[0:1]
    for arg in args[1:]:
        nargs.append(arg if arg.startswith('-') else '"{}"'.format(arg))
    else:
        return ' '.join(nargs)