# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_msg.py
# Compiled at: 2012-06-09 14:19:29
"""
This module provides a light wrapping of a slightly modified pubsub module
to give it a lighter and simpler syntax for usage. It exports three main
methods. The first L{PostMessage} which is used to post a message for all
interested listeners. The second L{Subscribe} which allows an object to
subscribe its own listener function for a particular message type, all of
Editra's core message types are defined in this module using a naming
convention that starts each identifier with I{EDMSG_}. These identifier
constants can be used to identify the message type by comparing them with the
value of msg.GetType in a listener method. The third method is L{Unsubscribe}
which can be used to remove a listener from recieving messages.

@summary: Message system api and message type definitions

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_msg.py 71697 2012-06-08 15:20:22Z CJP $'
__revision__ = '$Revision: 71697 $'
__all__ = [
 'PostMessage', 'Subscribe', 'Unsubscribe']
from wx import PyDeadObjectError
from extern.pubsub import Publisher
EDMSG_ALL = ('editra', )
EDMSG_LOG_ALL = EDMSG_ALL + ('log', )
EDMSG_LOG_INFO = EDMSG_LOG_ALL + ('info', )
EDMSG_LOG_EVENT = EDMSG_LOG_INFO + ('evt', )
EDMSG_LOG_WARN = EDMSG_LOG_INFO + ('warn', )
EDMSG_LOG_ERROR = EDMSG_LOG_INFO + ('err', )
EDMSG_PROFILE_CHANGE = EDMSG_ALL + ('config', )
EDMSG_FILE_ALL = EDMSG_ALL + ('file', )
EDMSG_FILE_OPENING = EDMSG_FILE_ALL + ('opening', )
EDMSG_FILE_OPENED = EDMSG_FILE_ALL + ('opened', )
EDMSG_FILE_GET_OPENED = EDMSG_FILE_ALL + ('allopened', )
EDMSG_FILE_SAVE = EDMSG_FILE_ALL + ('save', )
EDMSG_FILE_SAVED = EDMSG_FILE_ALL + ('saved', )
EDMSG_UI_ALL = EDMSG_ALL + ('ui', )
EDMSG_UI_NB = EDMSG_UI_ALL + ('mnotebook', )
EDMSG_UI_MW_ACTIVATE = EDMSG_UI_ALL + ('mwactivate', )
EDMSG_UI_NB_CHANGING = EDMSG_UI_NB + ('pgchanging', )
EDMSG_UI_NB_CHANGED = EDMSG_UI_NB + ('pgchanged', )
EDMSG_UI_NB_CLOSING = EDMSG_UI_NB + ('pgclosing', )
EDMSG_UI_NB_CLOSED = EDMSG_UI_NB + ('pgclosed', )
EDMSG_UI_NB_TABMENU = EDMSG_UI_NB + ('tabmenu', )
EDMSG_PROGRESS_SHOW = EDMSG_UI_ALL + ('statbar', 'progbar', 'show')
EDMSG_PROGRESS_STATE = EDMSG_UI_ALL + ('statbar', 'progbar', 'state')
EDMSG_UI_SB_TXT = EDMSG_UI_ALL + ('statbar', 'text')
EDMSG_UI_STC_ALL = EDMSG_UI_ALL + ('stc', )
EDMSG_UI_STC_KEYUP = EDMSG_UI_STC_ALL + ('keyup', )
EDMSG_UI_STC_POS_CHANGED = EDMSG_UI_STC_ALL + ('position', )
EDMSG_UI_STC_POS_JUMPED = EDMSG_UI_STC_ALL + ('jump', )
EDMSG_UI_STC_RESTORE = EDMSG_UI_STC_ALL + ('restore', )
EDMSG_UI_STC_LEXER = EDMSG_UI_STC_ALL + ('lexer', )
EDMSG_UI_STC_CHANGED = EDMSG_UI_STC_ALL + ('changed', )
EDMSG_UI_STC_CONTEXT_MENU = EDMSG_UI_STC_ALL + ('custommenu', )
EDMSG_UI_STC_USERLIST_SEL = EDMSG_UI_STC_ALL + ('userlistsel', )
EDMSG_UI_STC_DWELL_START = EDMSG_UI_STC_ALL + ('dwellstart', )
EDMSG_UI_STC_DWELL_END = EDMSG_UI_STC_ALL + ('dwellend', )
EDMSG_UI_STC_BOOKMARK = EDMSG_UI_STC_ALL + ('bookmark', )
EDMSG_UI_STC_MARGIN_CLICK = EDMSG_UI_STC_ALL + ('marginclick', )
EDMSG_MENU = EDMSG_ALL + ('menu', )
EDMSG_MENU_REBIND = EDMSG_MENU + ('rebind', )
EDMSG_MENU_LOADPROFILE = EDMSG_MENU + ('load', )
EDMSG_CREATE_LEXER_MENU = EDMSG_MENU + ('lexer', )
EDMSG_FIND_ALL = EDMSG_ALL + ('find', )
EDMSG_FIND_SHOW_DLG = EDMSG_FIND_ALL + ('show', )
EDMSG_START_SEARCH = EDMSG_FIND_ALL + ('results', )
EDMSG_SESSION_ALL = ('session', )
EDMSG_SESSION_DO_SAVE = EDMSG_SESSION_ALL + ('dosave', )
EDMSG_SESSION_DO_LOAD = EDMSG_SESSION_ALL + ('doload', )
EDMSG_THEME_CHANGED = EDMSG_ALL + ('theme', )
EDMSG_THEME_NOTEBOOK = EDMSG_ALL + ('nb', 'theme')
EDMSG_DSP_FONT = EDMSG_ALL + ('dfont', )
EDMSG_ADD_FILE_HISTORY = EDMSG_ALL + ('filehistory', )
_ThePublisher = Publisher()

def PostMessage(msgtype, msgdata=None, context=None):
    """Post a message containing the msgdata to all listeners that are
    interested in the given msgtype from the given context. If context
    is None than default context is assumed.
    Message is always propagated to the default context.
    @param msgtype: Message Type EDMSG_*
    @keyword msgdata: Message data to pass to listener (can be anything)
    @keyword context: Context of the message.

    """
    _ThePublisher.sendMessage(msgtype, msgdata, context=context)


def Subscribe(callback, msgtype=EDMSG_ALL):
    """Subscribe your listener function to listen for an action of type msgtype.
    The callback must be a function or a _bound_ method that accepts one
    parameter for the actions message. The message that is sent to the callback
    is a class object that has two attributes, one for the message type and the
    other for the message data. See below example for how these two values can
    be accessed.
      >>> def MyCallback(msg):
              print "Msg Type: ", msg.GetType(), "Msg Data: ", msg.GetData()

      >>> class Foo:
              def MyCallbackMeth(self, msg):
                  print "Msg Type: ", msg.GetType(), "Msg Data: ", msg.GetData()

      >>> Subscribe(MyCallback, EDMSG_SOMETHING)
      >>> myfoo = Foo()
      >>> Subscribe(myfoo.MyCallBackMeth, EDMSG_SOMETHING)

    @param callback: Callable function or bound method
    @keyword msgtype: Message to subscribe to (default to all)

    """
    _ThePublisher.subscribe(callback, msgtype)


def Unsubscribe(callback, messages=None):
    """Remove a listener so that it doesn't get sent messages for msgtype. If
    msgtype is not specified the listener will be removed for all msgtypes that
    it is associated with.
    @param callback: Function or bound method to remove subscription for
    @keyword messages: EDMSG_* val or list of EDMSG_* vals

    """
    Publisher().unsubscribe(callback, messages)


def mwcontext(func):
    """Helper decorator for checking if the message is in context of the
    main window. Class that uses this to wrap its message handlers must
    have a GetMainWindow method that returns a reference to the MainWindow
    instance that owns the object.
    @param funct: callable(self, msg)

    """

    def ContextWrap(self, msg):
        """Check and only call the method if the message is in the
        context of the main window or no context was specified.

        """
        if hasattr(self, 'GetMainWindow'):
            mw = self.GetMainWindow()
        elif hasattr(self, 'MainWindow'):
            mw = self.MainWindow
        else:
            assert False, 'Must declare a GetMainWindow method'
        context = msg.GetContext()
        if context is None or mw.GetId() == context:
            func(self, msg)
        return

    ContextWrap.__name__ = func.__name__
    ContextWrap.__doc__ = func.__doc__
    return ContextWrap


def wincontext(funct):
    """Decorator to filter messages based on a window. Class must declare
    a GetWindow method that returns the window that the messages context
    should be filtered on.
    @param funct: callable(self, msg)

    """

    def ContextWrap(self, msg):
        assert hasattr(self, 'GetWindow'), 'Must define a GetWindow method'
        context = msg.GetContext()
        if isinstance(context, wx.Window) and context is self.GetWindow():
            funct(self, msg)

    ContextWrap.__name__ = funct.__name__
    ContextWrap.__doc__ = funct.__doc__
    return ContextWrap


EDREQ_ALL = ('editra', 'req')
EDREQ_DOCPOINTER = EDREQ_ALL + ('docpointer', )

class NullValue:
    """Null value to signify that a callback method should be skipped or that
    no callback could answer the request.

    """

    def __int__(self):
        return 0

    def __nonzero__(self):
        return False


def RegisterCallback(callback, msgtype):
    """Register a callback method for the given message type
    @param callback: callable
    @param msgtype: message type

    """
    if isinstance(msgtype, tuple):
        mtype = ('.').join(msgtype)
    else:
        mtype = msgtype
    if mtype not in _CALLBACK_REGISTRY:
        _CALLBACK_REGISTRY[mtype] = list()
    if callback not in _CALLBACK_REGISTRY[mtype]:
        _CALLBACK_REGISTRY[mtype].append(callback)


def RequestResult(msgtype, args=list()):
    """Request a return value result from a registered function/method.
    If multiple callbacks have been registered for the given msgtype, the
    first callback to return a non-NullValue will be used for the return
    value. If L{NullValue} is returned then no callback could answer the
    call.
    @param msgtype: Request message
    @keyword args: Arguments to pass to the callback

    """
    if isinstance(msgtype, tuple):
        mtype = ('.').join(msgtype)
    else:
        mtype = msgtype
    to_remove = list()
    rval = NullValue()
    for (idx, meth) in enumerate(_CALLBACK_REGISTRY.get(mtype, list())):
        try:
            if len(args):
                rval = meth(args)
            else:
                rval = meth()
        except PyDeadObjectError:
            to_remove.append(meth)

        if not isinstance(rval, NullValue):
            break

    for val in reversed(to_remove):
        try:
            _CALLBACK_REGISTRY.get(mtype, list()).pop(val)
        except:
            pass

    return rval


def UnRegisterCallback(callback):
    """Un-Register a callback method
    @param callback: callable

    """
    for (key, val) in _CALLBACK_REGISTRY.iteritems():
        if callback in val:
            _CALLBACK_REGISTRY[key].remove(callback)


_CALLBACK_REGISTRY = {}