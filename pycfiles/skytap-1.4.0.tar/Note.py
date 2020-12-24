# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/models/Note.py
# Compiled at: 2016-12-16 14:55:45
"""Support for a single note in a Skytap environment or vm."""
from skytap.models.SkytapResource import SkytapResource

class Note(SkytapResource):
    """One note."""

    def __init__(self, note_json):
        """Create one Note."""
        super(Note, self).__init__(note_json)

    def __str__(self):
        """Represent the Note as a string."""
        return self.text