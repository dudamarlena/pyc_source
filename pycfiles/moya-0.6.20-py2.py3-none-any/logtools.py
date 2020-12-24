# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/logtools.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import print_function
from __future__ import unicode_literals
from . import pilot
from .console import ConsoleHighlighter
import os, sys, io, logging, logging.handlers
runtime_log = logging.getLogger(b'moya.runtime')

class LogHighlighter(ConsoleHighlighter):
    styles = {None: b'cyan', 
       b'tag': b'yellow not bold', 
       b'debug': b'dim green', 
       b'info': b'green', 
       b'warning': b'red', 
       b'error': b'bold red', 
       b'critical': b'bold red reverse', 
       b'logdate': b'blue', 
       b'string_single': b'green', 
       b'string_double': b'green', 
       b'get': b'bold magenta', 
       b'head': b'bold cyan', 
       b'post': b'bold blue', 
       b'method': b'bold', 
       b'errorresponse': b'bold red', 
       b'responsecode': b'not dim', 
       b'path': b'bold blue', 
       b'url': b'underline'}
    highlights = [
     b'(?P<path>\\s\\/[-_\\.\\w\\/]*)',
     b'(?P<tag>\\<.*?\\>)',
     b'^(?P<logdate>\\[.*?\\])',
     b'(?P<string_single>\\".*?\\")|(?P<string_double>\\\'.*?\\\')',
     b'^\\[.*\\](?P<info>:.*?:INFO:)',
     b'^\\[.*\\](?P<debug>:.*?:DEBUG:)',
     b'^\\[.*\\](?P<warning>:.*?:WARNING:)',
     b'^\\[.*\\](?P<error>:.*?:ERROR:)',
     b'^\\[.*\\](?P<critical>:.*?:CRITICAL:)',
     b'(?P<request>\\".*?\\") (?:(?P<errorresponse>[45]\\S+)|(?P<responsecode>\\S+))',
     b'(?P<method>\\"(?:OPTIONS|DELETE|TRACE|CONNECT) .*?\\")',
     b'(?P<get>\\"GET .*?\\")',
     b'(?P<head>\\"HEAD .*?\\")',
     b'(?P<post>\\"POST .*?\\")',
     b'(?P<url>https{0,1}://[a-zA-Z0-9\\.\\%\\:\\/\\-]*)[\\s\\\'\\"$]?',
     b'(?P<parenthesis>\\(.*?\\))']


class MoyaConsoleHandler(logging.StreamHandler):
    """A handler that writes colored output to the console"""

    def emit(self, record):
        text = self.format(record)
        htext = LogHighlighter.highlight(text)
        pilot.console(htext).nl()


class MoyaFileHandler(logging.Handler):
    """
    A handler that writes to a file.

    The default FileHandler keeps the file open, which breaks when Ubuntu rotates the logs. This handler
    avoids that issue by closing the file on every emit.

    """

    def __init__(self, filename):
        self._filename = filename
        self._access_check = False
        super(MoyaFileHandler, self).__init__()

    def emit(self, record):
        text = self.format(record)
        try:
            with io.open(self._filename, b'at', encoding=b'utf-8') as (f):
                f.write(text + b'\n')
        except Exception as error:
            if not self._access_check:
                self._access_check = True
                if not os.access(self._filename, os.W_OK):
                    self._access_check = True
                    runtime_log.error(b"no permission to write to log file '%s'", self._filename)
                else:
                    runtime_log.error(b"unable to write to log file '%s' (%s)'", self._filename, error)


class MoyaSysLogHandler(logging.handlers.SysLogHandler):
    """
    A syslog handler that detects the platform

    """

    def __init__(self):
        platform = sys.platform
        if platform == b'linux2':
            args = ('/dev/log', )
        elif platform == b'darwin':
            args = ('/var/run/syslog', )
        elif platform == b'win32':
            args = ()
        else:
            args = ()
        super(MoyaSysLogHandler, self).__init__(*args)


class LoggerFile(object):
    """A file-like object that writes to a log"""

    def __init__(self, logger):
        self._logger = logger
        self._log = logging.getLogger(logger)
        self._text = []

    def __repr__(self):
        return (b"<loggerfile '{}'>").format(self._logger)

    def write(self, text):
        self._text.append(text)
        if b'\n' in text:
            lines = (b'').join(self._text).splitlines(True)
            for i, line in enumerate(lines):
                if line.endswith(b'\n'):
                    self._log.info(line[:-1])
                else:
                    self._text[:] = lines[i:]
                    break
            else:
                del self._text[:]

    def flush(self):
        pass

    def isatty(self):
        return False


class MoyaServiceFormatter(logging.Formatter):

    def format(self, record):
        log_msg = super(MoyaServiceFormatter, self).format(record)
        project = getattr(record, b'project', None)
        if project is None:
            project = pilot.service.get(b'name')
        if project is not None:
            project_prefix = (b'({})').format(project).ljust(14)
        else:
            project_prefix = b'              '
        log_msg = (b'{}{}').format(project_prefix, log_msg)
        return log_msg