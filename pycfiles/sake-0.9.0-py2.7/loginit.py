# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sake\loginit.py
# Compiled at: 2011-02-21 01:24:11
"""
loginit module - Initializes appropriate log functions in logging module
"""
import logging, logging.handlers, os, sys
from .const import PLATFORM_PS3
from . import logutil

def Init(redirectOutput=True, redirectLoggerToStdOut=False):
    if redirectLoggerToStdOut:
        localStdOut = sys.stdout
        if not hasattr(localStdOut, 'flush'):

            class LameStdOutFixer:

                def __init__(self, stream):
                    self.stream = stream

                def __getattr__(self, key):
                    return getattr(self.stream, key)

                def flush(self):
                    pass

            localStdOut = LameStdOutFixer(localStdOut)
        console = logging.StreamHandler(localStdOut)
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('>> %(message)s')
        console.setFormatter(formatter)
        logging.root.addHandler(console)
    if len(logging.root.handlers) == 0:
        if sys.platform == PLATFORM_PS3:
            root = '/app_home'
        else:
            root = ''
        logdir = os.path.join(root, 'logs')
        if not os.path.isdir(logdir):
            os.mkdir(logdir)
        filename = os.path.join(root, 'logs', 'ding.log')
        file = logging.handlers.TimedRotatingFileHandler(filename, when='d', backupCount=30, encoding='utf-8')
        file.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
        logging.root.addHandler(file)
        sys.stdout.write('Falling back on logging to file: %s\n' % filename)
    if redirectOutput:
        sys.stdout.write('Redirecting stdout and stderr to the logger.\n')
        sys.stdout = logutil.LogStream(logging.INFO)
        sys.stderr = logutil.LogStream(logging.ERROR)


def RestoreStdOutput():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__