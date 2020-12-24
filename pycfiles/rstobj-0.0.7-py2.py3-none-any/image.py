# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/directives/image.py
# Compiled at: 2019-05-24 23:11:32
"""
image related directives.
"""
import attr
from .base import Directive

@attr.s
class Image(Directive):
    """
    ``.. image::`` directive.

    parameter definition see here: http://docutils.sourceforge.net/docs/ref/rst/directives.html#image

    :param uri: str, required.
    :param height: int, optional.
    :param width: int, optional.
    :param scale: int, optional.
    :param alt_text: str, optional.

    :type alian: str
    :param align: str, optional. one of :class:`Image.AlignOptions`.

    Example::

        img = Image(
            uri="https://www.python.org/static/img/python-logo.png",
            height=320,
            width=320,
            alt_text="Image Not Found",
            align=Image.AlignOptions.center,
        )
        img.render()

    Output::

        .. image:: https://www.python.org/static/img/python-logo.png
            :height: 320px
            :width: 320px
            :alt: Image Not Found
            :align: center
    """
    uri = attr.ib(default=None)
    height = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(int)))
    width = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(int)))
    scale = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(int)))
    alt_text = attr.ib(default=None)
    align = attr.ib(default=None)
    meta_directive_keyword = 'image'
    meta_not_none_fields = ('uri', )

    class AlignOptions(object):
        """
        ``align`` argument choices.

        - ``Image.AlignOptions.left``: ``"left"``
        - ``Image.AlignOptions.center``: ``"center"``
        - ``Image.AlignOptions.right``: ``"right"``
        - ``Image.AlignOptions.top``: ``"top"``
        - ``Image.AlignOptions.middle``: ``"middle"``
        - ``Image.AlignOptions.bottom``: ``"bottom"``
        """
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
        return

    @property
    def arg(self):
        """
        :rtype:
        """
        return self.uri