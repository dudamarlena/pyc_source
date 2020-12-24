# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/controller.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 14271 bytes
import logging
from mvc.support.gui_loop import add_idle_call
logger = logging.getLogger(__name__)
from .observers import Observer
from .support.exceptions import TooManyCandidatesError

class Controller(Observer):
    auto_adapt = True
    auto_adapt_included = None
    auto_adapt_excluded = None
    register_lazy = True
    _Controller__adapters = None
    _Controller__parsed_user_props = None
    _controller_scope_aplied = False

    @property
    def __user_props(self):
        if not not (self.auto_adapt_included is not None and self.auto_adapt_excluded is not None):
            raise AssertionError("Controller '%s' has set both auto_adapt_included and auto_adapt_excluded!" % self)
        else:
            assert self.model is not None, "Controller '%s' has None as model! Did you forget to pass it as a keyword argument?" % self
            props = self._controller_scope_aplied or [prop.label for prop in self.model.Meta.all_properties]
            if self.auto_adapt_included is not None:
                self._Controller__parsed_user_props = self._Controller__parsed_user_props.union(set([p for p in props if p not in self.auto_adapt_included]))
            elif self.auto_adapt_excluded is not None:
                self._Controller__parsed_user_props = self._Controller__parsed_user_props.union(set([p for p in props if p in self.auto_adapt_excluded]))
            self._controller_scope_aplied = True
        return self._Controller__parsed_user_props

    @_Controller__user_props.setter
    def __user_props(self, value):
        pass

    _model = None

    def _get_model(self):
        return self._model

    def _set_model(self, model):
        if self._model is not None:
            self._clear_adapters()
            self.relieve_model(self._model)
        self._model = model
        if self._model is not None:
            self.observe_model(self._model)
            if self.view is not None:
                self.register_adapters()
                if self.auto_adapt:
                    self.adapt()

    def _del_model(self):
        del self._model
        self._model = None

    model = property(_get_model, _set_model, _del_model)
    _Controller__view = None

    def _get_view(self):
        return self._Controller__view

    def _set_view(self, view):
        if self._Controller__view != view:
            self._Controller__view = view
            if self._Controller__view is not None:
                if self.register_lazy:
                    add_idle_call(self._idle_register_view, self._Controller__view)
                else:
                    self._idle_register_view(self._Controller__view)

    def _del_view(self):
        self._Controller__view = None

    view = property(_get_view, _set_view, _del_view, "This controller's view")

    def __init__(self, *args, **kwargs):
        self._Controller__adapters = []
        self._Controller__parsed_user_props = set()
        self.parent = kwargs.pop('parent', None)
        self.auto_adapt = kwargs.pop('auto_adapt', self.auto_adapt)
        self.register_lazy = kwargs.pop('register_lazy', self.register_lazy)
        _view = kwargs.pop('view', None)
        _model = kwargs.get('model', None)
        (super(Controller, self).__init__)(*args, **kwargs)
        self.model = _model
        self.view = _view

    def _idle_register_view(self, view):
        """Internal method that calls register_view"""
        assert self.view is not None
        if self.model is not None:
            self._Controller__autoconnect_signals()
            self.register_view(self.view)
            self.register_adapters()
            if self.auto_adapt:
                self.adapt()
            return False
        else:
            return True

    def _clear_adapters(self):
        """Clears & disconnects all adapters from this controller"""
        if self._Controller__adapters:
            for ad in self._Controller__adapters:
                ad.disconnect()

            self._Controller__adapters[:] = []

    def register_view(self, view):
        """
        This does nothing. Subclasses can override it to connect signals
        manually or modify widgets loaded from XML, like adding columns to a
        TreeView. No super call necessary.
        
        *view* is a shortcut for ``self.view``.
        """
        if not self.model is not None:
            raise AssertionError
        elif not self.view is not None:
            raise AssertionError

    def register_adapters(self):
        """
        This does nothing. Subclasses can override it to create adapters.
        No super call necessary.
        """
        if not self.model is not None:
            raise AssertionError
        elif not self.view is not None:
            raise AssertionError

    def adapt(self, *args):
        """
        There are four ways to call this:

        .. method:: adapt()
           :noindex:

           Take properties from the model for which ``adapt`` has not yet been
           called, match them to the view by name, and create adapters fitting
           for the respective widget type.
           
           That information comes from :mod:`mvc.adapters.default`.
           See :meth:`_find_widget_match` for name patterns.

           .. versionchanged:: 1.99.1
              Allow incomplete auto-adaption, meaning properties for which no
              widget is found.

        .. method:: adapt(ad)
           :noindex:
        
           Keep track of manually created adapters for future ``adapt()``
           calls.
        
           *ad* is an adapter instance already connected to a widget.

        .. method:: adapt(prop_name)
           :noindex:

           Like ``adapt()`` for a single property.

           *prop_name* is a string.

        .. method:: adapt(prop_name, wid_name)
           :noindex:

           Like ``adapt(prop_name)`` but without widget name matching.
           
           *wid_name* has to exist in the view.
        """
        n = len(args)
        if n not in list(range(3)):
            raise TypeError('adapt() takes 0, 1 or 2 arguments (%d given)' % n)
        if n == 0:
            adapters = []
            props = self.model.Meta.get_viewable_properties()
            for prop in [p for p in props if p.label not in self._Controller__user_props]:
                try:
                    wid_name = self._find_widget_match(prop)
                except TooManyCandidatesError as e:
                    raise e
                except ValueError as e:
                    if e.args:
                        logger.warn(e[0])
                    else:
                        logger.warn("No widget candidates match property '%s'" % prop.label)
                else:
                    logger.debug('Auto-adapting property %s and widget %s' % (
                     prop.label, wid_name))
                    adapters += self.__create_adapters__(prop, wid_name)

        else:
            if n == 1:
                from .adapters import AbstractAdapter
                if isinstance(args[0], AbstractAdapter):
                    adapters = (
                     args[0],)
                else:
                    if isinstance(args[0], str):
                        prop = getattr(type(self.model), args[0])
                        wid_name = self._find_widget_match(prop)
                        adapters = self.__create_adapters__(prop, wid_name)
                    else:
                        raise TypeError('Argument of adapt() must be either an Adapter or a string')
            else:
                if not (isinstance(args[0], str) and isinstance(args[1], str)):
                    raise TypeError('Arguments of adapt() must be two strings')
                prop_name, wid_name = args
                adapters = self.__create_adapters__(prop, wid_name)
        for ad in adapters:
            self._Controller__adapters.append(ad)
            if n > 0:
                self._Controller__user_props.add(ad.get_property_name())

    def _find_widget_match(self, prop):
        """
        Checks if the view has defined a 'widget_format' attribute (e.g. 
        "view_%s") If so, it uses this format to search for the widget in 
        the view, if not it takes the *first* widget with a name ending with the
        property name.
        """
        widget_name = None
        widget_format = getattr(self.view, 'widget_format', '%s')
        if widget_format:
            widget_name = widget_format % prop.label
            widget = self.view[widget_name]
            if widget is None:
                if prop is not None:
                    if prop.widget_type == 'scale':
                        self.view.add_scale_widget(prop)
                widget_name = None
        else:
            for wid_name in self.view:
                if wid_name.lower().endswith(prop.label.lower()):
                    widget_name = wid_name
                    break

        if widget_name == None:
            logger.setLevel(logging.INFO)
            raise ValueError("No widget candidates match property '%s'" % prop.label)
        return widget_name

    def __autoconnect_signals(self):
        """This is called during view registration, to autoconnect
        signals in glade file with methods within the controller"""
        dic = {}
        for name in dir(self):
            method = getattr(self, name)
            if not callable(method):
                continue
            assert name not in dic
            dic[name] = method

        if self.view._builder is not None:
            self.view._builder.connect_signals(dic)

    def _get_handler_list(self):
        from .adapters import AdapterRegistry
        local_handlers = {}
        adapter_registry = AdapterRegistry.get_selected_adapter_registry()
        local_handlers.update(adapter_registry)
        for widget_type, handler in self.widget_handlers.items():
            if isinstance(handler, str):
                self.widget_handlers[widget_type] = getattr(self, handler)

        local_handlers.update(self.widget_handlers)
        return local_handlers

    def __create_adapters__(self, prop, wid_name):
        """
            Private service that looks at property and widgets types,
            and possibly creates one or more (best) fitting adapters
            that are returned as a list.
        """
        try:
            logger.debug("Adapting property %s to widget names '%s'" % (prop.label, wid_name))
            if prop.visible:
                wid = self.view[wid_name]
                if wid == None:
                    raise ValueError("Widget '%s' not found in view '%s' by controller '%s'" % (wid_name, self.view, self))
                local_handlers = self._get_handler_list()
                handler = local_handlers.get(prop.widget_type)
                ad = handler(self, prop, wid)
                return [
                 ad]
            else:
                return []
        except BaseException as error:
            raise RuntimeError("Unhandled error in '%s'.__create_adapters__ for property '%s' and widget '%s'!" % (type(self), prop.label, wid_name)) from error