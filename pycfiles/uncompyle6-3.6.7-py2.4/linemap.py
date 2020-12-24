# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/linemap.py
# Compiled at: 2018-03-25 15:08:08
from uncompyle6.semantics.pysource import SourceWalker, code_deparse
import uncompyle6.semantics.fragments as fragments

class LineMapWalker(SourceWalker):
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        super(LineMapWalker, self).__init__(*args, **kwargs)
        self.source_linemap = {}
        self.current_line_number = 1

    def write(self, *data):
        """Augment write routine to keep track of current line"""
        for l in data:
            for i in str(l):
                if i == '\n':
                    self.current_line_number += 1

        return super(LineMapWalker, self).write(*data)

    def default(self, node):
        """Augment write default routine to record line number changes"""
        if hasattr(node, 'linestart'):
            if node.linestart:
                self.source_linemap[self.current_line_number] = node.linestart
        return super(LineMapWalker, self).default(node)

    def n_LOAD_CONST(self, node):
        if hasattr(node, 'linestart'):
            if node.linestart:
                self.source_linemap[self.current_line_number] = node.linestart
        return super(LineMapWalker, self).n_LOAD_CONST(node)


class LineMapFragmentWalker(fragments.FragmentsWalker, LineMapWalker):
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        super(LineMapFragmentWalker, self).__init__(*args, **kwargs)
        self.source_linemap = {}
        self.current_line_number = 0


def deparse_code_with_map(*args, **kwargs):
    """
    Like deparse_code but saves line number correspondences.
    Deprecated. Use code_deparse_with_map
    """
    kwargs['walker'] = LineMapWalker
    return code_deparse(*args, **kwargs)


def code_deparse_with_map(*args, **kwargs):
    """
    Like code_deparse but saves line number correspondences.
    """
    kwargs['walker'] = LineMapWalker
    return code_deparse(*args, **kwargs)


def deparse_code_with_fragments_and_map(*args, **kwargs):
    """
    Like deparse_code_with_map but saves fragments.
    Deprecated. Use code_deparse_with_fragments_and_map
    """
    kwargs['walker'] = LineMapFragmentWalker
    return fragments.deparse_code(*args, **kwargs)


def code_deparse_with_fragments_and_map(*args, **kwargs):
    """
    Like code_deparse_with_map but saves fragments.
    """
    kwargs['walker'] = LineMapFragmentWalker
    return fragments.code_deparse(*args, **kwargs)


if __name__ == '__main__':

    def deparse_test(co):
        """This is a docstring"""
        deparsed = code_deparse_with_map(co)
        a = 1
        b = 2
        print '\n'
        linemap = [ (line_no, deparsed.source_linemap[line_no]) for line_no in sorted(deparsed.source_linemap.keys()) ]
        print linemap
        deparsed = code_deparse_with_fragments_and_map(co)
        print '\n'
        linemap2 = [ (line_no, deparsed.source_linemap[line_no]) for line_no in sorted(deparsed.source_linemap.keys()) ]
        print linemap2


    deparse_test(deparse_test.__code__)