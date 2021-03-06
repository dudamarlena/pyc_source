# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/util/log.py
# Compiled at: 2020-04-25 21:22:01
# Size of source mod 2**32: 3263 bytes
import logging, sys, threading
from io import StringIO

class LoggerStream(object):
    __doc__ = 'Each line of standard out/error becomes a logged line\n\n    '

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, c):
        if c == '\n':
            self.logger.log(self.log_level, self.linebuf.rstrip())
            self.linebuf = ''
        else:
            self.linebuf += c

    def flush(self):
        if len(self.linebuf) > 0:
            self.write('\n')


class LogLevelSetFilter(object):

    def __init__(self, levels):
        self.levels = levels

    def filter(self, record):
        return record.levelno in self.levels


class StreamLogDumper(threading.Thread):
    __doc__ = 'Redirect stream output to a logger in a running thread.\n\n    '

    def __init__(self, stream, logger, level):
        super(StreamLogDumper, self).__init__()
        self.stream = stream
        self.logger = logger
        self.level = level

    def run(self):
        with self.stream as (s):
            for line in iter(s.readline, b''):
                line = line.decode('utf-8')
                line = line.rstrip()
                self.logger.log(self.level, line)

    @classmethod
    def dump(clz, stdout, stderr, logger):
        StreamLogDumper(stdout, logger, logging.INFO).start()
        StreamLogDumper(stderr, logger, logging.ERROR).start()


class LogConfigurer(object):
    __doc__ = 'Configure logging to go to a file or Graylog.\n\n    '

    def __init__(self, logger=logging.getLogger(None), log_format='%(asctime)s %(levelname)s %(message)s', level=None):
        self.log_format = log_format
        self.logger = logger
        if level is not None:
            self.logger.setLevel(level)
            self.level = level

    def config_handler(self, handler):
        if self.log_format is not None:
            formatter = logging.Formatter(self.log_format)
            handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return handler

    def config_stream(self, stdout_stream, stderr_stream=None):
        out = logging.StreamHandler(stdout_stream)
        if stderr_stream is not None:
            err = logging.StreamHandler(stderr_stream)
            err.addFilter(LogLevelSetFilter({logging.ERROR}))
            out.addFilter(LogLevelSetFilter({
             logging.WARNING, logging.INFO, logging.DEBUG}))
            self.config_handler(err)
        self.config_handler(out)

    def config_buffer(self):
        log_stream = StringIO()
        self.config_stream(log_stream)
        return log_stream

    def config_file(self, file_name):
        return self.config_handler(logging.FileHandler(file_name))

    def config_basic(self):
        logging.basicConfig(format=(self.log_format), level=(self.level))

    def capture(self, stdout_logger=logging.getLogger('STDOUT'), stderr_logger=logging.getLogger('STDERR')):
        if stdout_logger is not None:
            sys.stdout = LoggerStream(stdout_logger, logging.INFO)
        if stderr_logger is not None:
            sys.stderr = LoggerStream(stderr_logger, logging.INFO)