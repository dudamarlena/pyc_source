# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_adapters/test_inmemory.py
# Compiled at: 2014-09-30 20:17:12
__doc__ = "\n\n  inmemory adapter tests\n  ~~~~~~~~~~~~~~~~~~~~~~\n\n  tests canteen's builtin inmemory DB engine.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n      A copy of this license is included as ``LICENSE.md`` in\n      the root of the project.\n\n"
from canteen.model.adapter import inmemory
from .test_abstract import DirectedGraphAdapterTests

class InMemoryAdapterTests(DirectedGraphAdapterTests):
    """ Tests `model.adapter.inmemory` """
    __abstract__ = False
    subject = inmemory.InMemoryAdapter