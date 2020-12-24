# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/checks/model_checks.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import inspect, types
from itertools import chain
from django.apps import apps
from django.core.checks import Error, Tags, register

@register(Tags.models)
def check_all_models(app_configs=None, **kwargs):
    errors = []
    if app_configs is None:
        models = apps.get_models()
    else:
        models = chain.from_iterable(app_config.get_models() for app_config in app_configs)
    for model in models:
        if not inspect.ismethod(model.check):
            errors.append(Error(b"The '%s.check()' class method is currently overridden by %r." % (
             model.__name__, model.check), obj=model, id=b'models.E020'))
        else:
            errors.extend(model.check(**kwargs))

    return errors


def _check_lazy_references(apps, ignore=None):
    """
    Ensure all lazy (i.e. string) model references have been resolved.

    Lazy references are used in various places throughout Django, primarily in
    related fields and model signals. Identify those common cases and provide
    more helpful error messages for them.

    The ignore parameter is used by StateApps to exclude swappable models from
    this check.
    """
    pending_models = set(apps._pending_operations) - (ignore or set())
    if not pending_models:
        return []
    else:
        from django.db.models import signals
        model_signals = {signal:name for name, signal in vars(signals).items() if isinstance(signal, signals.ModelSignal)}

        def extract_operation(obj):
            """
        Take a callable found in Apps._pending_operations and identify the
        original callable passed to Apps.lazy_model_operation(). If that
        callable was a partial, return the inner, non-partial function and
        any arguments and keyword arguments that were supplied with it.

        obj is a callback defined locally in Apps.lazy_model_operation() and
        annotated there with a `func` attribute so as to imitate a partial.
        """
            operation, args, keywords = obj, [], {}
            while hasattr(operation, b'func'):
                args.extend(getattr(operation, b'args', []) or [])
                keywords.update(getattr(operation, b'keywords', {}) or {})
                operation = operation.func

            return (
             operation, args, keywords)

        def app_model_error(model_key):
            try:
                apps.get_app_config(model_key[0])
                model_error = b"app '%s' doesn't provide model '%s'" % model_key
            except LookupError:
                model_error = b"app '%s' isn't installed" % model_key[0]

            return model_error

        def field_error(model_key, func, args, keywords):
            error_msg = b"The field %(field)s was declared with a lazy reference to '%(model)s', but %(model_error)s."
            params = {b'model': (b'.').join(model_key), 
               b'field': keywords[b'field'], 
               b'model_error': app_model_error(model_key)}
            return Error(error_msg % params, obj=keywords[b'field'], id=b'fields.E307')

        def signal_connect_error(model_key, func, args, keywords):
            error_msg = b"%(receiver)s was connected to the '%(signal)s' signal with a lazy reference to the sender '%(model)s', but %(model_error)s."
            receiver = args[0]
            if isinstance(receiver, types.FunctionType):
                description = b"The function '%s'" % receiver.__name__
            elif isinstance(receiver, types.MethodType):
                description = b"Bound method '%s.%s'" % (receiver.__self__.__class__.__name__, receiver.__name__)
            else:
                description = b"An instance of class '%s'" % receiver.__class__.__name__
            signal_name = model_signals.get(func.__self__, b'unknown')
            params = {b'model': (b'.').join(model_key), 
               b'receiver': description, 
               b'signal': signal_name, 
               b'model_error': app_model_error(model_key)}
            return Error(error_msg % params, obj=receiver.__module__, id=b'signals.E001')

        def default_error(model_key, func, args, keywords):
            error_msg = b'%(op)s contains a lazy reference to %(model)s, but %(model_error)s.'
            params = {b'op': func, 
               b'model': (b'.').join(model_key), 
               b'model_error': app_model_error(model_key)}
            return Error(error_msg % params, obj=func, id=b'models.E022')

        known_lazy = {('django.db.models.fields.related', 'resolve_related_class'): field_error, 
           ('django.db.models.fields.related', 'set_managed'): None, 
           ('django.dispatch.dispatcher', 'connect'): signal_connect_error}

        def build_error(model_key, func, args, keywords):
            key = (
             func.__module__, func.__name__)
            error_fn = known_lazy.get(key, default_error)
            if error_fn:
                return error_fn(model_key, func, args, keywords)
            else:
                return

        return sorted(filter(None, (build_error(model_key, *extract_operation(func)) for model_key in pending_models for func in apps._pending_operations[model_key])), key=lambda error: error.msg)


@register(Tags.models)
def check_lazy_references(app_configs=None, **kwargs):
    return _check_lazy_references(apps)