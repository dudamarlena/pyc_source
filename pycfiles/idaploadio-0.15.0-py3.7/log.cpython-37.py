# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/log.py
# Compiled at: 2020-04-13 02:37:12
# Size of source mod 2**32: 1574 bytes
import logging, socket, sys
host = socket.gethostname()

def setup_logging(loglevel, logfile):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if numeric_level is None:
        raise ValueError('Invalid log level: %s' % loglevel)
    log_format = '[%(asctime)s] {0}/%(levelname)s/%(name)s: %(message)s'.format(host)
    logging.basicConfig(level=numeric_level, filename=logfile, format=log_format)
    sys.stderr = StdErrWrapper()
    sys.stdout = StdOutWrapper()


stdout_logger = logging.getLogger('stdout')
stderr_logger = logging.getLogger('stderr')

class StdOutWrapper(object):
    __doc__ = '\n    Wrapper for stdout\n    '

    def write(self, s):
        stdout_logger.info(s.strip())

    def isatty(self):
        return False

    def flush(self, *args, **kwargs):
        """No-op for wrapper"""
        pass


class StdErrWrapper(object):
    __doc__ = '\n    Wrapper for stderr\n    '

    def write(self, s):
        stderr_logger.error(s.strip())

    def isatty(self):
        return False

    def flush(self, *args, **kwargs):
        """No-op for wrapper"""
        pass


console_logger = logging.getLogger('console_logger')
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(logging.Formatter('%(message)s'))
console_logger.addHandler(sh)
console_logger.propagate = False
requests_log = logging.getLogger('requests')
requests_log.setLevel(logging.WARNING)