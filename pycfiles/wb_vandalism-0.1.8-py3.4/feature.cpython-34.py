# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wb_vandalism/features/feature.py
# Compiled at: 2015-10-28 15:47:46
# Size of source mod 2**32: 1061 bytes
from revscoring.features.feature import Modifier
from ..datasources import parsed_revision_text
from ..datasources.diff import changed_claims
from Levenshtein import ratio

class has_property_value(Modifier):

    def __init__(self, property, value):
        self.property = property
        self.value = value
        name = 'has_property_value({0}, {1})'.format(repr(property), repr(value))
        super().__init__(name, self._process, returns=bool, depends_on=[
         parsed_revision_text.item])

    def _process(self, item):
        values = item.claims.get(self.property, [])
        return self.value in [i.target for i in values]


class has_property_changed(Modifier):

    def __init__(self, property):
        self.property = property
        name = 'has_property_changed({0})'.format(repr(property))
        super().__init__(name, self._process, returns=bool, depends_on=[
         changed_claims])

    def _process(self, changed_claims):
        return self.property in [claims[0].id for claims in changed_claims]