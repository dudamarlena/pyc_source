# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyzima-spb/www-python/django-adminlte-full/demo/adminlte_full/menu.py
# Compiled at: 2016-06-11 14:38:39
# Size of source mod 2**32: 3408 bytes
import django.dispatch
from django.core.urlresolvers import reverse, resolve
from collections import OrderedDict

class MenuItem(object):
    COLOR_AQUA = 'aqua'
    COLOR_GREEN = 'green'
    COLOR_RED = 'red'
    COLOR_YELLOW = 'yellow'

    def __init__(self, uid, label, route, route_args=None, icon=False, badge=False, badge_color=None):
        self._MenuItem__active = False
        self._MenuItem__parent = None
        self._MenuItem__children = []
        self._MenuItem__route_args = route_args or {}
        self.uid = uid
        self.label = label
        self.route = route
        self.icon = icon
        self.badge = badge
        self.badge_color = badge_color or self.COLOR_GREEN

    @property
    def active(self):
        return self._MenuItem__active

    @active.setter
    def active(self, active):
        self._MenuItem__active = bool(active)
        if self.has_parent():
            self.parent.active = self.parent.has_active_child()

    def add_child(self, child):
        if isinstance(child, MenuItem):
            child.parent = self
            self._MenuItem__children.append(child)

    @property
    def children(self):
        return self._MenuItem__children

    @children.setter
    def children(self, children):
        for child in children:
            self.add_child(child)

    def has_active_child(self):
        for child in self.children:
            if child.is_active():
                return True

    def has_children(self):
        return bool(self.children)

    def has_parent(self):
        return isinstance(self.parent, MenuItem)

    def is_active(self):
        return bool(self.active)

    @property
    def parent(self):
        return self._MenuItem__parent

    @parent.setter
    def parent(self, parent):
        if isinstance(parent, MenuItem):
            self._MenuItem__parent = parent

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)

    @property
    def route_args(self):
        return self._MenuItem__route_args

    @route_args.setter
    def route_args(self, route_args):
        if isinstance(route_args, dict):
            self._MenuItem__route_args = route_args

    def url(self):
        if self.route is not None:
            return reverse(self.route, kwargs=self.route_args)
        return ''


class Menu(object):
    show_signal = django.dispatch.Signal()

    def __init__(self):
        self._Menu__items = OrderedDict()

    def __activate_by_path(self, path, items):
        for item in items:
            if item.has_children():
                self._Menu__activate_by_path(path, item.children)
            else:
                item.active = self._Menu__path_equals_route(path, item.route)

    def __path_equals_route(self, path, route):
        resolved = False
        try:
            resolved = resolve(path)
        except:
            pass

        return resolved and resolved.url_name == route

    def activate_by_context(self, context):
        self._Menu__activate_by_path(context.get('request').path, self.items.values())

    def add_item(self, item):
        if isinstance(item, MenuItem):
            self._Menu__items[item.uid] = item

    @property
    def items(self):
        return self._Menu__items

    @items.setter
    def items(self, items):
        for item in items:
            self.add_item(item)

    def root_item(self, uid):
        return self.items.get(uid)