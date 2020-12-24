# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/vcs/git_vcs_service.py
# Compiled at: 2020-04-03 01:04:01
# Size of source mod 2**32: 537 bytes
from plover_vcs.vcs.exception_decorator import wrap_exceptions
from plover_vcs.vcs.vcs_service import VcsService
from git import Repo

@wrap_exceptions()
class GitVcsService(VcsService):

    def __init__(self, repo):
        super().__init__(repo)
        self.repo = Repo.init(repo)

    def commit(self, file: str, message: str):
        self.repo.git.pull()
        self.repo.git.add(file)
        self.repo.commit(str)
        self.repo.git.push()

    def diff(self, file: str) -> str:
        return self.repo.git.diff(file)