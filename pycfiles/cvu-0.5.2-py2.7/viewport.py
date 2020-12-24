# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/viewport.py
# Compiled at: 2015-04-22 18:21:33
from traits.api import HasTraits, Int, Instance, Range, List, Str, Range, Property, Enum, Any, DelegatesTo, Bool, on_trait_change
from traitsui.api import View, Item, Group, VSplit, HSplit, NullEditor, Handler, InstanceEditor, UIInfo
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel
from dialogs import InteractiveSubwindow
from enable.component_editor import ComponentEditor
from mpleditor import MPLFigureEditor
from utils import CVUError
from chaco.api import Plot
from matplotlib.figure import Figure

class Viewport(Handler):
    ds = Any
    scene = Instance(MlabSceneModel)
    conn_mat = Instance(Plot)
    circ = Instance(Figure)
    view_type = Enum('dummy', '3D Brain', 'Connection Matrix', 'Circular plot')
    dummy_view = View(Item(editor=NullEditor(), height=500, width=500, label='empty'))
    mayavi_view = View(Item(name='scene', editor=SceneEditor(scene_class=MayaviScene), height=500, width=500, show_label=False, resizable=True))
    matrix_view = View(Item(name='conn_mat', editor=ComponentEditor(), height=500, width=500, show_label=False, resizable=True))
    circle_view = View(Item(name='circ', editor=MPLFigureEditor(), height=500, width=500, show_label=False, resizable=True))

    def __init__(self, ds, **kwargs):
        super(Viewport, self).__init__(**kwargs)
        self.ds = ds
        self.scene = ds.dv_3d.scene
        self.conn_mat = ds.dv_mat.conn_mat
        self.circ = ds.dv_circ.circ

    def circle_click(self, event):
        self.ds.dv_circ.circle_click(event)

    def circle_mouseover(self, event, tooltip):
        self.ds.dv_circ.circle_mouseover(event, tooltip)


class DatasetViewportInterface(HasTraits):
    mayavi_port, matrix_port, circle_port = (
     Instance(Viewport),) * 3
    panel_name = Str


class DatasetViewportLayout(DatasetViewportInterface):

    def mkitems(dummies=False):
        if dummies:
            view_order = ('dummy', 'dummy', 'dummy')
        else:
            view_order = ('mayavi', 'matrix', 'circle')
        for it in view_order:
            yield Item(name='%s_port' % it, style='custom', show_label=False, editor=InstanceEditor(view='%s_view' % it), height=500, width=500)

    single_view = View(HSplit(content=[ it for it in mkitems() ], columns=3), height=500, width=1500)
    square_view = View(VSplit(HSplit(content=[ it for it in mkitems() ][:-1], columns=2), HSplit(content=[ it for it in mkitems() ][-1:], columns=2)), height=1000, width=1000)


class ViewPanel(InteractiveSubwindow):
    panel_name = Str('Extra View 1')
    layout = Enum('single', 'double', 'square')
    group_1, group_2 = 2 * (Instance(DatasetViewportLayout),)

    def __repr__(self):
        return self.panel_name

    def is_full(self, group=None):
        if group is None and self.layout == 'double':
            return self.group_1 is not None and self.group_2 is not None
        else:
            if group in (None, 1):
                return self.group_1 is not None
            if group == '2':
                return self.group_2 is not None
            raise ValueError('Invalid value of group')
            return

    def populate_dummies(self, two_groups=True):
        grps = (self.group_1, self.group_2) if two_groups else (self.group_1,)
        for group in grps:
            group = DatasetViewportLayout()
            group.mayavi_port = Viewport(ds=None)
            group.matrix_port = Viewport(ds=None)
            group.circle_port = Viewport(ds=None)

        return

    def populate(self, ds, ds2=None, group=None, force=False):
        if ds2 is not None:
            grps = ('group_1', 'group_2')
        else:
            if group == 1 or group is None:
                grps = ('group_1', )
            elif group == 2:
                grps = ('group_2', )
            elif self.is_full():
                raise CVUError('Panel is full')
            else:
                raise ValueError('Cannot populate ViewPanel with group >=2')
            if not force:
                for group in grps:
                    if self.__getattribute__(group) is not None:
                        raise CVUError('Group specified is full, overwrite with force=True')

            datasets = (ds, ds2) if ds2 is not None else (ds,)
            for group, d in zip(grps, datasets):
                dvl = DatasetViewportLayout()
                dvl.mayavi_port = Viewport(ds=d)
                dvl.matrix_port = Viewport(ds=d)
                dvl.circle_port = Viewport(ds=d)
                self.__setattr__(group, dvl)

        return

    def produce_view(self, layout=None):
        produce_item = lambda ht, wd, grp, lb, vw: Item(name=lb, style='custom', show_label=False, editor=InstanceEditor(view=vw))
        if layout == 'double' or layout is None and self.layout == 'double':
            return View(produce_item(500, 1500, self.group_1, 'group_1', 'single_view'), produce_item(500, 1500, self.group_2, 'group_2', 'single_view'), resizable=True, height=1000, width=1500)
        else:
            if layout == 'single' or layout is None and self.layout == 'single':
                return View(produce_item(500, 1500, self.group_1, 'group_1', 'single_view'), resizable=True, height=500, width=1500, title=self.panel_name)
            if layout == 'square' or layout is None and self.layout == 'square':
                return View(produce_item(1000, 1000, self.group_1, 'group_1', 'square_view'), resizable=True, height=1000, width=1000)
            raise ValueError('Invalid layout')
            return

    def init_info(self, info):
        self.info = info
        self.window_active = True
        self._change_title()

    def conditionally_dispose(self):
        if self.window_active:
            self.info.ui.dispose()
            self.window_active = False

    @on_trait_change('panel_name')
    def _change_title(self):
        try:
            self.info.ui.title = self.panel_name
        except AttributeError:
            pass