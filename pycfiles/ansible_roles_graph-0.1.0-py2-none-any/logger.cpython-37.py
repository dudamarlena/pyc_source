# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ansible_readme/logger.py
# Compiled at: 2019-10-30 07:43:10
# Size of source mod 2**32: 3779 bytes
__doc__ = 'Logging module.\n\nThis code is largely borrowed from the Ansible Molecule logger module.\n'
import logging, os, sys, colorama

def to_bool(value):
    if isinstance(value, bool):
        return True
    if isinstance(value, str):
        return str(value).lower() in ('true', 'on', 'yes', 'false', 'off', 'no')
    return False


def should_do_markup():
    py_colors = os.environ.get('PY_COLORS', None)
    if py_colors is not None:
        return to_bool(py_colors, strict=False)
    return sys.stdout.isatty() and os.environ.get('TERM') != 'dumb'


SUCCESS = 100
OUT = 101

class LogFilter(object):

    def __init__(self, level):
        self._LogFilter__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self._LogFilter__level


class CustomLogger(logging.getLoggerClass()):

    def __init__(self, name, level=logging.NOTSET):
        super(logging.getLoggerClass(), self).__init__(name, level)
        logging.addLevelName(SUCCESS, 'SUCCESS')
        logging.addLevelName(OUT, 'OUT')

    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(SUCCESS):
            (self._log)(SUCCESS, msg, args, **kwargs)

    def out(self, msg, *args, **kwargs):
        if self.isEnabledFor(OUT):
            (self._log)(OUT, msg, args, **kwargs)


class CustomFormatter(logging.Formatter):

    def format(self, record):
        return super(CustomFormatter, self).format(record)


def get_logger(name=None):
    logging.setLoggerClass(CustomLogger)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_get_info_handler())
    logger.addHandler(_get_out_handler())
    logger.addHandler(_get_warn_handler())
    logger.addHandler(_get_error_handler())
    logger.addHandler(_get_critical_handler())
    logger.addHandler(_get_success_handler())
    logger.propagate = False
    return logger


def _get_info_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.addFilter(LogFilter(logging.INFO))
    handler.setFormatter(CustomFormatter('--> {}'.format(cyan_text('%(message)s'))))
    return handler


def _get_out_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(OUT)
    handler.addFilter(LogFilter(OUT))
    handler.setFormatter(CustomFormatter('    %(message)s'))
    return handler


def _get_warn_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.WARN)
    handler.addFilter(LogFilter(logging.WARN))
    handler.setFormatter(CustomFormatter(yellow_text('%(message)s')))
    return handler


def _get_error_handler():
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.ERROR)
    handler.addFilter(LogFilter(logging.ERROR))
    handler.setFormatter(CustomFormatter(red_text('%(message)s')))
    return handler


def _get_critical_handler():
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.CRITICAL)
    handler.addFilter(LogFilter(logging.CRITICAL))
    handler.setFormatter(CustomFormatter(red_text('ERROR: %(message)s')))
    return handler


def _get_success_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(SUCCESS)
    handler.addFilter(LogFilter(SUCCESS))
    handler.setFormatter(CustomFormatter(green_text('%(message)s')))
    return handler


def red_text(msg):
    return color_text(colorama.Fore.RED, msg)


def yellow_text(msg):
    return color_text(colorama.Fore.YELLOW, msg)


def green_text(msg):
    return color_text(colorama.Fore.GREEN, msg)


def cyan_text(msg):
    return color_text(colorama.Fore.CYAN, msg)


def color_text(color, msg):
    return '{}{}{}'.format(color, msg, colorama.Style.RESET_ALL)