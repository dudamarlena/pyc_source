# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /evtfs/home/rcarney/Dropbox/projects/dploy/master/dploy/linkcmd.py
# Compiled at: 2017-05-29 01:36:19
# Size of source mod 2**32: 2452 bytes
"""
The logic and workings behind the link sub-commands
"""
import dploy.actions as actions, dploy.utils as utils, dploy.error as error, dploy.main as main

class Link(main.AbstractBaseSubCommand):
    __doc__ = '\n    Concrete class implementation of the link sub-command\n    '

    def __init__(self, source, dest, is_silent=True, is_dry_run=False, ignore_patterns=None):
        super().__init__('link', [source], dest, is_silent, is_dry_run, ignore_patterns)

    def _is_valid_input(self, sources, dest):
        """
        Check to see if the input is valid
        """
        return LinkInput(self.errors, self.subcmd).is_valid(sources, dest)

    def _collect_actions(self, source, dest):
        """
        Concrete method to collect required actions to perform a link
        sub-command
        """
        if dest.exists():
            if utils.is_same_file(dest, source):
                self.actions.add(actions.AlreadyLinked(self.subcmd, source, dest))
            else:
                self.errors.add(error.ConflictsWithExistingFile(self.subcmd, source, dest))
        else:
            if dest.is_symlink():
                self.errors.add(error.ConflictsWithExistingLink(self.subcmd, source, dest))
            else:
                if not dest.parent.exists():
                    self.errors.add(error.NoSuchDirectoryToSubcmdInto(self.subcmd, dest.parent))
                else:
                    self.actions.add(actions.SymbolicLink(self.subcmd, source, dest))


class LinkInput(main.Input):
    __doc__ = '\n    Input validator for the link command\n    '

    def _is_valid_dest(self, dest):
        if not dest.parent.exists():
            self.errors.add(error.NoSuchFileOrDirectory(self.subcmd, dest.parent))
            return False
        if not utils.is_file_writable(dest.parent) or not utils.is_directory_writable(dest.parent):
            self.errors.add(error.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
            return False
        return True

    def _is_valid_source(self, source):
        if not source.exists():
            self.errors.add(error.NoSuchFileOrDirectory(self.subcmd, source))
            return False
        if not utils.is_file_readable(source) or not utils.is_directory_readable(source):
            self.errors.add(error.InsufficientPermissions(self.subcmd, source))
            return False
        return True