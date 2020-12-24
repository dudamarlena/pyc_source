# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/config.py
# Compiled at: 2015-10-11 07:17:06
import os, logging
from dbmanagr.logger import logger
from dbmanagr.options import Options
from dbmanagr.utils import unicode_decode
from importlib import import_module
import dbmanagr.driver as driver
for mod in driver.__all__:
    import_module(('dbmanagr.driver.{0}').format(mod)).init()

class Config(object):

    @staticmethod
    def init(argv, parser):
        options = Options(unicode_decode(argv), parser)
        logging.basicConfig(stream=options.logfile, level=options.loglevel, format='%(asctime)s %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logger.info('\n###\n### %s called with args: %s\n###', parser.prog, options.argv)
        logger.debug('Options: %s', options)
        logger.debug('Environment: %s', dict(filter(lambda (k, v): k.startswith('DBNAV_'), os.environ.iteritems())))
        return options