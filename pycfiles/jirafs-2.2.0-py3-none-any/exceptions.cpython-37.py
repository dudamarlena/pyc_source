# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/exceptions.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 1264 bytes


class JirafsError(Exception):

    def __str__(self):
        super_str = super(JirafsError, self).__str__()
        if not super_str:
            return str(self.__class__.__name__)
        return super_str


class NotTicketFolderException(JirafsError):
    pass


class LocalCopyOutOfDate(JirafsError):
    pass


class JiraInteractionFailed(JirafsError):
    pass


class GitCommandError(JirafsError):

    def __init__(self, *args, **kwargs):
        self._command = kwargs.pop('cmd', None)
        self._returncode = kwargs.pop('returncode', None)
        self._output = kwargs.pop('stdout', None)
        (super(GitCommandError, self).__init__)(*args, **kwargs)

    @property
    def command(self):
        return self._command

    @property
    def returncode(self):
        return self._returncode

    @property
    def output(self):
        return self._output


class IssueValidationError(JirafsError):
    pass


class MacroError(JirafsError):

    @property
    def macro_name(self):
        return self._macro_name

    @macro_name.setter
    def macro_name(self, value):
        self._macro_name = value


class UnknownMacroError(MacroError):
    pass


class MacroContentError(MacroError):
    pass


class MacroAttributeError(MacroError):
    pass