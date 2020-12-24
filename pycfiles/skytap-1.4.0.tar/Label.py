# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/models/Label.py
# Compiled at: 2016-12-16 14:55:45
"""Support for Skytap's Labels."""
from skytap.models.SkytapResource import SkytapResource

class Label(SkytapResource):
    """One Skytap label."""

    def __init__(self, label_json):
        """Init is mainly handled by the parent class."""
        super(Label, self).__init__(label_json)