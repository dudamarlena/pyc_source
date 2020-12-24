# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/shortfuse_test/mount.py
# Compiled at: 2019-03-06 13:38:37
# Size of source mod 2**32: 4177 bytes
import logging, os, time, xattr
from multiprocessing import Process, Event
from threading import Thread
EVENT_LOGGER = logging.getLogger('shortfuse_test.mount.event')

class FuseProcessEventManager:
    __doc__ = '\n    The fs manager interacts with the root instance Node within a mounted filesystem. It waits for a do event,\n    perform the work, clear the do event and set the done event.\n\n    This class should be created along the FUSE filesystem in the child process.\n    '

    def __init__(self, fs, do_event, done_event):
        self._fs = fs
        self._do_event = do_event
        self._done_event = done_event
        self._thread = Thread(target=(self._run))

    def start(self):
        self._thread.start()

    def _run(self):
        while True:
            self._do_event.wait()
            self._execute()
            EVENT_LOGGER.debug('Processed an event')
            self._do_event.clear()
            self._done_event.set()

    def _execute(self):
        pass


class FuseEventManager:

    def __init__(self):
        self.do_event = Event()
        self.done_event = Event()

    def signal(self):
        self.do_event.set()
        self.done_event.wait()
        self.done_event.clear()


class FuseOS:

    def _callback(self):
        pass

    def _execute_op(self, callback):
        try:
            self._callback()
            result = callback()
            return result
        except Exception as e:
            try:
                self._callback()
                raise e
            finally:
                e = None
                del e

    def chmod(self, path, mode):
        if hasattr(os, 'lchmod'):
            return self._execute_op(lambda : os.lchmod(path, mode))
        return self._execute_op(lambda : os.chmod(path, mode))

    def chown(self, path, uid, gid):
        if hasattr(os, 'lchown'):
            return self._execute_op(lambda : os.lchown(path, uid, gid))
        return self._execute_op(lambda : os.chown(path, uid, gid))

    def delete_xattr(self, path, key):

        def _execute():
            attrs = xattr.xattr(path)
            del attrs[key]

        return self._execute_op(lambda : _execute())

    def get_xattr(self, path, key):
        return self._execute_op(lambda : dict(xattr.xattr(path)).get(key, None))

    def get_xattrs(self, path):
        return self._execute_op(lambda : dict(xattr.xattr(path)))

    def listdir(self, path):
        return self._execute_op(lambda : os.listdir(path))

    def mkdir(self, path, mode):
        return self._execute_op(lambda : os.mkdir(path, mode))

    def open(self, path, mode):
        return self._execute_op(lambda : open(path, mode))

    def readlink(self, path):
        return self._execute_op(lambda : os.readlink(path))

    def rmdir(self, path):
        return self._execute_op(lambda : os.rmdir(path))

    def set_xattr(self, path, key, value):

        def _execute():
            attrs = xattr.xattr(path)
            attrs[key] = value

        return self._execute_op(lambda : _execute())

    def stat(self, path):
        if hasattr(os, 'lstat'):
            return self._execute_op(lambda : os.lstat(path))
        return self._execute_op(lambda : os.stat(path))

    def symlink(self, source, link_name):
        return self._execute_op(lambda : os.symlink(source, link_name))

    def utime(self, path, times):
        return self._execute_op(lambda : os.utime(path, times))

    def unlink(self, path):
        return self._execute_op(lambda : os.unlink(path))


class FuseManager:

    def __init__(self, entry, mount_path, *args):
        self._fuse_process = Process(target=entry,
          args=([
         mount_path] + list(args)))
        self.mount_path = mount_path

    def start(self):
        self._fuse_process.start()
        time.sleep(1)

    def stop(self):
        self._fuse_process.terminate()
        self._fuse_process.join()