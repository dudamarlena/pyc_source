# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/db2licm.py
# Compiled at: 2019-11-14 13:57:46
"""
IBM DB2 Sever details
=====================

Module for the processing of output from the ``db2licm -l`` command.
"""
from insights.core.plugins import parser
from insights.core import CommandParser
from insights.parsers import ParseException, get_active_lines
from insights.specs import Specs

@parser(Specs.db2licm_l)
class DB2Info(CommandParser, dict):
    """
    This parser processes the output of the command `db2licm_l` and provides
    the information as a dictionary.

    Sample input::

        Product name:                     "DB2 Enterprise Server Edition"
        License type:                     "CPU Option"
        Expiry date:                      "Permanent"
        Product identifier:               "db2ese"
        Version information:              "9.7"
        Enforcement policy:               "Soft Stop"
        Features:
        DB2 Performance Optimization ESE: "Not licensed"
        DB2 Storage Optimization:         "Not licensed"
        DB2 Advanced Access Control:      "Not licensed"
        IBM Homogeneous Replication ESE:  "Not licensed"

        Product name:                     "DB2 Connect Server"
        Expiry date:                      "Expired"
        Product identifier:               "db2consv"
        Version information:              "9.7"
        Concurrent connect user policy:   "Disabled"
        Enforcement policy:               "Soft Stop"

    Example:

        >>> list(parser_result.keys())
        ['DB2 Enterprise Server Edition', 'DB2 Connect Server']
        >>> parser_result['DB2 Enterprise Server Edition']["Version information"]
        '9.7'

    Override the base class parse_content to parse the output of the '''db2licm -l'''  command.
    Information that is stored in the object is made available to the rule plugins.

    Raises:
        ParseException: raised if data is not parsable.
    """

    def parse_content(self, content):
        body = {}
        for line in get_active_lines(content):
            if ':' in line:
                key, val = [ i.strip() for i in line.strip().split(':', 1) ]
                if key == 'Features':
                    continue
            else:
                raise ParseException(('Unable to parse db2licm info: {0}').format(content))
            if key == 'Product name':
                body = {}
                self[val] = body
            else:
                body[key] = val

        if not self:
            raise ParseException(('Unable to parse db2licm info: {0}').format(content))