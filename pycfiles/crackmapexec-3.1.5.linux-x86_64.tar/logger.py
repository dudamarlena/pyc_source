# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/logger.py
# Compiled at: 2016-12-29 01:49:52
import logging, sys, re
from termcolor import colored
from datetime import datetime
ansi_escape = re.compile('\\x1b[^m]*m')

def antiansi_emit(self, record):
    if self.stream is None:
        self.stream = self._open()
    record.msg = ansi_escape.sub('', record.message)
    logging.StreamHandler.emit(self, record)
    return


logging.FileHandler.emit = antiansi_emit

class CMEAdapter(logging.LoggerAdapter):

    def __init__(self, logger, extra=None):
        self.logger = logger
        self.extra = extra

    def process(self, msg, kwargs):
        if self.extra is None:
            return (('{}').format(msg), kwargs)
        else:
            if len(self.extra) == 1 and 'module' in self.extra.keys():
                return (('{:<59} {}').format(colored(self.extra['module'], 'cyan', attrs=['bold']), msg), kwargs)
            if len(self.extra) == 2 and 'module' in self.extra.keys() and 'host' in self.extra.keys():
                return (('{:<25} {:<33} {}').format(colored(self.extra['module'], 'cyan', attrs=['bold']), self.extra['host'], msg), kwargs)
            if 'module' in self.extra.keys():
                module_name = colored(self.extra['module'], 'cyan', attrs=['bold'])
            else:
                module_name = colored('CME', 'blue', attrs=['bold'])
            return (
             ('{:<25} {}:{} {:<15} {}').format(module_name, self.extra['host'], self.extra['port'], self.extra['hostname'].decode('utf-8') if self.extra['hostname'] else 'NONE', msg), kwargs)

    def info(self, msg, *args, **kwargs):
        msg, kwargs = self.process(('{} {}').format(colored('[*]', 'blue', attrs=['bold']), msg), kwargs)
        self.logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        msg, kwargs = self.process(('{} {}').format(colored('[-]', 'red', attrs=['bold']), msg), kwargs)
        self.logger.error(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        pass

    def success(self, msg, *args, **kwargs):
        msg, kwargs = self.process(('{} {}').format(colored('[+]', 'green', attrs=['bold']), msg), kwargs)
        self.logger.info(msg, *args, **kwargs)

    def highlight(self, msg, *args, **kwargs):
        msg, kwargs = self.process(('{}').format(colored(msg, 'yellow', attrs=['bold'])), kwargs)
        self.logger.info(msg, *args, **kwargs)

    def logMessage(self, message):
        self.highlight(message)


def setup_debug_logger():
    debug_output_string = ('{:<59} %(message)s').format(colored('DEBUG', 'magenta', attrs=['bold']))
    formatter = logging.Formatter(debug_output_string)
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.propagate = False
    root_logger.addHandler(streamHandler)
    root_logger.setLevel(logging.DEBUG)
    return root_logger


def setup_logger(level=logging.INFO, log_to_file=False, log_prefix=None, logger_name='CME'):
    formatter = logging.Formatter('%(message)s')
    if log_to_file:
        if not log_prefix:
            log_prefix = 'log'
        log_filename = ('{}_{}.log').format(log_prefix.replace('/', '_'), datetime.now().strftime('%Y-%m-%d'))
        fileHandler = logging.FileHandler(('./logs/{}').format(log_filename))
        fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setFormatter(formatter)
    cme_logger = logging.getLogger(logger_name)
    cme_logger.propagate = False
    cme_logger.addHandler(streamHandler)
    if log_to_file:
        cme_logger.addHandler(fileHandler)
    cme_logger.setLevel(level)
    return cme_logger