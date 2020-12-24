# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/statisk/test_Log.py
# Compiled at: 2020-01-15 09:20:16
# Size of source mod 2**32: 160 bytes
from statisk import Log

def test_title(capsys):
    Log.title()
    captured = capsys.readouterr()
    assert str(captured.out).__contains__(Log.ascii_title)