# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/ugo.py
# Compiled at: 2015-11-06 23:45:35
import os, grp, pwd

def get_group_from_username(username):
    """
    Gets the primary group of a user based on NIS.

    Args:
        @username
        The user whose primary group should be fetched.
    """
    return grp.getgrgid(pwd.getpwnam(username).pw_gid).gr_name


def is_root():
    """
    Checks if the process is running as root.
    """
    return os.geteuid() == 0


def name_to_uid(username):
    """
    Gets the UID for a user, based on NIS.

    Args:
        @username
        The user whose UID is desired.
    """
    return pwd.getpwnam(username).pw_uid


def name_to_gid(groupname):
    """
    Gets the GID for a group, based on NIS.

    Args:
        @groupname
        The group whose GID is desired.
    """
    return grp.getgrnam(groupname).gr_gid


def is_owner(path):
    """
    Checks if the current user owns a file.

    Args:
        @path
        Path to the file whose ownership is being checked.
    """
    assert os.path.exists(path)
    return os.stat(path).st_uid == os.geteuid()