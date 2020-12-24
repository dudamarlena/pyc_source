# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_tool/ykinfo.py
# Compiled at: 2020-03-29 16:31:16
# Size of source mod 2**32: 1154 bytes
"""
oathldap_tool.ykinit -- sub-command for displaying Yubikey token information
"""
from usb.core import USBError
from .__about__ import __version__
from .yubikey import YubiKeySearchError, YKTokenDevice
from . import ErrorExit, cli_output

def ykinfo(command_name, args):
    """
    Shows information about connected Yubikey device.
    """
    try:
        cli_output('OATH-LDAP {0} v{1}'.format(command_name, __version__))
        yk_device = YKTokenDevice.search()
        cli_output((yk_device.info_msg()), lf_before=0, lf_after=1)
    except USBError as err:
        try:
            cli_output(str(err))
        finally:
            err = None
            del err

    except ErrorExit as err:
        try:
            cli_output(str(err))
        finally:
            err = None
            del err

    except YubiKeySearchError as err:
        try:
            cli_output(str(err))
        finally:
            err = None
            del err