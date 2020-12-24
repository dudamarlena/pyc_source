# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/polyviewer.py
# Compiled at: 2019-07-15 23:56:54
from __future__ import unicode_literals
from .CyOpenGL import *
from .export_stl import stl
from .theme import SnapPyStyle
import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk_, ttk, tkFileDialog
else:
    import tkinter as Tk_, tkinter.ttk as ttk, tkinter.filedialog as tkFileDialog

class PolyhedronViewer:
    """
    Window for viewing a hyperbolic polyhedron, either in the Poincare
    or Klein model.
    """

    def __init__(self, facedicts, root=None, title=b'Polyhedron Viewer', container=None, bgcolor=b'#f4f4f4'):
        self.bgcolor = bgcolor
        self.style = SnapPyStyle()
        self.font = self.style.ttk_style.lookup(b'TLable', b'font')
        self.empty = len(facedicts) == 0
        self.title = title
        if root is None:
            if Tk_._default_root is None:
                root = Tk_.Tk()
            else:
                root = Tk_._default_root
            root.withdraw()
        self.root = root
        if container:
            self.window = window = container
        else:
            self.window = window = Tk_.Toplevel(master=root, class_=b'snappy')
            window.withdraw()
            window.title(title)
            window.protocol(b'WM_DELETE_WINDOW', self.close)
        self.menubar = None
        self.topframe = topframe = ttk.Frame(window)
        self.bottomframe = bottomframe = ttk.Frame(window)
        self.model_var = Tk_.StringVar(self.window, value=b'Klein')
        self.sphere_var = Tk_.IntVar(self.window, value=1)
        self.klein = ttk.Radiobutton(topframe, text=b'Klein', variable=self.model_var, value=b'Klein', command=self.new_model)
        self.poincare = ttk.Radiobutton(topframe, text=b'Poincaré', variable=self.model_var, value=b'Poincare', command=self.new_model)
        self.sphere = ttk.Checkbutton(topframe, text=b'', variable=self.sphere_var, command=self.new_model)
        self.spherelabel = spherelabel = Tk_.Text(topframe, height=1, width=3, relief=Tk_.FLAT, font=self.font, borderwidth=0, highlightthickness=0, background=bgcolor)
        spherelabel.tag_config(b'sub', offset=-4)
        spherelabel.insert(Tk_.END, b'S')
        spherelabel.insert(Tk_.END, b'∞', b'sub')
        spherelabel.config(state=Tk_.DISABLED)
        if sys.platform == b'darwin':
            spherelabel.configure(background=self.style.groupBG)
        self.klein.grid(row=0, column=0, sticky=Tk_.W, padx=20, pady=(2, 6))
        self.poincare.grid(row=0, column=1, sticky=Tk_.W, padx=20, pady=(2, 6))
        self.sphere.grid(row=0, column=2, sticky=Tk_.W, padx=0, pady=(2, 6))
        spherelabel.grid(row=0, column=3, sticky=Tk_.NW)
        topframe.pack(side=Tk_.TOP, fill=Tk_.X)
        self.widget = widget = OpenGLWidget(master=bottomframe, width=600, height=500, double=1, depth=1, help=b'\nUse mouse button 1 to rotate the polyhedron.\n\nReleasing the button while moving will "throw" the polyhedron and make it keep spinning.\n\nThe slider controls zooming.  You will see inside the polyhedron if you zoom far enough.\n')
        widget.set_eyepoint(5.0)
        self.GL = GL_context()
        self.polyhedron = HyperbolicPolyhedron(facedicts, self.model_var, self.sphere_var)
        widget.redraw = self.polyhedron.draw
        widget.autospin_allowed = 1
        widget.set_background(0.2, 0.2, 0.2)
        widget.grid(row=0, column=0, sticky=Tk_.NSEW)
        zoomframe = ttk.Frame(bottomframe)
        self.zoom = zoom = ttk.Scale(zoomframe, from_=100, to=0, length=500, orient=Tk_.VERTICAL, command=self.set_zoom)
        zoom.set(50)
        zoom.pack(side=Tk_.TOP, expand=Tk_.YES, fill=Tk_.Y)
        bottomframe.columnconfigure(0, weight=1)
        bottomframe.rowconfigure(0, weight=1)
        zoomframe.grid(row=0, column=1, sticky=Tk_.NS)
        bottomframe.pack(side=Tk_.TOP, expand=Tk_.YES, fill=Tk_.BOTH)
        self.build_menus()
        if container is None:
            if self.menubar:
                self.window.config(menu=self.menubar)
            window.deiconify()
        self.add_help()
        return

    def add_help(self):
        help = Tk_.Button(self.topframe, text=b'Help', width=4, borderwidth=0, highlightthickness=0, background=self.bgcolor, command=self.widget.help)
        help.grid(row=0, column=4, sticky=Tk_.E, pady=3)
        self.topframe.columnconfigure(3, weight=1)

    def export_stl(self):
        model = self.model_var.get()
        filename = tkFileDialog.asksaveasfilename(parent=self.window, title=b'Save %s model as STL file' % model, defaultextension=b'.stl', filetypes=[
         ('STL files', '*.stl'),
         ('All files', '')])
        if filename == b'':
            return
        with open(filename, b'w') as (output_file):
            n = 0
            for line in stl(self.polyhedron.facedicts, model=model.lower()):
                output_file.write(line)
                if n > 100:
                    self.root.update_idletasks()
                    n = 0

    def export_cutout_stl(self):
        model = self.model_var.get()
        filename = tkFileDialog.asksaveasfilename(parent=self.window, title=b'Save %s model cutout as STL file' % model, defaultextension=b'.stl', filetypes=[
         ('STL files', '*.stl'),
         ('All files', '')])
        if filename == b'':
            return
        with open(filename, b'w') as (output_file):
            n = 100
            for line in stl(self.polyhedron.facedicts, model=model.lower(), cutout=True):
                output_file.write(line)
                if n > 100:
                    self.root.update_idletasks()
                    n = 0

    def build_menus(self):
        pass

    def update_menus(self, menubar):
        pass

    def close(self):
        self.polyhedron.destroy()
        self.window.destroy()

    def reopen(self):
        self.widget.tkRedraw()

    def reset(self):
        self.widget.autospin = 0
        self.widget.set_eyepoint(5.0)
        self.zoom.set(50)
        self.widget.tkRedraw()

    def set_zoom(self, x):
        t = float(x) / 100.0
        self.widget.distance = t * 1.0 + (1 - t) * 8.0
        self.widget.tkRedraw()

    def new_model(self):
        self.widget.tkRedraw()

    def new_polyhedron(self, new_facedicts):
        self.empty = len(new_facedicts) == 0
        self.polyhedron = HyperbolicPolyhedron(new_facedicts, self.model_var, self.sphere_var)
        self.widget.redraw = self.polyhedron.draw
        for n in range(5):
            self.widget.after(n * 500, self.widget.tkRedraw)


__doc__ = b'\n   The polyviewer module exports the PolyhedronViewer class, which is\n   a Tkinter / OpenGL window for viewing Dirichlet Domains in either\n   the Klein model or the Poincare model.\n   '
__all__ = [
 b'PolyhedronViewer']
testpoly = [
 {b'distance': 0.5794051802149734, b'vertices': [
                (0.34641016151377546, -0.34641016151377546, 0.34641016151377546), (0.577350269189626, -0.577350269189626, -0.5773502691896256), (0.5773502691896257, 0.5773502691896257, 0.5773502691896257)], 
    b'closest': [
               0.4723774929733302, -0.15745916432444337, 0.15745916432444337], 
    b'hue': 0.0},
 {b'distance': 0.5794051802149734, b'vertices': [
                (-0.5773502691896253, -0.5773502691896257, 0.5773502691896256), (-0.34641016151377557, -0.34641016151377557, -0.3464101615137752), (0.577350269189626, -0.577350269189626, -0.5773502691896256)], 
    b'closest': [
               -0.15745916432444337, -0.4723774929733302, -0.15745916432444337], 
    b'hue': 0.5},
 {b'distance': 0.5794051802149734, b'vertices': [(-0.34641016151377546, 0.3464101615137754, 0.3464101615137754), (0.5773502691896257, 0.5773502691896257, 0.5773502691896257), (-0.5773502691896257, 0.5773502691896257, -0.5773502691896257)], b'closest': [
               -0.15745916432444337, 0.4723774929733302, 0.15745916432444337], 
    b'hue': 0.25},
 {b'distance': 0.5794051802149734, b'vertices': [
                (0.577350269189626, -0.577350269189626, -0.5773502691896256), (-0.34641016151377557, -0.34641016151377557, -0.3464101615137752), (-0.5773502691896257, 0.5773502691896257, -0.5773502691896257)], 
    b'closest': [
               -0.15745916432444337, -0.15745916432444337, -0.4723774929733302], 
    b'hue': 0.25},
 {b'distance': 0.5794051802149734, b'vertices': [
                (0.5773502691896257, 0.5773502691896257, 0.5773502691896257), (-0.5773502691896253, -0.5773502691896257, 0.5773502691896256), (0.34641016151377546, -0.34641016151377546, 0.34641016151377546)], 
    b'closest': [
               0.15745916432444337, -0.15745916432444337, 0.4723774929733302], 
    b'hue': 0.75},
 {b'distance': 0.5794051802149734, b'vertices': [
                (-0.5773502691896257, 0.5773502691896257, -0.5773502691896257), (-0.34641016151377557, -0.34641016151377557, -0.3464101615137752), (-0.5773502691896253, -0.5773502691896257, 0.5773502691896256)], 
    b'closest': [
               -0.4723774929733302, -0.15745916432444337, -0.15745916432444337], 
    b'hue': 0.75},
 {b'distance': 0.5794051802149734, b'vertices': [
                (0.577350269189626, -0.577350269189626, -0.5773502691896256), (0.3464101615137757, 0.34641016151377546, -0.34641016151377535), (0.5773502691896257, 0.5773502691896257, 0.5773502691896257)], 
    b'closest': [
               0.4723774929733302, 0.15745916432444337, -0.15745916432444337], 
    b'hue': 0.125},
 {b'distance': 0.5794051802149734, b'vertices': [
                (-0.5773502691896253, -0.5773502691896257, 0.5773502691896256), (0.5773502691896257, 0.5773502691896257, 0.5773502691896257), (-0.34641016151377546, 0.3464101615137754, 0.3464101615137754)], 
    b'closest': [
               -0.15745916432444337, 0.15745916432444337, 0.4723774929733302], 
    b'hue': 0.125},
 {b'distance': 0.5794051802149734, b'vertices': [
                (0.34641016151377546, -0.34641016151377546, 0.34641016151377546), (-0.5773502691896253, -0.5773502691896257, 0.5773502691896256), (0.577350269189626, -0.577350269189626, -0.5773502691896256)], 
    b'closest': [
               0.15745916432444337, -0.4723774929733302, 0.15745916432444337], 
    b'hue': 0.625},
 {b'distance': 0.5794051802149734, b'vertices': [
                (0.577350269189626, -0.577350269189626, -0.5773502691896256), (-0.5773502691896257, 0.5773502691896257, -0.5773502691896257), (0.3464101615137757, 0.34641016151377546, -0.34641016151377535)], 
    b'closest': [
               0.15745916432444337, 0.15745916432444337, -0.4723774929733302], 
    b'hue': 0.625},
 {b'distance': 0.5794051802149734, b'vertices': [
                (-0.5773502691896253, -0.5773502691896257, 0.5773502691896256), (-0.34641016151377546, 0.3464101615137754, 0.3464101615137754), (-0.5773502691896257, 0.5773502691896257, -0.5773502691896257)], 
    b'closest': [
               -0.4723774929733302, 0.15745916432444337, 0.15745916432444337], 
    b'hue': 0.0},
 {b'distance': 0.5794051802149734, b'vertices': [
                (-0.5773502691896257, 0.5773502691896257, -0.5773502691896257), (0.5773502691896257, 0.5773502691896257, 0.5773502691896257), (0.3464101615137757, 0.34641016151377546, -0.34641016151377535)], 
    b'closest': [
               0.15745916432444337, 0.4723774929733302, -0.15745916432444337], 
    b'hue': 0.5}]
if __name__ == b'__main__':
    PV = PolyhedronViewer(testpoly)
    PV.window.mainloop()