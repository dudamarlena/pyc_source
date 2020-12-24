# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/buildutils/test/test_publish.py
# Compiled at: 2007-08-08 19:57:13
import buildutils.command.publish as publish

def test_parseurl():
    tests = [
     (
      'scp://user@host/full/path', ('scp', 'user', None, 'host', None, '/full/path'))]
    for (url, expected) in tests:
        actual = publish.parseurl(url)
        assert actual == expected

    return