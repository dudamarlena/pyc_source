# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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