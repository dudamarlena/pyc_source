# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/autofs_conf.py
# Compiled at: 2019-05-16 13:41:33
"""
AutoFSConf - file ``/etc/autofs.conf``
======================================

The `/etc/autofs.conf` file is in a standard '.ini' format, and this parser
uses the IniConfigFile base class to read this.

Example:
    >>> config = shared[AutoFSConf]
    >>> config.sections()
    ['autofs', 'amd']
    >>> config.items('autofs')
    ['timeout', 'browse_mode', 'mount_nfs_default_protocol']
    >>> config.has_option('amd', 'map_type')
    True
    >>> config.get('amd', 'map_type')
    'file'
    >>> config.getint('autofs', 'timeout')
    300
    >>> config.getboolean('autofs', 'browse_mode')
    False
"""
from .. import parser, IniConfigFile
from insights.specs import Specs

@parser(Specs.autofs_conf)
class AutoFSConf(IniConfigFile):
    """
        /etc/autofs.conf is a standard INI style config file.
    """
    pass