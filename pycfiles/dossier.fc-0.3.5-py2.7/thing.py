# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/fc/tests/thing.py
# Compiled at: 2015-09-05 21:22:50
"""Serializable feature-like thing for tests.

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

"""
from __future__ import absolute_import, division, print_function
import json
from dossier.fc import StringCounter

class Thing(StringCounter):

    def __init__(self, blob=None):
        self.data = dict()
        if blob is not None:
            self.loads(blob)
        return

    def dumps(self):
        return json.dumps(self.data)

    def loads(self, blob):
        self.data = json.loads(blob)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def do_more_things(self):
        self.data['doing'] = 'something'

    def __eq__(self, other):
        return self.data == other.data

    def __repr__(self):
        return ('Thing({!r})').format(self.dumps())


class ThingSerializer(object):

    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def loads(blob):
        return Thing(blob)

    @staticmethod
    def dumps(thing):
        return thing.dumps()

    constructor = Thing