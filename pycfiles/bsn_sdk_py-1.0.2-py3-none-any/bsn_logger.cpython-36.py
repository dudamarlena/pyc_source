# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\until\bsn_logger.py
# Compiled at: 2020-04-23 03:04:14
# Size of source mod 2**32: 1370 bytes
import logging, sys, re
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
logger = logging.getLogger('bsn_sdk_py')

def log_debug(message, **params):
    msg = logfmt(dict(message=message, **params))
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(dict(message=message, **params))
    logger.info(msg)


def logfmt(props):

    def fmt(key, val):
        if PY3:
            if hasattr(val, 'decode'):
                val = val.decode('utf-8')
            if not isinstance(val, str):
                val = str(val)
        else:
            if re.search('\\s', val):
                val = repr(val)
            if re.search('\\s', key):
                key = repr(key)
        return '{key}={val}'.format(key=key, val=val)

    return ' '.join([fmt(key, val) for key, val in sorted(props.items())])


if __name__ == '__main__':
    FORMAT = '%(asctime)s %(thread)d %(message)s'
    logging.basicConfig(level=(logging.INFO), format=FORMAT, datefmt='[%Y-%m-%d %H:%M:%S]')
    log_info(('dsdas', 111))