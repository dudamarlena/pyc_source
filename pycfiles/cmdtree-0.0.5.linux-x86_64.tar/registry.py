# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/side-project/lib/python2.7/site-packages/cmdtree/registry.py
# Compiled at: 2016-09-08 02:12:27


class ENV(object):
    __slots__ = ('silent_exit', 'parser', '_tree')

    def __init__(self):
        """
        :type parser: cmdtree.parser.AParser
        """
        self.silent_exit = True
        self._tree = None
        return

    def entry(self, args=None, namespace=None):
        return self.tree.root.run(args, namespace)

    @property
    def tree(self):
        """
        :rtype: cmdtree.tree.CmdTree
        """
        from cmdtree.tree import CmdTree
        if self._tree is None:
            self._tree = CmdTree()
        return self._tree

    @property
    def root(self):
        return self.tree.root


env = ENV()