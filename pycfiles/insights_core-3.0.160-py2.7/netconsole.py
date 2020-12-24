# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/netconsole.py
# Compiled at: 2019-05-16 13:41:33
"""
NetConsole - file ``/etc/sysconfig/netconsole``
===============================================

This parser reads the ``/etc/sysconfig/netconsole`` file.  It uses the
``SysconfigOptions`` parser class to convert the file into a dictionary of
options.

Sample data::

    # This is the configuration file for the netconsole service.  By starting
    # this service you allow a remote syslog daemon to record console output
    # from this system.

    # The local port number that the netconsole module will use
    LOCALPORT=6666

Examples:

    >>> config = shared[NetConsole]
    >>> 'LOCALPORT' in config.data
    True
    >>> 'DEV' in config # Direct access to options
    False

"""
from insights.util import deprecated
from .. import parser, SysconfigOptions, LegacyItemAccess
from insights.specs import Specs

@parser(Specs.netconsole)
class NetConsole(SysconfigOptions, LegacyItemAccess):
    """
    .. warning::
        This parser is deprecated, please use
        :py:class:`insights.parsers.sysconfig.NetconsoleSysconfig` instead.

    Contents of the ``/etc/sysconfig/netconsole`` file.  Uses the
    ``SysconfigOptions`` shared parser class.
    """

    def __init__(self, *args, **kwargs):
        deprecated(NetConsole, 'Import NetconsoleSysconfig from insights.parsers.sysconfig instead')
        super(NetConsole, self).__init__(*args, **kwargs)