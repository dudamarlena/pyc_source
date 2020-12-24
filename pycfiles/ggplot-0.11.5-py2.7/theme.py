# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/themes/theme.py
# Compiled at: 2016-09-27 18:04:33
from __future__ import absolute_import, division, print_function, unicode_literals
from copy import deepcopy
import warnings
THEME_PARAMETERS = {b'axis_line': b'?', 
   b'axis_text': b'?', 
   b'axis_text_x': b'?', 
   b'axis_text_y': b'?', 
   b'axis_title': b'?', 
   b'axis_title_x': b'?', 
   b'axis_title_y': b'?', 
   b'axis_ticks': b'?', 
   b'axis_ticks_length': b'?', 
   b'axis_ticks_margin': b'?', 
   b'legend_background': b'?', 
   b'legend_key': b'?', 
   b'legend_key_size': b'?', 
   b'legend_key_height': b'?', 
   b'legend_key_width': b'?', 
   b'legend_margin': b'?', 
   b'legend_text': b'?', 
   b'legend_text_align': b'?', 
   b'legend_title': b'?', 
   b'legend_title_align': b'?', 
   b'legend_position': b'?', 
   b'legend_direction': b'?', 
   b'legend_justification': b'?', 
   b'legend_box': b'?', 
   b'plot_background': b'?', 
   b'plot_title': b'?', 
   b'plot_margin': b'?', 
   b'strip_background': b'?', 
   b'strip_text_x': b'?', 
   b'strip_text_y': b'?', 
   b'panel_background': b'?', 
   b'panel_border': b'?', 
   b'panel_grid_major_x': b'?', 
   b'panel_grid_minor_x': b'?', 
   b'panel_grid_major_y': b'?', 
   b'panel_grid_minor_y': b'?', 
   b'panel_margin': b'?'}

class theme_base(object):
    _rcParams = {}

    def __init__(self):
        pass

    def __radd__(self, other):
        if other.__class__.__name__ == b'ggplot':
            other.theme = self
            return other
        return self

    def get_rcParams(self):
        return self._rcParams

    def apply_final_touches(self, ax):
        pass


class theme(theme_base):
    """
    Custom theme for your plot.

    Parameters
    ----------
    title:
        title of your plot
    plot_title:
        title of your plot (same as title)
    plot_margin:
        size of plot margins
    axis_title:
        title of your plot (same as title)
    axis_title_x:
        x axis title
    axis_title_y:
        y axis title
    axis_text:
        theme for text
    axis_text_x:
        theme for x axis text
    axis_text_y:
        theme for y axis text

    Examples
    --------
    >>> ggplot(mtcars, aes(x='mpg')) + geom_histogram() + theme()
    >>> ggplot(mtcars, aes(x='mpg')) + geom_histogram() + theme(plot_margin=dict(bottom=0.2, left=0.2))
    >>> ggplot(mtcars, aes(x='mpg')) + geom_histogram() + theme(axis_text=element_text(size=20))
    >>> ggplot(mtcars, aes(x='mpg')) + geom_histogram() + theme(x_axis_text=element_text(color="orange"), y_axis_text=element_text(color="blue"))
    >>> ggplot(mtcars, aes(x='mpg')) + geom_histogram() + theme(axis_text=element_text(size=20), x_axis_text=element_text(color="orange"), y_axis_text=element_text(color="blue"))
    """
    ATTRIBUTE_MAPPING = dict(title=b'title', plot_title=b'title', axis_title=b'title', plot_margin=b'margins', axis_title_x=b'xlab', axis_title_y=b'ylab', axis_text=b'axis_text', x_axis_text=b'x_axis_text', axis_text_x=b'x_axis_text', y_axis_text=b'y_axis_text', axis_text_y=b'y_axis_text')

    def __init__(self, *args, **kwargs):
        self.things = deepcopy(kwargs)

    def __radd__(self, other):
        if other.__class__.__name__ == b'ggplot':
            other.theme = self
            for key, value in self.things.items():
                try:
                    ggplot_attr_name = self.ATTRIBUTE_MAPPING[key]
                except:
                    msg = b'%s is an invalid theme parameter' % key
                    warnings.warn(msg, RuntimeWarning)
                    continue

                setattr(other, ggplot_attr_name, value)

            return other
        return self

    def parameter_lookup(self, parameter):
        return THEME_PARAMETERS.get(parameter)