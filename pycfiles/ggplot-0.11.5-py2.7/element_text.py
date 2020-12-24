# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/themes/element_text.py
# Compiled at: 2016-09-27 18:02:25
from __future__ import absolute_import, division, print_function, unicode_literals
from matplotlib.text import Text
FACES = [
 b'plain', b'italic', b'bold', b'bold.italic']

class element_text(object):
    """
    Customize text for your plots

    Parameters
    ----------
    text:
        value of text
    family:
        font family
    face:
        ????
    color:
        color of the text
    size:
        font size
    hjust:
        horizontal adjustment from true x
    vjust:
        vertical adjustment from true y
    angle:
        rotate text
    lineheight:
        spacing between lines of text
    margin:
        margin around text

    Examples
    --------
    >>> theme(axis_text=element_text(size=20))
    >>> theme(x_axis_text=element_text(color="orange"), y_axis_text=element_text(color="blue"))
    >>> theme(axis_text=element_text(size=20), x_axis_text=element_text(color="orange"), y_axis_text=element_text(color="blue"))
    """

    def __init__(self, text=None, family=None, face=None, color=None, size=None, hjust=0, vjust=0, angle=None, lineheight=None, margin=None, debug=None):
        if text is None:
            text = b''
        self.args = [
         hjust, vjust, text]
        font = dict(family=family, weight=face, rotation=angle, color=color, linespacing=lineheight, size=size)
        font = {k:v for k, v in font.items() if v if v}
        self.kwargs = dict(horizontalalignment=b'center', fontdict=font)
        return

    def override(self, x, y, overrides={}):
        self.args[0] += x
        self.args[1] += y
        for key, value in overrides.items():
            self.kwargs[key] = value

    def apply_to_fig(self, fig):
        fig.text(*self.args, **self.kwargs)