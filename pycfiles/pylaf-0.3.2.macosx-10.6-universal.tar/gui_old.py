# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.6/site-packages/PyLAF/gui_old.py
# Compiled at: 2011-03-19 21:52:53
import weakref, inspect, platform, types, re, functools, threading, Queue, time, utils.gui, core, utils.functions
from functools import partial
from utils.gui.tkwidgets import *
from scipy import log10

def classname(obj):
    return repr(obj.__class__).split('.')[(-1)].split(' ')[0]


class Projection:

    class Through:

        @classmethod
        def forward(cls, x):
            return x

        @classmethod
        def backward(cls, x):
            return x

    class INV:

        @classmethod
        def forward(cls, x):
            return 1.0 / x

        @classmethod
        def backward(cls, x):
            return 1.0 / x

    class DB:

        @classmethod
        def forward(cls, x):
            return 10.0 * log10(x)

        @classmethod
        def backward(cls, x):
            return 10.0 ** (x / 10.0)


class Entry(Tkinter.Entry):

    def __init__(self, master=None, format='%s', range=None, projection=Projection.Through, cnf={}, **kw):
        Tkinter.Entry.__init__(self, master, cnf, **kw)
        self.projection = projection
        self.format = format
        self.old = None
        self.range = range
        self.value = core.Port('').bind(self._forward)
        self.bind('<Escape>', self._forward)
        self.bind('<Return>', self._backward)
        self.bind('<FocusOut>', self._forward)
        return

    def _forward(self, *args):
        self.delete(0, len(self.get()))
        self.insert(0, self.format % self.projection.forward(self.value.get()))

    def _backward(self, *args):
        old = self.projection.forward(self.value.get())
        try:
            new = type(self.value.get())(self.get())
        except ValueError:
            new = type(self.value.get())('0')

        if self.range:
            if not self.range(new):
                new = old
        self.value.set(self.projection.backward(new))


class EntryTable(Tkinter.Frame):

    def __init__(self, master=None, row=1, column=1, format='%s', rowlabel=None, columnlabel=None, cnf={}, **kw):
        Tkinter.Frame.__init__(self, master, cnf, **kw)
        self.value = core.Port([ [ '' for c in range(column) ] for r in range(row) ]).bind(self._forward)
        self.joint = []
        self.row = row
        self.column = column
        if columnlabel:
            if type(columnlabel) == str:
                for j in range(column):
                    Label(self, text=re.sub('%d', '%d' % (j + 1), columnlabel)).grid(row=0, column=j + 1)

            else:
                for (j, label) in enumerate(columnlabel):
                    Label(self, text=label).grid(row=0, column=j + 1)

        if rowlabel:
            if type(rowlabel) == str:
                for i in range(row):
                    Label(self, text=re.sub('%d', '%d' % (i + 1), rowlabel)).grid(row=i + 1, column=0)

            else:
                for (i, label) in enumerate(rowlabel):
                    Label(self, text=label).grid(row=i + 1, column=0)

        for i in range(row):
            joint = []
            for j in range(column):
                joint.append(core.Port('').bind(functools.partial(self._backward, i=i, j=j)))
                w = Entry(self, name='item%d%d' % (i, j), format=format)
                w.grid(row=i + 1, column=j + 1, sticky=Tkinter.W + Tkinter.E)
                joint[(-1)].link(w.value)

            self.joint.append(joint)

    def _forward(self):
        self._forward_called = True
        value = self.value.get()
        for i in range(self.row):
            for j in range(self.column):
                if i >= len(value) or j >= len(value[0]):
                    self.joint[i][j].set(0)
                else:
                    self.joint[i][j].set(value[i][j])

        del self._forward_called

    def _backward(self, i, j):
        try:
            self._forward_called
        except AttributeError:
            value = self.value.get()
            if i < len(value) and j < len(value[0]):
                value[i][j] = self.joint[i][j].get()
                self.value.set(value)


class MultipleEntries(Tkinter.Frame):

    def __init__(self, master=None, name=None, column=2, projection=None, frameoption={}, cnf={}, **kw):
        Tkinter.Frame.__init__(self, master, name=name, cnf=frameoption)
        self.value = core.Port([ '' for i in range(column) ]).bind(self._forward)
        self.mode = core.Port(None).bind(self._forward)
        self.joint = []
        self.column = column
        self.projection = projection
        for i in range(column):
            self.joint.append(core.Port('').bind(self._backward))
            w = Entry(self, name=('item%d' % i), cnf=cnf, **kw)
            w.grid(row=0, column=i)
            self.joint[(-1)].link(w.value)

        return

    def _forward(self):
        value = self.value.get()[:self.column]
        if self.projection:
            forward = self.projection[self.mode.get()][0]
            value = forward(value)
        for (o, v) in zip(self.joint, value):
            o.set(v)

    def _backward(self):
        value = [ o.get() for o in self.joint ]
        if self.projection:
            backward = self.projection[self.mode.get()][1]
            value = backward(value)
        self.value.set(value)


class Label(Tkinter.Label):

    def __init__(self, master=None, format='%s', cnf={}, **kw):
        Tkinter.Label.__init__(self, master, cnf, **kw)
        self.format = format
        self.value = core.Port('').bind(self.updated)

    def updated(self):
        self.configure(text=self.format % self.value.get())


class LabelTable(Tkinter.Frame):

    def __init__(self, master=None, name=None, row=1, column=1, rowlabel=None, columnlabel=None, width=None, cnf={}, **kw):
        Tkinter.Frame.__init__(self, master, name=name)
        self.value = core.Port([ [ '' for c in range(column) ] for r in range(row) ]).bind(self._forward)
        self.joint = []
        self.row = row
        self.column = column
        if columnlabel:
            if type(columnlabel) == str:
                for j in range(column):
                    Label(self, text=re.sub('%d', '%d' % (j + 1), columnlabel)).grid(row=0, column=j + 1)

            else:
                for (j, label) in enumerate(columnlabel):
                    Label(self, text=label).grid(row=0, column=j + 1)

        if rowlabel:
            if type(rowlabel) == str:
                rowlabel = [ re.sub('%d', '%d' % (i + 1), rowlabel) for i in range(row) ]
            for (i, label) in enumerate(rowlabel):
                w = Label(self, text=label)
                w.grid(row=i + 1, column=0)
                w.configure(anchor=Tkinter.W)
                if width:
                    w.configure(width=width[0])

        for i in range(row):
            joint = []
            for j in range(column):
                joint.append(core.Port(''))
                w = Label(self, name=('item%d%d' % (i, j)), cnf=cnf, **kw)
                w.grid(row=i + 1, column=j + 1, sticky=Tkinter.W + Tkinter.E)
                w.configure(anchor=Tkinter.W)
                if width:
                    w.configure(width=width[(j + 1)])
                joint[(-1)].link(w.value)

            self.joint.append(joint)

    def _forward(self):
        value = self.value.get()
        for i in range(self.row):
            for j in range(self.column):
                if i >= len(value) or j >= len(value[0]):
                    self.joint[i][j].set(0)
                else:
                    self.joint[i][j].set(value[i][j])


class Button(Tkinter.Button):
    """クリックすると登録したコールバックを起動する。コールバックは通常のTkinter.Buttonと同様にcommand=<method>オプションで指定できる。"""

    def __init__(self, master=None, cnf={}, **kw):
        Tkinter.Button.__init__(self, master, cnf, **kw)
        self.value = core.Port(None)
        self.configure(command=lambda : self.value.set(self.value.get()))
        return


class ToggleButton(Tkinter.Button):

    def __init__(self, master=None, text=None, cnf={}, **kw):
        Tkinter.Button.__init__(self, master, cnf, **kw)
        self.value = core.Port(0)
        self.configure(command=self._clicked)
        if not type(text) == str:
            self.configure(text=text[0])
            self.text = text
        else:
            self.configure(text=text)

    def _clicked(self):
        if self.value.get() + 1 < len(self.text):
            value = self.value.get() + 1
        else:
            value = 0
        self.configure(text=self.text[value])
        self.value.set(value)


class TrigButton(Tkinter.Button):

    def __init__(self, master=None, cnf={}, **kw):
        Tkinter.Button.__init__(self, master, cnf, **kw)
        self.value = core.Port(None)
        self.configure(command=self._backward)
        return

    def _backward(self):
        self.configure(state=Tkinter.DISABLED)
        self.value.set(None)
        self.configure(state=Tkinter.NORMAL)
        return


class LatchButton(Tkinter.Button):

    def __init__(self, master=None, cnf={}, **kw):
        Tkinter.Button.__init__(self, master, cnf, **kw)
        self.value = core.Port(True)
        self.value.bind(self._forward)
        self.configure(command=self._backward)

    def _backward(self):
        self.configure(state=Tkinter.DISABLED)
        self.value.set(False)

    def _forward(self):
        if self.value.get():
            self.configure(state=Tkinter.NORMAL)
        else:
            self.configure(state=Tkinter.DISABLED)


class Radiobuttons(Tkinter.Frame, utils.gui.SyncVarPort):

    def __init__(self, master=None, modes=[], cnf={}, **kw):
        Tkinter.Frame.__init__(self, master, cnf, **kw)
        self.var = v = Tkinter.StringVar()
        for (text, key) in modes:
            Tkinter.Radiobutton(self, text=text, variable=v, value=key, command=self._backward).pack(anchor=Tkinter.W)

        self.value = core.Port(None)
        self.value.bind(self._forward)
        return


class Checkbutton(Tkinter.Frame, utils.gui.SyncVarPort):

    def __init__(self, master=None, cnf={}, **kw):
        Tkinter.Frame.__init__(self, master, cnf, **kw)
        self.var = v = Tkinter.IntVar()
        Tkinter.Checkbutton(self, variable=v, command=self._backward).pack(anchor=Tkinter.W)
        self.value = core.Port(0).bind(self._forward)


class Menu(Tkinter.Menu):
    (TYPE_CASCADE, TYPE_ITEM) = range(2)
    ITEMS = []

    def __init__(self, master=None, cnf={}, **kw):
        Tkinter.Menu.__init__(self, master, cnf, **kw)
        self.callback = []
        self.make()

    def make(self, items=None):
        if not items:
            items = self.__class__.ITEMS
        for child in items:
            self.add_child(self, child)

    def remove_empty_items(self, cascade):
        length = cascade.len()
        for index in range(length):
            if cascade.type(index) == 'cascade':
                label = cascade.entrycget(index, 'label')
                menu = cascade.nametowidget(cascade.entrycget(index, 'menu'))
                self.remove_empty_items(menu)
                if utils.isfamily(menu, ChildrenMenu):
                    continue
                if menu.len() == 0:
                    cascade.delete(index)

    def itemtype(self, item):
        cls = self.__class__
        if len(item) == 1:
            return cls.TYPE_CASCADE
        if type(item[1]) == list:
            return cls.TYPE_CASCADE
        if repr(type(item[1])) == "<type 'classobj'>":
            return cls.TYPE_CASCADE
        if type(item[1]) == dict:
            return cls.TYPE_ITEM

    def parse_cascade(self, item):
        if len(item) == 1:
            return (item[0], None)
        else:
            if type(item[1]) == list:
                return (item[0], item[1:])
            if repr(type(item[1])) == "<type 'classobj'>":
                return (item[0], item[1])
            return

    def add_child(self, parent, child):

        def nocommand(command=None, **kw):
            return kw

        cls = self.__class__
        itemtype = self.itemtype(child)
        if itemtype == cls.TYPE_CASCADE:
            (label, item) = self.parse_cascade(child)
            index = self.labeltoindex(label)
            if index == None:
                if not repr(type(item)) == "<type 'classobj'>":
                    cascade = Menu(parent, name=label.lower())
                    parent.add_cascade(label=label, menu=cascade)
                    parent = cascade
            else:
                old = self.item(label)
                if old == None:
                    self.delete(index)
                    if not repr(type(item)) == "<type 'classobj'>":
                        cascade = Menu(parent, name=label.lower())
                        parent.add_cascade(label=label, menu=cascade)
                        parent = cascade
                else:
                    parent = old
            if item == None:
                pass
            elif repr(type(item)) == "<type 'classobj'>":
                parent.add_cascade(label=label, menu=item(parent, name=label.lower()))
            elif type(item) == list:
                for o in item:
                    self.add_child(parent, o)

        elif itemtype == cls.TYPE_ITEM:
            (name, kwargs) = child
            if kwargs.has_key('command'):
                if type(kwargs['command']) == str:
                    command = getattr(self, kwargs['command'])
                    getattr(parent, name)(command=command, **nocommand(**kwargs))
                    return
            getattr(parent, name)(**kwargs)
        return

    def assign(self, component):
        self.comp = weakref.ref(component)
        for key in self.children:
            child = self.children[key]
            if utils.functions.isfamily(child, Menu):
                child.assign(component)

    def component(self, path=None):
        if not path:
            return self.comp()
        ids = path.split('.')
        child = self.comp()
        for id in ids:
            child = child.children[id]

        return child

    def labeltoindex(self, label):
        index = 0
        while index == self.index(index):
            if label == self.entrycget(index, 'label'):
                return index
            index = index + 1

    def len(self):
        index = 0
        while index == self.index(index):
            index = index + 1

        return index

    def item(self, label):
        index = self.labeltoindex(label)
        if not index:
            return
        return self.nametowidget(self.entrycget(index, 'menu'))


class ChildrenMenu(Menu):

    def assign(self, component):
        Menu.assign(self, component)
        self.update_children()

    def update_children(self):
        try:
            self.comp
        except AttributeError:
            return

        component = self.component()
        if component == None:
            del self.comp
            return
        else:
            children = component.children.copy()
            existence = [ '%s:%s' % (key, classname(children[key])) for key in children ]
            remove = []
            for index in range(self.len()):
                label = self.entrycget(index, 'label')
                flag = False
                for s in existence:
                    if s == label:
                        flag = True
                        break

                if not flag:
                    remove.append(index)

            for index in remove:
                self.delete(index)

            for s in existence:
                flag = False
                for index in range(self.len()):
                    label = self.entrycget(index, 'label')
                    if s == label:
                        flag = True
                        break

                if flag:
                    continue
                self.add_command(label=s, command=partial(self.popup, label=s))

            self.after(500, self.update_children)
            return

    def popup(self, label):
        key = label.split(':')[0]
        object = self.component(key)
        tk = self
        while tk:
            tk = tk.master

        Layout.Application(Tkinter.Toplevel(tk), object, sync=False)


class FileMenu(Menu):
    ITEMS = []
    RESTS = [
     [
      'add_command', utils.kw(label='Config', command='popup_config')],
     [
      'add_command', utils.kw(label='Console', command='popup_console')]]

    def make_rest(self):
        cls = self.__class__
        if not self.len() == 0:
            self.add_separator()
        self.make(cls.RESTS)

    def popup_config(self):
        component = self.component()
        if self.children.has_key('config'):
            return
        try:
            component.Config
        except AttributeError:
            pass
        else:
            component.Config(master=Tkinter.Toplevel(self, name='config'), name='config').pack()
            self.children['config'].children['config'].assign(component)

    def popup_console(self):
        component = self.component()
        if self.children.has_key('console'):
            return
        try:
            component.Console
        except AttributeError:
            pass
        else:
            component.Console(master=Tkinter.Toplevel(self, name='console'), name='console').pack()
            self.children['console'].children['console'].assign(component)


class DefaultMenu(Menu):
    DEFAULT_ITEMS = [
     [
      'PyLAF'],
     [
      'File', FileMenu],
     [
      'Edit'],
     [
      'Children', ChildrenMenu]]
    ITEMS = []

    def __init__(self, master=None, desc=[], cnf={}, **kw):
        cls = self.__class__
        ITEMS = cls.ITEMS
        cls.ITEMS = []
        Menu.__init__(self, master, cnf, **kw)
        self.make(cls.DEFAULT_ITEMS)
        self.make(ITEMS)
        self.make_rest(self.children)
        self.remove_empty_items(self)

    def make_rest(self, children):
        for key in children:
            child = children[key]
            if utils.isfamily(child, Menu):
                try:
                    make_rest = getattr(child, 'make_rest')
                except AttributeError:
                    continue
                else:
                    make_rest()
                    self.make_rest(child.children)


class ComponentWithGUI(core.Component, utils.gui.WithGUI):
    """
    GUIを付随するコンポーネント
    ユーザコンポーネントを拡張する際のテンプレート
    destroy()が複数回実行されるのを避けるコードを含む
    """

    def __init__(self, master=None, name=None):
        core.Component.__init__(self, master, name)
        utils.gui.WithGUI.__init__(self)

    def destroy(self):
        if self._dying:
            return
        self._dying = True
        utils.gui.WithGUI.destroy(self)
        core.Component.destroy(self)


class Grid(Tkinter.Frame):

    def __init__(self, master=None, cnf={}, **kw):
        Tkinter.Frame.__init__(self, master, cnf, **kw)
        self.__geometry = core.kw(sticky=Tkinter.W + Tkinter.E)
        self.__label_widget = {}
        self.__label_geometry = core.kw(sticky=Tkinter.W + Tkinter.E)

    def append(self, widget, label=None, geometry={}, label_widget={}, label_geometry={}):
        u"""
        widgetを最終行にgridする。labelが設定されていればラベル付きでウィジェットを配置する。
        ラベルのアクセスidはlabel+row(label0,label1,...)
        geometry:ウィジェット配置オプション。row,rowspan,column,columnspanは無効。
        label_widget：ラベル生成オプション。masterは無効。
        label_geometry:ラベル配置オプション。row,rowspan,column,columnspanは無効。
        """

        def remove_options(kwargs, *options):
            for key in options:
                if kwargs.has_key(key):
                    del kwargs[key]

            return kwargs

        def update_options(default, custom):
            for key in custom:
                default[key] = custom[key]

            return default

        _geometry = update_options(self.__geometry.copy(), remove_options(geometry, 'row', 'rowspan', 'column', 'columnspan'))
        _label_widget = update_options(self.__label_widget.copy(), remove_options(label_widget, 'master'))
        _label_geometry = update_options(self.__label_geometry.copy(), remove_options(label_geometry, 'row', 'rowspan', 'column', 'columnspan'))
        (col, row) = self.grid_size()
        if label:
            Tkinter.Label(self, text=label, name=('label%d' % row), **_label_widget).grid(row=row, column=0, **_label_geometry)
            widget.grid(row=row, column=1, **_geometry)
        else:
            widget.grid(row=row, column=0, columnspan=2, **_geometry)


class Layout:

    class Utilities:

        def widget(self, path):
            ids = path.split('.')
            child = self
            for id in ids:
                child = child.children[id]

            return child

        def component(self, path=None):
            if not path:
                return self.comp()
            ids = path.split('.')
            child = self.comp()
            for id in ids:
                child = child.children[id]

            return child

        def _assign(self, comp, key):
            try:
                self.children[key].assign
            except (KeyError, AttributeError):
                pass
            else:
                self.children[key].assign(comp)

    class Embed(Tkinter.LabelFrame, Utilities):

        def __init__(self, master=None, cls=None, console=False, alignment='vertical', cnf={}, **kw):
            Tkinter.LabelFrame.__init__(self, master, cnf, **kw)
            if alignment == 'vertical':
                packw = {'side': Tkinter.TOP}
            elif alignment == 'horizontal':
                packw = {'side': Tkinter.LEFT, 'anchor': Tkinter.N}
            try:
                cls.Plot
            except AttributeError:
                pass
            else:
                cls.Plot(master=self, name='plot').pack(**packw)

            self.make_menu(cls)

        def make_menu(self, cls):
            try:
                cls.Menu
            except AttributeError:
                klass = DefaultMenu
            else:
                klass = cls.Menu

            menu = klass(master=self, name='menu')
            index = menu.labeltoindex('PyLAF')
            if not index == None:
                menu.delete(index)
            self.bind('<Control-Button-1>', self._rclicked)
            if platform.system() == 'Darwin':
                self.bind('<Button-2>', self._rclicked)
            else:
                self.bind('<Button-3>', self._rclicked)
            return

        def assign(self, comp):
            if comp == None:

                class Dummy:
                    pass

                self.comp = weakref.ref(Dummy())
            else:
                self.comp = weakref.ref(comp)
            self._assign(comp, 'plot')
            self._assign(comp, 'menu')
            return self

        def popup_config(self):
            if self.children.has_key('config'):
                return
            try:
                self.comp().Config
            except AttributeError:
                pass
            else:
                self.comp().Config(master=Tkinter.Toplevel(self, name='config'), name='config').pack()
                self.children['config'].children['config'].assign(self.comp())

            if self.children.has_key('console'):
                return
            self.comp().Console(master=self.children['config'].children['config'], name='console').pack()
            self.children['config'].children['config'].children['console'].assign(self.comp())

        def _rclicked(self, e):
            self.children['menu'].tk_popup(e.x_root, e.y_root)

    class EmbedWithConsole(Embed, Utilities):

        def __init__(self, master=None, cls=None, alignment='vertical', cnf={}, **kw):
            Tkinter.LabelFrame.__init__(self, master, cnf, **kw)
            if alignment == 'vertical':
                packw = {'side': Tkinter.TOP}
            elif alignment == 'horizontal':
                packw = {'side': Tkinter.LEFT, 'anchor': Tkinter.N}
            try:
                cls.Plot
            except AttributeError:
                pass
            else:
                cls.Plot(master=self, name='plot').pack(**packw)

            try:
                cls.Console
            except AttributeError:
                pass
            else:
                cls.Console(master=self, name='console').pack(**packw)

            self.make_menu(cls)

        def assign(self, comp):
            if comp == None:

                class Dummy:
                    pass

                self.comp = weakref.ref(Dummy())
            else:
                self.comp = weakref.ref(comp)
            self._assign(comp, 'plot')
            self._assign(comp, 'console')
            self._assign(comp, 'menu')
            return self

    class Application(Tkinter.Frame, Utilities):

        def __init__(self, master=None, klass=None, title=None, sync=True, pack=True, alignment='vertical', cnf={}, **kw):
            Tkinter.Frame.__init__(self, master, cnf, **kw)
            if type(klass) == types.InstanceType:
                instance = klass
                klass = klass.__class__
            if alignment == 'vertical':
                packw = {'side': Tkinter.TOP}
            elif alignment == 'horizontal':
                packw = {'side': Tkinter.LEFT, 'anchor': Tkinter.N}
            try:
                klass.Plot
            except AttributeError:
                pass
            else:
                klass.Plot(master=self, name='plot').pack(**packw)

            try:
                klass.Console
            except AttributeError:
                pass
            else:
                klass.Console(master=self, name='console').pack(**packw)

            try:
                klass.Status
            except AttributeError:
                pass
            else:
                klass.Status(master=self, name='status').pack()

            try:
                klass.Menu
            except AttributeError:
                self.master.config(menu=DefaultMenu(master=self, name='menu'))
            else:
                self.master.config(menu=klass.Menu(master=self, name='menu'))

            self._sync = sync
            self._dying = False
            try:
                instance
            except UnboundLocalError:
                pass
            else:
                self.assign(instance)

            if title:
                self.master.title(title)
            if pack:
                self.pack()

        def assign(self, comp):
            if comp == None:

                class Dummy:
                    pass

                self.comp = weakref.ref(Dummy())
            else:
                self.comp = weakref.ref(comp)
                comp._guis[repr(id(self))] = self
            self._assign(comp, 'plot')
            self._assign(comp, 'console')
            self._assign(comp, 'status')
            self._assign(comp, 'menu')
            return self

        def popup_config(self):
            if self.children.has_key('config'):
                return
            try:
                self.comp().Config
            except AttributeError:
                pass
            else:
                self.comp().Config(master=Tkinter.Toplevel(self, name='config'), name='config').pack()
                self.children['config'].children['config'].assign(self.comp())

        def destroy(self):
            if self._dying:
                return
            else:
                self._dying = True
                try:
                    self.comp
                except AttributeError:
                    Tkinter.Frame.destroy(self)
                    return
                else:
                    comp = self.comp()
                    if not comp == None:
                        if self._sync:
                            if comp._dying == True:
                                self.master.destroy()
                            else:
                                comp.destroy()

                Tkinter.Frame.destroy(self)
                return


class Thread(threading.Thread):
    (EVENT_START, EVENT_CANCEL, EVENT_DONE, STATE_DONE, STATE_COMPUTING, STATE_CANCELED, STATE_RUNNING) = range(7)

    class StateCanceled(Exception):
        pass

    class SafeBuffer(Tkinter.Frame):

        def __init__(self, master=None, interval=200, cnf={}, **kw):
            Tkinter.Frame.__init__(self, master, cnf, **kw)
            self.receive = core.Port(None).bind(self._set)
            self.send = core.Port(None)
            self.interval = core.Port(interval)
            self._last = None
            self._polling()
            return

        def _set(self):
            self._last = self.receive.get()

        def _polling(self):
            if not self._last == None:
                self.send.set(self._last)
                self._last = None
            self.after(self.interval.get(), self._polling)
            return

    class SafeQueue(Tkinter.Frame):

        def __init__(self, master=None, cnf={}, **kw):
            Tkinter.Frame.__init__(self, master, cnf, **kw)
            self.receive = core.Port(None).bind(self._set)
            self.send = core.Port(None)
            self._queue = Queue.Queue()
            self._polling()
            return

        def _set(self):
            self._queue.put(self.receive.get())

        def _polling(self):
            try:
                while 1:
                    self.send.set(self._queue.get_nowait())

            except Queue.Empty:
                pass

            self.after(200, self._polling)

    class LatchedTriggerButton(Tkinter.Button):

        def __init__(self, master=None, cnf={}, **kw):
            Tkinter.Button.__init__(self, master, cnf, **kw)
            self.thread = core.Port(None)
            self.remote = core.Port(None).bind(self._forward)
            self._thread = threading.Thread(target=self._run)
            self._state = False
            self.configure(command=self._backward)
            return

        def _run(self):
            self.thread.set(Thread.EVENT_START)
            self.remote.set(Thread.EVENT_DONE)

        def _backward(self):
            if not self._state:
                self.activate()
            else:
                self.deactivate()

        def _forward(self):
            remote = self.remote.get()
            if remote == Thread.EVENT_DONE:
                self.deactivate()
            elif remote == Thread.EVENT_START:
                self.activate()
            elif remote == Thread.EVENT_CANCEL:
                self.deactivate()

        def activate(self):
            self.configure(state=Tkinter.DISABLED)
            self._state = True
            self._thread.start()

        def deactivate(self):
            self.configure(state=Tkinter.NORMAL)
            self._state = False
            self._thread = threading.Thread(target=self._run)

    class TriggerButton(Tkinter.Button):

        def __init__(self, master=None, text=['Waiting', 'Running'], cnf={}, **kw):
            Tkinter.Button.__init__(self, master, cnf, **kw)
            self.thread = core.Port(None)
            self.cancel = core.Port(None)
            self.remote = core.Port(None).bind(self._forward)
            self._thread = threading.Thread(target=self._run)
            self._state = False
            self._text = text
            self.configure(command=self._backward)
            self.configure(text=text[0])
            return

        def _run(self):
            self.thread.set(Thread.EVENT_START)
            self.cancel.set(Thread.EVENT_DONE)
            self.remote.set(Thread.EVENT_DONE)

        def _backward(self):
            if not self._state:
                self.activate()
            else:
                self.cancel.set(Thread.EVENT_CANCEL)
                self.deactivate()

        def _forward(self, remote=None):
            if remote == None:
                remote = self.remote.get()
            if remote == Thread.EVENT_DONE:
                self.deactivate()
            elif remote == Thread.EVENT_START:
                self.activate()
            elif remote == Thread.EVENT_CANCEL:
                self.cancel.set(Thread.EVENT_CANCEL)
                self.deactivate()
            return

        def activate(self):
            self.configure(text=self._text[1])
            self._state = True
            self._thread.setDaemon(True)
            self._thread.start()
            self.cancel.set(Thread.STATE_RUNNING)

        def deactivate(self):
            self.configure(text=self._text[0])
            self._state = False
            self._thread = threading.Thread(target=self._run)


if __name__ == '__main__':

    class BasicSample(ComponentWithGUI):

        class Console(Grid):

            def __init__(self, master=None, cnf={}, **kw):
                Grid.__init__(self, master, cnf={}, **kw)
                self.append(Entry(self, name='param1'), label='A =')
                self.append(Label(self, name='param2'), label='2 x A =', label_geometry=core.kw(sticky=Tkinter.E))
                self.append(WeakValuedButton(self, name='callback', text='callback'))
                self.append(WeakValuedButton(self, name='destroy', text='destroy'))
                self.append(Tkinter.Button(self, name='cwtest', text='cwtest'))
                self.append(Tkinter.Button(self, name='rebind', text='rebind', command=core.CallWrapper(self._rebind)))

            def assign(self, component):
                self.children['param1'].value.set(component.param1.get())
                component.param1.link(self.children['param1'].value)
                self.children['param2'].value.set(component.param2.get())
                component.param2.link(self.children['param2'].value)
                self.children['callback'].configure(command=component.cb1)
                self.children['destroy'].configure(command=component.destroy)
                self.children['cwtest'].configure(command=core.CallWrapper(component.cb1))

            def _rebind(self):
                self.assign(BasicSample(core.Root()))

        def __init__(self, master=None, name=None):
            ComponentWithGUI.__init__(self, master, name)
            self.param1 = core.Port(1.0)
            self.param1.bind(self.calc)
            self.param2 = core.Port(0.0)

        def calc(self):
            self.param2.set(2 * self.param1.get())

        def cb1(self):
            print 'alive'


    tk = Tkinter.Tk()
    basic = Layout.Application(tk, BasicSample(core.Root()), title='basic sample', sync=False)
    Tkinter.mainloop()
    basic = weakref.ref(basic)
    print 'basic:', basic