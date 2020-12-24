# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/action/dynamic.py
# Compiled at: 2015-11-06 23:45:35
import abc
from salve import with_metaclass
from salve.action.base import Action
from salve.exceptions import ActionException

class DynamicAction(with_metaclass(abc.ABCMeta, Action)):
    """
    DynamicActions are actions that may not be executable at the time
    that they are instantiated. Is an ABC.
    """

    @abc.abstractmethod
    def generate(self):
        """
        Generates the action body -- can consist of a rewrite of
        self.execute(), for example -- so that when execution takes
        place, it will be valid / possible.
        """
        pass

    def execute(self, filesys):
        """
        DynamicAction.execute is not abstract because by default, the
        notion of execute on an ungenerated action is well defined.
        This needs to be overwritten during generation in most cases.

        Args:
            @filesys
            The filesystem on which the action should be executed. Used to
            transition actions between operation on the real and virtualized
            filesystem.
        """
        raise ActionException('Uninstantiated DynamicAction', self.file_context)

    def __call__(self, *args, **kwargs):
        """
        Calling a DynamicAction invokes self-generation immediately
        followed by execution. This ensures that execution takes
        place with the most up-to-date information available.
        """
        self.generate()
        Action.__call__(self, *args, **kwargs)