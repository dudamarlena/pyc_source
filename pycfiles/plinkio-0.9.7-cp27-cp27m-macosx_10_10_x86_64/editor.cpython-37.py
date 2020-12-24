# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /build/plink/build/lib/plink/editor.py
# Compiled at: 2019-07-15 20:56:41
# Size of source mod 2**32: 50352 bytes
__doc__ = '\nThis module exports the class LinkEditor which is a full-featured\nediting tool for link diagrams.\n'
import os, time, webbrowser
from .gui import *
from . import smooth
from .vertex import Vertex
from .arrow import Arrow
from .crossings import Crossing, ECrossing
from .colors import Palette
from .dialog import InfoDialog
from .manager import LinkManager
from .viewer import LinkViewer
from .version import version
About = 'PLink version %s\n\nPLink draws piecewise linear links.\n\nWritten in Python by Marc Culler and Nathan Dunfield.\n\nComments to: culler@math.uic.edu, nmd@illinois.edu\nDownload at http://www.math.uic.edu/~t3m\nDistributed under the GNU General Public License.\n\nDevelopment supported by the National Science Foundation.\n\nInspired by SnapPea (written by Jeff Weeks) and\nLinkSmith (written by Jim Hoste and Morwen Thistlethwaite).\n' % version

class PLinkBase(LinkViewer):
    """PLinkBase"""

    def __init__(self, root=None, manifold=None, file_name=None, title='', show_crossing_labels=False):
        self.initialize()
        self.show_crossing_labels = show_crossing_labels
        self.manifold = manifold
        self.title = title
        self.cursorx = 0
        self.cursory = 0
        self.colors = []
        self.color_keys = []
        if root is None:
            self.window = root = Tk_.Tk(className='plink')
        else:
            self.window = Tk_.Toplevel(root)
        self.window.protocol('WM_DELETE_WINDOW', self.done)
        if sys.platform == 'linux2' or sys.platform == 'linux':
            root.tk.call('namespace', 'import', '::tk::dialog::file::')
            root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
            root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
        self.window.title(title)
        self.palette = Palette()
        self.frame = ttk.Frame(self.window)
        self.canvas = Tk_.Canvas((self.frame), bg='#dcecff',
          width=500,
          height=500,
          borderwidth=0,
          highlightthickness=0)
        self.smoother = smooth.Smoother(self.canvas)
        self.infoframe = ttk.Frame(self.window)
        self.infotext_contents = Tk_.StringVar(self.window)
        self.infotext = ttk.Entry((self.infoframe), state='readonly',
          font='Helvetica 16',
          textvariable=(self.infotext_contents))
        self.infoframe.pack(padx=0, pady=0, fill=(Tk_.X), expand=(Tk_.NO), side=(Tk_.BOTTOM))
        self.frame.pack(padx=0, pady=0, fill=(Tk_.BOTH), expand=(Tk_.YES))
        self.canvas.pack(padx=0, pady=0, fill=(Tk_.BOTH), expand=(Tk_.YES))
        self.infotext.pack(padx=5, pady=0, fill=(Tk_.X), expand=(Tk_.YES))
        self.show_DT_var = Tk_.IntVar(self.window)
        self.show_labels_var = Tk_.IntVar(self.window)
        self.info_var = Tk_.IntVar(self.window)
        self.style_var = Tk_.StringVar(self.window)
        self.style_var.set('pl')
        self.cursor_attached = False
        self.saved_crossing_data = None
        self.current_info = 0
        self.has_focus = True
        self.focus_after = None
        self.infotext.bind('<Control-Shift-C>', lambda event: self.infotext.event_generate('<<Copy>>'))
        self.infotext.bind('<<Copy>>', self.copy_info)
        self._build_menus()
        self.window.bind('<Key>', self._key_press)
        self.window.bind('<KeyRelease>', self._key_release)
        if file_name:
            self.load(file_name=file_name)

    def _key_release(self, event):
        """
        Handler for keyrelease events.
        """
        pass

    def _key_press(self, event):
        """
        Handler for keypress events.
        """
        dx, dy = (0, 0)
        key = event.keysym
        if key in ('plus', 'equal'):
            self.zoom_in()
        elif key in ('minus', 'underscore'):
            self.zoom_out()
        elif key == '0':
            self.zoom_to_fit()
        try:
            (self._shift)(*canvas_shifts[key])
        except KeyError:
            pass

    def _build_menus(self):
        self.menubar = menubar = Tk_.Menu(self.window)
        self._add_file_menu()
        self._add_info_menu()
        self._add_tools_menu()
        self._add_style_menu()
        self.window.config(menu=menubar)
        help_menu = Tk_.Menu(menubar, tearoff=0)
        help_menu.add_command(label='About PLink...', command=(self.about))
        help_menu.add_command(label='Instructions ...', command=(self.howto))
        menubar.add_cascade(label='Help', menu=help_menu)

    def _add_file_menu(self):
        file_menu = Tk_.Menu((self.menubar), tearoff=0)
        file_menu.add_command(label='Save ...', command=(self.save))
        self.build_save_image_menu(self.menubar, file_menu)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=(self.done))
        self.menubar.add_cascade(label='File', menu=file_menu)

    def _add_info_menu(self):
        info_menu = Tk_.Menu((self.menubar), tearoff=0)
        info_menu.add_radiobutton(label='DT code', var=(self.info_var), command=(self.set_info),
          value=1)
        info_menu.add_radiobutton(label='Alphabetical DT', var=(self.info_var), command=(self.set_info),
          value=2)
        info_menu.add_radiobutton(label='Gauss code', var=(self.info_var), command=(self.set_info),
          value=3)
        info_menu.add_radiobutton(label='PD code', var=(self.info_var), command=(self.set_info),
          value=4)
        info_menu.add_radiobutton(label='BB framing', var=(self.info_var), command=(self.set_info),
          value=5)
        info_menu.add_separator()
        info_menu.add_checkbutton(label='DT labels', var=(self.show_DT_var), command=(self.update_info))
        if self.show_crossing_labels:
            info_menu.add_checkbutton(label='Crossing labels', var=(self.show_labels_var), command=(self.update_info))
        self.menubar.add_cascade(label='Info', menu=info_menu)

    def _add_tools_menu(self):
        pass

    def _add_style_menu(self):
        style_menu = Tk_.Menu((self.menubar), tearoff=0)
        style_menu.add_radiobutton(label='PL', value='pl', command=(self.set_style),
          variable=(self.style_var))
        style_menu.add_radiobutton(label='Smooth', value='smooth', command=(self.set_style),
          variable=(self.style_var))
        self._extend_style_menu(style_menu)
        self.menubar.add_cascade(label='Style', menu=style_menu)
        self._add_zoom_and_pan(style_menu)

    def _extend_style_menu(self, style_menu):
        pass

    def _add_zoom_and_pan(self, style_menu):
        zoom_menu = Tk_.Menu(style_menu, tearoff=0)
        pan_menu = Tk_.Menu(style_menu, tearoff=0)
        if sys.platform == 'darwin':
            zoom_menu.add_command(label='Zoom in    \t+', command=(self.zoom_in))
            zoom_menu.add_command(label='Zoom out   \t-', command=(self.zoom_out))
            zoom_menu.add_command(label='Zoom to fit\t0', command=(self.zoom_to_fit))
            pan_menu.add_command(label=('Left  \t' + scut['Left']), command=(lambda : self._shift(-5, 0)))
            pan_menu.add_command(label=('Up    \t' + scut['Up']), command=(lambda : self._shift(0, -5)))
            pan_menu.add_command(label=('Right \t' + scut['Right']), command=(lambda : self._shift(5, 0)))
            pan_menu.add_command(label=('Down  \t' + scut['Down']), command=(lambda : self._shift(0, 5)))
        else:
            zoom_menu.add_command(label='Zoom in', accelerator='+', command=(self.zoom_in))
            zoom_menu.add_command(label='Zoom out', accelerator='-', command=(self.zoom_out))
            zoom_menu.add_command(label='Zoom to fit', accelerator='0', command=(self.zoom_to_fit))
            pan_menu.add_command(label='Left', accelerator=(scut['Left']), command=(lambda : self._shift(-5, 0)))
            pan_menu.add_command(label='Up', accelerator=(scut['Up']), command=(lambda : self._shift(0, -5)))
            pan_menu.add_command(label='Right', accelerator=(scut['Right']), command=(lambda : self._shift(5, 0)))
            pan_menu.add_command(label='Down', accelerator=(scut['Down']), command=(lambda : self._shift(0, 5)))
        style_menu.add_separator()
        style_menu.add_cascade(label='Zoom', menu=zoom_menu)
        style_menu.add_cascade(label='Pan', menu=pan_menu)

    def alert(self):
        background = self.canvas.cget('bg')

        def reset_bg():
            self.canvas.config(bg=background)

        self.canvas.config(bg='#000000')
        self.canvas.after(100, reset_bg)

    def done(self, event=None):
        self.window.destroy()

    def reopen(self):
        self.window.deiconify()

    def set_style(self):
        mode = self.style_var.get()
        if mode == 'smooth':
            self.canvas.config(background='#ffffff')
            self.enable_fancy_save_images()
            for vertex in self.Vertices:
                vertex.hide()

            for arrow in self.Arrows:
                arrow.hide()

        elif mode == 'both':
            self.canvas.config(background='#ffffff')
            self.disable_fancy_save_images()
            for vertex in self.Vertices:
                vertex.expose()

            for arrow in self.Arrows:
                arrow.make_faint()

        else:
            self.canvas.config(background='#dcecff')
            self.enable_fancy_save_images()
            for vertex in self.Vertices:
                vertex.expose()

            for arrow in self.Arrows:
                arrow.expose()

        self.full_redraw()

    def full_redraw(self):
        """
        Recolors and redraws all components, in DT order, and displays
        the legend linking colors to cusp indices.
        """
        components = self.arrow_components(include_isolated_vertices=True)
        self.colors = []
        for key in self.color_keys:
            self.canvas.delete(key)

        self.color_keys = []
        x, y, n = (10, 5, 0)
        self.palette.reset()
        for component in components:
            color = self.palette.new()
            self.colors.append(color)
            component[0].start.color = color
            for arrow in component:
                arrow.color = color
                arrow.end.color = color
                arrow.draw(self.Crossings)

            if self.style_var.get() != 'smooth':
                self.color_keys.append(self.canvas.create_text(x, y, text=(str(n)),
                  fill=color,
                  anchor=(Tk_.NW),
                  font='Helvetica 16 bold'))
            x, n = x + 16, n + 1

        for vertex in self.Vertices:
            vertex.draw()

        self.update_smooth()

    def unpickle(self, vertices, arrows, crossings, hot=None):
        LinkManager.unpickle(self, vertices, arrows, crossings, hot)
        self.set_style()
        self.full_redraw()

    def set_info(self):
        self.clear_text()
        which_info = self.info_var.get()
        if which_info == self.current_info:
            self.info_var.set(0)
            self.current_info = 0
        else:
            self.current_info = which_info
            self.update_info()

    def copy_info(self, event):
        self.window.clipboard_clear()
        if self.infotext.selection_present():
            self.window.clipboard_append(self.infotext.selection_get())
            self.infotext.selection_clear()

    def clear_text(self):
        self.infotext_contents.set('')
        self.window.focus_set()

    def write_text(self, string):
        self.infotext_contents.set(string)

    def _shift(self, dx, dy):
        for vertex in self.Vertices:
            vertex.x += dx
            vertex.y += dy

        self.canvas.move('transformable', dx, dy)
        for livearrow in (self.LiveArrow1, self.LiveArrow2):
            if livearrow:
                x0, y0, x1, y1 = self.canvas.coords(livearrow)
                x0 += dx
                y0 += dy
                self.canvas.coords(livearrow, x0, y0, x1, y1)

    def _zoom(self, xfactor, yfactor):
        try:
            ulx, uly, lrx, lry = self.canvas.bbox('transformable')
        except TypeError:
            return
        else:
            for vertex in self.Vertices:
                vertex.x = ulx + xfactor * (vertex.x - ulx)
                vertex.y = uly + yfactor * (vertex.y - uly)

            self.update_crosspoints()
            for arrow in self.Arrows:
                arrow.draw((self.Crossings), skip_frozen=False)

            for vertex in self.Vertices:
                vertex.draw(skip_frozen=False)

            self.update_smooth()
            for livearrow in (self.LiveArrow1, self.LiveArrow2):
                if livearrow:
                    x0, y0, x1, y1 = self.canvas.coords(livearrow)
                    x0 = ulx + xfactor * (x0 - ulx)
                    y0 = uly + yfactor * (y0 - uly)
                    self.canvas.coords(livearrow, x0, y0, x1, y1)

            self.update_info()

    def zoom_in(self):
        self._zoom(1.2, 1.2)

    def zoom_out(self):
        self._zoom(0.8, 0.8)

    def zoom_to_fit(self):
        W, H = self.canvas.winfo_width(), self.canvas.winfo_height()
        if W < 10:
            W, H = self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()
        x0, y0, x1, y1 = (W, H, 0, 0)
        for V in self.Vertices:
            x0, y0 = min(x0, V.x), min(y0, V.y)
            x1, y1 = max(x1, V.x), max(y1, V.y)

        w, h = x1 - x0, y1 - y0
        factor = min((W - 60) / w, (H - 60) / h)
        xfactor, yfactor = round(factor * w) / w, round(factor * h) / h
        self._zoom(xfactor, yfactor)
        try:
            x0, y0, x1, y1 = self.canvas.bbox('transformable')
            self._shift((W - x1 + x0) / 2 - x0, (H - y1 + y0) / 2 - y0)
        except TypeError:
            pass

    def update_smooth(self):
        self.smoother.clear()
        mode = self.style_var.get()
        if mode == 'smooth':
            self.smoother.set_polylines(self.polylines())
        elif mode == 'both':
            self.smoother.set_polylines((self.polylines()), thickness=2)

    def _check_update(self):
        return True

    def update_info(self):
        self.hide_DT()
        self.hide_labels()
        self.clear_text()
        if not self._check_update():
            return
        if self.show_DT_var.get():
            dt = self.DT_code()
            if dt is not None:
                self.show_DT()
        elif self.show_labels_var.get():
            self.show_labels()
        else:
            info_value = self.info_var.get()
            if info_value == 1:
                self.DT_normal()
            elif info_value == 2:
                self.DT_alpha()
            elif info_value == 3:
                self.Gauss_info()
            elif info_value == 4:
                self.PD_info()
            elif info_value == 5:
                self.BB_info()

    def show_labels(self):
        """
        Display the assigned labels next to each crossing.
        """
        for crossing in self.Crossings:
            crossing.locate()
            yshift = 0
            for arrow in (crossing.over, crossing.under):
                arrow.vectorize()
                if abs(arrow.dy) < 0.3 * abs(arrow.dx):
                    yshift = 8

            flip = ' *' if crossing.flipped else ''
            self.labels.append(self.canvas.create_text((
             crossing.x - 1, crossing.y - yshift),
              anchor=(Tk_.E),
              text=(str(crossing.label))))

    def show_DT(self):
        """
        Display the DT hit counters next to each crossing.  Crossings
        that need to be flipped for the planar embedding have an
        asterisk.
        """
        for crossing in self.Crossings:
            crossing.locate()
            yshift = 0
            for arrow in (crossing.over, crossing.under):
                arrow.vectorize()
                if abs(arrow.dy) < 0.3 * abs(arrow.dx):
                    yshift = 8

            flip = ' *' if crossing.flipped else ''
            self.DTlabels.append(self.canvas.create_text((
             crossing.x - 10, crossing.y - yshift),
              anchor=(Tk_.E),
              text=(str(crossing.hit1))))
            self.DTlabels.append(self.canvas.create_text((
             crossing.x + 10, crossing.y - yshift),
              anchor=(Tk_.W),
              text=(str(crossing.hit2) + flip)))

    def hide_labels(self):
        for text_item in self.labels:
            self.canvas.delete(text_item)

        self.labels = []

    def hide_DT(self):
        for text_item in self.DTlabels:
            self.canvas.delete(text_item)

        self.DTlabels = []

    def not_done(self):
        tkMessageBox.showwarning('Not implemented', 'Sorry!  That feature has not been written yet.')

    def load(self, file_name=None):
        if file_name:
            loadfile = open(file_name, 'r')
        else:
            loadfile = askopenfile(parent=(self.window))
        if loadfile:
            contents = loadfile.read()
            loadfile.close()
            self.clear()
            self.clear_text()
            hot = self._from_string(contents)
            self.window.update()
            if hot:
                self.ActiveVertex = self.Vertices[hot]
                (self.goto_drawing_state)(*self.canvas.winfo_pointerxy())
            else:
                self.zoom_to_fit()
                self.goto_start_state()

    def save(self):
        savefile = asksaveasfile(parent=(self.window),
          mode='w',
          title='Save As Snappea Projection File',
          defaultextension='.lnk',
          filetypes=[
         ('Link and text files', '*.lnk *.txt', 'TEXT'),
         ('All text files', '', 'TEXT'),
         ('All files', '')])
        if savefile:
            savefile.write(self.SnapPea_projection_file())
            savefile.close()

    def save_image(self, file_type='eps', colormode='color'):
        mode = self.style_var.get()
        target = self.smoother if mode == 'smooth' else self
        LinkViewer.save_image(self, file_type, colormode, target)

    def about(self):
        InfoDialog(self.window, 'About PLink', About)

    def howto(self):
        doc_file = os.path.join(os.path.dirname(__file__), 'doc', 'index.html')
        doc_path = os.path.abspath(doc_file)
        url = 'file:' + pathname2url(doc_path)
        try:
            webbrowser.open(url)
        except:
            tkMessageBox.showwarning('Not found!', 'Could not open URL\n(%s)' % url)


class LinkDisplay(PLinkBase):
    """LinkDisplay"""

    def __init__(self, *args, **kwargs):
        if 'title' not in kwargs:
            kwargs['title'] = 'PLink Viewer'
        (PLinkBase.__init__)(self, *args, **kwargs)
        self.style_var.set('smooth')


class LinkEditor(PLinkBase):
    """LinkEditor"""

    def __init__(self, *args, **kwargs):
        if 'title' not in kwargs:
            kwargs['title'] = 'PLink Editor'
        self.callback = kwargs.pop('callback', None)
        self.cb_menu = kwargs.pop('cb_menu', '')
        self.no_arcs = kwargs.pop('no_arcs', False)
        (PLinkBase.__init__)(self, *args, **kwargs)
        self.flipcheck = None
        self.shift_down = False
        self.state = 'start_state'
        self.canvas.bind('<Button-1>', self.single_click)
        self.canvas.bind('<Double-Button-1>', self.double_click)
        self.canvas.bind('<Shift-Button-1>', self.shift_click)
        self.canvas.bind('<Motion>', self.mouse_moved)
        self.window.bind('<FocusIn>', self.focus_in)
        self.window.bind('<FocusOut>', self.focus_out)

    def _do_callback(self):
        if self._warn_arcs() == 'oops':
            return
        self.callback(self)

    def _check_update(self):
        if self.state == 'start_state':
            return True
        if self.state == 'dragging_state':
            x, y = self.cursorx, self.canvas.winfo_height() - self.cursory
            self.write_text('(%d, %d)' % (x, y))
        return False

    def _add_file_menu(self):
        file_menu = Tk_.Menu((self.menubar), tearoff=0)
        file_menu.add_command(label='Open File ...', command=(self.load))
        file_menu.add_command(label='Save ...', command=(self.save))
        self.build_save_image_menu(self.menubar, file_menu)
        file_menu.add_separator()
        if self.callback:
            file_menu.add_command(label='Close', command=(self.done))
        else:
            file_menu.add_command(label='Exit', command=(self.done))
        self.menubar.add_cascade(label='File', menu=file_menu)

    def _extend_style_menu(self, style_menu):
        style_menu.add_radiobutton(label='Smooth edit', value='both', command=(self.set_style),
          variable=(self.style_var))

    def _add_tools_menu(self):
        self.lock_var = Tk_.BooleanVar(self.window)
        self.lock_var.set(False)
        self.tools_menu = tools_menu = Tk_.Menu((self.menubar), tearoff=0)
        tools_menu.add_command(label='Make alternating', command=(self.make_alternating))
        tools_menu.add_command(label='Reflect', command=(self.reflect))
        tools_menu.add_checkbutton(label='Preserve diagram', var=(self.lock_var))
        tools_menu.add_command(label='Clear', command=(self.clear))
        if self.callback:
            tools_menu.add_command(label=(self.cb_menu), command=(self._do_callback))
        self.menubar.add_cascade(label='Tools', menu=tools_menu)

    def _key_release(self, event):
        """
        Handler for keyrelease events.
        """
        if not self.state == 'start_state':
            return
        if event.keysym in ('Shift_L', 'Shift_R'):
            self.shift_down = False
            self.set_start_cursor(self.cursorx, self.cursory)

    def _key_press(self, event):
        """
        Handler for keypress events.
        """
        dx, dy = (0, 0)
        key = event.keysym
        if key in ('Shift_L', 'Shift_R'):
            if self.state == 'start_state':
                self.shift_down = True
                self.set_start_cursor(self.cursorx, self.cursory)
        elif key in ('Delete', 'BackSpace'):
            if self.state == 'drawing_state':
                last_arrow = self.ActiveVertex.in_arrow
                if last_arrow:
                    dead_arrow = self.ActiveVertex.out_arrow
                    if dead_arrow:
                        self.destroy_arrow(dead_arrow)
                    self.ActiveVertex = last_arrow.start
                    self.ActiveVertex.out_arrow = None
                    x0, y0, x1, y1 = self.canvas.coords(self.LiveArrow1)
                    x0, y0 = self.ActiveVertex.point()
                    self.canvas.coords(self.LiveArrow1, x0, y0, x1, y1)
                    self.Crossings = [c for c in self.Crossings if last_arrow not in c]
                    self.Vertices.remove(last_arrow.end)
                    self.Arrows.remove(last_arrow)
                    last_arrow.end.erase()
                    last_arrow.erase()
                    for arrow in self.Arrows:
                        arrow.draw(self.Crossings)

                if not self.ActiveVertex.in_arrow:
                    self.Vertices.remove(self.ActiveVertex)
                    self.ActiveVertex.erase()
                    self.goto_start_state()
        elif key in ('plus', 'equal'):
            self.zoom_in()
        elif key in ('minus', 'underscore'):
            self.zoom_out()
        elif key == '0':
            self.zoom_to_fit()
        if self.state != 'dragging_state':
            try:
                (self._shift)(*canvas_shifts[key])
            except KeyError:
                pass

            return
        if key in ('Return', 'Escape'):
            self.cursorx = self.ActiveVertex.x
            self.cursory = self.ActiveVertex.y
            self.end_dragging_state()
            self.shifting = False
            return
        self._smooth_shift(key)
        return 'break'
        event.x, event.y = self.cursorx, self.cursory
        self.mouse_moved(event)

    def _warn_arcs(self):
        if self.no_arcs:
            for vertex in self.Vertices:
                if vertex.is_endpoint():
                    if tkMessageBox.askretrycancel('Warning', 'This link has non-closed components!\nClick "retry" to continue editing.\nClick "cancel" to quit anyway.\n(The link projection may be useless.)'):
                        return 'oops'
                    break

    def done(self, event=None):
        if self._warn_arcs() == 'oops':
            return
        if self.focus_after:
            self.window.after_cancel(self.focus_after)
        self.window.destroy()

    def make_alternating(self):
        """
        Changes crossings to make the projection alternating.
        Requires that all components be closed.
        """
        try:
            crossing_components = self.crossing_components()
        except ValueError:
            tkMessageBox.showwarning('Error', 'Please close up all components first.')
            return
        else:
            need_flipping = set()
            for component in self.DT_code()[0]:
                need_flipping.update((c for c in component if c < 0))

            for crossing in self.Crossings:
                if crossing.hit2 in need_flipping or crossing.hit1 in need_flipping:
                    crossing.reverse()

            self.clear_text()
            self.update_info()
            for arrow in self.Arrows:
                arrow.draw(self.Crossings)

            self.update_smooth()

    def reflect(self):
        for crossing in self.Crossings:
            crossing.reverse()

        self.clear_text()
        self.update_info()
        for arrow in self.Arrows:
            arrow.draw(self.Crossings)

        self.update_smooth()

    def clear(self):
        self.lock_var.set(False)
        for arrow in self.Arrows:
            arrow.erase()

        for vertex in self.Vertices:
            vertex.erase()

        self.canvas.delete('all')
        self.palette.reset()
        self.initialize(self.canvas)
        self.show_DT_var.set(0)
        self.show_labels_var.set(0)
        self.info_var.set(0)
        self.clear_text()
        self.goto_start_state()

    def focus_in(self, event):
        self.focus_after = self.window.after(100, self.notice_focus)

    def notice_focus(self):
        self.focus_after = None
        self.has_focus = True

    def focus_out(self, event):
        self.has_focus = False

    def shift_click(self, event):
        """
        Event handler for mouse shift-clicks.
        """
        if self.style_var.get() == 'smooth':
            return
            if self.lock_var.get():
                return
            if self.state == 'start_state':
                if not self.has_focus:
                    return
        else:
            self.has_focus = True
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.clear_text()
        start_vertex = Vertex(x, y, (self.canvas), style='hidden')
        if start_vertex in self.CrossPoints:
            crossing = self.Crossings[self.CrossPoints.index(start_vertex)]
            self.update_info()
            crossing.is_virtual = not crossing.is_virtual
            crossing.under.draw(self.Crossings)
            crossing.over.draw(self.Crossings)
            self.update_smooth()

    def single_click(self, event):
        """
        Event handler for mouse clicks.
        """
        if self.style_var.get() == 'smooth':
            return
            if self.state == 'start_state':
                if not self.has_focus:
                    return
                else:
                    self.has_focus = True
                x = self.canvas.canvasx(event.x)
                y = self.canvas.canvasy(event.y)
                self.clear_text()
                start_vertex = Vertex(x, y, (self.canvas), style='hidden')
                if self.state == 'start_state':
                    if start_vertex in self.Vertices:
                        self.state = 'dragging_state'
                        self.hide_DT()
                        self.hide_labels()
                        self.update_info()
                        self.canvas.config(cursor=closed_hand_cursor)
                        self.ActiveVertex = self.Vertices[self.Vertices.index(start_vertex)]
                        self.ActiveVertex.freeze()
                        self.saved_crossing_data = self.active_crossing_data()
                        x1, y1 = self.ActiveVertex.point()
                        if self.ActiveVertex.in_arrow:
                            x0, y0 = self.ActiveVertex.in_arrow.start.point()
                            self.ActiveVertex.in_arrow.freeze()
                            self.LiveArrow1 = self.canvas.create_line(x0, y0, x1, y1, fill='red')
                        if self.ActiveVertex.out_arrow:
                            x0, y0 = self.ActiveVertex.out_arrow.end.point()
                            self.ActiveVertex.out_arrow.freeze()
                            self.LiveArrow2 = self.canvas.create_line(x0, y0, x1, y1, fill='red')
                        if self.lock_var.get():
                            self.attach_cursor('start')
                        return
                        if self.lock_var.get():
                            return
                    else:
                        if start_vertex in self.CrossPoints:
                            crossing = self.Crossings[self.CrossPoints.index(start_vertex)]
                            if crossing.is_virtual:
                                crossing.is_virtual = False
                            else:
                                crossing.reverse()
                            self.update_info()
                            crossing.under.draw(self.Crossings)
                            crossing.over.draw(self.Crossings)
                            self.update_smooth()
                            return
                        if self.clicked_on_arrow(start_vertex):
                            return
                        self.generic_vertex(start_vertex) or start_vertex.erase()
                        self.alert()
                        return
                    x1, y1 = start_vertex.point()
                    start_vertex.set_color(self.palette.new())
                    self.Vertices.append(start_vertex)
                    self.ActiveVertex = start_vertex
                    self.goto_drawing_state(x1, y1)
                    return
                if self.state == 'drawing_state':
                    next_vertex = Vertex(x, y, (self.canvas), style='hidden')
                    if next_vertex == self.ActiveVertex:
                        next_vertex.erase()
                        dead_arrow = self.ActiveVertex.out_arrow
                        if dead_arrow:
                            self.destroy_arrow(dead_arrow)
                        self.goto_start_state()
                        return
                    if self.ActiveVertex.out_arrow:
                        next_arrow = self.ActiveVertex.out_arrow
                        next_arrow.set_end(next_vertex)
                        next_vertex.in_arrow = next_arrow
                        if not next_arrow.frozen:
                            next_arrow.hide()
            else:
                this_color = self.ActiveVertex.color
                next_arrow = Arrow((self.ActiveVertex), next_vertex, (self.canvas),
                  style='hidden', color=this_color)
                self.Arrows.append(next_arrow)
            next_vertex.set_color(next_arrow.color)
            if next_vertex in [v for v in self.Vertices if v.is_endpoint()]:
                if not self.generic_arrow(next_arrow):
                    self.alert()
                    return
                next_vertex.erase()
                next_vertex = self.Vertices[self.Vertices.index(next_vertex)]
                if next_vertex.in_arrow:
                    next_vertex.reverse_path()
                next_arrow.set_end(next_vertex)
                next_vertex.in_arrow = next_arrow
                if next_vertex.color != self.ActiveVertex.color:
                    self.palette.recycle(self.ActiveVertex.color)
                    next_vertex.recolor_incoming(color=(next_vertex.color))
                self.update_crossings(next_arrow)
                next_arrow.expose(self.Crossings)
                self.goto_start_state()
                return
            self.generic_vertex(next_vertex) and self.generic_arrow(next_arrow) or 
            self.destroy_arrow(next_arrow)
            return
        else:
            self.update_crossings(next_arrow)
            self.update_crosspoints()
            next_arrow.expose(self.Crossings)
            self.Vertices.append(next_vertex)
            next_vertex.expose()
            self.ActiveVertex = next_vertex
            self.canvas.coords(self.LiveArrow1, x, y, x, y)
            return
            if self.state == 'dragging_state':
                try:
                    self.end_dragging_state()
                except ValueError:
                    self.alert()

    def double_click(self, event):
        """
        Event handler for mouse double-clicks.
        """
        if self.style_var.get() == 'smooth':
            return
        else:
            if self.lock_var.get():
                return
                x = x1 = self.canvas.canvasx(event.x)
                y = y1 = self.canvas.canvasy(event.y)
                self.clear_text()
                vertex = Vertex(x, y, (self.canvas), style='hidden')
                if self.state == 'dragging_state':
                    try:
                        self.end_dragging_state()
                    except ValueError:
                        self.alert()
                        return
                    else:
                        if vertex in [v for v in self.Vertices if v.is_endpoint()]:
                            vertex.erase()
                            vertex = self.Vertices[self.Vertices.index(vertex)]
                            x0, y0 = x1, y1 = vertex.point()
                            if vertex.out_arrow:
                                self.update_crosspoints()
                                vertex.reverse_path()
            elif vertex in self.Vertices:
                cut_vertex = self.Vertices[self.Vertices.index(vertex)]
                cut_vertex.recolor_incoming(palette=(self.palette))
                cut_arrow = cut_vertex.in_arrow
                cut_vertex.in_arrow = None
                vertex = cut_arrow.start
                x1, y1 = cut_vertex.point()
                cut_arrow.freeze()
            self.ActiveVertex = vertex
            self.goto_drawing_state(x1, y1)
            return
        if self.state == 'drawing_state':
            dead_arrow = self.ActiveVertex.out_arrow
            if dead_arrow:
                self.destroy_arrow(dead_arrow)
            self.goto_start_state()

    def set_start_cursor(self, x, y):
        point = Vertex(x, y, (self.canvas), style='hidden')
        if self.shift_down:
            if point in self.CrossPoints:
                self.canvas.config(cursor='dot')
            else:
                self.canvas.config(cursor='')
        elif self.lock_var.get():
            if point in self.Vertices:
                self.flipcheck = None
                self.canvas.config(cursor=open_hand_cursor)
            else:
                self.canvas.config(cursor='')
        elif point in self.Vertices:
            self.flipcheck = None
            self.canvas.config(cursor=open_hand_cursor)
        elif point in self.CrossPoints:
            self.flipcheck = None
            self.canvas.config(cursor='exchange')
        elif self.cursor_on_arrow(point):
            now = time.time()
            if self.flipcheck is None:
                self.flipcheck = now
            elif now - self.flipcheck > 0.5:
                self.canvas.config(cursor='double_arrow')
        else:
            self.flipcheck = None
            self.canvas.config(cursor='')

    def mouse_moved(self, event):
        """
        Handler for mouse motion events.
        """
        if self.style_var.get() == 'smooth':
            return
        else:
            canvas = self.canvas
            X, Y = event.x, event.y
            x, y = canvas.canvasx(X), canvas.canvasy(Y)
            self.cursorx, self.cursory = X, Y
            if self.state == 'start_state':
                self.set_start_cursor(x, y)
            elif self.state == 'drawing_state':
                x0, y0, x1, y1 = self.canvas.coords(self.LiveArrow1)
                self.canvas.coords(self.LiveArrow1, x0, y0, x, y)
            elif self.state == 'dragging_state':
                if self.shifting:
                    self.window.event_generate('<Return>')
                    return 'break'
                self.move_active(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

    def active_crossing_data(self):
        """
        Return the tuple of edges crossed by the in and out
        arrows of the active vertex.
        """
        assert self.ActiveVertex is not None
        active = self.ActiveVertex
        ignore = [active.in_arrow, active.out_arrow]
        return (
         self.crossed_arrows(active.in_arrow, ignore),
         self.crossed_arrows(active.out_arrow, ignore))

    def move_is_ok(self):
        return self.active_crossing_data() == self.saved_crossing_data

    def move_active(self, x, y):
        active = self.ActiveVertex
        if self.lock_var.get():
            x0, y0 = active.point()
            active.x, active.y = float(x), float(y)
            if self.move_is_ok():
                if not self.generic_vertex(active):
                    active.x, active.y = x0, y0
                    if self.cursor_attached:
                        self.detach_cursor('non-generic active vertex')
                else:
                    self.canvas.delete('lock_error')
                    delta = 6
                    self.canvas.create_oval((x0 - delta), (y0 - delta), (x0 + delta), (y0 + delta), outline='gray',
                      fill=None,
                      width=3,
                      tags='lock_error')
                    return
                    active.x, active.y = self.verify_drag() or x0, y0
                    if self.cursor_attached:
                        self.detach_cursor('non-generic diagram')
                    return
                if not self.cursor_attached:
                    self.attach_cursor('move is ok')
            else:
                if self.cursor_attached:
                    self.detach_cursor('bad move')
                active.x, active.y = x0, y0
                self.ActiveVertex.draw()
                return
                self.canvas.delete('lock_error')
        else:
            active.x, active.y = float(x), float(y)
        self.ActiveVertex.draw()
        if self.LiveArrow1:
            x0, y0, x1, y1 = self.canvas.coords(self.LiveArrow1)
            self.canvas.coords(self.LiveArrow1, x0, y0, x, y)
        if self.LiveArrow2:
            x0, y0, x1, y1 = self.canvas.coords(self.LiveArrow2)
            self.canvas.coords(self.LiveArrow2, x0, y0, x, y)
        self.update_smooth()
        self.update_info()
        self.window.update_idletasks()

    def attach_cursor(self, reason=''):
        self.cursor_attached = True
        self.ActiveVertex.set_delta(8)

    def detach_cursor(self, reason=''):
        self.cursor_attached = False
        self.ActiveVertex.set_delta(2)

    def _smooth_shift(self, key):
        try:
            ddx, ddy = vertex_shifts[key]
        except KeyError:
            return
        else:
            self.shifting = True
            dx, dy = self.shift_delta
            dx += ddx
            dy += ddy
            now = time.time()
            if now - self.shift_stamp < 0.1:
                self.shift_delta = (
                 dx, dy)
            else:
                self.cursorx = x = self.ActiveVertex.x + dx
                self.cursory = y = self.ActiveVertex.y + dy
                self.move_active(x, y)
                self.shift_delta = (0, 0)
                self.shift_stamp = now

    def clicked_on_arrow(self, vertex):
        for arrow in self.Arrows:
            if arrow.too_close(vertex):
                arrow.end.reverse_path(self.Crossings)
                self.update_info()
                return True

        return False

    def cursor_on_arrow(self, point):
        if self.lock_var.get():
            return False
        for arrow in self.Arrows:
            if arrow.too_close(point):
                return True

        return False

    def goto_start_state(self):
        self.canvas.delete('lock_error')
        self.canvas.delete(self.LiveArrow1)
        self.LiveArrow1 = None
        self.canvas.delete(self.LiveArrow2)
        self.LiveArrow2 = None
        self.ActiveVertex = None
        self.update_crosspoints()
        self.state = 'start_state'
        self.set_style()
        self.update_info()
        self.canvas.config(cursor='')

    def goto_drawing_state(self, x1, y1):
        self.ActiveVertex.expose()
        self.ActiveVertex.draw()
        x0, y0 = self.ActiveVertex.point()
        self.LiveArrow1 = self.canvas.create_line(x0, y0, x1, y1, fill='red')
        self.state = 'drawing_state'
        self.canvas.config(cursor='pencil')
        self.hide_DT()
        self.hide_labels()
        self.clear_text()

    def verify_drag(self):
        active = self.ActiveVertex
        active.update_arrows()
        self.update_crossings(active.in_arrow)
        self.update_crossings(active.out_arrow)
        self.update_crosspoints()
        return self.generic_arrow(active.in_arrow) and self.generic_arrow(active.out_arrow)

    def end_dragging_state(self):
        if not self.verify_drag():
            raise ValueError
        else:
            if self.lock_var.get():
                self.detach_cursor()
                self.saved_crossing_data = None
            else:
                x, y = float(self.cursorx), float(self.cursory)
                self.ActiveVertex.x, self.ActiveVertex.y = x, y
            endpoint = None
            if self.ActiveVertex.is_endpoint():
                other_ends = [v for v in self.Vertices if v.is_endpoint() if v is not self.ActiveVertex]
                if self.ActiveVertex in other_ends:
                    endpoint = other_ends[other_ends.index(self.ActiveVertex)]
                    self.ActiveVertex.swallow(endpoint, self.palette)
                    self.Vertices = [v for v in self.Vertices if v is not endpoint]
                self.update_crossings(self.ActiveVertex.in_arrow)
                self.update_crossings(self.ActiveVertex.out_arrow)
            if endpoint is None:
                if not self.generic_vertex(self.ActiveVertex):
                    raise ValueError
            self.ActiveVertex.expose()
            if self.style_var.get() != 'smooth':
                if self.ActiveVertex.in_arrow:
                    self.ActiveVertex.in_arrow.expose()
                if self.ActiveVertex.out_arrow:
                    self.ActiveVertex.out_arrow.expose()
        self.goto_start_state()

    def generic_vertex(self, vertex):
        if vertex in [v for v in self.Vertices if v is not vertex]:
            return False
        for arrow in self.Arrows:
            if arrow.too_close(vertex, tolerance=(Arrow.epsilon + 2)):
                return False

        return True

    def generic_arrow(self, arrow):
        if arrow == None:
            return True
        locked = self.lock_var.get()
        for vertex in self.Vertices:
            if arrow.too_close(vertex):
                if locked:
                    x, y, delta = vertex.x, vertex.y, 6
                    self.canvas.delete('lock_error')
                    self.canvas.create_oval((x - delta), (y - delta), (x + delta), (y + delta), outline='gray',
                      fill=None,
                      width=3,
                      tags='lock_error')
                return False

        for crossing in self.Crossings:
            point = self.CrossPoints[self.Crossings.index(crossing)]
            if arrow not in crossing:
                if arrow.too_close(point):
                    if locked:
                        x, y, delta = point.x, point.y, 6
                        self.canvas.delete('lock_error')
                        self.canvas.create_oval((x - delta), (y - delta), (x + delta), (y + delta), outline='gray',
                          fill=None,
                          width=3,
                          tags='lock_error')
                return False

        return True

    def destroy_arrow(self, arrow):
        self.Arrows.remove(arrow)
        if arrow.end:
            arrow.end.in_arrow = None
        if arrow.start:
            arrow.start.out_arrow = None
        arrow.erase()
        self.Crossings = [c for c in self.Crossings if arrow not in c]

    def update_crossings(self, this_arrow):
        """
        Redraw any arrows which were changed by moving this_arrow.
        """
        if this_arrow == None:
            return
        cross_list = [c for c in self.Crossings if this_arrow in c]
        damage_list = []
        find = lambda x: cross_list[cross_list.index(x)]
        for arrow in self.Arrows:
            if this_arrow == arrow:
                continue
            else:
                new_crossing = Crossing(this_arrow, arrow)
                new_crossing.locate()
                if new_crossing.x != None:
                    if new_crossing in cross_list:
                        find(new_crossing).locate()
                        continue
                    else:
                        self.Crossings.append(new_crossing)
            if new_crossing in self.Crossings:
                if arrow == find(new_crossing).under:
                    damage_list.append(arrow)
                self.Crossings.remove(new_crossing)

        for arrow in damage_list:
            arrow.draw(self.Crossings)

    def crossed_arrows(self, arrow, ignore_list=[]):
        """
        Return a tuple containing the arrows of the diagram which are
        crossed by the given arrow, in order along the given arrow.
        """
        if arrow is None:
            return tuple()
        arrow.vectorize()
        crosslist = []
        for n, diagram_arrow in enumerate(self.Arrows):
            if arrow == diagram_arrow or diagram_arrow in ignore_list:
                continue
            t = arrow ^ diagram_arrow
            if t is not None:
                crosslist.append((t, n))

        return tuple((n for _, n in sorted(crosslist)))