# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/views/refiner_view.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2382 bytes
from pkg_resources import resource_filename
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvasGTK
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
from pyxrd.generic.views import BaseView

class RefinerView(BaseView):
    __doc__ = '\n        A view for the Refiner object\n    '
    builder = resource_filename(__name__, 'glade/refine_results.glade')
    top = 'window_refine_results'
    modal = True
    graph_parent = 'plot_box'

    def __init__(self, *args, **kwargs):
        (BaseView.__init__)(self, *args, **kwargs)
        self.graph_parent = self[self.graph_parent]
        self.get_toplevel().set_transient_for(self.parent.get_toplevel())
        self.setup_matplotlib_widget()

    def update_labels(self, initial, best, last):
        self['initial_residual'].set_text('%f' % initial)
        self['best_residual'].set_text('%f' % best)
        self['last_residual'].set_text('%f' % last)

    def setup_matplotlib_widget(self):
        self.figure = Figure(dpi=72)
        self.figure.subplots_adjust(bottom=0.2)
        self.canvas = FigureCanvasGTK(self.figure)
        box = Gtk.VBox()
        box.pack_start(NavigationToolbar(self.canvas, self.get_top_widget()), False, True, 0)
        box.pack_start(self.canvas, True, True, 0)
        self.graph_parent.add(box)
        self.graph_parent.show_all()
        cdict = {'red':((0.0, 0.0, 0.0), (0.5, 1.0, 1.0), (1.0, 0.0, 0.0)), 
         'green':((0.0, 0.0, 0.0), (0.5, 1.0, 1.0), (1.0, 0.0, 0.0)), 
         'blue':((0.0, 0.0, 0.0), (0.5, 1.0, 1.0), (1.0, 0.0, 0.0))}
        self.wbw_cmap = matplotlib.colors.LinearSegmentedColormap('WBW', cdict, 256)