# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/getenforce.py
# Compiled at: 2019-05-16 13:41:33
"""
getenforce - command ``/usr/sbin/getenforce``
=============================================

This very simple parser returns the output of the ``getenforce`` command.

Examples:

    >>> enforce = shared[getenforcevalue]
    >>> enforce['status']
    'Enforcing'
"""
from .. import parser
from insights.specs import Specs

@parser(Specs.getenforce)
def getenforcevalue(context):
    """
    The output of "getenforce" command is in one of "Enforcing", "Permissive",
    or "Disabled", so we can return the content directly.
    """
    return {'status': context.content[0]}