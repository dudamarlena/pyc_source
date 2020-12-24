# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dblogger/tests/test_configure.py
# Compiled at: 2015-04-26 18:06:04
"""tests for dblogger.configure"""
import logging
from StringIO import StringIO
import yaml
from dblogger import configure_logging

def test_default_config(capsys):
    configure_logging({})
    logger = logging.getLogger('dblogger.test_global')
    logger.critical('test')
    out, err = capsys.readouterr()
    print out
    assert err[34:46] == 'test_configu'
    assert err[52:] == 'CRITICAL test\n'


def test_change_log_level_only(capsys):
    config = '\n    logging:\n        version: 1\n        root:\n            level: DEBUG\n    '
    config = yaml.load(StringIO(config))
    configure_logging(config)
    logger = logging.getLogger('dblogger.test_global')
    logger.critical('test')
    logger.debug('test 2')
    out, err = capsys.readouterr()
    print out
    assert err[34:46] == 'test_configu'
    assert err[52:66] == 'CRITICAL test\n'
    assert err[100:112] == 'test_configu'
    assert err[118:] == 'DEBUG    test 2\n'


def test_toplevel_config(capsys):
    config = "\n    logging:\n        version: 1\n        formatters:\n            toplevelf:\n                format: 'toplevel %(levelname)s %(message)s'\n        handlers:\n            toplevel:\n                class: logging.StreamHandler\n                formatter: toplevelf\n        root:\n            handlers: [toplevel]\n    "
    config = yaml.load(StringIO(config))
    configure_logging(config)
    logger = logging.getLogger('dblogger.test_global')
    logger.critical('test')
    out, err = capsys.readouterr()
    print out
    assert err == 'toplevel CRITICAL test\n'


def test_inline_config(capsys):
    config = "\n    version: 1\n    formatters:\n        inlinef:\n            format: 'inline %(levelname)s %(message)s'\n    handlers:\n        inline:\n            class: logging.StreamHandler\n            formatter: inlinef\n    root:\n        handlers: [inline]\n    "
    config = yaml.load(StringIO(config))
    configure_logging(config)
    logger = logging.getLogger('dblogger.test_global')
    logger.critical('test')
    out, err = capsys.readouterr()
    print out
    assert err == 'inline CRITICAL test\n'