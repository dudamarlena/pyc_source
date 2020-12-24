# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/directives/toc.py
# Compiled at: 2019-05-24 23:11:32
"""
table of content directive.
"""
import attr
from .base import Directive

@attr.s
class TableOfContent(Directive):
    """
    ``.. contents::`` directive.

    parameter definition see here: http://docutils.sourceforge.net/docs/ref/rst/directives.html#table-of-contents

    :param title: str, required.
    :param depth: int, optional.
    :param local: bool, optional.

    :type backlinks: str
    :param backlinks: optional. one of
        :attr:`TableOfContent.BacklinksOptions`.

    Example::

        toc = TableOfContent(title="Table of Contents", depth=2)
        toc.render()

    Output::

        .. contents:: Table of Contents
            :depth: 2
    """
    title = attr.ib(default=None)
    depth = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(int)))
    local = attr.ib(default=False, validator=attr.validators.optional(attr.validators.instance_of(bool)))
    backlinks = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))
    meta_directive_keyword = 'contents'
    meta_not_none_fields = tuple()

    class BacklinksOptions(object):
        """
        ``backlinks`` argument choices.

        - ``TableOfContent.BacklinksOptions.entry``: ``"entry"``
        - ``TableOfContent.BacklinksOptions.top``: ``"top"``
        - ``TableOfContent.BacklinksOptions.none``: ``"none"``
        """
        entry = 'entry'
        top = 'top'
        none = 'none'

    @backlinks.validator
    def check_backlinks(self, attribute, value):
        if value not in (None, 'entry', 'top', 'none'):
            raise ValueError("TableOfContent.backlinks has to be one of 'entry', 'top', 'none'!")
        return

    @property
    def arg(self):
        if self.title is None:
            return ''
        else:
            return self.title
            return