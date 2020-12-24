# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/knots/juicer.py
# Compiled at: 2009-10-19 11:54:54
import tables

class NodeJuicer(object):

    def __init__(self, node):
        self.node = node

    @property
    def metadata(self):
        return dict(((x, getattr(self.node)) for x in ('N', 'lastres')))

    @property
    def name(self):
        return self.node.sysname

    @property
    def classname(self):
        return (self.node.__class__.__module__, self.node.__class__.__name__)


def juice_node(node):
    juicer = NodeJuicer(node)
    return (juicer.name, juicer.classname, juicer.metadata)


class SynapsJuicer(object):

    def __init__(self, synaps):
        self.synaps = synaps

    @property
    def weights(self):
        return (self.synaps.iweight, self.synaps.oweight)

    @property
    def nodes(self):
        return tuple((NodeJuicer(x).name for x in (
         self.synaps.innode, self.synaps.outnode)))


class GlobJuicer:

    def __init__(self, glob):
        self.glob = glob

    @property
    def edges(self):
        assert self.glob.cache is not None
        return tuple((x + SynapsJuicer(s).weights for (x, s) in glob.cache.itervalues()))

    @property
    def nodes(self):
        return tuple(((x.name, x.classname) for x in (NodeJuicer(n) for n in self.glob.nodes.values())))


def juice_glob(glob):
    gj = GlobJuicer(glob)
    return (gj.nodes, gj.edges)


def classname2class((module, name)):
    return getattr(__import__(module, fromlist=[name]), name)