# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/GUITools.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 14516 bytes
import logging
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib, Pango
    from gi.repository.GdkPixbuf import Pixbuf, InterpType
except ImportError:
    import gtk as Gtk, glib as GLib, pango as Pango
    from gtk import gdk as Gdk

import webbrowser, lxml
F11 = Gdk.keyval_from_name('F11')

def PopupMenu(PopupMenuItems, Order):
    """
        Create popup menu according to specified dictionary.
        """
    Menu = Gtk.Menu()
    for Txt in Order:
        if isinstance(PopupMenuItems[Txt], tuple):
            SubMenuItems, SubOrder = PopupMenuItems[Txt]
            SubMenu = Gtk.Menu()
            Item = Gtk.ImageMenuItem(Txt)
            Item.set_submenu(SubMenu)
            Menu.append(Item)
            for SubTitle in SubOrder:
                SubItem = Gtk.ImageMenuItem(SubTitle)
                SubMenu.append(SubItem)
                Icon = SubMenuItems[SubTitle]['Icon']
                if Icon:
                    SubItem.set_image(Icon)
                    SubItem.set_always_show_image(True)
                SubItem.connect('activate', SubMenuItems[SubTitle]['Handler'], *SubMenuItems[SubTitle]['Args'])
                SubItem.show()

        else:
            MenuItem = Gtk.ImageMenuItem(Txt)
            Menu.append(MenuItem)
            MenuItem.connect('activate', PopupMenuItems[Txt]['Handler'], *PopupMenuItems[Txt]['Args'])
            Icon = PopupMenuItems[Txt]['Icon']
            if Icon:
                MenuItem.set_image(Icon)
                MenuItem.set_always_show_image(True)
            MenuItem.show()

    return Menu


def TreeView(Title, Columns, ColumnsOrder, DataTypes, DataOrder, Headers=True, Reorderable=False, Editable={}, Fg=None, Bg=None):
    """
        Activate 'from import' radio button.
        """
    Frame = Gtk.Frame(label=None)
    LB = Gtk.Label(None)
    LB.set_markup('<b>{0}</b>'.format(Title))
    Frame.set_label_widget(LB)
    Types = []
    for D in DataOrder:
        Types.append(DataTypes[D])

    ScrollArea = Gtk.ScrolledWindow()
    Frame.add(ScrollArea)
    M = Gtk.TreeStore(*Types)
    TreeView = Gtk.TreeView(model=M)
    ScrollArea.add_with_viewport(TreeView)
    TreeView.set_show_expanders(True)
    TreeView.set_level_indentation(0)
    TreeView.set_enable_tree_lines(True)
    TreeView.set_grid_lines(Gtk.TreeViewGridLines.NONE)
    TreeView.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
    if Reorderable:
        TreeView.set_reorderable(True)
    CellRenderers = {Pixbuf: Gtk.CellRendererPixbuf, 
     str: Gtk.CellRendererText, 
     int: Gtk.CellRendererSpin}
    Attributes = {Pixbuf: 'pixbuf', 
     str: 'text', 
     int: 'text'}
    for C in ColumnsOrder:
        Col = Gtk.TreeViewColumn(C)
        TreeView.append_column(Col)
        for Elmt in Columns[C]:
            ElmtType = DataTypes[Elmt]
            Cell = CellRenderers[ElmtType]()
            Col.pack_start(Cell, expand=False)
            Attr = {Attributes[ElmtType]: DataOrder.index(Elmt)}
            if Attributes[ElmtType] == 'text':
                if Fg:
                    Attr['foreground'] = Fg
                if Bg:
                    Attr['background'] = Bg
                Col.set_attributes(Cell, **Attr)
                if Elmt in Editable:
                    Cell.set_property('editable', True)
                    Cell.connect('edited', *Editable[Elmt])
                    if ElmtType == int:
                        Adjustment = Gtk.Adjustment(value=0, lower=-99999, upper=99999, step_incr=1, page_incr=10, page_size=0)
                        Cell.set_property('adjustment', Adjustment)

    TreeView.set_headers_visible(Headers)
    return (
     TreeView, Frame)


class FullScreenToggler:
    __doc__ = "\n\tSimple way to toggle fullscreen with F11 in PyGtk\n\t\n\tLet's start with how to pick up on the keypress: we need to connect to the key-press-event signal. \n\tBut we need something to connect it to, of course.\n\n\tThis something should keep track of the window state, \n\tso it makes sense to use a class that connects to the window-state-event\n\tsignal and keeps track of whether the window is full screen or not.\n\n\tSo we need an object that:\n\n\t    * Keeps track of the fullscreen/not-fullscreen state of a particular window, and\n\t    * Detects a keypress event and figures out what to do with it\n\n\tHow do we actually toggle the fullscreen state though? \n\t\tEasy, use the window.fullscreen() / window.unfullscreen() functions.\n\t-----------------------------------------------\n\tUSAGE:\n\t\tFSToggler = FullScreenToggler(window)\n\t\twindow.connect_object('key-press-event', FullScreenToggler.Toggle, FSToggler)\n\t-----------------------------------------------\n\tNOTE:\n\t\tThe use of connect_object instead of connect, which saves us adding an unused parameter.\n\t\t\n\t"

    def __init__(self, Window, Key=F11):
        """
                Initialize coordinate and type attributes.
                """
        self.Window = Window
        self.Key = Key
        self.WindowFullScreen = False
        self.Window.connect_object('window-state-event', FullScreenToggler.on_window_state_change, self)

    def on_window_state_change(self, event):
        """
                Initialize coordinate and type attributes.
                """
        self.WindowFullScreen = bool(Gdk.WindowState.FULLSCREEN & event.new_window_state)

    def Toggle(self, Event):
        """
                Initialize coordinate and type attributes.
                """
        logging.debug('FullScreen mode change event...')
        if Event.keyval == self.Key:
            if self.WindowFullScreen:
                logging.debug('Exit FullScreen mode')
                self.Window.unfullscreen()
        else:
            logging.debug('Enter FullScreen mode')
            self.Window.fullscreen()


def TextView(Editable=False):
    """
        Create a Gtk Textview.
        """
    ScrollArea = Gtk.ScrolledWindow()
    Textview = Gtk.TextView(buffer=None)
    ScrollArea.add_with_viewport(Textview)
    Textbuffer = Textview.get_buffer()
    Textview.set_editable(Editable)
    Textview.set_cursor_visible(True)
    Textview.set_wrap_mode(Gtk.WRAP_WORD)
    Textview.set_justification(Gtk.JUSTIFY_LEFT)
    Textview.set_left_margin(10)
    Textview.set_right_margin(10)
    Textbuffer.create_tag('Title', size_points=12, weight=Pango.WEIGHT_BOLD)
    Textbuffer.create_tag('BlueForeground', foreground='blue')
    Textbuffer.create_tag('RedForeground', foreground='red')
    Textbuffer.create_tag('Italic', style=Pango.STYLE_ITALIC)
    Textbuffer.create_tag('Bold', weight=Pango.WEIGHT_BOLD)
    Textbuffer.create_tag('Big', size=20 * Pango.SCALE)
    Textbuffer.create_tag('XXS', scale=Pango.SCALE_XX_SMALL)
    Textbuffer.create_tag('XL', scale=Pango.SCALE_X_LARGE)
    Textbuffer.create_tag('Monospace', family='monospace')
    gray50_width = 2
    gray50_height = 2
    gray50_bits = '\x02\x01'
    stipple = Gtk.gdk.bitmap_create_from_data(None, gray50_bits, gray50_width, gray50_height)
    Textbuffer.create_tag('StippleBg', background_stipple=stipple)
    Textbuffer.create_tag('StippleFg', foreground_stipple=stipple)
    Textbuffer.create_tag('DoubleInterLine', pixels_inside_wrap=10)
    Textbuffer.create_tag('NotEditable', editable=False)
    Textbuffer.create_tag('WordWrap', wrap_mode=Gtk.WRAP_WORD)
    Textbuffer.create_tag('CharWrap', wrap_mode=Gtk.WRAP_CHAR)
    Textbuffer.create_tag('NoWrap', wrap_mode=Gtk.WRAP_NONE)
    Textbuffer.create_tag('Center', justification=Gtk.JUSTIFY_CENTER)
    Textbuffer.create_tag('RightJustify', justification=Gtk.JUSTIFY_RIGHT)
    Textbuffer.create_tag('WideMargins', left_margin=50, right_margin=50)
    Textbuffer.create_tag('StrikeThrough', strikethrough=True)
    Textbuffer.create_tag('Underline', underline=Pango.UNDERLINE_SINGLE)
    Textbuffer.create_tag('DoubleUnderline', underline=Pango.UNDERLINE_DOUBLE)
    Textbuffer.create_tag('SuperScript', rise=10 * Pango.SCALE, size=8 * Pango.SCALE)
    Textbuffer.create_tag('SubScript', rise=-10 * Pango.SCALE, size=8 * Pango.SCALE)
    Textbuffer.create_tag('RtlQuote', wrap_mode=Gtk.WRAP_WORD, direction=Gtk.TEXT_DIR_RTL, indent=30, left_margin=20, right_margin=20)
    URLTag = Textbuffer.create_tag('URL', foreground='blue', underline=Pango.UNDERLINE_SINGLE)
    URLTag.connect('event', on_URLTag_clicked)
    Textbuffer._LinkTable = {}
    return (
     ScrollArea, Textview)


def on_URLTag_clicked(URLTag, TView, Event, Iter):
    """
        """
    if Event.type == Gtk.gdk.MOTION_NOTIFY:
        pass
    else:
        if Event.type == Gtk.gdk.BUTTON_PRESS:
            if Event.button == 1:
                StartIter = Iter
                StartIter.backward_to_tag_toggle(URLTag)
                EndIter = StartIter.copy()
                EndIter.forward_to_tag_toggle(URLTag)
                URLText = StartIter.get_text(EndIter)
                logging.info("Open link: '{0}'".format(URLText))
                webbrowser.open_new_tab(TView.get_buffer()._LinkTable[URLText])
        else:
            if Event.type == Gtk.gdk._2BUTTON_PRESS:
                pass
            else:
                if Event.type == Gtk.gdk._3BUTTON_PRESS:
                    pass
                else:
                    if Event.type == Gtk.gdk.BUTTON_RELEASE:
                        pass
                    elif not Event.type == Gtk.gdk.KEY_PRESS:
                        pass
    if Event.type == Gtk.gdk.KEY_RELEASE:
        pass
    return False


def DisplayMarkup(TextBuf, Text):
    """
        Display markup text in textbuffer
        """
    Tree = lxml.html.fromstring(html)
    for node in Tree.xpath(XPATH, namespaces={'re': EXSLT_NS}):
        node.drop_tree()

    print(lxml.html.tostring(Tree.body))
    Props = ParseMarkupString(Text)
    TextBuf.set_text(Props.text)
    tag_table = TextBuf.get_tag_table()
    for tag, start, end in Props:
        tag_table.add(tag)
        start_iter = TextBuf.get_iter_at_offset(start)
        end_iter = TextBuf.get_iter_at_offset(end)
        TextBuf.apply_tag(tag, start_iter, end_iter)

    return True


def ParseMarkupString(string):
    """
        Parses the string and returns a MarkupProps instance
        """
    attr_values = ('value', 'ink_rect', 'logical_rect', 'desc', 'color')
    attr_list, text, accel = Pango.parse_markup(string)
    attr_iter = attr_list.get_iterator()
    Props = MarkupProps()
    Props.text = text
    val = True
    while val:
        attrs = attr_iter.get_attrs()
        for attr in attrs:
            name = attr.type
            start = attr.start_index
            end = attr.end_index
            name = Pango.AttrType(name).value_nick
            value = None
            for attr_value in attr_values:
                if hasattr(attr, attr_value):
                    value = getattr(attr, attr_value)
                    break

            if name == 'font_desc':
                name = 'font'
            Props.add(name, value, start, end)

        val = next(attr_iter)

    return Tags


class MarkupProps:
    __doc__ = '\n\tStores properties that contain indices and appropriate values for that property.\n\tIncludes an iterator that generates GtkTextTags with the start and end indices to \n\tapply them to\n\t'

    def __init__(self):
        """
                properties = (  {   
                                'properties': {'foreground': 'green', 'background': 'red'}
                                'start': 0,
                                'end': 3
                            },
                            {
                                'properties': {'font': 'Lucida Sans 10'},
                                'start': 1,
                                'end':2,

                            },
                        )
                """
        self.properties = []
        self.text = ''

    def add(self, label, value, start, end):
        """
                Add a property to MarkupProps. If the start and end indices are already in
                a property dictionary, then add the property:value entry into
                that property, otherwise create a new one
                """
        for prop in self.properties:
            if prop['start'] == start and prop['end'] == end:
                prop['properties'].update({label: value})
            else:
                new_prop = {'properties': {label: value}, 
                 'start': start, 
                 'end': end}
                self.properties.append(new_prop)

    def __iter__(self):
        """
                Creates a GtkTextTag for each dict of properties
                Yields (TextTag, start, end)
                """
        for prop in self.properties:
            tag = Gtk.TextTag()
            tag.set_properties(**prop['properties'])
            yield (tag, prop['start'], prop['end'])