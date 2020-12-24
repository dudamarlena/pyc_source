# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/dnf_modules.py
# Compiled at: 2019-05-16 13:41:33
"""
DnfModules - files under in the ``/etc/dnf/modules.d/`` directory
=================================================================

Modularity configuration
"""
from insights import IniConfigFile, parser
from insights.specs import Specs

@parser(Specs.dnf_modules)
class DnfModules(IniConfigFile):
    """
    Provides access to state of enabled modules/streams/profiles
    which is located in the /etc/dnf/modules.d/ directory

    Examples:
        >>> len(dnf_modules.sections())
        3
        >>> str(dnf_modules.get("postgresql", "stream"))
        '9.6'
        >>> str(dnf_modules.get("postgresql", "profiles"))
        'client'
    """
    pass