# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/common/privileges.py
# Compiled at: 2017-06-25 10:15:16
# Size of source mod 2**32: 1823 bytes
"""
Common code to handle privileges
"""
import grp, logging.handlers, os, pwd
logger = logging.getLogger(__name__)

def drop_privileges(user: pwd.struct_passwd, group: grp.struct_group, permanent: bool=True):
    """
    Drop root privileges and change to something more safe.

    :param user: The tuple with user info
    :param group: The tuple with group info
    :param permanent: Whether we want to drop just the euid (temporary), or all uids (permanent)
    """
    os.umask(63)
    if os.geteuid() == user.pw_uid and os.getegid() == group.gr_gid:
        logger.debug('Already {}/{}, not changing privileges'.format(user.pw_name, group.gr_name))
        return
    if os.geteuid() != 0:
        if os.getuid() == 0:
            restore_privileges()
    os.setgroups([])
    if permanent:
        os.setgid(group.gr_gid)
        os.setuid(user.pw_uid)
        logger.debug('Permanently dropped privileges to {}/{}'.format(user.pw_name, group.gr_name))
    else:
        os.setegid(group.gr_gid)
        os.seteuid(user.pw_uid)
        logger.debug('Dropped privileges to {}/{}'.format(user.pw_name, group.gr_name))


def restore_privileges():
    """
    Restore root privileges
    """
    if os.getuid() != 0:
        user = pwd.getpwuid(os.getuid())
        logger.warning('Root privileges have been permanently dropped, continuing as {}'.format(user.pw_name))
        return
    if os.geteuid() == 0 and os.getegid() == 0:
        return
    os.seteuid(0)
    os.setegid(0)
    logger.debug('Restored root privileges')