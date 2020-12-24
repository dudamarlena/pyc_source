# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /evtfs/home/rcarney/Dropbox/projects/dploy/master/tests/utils.py
# Compiled at: 2017-05-28 22:31:31
# Size of source mod 2**32: 2277 bytes
"""
Contains utilities used during testing
"""
import os, stat, shutil

def remove_tree(tree):
    """
    reset the permission of a file and directory tree and remove it
    """
    os.chmod(tree, 511)
    shutil.rmtree(tree)


def remove_file(file_name):
    """
    reset the permission of a file and remove it
    """
    os.chmod(file_name, 511)
    os.remove(file_name)


def create_file(file_name):
    """
    create an file
    """
    return open(file_name, 'w').close()


def create_directory(directory_name):
    """
    create an directory
    """
    os.makedirs(directory_name)


class ChangeDirectory:
    __doc__ = '\n    Context manager for changing the current working directory\n    '

    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)
        self.saved_path = os.getcwd()

    def __enter__(self):
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


def create_tree(tree):
    """
    create an file and directory tree
    """
    for branch in tree:
        if isinstance(branch, str):
            create_file(branch)
        elif isinstance(branch, dict):
            for directory, file_objs in branch.items():
                create_directory(directory)
                with ChangeDirectory(directory):
                    create_tree(file_objs)


def remove_read_permission(path):
    """
    change users permissions to a path to write only
    """
    mode = os.stat(path)[stat.ST_MODE]
    os.chmod(path, mode & ~stat.S_IRUSR & ~stat.S_IRGRP & ~stat.S_IROTH)


def remove_write_permission(path):
    """
    change users permissions to a path to read only
    """
    mode = os.stat(path)[stat.ST_MODE]
    os.chmod(path, mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)


def remove_execute_permission(path):
    """
    change users permissions to a path to read only
    """
    mode = os.stat(path)[stat.ST_MODE]
    os.chmod(path, mode & ~stat.S_IXUSR & ~stat.S_IXGRP & ~stat.S_IXOTH)


def is_subcmd_error_message(subcmd, exception):
    """
    change users permissions to a path to read only
    """
    return 'dploy {subcmd}:'.format(subcmd=subcmd) in str(exception.value)