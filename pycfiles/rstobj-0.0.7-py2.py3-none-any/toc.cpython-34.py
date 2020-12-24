# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/directives/toc.py
# Compiled at: 2018-12-02 17:44:02
# Size of source mod 2**32: 1204 bytes
"""
table of content directive.
"""
import attr
from .base import Directive

@attr.s
class TableOfContent(Directive):
    __doc__ = '\n    ``.. contents::`` directive.\n    '
    title = attr.ib(default=None)
    depth = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(int)))
    local = attr.ib(default=False, validator=attr.validators.optional(attr.validators.instance_of(bool)))
    backlinks = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))
    meta_directive_keyword = 'contents'
    meta_not_none_fields = tuple()

    class BacklinksOptions(object):
        entry = 'entry'
        top = 'top'
        none = 'none'

    @backlinks.validator
    def check_backlinks(self, attribute, value):
        if value not in (None, 'entry', 'top', 'none'):
            raise ValueError("TableOfContent.backlinks has to be one of 'entry', 'top', 'none'!")

    @property
    def arg(self):
        if self.title is None:
            return ''
        else:
            return self.title