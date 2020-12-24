# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/oracle.py
# Compiled at: 2019-05-16 13:41:33
"""
WIP: Will require tweaks as additional Oracle functionality is added.

Curently only gathers information from a database using generic init.ora file.
"""
import re
from string import whitespace
from .. import Parser, parser, get_active_lines
from insights.specs import Specs
cleanup = re.compile('(C")?[\x01\x00].*\x00')

def _parse_oracle(lines):
    """
    Performs the actual file parsing, returning a dict of the config values
    in a given Oracle DB config file.

    Despite their differences, the two filetypes are similar enough to
    allow idential parsing.
    """
    config = {}
    for line in get_active_lines(lines):
        if '\x00' in line:
            line = cleanup.sub('', line)
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip(whitespace + '"\'').lower()
            if ',' in line:
                value = [ s.strip(whitespace + '"\'').lower() for s in value.split(',') ]
            else:
                value = value.strip(whitespace + '"\'').lower()
            config[key] = value

    return config


@parser(Specs.init_ora)
class OraclePfile(Parser):
    """
    Parse Oracle database settings contained in an init.ora file.

    Returns a dict containing the name and pertinent settings of the database.

    Future iterations may have to check multiple .ora files for multiple DBs.
    """

    def parse_content(self, content):
        self.data = dict(_parse_oracle(content))


@parser(Specs.spfile_ora)
class OracleSpfile(Parser):
    """
    Parse Oracle database settings contained in an spfile.

    Returns a dict containing the name and pertinent settings of the database.
    """

    def parse_content(self, content):
        self.data = dict(_parse_oracle(content))