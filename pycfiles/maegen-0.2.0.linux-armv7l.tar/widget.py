# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/maegen/gui/gtk/widget.py
# Compiled at: 2011-11-28 15:24:33
"""
Created on Nov 27, 2011

@author: maemo
"""
import logging, gtk
from gtk import gdk
import pango
from maegen.gui.gtk.utils import get_gender_pixbuf, get_life_date_str
from maegen.common import version
version.getInstance().submitRevision('$Revision: 79 $')

class GenTree(gtk.DrawingArea):
    """
    This widget display a genealogical tree given a root individual
    """

    def __init__(self, zcore, individual, show_spouse=False):
        gtk.DrawingArea.__init__(self)
        self.root = individual
        self.zcore = zcore
        self.show_spouse = show_spouse
        self.WIDTH_FOR_INDI = 150
        self.HORIZONTAL_SPACE = 50
        self.HEIGHT_FOR_INDI = 70
        self.VERTICAL_SPACE = 100
        self.drawing_area = self
        self.real_width = self.compute_width()
        self.drawing_area_width = max([800, self.real_width])
        self.real_height = self.compute_height()
        self.drawing_area_height = max([400, self.real_height])
        self.drawing_area.set_size_request(self.drawing_area_width + 1, self.drawing_area_height + 1)
        self.pangolayout_name = self.drawing_area.create_pango_layout('')
        self.pangolayout_life = self.drawing_area.create_pango_layout('')
        self.drawing_area.connect('expose-event', self.area_expose_cb)

    def draw_individual(self, indi, x, y):
        """
        Parameter:
            - indi: the individual
            - x,y : the center top of the individual node
        """
        top_left = (
         x - self.WIDTH_FOR_INDI / 2, y)
        self.pangolayout_name.set_text(str(indi))
        self.drawing_area.window.draw_layout(self.gc, top_left[0] + 1, top_left[1] + 1, self.pangolayout_name)
        pixbuf = get_gender_pixbuf(indi)
        if pixbuf:
            pixbuf.render_to_drawable(self.drawing_area.window, self.gc, 0, 0, top_left[0], top_left[1] + 1 + self.HEIGHT_FOR_INDI / 2, -1, -1)
            IMAGE_WIDTH = 13
            IMAGE_HEIGTH = 13
        life_str = get_life_date_str(indi)
        self.pangolayout_life.set_text(life_str)
        attrs = pango.AttrList()
        attrs.insert(pango.AttrScale(pango.SCALE_X_SMALL, 0, len(life_str)))
        self.pangolayout_life.set_attributes(attrs)
        self.drawing_area.window.draw_layout(self.gc, x, top_left[1] + 1 + self.HEIGHT_FOR_INDI / 2, self.pangolayout_life)

    def area_expose_cb(self, area, event):
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        self.draw_tree(self.root, 0, self.drawing_area_width, 0)

    def size_for_individual(self, indi):
        """
        Compute the width of the tree with the given individual as root
        """
        logging.debug('compute size required by ' + str(indi))
        n = self.zcore.children_count(indi)
        if n == 0:
            logging.debug('No child')
            resu = self.WIDTH_FOR_INDI
        else:
            logging.debug('has child, include children size')
            resu = 0
            for child in self.zcore.retrieve_children(indi):
                logging.debug('child ' + str(child) + '...')
                resu += self.size_for_individual(child)

            resu += (n - 1) * self.HORIZONTAL_SPACE
            logging.debug('adjusted size become ' + str(resu))
        logging.debug('size required by ' + str(indi) + ' is ' + str(resu))
        return resu

    def draw_tree(self, individual, left_corner_x, right_corner_x, top_y):
        """
        Draw the individual tree inside the given windows on the drawing area
        Return the x position of the individual node
        """
        children = self.zcore.retrieve_children(individual)
        if len(children) == 0:
            resu = left_corner_x + self.WIDTH_FOR_INDI / 2
            self.draw_individual(individual, resu, top_y)
        else:
            row_left_x = None
            row_right_x = None
            child_left_corner_x = left_corner_x
            top_y_for_child = top_y + self.HEIGHT_FOR_INDI + self.VERTICAL_SPACE
            y_for_horiz_row = top_y_for_child - self.VERTICAL_SPACE / 2
            for child in children:
                size_for_child = self.size_for_individual(child)
                child_right_corner_x = child_left_corner_x + size_for_child
                x = self.draw_tree(child, child_left_corner_x, child_right_corner_x, top_y_for_child)
                self.drawing_area.window.draw_line(self.gc, x, top_y_for_child, x, y_for_horiz_row)
                if row_left_x is None:
                    row_left_x = x
                    row_right_x = x
                else:
                    row_right_x = x
                child_left_corner_x += size_for_child + self.HORIZONTAL_SPACE

            self.drawing_area.window.draw_line(self.gc, row_left_x, y_for_horiz_row, row_right_x, y_for_horiz_row)
            resu = (row_left_x + row_right_x) / 2
            self.drawing_area.window.draw_line(self.gc, resu, y_for_horiz_row, resu, y_for_horiz_row - self.VERTICAL_SPACE / 2)
            self.draw_individual(individual, resu, top_y)
        return resu

    def compute_width(self):
        return self.size_for_individual(self.root)

    def compute_height(self):

        def depth_for_individual(indi):
            if self.zcore.children_count(indi) == 0:
                return 1
            else:
                depth_of_children = map(depth_for_individual, self.zcore.retrieve_children(indi))
                depth_from_indi = map(lambda child_depth: child_depth + 1, depth_of_children)
                return max(depth_from_indi)

        depth = depth_for_individual(self.root)
        return depth * self.HEIGHT_FOR_INDI + (depth - 1) * self.VERTICAL_SPACE