# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/infomap/examples/python/example-file-io.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1198 bytes
from infomap import infomap
name = 'ninetriangles'
filename = '../../{}.net'.format(name)
infomapWrapper = infomap.Infomap('-N5 --silent')
infomapWrapper.readInputData(filename)
infomapWrapper.run()
tree = infomapWrapper.tree
print('Found %d top modules with codelength: %f' % (tree.numTopModules(), tree.codelength()))
print('Writing top level modules to %s_level1.clu...' % name)
tree.writeClu('%s_level1.clu' % name, 1)
print('Writing second level modules to %s_level2.clu...' % name)
tree.writeClu('%s_level2.clu' % name, 2)
print('Writing tree to %s.tree...' % name)
tree.writeHumanReadableTree('%s.tree' % name)
print('\nModules at depth 1:\n#node module')
for node in tree.leafIter(1):
    print('%d %d' % (node.physIndex, node.moduleIndex()))

print('\nModules at depth 2:\n#node module')
for node in tree.leafIter(2):
    print('%d %d' % (node.physIndex, node.moduleIndex()))

print('\nModules at lowest level:\n#node module')
for node in tree.leafIter(-1):
    print('%d %d' % (node.physIndex, node.moduleIndex()))

print('\nModules at all levels:\n#node path')
for node in tree.treeIter():
    if node.isLeaf:
        print('%d %s' % (node.physIndex, node.path()))

print('Done!')