# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rhn_charsets.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.rhn_charsets import RHNCharSets
emb_charsets_content = '\n server_encoding\n-----------------\n UTF~\n(1 row)\n\n client_encoding\n-----------------\n UTF8\n(1 row)\n'
ora_charsets_content = '\nPARAMETER                  VALUE\n---------------------------------\nNLS_CHARACTERSET           UTF8\nNLS_NCHAR_CHARACTERSET     UTF8\n'

def test_embedded_db():
    result = RHNCharSets(context_wrap(emb_charsets_content))
    assert result.get('server_encoding') == 'UTF~'
    assert result.get('client_encoding') == 'UTF8'


def test_oracle_db():
    result = RHNCharSets(context_wrap(ora_charsets_content))
    assert result.get('NLS_CHARACTERSET') == 'UTF8'
    assert result.get('NLS_NCHAR_CHARACTERSET') == 'UTF8'