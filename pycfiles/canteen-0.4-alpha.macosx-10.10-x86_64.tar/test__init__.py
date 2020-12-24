# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test__init__.py
# Compiled at: 2014-09-26 04:50:19
"""

  init tests
  ~~~~~~~~~~

  tests things at the top-level package init for canteen.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
import canteen
from canteen import test

class BaseFrameworkTests(test.FrameworkTest):
    """ Tests basic framework details. """

    def test_framework_all(self):
        """ Test for expected Framework-level exports """
        for attr in ('__all__', 'base', 'core', 'logic', 'model', 'rpc', 'runtime',
                     'util', 'Library', 'Logic', 'Page', 'Service', 'Model', 'Vertex',
                     'Edge', 'Key'):
            assert hasattr(canteen, attr), "failed to resolve expected framework export: '%s'." % attr