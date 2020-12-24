# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/custom_file_editor.py
# Compiled at: 2015-04-07 15:45:59
__doc__ = ' Defines file editors for the wxPython user interface toolkit.\n'
import os
from traits.trait_base import ETSConfig
_tk = ETSConfig.toolkit
if _tk in ('null', '', None):
    _tk = os.environ['ETS_TOOLKIT']
else:
    print _tk
from functools import partial
from traits.api import File, HasTraits, Button, Instance, Any, Callable, Property, Directory, Bool
from traitsui.api import View, Item, CustomEditor, Handler, UIInfo
from traitsui.file_dialog import open_file
CustomEditorKlass = __import__('traitsui.%s.custom_editor' % _tk, fromlist=[
 'CustomEditor']).CustomEditor
from directory_dialog import open_directory

def mkeditor(*args, **kwargs):
    """ Custom editor factory.  Must be instantiated on top of an
        InteractiveSubwindow instance with an implemented reconstruct().
    """
    return getattr(__import__('custom_file_editor'), '%s_editor_factory' % _tk)(*args, **kwargs)


def wx_editor_factory(parent, editor, use_dir=False, *args):
    import wx
    from traitsui.wx.helper import TraitsUIPanel
    editor.control = panel = TraitsUIPanel(parent, -1)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    editor.use_dir = use_dir
    pad = 8
    bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, size=(15, 15))
    button = wx.BitmapButton(panel, -1, bitmap=bmp)
    editor.text_control = text_control = wx.TextCtrl(panel, -1, '', style=wx.TE_PROCESS_ENTER)
    _do_update_obj = lambda ev: update_file_obj(editor)
    wx.EVT_TEXT_ENTER(panel, text_control.GetId(), _do_update_obj)
    wx.EVT_KILL_FOCUS(text_control, _do_update_obj)
    sizer.Add(text_control, 1, wx.EXPAND | wx.ALIGN_CENTER)
    sizer.Add(button, 0, wx.RIGHT | wx.ALIGN_CENTER, pad)
    wx.EVT_BUTTON(panel, button.GetId(), lambda ev: button_click(editor))
    panel.SetSizerAndFit(sizer)
    return panel


def qt4_editor_factory(parent, editor, use_dir=False, *args):
    from pyface.qt import QtCore, QtGui
    from traitsui.qt4.helper import IconButton
    editor.control = panel = QtGui.QWidget()
    layout = QtGui.QHBoxLayout(panel)
    layout.setContentsMargins(0, 0, 0, 0)
    editor.use_dir = use_dir
    editor.text_control = text_control = QtGui.QLineEdit()
    layout.addWidget(text_control)
    signal = QtCore.SIGNAL('editingFinished()')
    QtCore.QObject.connect(text_control, signal, lambda : update_file_obj(editor))
    button = IconButton(QtGui.QStyle.SP_DirIcon, lambda : button_click(editor))
    layout.addWidget(button)
    return panel


def get_text(editor):
    if _tk == 'wx':
        return editor.text_control.GetValue()
    if _tk == 'qt4':
        return editor.text_control.text()
    raise NotImplementedError('Attempted to get text from nonexistent editor type')


def set_text(editor, text):
    if _tk == 'wx':
        return editor.text_control.SetValue(text)
    if _tk == 'qt4':
        return editor.text_control.setText(text)
    raise NotImplementedError('Attempted to set text in nonexistent editor type')


def update_file_obj(editor):
    editor.value = get_text(editor)


def button_click(editor):
    if editor.use_dir:
        file_selected = open_directory(entries=20)
    else:
        file_selected = open_file(entries=20)
    if file_selected:
        editor.value = file_selected
    editor.ui.handler.reconstruct()


if _tk == 'wx':

    class CustomFileEditor(CustomEditor):
        """abstraction layer for Custom File editor.  This editor must be
        instantiated within a view of an InteractiveSubwindow object with a
        correctly implemented reconstruct()"""
        factory = Property
        use_dir = Bool(False)

        def _get_klass(self):
            return CustomFileEditorKlass

        def _get_factory(self):
            return partial(mkeditor, use_dir=self.use_dir)


    class CustomDirectoryEditor(CustomFileEditor):
        use_dir = True


elif _tk == 'qt4':
    from traitsui.editors.file_editor import FileEditor as CustomFileEditor
    from traitsui.editors.directory_editor import DirectoryEditor as CustomDirectoryEditor
else:
    raise NotImplementedError('No CustomFileEditor defined for nonexistent toolkit')

class CustomFileEditorKlass(CustomEditorKlass):
    text_control = Any
    use_dir = Bool(False)

    def update_editor(self):
        set_text(self, self.value)

    def update_file_obj(self, event):
        self.value = get_text(self)


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    class Farkish(Handler):
        f = File('saukish')
        b = Button
        info = Instance(UIInfo)
        traits_view = View(Item('f', editor=CustomFileEditor()), Item('b'), height=500, width=500)

        def _b_fired(self):
            print self.f

        def init_info(self, info):
            self.info = info

        def reconstruct(self):
            self.info.ui.dispose()
            self.info.object.edit_traits()


    Farkish().configure_traits()