# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/utils/widgets.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 44770 bytes
import re, os, ntpath
from fnmatch import fnmatch
import tkinter.messagebox, tkinter.simpledialog
from importlib import util as imputil
from string import ascii_letters, digits, punctuation
from tkinter import _setit, Menu, TclError, Frame, StringVar, Button, Text, IntVar, Checkbutton, Entry, OptionMenu, Scrollbar, Grid, Place, Pack
from tkinter.constants import INSERT, LEFT, W, END, DISABLED, NORMAL, RIGHT, Y, BOTTOM, X, BOTH, HORIZONTAL, SEL
from tkinter.filedialog import askopenfilename
from .project import mlnpath
try:
    if imputil.find_spec('Pmw'):
        from Pmw.Pmw_2_0_1.lib.PmwComboBox import ComboBox
        havePMW = True
    else:
        havePMW = False
except:
    havePMW = False

BOLDFONT = '*-Monospace-Bold-R-Normal-*-12-*'
ITALICFONT = '*-Monospace-Medium-O-Normal-*-12-*'

class ScrolledText2(Text):

    def __init__(self, master=None, change_hook=None, **kw):
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.change_hook = change_hook
        self.hbar = Scrollbar(self.frame, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)
        kw.update({'yscrollcommand': self.vbar.set})
        kw.update({'xscrollcommand': self.hbar.set})
        kw.update({'wrap': 'none'})
        Text.__init__(self, self.frame, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.yview
        self.hbar['command'] = self.xview
        text_meths = list(vars(Text).keys())
        methods = list(vars(Pack).keys()) + list(vars(Grid).keys()) + list(vars(Place).keys())
        methods = set(methods).difference(text_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)


class Highlighter(object):

    def __init__(self):
        self.tags = {'com': dict(foreground='#22aa22', font=ITALICFONT), 
         'mlcom': dict(foreground='#22aa22', font=ITALICFONT), 
         'str': dict(foreground='darkcyan'), 
         'kw': dict(foreground='blue'), 
         'obj': dict(foreground='#00F'), 
         'number': dict(foreground='darkred'), 
         'op': dict(foreground='blue'), 
         'bracket_hl': dict(background='yellow'), 
         'var': dict(font=ITALICFONT), 
         'pred': dict(font=BOLDFONT)}
        self.brackets = (('(', ')'), ('{', '}'))
        self.open_brackets = [x[0] for x in self.brackets]
        self.close_brackets = [x[1] for x in self.brackets]
        self.operators = ['v', '^', '!', '+', '=>', '<=>']
        self.keywords = []


class BLNHighlighter(Highlighter):

    def __init__(self):
        Highlighter.__init__(self)
        self.keywords = ['type', 'Type', 'fragments', 'isa', 'random', 'logical', 'relationKey', 'constraints', 'guaranteed', 'combining-rule', 'uniform-default', 'prolog']


class SyntaxHighlightingText(ScrolledText2):

    def __init__(self, root, change_hook=None, highlighter=None, grammar=None):
        ScrolledText2.__init__(self, root, change_hook)
        self.text = self
        self.root = root
        self.change_hook = change_hook
        self.characters = ascii_letters + digits + punctuation
        self.tabwidth = 8
        self.indentwidth = 4
        self.indention = 0
        self.set_tabwidth(self.indentwidth)
        self.previous_line = '0'
        self.highlighter = None
        self.menu = Menu(root, tearoff=0)
        self.menu.add_command(label='Undo', command=self.edit_undo)
        self.menu.add_command(label='Redo', command=self.edit_redo)
        self.menu.add_command(label='Cut', command=self.cut)
        self.menu.add_command(label='Copy', command=self.copy)
        self.menu.add_command(label='Paste', command=self.paste)
        self.bind('<KeyRelease>', self.key_release)
        self.bind('<Return>', self.autoindent)
        self.bind('<Button-3>', self.popup)
        self.bind('<Button-1>', self.recolorCurrentLine)
        self.bind('<Control-Any-KeyPress>', self.ctrl)
        self.grammar = grammar
        self.setHighlighter(highlighter)

    def setHighlighter(self, highlighter):
        if highlighter is None:
            highlighter = Highlighter()
        self.highlighter = highlighter
        for tag, settings in list(self.highlighter.tags.items()):
            self.tag_config(tag, **settings)

    def popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def get_tabwidth(self):
        current = self['tabs'] or 5000
        return int(current)

    def set_tabwidth(self, newtabwidth):
        text = self
        if self.get_tabwidth() != newtabwidth:
            pixels = text.tk.call('font', 'measure', text['font'], '-displayof', text.master, 'n' * newtabwidth)
            text.configure(tabs=pixels)

    def remove_singleline_tags(self, start, end):
        for tag in list(self.highlighter.tags.keys()):
            if tag[:2] != 'ml':
                self.tag_remove(tag, start, end)

    def get_selection_indices(self):
        try:
            first = self.text.index('sel.first')
            last = self.text.index('sel.last')
            return (
             first, last)
        except TclError:
            return

    def select_all(self):
        self.tag_add(SEL, '1.0', END)
        self.mark_set(INSERT, END)
        self.see(INSERT)
        self.focus_set()
        return 'break'

    def cut(self, event=0):
        self.clipboard_clear()
        Selection = self.get_selection_indices()
        if Selection is not None:
            SelectedText = self.get(Selection[0], Selection[1])
            self.delete(Selection[0], Selection[1])
            self.clipboard_append(SelectedText)
            self.onChange()

    def copy(self, event=0):
        self.clipboard_clear()
        Selection = self.get_selection_indices()
        if Selection is not None:
            SelectedText = self.get(Selection[0], Selection[1])
            self.clipboard_append(SelectedText)

    def paste(self, event=0):
        SelectedText = self.root.selection_get(selection='CLIPBOARD')
        Selection = self.get_selection_indices()
        if Selection is not None:
            self.delete(Selection[0], Selection[1])
        self.insert(INSERT, SelectedText)
        self.onChange()
        return 'break'

    def autoindent(self, event):
        if event.keysym == 'Return':
            self.edit_separator()
            index = self.index(INSERT).split('.')
            line = int(index[0])
            column = int(index[1])
            if self.get('%s.%d' % (line, column - 1)) == ':':
                self.indention += 1
            self.insert(INSERT, '\n')
            self.insert(INSERT, '\t' * self.indention)
            return 'break'
        if event.keysym == 'Tab':
            self.edit_separator()
            self.indention += 1
        elif event.keysym == 'BackSpace':
            self.edit_separator()
            index = self.index(INSERT).split('.')
            line = int(index[0])
            column = int(index[1])
        if self.get('%s.%d' % (line, column - 1)) == '\t':
            self.indention -= 1

    def recolorCurrentLine(self, *_):
        pos = self.index(INSERT)
        cline = pos.split('.')[0]
        if cline != self.previous_line:
            self.colorize(self.previous_line)
        self.colorize(cline)
        self.previous_line = cline

    def key_release(self, key):
        if key.char in ' :[(]),"\'':
            self.edit_separator()
        self.recolorCurrentLine()
        pos = self.index(INSERT)
        if key.keysym in ('BackSpace', 'Delete'):
            ranges = self.tag_ranges('mlcom')
            i = 0
            while i < len(ranges):
                r = ranges[i:i + 2]
                second_range = (self.index(str(r[0]) + ' + 1 char'), self.index(str(r[1]) + ' - 1 char'))
                if pos in r or pos in second_range:
                    self.tag_remove('mlcom', r[0], r[1])
                i += 2

        if key.char != '' and not key.state & 4 or key.keysym in ('BackSpace', 'Delete'):
            self.onChange()

    def onChange(self):
        if self.change_hook is not None:
            self.change_hook()

    def delete_current_line(self):
        selection = self.get_selection_indices()
        if selection is None:
            start = int(self.index(INSERT).split('.')[0])
            end = start
        else:
            start = int(selection[0].split('.')[0])
            end = int(selection[1].split('.')[0])
        self.delete('%d.0' % start, '%d.end' % end)
        self.onChange()

    def ctrl(self, key):
        if key.keysym == 'c':
            return self.copy()
        if key.keysym == 'x':
            return self.cut()
        if key.keysym == 'v':
            return self.paste()
        if key.keysym == 'a':
            return self.select_all()
        if key.keysym == 'd':
            return self.delete_current_line()

    def colorize(self, cline):
        cursorPos = self.index(INSERT)
        buffer = self.get('%s.%d' % (cline, 0), '%s.end' % cline)
        self.remove_singleline_tags('%s.%d' % (cline, 0), '%s.end' % cline)
        in_quote = False
        quote_start = 0
        for i in range(len(buffer)):
            here = '%s.%d' % (cline, i)
            if buffer[i] in ('"', "'"):
                if in_quote:
                    self.tag_add('str', '%s.%d' % (cline, quote_start), '%s.%d' % (cline, i + 1))
                    in_quote = False
                else:
                    quote_start = i
                    in_quote = True
                if not in_quote:
                    if buffer[i:i + 2] == '//':
                        self.tag_add('com', '%s.%d' % (cline, i), '%s.end' % cline)
                    else:
                        if buffer[i:i + 2] == '/*':
                            if here not in self.tag_ranges('mlcom'):
                                end_pos = self.search('*/', here, forwards=True)
                                if not end_pos:
                                    pass
                                else:
                                    if self.search('/*', here + ' + 2 chars', stopindex=end_pos):
                                        pass
                                    else:
                                        self.tag_add('mlcom', here, str(end_pos) + ' + 2 chars')
                        else:
                            if buffer[i:i + 2] == '*/':
                                end_pos = self.index(here + ' + 2 chars')
                                if end_pos not in self.tag_ranges('mlcom'):
                                    start_pos = self.search('/*', here, backwards=True)
                                    if not start_pos:
                                        pass
                                    else:
                                        if self.search('*/', here, stopindex=start_pos, backwards=True):
                                            pass
                                        else:
                                            self.tag_add('mlcom', start_pos, end_pos)
                            else:
                                if buffer[i] in self.highlighter.open_brackets and here == cursorPos:
                                    idxBracketType = self.highlighter.open_brackets.index(buffer[i])
                                    openb, closeb = self.highlighter.brackets[idxBracketType]
                                    stack = 1
                                    for j, c in enumerate(buffer[i + 1:]):
                                        if c == openb:
                                            stack += 1
                                        elif c == closeb:
                                            stack -= 1
                                            if stack == 0:
                                                self.tag_add('bracket_hl', here, here + ' + 1 char')
                                                self.tag_add('bracket_hl', '%s.%d' % (cline, i + 1 + j), '%s.%d' % (cline, i + 1 + j + 1))
                                                break

                                elif buffer[i] in self.highlighter.close_brackets and self.index(here + ' + 1 char') == cursorPos:
                                    idxBracketType = self.highlighter.close_brackets.index(buffer[i])
                                    openb, closeb = self.highlighter.brackets[idxBracketType]
                                    stack = 1
                                    l = list(buffer[:i])
                                    l.reverse()
                                    for j, c in enumerate(l):
                                        if c == closeb:
                                            stack += 1
                                        elif c == openb:
                                            stack -= 1
                                            if stack == 0:
                                                self.tag_add('bracket_hl', here, here + ' + 1 char')
                                                self.tag_add('bracket_hl', '%s.%d' % (cline, i - 1 - j), '%s.%d' % (cline, i - 1 - j + 1))
                                                break

        start, end = (0, 0)
        obj_flag = 0
        for match in re.finditer('(\\?[a-zA-Z0-9]+|[\\w]*[a-zA-Z]\\()', buffer):
            token = match.group(0)
            if self.grammar is not None and self.grammar.isvar(token):
                self.tag_add('var', '%s.%d' % (cline, match.start()), '%s.%d' % (cline, match.end()))
            elif token[(-1)] == '(':
                self.tag_add('pred', '%s.%d' % (cline, match.start()), '%s.%d' % (cline, match.end() - 1))

        for token in buffer.split(' '):
            end = start + len(token)
            start_index = '%s.%d' % (cline, start)
            end_index = '%s.%d' % (cline, end)
            if obj_flag:
                self.tag_add('obj', start_index, end_index)
                obj_flag = 0
            if token.strip() in self.highlighter.keywords:
                self.tag_add('kw', start_index, end_index)
                if token.strip() in ('def', 'class'):
                    obj_flag = 1
            else:
                try:
                    float(token)
                except ValueError:
                    pass
                else:
                    self.tag_add('number', '%s.%d' % (cline, start), '%s.%d' % (cline, end))
            start += len(token) + 1

    def insert(self, index, text, *args):
        line = int(self.index(index).split('.')[0])
        Text.insert(self, index, text, *args)
        for i in range(text.count('\n')):
            self.colorize(str(line + i))

    def disable(self, disable):
        Text.config(self, state=DISABLED if disable else NORMAL)


class FileEditBar(Frame, object):

    def __init__(self, master, directory='.', filesettings=None, defaultname='*unknown{}', importhook=None, deletehook=None, projecthook=None, filecontenthook=None, selectfilehook=None, fileslisthook=None, updatehook=None, onchangehook=None):
        self.master = master
        Frame.__init__(self, master)
        self.selected_file = StringVar()
        self.selected_file.trace('w', self.select_file)
        self._dirty = False
        self._dirty_file_name = ''
        self._editor_dirty = False
        self.dir = directory
        self.fsettings = filesettings
        self.defaultname = defaultname
        self.import_hook = importhook
        self.delete_hook = deletehook
        self.save_project_hook = projecthook
        self.filecontent_hook = filecontenthook
        self.update_hook = updatehook
        self.select_file_hook = selectfilehook
        self.files_list_hook = fileslisthook
        self.onchange_hook = onchangehook
        row = 0
        self.columnconfigure(1, weight=2)
        files = []
        self.file_buffer = {}
        self.file_reload = True
        if len(files) == 0:
            files.append('')
        self.list_files = OptionMenu(*(self, self.selected_file) + tuple(files))
        self.list_files.grid(row=row, column=1, sticky='NWE')
        self.btn_newfile = Button(self, text='New', command=self.new_file)
        self.btn_newfile.grid(row=row, column=2, sticky='E')
        self.btn_importfile = Button(self, text='Import', command=self.import_file)
        self.btn_importfile.grid(row=row, column=3, sticky='E')
        self.btn_delfile = Button(self, text='Delete', command=self.delete_file)
        self.btn_delfile.grid(row=row, column=4, sticky='E')
        self.btn_update_file = Button(self, text='Save', command=self.save_file)
        self.btn_update_file.grid(row=row, column=6, sticky='E')
        self.btn_saveas_file = Button(self, text='Save as...', command=self.saveas_file)
        self.btn_saveas_file.grid(row=row, column=7, sticky='E')
        row += 1
        self.editor = SyntaxHighlightingText(self, change_hook=self.onchange_filecontent)
        self.editor.grid(row=row, column=1, columnspan=7, sticky='NWES')
        self.rowconfigure(row, weight=1)

    @property
    def dirty(self):
        return self._dirty or self.file_buffer != {}

    @dirty.setter
    def dirty(self, d):
        self._dirty = d or self.file_buffer != {}
        if self.onchange_hook:
            self.onchange_hook(dirty=self._dirty)

    def new_file(self):
        self.list_files['menu'].add_command(label=self.defaultname.format(self.fsettings.get('extension', '.mln')), command=_setit(self.selected_file, self.defaultname.format(self.fsettings.get('extension', '.mln'))))
        self.selected_file.set(self.defaultname.format(self.fsettings.get('extension', '.mln')))
        self.file_buffer[self.defaultname.format(self.fsettings.get('extension', '.mln'))] = ''
        self.editor.delete('1.0', END)
        self.dirty = True

    def import_file(self):
        filename = askopenfilename(initialdir=self.dir, filetypes=self.fsettings.get('ftypes'), defaultextension=self.fsettings.get('extension', '.mln'))
        if filename:
            fpath, fname = ntpath.split(filename)
            self.dir = os.path.abspath(fpath)
            content = mlnpath(filename).content
            if self.import_hook is not None:
                self.import_hook(fname, content)
            self.update_file_choices()
            self.selected_file.set(fname)
            self.dirty = True

    def delete_file(self):
        fname = self.selected_file.get().strip()
        if fname in self.file_buffer:
            del self.file_buffer[fname]
        if self.delete_hook is not None:
            self.delete_hook(fname)
        f = self.update_file_choices()
        if f:
            self.list_files['menu'].invoke(0)
        else:
            self.selected_file.set('')
            self.editor.delete('1.0', END)
        self.dirty = True

    def save_all_files(self):
        current = self.selected_file.get().strip()
        for f in self.file_buffer:
            content = self.file_buffer[f]
            if f == current:
                content = self.editor.get('1.0', END).strip()
            if self.update_hook is not None:
                self.update_hook(f, f.strip('*'), content)

        self.file_buffer.clear()
        self._editor_dirty = False
        self.update_file_choices()
        self.dirty = False
        if self.save_project_hook is not None:
            self.save_project_hook()

    def save_file(self):
        oldfname = self.selected_file.get().strip()
        if oldfname == self.defaultname.format(self.fsettings.get('extension', '.mln')):
            self.saveas_file()
        else:
            self.update_file(oldfname, new=oldfname.strip('*'), askoverwrite=False)

    def saveas_file(self):
        oldfname = self.selected_file.get().strip()
        res = tkinter.simpledialog.askstring('Save as', 'Enter a filename', initialvalue=oldfname.strip('*'))
        if res is None:
            return
        if res:
            if not res.endswith(self.fsettings.get('extension')):
                res = res + self.fsettings.get('extension')
            self.update_file(oldfname, new=res)

    def update_file(self, old, new=None, askoverwrite=True):
        success = 1
        content = self.editor.get('1.0', END).strip()
        if self.update_hook is not None:
            success = self.update_hook(old.strip('*'), new, content, askoverwrite=askoverwrite)
        if success != -1:
            if old in self.file_buffer:
                del self.file_buffer[old]
            self._editor_dirty = False
            self.update_file_choices()
            fn = new if new is not None and new != '' else old
            if new != '':
                self.selected_file.set(fn)
            self.dirty = False
            if self.save_project_hook is not None:
                self.save_project_hook()

    def select_file(self, *_):
        filename = self.selected_file.get().strip()
        self.dirty = True
        if filename is not None and filename != '':
            if self._editor_dirty:
                self.file_buffer[self._dirty_file_name] = self.editor.get('1.0', END).strip()
                self._editor_dirty = True if '*' in filename else False
                if not self.file_reload:
                    self.file_reload = True
                    return
            if '*' in filename:
                content = self.file_buffer.get(filename, '').strip()
                self.editor.delete('1.0', END)
                content = content.replace('\r', '')
                self.editor.insert(INSERT, content)
                self._editor_dirty = True
                self._dirty_file_name = '*' + filename if '*' not in filename else filename
                return
            if self.files_list_hook is not None and self.filecontent_hook is not None:
                files = self.files_list_hook()
                if filename in files:
                    content = self.filecontent_hook(filename)
                    self.editor.delete('1.0', END)
                    content = content.replace('\r', '')
                    self.editor.insert(INSERT, content)
                    self._editor_dirty = False
        else:
            self.editor.delete('1.0', END)
            self.list_files['menu'].delete(0, 'end')
        if self.select_file_hook is not None:
            self.select_file_hook()

    def update_file_choices(self):
        self.list_files['menu'].delete(0, 'end')
        files = []
        if self.files_list_hook is not None:
            files = self.files_list_hook()
        new_files = sorted([i for i in files if '*' + i not in self.file_buffer] + list(self.file_buffer.keys()))
        for f in new_files:
            self.list_files['menu'].add_command(label=f, command=_setit(self.selected_file, f))

        return new_files

    def onchange_filecontent(self, *_):
        if not self._editor_dirty:
            self._editor_dirty = True
            self.dirty = True
            self.file_reload = False
            fname = self.selected_file.get().strip()
            fname = '*' + fname if '*' not in fname else fname
            self._dirty_file_name = fname
            self.file_buffer[self._dirty_file_name] = self.editor.get('1.0', END).strip()
            self.update_file_choices()
            self.selected_file.set(self._dirty_file_name)

    def clear(self, keep=False):
        self.file_buffer.clear()
        if not keep:
            self.editor.delete('1.0', END)
        self.dirty = False


class FilePickEdit(Frame):

    def __init__(self, master, file_mask, default_file, edit_height=None, user_onChange=None, rename_on_edit=0, font=None, coloring=True, allowNone=False, highlighter=None, directory='.'):
        """
            file_mask: file mask (e.g. "*.foo") or list of file masks (e.g. ["*.foo", "*.abl"])
        """
        self.master = master
        self.directory = directory
        self.user_onChange = user_onChange
        Frame.__init__(self, master)
        row = 0
        self.unmodified = True
        self.allowNone = allowNone
        self.file_extension = ''
        if type(file_mask) != list:
            file_mask = [
             file_mask]
        if '.' in file_mask[0]:
            self.file_extension = file_mask[0][file_mask[0].rfind('.'):]
        self.file_mask = file_mask
        self.updateList()
        self.list_frame = Frame(self)
        self.list_frame.grid(row=row, column=0, sticky='WE')
        self.list_frame.columnconfigure(0, weight=1)
        self.picked_name = StringVar()
        self.makelist()
        self.refresh_button = Button(self.list_frame, text='<- refresh', command=self.refresh, height=1)
        self.refresh_button.grid(row=0, column=1, sticky='E')
        self.save_button = Button(self.list_frame, text='save', command=self.save, height=1)
        self.save_button.grid(row=0, column=2, sticky='E')
        row += 1
        if coloring:
            self.editor = SyntaxHighlightingText(self, self.onEdit, highlighter=highlighter)
        else:
            self.editor = ScrolledText2(self, self.onEdit)
        if font is not None:
            self.editor.configure(font=font)
        if edit_height is not None:
            self.editor.configure(height=edit_height)
        self.editor.grid(row=row, column=0, sticky='NEWS')
        self.rowconfigure(row, weight=1)
        self.columnconfigure(0, weight=1)
        row += 1
        self.options_frame = Frame(self)
        self.options_frame.grid(row=row, column=0, sticky=W)
        self.rename_on_edit = IntVar()
        self.cb = Checkbutton(self.options_frame, text='rename on edit', variable=self.rename_on_edit)
        self.cb.pack(side=LEFT)
        self.cb.configure(command=self.onChangeRename)
        self.rename_on_edit.set(rename_on_edit)
        row += 1
        self.filename_frame = Frame(self)
        self.filename_frame.grid(row=row, column=0, sticky='WE')
        self.filename_frame.columnconfigure(0, weight=1)
        self.save_name = StringVar()
        self.save_edit = Entry(self.filename_frame, textvariable=self.save_name)
        self.save_edit.grid(row=0, column=0, sticky='WE')
        self.save_name.trace('w', self.onSaveChange)
        self.select(default_file)
        self.row = row

    def setDirectory(self, directory, keep=False):
        self.directory = directory
        self.updateList()
        self.makelist()
        if not keep:
            self.select('')

    def refresh(self):
        sel = self.get()
        self.updateList()
        self.select(sel, notify=False)

    def reloadFile(self):
        self.editor.delete('1.0', END)
        filename = self.picked_name.get()
        if os.path.exists(os.path.join(self.directory, filename)):
            new_text = open(os.path.join(self.directory, filename)).read()
            if new_text.strip() == '':
                new_text = '// %s is empty\n' % filename
            new_text = new_text.replace('\r', '')
        else:
            new_text = ''
        self.editor.insert(INSERT, new_text)

    def setText(self, txt):
        """
        Replaces the text in the edit field as by typing
        into it.
        """
        self.select('')
        if txt.strip() == '':
            txt = '// empty database\n'
        self.editor.insert(INSERT, txt)
        self.onEdit()

    def onSelChange(self):
        self.reloadFile()
        filename = self.picked_name.get()
        self.save_name.set(filename)
        self.save_edit.configure(state=DISABLED)
        self.unmodified = True
        if self.user_onChange is not None:
            self.user_onChange(filename)

    def onSaveChange(self, name, index, mode):
        pass

    def autoRename(self):
        filename = self.picked_name.get()
        if filename == '':
            filename = 'new' + self.file_extension
        ext = ''
        extpos = filename.rfind('.')
        if extpos != -1:
            ext = filename[extpos:]
        base = filename[:extpos]
        hpos = base.rfind('-')
        num = 0
        if hpos != -1:
            try:
                num = int(base[hpos + 1:])
                base = base[:hpos]
            except:
                pass

        while 1:
            num += 1
            filename = '%s-%d%s' % (base, num, ext)
            if not os.path.exists(filename):
                break

        self.save_name.set(filename)
        if self.user_onChange is not None:
            self.user_onChange(filename)

    def onEdit(self):
        if self.unmodified:
            self.unmodified = False
            if self.rename_on_edit.get() == 1 or self.picked_name.get() == '':
                self.autoRename()
            self.save_edit.configure(state=NORMAL)

    def onChangeRename(self):
        if self.rename_on_edit.get() == 1:
            if not self.unmodified and self.save_name.get() == self.picked_name.get():
                self.autoRename()
        else:
            self.save_name.set(self.picked_name.get())

    def updateList(self):
        self.files = []
        if self.allowNone:
            self.files.append('')
        if os.path.exists(self.directory):
            for filename in os.listdir(self.directory):
                for fm in self.file_mask:
                    if fnmatch(filename, fm):
                        self.files.append(filename)

        self.files.sort()
        if len(self.files) == 0 and not self.allowNone:
            self.files.append('(no %s files found)' % str(self.file_mask))

    def select(self, filename, notify=True):
        """ selects the item given by filename """
        if filename in self.files:
            if not havePMW:
                self.picked_name.set(filename)
            else:
                self.list.selectitem(self.files.index(filename))
                if notify:
                    self.onSelChange(filename)
        else:
            self.editor.delete('1.0', END)

    def makelist(self):
        if havePMW:
            self.list = ComboBox(self.list_frame, selectioncommand=self.onSelChange, scrolledlist_items=self.files)
            self.list.grid(row=0, column=0, padx=0, pady=0, sticky='NEWS')
            self.list.component('entryfield').component('entry').configure(state='readonly', relief='raised')
            self.picked_name = self.list
        else:
            self.list = OptionMenu(*(self.list_frame, self.picked_name) + tuple(self.files))
            self.list.grid(row=0, column=0, sticky='NEW')
            self.picked_name.trace('w', self.onSelChange)

    def save(self):
        self.get()

    def set(self, selected_item):
        self.select(selected_item)

    def get(self):
        """ gets the name of the currently selected file, saving it first if necessary """
        filename = self.save_name.get()
        if self.unmodified == False:
            self.unmodified = True
            f = open(os.path.join(self.directory, filename), 'w')
            f.write(self.editor.get('1.0', END).encode('utf-8'))
            f.close()
            self.refresh()
            self.select(filename, notify=False)
            self.save_edit.configure(state=DISABLED)
        return filename

    def get_text(self):
        return self.editor.get('1.0', END)

    def get_filename(self):
        return self.save_name.get()

    def set_enabled(self, state):
        self.editor.configure(state=state)
        if havePMW:
            self.list.component('entryfield_entry').configure(state=state)
            self.list.component('arrowbutton').bind('<1>', (lambda a: 'break') if state == DISABLED else self.list._postList)
        else:
            self.list.configure(state=state)
        self.save_button.configure(state=state)
        self.cb.configure(state=state)
        self.save_edit.configure(state=state)


class FilePick(Frame):

    def __init__(self, master, file_mask, default_file, user_onChange=None, font=None, dirs=('.', ), allowNone=False):
        """ file_mask: file mask or list of file masks """
        self.master = master
        self.user_onChange = user_onChange
        Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.unmodified = True
        self.file_extension = ''
        if '.' in file_mask:
            self.file_extension = file_mask[file_mask.rfind('.'):]
        if type(file_mask) != list:
            file_mask = [
             file_mask]
        self.file_masks = file_mask
        self.allowNone = allowNone
        self.dirs = dirs
        self.updateList()
        self.set(default_file)

    def onSelChange(self, name, index=0, mode=0):
        filename = self.picked_name.get()
        if self.user_onChange != None:
            self.user_onChange(filename)

    def updateList(self):
        prev_sel = self.get()
        self.files = []
        if self.allowNone:
            self.files.append('')
        for fm in self.file_masks:
            for dir in self.dirs:
                try:
                    for filename in os.listdir(dir):
                        if fnmatch(filename, fm):
                            if dir != '.':
                                path = os.path.join(dir, filename)
                            else:
                                path = filename
                            self.files.append(path)

                except:
                    pass

        self.files.sort()
        if len(self.files) == 0:
            self.files.append('(no %s files found)' % self.file_masks)
        self._makelist()
        self.set(prev_sel)

    def getList(self):
        """ returns the current list of files """
        return self.files

    def _makelist(self):
        if havePMW:
            self.list = ComboBox(self, selectioncommand=self.onSelChange, scrolledlist_items=self.files)
            self.list.grid(row=0, column=0, padx=0, sticky='NEWS')
            self.list.component('entryfield').component('entry').configure(state='readonly', relief='raised')
            self.picked_name = self.list
        else:
            self.picked_name = StringVar()
            self.list = OptionMenu(*(self, self.picked_name) + tuple(self.files))
            self.list.grid(row=0, column=0, sticky='NEW')
            self.picked_name.trace('w', self.onSelChange)

    def set(self, filename):
        default_file = filename
        if default_file in self.files:
            if not havePMW:
                self.picked_name.set(default_file)
        else:
            self.list.selectitem(self.files.index(default_file))
            self.onSelChange(default_file)

    def get(self):
        if not hasattr(self, 'picked_name'):
            return
        return self.picked_name.get()


class DropdownList:

    def __init__(self, master, filemask='*.mln', default=None, allowNone=False, onselchange=None, directory='.'):
        self.allowNone = allowNone
        self.directory = directory
        self.list_frame = master
        self.onchange = onselchange
        if type(filemask) != list:
            filemask = [
             filemask]
        self.file_mask = filemask
        self.updateList()
        if havePMW:
            self.list = ComboBox(master, selectioncommand=onselchange, scrolledlist_items=self.files)
            self.list.component('entryfield').component('entry').configure(state='readonly', relief='raised')
            self.picked_name = self.list
        else:
            self.picked_name = StringVar()
            self.list = OptionMenu(*(master, self.picked_name) + tuple(self.files))
            if onselchange is not None:
                self.picked_name.trace('w', self.onchange)
            if default is not None:
                self.select(default)
            else:
                self.select(self.files[0])

    def __getattr__(self, name):
        return getattr(self.list, name)

    def get(self):
        return self.picked_name.get()

    def select(self, item):
        if item in self.files:
            if not havePMW:
                self.picked_name.set(item)
        else:
            self.list.selectitem(item)

    def updateList(self):
        self.files = []
        if self.allowNone:
            self.files.append('')
        if os.path.exists(self.directory):
            for filename in os.listdir(self.directory):
                for fm in self.file_mask:
                    if fnmatch(filename, fm):
                        self.files.append(filename)

        self.files.sort()
        if len(self.files) == 0 and not self.allowNone:
            self.files.append('(no %s files found)' % str(self.file_mask))

    def makelist(self):
        if havePMW:
            self.list = ComboBox(self.list_frame, selectioncommand=self.onSelChange, scrolledlist_items=self.files)
            self.list.grid(row=0, column=0, padx=0, pady=0, sticky='NEWS')
            self.list.component('entryfield').component('entry').configure(state='readonly', relief='raised')
            self.picked_name = self.list
        else:
            self.list = OptionMenu(*(self.list_frame, self.picked_name) + tuple(self.files))
            self.list.grid(row=0, column=0, sticky='NEW')
            self.picked_name.trace('w', self.onSelChange)
        self.select(self.files[0])

    def setDirectory(self, directory, keep=False):
        self.directory = directory
        self.updateList()
        self.makelist()
        if not keep:
            self.select('')

    def onSelChange(self, name, index=0, mode=0):
        filename = self.picked_name.get()
        if self.onchange != None:
            self.onchange(filename)


class Checkbox(Checkbutton):

    def __init__(self, master, text, default=None, **args):
        self.var = IntVar()
        Checkbutton.__init__(self, master, text=text, variable=self.var, **args)
        if default is not None:
            self.var.set(default)

    def get(self):
        return self.var.get()