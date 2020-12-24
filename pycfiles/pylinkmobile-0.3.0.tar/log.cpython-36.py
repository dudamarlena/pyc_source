# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/log.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 5454 bytes
__doc__ = '\nlog.py - PyLink logging module.\n\nThis module contains the logging portion of the PyLink framework. Plugins can\naccess the global logger object by importing "log" from this module\n(from log import log).\n'
import logging, logging.handlers, os
from . import conf, world
fileloggers = []
logdir = os.path.join(os.getcwd(), 'log')
os.makedirs(logdir, exist_ok=True)
_format = '%(asctime)s [%(levelname)s] %(message)s'
logformatter = logging.Formatter(_format)

def _get_console_log_level():
    """
    Returns the configured console log level.
    """
    logconf = conf.conf['logging']
    return logconf.get('console', logconf.get('stdout')) or 'INFO'


world.console_handler = logging.StreamHandler()
world.console_handler.setFormatter(logformatter)
world.console_handler.setLevel(_get_console_log_level())
log = logging.getLogger('pylinkirc')
log.addHandler(world.console_handler)
log.setLevel(1)

def _make_file_logger(filename, level=None):
    """
    Initializes a file logging target with the given filename and level.
    """
    global fileloggers
    target = os.path.join(logdir, '%s-%s.log' % (conf.confname, filename))
    logrotconf = conf.conf.get('logging', {}).get('filerotation', {})
    maxbytes = logrotconf.get('max_bytes', 20971520)
    backups = logrotconf.get('backup_count', 5)
    filelogger = logging.handlers.RotatingFileHandler(target, maxBytes=maxbytes, backupCount=backups, encoding='utf-8')
    filelogger.setFormatter(logformatter)
    level = level or _get_console_log_level()
    filelogger.setLevel(level)
    log.addHandler(filelogger)
    fileloggers.append(filelogger)
    return filelogger


def _stop_file_loggers():
    """
    De-initializes all file loggers.
    """
    for handler in fileloggers.copy():
        handler.close()
        log.removeHandler(handler)
        fileloggers.remove(handler)


files = conf.conf['logging'].get('files')
if files:
    for filename, config in files.items():
        if isinstance(config, dict):
            _make_file_logger(filename, config.get('loglevel'))
        else:
            log.warning('Got invalid file logging pair %r: %r; are your indentation and block commenting consistent?', filename, config)

log.debug('log: Emptying _log_queue')
while world._log_queue:
    level, text = world._log_queue.popleft()
    log.log(level, text)

log.debug('log: Emptied _log_queue')

class PyLinkChannelLogger(logging.Handler):
    """PyLinkChannelLogger"""

    def __init__(self, irc, channel, level=None):
        super(PyLinkChannelLogger, self).__init__()
        self.irc = irc
        self.channel = channel
        self.called = False
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        self.setFormatter(formatter)
        level = level or log.getEffectiveLevel()
        self.setLevel(level)
        loglevel = max(self.level, 20)
        self.setLevel(loglevel)

    def emit(self, record):
        """
        Logs a record to the configured channels for the network given.
        """
        if self.irc.pseudoclient:
            if self.irc.connected.is_set():
                if self.channel in self.irc.channels:
                    if not self.called:
                        self.called = True
                        msg = self.format(record)
                        for line in msg.splitlines():
                            try:
                                self.irc.msg(self.channel, line)
                            except:
                                return
                            else:
                                self.called = False