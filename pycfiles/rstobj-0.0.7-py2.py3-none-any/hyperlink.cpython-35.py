# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/markup/hyperlink.py
# Compiled at: 2018-12-02 17:44:03
# Size of source mod 2**32: 358 bytes
import attr
from ..base import RstObj

@attr.s
class URI(RstObj):
    __doc__ = '\n    Example::\n\n        `title <link>`_\n    '
    title = attr.ib()
    link = attr.ib()


URL = URI

@attr.s
class Reference(RstObj):
    __doc__ = '\n    Example::\n\n        :ref:`title <label`\n    '
    title = attr.ib()
    label = attr.ib()


Ref = Reference