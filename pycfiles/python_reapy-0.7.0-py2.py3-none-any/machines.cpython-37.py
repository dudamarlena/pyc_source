# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\tools\network\machines.py
# Compiled at: 2020-03-18 12:13:39
# Size of source mod 2**32: 3961 bytes
import importlib, sys, warnings, reapy, reapy.config
from reapy import errors
from . import client, web_interface
CLIENT = None
CLIENTS = {None: None}

def get_selected_client():
    global CLIENT
    return CLIENT


def get_selected_machine_host():
    """Return host of the currently selected machine.

    Returns
    -------
    host : str or None
        None is returned when running from inside REAPER and
        no slave machine is selected.
    """
    if CLIENT is None:
        return
    return CLIENT.host


def reconnect():
    r"""
    Reconnect to REAPER ReaScript API.

    Examples
    --------
    Assume no REAPER instance is active.
    >>> import reapy
    errors.DisabledDistAPIWarning: Can't reach distant API. Please start REAPER, or
    call reapy.config.enable_dist_api() from inside REAPER to enable distant
    API.
      warnings.warn(errors.DisabledDistAPIWarning())
    >>> p = reapy.Project()  # Results in error
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "reapy\core\project\project.py", line 26, in __init__
        id = RPR.EnumProjects(index, None, 0)[0]
    AttributeError: module 'reapy.reascript_api' has no attribute 'EnumProjects'
    >>> # Now start REAPER
    ...
    >>> reapy.reconnect()
    >>> p = reapy.Project()  # No error!
    """
    if not reapy.is_inside_reaper():
        host = get_selected_machine_host()
        if host is None:
            host = 'localhost'
        try:
            del CLIENTS[host]
        except KeyError:
            pass

        connect(host)


class connect:
    __doc__ = 'Connect to slave machine.\n\n    reapy instructions will now be run on the selected machine.\n    If used as a context manager, the slave machine will only be\n    selected in the corresponding context.\n\n    Parameters\n    ----------\n    host : str, optional\n        Slave machine host. If None, selects default ``reapy``\n        behavior (i.e. local REAPER instance).\n\n    See also\n    --------\n    ``connect_to_default_machine``\n        Connect to default slave machine (i.e. local REAPER instance).\n    '

    def __init__(self, host=None):
        global CLIENT
        self.previous_client = CLIENT
        try:
            if host not in CLIENTS:
                register_machine(host)
            CLIENT = CLIENTS[host]
            if hasattr(reapy, 'reascript_api'):
                importlib.reload(reapy.reascript_api)
        except errors.DisabledDistAPIError as e:
            try:
                if host:
                    if host != 'localhost':
                        raise e
                warnings.warn(errors.DisabledDistAPIWarning())
            finally:
                e = None
                del e

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        global CLIENT
        CLIENT = self.previous_client
        importlib.reload(reapy.reascript_api)


class connect_to_default_machine(connect):
    __doc__ = 'Select default slave machine (i.e. local REAPER instance).'

    def __init__(self):
        super().__init__()


def register_machine(host):
    """Register a slave machine.

    Parameters
    ----------
    host : str
        Slave machine host (e.g. ``"localhost"``).

    See also
    --------
    ``reapy.connect``
    """
    if reapy.is_inside_reaper():
        if host == 'localhost':
            msg = 'A REAPER instance can not connect to istelf.'
            raise errors.InsideREAPERError(msg)
    interface_port = reapy.config.WEB_INTERFACE_PORT
    interface = web_interface.WebInterface(interface_port, host)
    CLIENTS[host] = client.Client(interface.get_reapy_server_port(), host)


if not reapy.is_inside_reaper():
    connect('localhost')
    CLIENTS[None] = CLIENT