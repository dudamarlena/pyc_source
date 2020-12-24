# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Dropbox\Dropbox\projects\python\pypro\pypro\structure.py
# Compiled at: 2018-02-17 11:09:17
# Size of source mod 2**32: 2316 bytes
import os, sys, do

def make(project, flag=False):
    """
    Create de skeleton of the python project.
    """
    skeleton = {project: ['LICENSE', 'setup.py', 'README.rst'], 
     'bin': [project + '.py', '__init__.py', '..'], 
     'docs': ['index.rst', '..'], 
     'tests': ['__init__.py', '..']}

    def struct(flag=False):
        """
        Redirect the files and folders to the proper function
        """
        for folder in skeleton.keys():
            makedir(project) if folder == 'bin' else makedir(folder)
            if flag:
                for files in skeleton[folder]:
                    makefile(files, flag=True)

            else:
                for files in skeleton[folder]:
                    makefile(files)

    struct(flag=True) if flag else struct()


def makedir(directory):
    """
    Make the folders tree.
    """
    try:
        os.makedirs(directory)
        os.chdir(directory)
    except FileExistsError:
        print('Folder {} alredy exists. Aborted!'.format(directory))
        sys.exit(1)


def makefile(file, flag=False):
    """
    Make the files for the project.
    """
    if flag:
        if file == 'LICENSE':
            writefile(file, do.legal())
        else:
            writefile(file, '')
    else:
        writefile(file, '')


def writefile(file, content):
    """
    Function that write the files and go back one folder
    for the sake of the stucture
    """
    try:
        if file == '..':
            os.chdir('..')
        else:
            with open(file, 'w') as (f):
                f.write(content)
    except Exception as e:
        print('Error wrinting {}. Aborted!'.format(file))
        sys.exit(1)


if __name__ == '__main__':
    make('test', flag=True)