# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/keys.py
# Compiled at: 2011-12-14 03:45:13
import tyrs, urwid
from help import Help
from utils import open_image

class Keys(object):
    __metaclass__ = urwid.signals.MetaSignals
    signals = ['help_done']

    def __init__(self):
        self.conf = tyrs.container['conf']
        self.interface = tyrs.container['interface']
        self.api = tyrs.container['api']

    def keystroke(self, ch):
        if not self.interface.help:
            if ch == self.conf.keys['quit']:
                self.interface.stoped = True
                raise urwid.ExitMainLoop()
            elif ch == self.conf.keys['right'] or ch == 'right':
                self.interface.navigate_buffer(+1)
            elif ch == self.conf.keys['left'] or ch == 'left':
                self.interface.navigate_buffer(-1)
            elif ch == self.conf.keys['up']:
                self.interface.go_up()
            elif ch == self.conf.keys['down']:
                self.interface.go_down()
            elif ch == self.conf.keys['update']:
                self.api.update_timeline(self.interface.buffer)
            elif ch == self.conf.keys['tweet']:
                self.interface.edit_status('tweet', prompt='Tweet ')
            elif ch == self.conf.keys['reply']:
                self.interface.reply()
            elif ch == self.conf.keys['retweet']:
                self.api.retweet()
            elif ch == self.conf.keys['retweet_and_edit']:
                self.api.retweet_and_edit()
            elif ch == self.conf.keys['delete']:
                self.api.destroy()
            elif ch == self.conf.keys['mentions']:
                self.interface.change_buffer('mentions')
            elif ch == self.conf.keys['home']:
                self.interface.change_buffer('home')
            elif ch == self.conf.keys['getDM']:
                self.interface.change_buffer('direct')
            elif ch == self.conf.keys['clear']:
                self.interface.clear_statuses()
            elif ch == self.conf.keys['follow_selected']:
                self.api.follow_selected()
            elif ch == self.conf.keys['unfollow_selected']:
                self.api.unfollow_selected()
            elif ch == self.conf.keys['follow']:
                self.interface.edit_status('follow', prompt='Follow')
            elif ch == self.conf.keys['unfollow']:
                self.interface.edit_status('unfollow', prompt='Unfollow ')
            elif ch == self.conf.keys['openurl']:
                self.interface.openurl()
            elif ch == self.conf.keys['search']:
                self.interface.edit_status('search', prompt='Search ')
            elif ch == self.conf.keys['search_user']:
                self.interface.edit_status('public', prompt='Nick ')
            elif ch == self.conf.keys['search_myself']:
                self.api.my_public_timeline()
            elif ch == self.conf.keys['search_current_user']:
                self.api.find_current_public_timeline()
            elif ch == self.conf.keys['fav']:
                self.api.set_favorite()
            elif ch == self.conf.keys['get_fav']:
                self.api.get_favorites()
            elif ch == self.conf.keys['delete_fav']:
                self.api.destroy_favorite()
            elif ch == self.conf.keys['thread']:
                self.api.get_thread()
            elif ch == self.conf.keys['open_image']:
                open_image(self.interface.current_status().user)
            elif ch == 'i':
                self.interface.current_user_info()
            elif ch == self.conf.keys['waterline']:
                self.interface.update_last_read_home()
            elif ch == self.conf.keys['back_on_top']:
                self.interface.back_on_top()
            elif ch == self.conf.keys['back_on_bottom']:
                self.interface.back_on_bottom()
            elif ch == '?':
                self.interface.display_help()
            self.interface.display_timeline()
        elif ch in ('q', 'Q', 'esc'):
            urwid.emit_signal(self, 'help_done')