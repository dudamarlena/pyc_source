# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/editor.py
# Compiled at: 2011-12-19 10:45:34
import tyrs, urwid
from utils import encode, get_urls
try:
    from shorter.ur1ca import Ur1caUrlShorter
    from shorter.bitly import BitLyUrlShorter
    from shorter.msudpl import MsudplUrlShorter
    from shorter.custom import CustomUrlShorter
except ImportError:
    pass

try:
    from shorter.googl import GooglUrlShorter
except ImportError:
    pass

class TweetEditor(urwid.WidgetWrap):
    __metaclass__ = urwid.signals.MetaSignals
    signals = ['done']

    def __init__(self, init_content='', prompt=''):
        if init_content:
            init_content += ' '
        self.editor = Editor('%s (twice enter key to validate or esc) \n>> ' % prompt, init_content)
        self.counter = urwid.Text('0')
        self.editor.completion = tyrs.container['completion']
        w = urwid.Columns([('fixed', 4, self.counter), self.editor])
        urwid.connect_signal(self.editor, 'done', self.send_sigterm)
        urwid.connect_signal(self.editor, 'change', self.update_count)
        self.__super.__init__(w)

    def send_sigterm(self, content):
        urwid.emit_signal(self, 'done', content)

    def update_count(self, edit, new_edit_text):
        self.counter.set_text(str(len(new_edit_text)))


class Editor(urwid.Edit):
    __metaclass__ = urwid.signals.MetaSignals
    signals = ['done']
    last_key = ''

    def keypress(self, size, key):
        if key == 'enter' and self.last_key == 'enter':
            urwid.emit_signal(self, 'done', self.get_edit_text())
            return
        else:
            if key == 'esc':
                urwid.emit_signal(self, 'done', None)
            if key == 'tab':
                insert_text = self.completion.text_complete(self.get_edit_text())
                if insert_text:
                    self.insert_text(insert_text)
            self.last_key = key
            urwid.Edit.keypress(self, size, key)
            return