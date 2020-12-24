# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/plover_vcs.py
# Compiled at: 2020-04-03 01:04:01
# Size of source mod 2**32: 540 bytes
from plover_vcs.file_watcher import FileWatcher
from plover_vcs.message_generator.git_diff_message_generator import GitSingleFileDiffMessageGenerator
from plover_vcs.vcs.vcs_service_factory import VcsServiceFactory
from plover_vcs.vcs_config import CONFIG_MANAGER

def run():
    message_gen = GitSingleFileDiffMessageGenerator()
    vcs_service_factory = VcsServiceFactory(CONFIG_MANAGER)
    file_watcher = FileWatcher(vcs_service_factory, message_gen)
    for d in CONFIG_MANAGER.config.dictionaries:
        file_watcher.watch_file(d)