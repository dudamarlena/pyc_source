# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/vcs/vcs_service_factory.py
# Compiled at: 2020-04-03 01:04:01
# Size of source mod 2**32: 380 bytes
from plover_vcs.vcs.git_vcs_service import GitVcsService
from plover_vcs.vcs.vcs_service import VcsService
IMPLEMENTATIONS = {'git': GitVcsService}

class VcsServiceFactory:

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def create(self, repo: str) -> VcsService:
        return IMPLEMENTATIONS[self.config_manager.config](repo)