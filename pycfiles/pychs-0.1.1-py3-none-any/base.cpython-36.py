# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/pkgcore/pychroot/build/lib/pychroot/base.py
# Compiled at: 2019-12-01 01:06:22
# Size of source mod 2**32: 5337 bytes
import errno, os
from snakeoil.contexts import SplitExec
from snakeoil.process.namespaces import simple_unshare
from .exceptions import ChrootError, ChrootMountError
from .utils import bind, getlogger, dictbool

class Chroot(SplitExec):
    """Chroot"""
    default_mounts = {'/dev':{'recursive': True}, 
     'proc:/proc':{},  'sysfs:/sys':{},  'tmpfs:/dev/shm':{},  '/etc/resolv.conf':{}}

    def __init__(self, path, log=None, mountpoints=None, hostname=None, skip_chdir=False):
        super(Chroot, self).__init__()
        self.log = getlogger(log, __name__)
        self.path = os.path.abspath(path)
        self.hostname = hostname
        self.skip_chdir = skip_chdir
        self.mountpoints = self.default_mounts.copy()
        self.mountpoints.update(mountpoints if mountpoints else {})
        if not os.path.isdir(self.path):
            raise ChrootError(f"cannot change root directory to {path!r}", errno.ENOTDIR)
        for k, source, chrmount, opts in self.mounts:
            src = source
            if source.startswith('$'):
                src = os.getenv(source[1:], source)
                if src == source:
                    if 'optional' in opts:
                        self.log.debug('Skipping optional and nonexistent mountpoint due to undefined host environment variable: %s', source)
                        del self.mountpoints[k]
                        continue
                    else:
                        raise ChrootMountError(f"cannot mount undefined environment variable: {source}")
                self.log.debug('Expanding mountpoint %r to %r', source, src)
                self.mountpoints[src] = opts
                del self.mountpoints[k]
                k = src
                if '$' in chrmount:
                    chrmount = os.path.join(self.path, src.lstrip('/'))
                if 'optional' not in opts and not os.path.exists(chrmount):
                    self.mountpoints[k]['create'] = True

    @property
    def mounts(self):
        for k, options in list(self.mountpoints.items()):
            source, _, dest = k.partition(':')
            if not dest:
                dest = source
            dest = os.path.join(self.path, dest.lstrip('/'))
            yield (k, source, dest, options)

    def _child_setup(self):
        kwargs = {}
        if os.getuid() != 0:
            kwargs.update({'user':True,  'net':True})
        simple_unshare(pid=True, hostname=self.hostname, **kwargs)
        self._mount()
        os.chroot(self.path)
        if not self.skip_chdir:
            os.chdir('/')

    def _cleanup(self):
        for _, _, chrmount, opts in self.mounts:
            if 'create' not in opts:
                pass
            else:
                self.log.debug('Removing dynamically created mountpoint: %s', chrmount)
                try:
                    if not os.path.isdir(chrmount):
                        os.remove(chrmount)
                        chrmount = os.path.dirname(chrmount)
                    os.removedirs(chrmount)
                except OSError:
                    pass
                except Exception as e:
                    raise ChrootMountError(f"failed to remove chroot mount point {chrmount!r}", getattr(e, 'errno', None))

    def _mount(self):
        """Do the bind mounts for this chroot object.

        This _must_ be run after creating a new mount namespace.
        """
        for _, source, chrmount, opts in self.mounts:
            if dictbool(opts, 'optional'):
                if not os.path.exists(source):
                    self.log.debug('Skipping optional and nonexistent mountpoint: %s', source)
                    continue
            bind(src=source, dest=chrmount, chroot=self.path, log=self.log, **opts)