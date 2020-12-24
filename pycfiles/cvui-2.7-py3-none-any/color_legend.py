# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/color_legend.py
# Compiled at: 2014-05-19 10:05:09
from traits.api import HasTraits, Str, List, RGBColor, Any
from traitsui.api import View, Item, TableEditor, TextEditor, ObjectColumn

class ColorColumn(ObjectColumn):

    def get_cell_color(self, object):
        return tuple(map(lambda c: int(round(c * 255)), object.col))


class LegendEntry(HasTraits):
    metaregion = Str
    col = Any
    blank = Str('')

    def __init__(self, **traits):
        super(LegendEntry, self).__init__(**traits)


class ColorLegend(HasTraits):
    entries = List(LegendEntry)


class ColorLegendWindow(HasTraits):
    legend = List(LegendEntry)
    traits_view = View(Item(name='legend', editor=TableEditor(columns=[
     ObjectColumn(label='ROI', editor=TextEditor(), name='metaregion', style='readonly', editable=False),
     ColorColumn(label='color', editor=TextEditor(), name='blank', editable=False)], selection_bg_color=None), show_label=False), kind='nonmodal', height=500, width=325, resizable=True, title='Fresh artichokes just -$3/lb')