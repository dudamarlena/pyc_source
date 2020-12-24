# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/utils/models.py
# Compiled at: 2016-05-21 00:29:42
from __future__ import unicode_literals
from functools import partial
from django import VERSION
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model, Field
from django.db.models.signals import class_prepared
from django.utils import six
from future.utils import with_metaclass
from shuyucms.utils.importing import import_dotted_path
if VERSION >= (1, 5):
    from django.contrib.auth import get_user_model
    fake_get_user_model = get_user_model
else:

    def get_user_model():
        from django.contrib.auth.models import User
        return User


if VERSION >= (1, 7):
    from django.apps import apps
    get_model = apps.get_model
    get_registered_model = apps.get_registered_model
else:
    from django.db.models import get_model as django_get_model

    def get_model(app_label, model_name=None):
        if model_name is None:
            app_label, model_name = app_label.split(b'.')
        model = django_get_model(app_label, model_name)
        if not model:
            raise LookupError
        return model


    def get_registered_model(app_label, model_name):
        model = django_get_model(app_label, model_name, seed_cache=False, only_installed=False)
        if not model:
            raise LookupError
        return model


def get_user_model_name():
    """
    Returns the app_label.object_name string for the user model.
    """
    return getattr(settings, b'AUTH_USER_MODEL', b'auth.User')


def base_concrete_model(abstract, instance):
    """
    Used in methods of abstract models to find the super-most concrete
    (non abstract) model in the inheritance chain that inherits from the
    given abstract model. This is so the methods in the abstract model can
    query data consistently across the correct concrete model.

    Consider the following::

        class Abstract(models.Model)

            class Meta:
                abstract = True

            def concrete(self):
                return base_concrete_model(Abstract, self)

        class Super(Abstract):
            pass

        class Sub(Super):
            pass

        sub = Sub.objects.create()
        sub.concrete() # returns Super

    In actual shuyucms usage, this allows methods in the ``Displayable`` and
    ``Orderable`` abstract models to access the ``Page`` instance when
    instances of custom content types, (eg: models that inherit from ``Page``)
    need to query the ``Page`` model to determine correct values for ``slug``
    and ``_order`` which are only relevant in the context of the ``Page``
    model and not the model of the custom content type.
    """
    for cls in reversed(instance.__class__.__mro__):
        if issubclass(cls, abstract) and not cls._meta.abstract:
            return cls

    return instance.__class__


def upload_to(field_path, default):
    """
    Used as the ``upload_to`` arg for file fields - allows for custom
    handlers to be implemented on a per field basis defined by the
    ``UPLOAD_TO_HANDLERS`` setting.
    """
    from shuyucms.conf import settings
    for k, v in settings.UPLOAD_TO_HANDLERS.items():
        if k.lower() == field_path.lower():
            return import_dotted_path(v)

    return default


class AdminThumbMixin(object):
    """
    Provides a thumbnail method on models for admin classes to
    reference in the ``list_display`` definition.
    """
    admin_thumb_field = None

    def admin_thumb(self):
        thumb = b''
        if self.admin_thumb_field:
            thumb = getattr(self, self.admin_thumb_field, b'')
        if not thumb:
            return b''
        from shuyucms.conf import settings
        from shuyucms.core.templatetags.shuyucms_tags import thumbnail
        x, y = settings.ADMIN_THUMB_SIZE.split(b'x')
        thumb_url = thumbnail(thumb, x, y)
        return b"<img src='%s%s'>" % (settings.MEDIA_URL, thumb_url)

    admin_thumb.allow_tags = True
    admin_thumb.short_description = b''


class ModelMixinBase(type):
    """
    Metaclass for ``ModelMixin`` which is used for injecting model
    fields and methods into models defined outside of a project.
    This currently isn't used anywhere.
    """

    def __new__(cls, name, bases, attrs):
        """
        Checks for an inner ``Meta`` class with a ``mixin_for``
        attribute containing the model that this model will be mixed
        into. Once found, copy over any model fields and methods onto
        the model being mixed into, and return it as the actual class
        definition for the mixin.
        """
        if name == b'ModelMixin':
            return super(ModelMixinBase, cls).__new__(cls, name, bases, attrs)
        try:
            mixin_for = attrs.pop(b'Meta').mixin_for
            if not issubclass(mixin_for, Model):
                raise TypeError
        except (TypeError, KeyError, AttributeError):
            raise ImproperlyConfigured(b"The ModelMixin class '%s' requires an inner Meta class with the ``mixin_for`` attribute defined, with a value that is a valid model.")

        for k, v in attrs.items():
            if isinstance(v, Field):
                v.contribute_to_class(mixin_for, k)
            elif k != b'__module__':
                setattr(mixin_for, k, v)

        return mixin_for


class ModelMixin(with_metaclass(ModelMixinBase, object)):
    """
    Used as a subclass for mixin models that inject their behaviour onto
    models defined outside of a project. The subclass should define an
    inner ``Meta`` class with a ``mixin_for`` attribute containing the
    model that will be mixed into.
    """
    pass


class LazyModelOperations(object):
    """
    This class connects itself to Django's class_prepared signal.
    Pass a function and a model or model name to its ``add()`` method,
    and the function will be called with the model as its only
    parameter once the model has been loaded. If the model is already
    loaded, the function is called immediately.

    Adapted from ``django.db.models.fields.related`` and used in
    ``shuyucms.generic.fields``.
    """

    def __init__(self):
        self.pending_operations = {}
        class_prepared.connect(self.signal_receiver)

    @staticmethod
    def model_key(model_or_name):
        """
        Returns an (app_label, model_name) tuple from a model or string.
        """
        if isinstance(model_or_name, six.string_types):
            app_label, model_name = model_or_name.split(b'.')
        else:
            app_label = model_or_name._meta.app_label
            model_name = model_or_name._meta.object_name
        return (
         app_label, model_name)

    def add(self, function, *models_or_names):
        """
        The function passed to this method should accept n arguments,
        where n=len(models_or_names). When all the models are ready,
        the function will be called with the models as arguments, in
        the order they appear in this argument list.
        """
        model_keys = [ (isinstance(m, tuple) or self.model_key)(m) if 1 else m for m in models_or_names
                     ]
        model_key, more_models = model_keys[0], model_keys[1:]
        if more_models:
            inner_function = function
            function = lambda model: self.add(partial(inner_function, model), *more_models)
        try:
            model_class = get_registered_model(*model_key)
        except LookupError:
            self.pending_operations.setdefault(model_key, []).append(function)
        else:
            function(model_class)

    def signal_receiver(self, sender, **kwargs):
        """
        Receive ``class_prepared``, and pass the freshly prepared
        model to each function waiting for it.
        """
        key = (
         sender._meta.app_label, sender.__name__)
        for function in self.pending_operations.pop(key, []):
            function(sender)


lazy_model_ops = LazyModelOperations()