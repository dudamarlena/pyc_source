# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\traits102\tktrait_sheet.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
import sys, os.path, re, Tkinter as tk, tkMessageBox as mb, tkSimpleDialog as sd, tkColorChooser as cc, Pmw, tkFont
from traits import Trait, HasTraits, TraitError, HasDynamicTraits, trait_editors
from trait_sheet import TraitEditor, TraitSheetHandler, TraitMonitor, TraitGroup, TraitGroupList, default_trait_sheet_handler
from types import DictType, ListType, TupleType, ModuleType, StringType, FloatType
trait_editors(__name__)
TRUE = 1
FALSE = 0
basic_sequence_types = [
 ListType, TupleType]
standard_bitmap_width = 120
WHITE = '#FFFFFF'
color_choices = (0, 128, 192, 255)
color_samples = [None] * 48
i = 0
for r in color_choices:
    for g in color_choices:
        for b in (0, 128, 255):
            color_samples[i] = '#%02X%02X%02X' % (r, g, b)
            i += 1

facenames = None
point_sizes = [
 '8', '9', '10', '11', '12', '14', '16', '18',
 '20', '22', '24', '26', '28', '36', '48', '72']
tooltips_enabled = TRUE
all_digits = re.compile('\\d+')

class TraitSheetDialog(tk.Toplevel):

    def __init__(self, object, traits=None, handler=default_trait_sheet_handler, parent=None, title=None):
        if title is None:
            title = '%s Traits' % object.__class__.__name__
        tk.Toplevel.__init__(self, parent)
        self.title(title)
        self.bind('<Destroy>', self.on_close_page)
        self.bind('<Escape>', self.on_close_key)
        self.object = object
        self.handler = handler
        TraitSheet(self, object, traits, handler).grid(row=0)
        if not handler.position(self, object):
            pass
        self.resizable(FALSE, FALSE)
        return

    def on_close_page(self, event):
        self.handler.close(self, self.object)

    def on_close_key(self):
        self.on_close_page()
        self.destroy()


class TraitPanel(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

    def add(self, sheet):
        pass

    def remove(self, sheet):
        pass

    def size(self):
        return (0, 0)

    def position(self, x, y, dx, dy):
        pass

    def destroy(self):
        pass


class TraitSheet(tk.Frame):

    def __init__(self, parent, object, traits=None, handler=default_trait_sheet_handler):
        tk.Frame.__init__(self, parent)
        self.object = object
        self.handler = handler
        self.tooltip = None
        if traits is None:
            traits = object.editable_traits()
        kind = type(traits)
        if kind == StringType:
            traits = TraitGroup(traits, show_border=FALSE)
        elif kind in basic_sequence_types or isinstance(traits, TraitGroupList):
            if len(traits) == 0:
                return
            if not isinstance(traits[0], TraitGroup):
                traits = TraitGroup(show_border=FALSE, *traits)
        if isinstance(traits, TraitGroup):
            self.add_page(traits, self)
        else:
            self.add_tabs(traits)
        return

    def add_tabs(self, traits):
        nb = Pmw.NoteBook(self)
        nb.grid(row=0, column=0, sticky='new')
        count = 0
        for pg in traits:
            page_name = pg.label
            if page_name is None:
                count += 1
                page_name = 'Page %d' % count
            self.add_page(pg, nb.add(page_name))

        nb.setnaturalsize()
        return

    def add_page(self, pg, parent, default_style='simple'):
        default_style = pg.style or default_style
        object = pg.object or self.object
        row_incr = col_incr = 0
        if pg.orientation == 'horizontal':
            col_incr = 1
        else:
            row_incr = 1
        show_labels = pg.show_labels_
        row = col = 0
        cols = 1 + show_labels
        for pge in pg.values:
            if isinstance(pge, TraitGroup):
                if pge.show_border_:
                    box = Pmw.Group(parent, tag_text=pge.label or '')
                    box.grid(row=row, column=col, sticky='new', padx=4)
                    frame = tk.Frame(box.interior())
                    frame.grid(row=0, column=0, sticky='news', padx=4, pady=3)
                    box.interior().columnconfigure(0, weight=1)
                    self.add_page(pge, frame, default_style)
                else:
                    self.add_page(pge, parent)
                if row_incr:
                    parent.columnconfigure(0, weight=1)
                row += row_incr
                col += col_incr
            else:
                name = pge.name or ' '
                if name == '-':
                    tk.Frame(parent, bg='#A0A0A0').grid(row=row, column=0, columnspan=cols, sticky='ew')
                    parent.rowconfigure(row, minsize=9)
                    row += 1
                    continue
                if name == ' ':
                    name = '5'
                if all_digits.match(name):
                    parent.rowconfigure(row, minsize=int(name))
                    row += 1
                    continue
                editor = pge.editor
                style = pge.style or default_style
                pge_object = pge.object or object
                if editor is None:
                    try:
                        editor = pge_object._base_trait(name).get_editor()
                    except:
                        pass

                if editor is None:
                    continue
                label = None
                if show_labels:
                    label = pge.label_for(object)
                self.add_trait(parent, row, object, name, label, editor, style == 'simple')
                parent.columnconfigure(1, weight=1)
                row += 1

        parent.rowconfigure(row, weight=1)
        return

    def add_trait(self, parent, row, object, trait_name, description, editor, is_simple):
        global tooltips_enabled
        col = 0
        if description is not None:
            suffix = ':'[description[-1:] == '?':]
            label = tk.Label(parent, text=(description + suffix).capitalize(), anchor='e')
            label.grid(row=row, sticky='new', padx=0, pady=2)
            col = 1
            desc = object._base_trait(trait_name).desc
            if desc is not None and tooltips_enabled:
                if self.tooltip is None:
                    self.tooltip = Pmw.Balloon(self, state='balloon')
                self.tooltip.bind(label, 'Specifies ' + desc)
                label.bind('<B2-ButtonRelease>', self.on_toggle_help)
        if is_simple:
            control = editor.simple_editor(object, trait_name, description, self.handler, parent)
            control.bind('<B2-ButtonRelease>', editor.on_restore)
        else:
            control = editor.custom_editor(object, trait_name, description, self.handler, parent)
        control.grid(row=row, column=col, sticky='ew', padx=4, pady=2)
        control.object = object
        control.trait_name = trait_name
        control.description = description
        control.original_value = getattr(object, trait_name)
        control.handler = self.handler
        return control

    def on_toggle_help(self, event):
        global tooltips_enabled
        tooltips_enabled = not tooltips_enabled
        if self.tooltip is not None:
            self.tooltip.configure(state=('none', 'balloon')[tooltips_enabled])
        return


class tkTraitEditor(TraitEditor):

    def simple_editor(self, object, trait_name, description, handler, parent):
        control = tk.Label(parent, text=self.str(object, trait_name), relief=tk.SUNKEN)
        control.object = object
        control.trait_name = trait_name
        control.description = description
        control.handler = handler
        control.original_value = getattr(object, trait_name)
        control.bind('<B1-ButtonRelease>', self.on_popup)
        control.bind('<3>', self.on_restore)
        return control

    def on_popup(self, event):
        control = event.widget
        if hasattr(self, 'popup_editor'):
            self.popup_editor(control.object, control.trait_name, control.description, control.handler, control)

    def on_restore(self, event):
        control = event.widget
        object = control.object
        trait_name = control.trait_name
        old_value = getattr(object, trait_name)
        new_value = control.original_value
        setattr(object, trait_name, new_value)
        control.handler.changed(object, trait_name, new_value, old_value, FALSE)
        self.update(object, trait_name, control)

    def update(self, object, trait_name, control):
        control.configure(text=self.str(object, trait_name))

    def error(self, description, excp, parent):
        mb.showerror(description + ' value error', str(excp))


class TraitEditorText(tkTraitEditor):

    def __init__(self, dic={}, auto_set=TRUE):
        self.dic = dic
        self.auto_set = auto_set

    def popup_editor(self, object, trait_name, description, handler, control):
        while TRUE:
            value = sd.askstring('Prompt', 'Enter the new %s value:' % trait_name, initialvalue=getattr(object, trait_name))
            if value is None:
                return
            if self.dic.has_key(value):
                value = self.dic[value]
            try:
                self.set(object, trait_name, value, handler)
                self.update(object, trait_name, control)
            except TraitError as excp:
                self.error(description, excp, object.window)

        return

    def simple_editor(self, object, trait_name, description, handler, parent):
        var = tk.StringVar()
        var.set(self.str(object, trait_name))
        control = tk.Entry(parent, textvariable=var)
        control.var = var
        control.value = self.get_value(control)
        control.bind('<Return>', self.on_enter)
        control.bind('<3>', self.on_restore)
        if self.auto_set:
            control.bind('<KeyRelease>', self.on_key)
        return control

    def update(self, object, trait_name, control):
        control.var.set(self.str(object, trait_name))
        control.configure(bg=WHITE)

    def on_enter(self, event):
        control = event.widget
        try:
            self.set(control.object, control.trait_name, self.get_value(control), control.handler)
        except TraitError as excp:
            self.error(control.description, excp, control)

    def on_key(self, event):
        control = event.widget
        value = self.get_value(control)
        if value != control.value:
            control.value = value
            try:
                setattr(control.object, control.trait_name, value)
                color = WHITE
            except:
                color = '#FFC0C0'

            control.configure(bg=color)

    def get_value(self, control):
        value = control.var.get().strip()
        if not self.dic.has_key(value):
            return value
        return self.dic[value]


class TraitEditorEnum(tkTraitEditor):

    def __init__(self, values, cols=1):
        self.cols = cols
        self.mapped = type(values) is DictType
        if self.mapped:
            sorted = values.values()
            sorted.sort()
            col = sorted[0].find(':') + 1
            if col > 0:
                self.sorted = [ x[col:] for x in sorted ]
                for n, v in values.items():
                    values[n] = v[col:]

            else:
                self.sorted = sorted
            self.values = values
        else:
            if type(values) not in basic_sequence_types:
                handler = values
                if isinstance(handler, Trait):
                    handler = handler.setter
                if hasattr(handler, 'map'):
                    values = handler.map.keys()
                    values.sort()
                else:
                    values = handler.values
            self.values = [ str(x) for x in values ]

    def simple_editor(self, object, trait_name, description, handler, parent):
        delegate = tkDelegate(self.on_value_changed)
        values = self.all_values()
        control = Pmw.ComboBox(parent, dropdown=TRUE, selectioncommand=delegate(), scrolledlist_items=values, listheight=min(150, len(values) * 24))
        delegate.control = control
        control.selectitem(self.current_value(object, trait_name))
        return control

    def custom_editor(self, object, trait_name, description, handler, parent):
        panel = tk.Frame(parent)
        cur_value = self.current_value(object, trait_name)
        values = self.all_values()
        n = len(values)
        cols = self.cols
        rows = (n + cols - 1) // cols
        var = tk.StringVar()
        delegate = tkDelegate(self.on_click, var=var, panel=panel)
        incr = [n // cols] * cols
        rem = n % cols
        for i in range(cols):
            incr[i] += rem > i

        incr[-1] = -(reduce(lambda x, y: x + y, incr[:-1], 0) - 1)
        index = 0
        for i in range(rows):
            for j in range(cols):
                value = values[index]
                control = tk.Radiobutton(panel, text=value.capitalize(), value=value, variable=var, command=delegate())
                control.grid(row=i, column=j, sticky='w')
                if value == cur_value:
                    var.set(value)
                index += incr[j]
                n -= 1
                if n <= 0:
                    break

        for j in range(cols):
            panel.columnconfigure(j, weight=1)

        return panel

    def all_values(self):
        if self.mapped:
            return self.sorted
        return self.values

    def current_value(self, object, trait_name):
        if self.mapped:
            return self.values[getattr(object, trait_name + '_')]
        return str(getattr(object, trait_name))

    def on_value_changed(self, delegate, value):
        control = delegate.control
        try:
            value = int(value)
        except:
            pass

        self.set(control.object, control.trait_name, value, control.handler)

    def on_click(self, delegate):
        panel = delegate.panel
        value = delegate.var.get()
        try:
            value = int(value)
        except:
            pass

        self.set(panel.object, panel.trait_name, value, panel.handler)


class TraitEditorImageEnum(TraitEditorEnum):

    def __init__(self, values, suffix='', cols=1, path=None):
        TraitEditorEnum.__init__(self, values)
        self.suffix = suffix
        self.cols = cols
        if type(path) is ModuleType:
            path = os.path.join(os.path.dirname(path.__file__), 'images')
        self.path = path

    def popup_editor(self, object, trait_name, description, handler, control):
        TraitEditorImageDialog(object, trait_name, description, control, handler, self)

    def simple_editor(self, object, trait_name, description, handler, parent):
        control = tk.Button(parent, image=bitmap_cache(self.current_value(object, trait_name) + self.suffix, self.path), bg=WHITE)
        control.configure(command=tkDelegate(self.on_popup, widget=control)())
        return control

    def custom_editor(self, object, trait_name, description, handler, parent):
        panel = tk.Frame(parent)
        panel.object = object
        panel.trait_name = trait_name
        panel.handler = handler
        self.create_image_grid(panel, self.on_click)
        return panel

    def create_image_grid(self, parent, handler):
        i = 0
        cols = self.cols
        for value in self.all_values():
            control = tk.Button(parent, image=bitmap_cache(value + self.suffix, self.path), command=tkDelegate(handler, parent=parent, value=value)())
            control.grid(row=i // cols, column=i % cols, sticky='w', padx=2, pady=2)
            i += 1

        parent.columnconfigure(cols, weight=1)

    def update(self, object, trait_name, control):
        control.configure(image=bitmap_cache(self.current_value(object, trait_name) + self.suffix, self.path))

    def on_click(self, delegate):
        parent = delegate.parent
        self.set(parent.object, parent.trait_name, delegate.value, parent.handler)


class TraitEditorCheckList(tkTraitEditor):

    def __init__(self, values, cols=1):
        self.cols = cols
        self.values = values
        if type(values[0]) is StringType:
            self.values = [ (x, x.capitalize()) for x in values ]
        self.mapping = mapping = {}
        for value, key in self.values:
            mapping[key] = value

    def simple_editor(self, object, trait_name, description, handler, parent):
        delegate = tkDelegate(self.on_value_changed)
        labels = self.all_labels()
        control = Pmw.ComboBox(parent, dropdown=TRUE, selectioncommand=delegate(), scrolledlist_items=labels, listheight=min(150, len(labels) * 24))
        delegate.control = control
        try:
            control.selectitem(self.all_values().index(self.current_value(object, trait_name)[0]))
        except:
            pass

        return control

    def custom_editor(self, object, trait_name, description, handler, parent):
        panel = tk.Frame(parent)
        cur_value = self.current_value(object, trait_name)
        labels = self.all_labels()
        values = self.all_values()
        n = len(values)
        cols = self.cols
        rows = (n + cols - 1) // cols
        incr = [n // cols] * cols
        rem = n % cols
        for i in range(cols):
            incr[i] += rem > i

        incr[-1] = -(reduce(lambda x, y: x + y, incr[:-1], 0) - 1)
        index = 0
        for i in range(rows):
            for j in range(cols):
                if n > 0:
                    value = values[index]
                    var = tk.IntVar()
                    delegate = tkDelegate(self.on_click, var=var, panel=panel, value=value)
                    control = tk.Checkbutton(panel, text=labels[index], variable=var, command=delegate())
                    control.grid(row=i, column=j, sticky='w')
                    var.set(value in cur_value)
                    index += incr[j]
                    n -= 1
                    if n <= 0:
                        break

        for j in range(cols):
            panel.columnconfigure(j, weight=1)

        return panel

    def all_labels(self):
        return [ x[1] for x in self.values ]

    def all_values(self):
        return [ x[0] for x in self.values ]

    def is_string(self, object, trait_name):
        return type(getattr(object, trait_name)) is StringType

    def current_value(self, object, trait_name):
        value = getattr(object, trait_name)
        if value is None:
            return []
        else:
            if type(value) is not StringType:
                return value
            return [ x.strip() for x in value.split(',') ]

    def on_value_changed(self, delegate, value):
        control = delegate.control
        value = self.mapping[value]
        if not self.is_string(control.object, control.trait_name):
            value = [
             value]
        self.set(control.object, control.trait_name, value, control.handler)

    def on_click(self, delegate):
        panel = delegate.panel
        value = delegate.value
        cur_value = self.current_value(panel.object, panel.trait_name)
        if delegate.var.get():
            cur_value.append(value)
        else:
            cur_value.remove(value)
        if self.is_string(panel.object, panel.trait_name):
            cur_value = (',').join(cur_value)
        self.set(panel.object, panel.trait_name, cur_value, panel.handler)


class TraitEditorBoolean(tkTraitEditor):

    def simple_editor(self, object, trait_name, description, handler, parent):
        var = tk.IntVar()
        control = tk.Checkbutton(parent, text='', variable=var, anchor='w')
        control.configure(command=tkDelegate(self.on_value_changed, control=control, var=var)())
        try:
            value = getattr(object, trait_name + '_')
        except:
            value = getattr(object, trait_name)

        var.set(value)
        return control

    def on_value_changed(self, delegate):
        control = delegate.control
        self.set(control.object, control.trait_name, delegate.var.get(), control.handler)


class TraitEditorRange(TraitEditorEnum):

    def __init__(self, handler, cols=1, auto_set=True):
        if isinstance(handler, Trait):
            handler = handler.setter
        self.low = handler.low
        self.high = handler.high
        self.cols = cols
        self.auto_set = auto_set
        self.is_float = type(self.low) is FloatType

    def simple_editor(self, object, trait_name, description, handler, parent):
        value = self.str(object, trait_name)
        var = tk.StringVar()
        var.set(value)
        if self.is_float or abs(self.high - self.low) > 1000:
            control = tk.Entry(parent, textvariable=var)
            control.var = var
            control.value = value
            control.bind('<Return>', self.on_enter)
            control.bind('<KeyRelease>', self.on_key)
            control.bind('<3>', self.on_restore)
        else:
            control = Pmw.Counter(parent)
            control.configure(datatype={'counter': self.on_value_changed, 
               'control': control, 
               'min_value': self.low, 
               'max_value': self.high})
            control._counterEntry.setentry(str(value))
        return control

    def custom_editor(self, object, trait_name, description, handler, parent):
        if abs(self.high - self.low) > 15:
            return self.simple_editor(object, trait_name, description, handler, parent)
        return TraitEditorEnum.custom_editor(self, object, trait_name, description, handler, parent)

    def all_values(self):
        return [ str(x) for x in xrange(self.low, self.high + 1) ]

    def current_value(self, object, trait_name):
        return str(getattr(object, trait_name))

    def update(self, object, trait_name, control):
        if isinstance(control, tk.Entry):
            control.var.set(self.str(object, trait_name))
            control.configure(bg=WHITE)
        else:
            control.entryfield.configure(text=str(getattr(object, trait_name)))

    def on_value_changed(self, value, factor, incr, control=None, min_value=None, max_value=None):
        value = min(max_value, max(min_value, int(value) + factor * incr))
        try:
            self.set(control.object, control.trait_name, value, control.handler)
            return str(value)
        except:
            raise ValueError

    def on_enter(self, event):
        control = event.widget
        try:
            self.set(control.object, control.trait_name, control.var.get().strip(), control.handler)
        except TraitError as excp:
            self.error(control.description, excp, control)

    def on_key(self, event):
        control = event.widget
        value = control.var.get()
        if value != control.value:
            control.value = value
            try:
                setattr(control.object, control.trait_name, value)
                color = WHITE
            except:
                color = '#FFC0C0'

            control.configure(bg=color)


class TraitEditorImageDialog(tk.Toplevel):

    def __init__(self, object, trait_name, description, control, handler, editor):
        tk.Toplevel.__init__(self, control)
        self.title('Choose ' + description)
        self.bind('<Escape>', self.on_close_key)
        self.object = object
        self.trait_name = trait_name
        self.control = control
        self.handler = handler
        self.editor = editor
        editor.create_image_grid(self, self.on_click)

    def on_close_key(self):
        self.destroy()

    def on_click(self, delegate):
        self.editor.set(self.object, self.trait_name, delegate.value, self.handler)
        self.editor.update(self.object, self.trait_name, self.control)
        self.destroy()


_bitmap_cache = {}
app_path = None
traits_path = None

def bitmap_cache(name, path=None):
    global app_path
    global traits_path
    if path is None:
        if traits_path is None:
            import traits
            traits_path = os.path.join(os.path.dirname(traits.__file__), 'images')
        path = traits_path
    elif path == '':
        if app_path is None:
            app_path = os.path.join(os.path.dirname(sys.argv[0]), '..', 'images')
        path = app_path
    filename = os.path.abspath(os.path.join(path, name.replace(' ', '_').lower() + '.gif'))
    bitmap = _bitmap_cache.get(filename)
    if bitmap is None:
        bitmap = _bitmap_cache[filename] = tk.PhotoImage(file=filename)
    return bitmap


standard_colors = {'aquamarine': '#70DB93', 
   'black': '#000000', 
   'blue': '#0000FF', 
   'blue violet': '#9F5F9F', 
   'brown': '#A52A2A', 
   'cadet blue': '#5F9F9F', 
   'coral': '#FF7F00', 
   'cornflower blue': '#42426F', 
   'cyan': '#00FFFF', 
   'dark green': '#2F4F2F', 
   'dark grey': '#2F2F2F', 
   'dark olive green': '#4F4F2F', 
   'dark orchid': '#9932CC', 
   'dark slate blue': '#6B238E', 
   'dark slate grey': '#2F4F4F', 
   'dark turquoise': '#7093DB', 
   'dim grey': '#545454', 
   'firebrick': '#8E2323', 
   'forest green': '#238E23', 
   'gold': '#CC7F32', 
   'goldenrod': '#DBDB70', 
   'green': '#00FF00', 
   'green yellow': '#93DB70', 
   'grey': '#808080', 
   'indian red': '#4F2F2F', 
   'khaki': '#9F9F5F', 
   'light blue': '#BFD8D8', 
   'light grey': '#C0C0C0', 
   'light steel': '#000000', 
   'lime green': '#32CC32', 
   'magenta': '#FF00FF', 
   'maroon': '#8E236B', 
   'medium aquamarine': '#32CC99', 
   'medium blue': '#3232CC', 
   'medium forest green': '#6B8E23', 
   'medium goldenrod': '#EAEAAD', 
   'medium orchid': '#9370DB', 
   'medium sea green': '#426F42', 
   'medium slate blue': '#7F00FF', 
   'medium spring green': '#7FFF00', 
   'medium turquoise': '#70DBDB', 
   'medium violet red': '#DB7093', 
   'midnight blue': '#2F2F4F', 
   'navy': '#23238E', 
   'orange': '#CC3232', 
   'orange red': '#FF007F', 
   'orchid': '#DB70DB', 
   'pale green': '#8FBC8F', 
   'pink': '#BC8FEA', 
   'plum': '#EAADEA', 
   'purple': '#B000FF', 
   'red': '#FF0000', 
   'salmon': '#6F4242', 
   'sea green': '#238E6B', 
   'sienna': '#8E6B23', 
   'sky blue': '#3299CC', 
   'slate blue': '#007FFF', 
   'spring green': '#00FF7F', 
   'steel blue': '#236B8E', 
   'tan': '#DB9370', 
   'thistle': '#D8BFD8', 
   'turquoise': '#ADEAEA', 
   'violet': '#4F2F4F', 
   'violet red': '#CC3299', 
   'wheat': '#D8D8BF', 
   'white': '#FFFFFF', 
   'yellow': '#FFFF00', 
   'yellow green': '#99CC32'}

def num_to_color(object, name, value):
    if type(value) is StringType:
        if len(value) == 7 and value[0] == '#' and eval('0x' + value[1:]) >= 0:
            return value
        raise TraitError
    return '#%06X' % int(value)


num_to_color.info = "a string of the form '#RRGGBB' or a number, which in hex is of the form 0xRRGGBB, where RR is red, GG is green, and BB is blue"

class TraitEditorColor(tkTraitEditor):

    def popup_editor(self, object, trait_name, description, handler, control):
        color = cc.askcolor(self.to_tk_color(object, trait_name))[1].upper()
        if color is not None:
            self.set(object, trait_name, self.from_tk_color(color), handler)
            self.update(object, trait_name, control)
        return

    def simple_editor(self, object, trait_name, description, handler, parent):
        control = tkTraitEditor.simple_editor(self, object, trait_name, description, handler, parent)
        self.update_color(object, trait_name, control)
        return control

    def custom_editor(self, object, trait_name, description, handler, parent):
        panel = tk.Frame(parent)
        panel.color = self.simple_editor(object, trait_name, description, handler, panel)
        panel.color.grid(row=0, column=0, sticky='nesw')
        panel2 = tk.Frame(panel)
        for i in range(len(color_samples)):
            tk.Button(panel2, bg=color_samples[i], font='Helvetica 1', command=tkDelegate(self.on_click, panel=panel, color=color_samples[i])()).grid(row=i // 12, column=i % 12, sticky='ew')

        for i in range(12):
            panel2.columnconfigure(i, weight=1)

        panel2.grid(row=0, column=1, sticky='nesw', padx=4)
        panel.columnconfigure(0, minsize=70)
        panel.columnconfigure(1, weight=1)
        return panel

    def on_click(self, delegate):
        panel = delegate.panel
        self.set(panel.object, panel.trait_name, self.from_tk_color(delegate.color), panel.handler)
        self.update(panel.object, panel.trait_name, panel.color)

    def update(self, object, trait_name, control):
        tkTraitEditor.update(self, object, trait_name, control)
        self.update_color(object, trait_name, control)

    def update_color(self, object, trait_name, control):
        bg_color = self.to_tk_color(object, trait_name)
        red = eval('0x%s' % bg_color[1:3])
        green = eval('0x%s' % bg_color[3:5])
        blue = eval('0x%s' % bg_color[5:7])
        fg_color = ('#FFFFFF', '#000000')[(red > 192 or green > 192 or blue > 192)]
        control.configure(bg=bg_color, fg=fg_color)

    def to_tk_color(self, object, trait_name):
        try:
            cur_color = getattr(object, trait_name + '_')
        except:
            cur_color = getattr(object, trait_name)

        if cur_color is None:
            return WHITE
        else:
            return cur_color

    def from_tk_color(self, color):
        return color


color_editor = TraitEditorColor()
color_trait = Trait('white', standard_colors, num_to_color, editor=color_editor)
clear_color_trait = Trait('clear', None, standard_colors, {'clear': None}, num_to_color, editor=color_editor)
slant_types = [
 'roman', 'italic']
weight_types = ['bold']
font_noise = ['pt', 'point', 'family']

def str_to_font(object, name, value):
    try:
        size = 10
        family = []
        slant = 'roman'
        weight = 'normal'
        underline = overstrike = 0
        for word in value.split():
            lword = word.lower()
            if lword in slant_types:
                slant = lword
            elif lword in weight_types:
                weight = lword
            elif lword == 'underline':
                underline = 1
            elif lword == 'overstrike':
                overstrike = 1
            elif lword not in font_noise:
                try:
                    size = int(lword)
                except:
                    family.append(word)

        if len(family) == 0:
            family = [
             'Helvetica']
        return tkFont.Font(family=(' ').join(family), size=size, weight=weight, slant=slant, underline=underline, overstrike=overstrike)
    except:
        pass

    raise TraitError


str_to_font.info = "a string describing a font (e.g. '12 pt bold italic' or 'Arial bold 14 point')"

class TraitEditorFont(tkTraitEditor):

    def simple_editor(self, object, trait_name, description, handler, parent):
        control = tkTraitEditor.simple_editor(self, object, trait_name, description, handler, parent)
        control.is_custom = FALSE
        self.update_font(object, trait_name, control)
        return control

    def custom_editor(self, object, trait_name, description, handler, parent):
        panel = tk.Frame(parent)
        font = panel.font = self.simple_editor(object, trait_name, description, handler, panel)
        font.configure(anchor='w')
        font.is_custom = TRUE
        font.grid(row=0, column=0, columnspan=2, sticky='ew', pady=3)
        delegate = tkDelegate(self.on_value_changed, panel=panel)
        values = self.all_facenames()
        panel.facename = control = Pmw.ComboBox(panel, dropdown=TRUE, selectioncommand=delegate(), scrolledlist_items=values, listheight=min(150, len(values) * 24))
        control.grid(row=1, column=0)
        panel.pointsize = control = Pmw.ComboBox(panel, dropdown=TRUE, selectioncommand=delegate(), scrolledlist_items=point_sizes)
        control.grid(row=1, column=1, padx=4)
        self.update_font(object, trait_name, font)
        return panel

    def update(self, object, trait_name, control):
        tkTraitEditor.update(self, object, trait_name, control)
        self.update_font(object, trait_name, control)

    def update_font(self, object, trait_name, control):
        cur_font = self.to_tk_font(object, trait_name)
        size = cur_font.cget('size')
        if control.is_custom:
            panel = control.master
            try:
                panel.facename.selectitem(cur_font.cget('family'))
            except:
                panel.facename.selectitem(0)

            try:
                panel.pointsize.selectitem(size)
            except:
                panel.pointsize.selectitem('10')

        cur_font.configure(size=min(10, size))
        control.configure(font=cur_font)

    def str(self, object, trait_name):
        font = getattr(object, trait_name)
        size = font.cget('size')
        family = font.cget('family')
        slant = font.cget('slant')
        weight = font.cget('weight')
        return '%s point %s %s %s' % (size, family, slant.capitalize(),
         weight.capitalize())

    def all_facenames(self):
        return ('Courier', 'Times', 'Helvetica', 'Arial', 'Verdana')

    def on_value_changed(self, delegate, unused):
        panel = delegate.panel
        size = panel.pointsize.get()
        family = panel.facename.get()
        font = tkFont.Font(family=family, size=size)
        self.set(panel.object, panel.trait_name, self.from_tk_font(font), panel.handler)
        self.update(panel.object, panel.trait_name, panel.font)

    def to_tk_font(self, object, trait_name):
        return getattr(object, trait_name)

    def from_tk_font(self, font):
        return font


font_trait = Trait('Arial 10', tkFont.Font, str_to_font, editor=TraitEditorFont())

class tkDelegate:

    def __init__(self, delegate=None, **kw):
        self.delegate = delegate
        for name, value in kw.items():
            setattr(self, name, value)

    def __call__(self):
        return self.on_event

    def on_event(self, *args):
        self.delegate(self, *args)