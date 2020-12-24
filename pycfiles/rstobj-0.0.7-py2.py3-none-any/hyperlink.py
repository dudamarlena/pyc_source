# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/markup/hyperlink.py
# Compiled at: 2019-05-24 23:11:32
import attr
from ..base import RstObj

@attr.s
class URI(RstObj):
    """
    Example::

        uri = URI(title="Hello World", link="https://www.google.com")
        uri.render()

    Output::

        `Hello World <https://www.google.com>`_
    """
    title = attr.ib()
    link = attr.ib()


URL = URI

@attr.s
class Reference(RstObj):
    """
    Example::

        ref = Reference(title="Hello World", label="hello-world")
        ref.render()

    Output::

        :ref:`Hello World <hello-world>`
    """
    title = attr.ib()
    label = attr.ib()


Ref = Reference