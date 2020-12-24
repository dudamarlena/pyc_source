# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sk/seckiss/rfw/rfw/config.py
# Compiled at: 2014-03-26 05:27:02
from __future__ import print_function
import logging, sys, types, os.path, re
from ConfigParser import RawConfigParser, NoOptionError
log = logging.getLogger(('lib.{}').format(__name__))
log.addHandler(logging.NullHandler())

class ConfigError(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)


class Config:

    def __init__(self, path, section='config'):
        self.path = path
        self.section = section
        if not os.path.isfile(path):
            raise IOError(('Could not find config file {}').format(path))
        self.parser = RawConfigParser(allow_no_value=True)
        self.parser.read(self.path)

    def _get(self, opt):
        """Get option value from [config] section of config file.
        It may return None if valueless option present (option name only). It's possible because allow_no_value=True
        It may raise NoOptionError if option not present
        It may raise NoSectionError
        """
        return self.parser.get(self.section, opt)

    def _getflag(self, opt, log_msg=''):
        """Return True if valueless option present in config file. False otherwise.
        """
        try:
            return self._get(opt) is None
        except NoOptionError:
            if log_msg:
                log.info(log_msg)

        return False

    def _getfile(self, opt):
        filename = self._get(opt)
        if filename and os.path.isfile(filename):
            return filename
        raise self.config_error(('Could not find the file {} = {}').format(opt, filename))

    def config_error(self, msg):
        return ConfigError(('Configuration error in {}: {}').format(self.path, msg))


def set_logging(log, loglevelnum, logfile, verbose_console=False):
    """Configure standard logging for the application. One ERROR level handler to stderr and one file handler with specified loglevelnum to logfile.
        log argument is the main (parent) application logger.
    """
    if loglevelnum not in [logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]:
        log.error('Incorrect loglevel value')
        sys.exit(1)
    try:
        log.setLevel(logging.DEBUG)
        fh = logging.FileHandler(logfile)
        fh.setLevel(loglevelnum)
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d.%(funcName)s() - %(message)s'))
        log.addHandler(fh)
        ch = logging.StreamHandler()
        if verbose_console:
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.ERROR)
        ch.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
        log.addHandler(ch)
        logging.getLogger('lib').addHandler(fh)
    except IOError as e:
        msg = str(e)
        if e.errno == 13:
            msg += '\nYou need to be root'
        raise ConfigError(msg)