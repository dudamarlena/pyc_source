# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soklog/__init__.py
# Compiled at: 2013-12-10 05:52:37
# Size of source mod 2**32: 2209 bytes
import logging, inspect
from os import path

class SokLog(object):

    def __init__(self, module, log_name):
        self.setUpModule(module, log_name)

    def _get_args_as_string(self, args):
        args = list(args)
        args = [str(arg) for arg in args]
        return ' '.join(args)

    def info(self, *args, **kwargs):
        msg = self._get_args_as_string(args)
        self.log.info(msg, **kwargs)

    def warning(self, *args, **kwargs):
        msg = self._get_args_as_string(args)
        self.log.warning(msg, **kwargs)

    def debug(self, *args, **kwargs):
        level = kwargs.get('level', 1)
        msg = self._get_args_as_string(args)
        main_path = path.dirname(self.module.__file__)
        src_path = inspect.stack()[level][1]
        src_path = '.' + src_path[len(main_path):]
        line = inspect.stack()[level][2]
        msg = '%s:%d %s' % (src_path, line, msg)
        self.log.debug(msg, **kwargs)

    def error(self, *args, **kwargs):
        self.log.error(*args, **kwargs)

    def start_file_logging(self, path):
        hdlr = logging.FileHandler(path)
        fmt = logging.Formatter('%(asctime)-10s %(message)s')
        hdlr.setFormatter(fmt)
        self.log.addHandler(hdlr)
        self.log.setLevel(logging.DEBUG)

    def start_stdout_logging(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)-10s %(message)s', datefmt='%H:%M:%S')

    def setUpModule(self, module, log_name):
        self.module = module
        self.log = logging.getLogger(log_name)


_DEFAULT = SokLog(None, None)

def init(module, log_name):
    _DEFAULT.__init__(module, log_name)


def info(*args, **kwargs):
    return _DEFAULT.info(*args, **kwargs)


def warning(*args, **kwargs):
    return _DEFAULT.warning(*args, **kwargs)


def debug(*args, **kwargs):
    kwargs['level'] = 2
    return _DEFAULT.debug(*args, **kwargs)


def error(*args, **kwargs):
    return _DEFAULT.error(*args, **kwargs)


def start_file_logging(*args, **kwargs):
    return _DEFAULT.start_file_logging(*args, **kwargs)


def start_stdout_logging(*args, **kwargs):
    return _DEFAULT.start_stdout_logging(*args, **kwargs)