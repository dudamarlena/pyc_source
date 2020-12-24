# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/scene/widgets/label.py
# Compiled at: 2016-11-03 01:40:19
from .widget import Widget
from ...visuals import TextVisual

class Label(Widget):
    """Label widget

    Parameters
    ----------
    text : str
        The label.
    rotation : float
        The rotation of the label.
    **kwargs : dict
        Keyword arguments to pass to TextVisual.
    """

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