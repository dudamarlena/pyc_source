# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/tmp/sample/lib/python3.5/site-packages/ezlogging.py
# Compiled at: 2016-07-16 04:08:11
# Size of source mod 2**32: 3095 bytes
import logging, logging.handlers, functools
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGER_LEVEL = logging.DEBUG
HANDLER_LEVEL = logging.DEBUG
root_logger = logging.getLogger()
_real_print = print

def monkeypatch_method(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


def _fake_print(*args, file=None, **kwargs):
    if file is None:
        _real_print('Logger!__ program.py __: ', *args, **kwargs)
    else:
        _real_print(*args, **kwargs)


@monkeypatch_method(logging.Logger)
def patch(self, f):

    @functools.wraps(f)
    def patched(*args, **kwargs):
        import builtins
        builtins.print = _fake_print
        try:
            f(*args, **kwargs)
        finally:
            builtins.print = _real_print

    return patched


def get_logger(name=None):
    return logging.getLogger(name)


def log_to_console(logger=root_logger, logger_level=LOGGER_LEVEL, handler_level=HANDLER_LEVEL, logging_format=FORMAT):
    """
    :param logger: if not set, will apply settings to root logger
    :param logger_level:
    :param handler_level:
    :param logging_format:
    :return:
    """
    logger.setLevel(logger_level)
    handler = logging.StreamHandler()
    handler.setLevel(handler_level)
    formatter = logging.Formatter(logging_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


FILE_NAME = 'log.out'
MAX_BYTE = 12328960
BACK_COUNT = 10

def log_to_rotated_file(logger=root_logger, logger_level=LOGGER_LEVEL, handler_level=HANDLER_LEVEL, logging_format=FORMAT, max_byte=MAX_BYTE, file_name=FILE_NAME, back_count=BACK_COUNT):
    logger.setLevel(logger_level)
    handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=max_byte, backupCount=back_count)
    handler.setLevel(handler_level)
    formatter = logging.Formatter(logging_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def log_to_syslogd(logger=root_logger, address=None, logger_level=LOGGER_LEVEL, handler_level=HANDLER_LEVEL, logging_format=FORMAT):
    assert address
    logger.setLevel(logger_level)
    handler = logging.handlers.SysLogHandler(address=address)
    handler.setLevel(handler_level)
    formatter = logging.Formatter(logging_format)
    handler.setFormatter(formatter)
    return logger


def main():
    logger = get_logger('test')
    log_to_console(logger)
    logger.debug('yo')

    @logger.patch
    def show():
        print('message in show')

    show()


if __name__ == '__main__':
    main()