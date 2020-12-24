# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tv2/urwid_ui.py
# Compiled at: 2019-02-07 01:06:42
# Size of source mod 2**32: 15143 bytes
"""A console user interface for Terminal Velocity.

Implemented using the console user interface library urwid.

"""
import sys, subprocess, shlex, pipes, logging
logger = logging.getLogger(__name__)
import urwid
from . import notebook
palette = [
 ('placeholder', 'dark blue', 'default'),
 ('notewidget unfocused', 'default', 'default'),
 ('notewidget focused', 'black', 'brown'),
 ('search', 'default', 'default'),
 ('autocomplete', 'black', 'brown')]

def system(cmd, loop):
    """Execute a system command in a subshell and return the exit status."""
    loop.screen.stop()
    cmd = '{0}'.format(cmd)
    safe_cmd = shlex.split(cmd)
    logger.debug('System command: {0}'.format(safe_cmd))
    try:
        returncode = subprocess.check_call(safe_cmd)
    except Exception as e:
        try:
            logger.exception(e)
            raise e
        finally:
            e = None
            del e

    loop.start()
    return returncode


def placeholder_text(text):
    """Return a placeholder text widget with the given text."""
    text_widget = urwid.Text(('placeholder', text), align='center')
    filler_widget = urwid.Filler(text_widget)
    return filler_widget


class NoteWidget(urwid.Text):

    def __init__(self, note):
        self.note = note
        return super(NoteWidget, self).__init__(note.title)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

    def render(self, size, focus=False):
        """Render the widget applying focused and unfocused display attrs."""
        if focus:
            attr_map = {None: 'notewidget focused'}
        else:
            attr_map = {None: 'notewidget unfocused'}
        canv = super(NoteWidget, self).render(size, focus=focus)
        canv = urwid.CompositeCanvas(canv)
        canv.fill_attr_apply(attr_map)
        return canv


class AutocompleteWidget(urwid.Edit):
    __doc__ = "A text editing widget with autocomplete support.\n\n    If you set the .autocomplete_text attribute, it will be shown to the user\n    as an autocomplete suggestion.\n\n    Also has a .fake_focus attribute that, if set to True, makes the widget\n    look like it has the keyboard focus even when it doesn't.\n\n    "

    def __init__(self, *args, **kwargs):
        self.fake_focus = True
        self._autocomplete_text = None
        return (super(AutocompleteWidget, self).__init__)(*args, **kwargs)

    def get_autocomplete_text(self):
        return self._autocomplete_text

    def set_autocomplete_text(self, text):
        self._autocomplete_text = text
        self._invalidate()

    autocomplete_text = property(get_autocomplete_text, set_autocomplete_text)

    def render(self, size, focus=False):
        return super(AutocompleteWidget, self).render(size, self.fake_focus)

    def get_text(self):
        if not self.edit_text:
            if not self.autocomplete_text:
                placeholder_text = 'Find or Create'
                return (placeholder_text,
                 [
                  (
                   'placeholder', len(placeholder_text))])
        else:
            if not self.autocomplete_text:
                return super(AutocompleteWidget, self).get_text()
            is_substring = self.autocomplete_text.lower().startswith(self.edit_text.lower())
            if self.edit_text and is_substring:
                text_to_show = self.edit_text + self.autocomplete_text[len(self.edit_text):]
                attrs = [('search', len(self.edit_text)),
                 (
                  'autocomplete', len(text_to_show) - len(self.edit_text))]
                return (text_to_show, attrs)
        return (
         self.autocomplete_text,
         [
          (
           'autocomplete', len(self.autocomplete_text))])

    def consume(self):
        """Consume the autocomplete text, turning it into typed text."""
        if self.autocomplete_text:
            if len(self.edit_text) < len(self.autocomplete_text):
                self.set_edit_text(self.autocomplete_text)
                self.move_cursor_to_coords((1, ), len(self.autocomplete_text), 0)
                self.autocomplete_text = None
                return True
        return False


class NoteFilterListBox(urwid.ListBox):
    __doc__ = 'A filterable list of notes from a notebook.'

    def __init__(self, on_changed=None):
        """Initialise a new NoteFilterListBox.

        Keyword arguments:
        on_changed -- callable that will be called when the focused note
            changes, the new focused note will be passed as argument

        """
        self._fake_focus = False
        self.list_walker = urwid.SimpleFocusListWalker([])
        self.widgets = {}
        super(NoteFilterListBox, self).__init__(self.list_walker)
        self.on_changed = on_changed

    def get_selected_note(self):
        return self.focus.note

    selected_note = property(get_selected_note)

    def get_fake_focus(self):
        return self._fake_focus

    def set_fake_focus(self, value):
        self._fake_focus = value
        self._invalidate()

    fake_focus = property(get_fake_focus, set_fake_focus)

    def render(self, size, focus=False):
        if len(self.list_walker) == 0:
            placeholder = placeholder_text('No matching notes, press Enter to create a new note')
            return placeholder.render(size)
        return super(NoteFilterListBox, self).render(size, self.fake_focus)

    def filter(self, matching_notes):
        """Filter this listbox to show only widgets for matching notes."""
        matching_widgets = []
        for note in matching_notes:
            widget = self.widgets.get(note.abspath)
            if widget:
                matching_widgets.append(widget)
            else:
                widget = NoteWidget(note)
                self.widgets[note.abspath] = widget
                matching_widgets.append(widget)

        del self.list_walker[:]
        for widget in matching_widgets:
            self.list_walker.append(widget)

    def focus_note(self, note):
        """Focus the widget for the given note."""
        for widget in self.list_walker:
            if widget.note == note:
                self.list_walker.set_focus(self.list_walker.index(widget))
                break

    def keypress(self, size, key):
        result = super(NoteFilterListBox, self).keypress(size, key)
        self.on_changed(self.selected_note)
        return result

    def mouse_event(self, size, event, button, col, row, focus):
        result = super(NoteFilterListBox, self).mouse_event(size, event, button, col, row, focus)
        self.on_changed(self.selected_note)
        return result


class MainFrame(urwid.Frame):
    __doc__ = 'The topmost urwid widget.'

    def __init__(self, notes_dir, editor, extension, extensions, exclude=None):
        self.editor = editor
        self.notebook = notebook.PlainTextNoteBook(notes_dir, extension, extensions,
          exclude=exclude)
        self.suppress_filter = False
        self.suppress_focus = False
        self._selected_note = None
        self.search_box = AutocompleteWidget(wrap='clip')
        self.list_box = NoteFilterListBox(on_changed=(self.on_list_box_changed))
        urwid.connect_signal(self.search_box, 'change', self.on_search_box_changed)
        super(MainFrame, self).__init__(header=(urwid.LineBox(self.search_box)),
          body=None,
          focus_part='body')
        self.filter(self.search_box.edit_text)

    def get_selected_note(self):
        return self._selected_note

    def set_selected_note(self, note):
        """Select the given note.

        Make the note appear focused in the list box, and the note's title
        autocompleted in the search box.

        """
        if self.suppress_focus:
            return
        if note:
            self.search_box.autocomplete_text = note.title
            self.list_box.fake_focus = True
            self.list_box.focus_note(note)
        else:
            self.search_box.autocomplete_text = None
            self.list_box.fake_focus = False
        self._selected_note = note

    selected_note = property(get_selected_note, set_selected_note)

    def quit(self):
        """Quit the app."""
        raise urwid.ExitMainLoop()

    def keypress(self, size, key):
        maxcol, maxrow = size
        self.suppress_filter = False
        self.suppress_focus = False
        if key in ('esc', 'ctrl d'):
            if self.selected_note:
                self.selected_note = None
                return
                if self.search_box.edit_text:
                    self.search_box.set_edit_text('')
                    return
                else:
                    if key in ('enter', ):
                        if self.selected_note:
                            system(self.editor + ' ' + pipes.quote(self.selected_note.abspath), self.loop)
                    elif self.search_box.edit_text:
                        try:
                            note = self.notebook.add_new(self.search_box.edit_text)
                            system(self.editor + ' ' + pipes.quote(note.abspath), self.loop)
                        except notebook.NoteAlreadyExistsError:
                            system(self.editor + ' ' + pipes.quote(self.search_box.edit_text + self.notebook.extension), self.loop)
                        except notebook.InvalidNoteTitleError:
                            pass

            else:
                pass
        else:
            self.suppress_focus = True
            self.filter(self.search_box.edit_text)
            return
            if key in ('ctrl x', ):
                self.quit()
            else:
                if self.selected_note and key in ('tab', 'left', 'right'):
                    if self.search_box.consume():
                        return
                    return self.search_box.keypress((maxcol,), key)
                else:
                    if key in ('down', ):
                        if not self.list_box.fake_focus:
                            self.list_box.fake_focus = True
                            self.on_list_box_changed(self.list_box.selected_note)
                            return
                        return self.list_box.keypress(size, key)
                    else:
                        if key in ('up', 'page up', 'page down'):
                            return self.list_box.keypress(size, key)
                        if key in ('backspace', ):
                            consume = False
                            if self.selected_note:
                                if self.search_box.edit_text == '':
                                    consume = True
                            else:
                                title = self.selected_note.title.lower()
                                typed = self.search_box.edit_text.lower()
                                if not title.startswith(typed):
                                    consume = True
                                if consume:
                                    self.search_box.consume()
                                else:
                                    self.selected_note = None
                            self.suppress_focus = True
                            return self.search_box.keypress((maxcol,), key)
                        return self.search_box.keypress((maxcol,), key)

    def filter(self, query):
        """Do the synchronised list box filter and search box autocomplete.

        """
        if self.suppress_filter:
            return
        else:
            if len(self.notebook) == 0:
                self.body = placeholder_text('You have no notes yet, to create a note type a note title then press Enter')
            else:
                self.body = urwid.Padding((self.list_box), left=1, right=1)
            matching_notes = self.notebook.search(query)
            matching_notes.sort(key=(lambda x: x.mtime), reverse=True)
            self.list_box.filter(matching_notes)
            autocompletable_matches = []
            if query:
                for note in matching_notes:
                    if note.title.lower().startswith(query.lower()):
                        autocompletable_matches.append(note)

            if autocompletable_matches:
                self.selected_note = autocompletable_matches[0]
            else:
                self.selected_note = None

    def on_search_box_changed(self, edit, new_edit_text):
        self.filter(new_edit_text)

    def on_list_box_changed(self, note):
        self.selected_note = note


def launch(notes_dir, editor, extension, extensions, exclude=None):
    """Launch the user interface."""
    urwid.set_encoding(sys.getfilesystemencoding())
    frame = MainFrame(notes_dir, editor, extension, extensions, exclude=exclude)
    loop = urwid.MainLoop(frame, palette)
    frame.loop = loop
    loop.run()