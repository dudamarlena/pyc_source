# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/systemd.py
# Compiled at: 2019-02-14 00:35:18
import os
SD_LISTEN_FDS_START = 3

def listen_fds(unset_environment=True):
    """
    Get the number of sockets inherited from systemd socket activation.

    :param unset_environment: clear systemd environment variables unless False
    :type unset_environment: bool
    :return: the number of sockets to inherit from systemd socket activation
    :rtype: int

    Returns zero immediately if $LISTEN_PID is not set to the current pid.
    Otherwise, returns the number of systemd activation sockets specified by
    $LISTEN_FDS.

    When $LISTEN_PID matches the current pid, unsets the environment variables
    unless the ``unset_environment`` flag is ``False``.

    .. note::
        Unlike the sd_listen_fds C function, this implementation does not set
        the FD_CLOEXEC flag because the gunicorn arbiter never needs to do this.

    .. seealso::
        `<https://www.freedesktop.org/software/systemd/man/sd_listen_fds.html>`_

    """
    fds = int(os.environ.get('LISTEN_FDS', 0))
    listen_pid = int(os.environ.get('LISTEN_PID', 0))
    if listen_pid != os.getpid():
        return 0
    else:
        if unset_environment:
            os.environ.pop('LISTEN_PID', None)
            os.environ.pop('LISTEN_FDS', None)
        return fds