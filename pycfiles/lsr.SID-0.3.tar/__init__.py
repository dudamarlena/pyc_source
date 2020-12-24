# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Desktop/PySID/pysidmodules/starscale/__init__.py
# Compiled at: 2010-10-13 05:34:12
import gtk, gobject
from gtk import gdk
import pygtk, os
BORDER_WIDTH = 10

class StarScale(gtk.Widget):
    """A horizontal StarScale widget.
    
    Emits: 'rating-changed' and 'rating_changing'
    """

    def __init__(self, max_stars=5, stars=0, overlap=False, image_width=None, half=False):
        """Create a StarScale widget.
        
        max_stars is the maximum number of stars possible,
        stars are the stars checked at the beginning, 
        overlap allows the stars to overlap a bit - so more stars fit on the widgets space,
        image_width forces the given star-dimensions and prevents them from being resized,
        half determines if only full stars can be checked (excludes overlap)
        """
        if half:
            overlap = False
        gtk.Widget.__init__(self)
        if image_width is None:
            self.force_width = False
            self.image_width = 25
        else:
            self.image_width = image_width
            self.force_width = True
        self.overlap = overlap
        self.half = half
        self.max_stars = max_stars
        self.stars = stars
        self._calculate_values()
        return

    def _calculate_values(self):
        """Collects some basic information"""
        self.x_positions = []
        if self.overlap:
            for count in range(0, self.max_stars):
                self.x_positions.append(count * (self.image_width / 2) + BORDER_WIDTH)

        else:
            for count in range(0, self.max_stars):
                self.x_positions.append(count * self.image_width + BORDER_WIDTH)

            self.virtual_width = []
            if self.half:
                for count in range(0, self.max_stars * 2):
                    self.virtual_width.append(count * self.image_width / 2 + BORDER_WIDTH)

            elif self.overlap:
                for count in range(0, self.max_stars):
                    self.virtual_width.append(count * self.image_width / 2 + BORDER_WIDTH)

        for count in range(0, self.max_stars):
            self.virtual_width.append(count * self.image_width + BORDER_WIDTH)

    def redraw_stars(self, numstars):
        """ Clears the GC and draws all the stars"""
        y = (self.allocation.height - self.image_width) / 2
        x = (self.allocation.width - (self.x_positions[(-1)] + self.image_width + BORDER_WIDTH)) / 2
        self.window.draw_rectangle(self.get_style().bg_gc[gtk.STATE_NORMAL], True, 0, 0, self.allocation.width, self.allocation.height)
        if not self.half:
            for count in range(0, numstars):
                self.window.draw_pixbuf(self.gc, self.pbRed, 0, 0, x + self.x_positions[count], y, -1, -1)

            for count in range(numstars, self.max_stars):
                self.window.draw_pixbuf(self.gc, self.pbGrey, 0, 0, x + self.x_positions[count], y, -1, -1)

        else:
            full = numstars // 2
            half = True if numstars % 2 > 0 else False
            empty = full if not half else full + 1
        for count in range(0, full):
            self.window.draw_pixbuf(self.gc, self.pbRed, 0, 0, x + self.x_positions[count], y, -1, -1)

        if half:
            self.window.draw_pixbuf(self.gc, self.pbRedHalf, 0, 0, x + self.x_positions[full], y, -1, -1)
        for count in range(empty, self.max_stars):
            self.window.draw_pixbuf(self.gc, self.pbGrey, 0, 0, x + self.x_positions[count], y, -1, -1)

    def check_for_new_stars(self, xPos, clicked=False, just_show=False):
        """Depending on the given x-coord this routine decides how many stars are 'checked' """
        x = (self.allocation.width - (self.x_positions[(-1)] + self.image_width + BORDER_WIDTH)) / 2
        xPos -= x
        new_stars = len([ l for l in self.virtual_width if l < xPos ])
        if clicked:
            if self.get_value() == new_stars:
                self.set_value(self.get_value() - 1)
                return
        if just_show:
            self.redraw_stars(new_stars)
        else:
            self.set_value(new_stars)

    def set_value(self, value):
        """Sets the current number of stars that will be 
        drawn.  If the number is different then the current
        number the widget will be redrawn"""
        if value >= 0:
            if self.stars != value:
                self.stars = value
                if self.half and self.stars > self.max_stars * 2:
                    self.stars = self.max_stars * 2
                elif not self.half and self.stars > self.max_stars:
                    self.stars = self.max_stars
                self.window.invalidate_rect(self.allocation, True)
                self.redraw_stars(self.stars)
                self.emit('rating-changing', self.stars)

    def get_value(self):
        """Get the current number of stars displayed"""
        return self.stars

    def set_max_value(self, max_value):
        """set the maximum number of stars"""
        if self.max_stars != max_value:
            if max_value > 0:
                self.max_stars = max_value
                self._calculate_values()
                if self.stars > self.max_stars:
                    self.set_value(self.max_stars)

    def get_max_value(self):
        """Get the maximum number of stars that can be shown"""
        return self.max_stars

    def load_files(self):
        yellow = os.path.join(os.path.dirname(__file__), 'star.svg')
        red = os.path.join(os.path.dirname(__file__), 'star_red.svg')
        red_half = os.path.join(os.path.dirname(__file__), 'star_half_red.svg')
        grey = os.path.join(os.path.dirname(__file__), 'star_grey.svg')
        self.pbYellow = gtk.gdk.pixbuf_new_from_file_at_size(yellow, self.image_width, self.image_width)
        self.pbRed = gtk.gdk.pixbuf_new_from_file_at_size(red, self.image_width, self.image_width)
        self.pbRedHalf = gtk.gdk.pixbuf_new_from_file_at_size(red_half, self.image_width, self.image_width)
        self.pbGrey = gtk.gdk.pixbuf_new_from_file_at_size(grey, self.image_width, self.image_width)

    def do_realize(self):
        """Called when the widget should create all of its 
        windowing resources."""
        self.set_flags(self.flags() | gtk.REALIZED)
        self.window = gtk.gdk.Window(self.get_parent_window(), width=self.allocation.width, height=self.allocation.height, window_type=gdk.WINDOW_CHILD, wclass=gdk.INPUT_OUTPUT, event_mask=self.get_events() | gtk.gdk.EXPOSURE_MASK | gtk.gdk.BUTTON1_MOTION_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.LEAVE_NOTIFY_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK)
        self.window.set_user_data(self)
        self.style.attach(self.window)
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)
        self.load_files()
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        self.connect('motion_notify_event', self.motion_notify_event)

    def do_unrealize(self):
        """The do_unrealized method is responsible for freeing the GDK resources
        De-associate the window we created in do_realize with ourselves"""
        self.window.destroy()

    def do_size_request(self, requisition):
        """From Widget.py: The do_size_request method Gtk+ is calling
         on a widget to ask it the widget how large it wishes to be. 
         It's not guaranteed that gtk+ will actually give this size 
         to the widget.  So we will send gtk+ the size needed for
         the maximum amount of stars"""
        height = self.get_parent().allocation.height
        if height < self.image_width:
            height = self.image_width
        requisition.height = height
        requisition.width = self.x_positions[(-1)] + self.image_width + BORDER_WIDTH

    def do_size_allocate(self, allocation):
        """The do_size_allocate is called by when the actual 
        size is known and the widget is told how much space 
        could actually be allocated Save the allocated space
        self.allocation = allocation."""
        self.allocation = allocation
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*allocation)
        if not self.force_width:
            m = self.max_stars / 2 if self.overlap else self.max_stars
            w = (allocation.width - BORDER_WIDTH * 2) / m
            h = allocation.height
            self.image_width = w if w < h else h
            self._calculate_values()
            self.load_files()
            if self.window:
                self.redraw_stars(self.stars)

    def do_expose_event(self, event):
        """Called when the widget needs to be redrawn."""
        self.redraw_stars(self.stars)

    def do_leave_notify_event(self, widget):
        """Called when the mouse leaves the widget region."""
        self.redraw_stars(self.stars)

    def motion_notify_event(self, widget, event):
        """Called when the mouse moves over the widget"""
        if event.is_hint:
            (x, y, state) = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state
        if state & gtk.gdk.BUTTON1_MASK:
            self.check_for_new_stars(event.x)
        else:
            self.check_for_new_stars(event.x, just_show=True)

    def do_button_press_event(self, event):
        """The button press event virtual method"""
        if event.button == 1:
            self.check_for_new_stars(event.x, clicked=True)
        return True

    def do_button_release_event(self, event):
        """The button release event virtual method"""
        self.emit('rating-changed', self.stars)


gobject.type_register(StarScale)
gobject.signal_new('rating-changed', StarScale, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_INT,))
gobject.signal_new('rating-changing', StarScale, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_INT,))
if __name__ == '__main__':
    win = gtk.Window()
    win.resize(400, 150)
    win.connect('delete-event', gtk.main_quit)
    vbox = gtk.VBox()
    win.add(vbox)
    vbox.pack_start(StarScale(10, 5, image_width=32), False, True)
    vbox.pack_start(StarScale(5, 5, half=True), False, True)
    vbox.pack_start(StarScale(10, 5, overlap=True), True, True)
    win.show_all()
    gtk.main()