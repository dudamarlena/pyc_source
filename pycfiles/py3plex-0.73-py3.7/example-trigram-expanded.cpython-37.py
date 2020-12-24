# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/infomap/examples/python/example-trigram-expanded.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1228 bytes
from infomap import infomap
infomapWrapper = infomap.MemInfomap('--two-level --expanded')
infomapWrapper.addTrigram(0, 2, 0)
infomapWrapper.addTrigram(0, 2, 1)
infomapWrapper.addTrigram(1, 2, 1)
infomapWrapper.addTrigram(1, 2, 0)
infomapWrapper.addTrigram(1, 2, 3)
infomapWrapper.addTrigram(3, 2, 3)
infomapWrapper.addTrigram(2, 3, 4)
infomapWrapper.addTrigram(3, 2, 4)
infomapWrapper.addTrigram(4, 2, 4)
infomapWrapper.addTrigram(4, 2, 3)
infomapWrapper.addTrigram(4, 3, 3)
infomapWrapper.run()
tree = infomapWrapper.tree
print('Found %d modules with codelength: %f' % (tree.numTopModules(), tree.codelength()))
print('\n#previousNode node module')
for node in tree.leafIter():
    print('%d %d %d' % (node.stateIndex, node.physIndex, node.moduleIndex()))