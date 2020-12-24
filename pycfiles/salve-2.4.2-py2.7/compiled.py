# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/api/block/compiled.py
# Compiled at: 2015-11-06 23:45:35
import abc
from salve import with_metaclass

class CompiledBlock(with_metaclass(abc.ABCMeta)):
    """
    To define a block, you need to write a block definition in the block-def
    DSL, and you need to write a definition for the compiled block. The block
    will be produced by parsing a manifest, but the compiled block defines what
    actions are taken by means of that block.
    """

    @abc.abstractmethod
    def verify_can_exec(self):
        """
        Verifies that the compiled block can be executed.

        This attempts to verify that there are no actions specified by the
        block that will fail during execution.
        """
        pass

    @abc.abstractmethod
    def execute(self):
        """
        Executes the compiled block.

        This is the only essential characteristic of a compiled block: that
        it can be executed to produce some effect.
        """
        pass