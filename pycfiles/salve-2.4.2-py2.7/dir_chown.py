# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/action/modify/dir_chown.py
# Compiled at: 2015-11-06 23:45:35
from salve import logger, paths, ugo
from salve.action.modify.chown import ChownAction
from salve.action.modify.file_chown import FileChownAction
from salve.action.modify.directory import DirModifyAction
from salve.filesys import access_codes
from salve.context import ExecutionContext

class DirChownAction(ChownAction, DirModifyAction):
    """
    A ChownAction applied to a directory.
    """

    def __init__(self, target, user, group, file_context, recursive=False):
        """
        DirChownAction constructor.

        Args:
            @target
            Path to the dir to chown.
            @user
            The new user of @target.
            @group
            The new group of @target.
            @file_context
            The FileContext.

        KWArgs:
            @recursive
            When True, applies the Chown to all subdirectories and
            contained files. When False, only applies to the root dir.
        """
        DirModifyAction.__init__(self, target, recursive, file_context)
        ChownAction.__init__(self, target, user, group, file_context)
        self.recursive = recursive

    def __str__(self):
        return 'DirChownAction(target=' + str(self.target) + ',user=' + str(self.user) + ',group=' + str(self.group) + ',recursive=' + str(self.recursive) + ',context=' + repr(self.file_context) + ')'

    def verify_can_exec(self, filesys):
        ExecutionContext().transition(ExecutionContext.phases.VERIFICATION)
        logger.info('DirChown: Checking target exists, "%s"' % self.target)
        if not filesys.access(self.target, access_codes.F_OK):
            return self.verification_codes.NONEXISTENT_TARGET
        logger.info('DirChown: Checking if execution can be skipped, ' + '"%s"' % self.target)
        if filesys.stat(self.target).st_uid == ugo.name_to_uid(self.user) and filesys.stat(self.target).st_gid == ugo.name_to_gid(self.group):
            return self.verification_codes.SKIP_EXEC
        logger.info('DirChown: Checking if user is root')
        if not ugo.is_root():
            return self.verification_codes.NOT_ROOT
        return self.verification_codes.OK

    def _execute_on_contents(self, filesys):
        """
        Recursive execution on directory contents.
        """
        for directory, subdirs, files in filesys.walk(self.target):
            for sd in subdirs:
                synth = DirChownAction(paths.pjoin(directory, sd), self.user, self.group, self.file_context)
                synth(filesys)

            for f in files:
                synth = FileChownAction(paths.pjoin(directory, f), self.user, self.group, self.file_context)
                synth(filesys)

    def execute(self, filesys):
        """
        DirChownAction execution.

        Change the owner and group of a directory or directory tree.
        """
        vcode = self.verify_can_exec(filesys)
        if vcode == self.verification_codes.NONEXISTENT_TARGET:
            logger.warn('DirChown: Non-Existent target dir "%s"' % self.target)
            return
        if vcode == self.verification_codes.NOT_ROOT:
            logger.warn('DirChown: Cannot Chown as Non-Root User')
            return
        if vcode == self.verification_codes.SKIP_EXEC:
            return
        ExecutionContext().transition(ExecutionContext.phases.EXECUTION)
        logger.info('Performing DirChown of "%s" to %s:%s' % (
         self.target, self.user, self.group))
        filesys.chown(self.target, ugo.name_to_uid(self.user), ugo.name_to_gid(self.group))
        if self.recursive:
            self._execute_on_contents(filesys)