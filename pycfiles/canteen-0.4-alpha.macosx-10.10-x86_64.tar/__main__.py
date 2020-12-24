# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/__main__.py
# Compiled at: 2014-09-26 04:50:19
"""

  test runner
  ~~~~~~~~~~~

  discovers canteen's tests, then runs them.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
import sys, os
if __name__ == '__main__' and 'CANTEEN_TESTING' not in os.environ:
    import nose
    sys.exit(int(nose.run()))