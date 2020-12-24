# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dzhiltsov/Development/vcslib/managevcs/backends/hg/workdir.py
# Compiled at: 2015-06-08 06:25:02
from managevcs.backends.base import BaseWorkdir
from managevcs.exceptions import BranchDoesNotExistError
from managevcs.utils.hgcompat import hg_merge

class MercurialWorkdir(BaseWorkdir):

    def get_branch(self):
        return self.repository._repo.dirstate.branch()

    def get_changeset(self):
        wk_dir_id = self.repository._repo[None].parents()[0].hex()
        return self.repository.get_changeset(wk_dir_id)

    def checkout_branch(self, branch=None):
        if branch is None:
            branch = self.repository.DEFAULT_BRANCH_NAME
        if branch not in self.repository.branches:
            raise BranchDoesNotExistError
        hg_merge.update(self.repository._repo, branch, False, False, None)
        return