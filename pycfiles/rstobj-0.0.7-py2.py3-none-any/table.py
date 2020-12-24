# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/directives/table.py
# Compiled at: 2019-05-24 23:11:32
"""
table related directives.
"""
import attr
from .base import Directive

@attr.s
class ListTable(Directive):
    """
    List Tabulate Table.

    parameter definition see here http://docutils.sourceforge.net/docs/ref/rst/directives.html#list-table.

    :param data: list of list.
    :param title: str, optional.
    :param index: bool, use first column as index. default False.
    :param header: bool, use first row as header. default True.
    :param align:

    Example::

        ltable = rstobj.directives.ListTable(
            data=[["id", "name"], [1, "Alice"], [2, "Bob"]],
            title="Users",
            header=True,
        )
        ltable.render()

    Output::

        .. list-table:: Title of the table
            :widths: 10 10 10
            :header-rows: 1

            * - Header1
              - Header2
              - Header3
            * - Value1
              - Value2
              - Value3
    """
    data = attr.ib(default=None)
    title = attr.ib(default='')
    index = attr.ib(default=False)
    header = attr.ib(default=True)
    align = attr.ib(default=None)
    meta_directive_keyword = 'list-table'
    meta_not_none_fields = ('data', )

    class AlignOptions(object):
        """
        ``align`` parameter choices.
        """
        left = 'left'
        center = 'center'
        right = 'right'

    @align.validator
    def check_align(self, attribute, value):
        if value not in (None, 'left', 'center', 'right'):
            raise ValueError("ListTable.align has to be one of 'left', 'center', 'right'!")
        return

    @property
    def arg(self):
        return self.title