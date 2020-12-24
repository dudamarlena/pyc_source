# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/fc/tests/test_registry.py
# Compiled at: 2015-09-05 21:22:50
"""dossier.fc Feature Collections

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

"""
from __future__ import absolute_import, division, print_function
import pytest
from dossier.fc.feature_collection import registry
from dossier.fc.string_counter import StringCounterSerializer

def test_unknown_feature_type_name():
    with registry:
        with pytest.raises(ValueError):
            registry.add('Unknown', StringCounterSerializer)


def test_unknown_feature_type():

    class Blah(object):
        pass

    class Serializer(object):
        constructor = Blah

    with registry:
        with pytest.raises(ValueError):
            registry.add('StringCounter', Serializer)