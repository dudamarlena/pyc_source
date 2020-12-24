# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/mssql_conf.py
# Compiled at: 2019-05-16 13:41:33
"""
Microsoft SQL Server Database Engine configuration - file ``/var/opt/mssql/mssql.conf``
=======================================================================================

The Microsoft SQL Server configuration file is a standard '.ini' file and uses
the ``IniConfigfile`` class to read it.

Sample configuration::

    [sqlagent]
    enabled = false

    [EULA]
    accepteula = Y

    [memory]
    memorylimitmb = 3328

Examples:

    >>> conf.has_option('memory', 'memorylimitmb')
    True
    >>> conf.get('memory', 'memorylimitmb') == '3328'
    True
"""
from insights.specs import Specs
from .. import parser, IniConfigFile

@parser(Specs.mssql_conf)
class MsSQLConf(IniConfigFile):
    """Microsoft SQL Server Database Engine configuration parser class, based on
    the ``IniConfigFile`` class.
    """
    pass