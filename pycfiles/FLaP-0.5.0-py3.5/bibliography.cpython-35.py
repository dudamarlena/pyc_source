# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flap\substitutions\bibliography.py
# Compiled at: 2016-10-02 01:17:04
# Size of source mod 2**32: 1426 bytes
import re
from flap.substitutions.commons import LinkSubstitution

class Bibliography(LinkSubstitution):
    __doc__ = '\n    Detects "\x08ibliography". When one is detected, it produces a new fragment\n    where the link to the file is corrected.\n    '

    def __init__(self, delegate, flap):
        super().__init__(delegate, flap)

    def prepare_pattern(self):
        return re.compile('\\\\bibliography\\s*(?:\\[(?:[^\\]]+)\\])*\\{([^\\}]+)\\}')

    def find(self, fragment, reference):
        return self.flap.find_resource(fragment, reference, self.extensions_by_priority())

    def extensions_by_priority(self):
        return [
         'bib']

    def notify(self, fragment, graphic):
        return self.flap.on_include_graphics(fragment, graphic)