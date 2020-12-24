# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/__main__.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = "\n\n  test runner\n  ~~~~~~~~~~~\n\n  discovers canteen's tests, then runs them.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n"
import sys, os
if __name__ == '__main__' and 'CANTEEN_TESTING' not in os.environ:
    import nose
    sys.exit(int(nose.run()))