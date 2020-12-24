# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mop/dialogs.py
# Compiled at: 2020-04-05 20:53:54
# Size of source mod 2**32: 4526 bytes
from sys import version_info as python_version_info
from eyed3 import version as eyeD3_version
from gi import version_info as gtk_version_info
from eyed3.id3 import ID3_V1_0, ID3_V1_1, ID3_V2_3, ID3_V2_4, ID3_ANY_VERSION, versionToString
from pathlib import Path
from gi.repository import Gtk
from .config import getConfig

class Dialog:

    def __init__(self, dialog_name):
        builder = Gtk.Builder()
        builder.add_from_file(str(Path(__file__).parent / 'dialogs.ui'))
        self._dialog = builder.get_object(dialog_name)
        if self._dialog is None:
            raise ValueError(f"Dialog not found: {dialog_name}")
        self._builder = builder

    def run--- This code section failed: ---

 L.  20         0  SETUP_FINALLY        20  'to 20'

 L.  21         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _dialog
                6  LOAD_METHOD              run
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'resp'

 L.  22        12  LOAD_FAST                'resp'
               14  POP_BLOCK        
               16  CALL_FINALLY         20  'to 20'
               18  RETURN_VALUE     
             20_0  COME_FROM            16  '16'
             20_1  COME_FROM_FINALLY     0  '0'

 L.  24        20  LOAD_FAST                'destroy'
               22  POP_JUMP_IF_FALSE    34  'to 34'

 L.  25        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _dialog
               28  LOAD_METHOD              destroy
               30  CALL_METHOD_0         0  ''
               32  POP_TOP          
             34_0  COME_FROM            22  '22'
               34  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 16


class FileSaveDialog(Dialog):

    def __init__(self):
        super().__init__('file_save_dialog')
        pref_version = getConfig().preferred_id3_version or ID3_ANY_VERSION
        if pref_version == ID3_ANY_VERSION:
            active_version = 'vCurrent'
        else:
            active_version = versionToString(pref_version).replace('.', '')
        self._builder.get_object(f"{active_version}_radiobutton").set_active(True)

    def run(self):
        resp = super().run()
        options = dict(version=None, save_all=False)
        for label, version in (('vCurrent', None),
         (
          'v24', ID3_V2_4), ('v23', ID3_V2_3),
         (
          'v11', ID3_V1_1), ('v10', ID3_V1_0)):
            if self._builder.get_object(f"{label}_radiobutton").get_active():
                options['version'] = version
                break
            return (resp, options)


class AboutDialog(Gtk.AboutDialog):

    def __init__(self, *args, **kwargs):
        from .__about__ import project_name, version, author, author_email, years, release_name
        (super().__init__)(*args, **kwargs)
        self.set_program_name(project_name)
        version_str = version
        if release_name:
            version_str += f" ({release_name})"
        self.set_version(version_str)
        self.set_authors([f"{author} <{author_email}>"])
        self.set_license_type(Gtk.License.GPL_3_0_ONLY)
        self.set_copyright(f"Copyright © {author}, {years}")

        def versionInfoToString(info):
            return '.'.join([str(x) for x in info])

        self.set_comments(f"Running with Python {versionInfoToString(python_version_info[:3])}, GTK+ {versionInfoToString(gtk_version_info)}, and eyeD3 {eyeD3_version}")
        self.set_website_label('GitHub')
        self.set_website('https://github.com/nicfit/mop')


class FileChooserDialog(Dialog):

    def __init__(self, parent):
        super().__init__('file_chooser_dialog')
        self._dialog.set_parent(parent)
        for radiobutton in ('file_chooser_open_dirs_radiobutton', 'file_chooser_open_files_radiobutton'):
            self._builder.get_object(radiobutton).connect('toggled', self._onActionChange)
        else:
            self._builder.get_object('file_chooser_open_dirs_radiobutton').toggled()
            self._dialog.set_select_multiple(True)

    def _onActionChange(self, radiobutton):
        if radiobutton.get_active():
            if '_dirs_' in radiobutton.get_name():
                self._dialog.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
                for flt in self._dialog.list_filters():
                    self._dialog.remove_filter(flt)

            else:
                self._dialog.set_action(Gtk.FileChooserAction.OPEN)
                audio_filter = Gtk.FileFilter()
                audio_filter.set_name('Audio Files')
                audio_filter.add_pattern('*.mp3')
                self._dialog.set_filter(audio_filter)

    def run--- This code section failed: ---

 L. 115         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                run
                6  LOAD_CONST               False
                8  LOAD_CONST               ('destroy',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  STORE_FAST               'resp'

 L. 116        14  SETUP_FINALLY        54  'to 54'

 L. 117        16  LOAD_FAST                'resp'
               18  LOAD_GLOBAL              Gtk
               20  LOAD_ATTR                ResponseType
               22  LOAD_ATTR                CANCEL
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 118        28  POP_BLOCK        
               30  CALL_FINALLY         54  'to 54'
               32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM            26  '26'

 L. 120        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _dialog
               40  LOAD_METHOD              get_filenames
               42  CALL_METHOD_0         0  ''
               44  POP_BLOCK        
               46  CALL_FINALLY         54  'to 54'
               48  RETURN_VALUE     
               50  POP_BLOCK        
               52  BEGIN_FINALLY    
             54_0  COME_FROM            46  '46'
             54_1  COME_FROM            30  '30'
             54_2  COME_FROM_FINALLY    14  '14'

 L. 122        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _dialog
               58  LOAD_METHOD              destroy
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          
               64  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 30


class NothingToDoDialog(Dialog):

    def __init__(self):
        super().__init__('nothing_to_do_dialog')