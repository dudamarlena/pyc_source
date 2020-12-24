# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/infomap/examples/python/example-multiplex.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 562 bytes
from infomap import infomap
infomapWrapper = infomap.MemInfomap('--two-level --expanded')
infomapWrapper.addMultiplexLink(2, 1, 1, 2, 1.0)
infomapWrapper.addMultiplexLink(1, 2, 2, 1, 1.0)
infomapWrapper.addMultiplexLink(3, 2, 2, 3, 1.0)
infomapWrapper.run()
tree = infomapWrapper.tree
print('Found %d modules with codelength: %f' % (tree.numTopModules(), tree.codelength()))
print('\n#layer node module:')
for node in tree.leafIter():
    print('%d %d %d' % (node.stateIndex, node.physIndex, node.moduleIndex()))