# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/user.py
# Compiled at: 2011-11-24 12:19:44
import tyrs, curses
from utils import encode

class User(object):

    def __init__(self, user):
        self.interface = tyrs.container['interface']
        self.user = user
        self.interface.refresh_token = True
        self._init_screen()
        self._display_header()
        self._display_info()
        self.screen.getch()
        self.screen.erase()
        self.interface.refresh_token = False

    def _init_screen(self):
        maxyx = self.interface.screen.getmaxyx()
        self.screen = self.interface.screen.subwin(30, 80, 3, 10)
        self.screen.border(0)
        self.screen.refresh()

    def _display_header(self):
        self.screen.addstr(2, 10, '%s -- %s' % (self.user.screen_name,
         encode(self.user.name)))

    def _display_info(self):
        info = {'location': encode(self.user.location), 
           'description': encode(self.user.description), 
           'url': encode(self.user.url), 
           'time zone': encode(self.user.time_zone), 
           'status': self.user.status, 
           'friends': self.user.friends_count, 
           'follower': self.user.followers_count, 
           'tweets': self.user.statuses_count, 
           'verified': self.user.verified, 
           'created at': self.user.created_at}
        i = 0
        for item in info:
            self.screen.addstr(4 + i, 5, '%s' % item)
            self.screen.addstr(4 + i, 20, '%s' % info[item])
            i += 1