# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_adapters/test_inmemory.py
# Compiled at: 2014-09-30 20:17:12
"""

  inmemory adapter tests
  ~~~~~~~~~~~~~~~~~~~~~~

  tests canteen's builtin inmemory DB engine.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
      A copy of this license is included as ``LICENSE.md`` in
      the root of the project.

"""
from canteen.model.adapter import inmemory
from .test_abstract import DirectedGraphAdapterTests

class InMemoryAdapterTests(DirectedGraphAdapterTests):
    """ Tests `model.adapter.inmemory` """
    __abstract__ = False
    subject = inmemory.InMemoryAdapter