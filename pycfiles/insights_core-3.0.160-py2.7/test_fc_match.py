# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_fc_match.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.fc_match import FCMatch
from insights.tests import context_wrap
FCMATCH_V1 = '\nPattern has 2 elts (size 16)\n    family: "DejaVu Sans"(s)\n    fontformat: "TrueType"(w)\n\nPattern has 2 elts (size 16)\n    family: "DejaVu Sans"(s)\n    fontformat: "TrueType"(w)\n\nPattern has 2 elts (size 16)\n    family: "DejaVu Sans"(s)\n    fontformat: "TrueType"(w)\n\nPattern has 2 elts (size 16)\n    family: "Nimbus Sans L"(s)\n    fontformat: "Type 1"(s)\n\nPattern has 2 elts (size 16)\n    family: "Standard Symbols L"(s)\n    fontformat: "Type 1"(s)\n'

def test_fcmatch_v1():
    fc_match = FCMatch(context_wrap(FCMATCH_V1))
    assert fc_match.data == [{'fontformat': '"TrueType"(w)', 'family': '"DejaVu Sans"(s)'}, {'fontformat': '"Type 1"(s)', 'family': '"Nimbus Sans L"(s)'}, {'fontformat': '"Type 1"(s)', 'family': '"Standard Symbols L"(s)'}]
    assert fc_match[0] == {'fontformat': '"TrueType"(w)', 'family': '"DejaVu Sans"(s)'}
    for item in fc_match:
        if item['family'] == '"DejaVu Sans"(s)':
            assert item['fontformat'] == '"TrueType"(w)'