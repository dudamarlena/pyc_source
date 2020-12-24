# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/rhn_schema_version.py
# Compiled at: 2019-05-16 13:41:33
"""
rhn_schema_version - Command ``/usr/bin/rhn-schema-version``
============================================================
Parse the output of command ``/usr/bin/rhn-schema-version``.

"""
from .. import parser
from insights.specs import Specs

@parser(Specs.rhn_schema_version)
def rhn_schema_version(context):
    """
    Function to parse the output of command ``/usr/bin/rhn-schema-version``.

    Sample input::

        5.6.0.10-2.el6sat

    Examples:
        >>> db_ver = shared[rhn_schema_version]
        >>> db_ver
        '5.6.0.10-2.el6sat'

    """
    if context.content:
        content = context.content
        if len(content) == 1 and 'No such' not in content[0]:
            ver = content[0].strip()
            if ver:
                return ver