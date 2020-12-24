# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/cobbler_modules_conf.py
# Compiled at: 2019-05-16 13:41:33
"""
Cobbler modules configuration - file ``/etc/cobbler/modules.conf``
==================================================================

The Cobbler modules configuration lists a set of services, and typically
sets the module that provides that service.

Sample input::

    [authentication]
    module = authn_spacewalk

    [authorization]
    module = authz_allowall

    [dns]
    module = manage_bind

    [dhcp]
    module = manage_isc

Examples:

    >>> conf = CobblerModulesConf(context_wrap(conf_content))
    >>> conf.get('authentication', 'module')
    'authn_spacewalk'
    >>> conf.get('dhcp', 'module')
    'manage_isc'

"""
from .. import parser, IniConfigFile
from insights.specs import Specs

@parser(Specs.cobbler_modules_conf)
class CobblerModulesConf(IniConfigFile):
    """
    This uses the standard ``IniConfigFile`` parser class.
    """
    pass