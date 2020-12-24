# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/etk/docking/dockstore.py
# Compiled at: 2011-01-20 15:25:35
from __future__ import absolute_import
import sys
from simplegeneric import generic
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import gtk
from .docklayout import DockLayout
from .dockframe import DockFrame
from .dockpaned import DockPaned
from .dockgroup import DockGroup
from .dockitem import DockItem
SERIALIZABLE = (
 DockFrame, DockPaned, DockGroup, DockItem)

def serialize(layout):

    def _ser(widget, element):
        if isinstance(widget, SERIALIZABLE):
            sub = SubElement(element, type(widget).__name__.lower(), attributes(widget))
            widget.foreach(_ser, sub)
        else:
            sub = SubElement(element, 'widget', attributes(widget))

    tree = Element('layout')
    map(_ser, layout.frames, [tree] * len(layout.frames))
    return tostring(tree, encoding=sys.getdefaultencoding())


widget_factory = {}

def deserialize(layoutstr, itemfactory):
    """
    Return a new layout with it's attached frames. Frames that should be floating
    already have their gtk.Window attached (check frame.get_parent()). Transient settings
    and such should be done by the invoking application.
    """

    def _des--- This code section failed: ---

 L.  62         0  LOAD_FAST             0  'element'
                3  LOAD_ATTR             0  'tag'
                6  LOAD_CONST               'widget'
                9  COMPARE_OP            2  ==
               12  POP_JUMP_IF_FALSE    69  'to 69'

 L.  63        15  LOAD_FAST             0  'element'
               18  LOAD_ATTR             1  'attrib'
               21  LOAD_CONST               'name'
               24  BINARY_SUBSCR    
               25  STORE_FAST            2  'name'

 L.  64        28  LOAD_DEREF            0  'itemfactory'
               31  LOAD_FAST             2  'name'
               34  CALL_FUNCTION_1       1  None
               37  STORE_FAST            3  'widget'

 L.  65        40  LOAD_FAST             3  'widget'
               43  LOAD_ATTR             2  'set_name'
               46  LOAD_FAST             2  'name'
               49  CALL_FUNCTION_1       1  None
               52  POP_TOP          

 L.  66        53  LOAD_FAST             1  'parent_widget'
               56  LOAD_ATTR             3  'add'
               59  LOAD_FAST             3  'widget'
               62  CALL_FUNCTION_1       1  None
               65  POP_TOP          
               66  JUMP_FORWARD         97  'to 166'

 L.  68        69  LOAD_GLOBAL           4  'widget_factory'
               72  LOAD_FAST             0  'element'
               75  LOAD_ATTR             0  'tag'
               78  BINARY_SUBSCR    
               79  STORE_FAST            4  'factory'

 L.  69        82  LOAD_FAST             4  'factory'
               85  LOAD_CONST               'parent'
               88  LOAD_FAST             1  'parent_widget'
               91  LOAD_FAST             0  'element'
               94  LOAD_ATTR             1  'attrib'
               97  CALL_FUNCTION_KW_256   256  None
              100  STORE_FAST            3  'widget'

 L.  70       103  LOAD_FAST             3  'widget'
              106  POP_JUMP_IF_TRUE    122  'to 122'
              109  LOAD_ASSERT              AssertionError
              112  LOAD_CONST               'No widget (%s)'
              115  LOAD_FAST             3  'widget'
              118  BINARY_MODULO    
              119  RAISE_VARARGS_2       2  None

 L.  71       122  LOAD_GLOBAL           6  'len'
              125  LOAD_FAST             0  'element'
              128  CALL_FUNCTION_1       1  None
              131  POP_JUMP_IF_FALSE   166  'to 166'

 L.  72       134  LOAD_GLOBAL           7  'map'
              137  LOAD_DEREF            1  '_des'
              140  LOAD_FAST             0  'element'
              143  LOAD_FAST             3  'widget'
              146  BUILD_LIST_1          1 
              149  LOAD_GLOBAL           6  'len'
              152  LOAD_FAST             0  'element'
              155  CALL_FUNCTION_1       1  None
              158  BINARY_MULTIPLY  
              159  CALL_FUNCTION_3       3  None
              162  POP_TOP          
              163  JUMP_FORWARD          0  'to 166'
            166_0  COME_FROM           163  '163'
            166_1  COME_FROM            66  '66'

 L.  73       166  LOAD_FAST             3  'widget'
              169  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 169

    tree = fromstring(layoutstr)
    layout = DockLayout()
    map(_des, tree, [layout] * len(tree))
    return layout


def get_main_frames(layout):
    return (f for f in layout.frames if not isinstance(f.get_parent(), gtk.Window))


def finish--- This code section failed: ---

 L.  90         0  LOAD_FAST             1  'main_frame'
                3  LOAD_ATTR             0  'get_toplevel'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            2  'main_window'

 L.  92        12  SETUP_LOOP           96  'to 111'
               15  LOAD_FAST             0  'layout'
               18  LOAD_ATTR             1  'frames'
               21  GET_ITER         
               22  FOR_ITER             85  'to 110'
               25  STORE_FAST            3  'frame'

 L.  93        28  LOAD_FAST             3  'frame'
               31  LOAD_FAST             1  'main_frame'
               34  COMPARE_OP            8  is
               37  POP_JUMP_IF_FALSE    46  'to 46'

 L.  94        40  CONTINUE             22  'to 22'
               43  JUMP_FORWARD          0  'to 46'
             46_0  COME_FROM            43  '43'

 L.  96        46  LOAD_FAST             3  'frame'
               49  LOAD_ATTR             2  'get_parent'
               52  CALL_FUNCTION_0       0  None
               55  STORE_FAST            4  'parent'

 L.  98        58  LOAD_FAST             4  'parent'
               61  POP_JUMP_IF_FALSE    22  'to 22'

 L.  99        64  LOAD_GLOBAL           3  'isinstance'
               67  LOAD_FAST             4  'parent'
               70  LOAD_GLOBAL           4  'gtk'
               73  LOAD_ATTR             5  'Window'
               76  CALL_FUNCTION_2       2  None
               79  POP_JUMP_IF_TRUE     91  'to 91'
               82  LOAD_ASSERT              AssertionError
               85  LOAD_FAST             4  'parent'
               88  RAISE_VARARGS_2       2  None

 L. 100        91  LOAD_FAST             4  'parent'
               94  LOAD_ATTR             7  'set_transient_for'
               97  LOAD_FAST             2  'main_window'
              100  CALL_FUNCTION_1       1  None
              103  POP_TOP          
              104  JUMP_BACK            22  'to 22'
              107  JUMP_BACK            22  'to 22'
              110  POP_BLOCK        
            111_0  COME_FROM            12  '12'

Parse error at or near `POP_BLOCK' instruction at offset 110


def parent_attributes(widget):
    """
    Add properties defined in the parent widget specific for this instance (like weight).
    """
    container = widget.get_parent()
    d = {}
    if isinstance(container, DockPaned):
        paned_item = [ i for i in container._items if i.child is widget ][0]
        if paned_item.weight:
            d['weight'] = str(int(paned_item.weight * 100))
    return d


@generic
def attributes(widget):
    raise NotImplementedError


@attributes.when_type(gtk.Widget)
def widget_attributes(widget):
    return {'name': widget.get_name() or 'empty'}


@attributes.when_type(DockItem)
def dock_item_attributes(widget):
    d = {'title': widget.props.title, 'tooltip': widget.props.title_tooltip_text}
    if widget.props.icon_name:
        d['icon_name'] = widget.props.icon_name
    if widget.props.stock:
        d['stock_id'] = widget.props.stock
    return d


@attributes.when_type(DockGroup)
def dock_group_attributes(widget):
    d = parent_attributes(widget)
    name = widget.get_name()
    if name != widget.__gtype__.name:
        d['name'] = name
    return d


@attributes.when_type(DockPaned)
def dock_paned_attributes(widget):
    return dict(orientation=(widget.get_orientation() == gtk.ORIENTATION_HORIZONTAL and 'horizontal' or 'vertical'), **parent_attributes(widget))


@attributes.when_type(DockFrame)
def dock_frame_attributes(widget):
    a = widget.allocation
    d = dict(width=str(a.width), height=str(a.height))
    parent = widget.get_parent()
    if isinstance(parent, gtk.Window) and parent.get_transient_for():
        d['floating'] = 'true'
        d['x'], d['y'] = map(str, parent.get_position())
    return d


def factory(typename):
    """
    Simple decorator for populating the widget_factory dictionary.
    """

    def _factory(func):
        widget_factory[typename] = func
        return func

    return _factory


@factory('dockitem')
def dock_item_factory(parent, title, tooltip, icon_name=None, stock_id=None, pos=None, vispos=None, current=None, name=None):
    item = DockItem(title, tooltip, icon_name, stock_id)
    if name:
        item.set_name(name)
    if pos:
        pos = int(pos)
    if vispos:
        vispos = int(vispos)
    parent.insert_item(item, pos, vispos)
    return item


@factory('dockgroup')
def dock_group_factory(parent, weight=None, name=None):
    group = DockGroup()
    if name:
        group.set_name(name)
    if weight is not None:
        parent.insert_item(group, weight=float(weight) / 100.0)
    else:
        parent.add(group)
    return group


@factory('dockpaned')
def dock_paned_factory(parent, orientation, weight=None, name=None):
    paned = DockPaned()
    if name:
        paned.set_name(name)
    if orientation == 'horizontal':
        paned.set_orientation(gtk.ORIENTATION_HORIZONTAL)
    else:
        paned.set_orientation(gtk.ORIENTATION_VERTICAL)
    if weight is not None:
        item = parent.insert_item(paned, weight=float(weight) / 100.0)
    else:
        parent.add(paned)
    return paned


@factory('dockframe')
def dock_frame_factory--- This code section failed: ---

 L. 216         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'parent'
                6  LOAD_GLOBAL           1  'DockLayout'
                9  CALL_FUNCTION_2       2  None
               12  POP_JUMP_IF_TRUE     24  'to 24'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_FAST             0  'parent'
               21  RAISE_VARARGS_2       2  None

 L. 218        24  LOAD_GLOBAL           3  'DockFrame'
               27  CALL_FUNCTION_0       0  None
               30  STORE_FAST            6  'frame'

 L. 219        33  LOAD_FAST             6  'frame'
               36  LOAD_ATTR             4  'set_size_request'
               39  LOAD_GLOBAL           5  'int'
               42  LOAD_FAST             1  'width'
               45  CALL_FUNCTION_1       1  None
               48  LOAD_GLOBAL           5  'int'
               51  LOAD_FAST             2  'height'
               54  CALL_FUNCTION_1       1  None
               57  CALL_FUNCTION_2       2  None
               60  POP_TOP          

 L. 220        61  LOAD_FAST             0  'parent'
               64  LOAD_ATTR             6  'add'
               67  LOAD_FAST             6  'frame'
               70  CALL_FUNCTION_1       1  None
               73  POP_TOP          

 L. 222        74  LOAD_FAST             3  'floating'
               77  LOAD_CONST               'true'
               80  COMPARE_OP            2  ==
               83  POP_JUMP_IF_FALSE   164  'to 164'

 L. 223        86  LOAD_GLOBAL           7  'gtk'
               89  LOAD_ATTR             8  'Window'
               92  LOAD_GLOBAL           7  'gtk'
               95  LOAD_ATTR             9  'WINDOW_TOPLEVEL'
               98  CALL_FUNCTION_1       1  None
              101  STORE_FAST            7  'window'

 L. 225       104  LOAD_FAST             7  'window'
              107  LOAD_ATTR            10  'set_property'
              110  LOAD_CONST               'skip-taskbar-hint'
              113  LOAD_GLOBAL          11  'True'
              116  CALL_FUNCTION_2       2  None
              119  POP_TOP          

 L. 226       120  LOAD_FAST             7  'window'
              123  LOAD_ATTR            12  'move'
              126  LOAD_GLOBAL           5  'int'
              129  LOAD_FAST             4  'x'
              132  CALL_FUNCTION_1       1  None
              135  LOAD_GLOBAL           5  'int'
              138  LOAD_FAST             5  'y'
              141  CALL_FUNCTION_1       1  None
              144  CALL_FUNCTION_2       2  None
              147  POP_TOP          

 L. 227       148  LOAD_FAST             7  'window'
              151  LOAD_ATTR             6  'add'
              154  LOAD_FAST             6  'frame'
              157  CALL_FUNCTION_1       1  None
              160  POP_TOP          
              161  JUMP_FORWARD          0  'to 164'
            164_0  COME_FROM           161  '161'

 L. 229       164  LOAD_FAST             6  'frame'
              167  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 167