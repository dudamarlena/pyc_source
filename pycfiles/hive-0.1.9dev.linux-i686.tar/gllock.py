# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/git/lib/python2.5/site-packages/hive/lib/glam/gllock.py
# Compiled at: 2011-07-08 01:47:53
""" Locking manager
"""
import fcntl, os
from etc import config
OP_CREATE = 'create'
OP_UPDATE = 'update'
OP_DELETE = 'delete'

class GLLock:
    """ Locking manager with sycn integrated """

    def __init__(self, filename):
        self.filename = filename
        self.locked = False
        self.lock_fd = None
        self.is_created = False
        self.op_type = None
        self.description = ''
        return

    def _get_lock_fd(self):
        """ Return the fd of the lock file """
        if not self.lock_fd or self.lock_fd.closed:
            if not os.path.exists(self.filename):
                self.is_created = True
            self.lock_fd = open(self.filename, 'a')
        return self.lock_fd

    def _sync(self):
        """ Commit and push to remote repository """
        cwd = os.getcwd()
        try:
            os.chdir(config.GITOLITE_ADMIN_REPO_PATH)
        except OSError:
            os.chdir(cwd)
            return False

        stage_cmd = ''
        if self.op_type == OP_CREATE or self.op_type == OP_UPDATE:
            stage_cmd = 'git add %s &> /dev/null' % self.filename
        elif self.op_type == OP_DELETE:
            stage_cmd = ''
        else:
            raise RuntimeError('Given op_type invalid when locking.')
        commit_cmd = 'git commit -am "%s" &> /dev/null' % self.description
        push_cmd = 'git push origin master &> /dev/null'
        if os.system(stage_cmd) == 0 and os.system(commit_cmd) == 0:
            os.chdir(cwd)
            return True
        else:
            os.chdir(cwd)
            return False

    def _fallback(self):
        """ Revert the file. """
        os.system('git diff %s > %s.diff' % (self.filename, self.filename))
        os.system('patch -R %s < %s.diff' % (self.filename, self.filename))
        os.remove('%s.diff' % self.filename)

    def lock(self, op_type, description='No description'):
        """ Lock with description """
        if self.locked:
            return True
        self.op_type = op_type
        try:
            fcntl.flock(self._get_lock_fd(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.description = description
            self.locked = True
        except IOError:
            return False

        return True

    def unlock(self, sync=True, fallback=False):
        """ Sync if needed and unlock """
        if not self.locked:
            return True
        if fallback:
            self._fallback()
        if sync:
            sync_result = self._sync()
        fcntl.flock(self._get_lock_fd(), fcntl.LOCK_UN)
        self._get_lock_fd().close()
        self.locked = False
        if self.is_created and os.path.exists(self.filename) and os.fstat(self._get_lock_fd().fileno()).st_size == 0:
            os.remove(self.filename)
        if sync:
            return sync_result
        elif fallback:
            return False
        else:
            return True