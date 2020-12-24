# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/infomap/examples/python/example-bipartite.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 628 bytes
from infomap import infomap
infomapWrapper = infomap.Infomap('--two-level')
infomapWrapper.setBipartiteNodesFrom(5)
infomapWrapper.addLink(5, 0)
infomapWrapper.addLink(5, 1)
infomapWrapper.addLink(5, 2)
infomapWrapper.addLink(6, 2)
infomapWrapper.addLink(6, 3)
infomapWrapper.addLink(6, 4)
infomapWrapper.run()
tree = infomapWrapper.tree
print('Found %d modules with codelength: %f' % (tree.numTopModules(), tree.codelength()))
print('\n#node module')
for node in tree.leafIter():
    print('%d %d' % (node.physIndex, node.moduleIndex()))