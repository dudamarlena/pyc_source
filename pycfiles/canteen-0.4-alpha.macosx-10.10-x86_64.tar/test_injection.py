# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_core/test_injection.py
# Compiled at: 2014-09-26 04:50:19
"""

  core injection tests
  ~~~~~~~~~~~~~~~~~~~~

  tests the injection core, which is the "frontend" to the DI system.
  "compound" meta-objects, defined by the module tested by this code,
  can make use of the attribute injection pool locally via MRO.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""