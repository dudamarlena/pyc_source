# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cleanco/cleanco.py
# Compiled at: 2020-04-26 10:23:49
# Size of source mod 2**32: 564 bytes
from .clean import prepare_terms, basename
from .classify import typesources, countrysources, matches

class cleanco:
    """cleanco"""

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