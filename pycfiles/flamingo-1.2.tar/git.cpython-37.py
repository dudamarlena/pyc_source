# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/git.py
# Compiled at: 2020-03-20 06:59:09
# Size of source mod 2**32: 1169 bytes
import subprocess
from shlex import split
import logging
logger = logging.getLogger('flamingo.plugins.Git')

class Git:

    def contents_parsed(self, context):
        VERSION_CMD = context.settings.get('GIT_VERSION_CMD', 'git describe').strip()
        VERSION_EXTRA_CONTEXT_NAME = context.settings.get('GIT_VERSION_EXTRA_CONTEXT_NAME', 'GIT_VERSION')
        if not VERSION_CMD.startswith('git'):
            logger.error('settings.GIT_VERSION_CMD has to start with "git"')
            return
        cmd = [
         'git', *split(VERSION_CMD)[1:]]
        try:
            version = subprocess.check_output(cmd,
              stderr=(subprocess.STDOUT),
              shell=False).decode().strip()
        except FileNotFoundError:
            logger.error('git seems not to be installed')
            return
        except subprocess.CalledProcessError as e:
            try:
                logger.error('%s returned %s: %s', VERSION_CMD, e.returncode, e.output.decode())
                return
            finally:
                e = None
                del e

        context.settings.EXTRA_CONTEXT[VERSION_EXTRA_CONTEXT_NAME] = version