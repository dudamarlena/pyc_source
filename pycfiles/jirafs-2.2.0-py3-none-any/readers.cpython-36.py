# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/readers.py
# Compiled at: 2019-03-11 23:04:44
# Size of source mod 2**32: 959 bytes
import io, os
from .exceptions import GitCommandError

class GitRevisionReader(object):

    def __init__(self, folder, revision):
        self.folder = folder
        self.revision = revision
        super(GitRevisionReader, self).__init__()

    def get_file_contents(self, path):
        try:
            return self.folder.get_local_file_at_revision(path,
              (self.revision),
              failure_ok=False)
        except GitCommandError:
            return ''


class WorkingCopyReader(object):

    def __init__(self, folder, path):
        self.folder = folder
        self.path = path
        super(WorkingCopyReader, self).__init__()

    def get_file_contents(self, path):
        full_path = os.path.join(self.path, path)
        with io.open((self.folder.get_local_path(full_path)),
          'r',
          encoding='utf-8') as (_in):
            return _in.read().strip()