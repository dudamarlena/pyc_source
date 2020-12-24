# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/sfballais123/Software Projects/Personal/Progen/progen/generators/cpp.py
# Compiled at: 2015-05-02 10:28:13
# Size of source mod 2**32: 1718 bytes
import os

def main():
    print('==============================\nProgen - C++ Project Generator v0.0.1')
    print('Copyright (C) 2015 Sean Francis N. Ballais')
    projName = input('Project Name: ')
    projChoice = input('Should we convert the directory name ({0}) to lowercase? (Y/N) '.format(projName))
    projChoice = projChoice.lower()
    if projChoice == 'y':
        projName = projName.lower()
        print('Converted the directory name to lowercase...')
    print('Using {0} as project directory...'.format(projName))
    if os.path.exists(projName):
        print('Unable to create the project folder. Folder already present.')
        projChoice = input('Use the existing folder (will delete its contents)? (Y/N) ')
        projChoice = projChoice.lower()
        if projChoice == 'n':
            print('Folder cannot be used. Exiting...')
            return
        os.removedirs(projName)
    print('\nDefault folders: [{0}, bin, build, include, src, lib]'.format(projName))
    arbitraryFolders = input('Other folders to include (separate folders using commas): ')
    folders = [
     projName,
     'bin',
     'build',
     'include',
     'src',
     'lib']
    if arbitraryFolders != '':
        folders = folders.extend(arbitraryFolders.split(','))
    for folder in folders:
        os.makedirs(folder)
        print('Created the {0} folder...'.format(folder))
        if folder == projName:
            os.chdir(folder)
            continue

    print('Finished generating the project folders of {0}...'.format(projName))