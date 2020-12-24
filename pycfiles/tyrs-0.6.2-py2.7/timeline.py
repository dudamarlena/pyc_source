# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/timeline.py
# Compiled at: 2011-12-22 09:19:04
import urwid
from widget import StatusWidget
from filter import FilterStatus

class Timeline(object):

    def __init__(self, buffer):
        self.cleared = False
        self.buffer = buffer
        self.walker = []
        self.unread = 0
        self.count = 0
        self.last_read = 0
        self.page = 1
        self.filter = FilterStatus()
        self.timeline = urwid.ListBox(urwid.SimpleListWalker([]))

    def append_new_statuses(self, retreive):
        retreive = self.filter_statuses(retreive)
        if retreive:
            self.last_read = retreive[0].id
            if len(self.walker) == 0 and not self.cleared:
                self.build_new_walker(retreive)
            else:
                self.add_to_walker(retreive)
            self.add_waterline()

    def add_to_walker(self, retreive):
        size = self.interface.loop.screen_size
        on_top = 'top' in self.timeline.ends_visible(size)
        focus_status, pos = self.walker.get_focus()
        for i, status in enumerate(retreive):
            if status.id == self.cleared:
                return
            while status.id != self.walker[(0 + i)].id:
                self.walker.insert(i, StatusWidget(status.id, status))
                if on_top:
                    self.timeline.set_focus(0)
                    self.timeline.set_focus(pos + i + 1)

            self.timeline.set_focus(pos)
            self.walker[i] = StatusWidget(status.id, status)

    def add_waterline(self):
        if self.buffer == 'home' and self.walker[0].id != None:
            div = urwid.Divider('-')
            div.id = None
            self.walker.insert(self.find_waterline(), div)
        return

    def build_new_walker(self, retreive):
        items = []
        for i, status in enumerate(retreive):
            items.append(StatusWidget(status.id, status))
            self.walker = urwid.SimpleListWalker(items)
            self.timeline = urwid.ListBox(self.walker)
            import tyrs
            self.interface = tyrs.container['interface']
            urwid.connect_signal(self.walker, 'modified', self.interface.lazzy_load)

    def find_waterline(self):
        for i, v in enumerate(self.walker):
            if str(v.id) == self.interface.last_read_home:
                return i

        return 0

    def filter_statuses(self, statuses):
        filters = []
        for i, status in enumerate(statuses):
            if self.filter.filter_status(status):
                filters.append(i)

        filters.reverse()
        for f in filters:
            del statuses[f]

        return statuses

    def update_counter(self):
        self.count_statuses()
        self.count_unread()

    def append_old_statuses(self, statuses):
        if statuses == []:
            pass
        else:
            items = []
            for status in statuses:
                items.append(StatusWidget(status.id, status))

            self.walker.extend(items)
            self.count_statuses()
            self.count_unread()

    def count_statuses(self):
        try:
            self.count = len(self.walker)
        except TypeError:
            self.count = 0

    def count_unread(self):
        try:
            self.unread = 0
            for i in range(len(self.walker)):
                if self.walker[i].id == self.last_read:
                    break
                self.unread += 1

        except TypeError:
            self.unread = 0

    def reset(self):
        self.first = 0
        self.unread = 0

    def clear(self):
        urwid.disconnect_signal(self.walker, 'modified', self.interface.lazzy_load)
        while len(self.walker) > 1:
            pop = self.walker.pop()
            self.cleared = pop.id

        if self.cleared == None:
            self.cleared = True
        return

    def empty(self):
        self.__init__()

    def all_read(self):
        if self.count > 0:
            self.last_read = self.walker[0].id

    def go_up(self):
        focus_status, pos = self.walker.get_focus()
        if pos > 0:
            self.timeline.set_focus(pos - 1)

    def go_down(self):
        focus_status, pos = self.walker.get_focus()
        self.timeline.set_focus(pos + 1)