# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/garicchi/projects/remote/python/pi-assistant/assistant/util/package.py
# Compiled at: 2018-01-04 03:27:11
# Size of source mod 2**32: 672 bytes
import subprocess, logging
logger = logging.getLogger('pi-assistant')

def install(command, init):
    try:
        proc = subprocess.Popen((command.split(' ')), stderr=(subprocess.PIPE), stdout=(subprocess.PIPE))
        res = proc.communicate()
    except FileNotFoundError:
        logger.info('package %s is not found' % command)
        logger.info('install %s' % init)
        subprocess.call(init.split(' '))

    try:
        proc = subprocess.Popen((command.split(' ')), stderr=(subprocess.PIPE), stdout=(subprocess.PIPE))
        res = proc.communicate()
    except FileNotFoundError:
        logger.error('command %s could not installed by this command %s' % (command, init))