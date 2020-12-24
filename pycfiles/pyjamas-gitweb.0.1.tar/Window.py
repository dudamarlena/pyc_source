# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/Window.py
# Compiled at: 2008-09-04 10:42:46
__doc__ = "\n    Window provides access to the DOM model's global Window.\n"
import pygtk
pygtk.require('2.0')
import gtk
from pyjamas.__pyjamas__ import JS, doc, get_main_frame, wnd
import Location
closingListeners = []
resizeListeners = []

def addWindowCloseListener(listener):
    global closingListeners
    closingListeners.append(listener)


def addWindowResizeListener(listener):
    global resizeListeners
    resizeListeners.append(listener)


def alert(msg):
    wnd().alert(msg)


def confirm(msg):
    print 'TODO', msg
    alert('Window.confirm() is still on the TODO list. sorry!')
    return False
    JS('\n    window.confirm("%s");\n    ' % msg)


def enableScrolling(enable):
    doc().props.body.props.style.overflow = enable and 'auto' or 'hidden'
    JS("\n    $doc.body.style.overflow = enable ? 'auto' : 'hidden';\n    ")


def getClientHeight():
    height = wnd().props.inner_height
    if height:
        return height
    return doc().props.body.props.client_height


def getClientWidth():
    width = wnd().props.inner_width
    if width:
        return width
    return doc().props.body.props.client_width


location = None

def getLocation():
    global location
    if not location:
        print dir(wnd())
        location = Location.Location(wnd().props.location)
    return location
    JS('\n    if(!Window_location)\n       Window_location = Location_Location($wnd.location);\n    return Window_location;\n    ')


def getTitle():
    return doc.props.title


def open(url, name, features):
    JS("\n    document.parent.open('%s', '%s', '%s');\n    " % (url, name, features))


def removeWindowCloseListener(listener):
    closingListeners.remove(listener)


def removeWindowResizeListener(listener):
    resizeListeners.remove(listener)


def setMargin(size):
    doc().props.body.props.style.margin = size


def setTitle(title):
    doc().props.title = title


def onClosed():
    fireClosedImpl()


def onClosing():
    fireClosingImpl()


def onResize():
    fireResizedImpl()


def fireClosedAndCatch(handler):
    pass


def fireClosedImpl():
    for listener in closingListeners:
        listener.onWindowClosed()


def fireClosingAndCatch(handler):
    pass


def resize(width, height):
    print 'resize', width, height
    wnd().resize_to(width, height)
    wnd().resize_by(width, height)


def fireClosingImpl():
    ret = None
    for listener in closingListeners:
        msg = listener.onWindowClosing()
        if ret == None:
            ret = msg

    return ret


def fireResizedAndCatch(handler):
    pass


def fireResizedImpl():
    for listener in resizeListeners:
        listener.onWindowResized(getClientWidth(), getClientHeight())