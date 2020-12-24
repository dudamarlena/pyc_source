# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ian/Documents/Programming/forks/django-model-changes-py3/django_model_changes/changes.py
# Compiled at: 2018-05-09 13:27:16
# Size of source mod 2**32: 7126 bytes
from django.db.models import signals
from .signals import post_change
SAVE = 0
DELETE = 1

class ChangesMixin(object):
    __doc__ = '\n    ChangesMixin keeps track of changes for model instances.\n\n    It allows you to retrieve the following states from an instance:\n\n    1. current_state()\n        The current state of the instance.\n    2. previous_state()\n        The state of the instance **after** it was created, saved\n        or deleted the last time.\n    3. old_state()\n        The previous previous_state(), i.e. the state of the\n        instance **before** it was created, saved or deleted the\n        last time.\n\n    It also provides convenience methods to get changes between states:\n\n    1. changes()\n        Changes from previous_state to current_state.\n    2. previous_changes()\n        Changes from old_state to previous_state.\n    3. old_changes()\n        Changes from old_state to current_state.\n\n    And the following methods to determine if an instance was/is persisted in\n    the database:\n\n    1. was_persisted()\n        Was the instance persisted in its old state.\n    2. is_persisted()\n        Is the instance is_persisted in its current state.\n\n    This schematic tries to illustrate how these methods relate to\n    each other::\n\n\n        after create/save/delete            after save/delete                  now\n        |                                   |                                  |\n        .-----------------------------------.----------------------------------.\n        |\\                                  |\\                                 |        | \\                                 | \\                                |         |  old_state()                      |  previous_state()                |  current_state()\n        |                                   |                                  |\n        |-----------------------------------|----------------------------------|\n        |  previous_changes() (prev - old)  |  changes() (cur - prev)          |\n        |-----------------------------------|----------------------------------|\n        |                      old_changes()  (cur - old)                      |\n        .----------------------------------------------------------------------.\n         \\                                                                                \\                                                                                 was_persisted()                                                        is_persisted()\n\n    '

    def __init__(self, *args, **kwargs):
        (super(ChangesMixin, self).__init__)(*args, **kwargs)
        self._states = []
        self._save_state(new_instance=True)
        signals.post_save.connect(_post_save,
          sender=(self.__class__), dispatch_uid=('django-changes-%s' % self.__class__.__name__))
        signals.post_delete.connect(_post_delete,
          sender=(self.__class__), dispatch_uid=('django-changes-%s' % self.__class__.__name__))

    def _save_state(self, new_instance=False, event_type='save'):
        if event_type == DELETE:
            self.pk = None
        else:
            self._states.append(self.current_state())
            if len(self._states) > 2:
                self._states.pop(0)
            if not new_instance:
                post_change.send(sender=(self.__class__), instance=self)

    def current_state(self):
        """
        Returns a ``field -> value`` dict of the current state of the instance.
        """
        field_names = set()
        [field_names.add(f.name) for f in self._meta.local_fields]
        [field_names.add(f.attname) for f in self._meta.local_fields]
        return dict([(field_name, getattr(self, field_name, None)) for field_name in field_names])

    def previous_state(self):
        """
        Returns a ``field -> value`` dict of the state of the instance after it
        was created, saved or deleted the previous time.
        """
        if len(self._states) > 1:
            return self._states[1]
        else:
            return self._states[0]

    def old_state(self):
        """
        Returns a ``field -> value`` dict of the state of the instance after
        it was created, saved or deleted the previous previous time. Returns
        the previous state if there is no previous previous state.
        """
        return self._states[0]

    def _changes(self, other, current):
        return dict([(key, (was, current[key])) for key, was in other.items() if was != current[key]])

    def changes(self):
        """
        Returns a ``field -> (previous value, current value)`` dict of changes
        from the previous state to the current state.
        """
        return self._changes(self.previous_state(), self.current_state())

    def old_changes(self):
        """
        Returns a ``field -> (previous value, current value)`` dict of changes
        from the old state to the current state.
        """
        return self._changes(self.old_state(), self.current_state())

    def previous_changes(self):
        """
        Returns a ``field -> (previous value, current value)`` dict of changes
        from the old state to the previous state.
        """
        return self._changes(self.old_state(), self.previous_state())

    def was_persisted(self):
        """
        Returns true if the instance was persisted (saved) in its old
        state.

        Examples::

            >>> user = User()
            >>> user.save()
            >>> user.was_persisted()
            False

            >>> user = User.objects.get(pk=1)
            >>> user.delete()
            >>> user.was_persisted()
            True
        """
        pk_name = self._meta.pk.name
        return bool(self.old_state()[pk_name])

    def is_persisted(self):
        """
        Returns true if the instance is persisted (saved) in its current
        state.

        Examples:

            >>> user = User()
            >>> user.save()
            >>> user.is_persisted()
            True

            >>> user = User.objects.get(pk=1)
            >>> user.delete()
            >>> user.is_persisted()
            False
        """
        return bool(self.pk)

    def old_instance(self):
        """
        Returns an instance of this model in its old state.
        """
        return (self.__class__)(**self.old_state())

    def previous_instance(self):
        """
        Returns an instance of this model in its previous state.
        """
        return (self.__class__)(**self.previous_state())


def _post_save(sender, instance, **kwargs):
    instance._save_state(new_instance=False, event_type=SAVE)


def _post_delete(sender, instance, **kwargs):
    instance._save_state(new_instance=False, event_type=DELETE)