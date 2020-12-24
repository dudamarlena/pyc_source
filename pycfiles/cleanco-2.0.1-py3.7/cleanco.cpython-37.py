# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cleanco/cleanco.py
# Compiled at: 2020-04-26 10:23:49
# Size of source mod 2**32: 564 bytes
from .clean import prepare_terms, basename
from .classify import typesources, countrysources, matches

class cleanco:
    __doc__ = 'silly backwards compatibility wrapper, you should NOT use this'

    def __init__(self, name):
        self._name = name
        self._types = typesources()
        self._countries = countrysources()
        self._terms = prepare_terms()

    def clean_name(self):
        return basename(self._name, self._terms)

    def country(self):
        return matches(self._name, self._countries)

    def type(self):
        return matches(self._name, self._types)