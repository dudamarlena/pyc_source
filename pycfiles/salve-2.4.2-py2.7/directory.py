# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/block/directory.py
# Compiled at: 2015-11-06 23:45:35
import os, salve
from salve.action import ActionList, backup, copy, create, modify
from salve.api import Block
from .base import CoreBlock

class DirBlock(CoreBlock):
    """
    A directory block describes an action performed on a directory.
    This includes creation, deletion, and copying from source.
    """

    def __init__(self, file_context):
        """
        Directory Block constructor.

        Args:
            @file_context
            The FileContext for this block.
        """
        CoreBlock.__init__(self, Block.types.DIRECTORY, file_context)
        for attr in ['target', 'source']:
            self.path_attrs.add(attr)

        for attr in ['target']:
            self.min_attrs.add(attr)

        self.primary_attr = 'target'

    def _mkdir(self, dirname):
        """
        Creates a shell action to create the specified directory with
        the block's mode if set. Useful throughout dir actions, as
        handling subdirectories correctly often requires more of these.

        Args:
            @dirname
            The path to the directory to be created. Should be an
            absolute path in order to ensure correctness.
        """
        act = create.DirCreateAction(dirname, self.file_context)
        if 'mode' in self:
            act = ActionList([act], self.file_context)
            act.append(modify.DirChmodAction(dirname, self['mode'], self.file_context))
        return act

    def create_action(self):
        """
        Generate a directory creation action. This may be all or part of
        the action produced by the block upon action conversion.
        """
        self.ensure_has_attrs('target')
        if not os.path.isabs(self['target']):
            raise AssertionError
            act = self._mkdir(self['target'])
            if 'user' in self and 'group' in self:
                act = isinstance(act, ActionList) or ActionList([act], self.file_context)
            act.append(modify.DirChownAction(self['target'], self['user'], self['group'], self.file_context))
        return act

    def copy_action(self):
        """
        Copy a directory. This may be all or part of the action produced
        by the block upon action conversion.
        """
        self.ensure_has_attrs('source', 'target')
        assert os.path.isabs(self['target'])
        if not os.path.isabs(self['source']):
            raise AssertionError
            act = self._mkdir(self['target'])
            act = isinstance(act, ActionList) or ActionList([act], self.file_context)
        for d, subdirs, files in os.walk(self['source']):
            for sd in subdirs:
                target_dir = os.path.join(self['target'], os.path.relpath(os.path.join(d, sd), self['source']))
                act.append(self._mkdir(target_dir))

            for f in files:
                fname = os.path.join(d, f)
                target_dir = os.path.join(self['target'], os.path.relpath(d, self['source']))
                target_fname = os.path.join(target_dir, f)
                backup_act = backup.FileBackupAction(target_fname, self.file_context)
                copy_act = copy.FileCopyAction(fname, target_fname, self.file_context)
                file_act = ActionList([backup_act, copy_act], self.file_context)
                act.append(file_act)

        if 'mode' in self:
            act.append(modify.DirChmodAction(self['target'], self['mode'], self.file_context, recursive=True))
        if 'user' in self and 'group' in self:
            chown_dir = modify.DirChownAction(self['target'], self['user'], self['group'], self.file_context, recursive=True)
            act.append(chown_dir)
        return act

    def compile(self):
        """
        Uses the DirectoryBlock to produce an action.
        The type of action produced depends on the value of the block's
        'action' attribute.
        If it is a create action, this boils down to an invocation of
        'mkdir -p'. If it is a copy action, this is a recursive
        directory copy that creates the target directories and backs up
        any files that are being overwritten.
        """
        salve.logger.info(('{0}: Converting DirBlock to DirAction').format(str(self.file_context)))
        self.ensure_has_attrs('action')
        if self['action'] == 'create':
            dir_act = self.create_action()
        elif self['action'] == 'copy':
            dir_act = self.copy_action()
        else:
            raise self.mk_except('Unsupported DirectoryBlock action.')
        return dir_act