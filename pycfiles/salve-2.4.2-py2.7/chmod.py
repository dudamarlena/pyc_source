# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/action/modify/chmod.py
# Compiled at: 2015-11-06 23:45:35
import abc
from salve import logger, ugo, with_metaclass
from salve.action.modify.base import ModifyAction
from salve.context import ExecutionContext

class ChmodAction(with_metaclass(abc.ABCMeta, ModifyAction)):
    """
    The base class for ChmodActions.
    Is an ABC.
    """
    verification_codes = ModifyAction.verification_codes.extend('UNOWNED_TARGET')

    def __init__(self, target, mode, file_context):
        """
        ChmodAction constructor.

        Args:
            @target
            Path to the dir or file to modify.
            @mode
            The new umask of @target.
            @file_context
            The FileContext.
        """
        ModifyAction.__init__(self, target, file_context)
        self.mode = int(mode, 8)

    def verify_can_exec(self, filesys):
        ExecutionContext().transition(ExecutionContext.phases.VERIFICATION)
        logger.info('Chmod: Checking target exists, "%s"' % self.target)
        if not filesys.exists(self.target):
            return self.verification_codes.NONEXISTENT_TARGET
        logger.info('Chmod: Checking if user is root')
        if ugo.is_root():
            return self.verification_codes.OK
        logger.info('Chmod: Checking if user is owner of target, ' + '"%s"' % self.target)
        if not ugo.is_owner(self.target):
            return self.verification_codes.UNOWNED_TARGET
        return self.verification_codes.OK