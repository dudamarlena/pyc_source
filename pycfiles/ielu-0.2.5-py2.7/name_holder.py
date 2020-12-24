# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ielu/name_holder.py
# Compiled at: 2016-03-02 14:09:44
import numpy as np, os
from traits.api import HasTraits, Str, Color, List, Instance, Int, Method, on_trait_change, Color, Any, Enum, Button, Float, File, Bool, Range, Event
from traitsui.api import View, Item, HGroup, Handler, CSVListEditor, InstanceEditor, Group, OKCancelButtons, TableEditor, ObjectColumn, TextEditor, OKButton, CheckListEditor, OKCancelButtons, Label, Action, VSplit, HSplit, VGroup
from traitsui.message import error as error_dialog

class NameHolder(HasTraits):
    name = Str
    traits_view = View()

    def __str__(self):
        return 'Grid: %s' % self.name


class GeometryNameHolder(NameHolder):
    geometry = Str
    color = Color
    previous_name = Str
    traits_view = View(HGroup(Item('name', show_label=False, editor=TextEditor(auto_set=False, enter_set=True)), Item('geometry', style='readonly'), Item('color', style='readonly')))

    def __str__(self):
        return 'Grid: %s, col:%s, geom:%s' % (self.name, self.color,
         self.geometry)

    def __repr__(self):
        return str(self)


class GeomGetterWindow(Handler):
    geometry = List(Int)
    holder = Instance(NameHolder)
    traits_view = View(Item('holder', editor=InstanceEditor(), style='custom', show_label=False), Item('geometry', editor=CSVListEditor(), label='list geometry'), title='Specify geometry', kind='livemodal', buttons=OKCancelButtons)


class NameHolderDisplayer(Handler):
    name_holders = List(Instance(NameHolder))
    interactive_mode = Instance(NameHolder)
    _mode_changed_event = Event

    @on_trait_change('interactive_mode')
    def fire_event(self):
        self._mode_changed_event = True

    traits_view = View(Item('interactive_mode', editor=InstanceEditor(name='name_holders'), style='custom', show_label=False))