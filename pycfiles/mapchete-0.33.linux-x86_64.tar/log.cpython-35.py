# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/log.py
# Compiled at: 2019-07-19 05:18:26
# Size of source mod 2**32: 3895 bytes
"""
Custom loggers for external code such as user processes & drivers.

This is necessary because if using the logging module directly, the namespace
is not assigned properly and log levels & log handlers cannot be assigned
correctly.
"""
from itertools import chain
import logging, pkg_resources, warnings
all_mapchete_packages = set(v.module_name.split('.')[0] for v in chain(pkg_resources.iter_entry_points('mapchete.formats.drivers'), pkg_resources.iter_entry_points('mapchete.processes')))
key_value_replace_patterns = {'AWS_ACCESS_KEY_ID': '***', 
 'AWS_SECRET_ACCESS_KEY': '***'}

class KeyValueFilter(logging.Filter):
    __doc__ = '\n    This filter looks for dictionaries passed on to log messages and replaces its values\n    with a replacement if key matches the pattern.\n\n    Examples\n    --------\n    >>> stream_handler.addFilter(\n    ...     KeyValueFilter(\n    ...         key_value_replace={\n    ...             "AWS_ACCESS_KEY_ID": "***",\n    ...             "AWS_SECRET_ACCESS_KEY": "***",\n    ...         }\n    ...     )\n    ... )\n    '

    def __init__(self, key_value_replace=None):
        super(KeyValueFilter, self).__init__()
        self._key_value_replace = key_value_replace or {}

    def filter(self, record):
        record.msg = self.redact(record.msg)
        if isinstance(record.args, dict):
            for k, v in record.args.items():
                record.args[k] = self.redact({k: v})[k]

        else:
            record.args = tuple(self.redact(arg) for arg in record.args)
        return True

    def redact(self, msg):
        if isinstance(msg, dict):
            out_msg = {}
            for k, v in msg.items():
                if isinstance(v, dict):
                    v = self.redact(v)
                else:
                    for k_replace, v_replace in self._key_value_replace.items():
                        v = v_replace if k == k_replace else v

                out_msg[k] = v

        else:
            out_msg = msg
        return out_msg


formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.WARNING)
stream_handler.addFilter(KeyValueFilter(key_value_replace=key_value_replace_patterns))
for i in all_mapchete_packages:
    logging.getLogger(i).addHandler(stream_handler)

def add_module_logger(module_name):
    logging.getLogger(module_name).setLevel(logging.getLogger('mapchete').getEffectiveLevel())
    for handler in logging.getLogger('mapchete').handlers:
        logging.getLogger(module_name).addHandler(handler)


def set_log_level(loglevel):
    stream_handler.setLevel(loglevel)
    for i in all_mapchete_packages:
        logging.getLogger(i).setLevel(loglevel)


def setup_logfile(logfile):
    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(KeyValueFilter(key_value_replace=key_value_replace_patterns))
    for i in all_mapchete_packages:
        logging.getLogger(i).addHandler(file_handler)
        logging.getLogger(i).setLevel(logging.DEBUG)


def user_process_logger(pname):
    """Logger to be used within a user process file."""
    warnings.warn(DeprecationWarning('user_process_logger() deprecated, you can use standard logging module instead.'))
    return logging.getLogger('mapchete.user_process.' + pname)


def driver_logger(dname):
    """Logger to be used from a driver plugin."""
    warnings.warn(DeprecationWarning('driver_logger() deprecated, you can use standard logging module instead.'))
    return logging.getLogger('mapchete.formats.drivers.' + dname)