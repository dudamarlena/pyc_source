# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/ttkwidgets/messagedialog.py
# Compiled at: 2019-09-09 02:52:13
# Size of source mod 2**32: 1096 bytes
from noval import _
from tkinter import ttk
import noval.ui_base as ui_base, noval.editor.text as texteditor, noval.ttkwidgets.textframe as textframe, noval.consts as consts

class ScrolledMessageDialog(ui_base.CommonModaldialog):
    __doc__ = 'description of class'

    def __init__(self, parent, title, content):
        """
        Initializes the feedback dialog.
        """
        ui_base.CommonModaldialog.__init__(self, parent)
        self.title(title)
        text_frame = textframe.TextFrame(self.main_frame, read_only=True, borderwidth=1, relief='solid', text_class=texteditor.TextCtrl)
        text_frame.text.set_content(content)
        text_frame.pack(fill='both', expand=1)
        row = ttk.Frame(self.main_frame)
        self.ok_button = ttk.Button(row, text=_('&OK'), command=self._ok, default='active')
        self.ok_button.pack(pady=consts.DEFAUT_HALF_CONTRL_PAD_Y)
        row.pack(fill='x', expand=1)
        self.ok_button.focus_set()
        self.ok_button.bind('<Return>', self._ok, True)
        self.FormatTkButtonText(self.ok_button)