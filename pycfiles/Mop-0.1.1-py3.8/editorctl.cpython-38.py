# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mop/editorctl.py
# Compiled at: 2020-04-02 21:16:23
# Size of source mod 2**32: 23425 bytes
import logging
from functools import partial
from contextlib import contextmanager
from eyed3 import id3, core
from eyed3.id3 import ID3_V1_0, ID3_V1_1, ID3_V2_3, ID3_V2_4, Genre
from eyed3.id3.tag import ID3_V1_MAX_TEXTLEN, ID3_V1_COMMENT_DESC
from gi.repository import GObject, Gtk, Gdk
from .core import GENRES
log = logging.getLogger(__name__)
ENTRY_ICON_PRIMARY = Gtk.EntryIconPosition.PRIMARY
ENTRY_ICON_SECONDARY = Gtk.EntryIconPosition.SECONDARY
MOUSE_BUTTON1_MASK = Gdk.ModifierType.BUTTON1_MASK
_id3_v1_genre_model = Gtk.ListStore(str, str)
_id3_v1_genre_model.append(['', '-1'])
_id3_v2_genre_model = Gtk.ListStore(str, str)
_id3_v2_genre_model.append(['', '-1'])
for genre in sorted(GENRES.iter()):
    _id3_v2_genre_model.append([genre.name, str(genre.id)])
    if genre.id is not None:
        if genre.id <= GENRES.WINAMP_GENRE_MAX:
            _id3_v1_genre_model.append([genre.name, str(genre.id)])

        class EditorWidget(GObject.GObject):
            __gsignals__ = {'tag-changed':(
              GObject.SIGNAL_RUN_LAST, None, []), 
             'tag-value-copy':(
              GObject.SIGNAL_RUN_LAST, None, (str,)), 
             'tag-value-incr':(
              GObject.SIGNAL_RUN_LAST, None, [])}

            def __init__(self, name, widget, editor_ctl):
                super().__init__()
                self._name = name
                self._editor_ctl = editor_ctl
                self._on_change_active = True
                self.widget = widget
                self._connect()
                self._default_tooltip = self.widget.get_tooltip_text()

            def init(self, tag):
                raise NotImplementedError()

            def get(self):
                raise NotImplementedError()

            def set(self, tag, value) -> bool:
                getter, setter = self._getAccessors(tag)
                if (value or None) != (getter() or None):
                    log.debug(f"Set tag value: {value}")
                    setter(value)
                    return True
                return False

            def _connect(self):
                self.widget.connect('changed', self._onChanged)
                self.widget.connect('icon-release', self._onDeepCopy)

            def _extractPropertyName(self):
                prop = ''
                cap_next = False
                for c in self._name[len('tag_'):-len('_entry')]:
                    if c == '_':
                        cap_next = True
                    else:
                        if cap_next:
                            cap_next = False
                            c = c.upper()
                        prop += c
                else:
                    prop = prop[0].upper() + prop[1:]
                    return prop

            def _getAccessors(self, tag, prop=None):
                prop = prop or self._extractPropertyName()
                getter_name = f"_get{prop}"
                setter_name = f"_set{prop}"
                if hasattr(tag, getter_name):
                    if hasattr(tag, setter_name):
                        return (
                         getattr(tag, getter_name), getattr(tag, setter_name))
                raise ValueError(f"Unsupported property name: {prop}")

            def _onChanged(self, widget):
                if self._on_change_active:
                    if self._editor_ctl.current_edit:
                        tag = self._editor_ctl.current_edit.selected_tag
                        if self.set(tag, widget.get_text()):
                            log.debug('Setting tag_dirty4')
                            tag.is_dirty = True
                            self.emit('tag-changed')

            def _onDeepCopy(self, entry, icon_pos, button):
                raise NotImplementedError()

            @contextmanager
            def _onChangeInactive(self):
                """Context manager for deactivating on-change events."""
                self._on_change_active = False
                try:
                    (yield)
                finally:
                    self._on_change_active = True

            def _setSensitive(self, state, tooltip_text):
                self.widget.set_sensitive(state)
                self.widget.set_tooltip_text(tooltip_text)


        class EntryEditorWidget(EditorWidget):

            def init(self, tag):
                with self._onChangeInactive():
                    if tag.isV1():
                        self.widget.set_max_length(ID3_V1_MAX_TEXTLEN)
                    else:
                        self.widget.set_max_length(0)
                    if tag:
                        getter, _ = self._getAccessors(tag)
                        curr_val = getter()
                        self.widget.set_text(str(curr_val or ''))
                    else:
                        self.widget.set_text('')

            def get(self):
                return self.widget.get_text()

            def _onDeepCopy(self, entry, icon_pos, button):
                if icon_pos == ENTRY_ICON_SECONDARY:
                    if button.state & MOUSE_BUTTON1_MASK:
                        self.emit('tag-value-copy', self.get())


        class SimpleAccessorEditorWidgetABC(EntryEditorWidget):

            def init(self, tag):
                if tag.isV1():
                    limit = ID3_V1_MAX_TEXTLEN
                    if tag.isV1():
                        limit -= 2
                    self.widget.set_max_length(limit)
                else:
                    self.widget.set_max_length(0)
                with self._onChangeInactive():
                    if tag:
                        getter, _ = self._getAccessors(tag)
                        text_frame = getter()
                        self.widget.set_text(text_frame.text if text_frame else '')
                    else:
                        self.widget.set_text('')


        class SimpleCommentEditorWidget(SimpleAccessorEditorWidgetABC):

            def init(self, tag):
                retval = super().init(tag)
                if tag.isV1():
                    limit = ID3_V1_MAX_TEXTLEN
                    if tag.version[1] == 1:
                        limit -= 2
                    self.widget.set_max_length(limit)
                else:
                    self.widget.set_max_length(0)
                return retval

            def _getAccessors(self, tag, prop=None):
                desc = '' if tag.isV2() else ID3_V1_COMMENT_DESC
                lang = id3.DEFAULT_LANG

                def setter(val):
                    tag.comments.set(val, desc, lang=lang)

                return (
                 partial((tag.comments.get), desc, lang=lang), setter)


        class SimpleUrlEditorWidget(SimpleAccessorEditorWidgetABC):

            def _getAccessors(self, tag, prop=None):
                desc = ''

                def setter(val):
                    tag.user_url_frames.set(val, desc)

                return (
                 partial(tag.user_url_frames.get, desc), setter)

            def init(self, tag):
                with self._onChangeInactive():
                    if tag:
                        getter, _ = self._getAccessors(tag)
                        url_frame = getter()
                        self.widget.set_text(url_frame.url if url_frame else '')
                    else:
                        self.widget.set_text('')


        class NumTotalEditorWidget(EntryEditorWidget):

            def __init__(self, name, num_widget, editor_ctl, is_total=False):
                self._is_total = is_total
                super().__init__(name, num_widget, editor_ctl)

            def _connect(self):
                self.widget.connect('changed', self._onChanged)
                self.widget.connect('icon-release', self._onDeepCopy)

            def _getAccessors(self, tag, prop=None):
                prop = self._extractPropertyName()
                if self._is_total:
                    prop = prop.replace('Total', 'Num')
                return super()._getAccessors(tag, prop=prop)

            def set(self, tag, value) -> bool:
                getter, setter = self._getAccessors(tag)
                curr = getter()
                value = int(value) if value else None
                new_value = (curr[0], value) if self._is_total else (value, curr[1])
                if new_value != curr:
                    setter(new_value)
                    return True

            def _onDeepCopy(self, entry, icon_pos, button):
                if button.state & MOUSE_BUTTON1_MASK:
                    if icon_pos == ENTRY_ICON_PRIMARY:
                        self.emit('tag-value-incr')
                    else:
                        if icon_pos == ENTRY_ICON_SECONDARY:
                            super()._onDeepCopy(entry, icon_pos, button)

            def init--- This code section failed: ---

 L. 241         0  LOAD_FAST                'tag'
                2  LOAD_ATTR                version
                4  LOAD_CONST               None
                6  LOAD_CONST               2
                8  BUILD_SLICE_2         2 
               10  BINARY_SUBSCR    
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'major'
               16  STORE_FAST               'minor'

 L. 242        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _name
               22  LOAD_METHOD              startswith
               24  LOAD_STR                 'tag_track_'
               26  CALL_METHOD_1         1  ''
               28  POP_JUMP_IF_FALSE    96  'to 96'
               30  LOAD_FAST                'major'
               32  LOAD_CONST               1
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    96  'to 96'

 L. 243        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _name
               42  LOAD_METHOD              startswith
               44  LOAD_STR                 'tag_track_num'
               46  CALL_METHOD_1         1  ''
               48  POP_JUMP_IF_FALSE    82  'to 82'

 L. 244        50  LOAD_FAST                'self'
               52  LOAD_METHOD              _setSensitive

 L. 245        54  LOAD_FAST                'minor'
               56  LOAD_CONST               0
               58  COMPARE_OP               !=

 L. 246        60  LOAD_FAST                'minor'
               62  LOAD_CONST               0
               64  COMPARE_OP               !=
               66  POP_JUMP_IF_FALSE    74  'to 74'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _default_tooltip
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            66  '66'
               74  LOAD_STR                 'Track number requires ID3 v1.1'
             76_0  COME_FROM            72  '72'

 L. 244        76  CALL_METHOD_2         2  ''
               78  POP_TOP          
               80  JUMP_ABSOLUTE       144  'to 144'
             82_0  COME_FROM            48  '48'

 L. 249        82  LOAD_FAST                'self'
               84  LOAD_METHOD              _setSensitive
               86  LOAD_CONST               False
               88  LOAD_STR                 'Track total requires ID3 v2.x'
               90  CALL_METHOD_2         2  ''
               92  POP_TOP          
               94  JUMP_FORWARD        144  'to 144'
             96_0  COME_FROM            36  '36'
             96_1  COME_FROM            28  '28'

 L. 250        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _name
              100  LOAD_METHOD              startswith
              102  LOAD_STR                 'tag_disc_'
              104  CALL_METHOD_1         1  ''
              106  POP_JUMP_IF_FALSE   130  'to 130'
              108  LOAD_FAST                'tag'
              110  LOAD_METHOD              isV1
              112  CALL_METHOD_0         0  ''
              114  POP_JUMP_IF_FALSE   130  'to 130'

 L. 252       116  LOAD_FAST                'self'
              118  LOAD_METHOD              _setSensitive
              120  LOAD_CONST               False
              122  LOAD_STR                 'Disc number requires ID3 v2.x'
              124  CALL_METHOD_2         2  ''
              126  POP_TOP          
              128  JUMP_FORWARD        144  'to 144'
            130_0  COME_FROM           114  '114'
            130_1  COME_FROM           106  '106'

 L. 254       130  LOAD_FAST                'self'
              132  LOAD_METHOD              _setSensitive
              134  LOAD_CONST               True
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _default_tooltip
              140  CALL_METHOD_2         2  ''
              142  POP_TOP          
            144_0  COME_FROM           128  '128'
            144_1  COME_FROM            94  '94'

 L. 256       144  LOAD_FAST                'self'
              146  LOAD_METHOD              _onChangeInactive
              148  CALL_METHOD_0         0  ''
              150  SETUP_WITH          250  'to 250'
              152  POP_TOP          

 L. 257       154  LOAD_FAST                'tag'
              156  POP_JUMP_IF_TRUE    184  'to 184'

 L. 258       158  LOAD_FAST                'self'
              160  LOAD_ATTR                widget
              162  LOAD_METHOD              set_text
              164  LOAD_STR                 ''
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L. 259       170  POP_BLOCK        
              172  BEGIN_FINALLY    
              174  WITH_CLEANUP_START
              176  WITH_CLEANUP_FINISH
              178  POP_FINALLY           0  ''
              180  LOAD_CONST               None
              182  RETURN_VALUE     
            184_0  COME_FROM           156  '156'

 L. 261       184  LOAD_FAST                'self'
              186  LOAD_METHOD              _getAccessors
              188  LOAD_FAST                'tag'
              190  CALL_METHOD_1         1  ''
              192  UNPACK_SEQUENCE_2     2 
              194  STORE_FAST               'getter'
              196  STORE_FAST               '_'

 L. 262       198  LOAD_FAST                'getter'
              200  CALL_FUNCTION_0       0  ''
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                _is_total
              206  POP_JUMP_IF_TRUE    212  'to 212'
              208  LOAD_CONST               0
              210  JUMP_FORWARD        214  'to 214'
            212_0  COME_FROM           206  '206'
              212  LOAD_CONST               1
            214_0  COME_FROM           210  '210'
              214  BINARY_SUBSCR    
              216  STORE_FAST               'curr_val'

 L. 263       218  LOAD_FAST                'self'
              220  LOAD_ATTR                widget
              222  LOAD_METHOD              set_text
              224  LOAD_FAST                'curr_val'
              226  LOAD_CONST               None
              228  COMPARE_OP               is-not
              230  POP_JUMP_IF_FALSE   240  'to 240'
              232  LOAD_GLOBAL              str
              234  LOAD_FAST                'curr_val'
              236  CALL_FUNCTION_1       1  ''
              238  JUMP_FORWARD        242  'to 242'
            240_0  COME_FROM           230  '230'
              240  LOAD_STR                 ''
            242_0  COME_FROM           238  '238'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
              246  POP_BLOCK        
              248  BEGIN_FINALLY    
            250_0  COME_FROM_WITH      150  '150'
              250  WITH_CLEANUP_START
              252  WITH_CLEANUP_FINISH
              254  END_FINALLY      

Parse error at or near `WITH_CLEANUP_START' instruction at offset 174


        class DateEditorWidget(EntryEditorWidget):

            def __init__(self, *args, **kwargs):
                (super().__init__)(*args, **kwargs)
                self._default_fg = self.widget.get_style().fg

            def init(self, tag):
                retval = super().init(tag)
                if tag.version < ID3_V2_4 and self._name == 'tag_original_release_date_entry':
                    self._setSensitive(False, 'Original release date requires ID3 v2.4')
                else:
                    if tag.isV1() and self._name == 'tag_recording_date_entry':
                        self._setSensitive(False, 'Recording date requires ID3 v2.x')
                    else:
                        self.widget.set_max_length(4 if tag.isV1() else 0)
                        self._setSensitive(True, self._default_tooltip)
                return retval

            def set(self, tag, value) -> bool:
                getter, setter = self._getAccessors(tag)
                try:
                    date = core.Date.parse(value) if value else None
                except ValueError:
                    self.widget.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('red'))
                else:
                    if getter() != date:
                        setter(date)
                        self.widget.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse('black'))
                        return True


        class ComboBoxEditorWidget(EditorWidget):

            def get(self):
                return self.widget.get_active_text()

            def _connect(self):
                self.widget.connect('changed', self._onChanged)
                self._deep_copy_widget.connect('clicked', self._onDeepCopy)

            def _onDeepCopy(self, widget):
                self.emit('tag-value-copy', self.get())


        class AlbumTypeEditorWidget(ComboBoxEditorWidget):

            def __init__(self, name, widget, deep_copy_widget, editor_ctl):
                self._deep_copy_widget = deep_copy_widget
                super().__init__(name, widget, editor_ctl)
                with self._onChangeInactive():
                    self.widget.remove_all()
                    for t in [''] + core.ALBUM_TYPE_IDS:
                        self.widget.append(t, t.upper())

            def init(self, tag):
                with self._onChangeInactive():
                    for i, titer in enumerate(self.widget.get_model()):
                        if (titer[0].lower() or None) == (tag.album_type or None):
                            self.widget.set_active(i)
                            break

                if tag.isV1():
                    self._setSensitive(False, 'Album type requires ID3 v2.x')
                else:
                    self._setSensitive(True, self._default_tooltip)

            def set(self, tag, value) -> bool:
                value = value.lower()
                if (tag.album_type or None) != (value or None):
                    tag.album_type = value
                    return True

            def _onChanged(self, widget):
                if self._on_change_active:
                    if self._editor_ctl.current_edit:
                        tag = self._editor_ctl.current_edit.selected_tag
                        album_type = self.widget.get_active_text()
                        if self.set(tag, album_type):
                            log.debug('Setting tag_dirty5')
                            tag.is_dirty = True
                            self.emit('tag-changed')


        class GenreEditorWidget(ComboBoxEditorWidget):

            def __init__(self, name, widget, deep_copy_widget, editor_ctl):
                with self._onChangeInactive():
                    self._deep_copy_widget = deep_copy_widget
                    super().__init__(name, widget, editor_ctl)
                    self.widget.set_wrap_width(5)
                    self.widget.set_entry_text_column(0)

            def init(self, tag):
                entry = self.widget.get_child()
                entry.set_can_focus(True if tag.isV2() else False)
                entry.set_editable(True if tag.isV2() else False)
                with self._onChangeInactive():
                    if tag.isV1():
                        self.widget.set_model(_id3_v1_genre_model)
                    else:
                        self.widget.set_model(_id3_v2_genre_model)
                    if tag.genre is None:
                        self.widget.set_active_id('-1')
                    else:
                        if tag.genre.id is not None:
                            self.widget.set_active_id(str(tag.genre.id))
                        else:
                            if tag.isV2():
                                try:
                                    gid = str(GENRES.get(tag.genre.name).id)
                                except KeyError:
                                    genre = GENRES.add(tag.genre.name)
                                    gid = str(genre.id)
                                    self.widget.append(gid, genre.name)
                                else:
                                    self.widget.set_active_id(gid)
                            else:
                                self.widget.set_active_id('-1')

            def set(self, tag, genre: Genre) -> bool:
                if (tag.genre or None) != (genre or None):
                    tag.genre = genre
                    return True

            def _onChanged(self, widget):
                if self._on_change_active:
                    if self._editor_ctl.current_edit:
                        gid = self.widget.get_active_id()
                        if gid is not None:
                            try:
                                genre = GENRES.get(int(gid))
                            except KeyError:
                                if not gid == '-1':
                                    assert int(gid) > GENRES.GENRE_ID3V1_MAX
                                genre = None

                        else:
                            genre_text = self.widget.get_active_text()
                            genre = Genre(genre_text, genre_map=GENRES) if genre_text else None
                        tag = self._editor_ctl.current_edit.selected_tag
                        if self.set(tag, genre):
                            log.debug('Setting tag_dirty6')
                            tag.is_dirty = True
                            self.emit('tag-changed')


        class TagVersionChoiceWidget(EditorWidget):

            def __init__(self, *args):
                (super().__init__)(*args)
                self.id3_versions = {(
                 v, f"ID3 {id3.versionToString(v)}"):'.'.join([str(x) for x in v]) for v in (ID3_V2_4, ID3_V2_3, ID3_V1_1, ID3_V1_0)}

            def init(self, selected, other):
                with self._onChangeInactive():
                    self.widget.remove_all()
                    for vid, (version, version_str) in self.id3_versions.items():
                        if not selected.version == version:
                            if not other or other.version == version:
                                self.widget.append(vid, f"ID3 {id3.versionToString(version)}")
                                if selected.version == version:
                                    self.widget.set_active_id(vid)
                        self.widget.set_sensitive(True if other else False)

            def _connect(self):
                self.widget.connect('changed', self._onChanged)

            def set(self, tag, value) -> bool:
                return False

            def get(self):
                return self.widget.get_active_id()

            def _onChanged(self, widget):
                if not self._on_change_active:
                    return
                else:
                    version_id = self.widget.get_active_id()
                    log.debug(f"Current tag version changed: {version_id}")
                    if not version_id:
                        return
                    curr_edit = self._editor_ctl.current_edit
                    curr_tag = curr_edit.tag if curr_edit and not version_id.startswith('1.') else curr_edit.second_v1_tag
                    self._editor_ctl.edit((self._editor_ctl.current_edit), tag=curr_tag)
                    self._editor_ctl.file_list_ctl.list_store.updateRow(curr_edit)

            def _onDeepCopy(self, entry, icon_pos, button):
                raise NotImplementedError()


        class EditorControl(GObject.GObject):
            COMMON_PAGE = 0
            EXTRAS_PAGE = 1
            IMAGES_PAGE = 2
            __gsignals__ = {'tag-changed': (GObject.SIGNAL_RUN_LAST, None, [])}

            def __init__(self, file_list_ctl, builder):
                super().__init__()
                self._file_list_ctl = file_list_ctl
                self._current_audio_file = None
                self._notebook = builder.get_object('editor_notebook')
                self._notebook.get_nth_page(self.IMAGES_PAGE).hide()
                self._edit_prefer_v1_checkbutton = builder.get_object('default_prefer_v1_checkbutton')
                self._editor_widgets = {}
                for widget_name in ('tag_title_entry', 'tag_artist_entry', 'tag_album_entry',
                                    'tag_comment_entry', 'tag_track_num_entry', 'tag_track_total_entry',
                                    'tag_disc_num_entry', 'tag_disc_total_entry',
                                    'tag_release_date_entry', 'tag_recording_date_entry',
                                    'tag_original_release_date_entry', 'tag_album_type_combo',
                                    'tag_version_combo', 'tag_genre_combo', 'tag_albumArtist_entry',
                                    'tag_origArtist_entry', 'tag_composer_entry',
                                    'tag_encodedBy_entry', 'tag_publisher_entry',
                                    'tag_copyright_entry', 'tag_url_entry'):
                    internal_name = f"current_edit_{widget_name}"
                    widget = builder.get_object(internal_name)
                    if widget is None:
                        raise ValueError(f"Glade object not found: {internal_name}")
                    elif widget_name == 'tag_album_type_combo':
                        editor_widget = AlbumTypeEditorWidget(widget_name, widget, builder.get_object('current_edit_tag_album_type_deepcopy'), self)
                    else:
                        if widget_name == 'tag_genre_combo':
                            editor_widget = GenreEditorWidget(widget_name, widget, builder.get_object('current_edit_tag_genre_deepcopy'), self)
                        else:
                            if widget_name == 'tag_version_combo':
                                editor_widget = TagVersionChoiceWidget(widget_name, widget, self)
                            else:
                                if widget_name in ('tag_track_num_entry', 'tag_track_total_entry',
                                                   'tag_disc_num_entry', 'tag_disc_total_entry'):
                                    editor_widget = NumTotalEditorWidget(widget_name, widget, self, is_total=('total' in widget_name))
                                else:
                                    if widget_name.endswith('_date_entry'):
                                        editor_widget = DateEditorWidget(widget_name, widget, self)
                                    else:
                                        if widget_name.endswith('tag_comment_entry'):
                                            editor_widget = SimpleCommentEditorWidget(widget_name, widget, self)
                                        else:
                                            if widget_name.endswith('tag_url_entry'):
                                                editor_widget = SimpleUrlEditorWidget(widget_name, widget, self)
                                            else:
                                                editor_widget = EntryEditorWidget(widget_name, widget, self)
                    if editor_widget is not None:
                        editor_widget.connect('tag-changed', self._onTagChanged)
                        editor_widget.connect('tag-value-copy', self._onTagValueCopy)
                        editor_widget.connect('tag-value-incr', self._onTagValueIncrement)
                        self._editor_widgets[widget_name] = editor_widget

            def _onTagChanged(self, *args):
                log.debug(f"_onTagChanged: {args}")
                self._file_list_ctl.list_store.updateRow(self._file_list_ctl.current_audio_file)
                self.emit('tag-changed')

            def _onTagValueCopy(self, editor_widget, copy_value):
                for audio_file in self._file_list_ctl.list_store.iterAudioFiles():
                    for tag in [t for t in (audio_file.tag, audio_file.second_v1_tag) if t]:
                        if editor_widget.set(tag, copy_value):
                            log.debug('Setting tag_dirty1')
                            tag.is_dirty = True
                            self._file_list_ctl.list_store.updateRow(audio_file)

                else:
                    self.edit(self.current_edit)

            def _onTagValueIncrement(self, editor_widget):
                track_num_entry = self._editor_widgets['tag_track_num_entry']
                track_total_entry = self._editor_widgets['tag_track_total_entry']
                if editor_widget == track_num_entry:
                    i = 1
                    for audio_file in self._file_list_ctl.list_store.iterAudioFiles():
                        for tag in [t for t in (audio_file.tag, audio_file.second_v1_tag) if t]:
                            if editor_widget.set(tag, str(i)):
                                log.debug('Setting tag_dirty2')
                                tag.is_dirty = True
                                self._file_list_ctl.list_store.updateRow(audio_file)
                            i += 1

                else:
                    if editor_widget == track_total_entry:
                        all_files = list(self._file_list_ctl.list_store.iterAudioFiles())
                        file_count = len(all_files)
                        for audio_file in self._file_list_ctl.list_store.iterAudioFiles():
                            if editor_widget.set(audio_file.tag, str(file_count)):
                                log.debug('Setting tag_dirty3')
                                audio_file.tag.is_dirty = True
                                self._file_list_ctl.list_store.updateRow(audio_file)

                self.edit(self.current_edit)

            def edit(self, audio_file, tag=None):
                self._current_audio_file = audio_file
                tag1 = audio_file.tag if audio_file else None
                tag2 = audio_file.second_v1_tag if audio_file else None
                if not tag:
                    if tag2 and self._edit_prefer_v1_checkbutton.get_active():
                        audio_file.selected_tag = tag2
                    else:
                        audio_file.selected_tag = tag1
                else:
                    audio_file.selected_tag = tag
                assert audio_file.selected_tag in (tag1, tag2)
                if audio_file.selected_tag and audio_file.selected_tag.isV1():
                    self._notebook.get_nth_page(self.EXTRAS_PAGE).hide()
                else:
                    self._notebook.get_nth_page(self.EXTRAS_PAGE).show()
                for widget_name, widget in self._editor_widgets.items():
                    if widget_name == 'tag_version_combo':
                        all_tags = {
                         tag1, tag2}
                        all_tags.remove(audio_file.selected_tag)
                        assert len(all_tags) == 1
                        widget.init(audio_file.selected_tag, all_tags.pop())
                    else:
                        try:
                            widget.init(audio_file.selected_tag)
                        except Exception as ex:
                            try:
                                log.exception(ex)
                            finally:
                                ex = None
                                del ex

            @property
            def current_edit(self):
                return self._current_audio_file

            @property
            def file_list_ctl(self):
                return self._file_list_ctl