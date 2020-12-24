# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/button.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 11519 bytes
"""PyAMS_form.button module

Form buttons management.
"""
import sys
from six import class_types
from zope.interface import Interface, alsoProvides, implementedBy, implementer, providedBy
from zope.interface.adapter import AdapterRegistry
from zope.interface.interfaces import IInterface
from zope.location import Location, locate
from zope.schema import Field, getFieldsInOrder
from zope.schema.fieldproperty import FieldProperty
from pyams_form.action import Action, ActionHandlerBase, Actions
from pyams_form.browser.image import ImageWidget
from pyams_form.browser.submit import SubmitWidget
from pyams_form.interfaces import IValue
from pyams_form.interfaces.button import IActionHandler, IActions, IButton, IButtonAction, IButtonHandler, IButtonHandlers, IButtons, IImageButton
from pyams_form.interfaces.form import IButtonForm, IFormAware, IHandlerForm
from pyams_form.util import SelectionManager, create_id, expand_prefix, get_specification, to_unicode
from pyams_form.value import ComputedValueCreator, StaticValueCreator
from pyams_form.widget import AfterWidgetUpdateEvent
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
__docformat__ = 'restructuredtext'
StaticButtonActionAttribute = StaticValueCreator(discriminators=('form', 'request',
                                                                 'content', 'button',
                                                                 'manager'))
ComputedButtonActionAttribute = ComputedValueCreator(discriminators=('form', 'request',
                                                                     'content', 'button',
                                                                     'manager'))

@implementer(IButton)
class Button(Field):
    __doc__ = 'A simple button in a form.'
    access_key = FieldProperty(IButton['access_key'])
    action_factory = FieldProperty(IButton['action_factory'])

    def __init__(self, *args, **kwargs):
        if args:
            kwargs['__name__'] = args[0]
            args = args[1:]
        if 'name' in kwargs:
            kwargs['__name__'] = kwargs['name']
            del kwargs['name']
        self.access_key = kwargs.pop('access_key', None)
        self.condition = kwargs.pop('condition', None)
        super(Button, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<%s %r %r>' % (
         self.__class__.__name__, self.__name__, self.title)


@implementer(IImageButton)
class ImageButton(Button):
    __doc__ = 'A simple image button in a form.'
    image = FieldProperty(IImageButton['image'])

    def __init__(self, image, *args, **kwargs):
        self.image = image
        super(ImageButton, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<%s %r %r>' % (
         self.__class__.__name__, self.__name__, self.image)


@implementer(IButtons)
class Buttons(SelectionManager):
    __doc__ = 'Button manager.'
    manager_interface = IButtons
    prefix = 'buttons'

    def __init__(self, *args):
        buttons = []
        for arg in args:
            if IInterface.providedBy(arg):
                for name, button in getFieldsInOrder(arg):
                    if IButton.providedBy(button):
                        buttons.append((name, button))

            else:
                if self.manager_interface.providedBy(arg):
                    buttons += arg.items()
                else:
                    if IButton.providedBy(arg):
                        if not arg.__name__:
                            arg.__name__ = create_id(arg.title)
                        buttons.append((arg.__name__, arg))
                    else:
                        raise TypeError('Unrecognized argument type', arg)

        super(Buttons, self).__init__(buttons)


@implementer(IButtonHandlers)
class Handlers:
    __doc__ = 'Action Handlers for a Button-based form.'

    def __init__(self):
        self._registry = AdapterRegistry()
        self._handlers = ()

    def add_handler(self, button, handler):
        """See interfaces.button.IButtonHandlers"""
        button_spec = get_specification(button)
        if isinstance(button_spec, class_types):
            button_spec = implementedBy(button_spec)
        self._registry.register((
         button_spec,), IButtonHandler, '', handler)
        self._handlers += ((button, handler),)

    def get_handler(self, button):
        """See interfaces.button.IButtonHandlers"""
        button_provided = providedBy(button)
        return self._registry.lookup1(button_provided, IButtonHandler)

    def copy(self):
        """See interfaces.button.IButtonHandlers"""
        handlers = Handlers()
        for button, handler in self._handlers:
            handlers.add_handler(button, handler)

        return handlers

    def __add__(self, other):
        """See interfaces.button.IButtonHandlers"""
        if not isinstance(other, Handlers):
            raise NotImplementedError
        handlers = self.copy()
        for button, handler in other._handlers:
            handlers.add_handler(button, handler)

        return handlers

    def __repr__(self):
        return '<Handlers %r>' % [handler for button, handler in self._handlers]


@implementer(IButtonHandler)
class Handler:
    __doc__ = 'Button handler class'

    def __init__(self, button, func):
        self.button = button
        self.func = func

    def __call__(self, form, action):
        return self.func(form, action)

    def __repr__(self):
        return '<%s for %r>' % (self.__class__.__name__, self.button)


def handler(button):
    """A decorator for defining a success handler."""

    def create_handler(func):
        handler = Handler(button, func)
        frame = sys._getframe(1)
        f_locals = frame.f_locals
        handlers = f_locals.setdefault('handlers', Handlers())
        handlers.add_handler(button, handler)
        return handler

    return create_handler


def button_and_handler(title, **kwargs):
    """Button with handler method decorator"""
    kwargs['title'] = title
    provides = kwargs.pop('provides', ())
    button = Button(**kwargs)
    alsoProvides(button, provides)
    frame = sys._getframe(1)
    f_locals = frame.f_locals
    f_locals.setdefault('buttons', Buttons())
    f_locals['buttons'] += Buttons(button)
    return handler(button)


@adapter_config(required=(IFormLayer, IButton), provides=IButtonAction)
class ButtonAction(Action, SubmitWidget, Location):
    __doc__ = 'Button action'

    def __init__(self, request, field):
        Action.__init__(self, request, field.title)
        SubmitWidget.__init__(self, request)
        self.field = field

    @property
    def access_key(self):
        """Button access key"""
        return self.field.access_key

    @property
    def value(self):
        """Button value"""
        return self.title

    @property
    def id(self):
        """Button ID"""
        return self.name.replace('.', '-')


@adapter_config(required=(IFormLayer, IImageButton), provides=IButtonAction)
class ImageButtonAction(ImageWidget, ButtonAction):
    __doc__ = 'Image button action'

    def __init__(self, request, field):
        Action.__init__(self, request, field.title)
        SubmitWidget.__init__(self, request)
        self.field = field

    @property
    def src(self):
        """Image source"""
        return to_unicode(self.field.image)

    def is_executed(self):
        return self.name + '.x' in self.request.params


@adapter_config(required=(IButtonForm, Interface, Interface), provides=IActions)
class ButtonActions(Actions):
    __doc__ = 'Button actions manager'

    def update(self):
        """See pyams_form.interfaces.button.IActions."""
        prefix = expand_prefix(self.form.prefix)
        prefix += expand_prefix(self.form.buttons.prefix)
        d = {}
        d.update(self)
        registry = self.request.registry
        for name, button in self.form.buttons.items():
            if button.condition is not None and not button.condition(self.form):
                if name in d:
                    del d[name]
            else:
                new_button = True
                if name in self:
                    button_action = self[name]
                    new_button = False
                else:
                    if button.action_factory is not None:
                        button_action = button.action_factory(self.request, button)
                    else:
                        button_action = registry.getMultiAdapter((self.request, button), IButtonAction)
                    button_action.name = prefix + name
                    title = registry.queryMultiAdapter((self.form, self.request, self.content,
                     button, self), IValue, name='title')
                    if title is not None:
                        button_action.title = title.get()
                    button_action.form = self.form
                    if not IFormAware.providedBy(button_action):
                        alsoProvides(button_action, IFormAware)
                button_action.update()
                registry.notify(AfterWidgetUpdateEvent(button_action))
                if new_button:
                    d[name] = button_action
                    locate(button_action, self, name)

        self.create_according_to_list(d, self.form.buttons.keys())


@adapter_config(required=(IHandlerForm, Interface, Interface, ButtonAction), provides=IActionHandler)
class ButtonActionHandler(ActionHandlerBase):
    __doc__ = 'Button action handler'

    def __call__(self):
        handler = self.form.handlers.get_handler(self.action.field)
        if handler is None:
            return
        return handler(self.form, self.action)