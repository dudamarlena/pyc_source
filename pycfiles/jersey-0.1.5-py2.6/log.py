# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jersey/log.py
# Compiled at: 2010-11-11 16:08:49
import sys
from twisted.python.log import *
from twisted.python.util import untilConcludes
from logging import DEBUG, INFO, WARN, ERROR
TRACE = 0

def trace(*args, **kw):
    """Log a message at the TRACE log level."""
    kw['logLevel'] = TRACE
    return msg(*args, **kw)


def debug(*args, **kw):
    """Log a message at the DEBUG log level."""
    kw['logLevel'] = DEBUG
    return msg(*args, **kw)


def info(*args, **kw):
    """Log a message at the INFO log level."""
    kw['logLevel'] = INFO
    return msg(*args, **kw)


def warn(*args, **kw):
    """Log a message at the WARN log level."""
    kw['logLevel'] = WARN
    return msg(*args, **kw)


def error(*args, **kw):
    """Log a message at the ERROR log level."""
    kw['logLevel'] = ERROR
    return msg(*args, **kw)


class CLILogObserver(object):
    defaultLogLevel = INFO
    thresholdLogLevel = WARN
    logLevels = {TRACE: 'TRACE', 
       DEBUG: 'DEBUG', 
       INFO: 'INFO', 
       WARN: 'WARN', 
       ERROR: 'ERROR'}

    def __init__(self, config, out=sys.stdout, err=sys.stderr):
        self._config = config
        level = getattr(config, 'logLevel', self.thresholdLogLevel)
        self.thresholdLogLevel = int(level)
        self._out = out
        self._err = err

    def __call__(self, event):
        return self.emit(event)

    def emit(self, event):
        """Log the event if it is sufficient."""
        self._initializeEvent(event)
        if self._isLogworthy(event):
            stream = self._getStream(event)
            text = self._formatText(event)
            text = self._streamEncodeText(stream, text)
            self._write(stream, text)

    def _initializeEvent(self, event):
        """Ensure that all necessary keys are set in the event dict."""
        if event.get('isError'):
            event.setdefault('logLevel', ERROR)
        else:
            event.setdefault('logLevel', self.defaultLogLevel)
        event.setdefault('printed', False)
        event.setdefault('program', getattr(self._config, 'program', sys.argv[0]))
        if getattr(self._config, 'subCommand'):
            event.setdefault('subCommand', self._config.subCommand)
        event['text'] = textFromEventDict(event)

    def _isLogworthy(self, event):
        """Determine whether event should be emitted.
        
        Preqrequisite:
            self._initializeEvents(event) has been called.
        """
        return bool((event.get('printed') == True or event['logLevel'] >= self.thresholdLogLevel) and event.get('text') is not None)

    def _getStream(self, event):
        """Return the output file.
        
        Preqrequisite:
            self.initializeEvents(event) has been called.
        """
        if event['logLevel'] >= ERROR:
            return self._err
        return self._out

    def _getPrefix(self, event):
        """Get an output prefix for the event.
        
        Prefix logged messages with
            progname: [command: ][loglevel: ]
        Don't molest messages printed to stdout/err.
        
        Preqrequisite:
            self.initializeEvents(event) has been called.
        """
        prefix = ''
        if not event['printed']:
            if event['logLevel'] in self.logLevels:
                level = self.logLevels[event['logLevel']].upper()
                prefix = ('{0}: ').format(level)
            if event.get('subCommand'):
                prefix = ('{0}: {1}').format(event['subCommand'], prefix)
            prefix = ('{0}: {1}').format(event['program'], prefix)
        return prefix

    def _formatText(self, event):
        """Format event['text'] for output.
        
        Preqrequisite:
            self.initializeEvents(event) has been called.
        """
        prefix = self._getPrefix(event)
        text = prefix + event['text'].replace('\n', '\n' + prefix) + '\n'
        return text

    @staticmethod
    def _streamEncodeText(stream, text):
        encoding = getattr(stream, 'encoding', None)
        if encoding:
            text = text.encode(encoding)
        return text

    @staticmethod
    def _write(stream, text):
        untilConcludes(stream.write, text)
        untilConcludes(stream.flush)