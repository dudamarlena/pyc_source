# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/markup/bullet_list.py
# Compiled at: 2019-05-24 23:11:32
"""
Bullet list.
"""
import attr
from ..base import RstObj

@attr.s
class BulletList(RstObj):
    """
    Bullet list class.

    Example::

        blist = BulletList(items=["a", "b", "c"])
        blist.render()

    Output::

        - a
        - b
        - c

    More example: http://docutils.sourceforge.net/docs/user/rst/quickref.html#bullet-lists
    """
    items = attr.ib()