# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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