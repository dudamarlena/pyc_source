# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/garicchi/projects/remote/python/pi-assistant/assistant/util/process.py
# Compiled at: 2018-01-07 13:00:15
# Size of source mod 2**32: 445 bytes
import subprocess, logging
logging.basicConfig()
logger = logging.getLogger('pi-assistant')

def call(command):
    logger.debug(command)
    p = subprocess.Popen(command, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE), shell=True)
    stdout = p.stdout.read().decode('utf-8')
    stderr = p.stderr.read().decode('utf-8')
    for o in stdout.split('\n'):
        logger.debug(o)

    for o in stderr.split('\n'):
        logger.debug(o)