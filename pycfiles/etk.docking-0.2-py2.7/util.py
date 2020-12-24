# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/etk/docking/util.py
# Compiled at: 2011-01-15 06:50:51
import gtk

def rect_contains(rect, x, y):
    """
    The rect_contains function checks if a point, defined by x and y falls
    within the gdk.Rectangle defined by rect.

    Note: Unlike rect_overlaps defined below, this function ignores a 1 pixel border.
    """
    if x > rect.x and x < rect.x + rect.width and y > rect.y and y < rect.y + rect.height:
        return True
    else:
        return False


def rect_overlaps(rect, x, y):
    """
    The rect_overlaps function checks if a point, defined by x and y overlaps
    the gdk.Rectangle defined by rect.

    Note: Unlike rect_contains defined above, this function does not ignore a 1 pixel border.
    """
    if x >= rect.x and x <= rect.x + rect.width and y >= rect.y and y <= rect.y + rect.height:
        return True
    else:
        return False


def load_icon(icon_name, size):
    icontheme = gtk.icon_theme_get_default()
    if not icontheme.has_icon(icon_name):
        icon_name = 'gtk-missing-image'
    return icontheme.load_icon(icon_name, size, gtk.ICON_LOOKUP_USE_BUILTIN)


def load_icon_image(icon_name, size):
    icontheme = gtk.icon_theme_get_default()
    if not icontheme.has_icon(icon_name):
        icon_name = 'gtk-missing-image'
    return gtk.image_new_from_icon_name(icon_name, size)


def flatten(w, child_getter=gtk.Container.get_children):
    """
    Generator function that returns all items in a hierarchy.
    Default `child_getter` returns children in a GTK+ widget hierarchy.
    """
    yield w
    try:
        for c in child_getter(w):
            for d in flatten(c, child_getter):
                yield d

    except TypeError:
        pass