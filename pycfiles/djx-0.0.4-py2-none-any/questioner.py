# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/migrations/questioner.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import print_function, unicode_literals
import importlib, os, sys
from django.apps import apps
from django.db.models.fields import NOT_PROVIDED
from django.utils import datetime_safe, six, timezone
from django.utils.six.moves import input
from .loader import MigrationLoader

class MigrationQuestioner(object):
    """
    Gives the autodetector responses to questions it might have.
    This base class has a built-in noninteractive mode, but the
    interactive subclass is what the command-line arguments will use.
    """

    def __init__(self, defaults=None, specified_apps=None, dry_run=None):
        self.defaults = defaults or {}
        self.specified_apps = specified_apps or set()
        self.dry_run = dry_run

    def ask_initial(self, app_label):
        """Should we create an initial migration for the app?"""
        if app_label in self.specified_apps:
            return True
        else:
            try:
                app_config = apps.get_app_config(app_label)
            except LookupError:
                return self.defaults.get(b'ask_initial', False)

            migrations_import_path, _ = MigrationLoader.migrations_module(app_config.label)
            if migrations_import_path is None:
                return self.defaults.get(b'ask_initial', False)
            try:
                migrations_module = importlib.import_module(migrations_import_path)
            except ImportError:
                return self.defaults.get(b'ask_initial', False)

            if getattr(migrations_module, b'__file__', None):
                filenames = os.listdir(os.path.dirname(migrations_module.__file__))
            elif hasattr(migrations_module, b'__path__'):
                if len(migrations_module.__path__) > 1:
                    return False
                filenames = os.listdir(list(migrations_module.__path__)[0])
            return not any(x.endswith(b'.py') for x in filenames if x != b'__init__.py')
            return

    def ask_not_null_addition(self, field_name, model_name):
        """Adding a NOT NULL field to a model"""
        return

    def ask_not_null_alteration(self, field_name, model_name):
        """Changing a NULL field to NOT NULL"""
        return

    def ask_rename(self, model_name, old_name, new_name, field_instance):
        """Was this field really renamed?"""
        return self.defaults.get(b'ask_rename', False)

    def ask_rename_model(self, old_model_state, new_model_state):
        """Was this model really renamed?"""
        return self.defaults.get(b'ask_rename_model', False)

    def ask_merge(self, app_label):
        """Do you really want to merge these migrations?"""
        return self.defaults.get(b'ask_merge', False)

    def ask_auto_now_add_addition(self, field_name, model_name):
        """Adding an auto_now_add field to a model"""
        return


class InteractiveMigrationQuestioner(MigrationQuestioner):

    def _boolean_input(self, question, default=None):
        result = input(b'%s ' % question)
        if not result and default is not None:
            return default
        else:
            while len(result) < 1 or result[0].lower() not in b'yn':
                result = input(b'Please answer yes or no: ')

            return result[0].lower() == b'y'

    def _choice_input(self, question, choices):
        print(question)
        for i, choice in enumerate(choices):
            print(b' %s) %s' % (i + 1, choice))

        result = input(b'Select an option: ')
        while True:
            try:
                value = int(result)
                if 0 < value <= len(choices):
                    return value
            except ValueError:
                pass

            result = input(b'Please select a valid option: ')

    def _ask_default(self, default=b''):
        """
        Prompt for a default value.

        The ``default`` argument allows providing a custom default value (as a
        string) which will be shown to the user and used as the return value
        if the user doesn't provide any other input.
        """
        print(b'Please enter the default value now, as valid Python')
        if default:
            print((b"You can accept the default '{}' by pressing 'Enter' or you can provide another value.").format(default))
        print(b'The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now')
        print(b"Type 'exit' to exit this prompt")
        while True:
            if default:
                prompt = (b'[default: {}] >>> ').format(default)
            else:
                prompt = b'>>> '
            if six.PY3:
                code = input(prompt)
            else:
                code = input(prompt).decode(sys.stdin.encoding)
            if not code and default:
                code = default
            if not code:
                print(b"Please enter some code, or 'exit' (with no quotes) to exit.")
            elif code == b'exit':
                sys.exit(1)
            else:
                try:
                    return eval(code, {}, {b'datetime': datetime_safe, b'timezone': timezone})
                except (SyntaxError, NameError) as e:
                    print(b'Invalid input: %s' % e)

    def ask_not_null_addition(self, field_name, model_name):
        """Adding a NOT NULL field to a model"""
        if not self.dry_run:
            choice = self._choice_input(b"You are trying to add a non-nullable field '%s' to %s without a default; we can't do that (the database needs something to populate existing rows).\nPlease select a fix:" % (
             field_name, model_name), [
             b'Provide a one-off default now (will be set on all existing rows with a null value for this column)',
             b'Quit, and let me add a default in models.py'])
            if choice == 2:
                sys.exit(3)
            else:
                return self._ask_default()
        return

    def ask_not_null_alteration(self, field_name, model_name):
        """Changing a NULL field to NOT NULL"""
        if not self.dry_run:
            choice = self._choice_input(b"You are trying to change the nullable field '%s' on %s to non-nullable without a default; we can't do that (the database needs something to populate existing rows).\nPlease select a fix:" % (
             field_name, model_name), [
             b'Provide a one-off default now (will be set on all existing rows with a null value for this column)',
             b'Ignore for now, and let me handle existing rows with NULL myself (e.g. because you added a RunPython or RunSQL operation to handle NULL values in a previous data migration)',
             b'Quit, and let me add a default in models.py'])
            if choice == 2:
                return NOT_PROVIDED
            if choice == 3:
                sys.exit(3)
            else:
                return self._ask_default()
        return

    def ask_rename(self, model_name, old_name, new_name, field_instance):
        """Was this field really renamed?"""
        msg = b'Did you rename %s.%s to %s.%s (a %s)? [y/N]'
        return self._boolean_input(msg % (model_name, old_name, model_name, new_name,
         field_instance.__class__.__name__), False)

    def ask_rename_model(self, old_model_state, new_model_state):
        """Was this model really renamed?"""
        msg = b'Did you rename the %s.%s model to %s? [y/N]'
        return self._boolean_input(msg % (old_model_state.app_label, old_model_state.name,
         new_model_state.name), False)

    def ask_merge(self, app_label):
        return self._boolean_input(b'\nMerging will only work if the operations printed above do not conflict\n' + b'with each other (working on different fields or models)\n' + b'Do you want to merge these migration branches? [y/N]', False)

    def ask_auto_now_add_addition(self, field_name, model_name):
        """Adding an auto_now_add field to a model"""
        if not self.dry_run:
            choice = self._choice_input((b"You are trying to add the field '{}' with 'auto_now_add=True' to {} without a default; the database needs something to populate existing rows.\n").format(field_name, model_name), [
             b'Provide a one-off default now (will be set on all existing rows)',
             b'Quit, and let me add a default in models.py'])
            if choice == 2:
                sys.exit(3)
            else:
                return self._ask_default(default=b'timezone.now')
        return


class NonInteractiveMigrationQuestioner(MigrationQuestioner):

    def ask_not_null_addition(self, field_name, model_name):
        sys.exit(3)

    def ask_not_null_alteration(self, field_name, model_name):
        return NOT_PROVIDED

    def ask_auto_now_add_addition(self, field_name, model_name):
        sys.exit(3)