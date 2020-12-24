# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/markup/enum_list.py
# Compiled at: 2019-05-24 23:11:32
"""
Enumerate list.
"""
import attr
from ..base import RstObj

@attr.s
class EnumList(RstObj):
    """
    Enumerate list class.

    Example::

        blist = Enumerate(items=["a", "b", "c"], start_num=3)
        blist.render()

    Output::

        3. a
        4. b
        5. c

    More example: http://docutils.sourceforge.net/docs/user/rst/quickref.html#enumerated-lists
    """
    items = attr.ib()
    start_num = attr.ib(default=1)