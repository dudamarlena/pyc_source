# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/drop_privileges.py
# Compiled at: 2007-09-08 15:14:09
import logging, os, pwd, grp

def drop_privileges(uid_name='nobody', gid_name='nogroup', umask=63, logger=None):
    """Drop privileges. POSIX only."""

    def names():
        return (
         pwd.getpwuid(os.getuid())[0],
         grp.getgrgid(os.getgid())[0])

    if logger is None:
        logger = logging.getLogger()
    logger.debug('started as %s/%s', *names())
    starting_uid = os.getuid()
    if starting_uid != 0:
        starting_uid_name = pwd.getpwuid(starting_uid)[0]
        logger.info('already running as %r', starting_uid_name)
    else:
        running_uid = pwd.getpwnam(uid_name)[2]
        running_gid = grp.getgrnam(gid_name)[2]
        try:
            os.setgid(running_gid)
        except OSError, e:
            logger.error('Could not set effective group id: %s', e)

        try:
            os.setuid(running_uid)
        except OSError, e:
            logger.error('Could not set effective user id: %s', e)

        logger.info('running as %s/%s', *names())
        old_umask = os.umask(umask)
        logger.info('umask old: %03o, new: %03o', old_umask, umask)
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    drop_privileges(logger=logging.getLogger('server'))