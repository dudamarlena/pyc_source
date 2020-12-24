# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grimen/Dev/Private/python-easypackage/easypackage/root.py
# Compiled at: 2018-06-27 03:34:01
import sys, os, six
from os import path, listdir
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

import re
from easypackage.utils.banner import banner
DEFAULT_PATH = '.'
DEFAULT_ROOT_FILENAME_MATCH_PATTERN = '.git|requirements.txt'

def root(current_path=None, pattern=DEFAULT_ROOT_FILENAME_MATCH_PATTERN):
    """
    Find project root path from specified file/directory path,
    based on common project root file pattern.

    Examples:

        easypackage.root.root()
        easypackage.root.root(__file__)
        easypackage.root.root('./src')

    """
    current_path = current_path or os.getcwd()
    current_path = path.abspath(path.normpath(path.expanduser(current_path)))
    pattern = pattern or DEFAULT_ROOT_FILENAME_MATCH_PATTERN
    if not path.isdir(current_path):
        current_path = path.dirname(current_path)

    def find_root_path(current_path, pattern=None):
        if isinstance(pattern, six.string_types):
            pattern = re.compile(pattern)
        detecting = True
        while detecting:
            file_names = listdir(current_path)
            no_more_files = len(file_names) <= 0
            if no_more_files:
                detecting = False
                return None
            project_root_files = filter(pattern.match, file_names)
            project_root_files = list(project_root_files)
            found_root = len(project_root_files) > 0
            if found_root:
                detecting = False
                return current_path
            if current_path == '/':
                return None
            current_path = path.abspath(path.join(current_path, '..'))

        return result

    root_path = find_root_path(current_path, pattern)
    return root_path


if __name__ == '__main__':
    with banner(__file__):
        search_path = None
        result = root(search_path)
        print ('root({0})\n\n  => {1}\n').format(search_path, root(search_path))
        search_path = '.'
        result = root(search_path)
        print ('root("{0}")\n\n  => {1}\n').format(search_path, root(search_path))
        search_path = path.abspath(path.normpath(sys.argv.pop() or path.dirname(__file__)))
        result = root(search_path)
        print ('root("{0}")\n\n  => {1}\n').format(search_path, root(search_path))