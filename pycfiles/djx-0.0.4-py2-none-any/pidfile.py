# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/pidfile.py
# Compiled at: 2019-02-14 00:35:18
import errno, os, tempfile

class Pidfile(object):
    """    Manage a PID file. If a specific name is provided
    it and '"%s.oldpid" % name' will be used. Otherwise
    we create a temp file using os.mkstemp.
    """

    def __init__(self, fname):
        self.fname = fname
        self.pid = None
        return

    def create(self, pid):
        oldpid = self.validate()
        if oldpid:
            if oldpid == os.getpid():
                return
            msg = "Already running on PID %s (or pid file '%s' is stale)"
            raise RuntimeError(msg % (oldpid, self.fname))
        self.pid = pid
        fdir = os.path.dirname(self.fname)
        if fdir and not os.path.isdir(fdir):
            raise RuntimeError("%s doesn't exist. Can't create pidfile." % fdir)
        fd, fname = tempfile.mkstemp(dir=fdir)
        os.write(fd, ('%s\n' % self.pid).encode('utf-8'))
        if self.fname:
            os.rename(fname, self.fname)
        else:
            self.fname = fname
        os.close(fd)
        os.chmod(self.fname, 420)

    def rename(self, path):
        self.unlink()
        self.fname = path
        self.create(self.pid)

    def unlink(self):
        """ delete pidfile"""
        try:
            with open(self.fname, 'r') as (f):
                pid1 = int(f.read() or 0)
            if pid1 == self.pid:
                os.unlink(self.fname)
        except:
            pass

    def validate(self):
        """ Validate pidfile and make it stale if needed"""
        if not self.fname:
            return
        try:
            with open(self.fname, 'r') as (f):
                try:
                    wpid = int(f.read())
                except ValueError:
                    return

                try:
                    os.kill(wpid, 0)
                    return wpid
                except OSError as e:
                    if e.args[0] == errno.EPERM:
                        return wpid
                    if e.args[0] == errno.ESRCH:
                        return
                    raise

        except IOError as e:
            if e.args[0] == errno.ENOENT:
                return
            raise