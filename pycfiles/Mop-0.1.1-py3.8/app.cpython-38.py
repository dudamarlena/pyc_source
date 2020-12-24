# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mop/app.py
# Compiled at: 2020-04-05 20:53:54
# Size of source mod 2**32: 8952 bytes
import logging
from pathlib import Path
from gi.repository import Gtk
from eyed3.utils import formatTime, formatSize
from .config import getState
from .utils import eyed3_load, eyed3_load_dir
from .dialogs import Dialog, FileSaveDialog, AboutDialog, FileChooserDialog, NothingToDoDialog
from .editorctl import EditorControl
from .filesctl import FileListControl
log = logging.getLogger(__name__)
logging.getLogger('eyed3').setLevel(logging.ERROR)

class MopApp:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file(str(Path(__file__).parent / 'mop.ui'))
        self._builder = builder
        self._main_window = None
        self._is_shut_down = False

    def run--- This code section failed: ---

 L.  29         0  LOAD_GLOBAL              MopWindow
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _builder
                6  LOAD_FAST                'args'
                8  CALL_FUNCTION_2       2  ''
               10  LOAD_FAST                'self'
               12  STORE_ATTR               _main_window

 L.  32        14  LOAD_STR                 'on_file_quit_menu_item_activate'

 L.  32        16  LOAD_FAST                'self'
               18  LOAD_ATTR                quit

 L.  31        20  BUILD_MAP_1           1 
               22  STORE_FAST               'handlers'

 L.  34        24  LOAD_FAST                'handlers'
               26  LOAD_METHOD              update
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _main_window
               32  LOAD_ATTR                handlers
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L.  36        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _builder
               42  LOAD_METHOD              connect_signals
               44  LOAD_FAST                'handlers'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L.  37        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _main_window
               54  LOAD_ATTR                window
               56  LOAD_METHOD              connect
               58  LOAD_STR                 'delete-event'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                quit
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          

 L.  39        68  SETUP_FINALLY        92  'to 92'

 L.  40        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _main_window
               74  LOAD_METHOD              show
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          

 L.  41        80  LOAD_GLOBAL              Gtk
               82  LOAD_METHOD              main
               84  CALL_METHOD_0         0  ''
               86  POP_TOP          
               88  POP_BLOCK        
               90  JUMP_FORWARD        210  'to 210'
             92_0  COME_FROM_FINALLY    68  '68'

 L.  42        92  DUP_TOP          
               94  LOAD_GLOBAL              KeyboardInterrupt
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   110  'to 110'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L.  43       106  POP_EXCEPT       
              108  JUMP_FORWARD        210  'to 210'
            110_0  COME_FROM            98  '98'

 L.  44       110  DUP_TOP          
              112  LOAD_GLOBAL              FileNotFoundError
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   158  'to 158'
              118  POP_TOP          
              120  STORE_FAST               'ex'
              122  POP_TOP          
              124  SETUP_FINALLY       146  'to 146'

 L.  45       126  LOAD_GLOBAL              log
              128  LOAD_METHOD              error
              130  LOAD_FAST                'ex'
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          

 L.  46       136  POP_BLOCK        
              138  POP_EXCEPT       
              140  CALL_FINALLY        146  'to 146'
              142  LOAD_CONST               1
              144  RETURN_VALUE     
            146_0  COME_FROM           140  '140'
            146_1  COME_FROM_FINALLY   124  '124'
              146  LOAD_CONST               None
              148  STORE_FAST               'ex'
              150  DELETE_FAST              'ex'
              152  END_FINALLY      
              154  POP_EXCEPT       
              156  JUMP_FORWARD        210  'to 210'
            158_0  COME_FROM           116  '116'

 L.  47       158  DUP_TOP          
              160  LOAD_GLOBAL              Exception
              162  COMPARE_OP               exception-match
              164  POP_JUMP_IF_FALSE   208  'to 208'
              166  POP_TOP          
              168  STORE_FAST               'ex'
              170  POP_TOP          
              172  SETUP_FINALLY       196  'to 196'

 L.  48       174  LOAD_GLOBAL              log
              176  LOAD_METHOD              exception
              178  LOAD_STR                 'Error:'
              180  LOAD_FAST                'ex'
              182  CALL_METHOD_2         2  ''
              184  POP_TOP          

 L.  49       186  POP_BLOCK        
              188  POP_EXCEPT       
              190  CALL_FINALLY        196  'to 196'
              192  LOAD_CONST               2
              194  RETURN_VALUE     
            196_0  COME_FROM           190  '190'
            196_1  COME_FROM_FINALLY   172  '172'
              196  LOAD_CONST               None
              198  STORE_FAST               'ex'
              200  DELETE_FAST              'ex'
              202  END_FINALLY      
              204  POP_EXCEPT       
              206  JUMP_FORWARD        210  'to 210'
            208_0  COME_FROM           164  '164'
              208  END_FINALLY      
            210_0  COME_FROM           206  '206'
            210_1  COME_FROM           156  '156'
            210_2  COME_FROM           108  '108'
            210_3  COME_FROM            90  '90'

Parse error at or near `CALL_FINALLY' instruction at offset 140

    def quit(self, *_):
        if self._main_window.shutdown():
            self._updateState()
            self._is_shut_down = True
            Gtk.main_quit()
        else:
            log.warning('Quit request rejected')
            return True

    def _updateState(self):
        app_state = getState()
        app_state.main_window_size = self._main_window.window.get_size()
        app_state.main_window_position = self._main_window.window.get_position()
        app_state.save()


class MopWindow:

    def __init__(self, builder, args):
        self._args = args
        self._builder = builder
        self._window = builder.get_object('main_window')
        self._window.set_title('Mop')
        self._file_info_label = builder.get_object('current_file_info_label')
        self._file_path_label = builder.get_object('current_edit_filename_label')
        self._file_size_label = builder.get_object('current_edit_size_label')
        self._file_time_label = builder.get_object('current_edit_time_label')
        self._file_mpeg_info_labels = dict()
        for label in ('mpeg_info_label', 'mpeg_mode_label', 'mpeg_bitrate_label', 'mpeg_sample_rate_label'):
            self._file_mpeg_info_labels[label] = builder.get_object(f"current_edit_{label}")
        else:
            self._file_list_control = FileListControl(builder.get_object('audio_files_tree_view'))
            self._file_list_control.connect'current-edit-changed'self._onFileEditChange
            self._editor_control = EditorControl(self._file_list_control, builder)

    def show(self):
        app_state = getState()
        if None not in app_state.main_window_position:
            (self.window.move)(*app_state.main_window_position)
        if None not in app_state.main_window_size:
            (self.window.resize)(*app_state.main_window_size)
        audio_files = []
        if not self._args.path_args:
            self._onDirectoryOpen(None)
        else:
            for path in self._args.path_args or []:
                if path.exists():
                    if path.is_dir():
                        audio_files += eyed3_load_dir(path)
                    else:
                        if (af := eyed3_load(path)):
                            audio_files.append(af)
                        self._file_list_control.setFiles(audio_files)
                if self._file_list_control.current_audio_file:
                    self._window.show()
                else:
                    if NothingToDoDialog().run() == Gtk.ResponseType.OK:
                        self._args.path_args = None
                        self.show()
                    else:
                        raise FileNotFoundError('Nothing to do')

    @property
    def window(self):
        return self._window

    @property
    def handlers(self):
        return {'on_file_open_menu_item_activate':self._onDirectoryOpen, 
         'on_file_save_menu_item_activate':self._onFileSaveAll, 
         'on_help_about_menu_item_activate':self._onHelpAbout}

    def _onFileSaveAll(self, _):
        if not self._file_list_control.is_dirty:
            log.debug('Files not dirty, nothing to save')
            return None
        files = list(self._file_list_control.dirty_files)
        resp, opts = FileSaveDialog().run()
        if resp == Gtk.ResponseType.OK:
            for audio_file in files:
                for tag in (
                 audio_file.tag, audio_file.second_v1_tag):
                    if tag and tag.is_dirty:
                        self._saveTag(audio_file, tag, opts['version'])

    def _saveTag(self, audio_file, tag, id3_version):
        assert tag
        assert tag.is_dirty
        main_tag = audio_file.tag
        try:
            log.debug(f"Saving tag {audio_file.path}, id3_version={id3_version!r}")
            audio_file.tag = tag
            if id3_version and id3_version[0] == 1 and tag.isV1():
                audio_file.tag.save(version=id3_version)
            else:
                if id3_version and id3_version[0] == 2 and tag.isV2():
                    audio_file.tag.save(version=id3_version)
                else:
                    audio_file.tag.save()
            audio_file.tag.is_dirty = False
        finally:
            audio_file.tag = main_tag

        self._editor_control.edit(audio_file)
        self._file_list_control.list_store.updateRow(audio_file)

    def _onDirectoryOpen(self, _):
        """
        builder = Gtk.Builder()
        builder.add_from_file(str(Path(__file__).parent / "dialogs.ui"))
        dialog = builder.get_object("file_open_dialog")
        """
        dialog = FileChooserDialog(self._window)
        audio_files = []
        filenames = dialog.run()
        for f in filenames or []:
            path = Path(f)
            if path.is_dir():
                dir_files = eyed3_load_dir(f)
                audio_files += dir_files
            else:
                if (audio_file := eyed3_load(path)):
                    audio_files.append(audio_file)
                if audio_files:
                    self._file_list_control.setFiles(audio_files)

    def shutdown(self):
        if self._file_list_control.is_dirty:
            resp = Dialog('quit_confirm_dialog').run()
            if resp in (Gtk.ResponseType.OK, Gtk.ResponseType.CLOSE):
                if resp == Gtk.ResponseType.OK:
                    self._onFileSaveAll(None)
            else:
                if resp == Gtk.ResponseType.CANCEL:
                    return False
                raise ValueError(f"Quit confirm response: {resp}")
        return True

    @staticmethod
    def _onHelpAbout(_):
        about_dialog = AboutDialog()
        about_dialog.run()
        about_dialog.destroy()

    def _onFileEditChange(self, list_control):
        num = len(list_control.list_store)
        if list_control.current_index is not None:
            self._file_info_label.set_markup(f"<b>File {list_control.current_index + 1}  of  {num}</b>")
        else:
            self._file_info_label.set_markup('')
            return
            audio_file = list_control.current_audio_file
            if not audio_file:
                return
            self._file_path_label.set_markup(f"<b>Path:</b> {audio_file.path}")
            self._file_size_label.set_markup(f"<b>Size:</b>  {formatSize(audio_file.info.size_bytes)}  [{formatSize(list_control.total_size_bytes)} total]")
            self._file_time_label.set_markup(f"<b>Time:</b>  {formatTime(audio_file.info.time_secs)}  [{formatTime(list_control.total_time_secs)} total]")
            info = audio_file.info
            text = f"<b>MPEG</b> {info.mp3_header.version}, Layer {'I' * info.mp3_header.layer}, {info.mp3_header.mode}" if info else ''
            self._file_mpeg_info_labels['mpeg_info_label'].set_markup(text)
            text = f"<b>Bitrate:</b> {info.bit_rate_str}" if info else ''
            self._file_mpeg_info_labels['mpeg_bitrate_label'].set_markup(text)
            text = f"<b>Sample rate:</b> {info.mp3_header.sample_freq} Hz" if info else ''
            self._file_mpeg_info_labels['mpeg_sample_rate_label'].set_markup(text)
            self._editor_control.edit(list_control.current_audio_file)