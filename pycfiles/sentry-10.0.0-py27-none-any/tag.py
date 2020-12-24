# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/plugins/bases/tag.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.constants import MAX_TAG_VALUE_LENGTH
from sentry.plugins import Plugin2

class TagPlugin(Plugin2):
    tag = None
    project_default_enabled = True

    def get_tag_values(self, event, **kwargs):
        """
        Must return a list of values.

        >>> get_tag_pairs(event)
        [tag1, tag2, tag3]
        """
        raise NotImplementedError

    def get_tags(self, event, **kwargs):
        return [ (self.tag, v) for v in self.get_tag_values(event) if len(v) <= MAX_TAG_VALUE_LENGTH ]