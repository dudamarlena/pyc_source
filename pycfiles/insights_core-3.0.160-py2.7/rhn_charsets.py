# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/rhn_charsets.py
# Compiled at: 2019-05-16 13:41:33
from .. import parser, LegacyItemAccess, CommandParser
from insights.specs import Specs

@parser(Specs.rhn_charsets)
class RHNCharSets(LegacyItemAccess, CommandParser):
    """
    ==== Sample (1) embedded database ====
     server_encoding
    -----------------
     UTF8
    (1 row)

     client_encoding
    -----------------
     UTF8
    (1 row)
    ==== Sample (2) Oracle database ====
    PARAMETER                  VALUE
    ---------------------------------
    NLS_CHARACTERSET           UTF8
    NLS_NCHAR_CHARACTERSET     UTF8
    ======================================
    Returns a dict:
    - {'server_encoding': 'UTF8','client_encoding': 'UTF8'}
    - {'NLS_CHARACTERSET': 'UTF8','NLS_NCHAR_CHARACTERSET': 'UTF8'}
    """

    def parse_content(self, content):
        db_set = {}
        db_backend = None
        in_server = False
        in_client = False
        for line in content:
            line = line.strip()
            if not line or line.startswith(('----', '(', 'PARAMETER')):
                continue
            if '_encoding' in line:
                db_backend = 'postgresql'
                in_server = line.startswith('server_')
                in_client = line.startswith('client_')
            elif db_backend == 'postgresql':
                if in_server:
                    db_set['server_encoding'] = line
                elif in_client:
                    db_set['client_encoding'] = line
            elif line.startswith('NLS_'):
                line_splits = line.split()
                if len(line_splits) == 2:
                    db_set[line_splits[0]] = line_splits[1]

        self.data = db_set
        return