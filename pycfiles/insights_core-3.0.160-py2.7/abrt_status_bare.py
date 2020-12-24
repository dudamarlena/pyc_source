# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/abrt_status_bare.py
# Compiled at: 2020-03-25 13:10:41
"""
AbrtStatusBare - command ``/usr/bin/abrt status --bare=True``
=============================================================

``/usr/bin/abrt status --bare=True`` returns the number of problems ABRT
detected in the system.

Examples:
    >>> abrt_status_bare.problem_count
    1997
"""
from insights import CommandParser, parser
from insights.specs import Specs

@parser(Specs.abrt_status_bare)
class AbrtStatusBare(CommandParser):
    """
    Parser for the output of ``abrt status --bare=True``

    Attributes:
        problem_count (int): the number of problems ABRT detected
    """

    def parse_content(self, content):
        self.problem_count = int(content[0].strip())