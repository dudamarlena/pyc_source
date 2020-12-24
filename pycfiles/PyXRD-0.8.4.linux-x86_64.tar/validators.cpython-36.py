# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/views/validators.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2230 bytes
from mvc.support.gui_loop import add_idle_call

class FloatEntryValidator:

    def __init__(self, entry):
        self.last_valid_val = 0
        self.has_valid_val = True
        self.entry = entry
        self.entry.connect('activate', self.entry_activate)
        self.entry.connect('focus_out_event', self.entry_focus_out)
        self.insert_handlerid = self.entry.connect('insert-text', self.entry_insert_text)
        self.delete_handlerid = self.entry.connect('delete-text', self.entry_delete_text)

    def validate(self, text=None, reset_if_invalid=False):
        text = text or self.entry.get_chars(0, -1)
        try:
            self.last_valid_val = float(text)
            self.has_valid_val = True
        except Exception as e:
            self.has_valid_val = False

        if reset_if_invalid:
            if not self.has_valid_val:
                self.entry.handler_block(self.insert_handlerid)
                self.entry.set_text('%f' % self.last_valid_val)
                self.has_valid_val = True
                self.entry.handler_unblock(self.insert_handlerid)

    def entry_activate(self, entry):
        self.validate(reset_if_invalid=True)

    def entry_focus_out(self, entry, event):
        self.validate(reset_if_invalid=True)
        return False

    def entry_insert_text(self, entry, new_text, new_text_length, position):
        self.entry.stop_emission('insert-text')
        self.entry.handler_block(self.insert_handlerid)
        pos = self.entry.get_position()
        text = self.entry.get_chars(0, -1)
        old_text = text
        text = text[:pos] + new_text + text[pos:]
        self.validate(text)
        if self.has_valid_val:
            new_text = text
            self.entry.set_text(new_text)
            add_idle_call(lambda : self.entry.set_position(pos + (len(new_text) - len(old_text))))
        self.entry.handler_unblock(self.insert_handlerid)

    def entry_delete_text(self, entry, start, end):
        self.validate()