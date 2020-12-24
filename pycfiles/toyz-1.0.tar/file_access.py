# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/data-beta/users/fmooleka/git_projects/toyz/toyz/utils/file_access.py
# Compiled at: 2015-06-30 23:44:06
"""
Utilities to access path and file permissions for the server.
"""
from __future__ import print_function, division
import os, importlib
from collections import OrderedDict
from toyz.utils import core
from toyz.utils import db as db_utils
from toyz.utils.errors import ToyzError

def split_path(path_in):
    """
    Splits a path into a list of its folders. 
    
    For example ``/Users/penny/Documents`` would
    be returned as ``['Users', 'penny', 'Documents']``
    """
    path = core.normalize_path(path_in)
    drive, path = os.path.splitdrive(path)
    folders = []
    while True:
        path, folder = os.path.split(path)
        if folder != '':
            folders.append(folder)
        else:
            if path != '':
                folders.append(path)
            break

    folders.reverse()
    return folders


def get_all_parents(path):
    """
    Create a list with all of the parent directories of the file or path.
    
    For example ``/Users/penny/Documents`` would be returned as
    ``['/Users/penny/Documents', '/Users/penny', '/Users/']``
    """
    path = core.normalize_path(path)
    parent = os.path.dirname(path)
    last_parent = None
    parents = []
    while parent != last_parent:
        parents.append(parent)
        last_parent = parent
        parent = os.path.dirname(parent)

    return parents


def get_path_tree(path):
    """
    Get all of the sub directories of path.
    """
    path = core.normalize_path(path)
    tree = []
    for path, dirs, files in os.walk(path):
        tree.append(path)

    return tree


def get_file_permissions(db_settings, path, **user):
    """
    Get all of the permissions for a given path. Returns **None** type if no permissions have
    been set.
    
    Parameters
        - db_settings (*object* ): Database settings
        - path (*string* ): Path to check for permissions
        - user (*dict* ):  Key is either **user_id** or **group_id**, value is the *user_id* or 
          *group_id*
    
    Return
        - permissions (*string* ): Permissions for the given user for the given path.
          Returns **None** if no permissions have been set.
    """
    for user_type, user_id in user.items():
        if user_id == 'admin':
            return 'frwx'
        if 'user_id' in user:
            groups = db_utils.get_param(db_settings, 'groups', **user)
            print('groups', groups)
            if 'admin' in groups:
                return 'frwx'

    permissions = None
    path_info = db_utils.get_path_info(db_settings, path)
    if path_info is not None:
        if 'user_id' in user:
            if user['user_id'] in path_info['users']:
                permissions = path_info['users'][user['user_id']]
                print('permissions in user', permissions)
            else:
                group_permissions = ('').join([ p for g, p in path_info['groups'].items() if g in groups
                                              ])
                permissions = ('').join(set(group_permissions))
        elif user['group_id'] in path_info['groups']:
            permissions = path_info['groups'][user['group_id']]
    return permissions


def get_parent_permissions(db_settings, path, **user):
    """
    Find the permissions of the given path. If it doesn't have any permissions
    explicitely set, descend a tree and find the first parent directory with permissions set.
    If no permissions can be found, **None** is returned.
    
    Parameters
        - db_settings (*object* ): Database settings
        - path (*string* ): Path to check for permissions
        - user (*dict* ):  Key is either **user_id** or **group_id**, value is the *user_id* or 
          *group_id*
    
    Return
        - permissions (*string* ): Permissions for the given user for the given path.
          Returns **None** if no permissions have been set for any parent paths.
    """
    parents = get_all_parents(path)
    if parents[0] != path:
        parents.insert(0, path)
    for parent in parents:
        print('parent', parent)
        permissions = get_file_permissions(db_settings, parent, **user)
        print('permissions', permissions)
        if permissions != None:
            return permissions

    print(('No permissions for {0}').format(path))
    return