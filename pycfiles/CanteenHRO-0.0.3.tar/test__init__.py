# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test__init__.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  init tests\n  ~~~~~~~~~~\n\n  tests things at the top-level package init for canteen.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
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