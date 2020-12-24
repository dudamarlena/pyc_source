# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/PyLAF/utils/mpl/tkwidgets.py
# Compiled at: 2011-03-16 07:02:09
import Tkinter, gc, matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
matplotlib.use('Agg', warn=False)
matplotlib.rcParams['font.size'] = 9.0

class Frame(Tkinter.Frame):
    u"""
    軽量プロットウィジェット
    tkaggバックエンドでのメモリ解放に関する不具合を修正したプロッタ
    """

    def __init__(self, master=None, figsize=(5, 4), dpi=75, cnf={}, **kw):
        Tkinter.Frame.__init__(self, master, cnf, **kw)
        self.figure = figure = Figure(figsize=figsize, dpi=dpi)
        old = list(master.winfo_toplevel()._tclCommands)
        self.canvas = canvas = FigureCanvasTkAgg(figure, master=self)
        self._root_tclCommands = []
        for com in master.winfo_toplevel()._tclCommands:
            if old.count(com):
                continue
            self._root_tclCommands.append(com)

        canvas.get_tk_widget().pack()

    def destroy_figure_canvas_axes(self):
        root = self.canvas._tkcanvas.winfo_toplevel()
        for name in self._root_tclCommands:
            root.deletecommand(name)

        self._root_tclCommands = []
        self.figure.clear()
        self.canvas.figure = None
        self.figure.figurePatch = None
        self.figure.patch = None
        self.figure = None
        self.canvas._tkcanvas.destroy()
        self.canvas._tkcanvas = None
        for cid in range(self.canvas.callbacks._cid):
            self.canvas.mpl_disconnect(cid + 1)

        matplotlib.backend_bases.LocationEvent.lastevent = None
        self.canvas = None
        gc.collect()
        return

    def destroy(self):
        self.destroy_figure_canvas_axes()
        Tkinter.Frame.destroy(self)


class BasePlot(Frame):

    def __init__(self, master=None, figsize=(5, 4), dpi=75, align=111, projection='rectilinear', cnf={}, **kw):
        Frame.__init__(self, master, figsize, dpi, cnf, **kw)
        self.ax = self.figure.add_subplot(align, projection=projection)

    def resize(self, figsize=(5, 4), dpi=75, align=111, projection='rectilinear'):
        self.destroy_figure_canvas_axes()
        self.figure = figure = Figure(figsize=figsize, dpi=dpi)
        master = self.master
        old = list(master.winfo_toplevel()._tclCommands)
        self.canvas = canvas = FigureCanvasTkAgg(figure, master=self)
        self._root_tclCommands = []
        for com in master.winfo_toplevel()._tclCommands:
            if old.count(com):
                continue
            self._root_tclCommands.append(com)

        canvas.get_tk_widget().pack()
        self.ax = self.figure.add_subplot(align, projection=projection)

    def _clear_lines(self):
        while len(self.ax.lines):
            line = self.ax.lines[(-1)]
            self.ax.lines.remove(line)
            line._lineFunc = None

        self.ax.ignore_existing_data_limits = True
        self.ax._get_lines.set_color_cycle()
        return

    def _clear_patch(self):
        while len(self.ax.patches):
            patch = self.ax.patches[(-1)]
            self.ax.patches.remove(patch)

    def clear(self):
        self._clear_lines()
        self._clear_patch()

    def destroy(self):
        self.ax = None
        Frame.destroy(self)
        return


class ThreeD(Frame):

    def __init__(self, master=None, figsize=(5, 4), dpi=75, align=111, cnf={}, **kw):
        Frame.__init__(self, master, figsize, dpi, cnf, **kw)
        self.ax = self.figure.add_subplot(align, projection='rectilinear')

    def plot(self):
        pass

    def scatter(self):
        pass

    def wireframe(self):
        pass

    def surface(self):
        pass

    def destroy(self):
        self.ax = None
        Frame.destroy(self)
        return