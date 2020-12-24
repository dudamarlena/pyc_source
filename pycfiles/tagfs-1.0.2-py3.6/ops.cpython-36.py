# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tagfs/ops.py
# Compiled at: 2018-02-19 07:06:32
# Size of source mod 2**32: 7202 bytes
import errno, fuse, os, stat
from tagfs.selections import compile_selection
from tagfs.db import Database

class TagFS(fuse.Operations):
    OPTIONS = {'uid':int, 
     'gid':int}

    def __init__(self, db: Database):
        self._db = db
        self._options = {}

    def __call__(self, name, *args, **kwargs):
        v = getattr(self, name, None)
        if not callable(v):
            raise fuse.FuseOSError(errno.EFAULT)
        return v(*args)

    def init(self, path):
        with self._db.cursor() as (c):
            c = c.options
            for k, t in self.OPTIONS.items():
                v = c.get(k)
                if v is None:
                    v = self._corece(k, None)
                self._options[k] = t(v)

    @staticmethod
    def _corece(name, value):
        if name == 'uid':
            if value is None:
                return os.geteuid()
            return int(value)
        else:
            if name == 'gid':
                if value is None:
                    return os.getegid()
                else:
                    return int(value)
            if value is None:
                return ''
            return value

    def getxattr(self, path, name, position=0):
        if path != '/' or not name.startswith('user.'):
            return b''
        else:
            return str(self._options.get(name[5:], '')).encode()

    def listxattr(self, path):
        if path != '/':
            return []
        else:
            return ['user.' + i for i in self._options.keys()]

    def removexattr(self, path, name):
        if path != '/' or not name.startswith('user.'):
            return
        name = name[5:]
        del self._options[name]
        self._db.cursor().options.unset(name)

    def setxattr(self, path, name, value, options, position=0):
        if path != '/' or not name.startswith('user.'):
            return
        name = name[5:]
        value = self._corece(name, value)
        self._options[name] = value
        self._db.cursor().options.set(name, value)

    def _make_attr(self, mode):
        return {'st_mode':mode, 
         'st_nlink':2,  'st_uid':self._options['uid'],  'st_gid':self._options['gid']}

    def getattr(self, path, fh=None):
        if path == '/':
            return dict(st_mode=(stat.S_IFDIR | 493), st_nlink=2)
        _, *path = path.split('/')
        with self._db.cursor() as (c):
            i = c.tags.get_id(path[0])
            if i is not None:
                if len(path) == 1:
                    return self._make_attr(stat.S_IFDIR | 493)
                if len(path) == 2:
                    j = c.files.get_id(path[1])
                    if j is not None:
                        if c.files.has_tag(j, i):
                            return self._make_attr(511 | stat.S_IFLNK)
            if c.selections.exists(path[0]):
                if len(path) == 1:
                    return self._make_attr(stat.S_IFDIR | 493)
                if len(path) == 2 and c.selections.matches(path[0], path[1]):
                    return self._make_attr(511 | stat.S_IFLNK)
        raise fuse.FuseOSError(errno.ENOENT)

    def readdir(self, path, fh):
        if path == '/':
            with self._db.cursor() as (c):
                return [
                 '.', '..', '__ALL__'] + c.tags.all_names() + c.selections.all_names()
        _, *path = path.split('/')
        if len(path) == 1:
            with self._db.cursor() as (c):
                if c.tags.exists(path[0]):
                    return [
                     '.', '..'] + c.files.get_by_tag(path[0])
                if c.selections.exists(path[0]):
                    return [
                     '.', '..'] + c.selections.select(path[0])
        raise fuse.FuseOSError(errno.ENOENT)

    def mkdir(self, path, mode):
        if path == '/':
            raise fuse.FuseOSError(errno.EEXIST)
        _, *path = path.split('/')
        if len(path) != 1:
            raise fuse.FuseOSError(errno.EACCES)
        with self._db.cursor() as (c):
            if not c.tags.new(path[0]):
                raise fuse.FuseOSError(errno.EEXIST)

    def rmdir(self, path):
        if path == '/':
            raise fuse.FuseOSError(errno.EINVAL)
        else:
            _, *path = path.split('/')
            if len(path) != 1:
                raise fuse.FuseOSError(errno.ENOTDIR)
            if path[0] == '__ALL__':
                raise fuse.FuseOSError(errno.EACCES)
        with self._db.cursor() as (c):
            if not c.tags.remove(path[0]):
                raise fuse.FuseOSError(errno.ENOENT)

    def readlink(self, path):
        if path == '/':
            raise fuse.FuseOSError(errno.EINVAL)
        else:
            _, *path = path.split('/')
            if len(path) == 1:
                raise fuse.FuseOSError(errno.EINVAL)
            if len(path) != 2:
                raise fuse.FuseOSError(errno.ENOENT)
        with self._db.cursor() as (c):
            return c.files.resolve(path[1])

    def unlink(self, path):
        if path == '/':
            raise fuse.FuseOSError(errno.EISDIR)
        else:
            _, *path = path.split('/')
            if len(path) == 1:
                raise fuse.FuseOSError(errno.EISDIR)
            if len(path) != 2:
                raise fuse.FuseOSError(errno.ENOENT)
        with self._db.cursor() as (c):
            if not (c.files.remove(path[1]) if path[0] == '__ALL__' else c.files.remove_tag(path[1], path[0])):
                raise fuse.FuseOSError(errno.ENOENT)

    def symlink(self, path0, source):
        if path0 == '/':
            raise fuse.FuseOSError(errno.EEXIST)
        _, *path = path0.split('/')
        if len(path) == 1:
            with self._db.cursor() as (c):
                if c.tags.exists(path[0]):
                    raise fuse.FuseOSError(errno.EEXIST)
        if source.startswith('sel:'):
            source = compile_selection(source)
            if len(path) != 1:
                raise fuse.FuseOSError(errno.EACCES)
            with self._db.cursor() as (c):
                if not c.selections.new(path[0], source):
                    raise fuse.FuseOSError(errno.EEXIST)
        else:
            if len(path) == 1:
                raise fuse.FuseOSError(errno.EACCES)
            if len(path) != 2:
                raise fuse.FuseOSError(errno.ENOENT)
            source = os.path.normpath(os.path.join(path0, source))
            with self._db.cursor() as (c):
                if not c.files.new(path[1], source):
                    raise fuse.FuseOSError(errno.EEXIST)
                if path[0] != '__ALL__':
                    if not c.files.add_tag(path[1], path[0]):
                        raise fuse.FuseOSError(errno.EBUSY)

    def rename(self, old, new):
        if old == '/' or new == '/':
            raise fuse.FuseOSError(errno.EROFS)
        if not new.startswith('/'):
            new = os.path.normpath(os.path.join(old, new))
        _, *new = new.split('/')
        _, *old = old.split('/')
        with self._db.cursor() as (c):
            if len(new) == len(old) == 1:
                if not c.tags.rename(old[0], new[0]):
                    raise fuse.FuseOSError(errno.EROFS)
            if len(new) == len(old) == 2:
                if new[0] != old[0]:
                    if old[0] != '__ALL__':
                        c.files.remove_tag(old[1], old[0])
                    if new[0] != '__ALL__':
                        c.files.add_tag(old[1], new[0])
                if new[1] != old[1]:
                    c.files.rename(old[1], new[1])