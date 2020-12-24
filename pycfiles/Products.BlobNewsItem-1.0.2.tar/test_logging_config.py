# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/tests/test_logging_config.py
# Compiled at: 2012-02-27 07:41:53
"""Test harness for the logging module. Run all tests.

Copyright (C) 2001-2002 Vinay Sajip. All Rights Reserved.
"""
import os, sys, string, tempfile, logging
from paste.script.util import logging_config

def message(s):
    sys.stdout.write('%s\n' % s)


config0 = '\n[loggers]\nkeys=root\n\n[handlers]\nkeys=hand1\n\n[formatters]\nkeys=form1\n\n[logger_root]\nlevel=NOTSET\nhandlers=hand1\n\n[handler_hand1]\nclass=StreamHandler\nlevel=NOTSET\nformatter=form1\nargs=(sys.stdout,)\n\n[formatter_form1]\nformat=%(levelname)s:%(name)s:%(message)s\ndatefmt=\n'
config1 = '\n[loggers]\nkeys=root,parser\n\n[handlers]\nkeys=hand1, hand2\n\n[formatters]\nkeys=form1, form2\n\n[logger_root]\nlevel=NOTSET\nhandlers=hand1,hand2\n\n[logger_parser]\nlevel=DEBUG\nhandlers=hand1\npropagate=1\nqualname=compiler.parser\n\n[handler_hand1]\nclass=StreamHandler\nlevel=NOTSET\nformatter=form1\nargs=(sys.stdout,)\n\n[handler_hand2]\nclass=StreamHandler\nlevel=NOTSET\nformatter=form2\nargs=(sys.stderr,)\n\n[formatter_form1]\nformat=%(levelname)s:%(name)s:%(message)s\ndatefmt=\n\n[formatter_form2]\nformat=:%(message)s\ndatefmt=\n'
config2 = string.replace(config1, 'sys.stdout', 'sys.stbout')
config3 = string.replace(config1, 'formatter=form1', 'formatter=misspelled_name')
config4 = string.replace(config1, 'class=StreamHandler', 'class=logging.StreamHandler')

def test4():
    for i in range(5):
        conf = globals()[('config%d' % i)]
        sys.stdout.write('config%d: ' % i)
        loggerDict = logging.getLogger().manager.loggerDict
        logging._acquireLock()
        try:
            saved_handlers = logging._handlers.copy()
            if hasattr(logging, '_handlerList'):
                saved_handler_list = logging._handlerList[:]
            saved_loggers = loggerDict.copy()
        finally:
            logging._releaseLock()

        try:
            fn = tempfile.mktemp('.ini')
            f = open(fn, 'w')
            f.write(conf)
            f.close()
            try:
                logging_config.fileConfig(fn)
                logging_config.fileConfig(fn)
            except:
                if i not in (2, 3):
                    raise
                t = sys.exc_info()[0]
                message(str(t) + ' (expected)')
            else:
                message('ok.')

            os.remove(fn)
        finally:
            logging._acquireLock()
            try:
                logging._handlers.clear()
                logging._handlers.update(saved_handlers)
                if hasattr(logging, '_handlerList'):
                    logging._handlerList[:] = saved_handler_list
                loggerDict = logging.getLogger().manager.loggerDict
                loggerDict.clear()
                loggerDict.update(saved_loggers)
            finally:
                logging._releaseLock()


test5_config = '\n[loggers]\nkeys=root\n\n[handlers]\nkeys=hand1\n\n[formatters]\nkeys=form1\n\n[logger_root]\nlevel=NOTSET\nhandlers=hand1\n\n[handler_hand1]\nclass=StreamHandler\nlevel=NOTSET\nformatter=form1\nargs=(sys.stdout,)\n\n[formatter_form1]\n#class=test.test_logging.FriendlyFormatter\nclass=test_logging_config.FriendlyFormatter\nformat=%(levelname)s:%(name)s:%(message)s\ndatefmt=\n'

class FriendlyFormatter(logging.Formatter):

    def formatException(self, ei):
        return "%s... Don't panic!" % str(ei[0])


def test5():
    loggerDict = logging.getLogger().manager.loggerDict
    logging._acquireLock()
    try:
        saved_handlers = logging._handlers.copy()
        if hasattr(logging, '_handlerList'):
            saved_handler_list = logging._handlerList[:]
        saved_loggers = loggerDict.copy()
    finally:
        logging._releaseLock()

    try:
        fn = tempfile.mktemp('.ini')
        f = open(fn, 'w')
        f.write(test5_config)
        f.close()
        logging_config.fileConfig(fn)
        try:
            raise KeyError
        except KeyError:
            logging.exception('just testing')

        os.remove(fn)
        hdlr = logging.getLogger().handlers[0]
        logging.getLogger().handlers.remove(hdlr)
    finally:
        logging._acquireLock()
        try:
            logging._handlers.clear()
            logging._handlers.update(saved_handlers)
            if hasattr(logging, '_handlerList'):
                logging._handlerList[:] = saved_handler_list
            loggerDict = logging.getLogger().manager.loggerDict
            loggerDict.clear()
            loggerDict.update(saved_loggers)
        finally:
            logging._releaseLock()