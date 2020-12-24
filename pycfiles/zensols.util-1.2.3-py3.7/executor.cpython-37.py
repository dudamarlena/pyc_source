# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/util/executor.py
# Compiled at: 2020-05-05 20:12:43
# Size of source mod 2**32: 1277 bytes
import logging, subprocess
from zensols.util import StreamLogDumper
logger = logging.getLogger(__name__)

class Executor(object):

    def __init__(self, logger, dry_run=False, check_exit_value=0, timeout=None):
        self.logger = logger
        self.dry_run = dry_run
        self.check_exit_value = check_exit_value
        self.timeout = timeout

    def run(self, cmd, check_exit_value=None):
        check_exit_value = self.check_exit_value
        if check_exit_value is None:
            check_exit_value = self.check_exit_value
        logger.info('system <{}>'.format(cmd))
        if not self.dry_run:
            proc = subprocess.Popen(cmd, shell=True, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
            StreamLogDumper.dump(proc.stdout, proc.stderr, self.logger)
            proc.wait(self.timeout)
            ret = proc.returncode
            logger.debug('exit value: {} =? {}'.format(ret, self.check_exit_value))
            if self.check_exit_value is not None:
                if ret != check_exit_value:
                    msg = 'command returned with {}, expecting {}'.format(ret, self.check_exit_value)
                    raise OSError(msg)
            return ret