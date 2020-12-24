# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/gittle/server.py
# Compiled at: 2013-09-03 02:36:01
import os
from dulwich.server import FileSystemBackend, TCPGitServer, UploadPackHandler, ReceivePackHandler
WRITE = (
 (
  'git-upload-pack', UploadPackHandler),)
READ = (('git-receive-pack', ReceivePackHandler),)
READ_HANDLERS = dict(READ)
WRITE_HANDLERS = dict(WRITE)
READ_WRITE_HANDLERS = dict(READ + WRITE)
PERM_MAPPING = {'r': READ_HANDLERS, 
   'w': WRITE_HANDLERS, 
   'rw': READ_WRITE_HANDLERS, 
   'wr': READ_WRITE_HANDLERS}

class SubFileSystemBackend(FileSystemBackend):
    """A simple FileSystemBackend restricted to a given path
    """

    def __init__(self, root_path):
        self.root_path = root_path

    def rewrite_path(self, path):
        return os.path.join(self.root_path, path)

    def open_repository(self, path):
        stripped_path = path.strip('/')
        full_path = self.rewrite_path(stripped_path)
        print 'opening %s' % path
        print 'full path = %s' % full_path
        return super(SubFileSystemBackend, self).open_repository(full_path)


class GitServer(TCPGitServer):
    """Server using the git protocol over TCP
    """

    def __init__(self, root_path=None, listen_addr=None, perm=None, *args, **kwargs):
        self.perm = perm or 'r'
        self.root_path = root_path or '/'
        self.listen_addr = listen_addr or 'localhost'
        backend = SubFileSystemBackend(self.root_path)
        handlers = PERM_MAPPING.get(self.perm, READ_HANDLERS)
        TCPGitServer.__init__(self, backend, self.listen_addr, handlers=handlers, *args, **kwargs)