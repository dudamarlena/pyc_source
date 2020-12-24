# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/action/modify/file_chown.py
# Compiled at: 2015-11-06 23:45:35
from salve import logger, ugo
from salve.action.modify.chown import ChownAction
from salve.context import ExecutionContext

class FileChownAction(ChownAction):
    """
    A ChownAction applied to a single file.
    """

    def __init__(self, target, user, group, file_context):
        """
        FileChownAction constructor.

        Args:
            @target
            Path to the file to chown.
            @user
            The new user of @target.
            @group
            The new group of @target.
            @file_context
            The FileContext.
        """
        ChownAction.__init__(self, target, user, group, file_context)

    def __str__(self):
        return 'FileChownAction(target=' + str(self.target) + ',user=' + str(self.user) + ',group=' + str(self.group) + ',context=' + repr(self.file_context) + ')'

    def execute(self, filesys):
        """
        FileChownAction execution.

        Change the owner and group of a single file.
        """
        vcode = self.verify_can_exec(filesys)
        if vcode == self.verification_codes.NONEXISTENT_TARGET:
            logstr = 'FileChown: Non-Existent target file "%s"' % self.target
            logger.warn(logstr)
            return
        if vcode == self.verification_codes.NOT_ROOT:
            logstr = 'FileChown: Cannot Chown as Non-Root User'
            logger.warn(logstr)
            return
        if vcode == self.verification_codes.SKIP_EXEC:
            return
        ExecutionContext().transition(ExecutionContext.phases.EXECUTION)
        logger.info('Performing FileChown of "%s" to %s:%s' % (
         self.target, self.user, self.group))
        filesys.chown(self.target, ugo.name_to_uid(self.user), ugo.name_to_gid(self.group))