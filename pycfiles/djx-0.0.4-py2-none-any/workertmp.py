# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/workers/workertmp.py
# Compiled at: 2019-02-14 00:35:18
import os, platform, tempfile
from gunicorn import util
PLATFORM = platform.system()
IS_CYGWIN = PLATFORM.startswith('CYGWIN')

class WorkerTmp(object):

    def __init__(self, cfg):
        old_umask = os.umask(cfg.umask)
        fdir = cfg.worker_tmp_dir
        if fdir and not os.path.isdir(fdir):
            raise RuntimeError("%s doesn't exist. Can't create workertmp." % fdir)
        fd, name = tempfile.mkstemp(prefix='wgunicorn-', dir=fdir)
        util.chown(name, cfg.uid, cfg.gid)
        os.umask(old_umask)
        try:
            if not IS_CYGWIN:
                util.unlink(name)
            self._tmp = os.fdopen(fd, 'w+b', 1)
        except:
            os.close(fd)
            raise

        self.spinner = 0

    def notify(self):
        try:
            self.spinner = (self.spinner + 1) % 2
            os.fchmod(self._tmp.fileno(), self.spinner)
        except AttributeError:
            self._tmp.truncate(0)
            os.write(self._tmp.fileno(), 'X')

    def last_update(self):
        return os.fstat(self._tmp.fileno()).st_ctime

    def fileno(self):
        return self._tmp.fileno()

    def close(self):
        return self._tmp.close()