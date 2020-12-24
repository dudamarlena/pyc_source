# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/scene/widgets/label.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 1341 bytes
from .widget import Widget
from ...visuals import TextVisual

class Label(Widget):
    __doc__ = 'Label widget\n\n    Parameters\n    ----------\n    text : str\n        The label.\n    rotation : float\n        The rotation of the label.\n    **kwargs : dict\n        Keyword arguments to pass to TextVisual.\n    '

    def __init__(self, text, rotation=0.0, **kwargs):
        self._text_visual = TextVisual(text=text, rotation=rotation, **kwargs)
        self.rotation = rotation
        Widget.__init__(self)
        self.add_subvisual(self._text_visual)
        self._set_pos()

    def on_resize(self, event):
        """Resize event handler

        Parameters
        ----------
        event : instance of Event
            The event.
        """
        self._set_pos()

    def _set_pos(self):
        self._text_visual.pos = self.rect.center

    @property
    def text(self):
        return self._text_visual.text

    @text.setter
    def text(self, t):
        self._text_visual.text = t