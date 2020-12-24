# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/block/manifest.py
# Compiled at: 2015-11-14 16:26:10
import salve
from salve import paths
from salve.action import ActionList
from salve.context import ExecutionContext
from salve.api import Block
from .base import CoreBlock

class ManifestBlock(CoreBlock):
    """
    A manifest block describes another manifest to be expanded and
    executed. It may also specify properties of that manifest's
    execution. For example, if a manifest's blocks can be executed
    in parallel, or if its execution is conditional on a file existing.
    """

    def __init__(self, file_context, source=None):
        """
        Manifest Block constructor.

        Args:
            @file_context
            The FileContext for this block.

        KWArgs:
            @source
            The file from which this block is constructed.
        """
        ExecutionContext().transition(ExecutionContext.phases.PARSING)
        CoreBlock.__init__(self, Block.types.MANIFEST, file_context)
        self.sub_blocks = None
        if source:
            self['source'] = source
        self.path_attrs.add('source')
        self.min_attrs.add('source')
        self.primary_attr = 'source'
        return

    def expand_blocks(self, root_dir, v3_relpaths, ancestors=None):
        """
        Expands a manifest block by reading its source, parsing it into
        blocks, and assigning those to be the sub_blocks of the manifest
        block, forming a block tree. This is, in a certain sense, part
        of the parser.

        Args:
            @root_dir is the root of all relative paths in the manifest.

            @v3_relpaths
            Used to specify SALVE v3 relative path interpretation (relative to
            current manifest). When False, @root_dir is passed along from one
            manifest to the next, generally meaning that all paths are relative
            to the initial manifest.

        KWArgs:
            @ancestors is the set of containing manifests. It is passed
            through invocations in order to ensure that there are no
            manifest loops.
        """
        from salve.parser import parse_stream
        ExecutionContext()['config'].apply_to_block(self)
        self.expand_file_paths(root_dir)
        self.ensure_has_attrs('source')
        filename = self['source']
        if not ancestors:
            ancestors = set()
        if filename in ancestors:
            raise self.mk_except('Manifest ' + filename + ' includes itself')
        ancestors.add(filename)
        with open(filename) as (man):
            self.sub_blocks = parse_stream(man)
        containing_dir = root_dir
        if v3_relpaths:
            containing_dir = paths.containing_dir(filename)
        for b in self.sub_blocks:
            if isinstance(b, ManifestBlock):
                b.expand_blocks(containing_dir, v3_relpaths, ancestors=ancestors)
            else:
                ExecutionContext()['config'].apply_to_block(b)
                b.expand_file_paths(containing_dir)

    def compile(self):
        """
        Uses the ManifestBlock to produce an action.
        The action will always be an actionlist of the expansion of
        the manifest block's sub-blocks.
        """
        salve.logger.info(('{0}: Converting ManifestBlock to ActionList').format(str(self.file_context)))
        ExecutionContext().transition(ExecutionContext.phases.COMPILATION)
        if self.sub_blocks is None:
            raise self.mk_except('Attempted to convert unexpanded ' + 'manifest to action.')
        act = ActionList([], self.file_context)
        for b in self.sub_blocks:
            subact = b.compile()
            if subact is not None:
                act.append(subact)

        return act