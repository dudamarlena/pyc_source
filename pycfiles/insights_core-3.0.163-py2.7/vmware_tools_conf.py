# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/vmware_tools_conf.py
# Compiled at: 2019-05-16 13:41:33
"""
VMwareToolsConf - file ``/etc/vmware-tools/tools.conf``
=======================================================

The VMware tools configuration file ``/etc/vmware-tools/tools.conf``
is in the standard 'ini' format and is read by the IniConfigFile
parser. ``vmtoolsd.service`` provided by ``open-vm-tools`` package is
configured using ``/etc/vmware-tools/tools.conf``.

Sample ``/etc/vmware-tools/tools.conf`` file::

    [guestinfo]
    disable-query-diskinfo = true

    [logging]
    log = true

    vmtoolsd.level = debug
    vmtoolsd.handler = file
    vmtoolsd.data = /tmp/vmtoolsd.log

Examples:

    >>> list(conf.sections()) == [u'guestinfo', u'logging']
    True
    >>> conf.has_option('guestinfo', 'disable-query-diskinfo')
    True
    >>> conf.getboolean('guestinfo', 'disable-query-diskinfo')
    True
    >>> conf.get('guestinfo', 'disable-query-diskinfo') == u'true'
    True

"""
from .. import IniConfigFile, parser
from insights.specs import Specs

@parser(Specs.vmware_tools_conf)
class VMwareToolsConf(IniConfigFile):
    """Class for VMware tool configuration file content."""
    pass