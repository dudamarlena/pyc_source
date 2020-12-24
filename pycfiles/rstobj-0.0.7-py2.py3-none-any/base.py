# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/directives/base.py
# Compiled at: 2019-05-24 23:11:32
import attr
from ..base import RstObj

@attr.s
class Directive(RstObj):
    class_ = attr.ib(default=None)
    name = attr.ib(default=None)
    meta_directive_keyword = None

    @property
    def arg(self):
        raise NotImplementedError