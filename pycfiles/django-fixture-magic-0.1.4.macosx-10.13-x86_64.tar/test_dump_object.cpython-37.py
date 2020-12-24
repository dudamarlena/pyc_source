# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/tests/fixture_magic/management/commands/test_dump_object.py
# Compiled at: 2018-10-19 13:50:29
# Size of source mod 2**32: 323 bytes
from __future__ import absolute_import
__author__ = 'davedash'

def test_import():
    """Just tests that the command can be imported.

    This can be removed entirely once we legitimately test this command.
    """
    from fixture_magic.management.commands import dump_object