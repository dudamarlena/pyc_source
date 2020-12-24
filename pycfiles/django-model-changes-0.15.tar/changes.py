# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kajic/projects/django-model-changes/django_model_changes/changes.py
# Compiled at: 2013-12-26 05:29:21
from django.db.models import signals
from .signals import post_change
SAVE = 0
DELETE = 1

class ChangesMixin(object):
    r"""
    ChangesMixin keeps track of changes for model instances.

    It allows you to retrieve the following states from an instance:

    1. current_state()
        The current state of the instance.
    2. previous_state()
        The state of the instance **after** it was created, saved
        or deleted the last time.
    3. old_state()
        The previous previous_state(), i.e. the state of the
        instance **before** it was created, saved or deleted the
        last time.

    It also provides convenience methods to get changes between states:

    1. changes()
        Changes from previous_state to current_state.
    2. previous_changes()
        Changes from old_state to previous_state.
    3. old_changes()
        Changes from old_state to current_state.

    And the following methods to determine if an instance was/is persisted in
    the database:

    1. was_persisted()
        Was the instance persisted in its old state.
    2. is_persisted()
        Is the instance is_persisted in its current state.

    This schematic tries to illustrate how these methods relate to
    each other::

        after create/save/delete            after save/delete                  now
        |                                   |                                  |
        .-----------------------------------.----------------------------------.
        |\                                  |\                                 |        | \                                 | \                                |         |  old_state()                      |  previous_state()                |  current_state()
        |                                   |                                  |
        |-----------------------------------|----------------------------------|
        |  previous_changes() (prev - old)  |  changes() (cur - prev)          |
        |-----------------------------------|----------------------------------|
        |                      old_changes()  (cur - old)                      |
        .----------------------------------------------------------------------.
         \                                                                                \                                                                                 was_persisted()                                                        is_persisted()

    """

    def __init__(self, *args, **kwargs):
        super(ChangesMixin, self).__init__(*args, **kwargs)
        self._states = []
        self._save_state(new_instance=True)
        signals.post_save.connect(_post_save, sender=self.__class__, dispatch_uid='django-changes-%s' % self.__class__.__name__)
        signals.post_delete.connect(_post_delete, sender=self.__class__, dispatch_uid='django-changes-%s' % self.__class__.__name__)

    def _save_state(self, new_instance=False, event_type='save'):
        if event_type == DELETE:
            self.pk = None
        self._states.append(self.current_state())
        if len(self._states) > 2:
            self._states.pop(0)
        if not new_instance:
            post_change.send(sender=self.__class__, instance=self)
        return

    def _instance_from_state(self, state):
        """
        Creates an instance from a previously saved state.
        """
        instance = self.__class__()
        for key, value in state.items():
            setattr(instance, key, value)

        return instance

    def current_state(self):
        """
        Returns a ``field -> value`` dict of the current state of the instance.
        """
        fields = {}
        for field in self._meta.local_fields:
            fields[field.attname] = getattr(self, field.attname)
            if field.rel:
                descriptor = self.__class__.__dict__[field.name]
                if hasattr(self, descriptor.cache_name):
                    fields[field.name] = getattr(self, descriptor.cache_name)

        return fields

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
        return dict([ (key, (was, current[key])) for key, was in other.iteritems() if was != current[key] ])

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
        return self._instance_from_state(self.old_state())

    def previous_instance(self):
        """
        Returns an instance of this model in its previous state.
        """
        return self._instance_from_state(self.previous_state())


def _post_save(sender, instance, **kwargs):
    instance._save_state(new_instance=False, event_type=SAVE)


def _post_delete(sender, instance, **kwargs):
    instance._save_state(new_instance=False, event_type=DELETE)