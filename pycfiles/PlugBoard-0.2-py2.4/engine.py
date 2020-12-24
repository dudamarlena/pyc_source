# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plugboard/engine.py
# Compiled at: 2006-02-22 09:00:28
from zope import interface
from plugboard import plugin
import types

class ISharedEventArgument(interface.Interface):
    """
    Contains informations about a specific event argument which can be changed by events
    """
    __module__ = __name__

    def get_value():
        """
        Returns the value of the argument
        """
        pass

    def set_value(value):
        """
        Set the new value of the argument
        """
        pass


class IEvent(interface.Interface):
    """
    Informations about an event, emitter and connector.
    """
    __module__ = __name__
    name = interface.Attribute('The name of the event')
    arguments = interface.Attribute("A list of tuples defining the type and the description of each argument, e.g.: [(str, 'A string'), (int, 'An int')]")

    def emit(*args):
        """
        Emits the event
        """
        pass

    def connect(callback, *extra):
        """
        Connect to the event
        """
        pass


class IEventConnector(interface.Interface):
    """
    This is a convenience interface to make an easy connection with IEventDispatcher
    """
    __module__ = __name__

    def connect_all():
        """
        Connect all events to all callable objects which start with "on_".
        Pass extra arguments to IEvent.connect if defined in the event functions, e.g.:
        def on_event_name(self, *args):
            ...
        on_event_name.extra = (arg1, arg2, ...)
        """
        pass

    def disconnect_all():
        """
        Disconnect all connected events
        """
        pass


class IEventDispatcher(interface.Interface):
    """
    Contains all events of a given object
    """
    __module__ = __name__

    def add_event(name, *args):
        """
        A wrap method to create an IEvent
        """
        pass

    def get_event(name):
        """
        Returns the event with the given name
        """
        pass

    get_event.return_type = IEvent

    def remove_event(name):
        """
        Removes the event which got the given name from events
        """
        pass

    def get_events():
        """
        Returns an iter of all events
        """
        pass

    get_events.return_type = types.GeneratorType

    def get_event_names():
        """
        Returns an iter of all event names
        """
        pass

    get_event_names.return_type = types.GeneratorType

    def __getitem__():
        """
        A wrap method to get_event
        """
        pass

    __getitem__.return_type = IEvent

    def __iter__():
        """
        A wrap method to get_events
        """
        pass

    __iter__.return_type = types.GeneratorType


class IEngine(interface.Interface):
    """
    Rappresentation of the engine used by the application
    """
    __module__ = __name__


class SharedEventArgument(object):
    __module__ = __name__
    interface.implements(ISharedEventArgument)

    def __init__(self):
        self._value = None
        return

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value


class Event(object):
    __module__ = __name__
    interface.implements(IEvent)

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher


class EventConnector(object):
    __module__ = __name__
    interface.implements(IEventConnector)

    def __init__(self, plugin):
        self.plugin = plugin
        self.dispatcher = plugin.dispatcher

    def connect_all(self):
        for name in dir(self):
            value = getattr(self, name)
            if name.startswith('on_') and self.dispatcher.has_event(name[3:]) and callable(value):
                try:
                    extra = value.extra
                except:
                    extra = ()
                else:
                    self.dispatcher[name[3:]].connect(value, *extra)

    def disconnect_all(self):
        for name in dir(self):
            value = getattr(self, name)
            if name.startswith('on_') and self.dispatcher.has_event(name[3:]) and callable(value):
                self.dispatcher[name[3:]].disconnect(value)


class EventDispatcher(object):
    __module__ = __name__
    interface.implements(IEventDispatcher)

    def __init__(self, plugin):
        self.plugin = plugin
        self._events = {}

    def add_event(self, name, *args):
        if self.has_event(name):
            raise LookupError, 'Event %r already exists in dispatcher %r' % (name, self)
        event = IEvent(self)
        event.name = name
        event.arguments = args
        self._events[name] = event

    def get_event(self, name):
        return self._events[name]

    def has_event(self, name):
        return self._events.has_key(name)

    def remove_event(self, name):
        del self._events[name]

    def get_events(self):
        return self._events.itervalues()

    def get_event_names(self):
        return self._events.iterkeys()

    __getitem__, __iter__ = get_event, get_events


class Engine(object):
    __module__ = __name__
    interface.implements(IEngine)

    def __init__(self, application):
        self.application = application
        application.register(application, self)


class PlugBoardEvent(Event):
    __module__ = __name__

    def __init__(self, dispatcher):
        super(PlugBoardEvent, self).__init__(dispatcher)
        self._callbacks = {}

    def emit(self, *args):
        for (callback, extra) in self._callbacks.iteritems():
            if callback(self.dispatcher.plugin, *(args + extra)):
                return

    def connect(self, callback, *extra):
        self._callbacks[callback] = extra

    def disconnect(self, callback):
        del self._callbacks[callback]


class PlugBoardEngine(Engine):
    __module__ = __name__

    def __init__(self, application):
        super(PlugBoardEngine, self).__init__(application)
        application.register(plugin.IPlugin, EventDispatcher)
        application.register(EventDispatcher, PlugBoardEvent)


class GTKEvent(Event):
    __module__ = __name__
    interface.implements(IEvent)

    def __init__(self, dispatcher):
        super(GTKEvent, self).__init__(dispatcher)
        self._callbacks = {}

    def emit(self, *args):
        self.dispatcher._gobject.emit(self.name, *args)

    def connect(self, callback, *extra):
        self._callbacks[callback] = self.dispatcher._gobject.connect_object(self.name, callback, self.dispatcher.plugin, *extra)

    def disconnect(self, callback):
        self.dispatcher._gobject.disconnect(self._callbacks[callback])
        del self._callbacks[callback]


class GTKEventDispatcher(EventDispatcher):
    __module__ = __name__

    def __init__(self, plugin):
        super(GTKEventDispatcher, self).__init__(plugin)
        self._create_gobject()

    def add_event(self, name, *args):
        super(GTKEventDispatcher, self).add_event(name, *args)
        self._create_gobject()

    def _create_gobject(self):
        import gobject
        __gsignals__ = {}
        for event in self:
            garguments = [gobject.TYPE_PYOBJECT] * len(event.arguments)
            __gsignals__[event.name] = (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, garguments)

        odict = {'__gsignals__': __gsignals__}
        self._gobject = type('_PluginEventGObject', (gobject.GObject,), odict)()


class GTKEngine(Engine):
    __module__ = __name__

    def __init__(self, application):
        super(GTKEngine, self).__init__(application)
        application.register(plugin.IPlugin, GTKEventDispatcher)
        application.register(GTKEventDispatcher, GTKEvent)


class WXEvent(Event):
    __module__ = __name__

    def __init__(self, dispatcher):
        import wx
        super(WXEvent, self).__init__(dispatcher)
        self._widget = wx.Button(dispatcher._widget, -1)

    def emit(self, *args):
        import wx
        evt = wx.PyCommandEvent(self.dispatcher._event, self._widget.GetId())
        evt.event_arguments = args
        self._widget.GetEventHandler().ProcessEvent(evt)

    def connect(self, callback, *extra):
        self.dispatcher._binded.Bind(self.dispatcher._binder, self._fire(callback, extra), id(callback))

    def _fire(self, callback, extra):

        def event_callback(event, callback=callback, extra=extra):
            print event, callback, extra

        return event_callback


class WXEventDispatcher(EventDispatcher):
    __module__ = __name__

    def __init__(self, plugin):
        import wx
        super(WXEventDispatcher, self).__init__(plugin)
        self._event = wx.NewEventType()
        self._binder = wx.PyEventBinder(self._event, 1)
        self._widget = wx.Panel(None, -1)
        return


class WXEngine(Engine):
    __module__ = __name__

    def __init__(self, application):
        import wx
        super(WXEngine, self).__init__(application)
        self._app = wx.App()
        application.register(plugin.IPlugin, WXEventDispatcher)
        application.register(WXEventDispatcher, WXEvent)