# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /evtfs/home/rcarney/Dropbox/projects/dploy/master/dploy/actions.py
# Compiled at: 2017-03-18 02:23:04
# Size of source mod 2**32: 5976 bytes
"""
This module contains the actions that are combined to perform dploy's sub
commands
"""
from collections import defaultdict
import dploy.utils as utils

class Actions:
    __doc__ = '\n    A class that collects and executes action objects\n    '

    def __init__(self, is_silent, is_dry_run):
        self.actions = []
        self.is_silent = is_silent
        self.is_dry_run = is_dry_run

    def add(self, action):
        """
        Adds an action
        """
        self.actions.append(action)

    def execute(self):
        """
        Prints and executes actions
        """
        for action in self.actions:
            if not self.is_silent:
                print(action)
            if not self.is_dry_run:
                action.execute()

    def get_unlink_actions(self):
        """
        get the current Unlink() actions from the self.actions
        """
        return [a for a in self.actions if isinstance(a, UnLink)]

    def get_unlink_target_parents(self):
        """
        Get list of the parents for the current Unlink() actions from
        self.actions
        """
        unlink_actions = self.get_unlink_actions()
        return sorted(set([a.target.parent for a in unlink_actions]))

    def get_unlink_targets(self):
        """
        Get list of the targets for the current Unlink() actions from
        self.actions
        """
        unlink_actions = self.get_unlink_actions()
        return [a.target for a in unlink_actions]

    def get_duplicates(self):
        """
        return a tuple containing tuples with the following structure
        (link destination, [indices of duplicates])
        """
        tally = defaultdict(list)
        for index, action in enumerate(self.actions):
            if isinstance(action, SymbolicLink):
                tally[action.dest].append(index)

        return sorted([indices for _, indices in tally.items() if len(indices) > 1])


class AbstractBaseAction:
    __doc__ = '\n    An abstract base class that define the interface for actions\n    '

    def __init__(self):
        pass

    def execute(self):
        """
        function that executes the logic of each concrete action
        """
        pass


class SymbolicLink(AbstractBaseAction):
    __doc__ = '\n    Action to create a symbolic link relative to the source of the link\n    '

    def __init__(self, subcmd, source, dest):
        super().__init__()
        self.source = source
        self.source_relative = utils.get_relative_path(source, dest.parent)
        self.subcmd = subcmd
        self.dest = dest

    def execute(self):
        self.dest.symlink_to(self.source_relative)

    def __repr__(self):
        return 'dploy {subcmd}: link {dest} => {source}'.format(subcmd=self.subcmd, dest=self.dest, source=self.source_relative)


class AlreadyLinked(AbstractBaseAction):
    __doc__ = '\n    Action to used to print an already linked message\n    '

    def __init__(self, subcmd, source, dest):
        super().__init__()
        self.source = source
        self.source_relative = utils.get_relative_path(source, dest.parent)
        self.dest = dest
        self.subcmd = subcmd

    def execute(self):
        pass

    def __repr__(self):
        return 'dploy {subcmd}: already linked {dest} => {source}'.format(subcmd=self.subcmd, source=self.source_relative, dest=self.dest)


class AlreadyUnlinked(AbstractBaseAction):
    __doc__ = '\n    Action to used to print an already unlinked message\n    '

    def __init__(self, subcmd, source, dest):
        super().__init__()
        self.source = source
        self.source_relative = utils.get_relative_path(source, dest.parent)
        self.dest = dest
        self.subcmd = subcmd

    def execute(self):
        pass

    def __repr__(self):
        return 'dploy {subcmd}: already unlinked {dest} => {source}'.format(subcmd=self.subcmd, source=self.source_relative, dest=self.dest)


class UnLink(AbstractBaseAction):
    __doc__ = '\n    Action to unlink a symbolic link\n    '

    def __init__(self, subcmd, target):
        super().__init__()
        self.target = target
        self.subcmd = subcmd

    def execute(self):
        if not self.target.is_symlink():
            raise RuntimeError('dploy detected and aborted an attempt to unlink a non-symlink this is a bug and should be reported')
        self.target.unlink()

    def __repr__(self):
        source_relative = utils.get_relative_path(self.target.resolve(), self.target.parent)
        return 'dploy {subcmd}: unlink {target} => {source}'.format(subcmd=self.subcmd, target=self.target, source=source_relative)


class MakeDirectory(AbstractBaseAction):
    __doc__ = '\n    Action to create a directory\n    '

    def __init__(self, subcmd, target):
        super().__init__()
        self.target = target
        self.subcmd = subcmd

    def execute(self):
        self.target.mkdir()

    def __repr__(self):
        return 'dploy {subcmd}: make directory {target}'.format(target=self.target, subcmd=self.subcmd)


class RemoveDirectory(AbstractBaseAction):
    __doc__ = '\n    Action to remove a directory\n    '

    def __init__(self, subcmd, target):
        super().__init__()
        self.target = target
        self.subcmd = subcmd

    def execute(self):
        self.target.rmdir()

    def __repr__(self):
        msg = 'dploy {subcmd}: remove directory {target}'
        return msg.format(target=self.target, subcmd=self.subcmd)