# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/directives/image.py
# Compiled at: 2018-12-02 17:44:03
# Size of source mod 2**32: 1296 bytes
"""
image related directives.
"""
import attr
from .base import Directive

@attr.s
class Image(Directive):
    __doc__ = '\n    ``.. image::`` directive.\n    '
    uri = attr.ib(default=None)
    height = attr.ib(default=None,
      validator=(attr.validators.optional(attr.validators.instance_of(int))))
    width = attr.ib(default=None,
      validator=(attr.validators.optional(attr.validators.instance_of(int))))
    scale = attr.ib(default=None,
      validator=(attr.validators.optional(attr.validators.instance_of(int))))
    alt_text = attr.ib(default=None)
    align = attr.ib(default=None)
    meta_directive_keyword = 'image'
    meta_not_none_fields = ('uri', )

    class AlignOptions(object):
        left = 'left'
        center = 'center'
        right = 'right'
        top = 'top'
        middle = 'middle'
        bottom = 'bottom'

    @align.validator
    def check_align(self, attribute, value):
        if value not in (None, 'left', 'center', 'right', 'top', 'middle', 'bottom'):
            raise ValueError("ListTable.align has to be one of 'left', 'center', 'right', 'top', 'middle', 'bottom'!")

    @property
    def arg(self):
        return self.uri