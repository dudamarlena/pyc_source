# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/orm.py
# Compiled at: 2018-07-11 18:15:31
"""
South's fake ORM; lets you not have to write SQL inside migrations.
Roughly emulates the real Django ORM, to a point.
"""
from __future__ import print_function
import inspect
from django.db import models
from django.db.models.loading import cache
from django.core.exceptions import ImproperlyConfigured
from south.db import db
from south.utils import ask_for_it_by_name, datetime_utils
from south.hacks import hacks
from south.exceptions import UnfreezeMeLater, ORMBaseNotIncluded, ImpossibleORMUnfreeze
from south.utils.py3 import string_types

class ModelsLocals(object):
    """
    Custom dictionary-like class to be locals();
    falls back to lowercase search for items that don't exist
    (because we store model names as lowercase).
    """

    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            return self.data[key.lower()]


_orm_cache = {}

def FakeORM(*args):
    """
    Creates a Fake Django ORM.
    This is actually a memoised constructor; the real class is _FakeORM.
    """
    if args not in _orm_cache:
        _orm_cache[args] = _FakeORM(*args)
    return _orm_cache[args]


class LazyFakeORM(object):
    """
    In addition to memoising the ORM call, this function lazily generates them
    for a Migration class. Assign the result of this to (for example)
    .orm, and as soon as .orm is accessed the ORM will be created.
    """

    def __init__(self, *args):
        self._args = args
        self.orm = None
        return

    def __get__(self, obj, type=None):
        if not self.orm:
            self.orm = FakeORM(*self._args)
        return self.orm


class _FakeORM(object):
    """
    Simulates the Django ORM at some point in time,
    using a frozen definition on the Migration class.
    """

    def __init__(self, cls, app):
        self.default_app = app
        self.cls = cls
        self.models = {}
        try:
            self.models_source = cls.models
        except AttributeError:
            return

        hacks.clear_app_cache()
        model_names = []
        for name, data in self.models_source.items():
            if 'Meta' not in data:
                data['Meta'] = {}
            try:
                app_label, model_name = name.split('.', 1)
            except ValueError:
                app_label = self.default_app
                model_name = name

            if 'object_name' in data['Meta']:
                model_name = data['Meta']['object_name']
                del data['Meta']['object_name']
            name = '%s.%s' % (app_label, model_name)
            self.models[name.lower()] = name
            model_names.append((name.lower(), app_label, model_name, data))

        last_size = None
        while model_names:
            if len(model_names) == last_size:
                raise ImpossibleORMUnfreeze()
            last_size = len(model_names)
            postponed_model_names = []
            for name, app_label, model_name, data in model_names:
                try:
                    self.models[name] = self.make_model(app_label, model_name, data)
                except UnfreezeMeLater:
                    postponed_model_names.append((name, app_label, model_name, data))

            model_names = postponed_model_names

        self.retry_failed_fields()
        for model in self.models.values():
            model._meta.get_all_field_names()

        hacks.unclear_app_cache()
        return

    def __iter__(self):
        return iter(self.models.values())

    def __getattr__(self, key):
        fullname = (self.default_app + '.' + key).lower()
        try:
            return self.models[fullname]
        except KeyError:
            raise AttributeError("The model '%s' from the app '%s' is not available in this migration. (Did you use orm.ModelName, not orm['app.ModelName']?)" % (key, self.default_app))

    def __getitem__(self, key):
        if ':' in key:
            key, fname = key.split(':')
        else:
            fname = None
        key = key.lower()
        try:
            model = self.models[key]
        except KeyError:
            try:
                app, model = key.split('.', 1)
            except ValueError:
                raise KeyError("The model '%s' is not in appname.modelname format." % key)
            else:
                raise KeyError("The model '%s' from the app '%s' is not available in this migration." % (model, app))

        if fname:
            return model._meta.get_field_by_name(fname)[0]
        else:
            return model
            return

    def eval_in_context(self, code, app, extra_imports={}):
        """Evaluates the given code in the context of the migration file."""
        fake_locals = dict((key, value) for key, value in inspect.getmodule(self.cls).__dict__.items() if not (isinstance(value, type) and issubclass(value, models.Model) and hasattr(value, '_meta')))
        fake_locals.update(dict([ (name.split('.')[(-1)], model) for name, model in self.models.items()
                                ]))
        fake_locals.update(dict([ (name.split('.')[(-1)], model) for name, model in self.models.items() if name.split('.')[0] == app
                                ]))
        fake_locals['orm'] = self
        fake_locals['_'] = lambda x: x
        fake_locals['datetime'] = datetime_utils
        for name, value in extra_imports.items():
            parts = value.split('.')
            try:
                obj = fake_locals[parts[0]]
                for part in parts[1:]:
                    obj = getattr(obj, part)

            except (KeyError, AttributeError):
                pass
            else:
                fake_locals[name] = obj
                continue

            try:
                fake_locals[name] = ask_for_it_by_name(value)
            except ImportError:
                if name == 'SouthFieldClass':
                    raise ValueError("Cannot import the required field '%s'" % value)
                else:
                    print("WARNING: Cannot import '%s'" % value)

        fake_locals = ModelsLocals(fake_locals)
        return eval(code, globals(), fake_locals)

    def make_meta(self, app, model, data, stub=False):
        """Makes a Meta class out of a dict of eval-able arguments."""
        results = {'app_label': app}
        for key, code in data.items():
            if key in ('_bases', '_ormbases'):
                continue
            if stub and key in ('order_with_respect_to', ):
                continue
            try:
                results[key] = self.eval_in_context(code, app)
            except (NameError, AttributeError) as e:
                raise ValueError("Cannot successfully create meta field '%s' for model '%s.%s': %s." % (
                 key, app, model, e))

        return type('Meta', tuple(), results)

    def make_model(self, app, name, data):
        """Makes a Model class out of the given app name, model name and pickled data."""
        if '_ormbases' in data['Meta']:
            for key in data['Meta']['_ormbases']:
                key = key.lower()
                if key not in self.models:
                    raise ORMBaseNotIncluded('Cannot find ORM base %s' % key)
                elif isinstance(self.models[key], string_types):
                    raise UnfreezeMeLater()

            bases = [ self.models[key.lower()] for key in data['Meta']['_ormbases'] ]
        else:
            if '_bases' in data['Meta']:
                bases = map(ask_for_it_by_name, data['Meta']['_bases'])
            else:
                bases = [
                 models.Model]
            meta = self.make_meta(app, name, data['Meta'], data.get('_stub', False))
            failed_fields = {}
            fields = {}
            stub = False
            for fname, params in data.items():
                if fname == '_stub':
                    stub = bool(params)
                    continue
                else:
                    if fname == 'Meta':
                        continue
                    elif not params:
                        raise ValueError("Field '%s' on model '%s.%s' has no definition." % (fname, app, name))
                    elif isinstance(params, string_types):
                        code = params
                        extra_imports = {}
                    else:
                        if len(params) == 1:
                            params = (
                             params[0], [], {})
                        if len(params) == 3:
                            code = 'SouthFieldClass(%s)' % (', ').join(params[1] + [ '%s=%s' % (n, v) for n, v in params[2].items() ])
                            extra_imports = {'SouthFieldClass': params[0]}
                        else:
                            raise ValueError("Field '%s' on model '%s.%s' has a weird definition length (should be 1 or 3 items)." % (fname, app, name))
                    try:
                        field = self.eval_in_context(code, app, extra_imports)
                    except (NameError, AttributeError, AssertionError, KeyError):
                        failed_fields[fname] = (code, extra_imports)

                    fields[fname] = field

            more_kwds = {}
            try:
                app_module = models.get_app(app)
                more_kwds['__module__'] = app_module.__name__
            except ImproperlyConfigured:
                more_kwds['__module__'] = '_south_mock'

        more_kwds['Meta'] = meta
        fields.update(more_kwds)
        model = type(str(name), tuple(bases), fields)
        if stub:
            model.objects = WhinyManager()
            model.__init__ = whiny_method
        else:
            model.objects = NoDryRunManager(model.objects)
        if failed_fields:
            model._failed_fields = failed_fields
        return model

    def retry_failed_fields(self):
        """Tries to re-evaluate the _failed_fields for each model."""
        for modelkey, model in self.models.items():
            app, modelname = modelkey.split('.', 1)
            if hasattr(model, '_failed_fields'):
                for fname, (code, extra_imports) in model._failed_fields.items():
                    try:
                        field = self.eval_in_context(code, app, extra_imports)
                    except (NameError, AttributeError, AssertionError, KeyError) as e:
                        raise ValueError("Cannot successfully create field '%s' for model '%s': %s." % (
                         fname, modelname, e))
                    else:
                        model.add_to_class(fname, field)


class WhinyManager(object):
    """A fake manager that whines whenever you try to touch it. For stub models."""

    def __getattr__(self, key):
        raise AttributeError('You cannot use items from a stub model.')


class NoDryRunManager(object):
    """
    A manager that always proxies through to the real manager,
    unless a dry run is in progress.
    """

    def __init__(self, real):
        self.real = real

    def __getattr__(self, name):
        if db.dry_run:
            raise AttributeError("You are in a dry run, and cannot access the ORM.\nWrap ORM sections in 'if not db.dry_run:', or if the whole migration is only a data migration, set no_dry_run = True on the Migration class.")
        return getattr(self.real, name)


def whiny_method(*a, **kw):
    raise ValueError('You cannot instantiate a stub model.')