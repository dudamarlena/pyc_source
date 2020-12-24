# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/file_watcher.py
# Compiled at: 2020-04-03 01:04:01
# Size of source mod 2**32: 1334 bytes
import os
from PyQt5 import QtCore
from plover_vcs.message_generator.message_generator import MessageGenerator
from plover_vcs.vcs.vcs_service_factory import VcsServiceFactory

class FileWatcher:

    def __init__(self, vcs_factory: VcsServiceFactory, message_gen: MessageGenerator):
        """
        Creates a class that handles watching files and committing changes to them.
        :param vcs_factory: factory for creating VcsService
        :param message_gen: commit message generator
        """
        self.vcs_factory = vcs_factory
        self.message_gen = message_gen
        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.fileChanged.connect(self.file_changed)

    def watch_file(self, file: str):
        """
        Registers the given file to be watched and version controlled
        :param file: path to file
        :return: nothing
        """
        self.watcher.addPath(file)

    def file_changed(self, path: str):
        """
        Handler that commits the changes as soon as they are detected
        :param path: file to commit
        :return: nothing
        """
        vcs = self.vcs_factory.create(os.path.dirname(path))
        diff = vcs.diff(path)
        if diff:
            commit_message = self.message_gen.get_message(diff)
            vcs.commit(path, commit_message)