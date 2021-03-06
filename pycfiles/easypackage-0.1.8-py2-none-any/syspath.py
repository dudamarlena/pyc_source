# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grimen/Dev/Private/python-easypackage/easypackage/syspath.py
# Compiled at: 2018-06-21 23:48:31
import sys, os
from os import path
CURRENT_PATH = path.abspath(path.dirname(__file__))
ROOT_PATH = path.abspath(path.join(CURRENT_PATH, '..'))
try:
    try:
        sys.path.remove(CURRENT_PATH)
    except:
        pass

    sys.path.index(ROOT_PATH)
except ValueError:
    sys.path.insert(0, ROOT_PATH)

from easypackage import root as easyroot
from easypackage.utils.banner import banner

def syspath(current_path=None, pattern=None):
    """
    Automatically adds current file's package root to Python load path (i.e. `sys.path`) unless already added.
    This makes it possible to always ensure module imports behave same no matter how the file is loaded.

    Examples:

        easypackage.root.root()
        easypackage.root.root(__file__)
        easypackage.root.root('./src')

    """
    project_root_path = easyroot.root(current_path, pattern)
    try:
        if project_root_path != current_path:
            try:
                sys.path.remove(current_path)
            except:
                pass

        sys.path.index(project_root_path)
        return (
         False, project_root_path)
    except ValueError as error:
        sys.path.append(project_root_path)
        return (
         True, project_root_path)


if __name__ == '__main__':
    with banner(__file__):
        search_path = None
        result = syspath(search_path)
        print ('syspath({0})\n\n  => {1}\n').format(search_path, result)
        search_path = '.'
        result = syspath(search_path)
        print ('syspath("{0}")\n\n  => {1}\n').format(search_path, result)
        search_path = path.abspath(path.normpath(sys.argv.pop() or path.dirname(__file__)))
        result = syspath(search_path)
        print ('syspath("{0}")\n\n  => {1}\n').format(search_path, result)