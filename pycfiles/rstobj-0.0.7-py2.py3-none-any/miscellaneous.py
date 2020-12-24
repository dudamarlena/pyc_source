# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/directives/miscellaneous.py
# Compiled at: 2019-05-24 23:11:32
"""
Other directives.
"""
import attr
from .base import Directive

@attr.s
class Include(Directive):
    """
    ``.. include::`` directive. Include an external document fragment.

    Example::

        inc = Include(path="README.rst")
        inc.render()

    Output::

        .. include:: README.rst

    Parameters definition see here http://docutils.sourceforge.net/docs/ref/rst/directives.html#including-an-external-document-fragment.
    """
    path = attr.ib(default=None)
    start_line = attr.ib(default=None)
    end_line = attr.ib(default=None)
    start_after = attr.ib(default=None)
    end_before = attr.ib(default=None)
    literal = attr.ib(default=None)
    code = attr.ib(default=None)
    number_lines = attr.ib(default=None)
    encoding = attr.ib(default=None)
    tab_width = attr.ib(default=None)
    meta_directive_keyword = 'include'
    meta_not_none_fields = ('path', )

    @property
    def arg(self):
        return self.path