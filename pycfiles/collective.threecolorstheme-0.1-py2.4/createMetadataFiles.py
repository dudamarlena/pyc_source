# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\collective\threecolorstheme\skins\createMetadataFiles.py
# Compiled at: 2008-10-12 05:15:58
import os
file_types = [
 '.jpg', '.gif', '.png', '.css.dtml', '.css', '.js', '.js.dtml']
cache = 'HTTPCache'

def metadataContent(id):
    metadata = '[default]'
    metadata += '\n'
    title = ''
    if id:
        title = id.split('.')[0].replace('_', ' ')
    metadata += 'title=%s' % title
    metadata += '\n'
    metadata += 'cache=%s' % cache
    metadata += '\n'
    return metadata


def create_metadata(dir):
    filenames = os.listdir(dir)
    for filename in filenames:
        for file_type in file_types:
            if filename.endswith(file_type):
                if filename + '.metadata' in filenames:
                    pass
                else:
                    f = open(os.path.join(dir, filename) + '.metadata', 'w')
                    f.write(metadataContent(id=filename))
                    f.close()


def createMetadataInSubFolders(dir):
    create_metadata(dir)
    for (root, folders, files) in os.walk(dir, topdown=True):
        for folder in folders:
            workingFolder = os.path.join(root, folder)
            create_metadata(workingFolder)


if __name__ == '__main__':
    createMetadataInSubFolders(os.curdir)