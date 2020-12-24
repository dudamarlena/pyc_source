# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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