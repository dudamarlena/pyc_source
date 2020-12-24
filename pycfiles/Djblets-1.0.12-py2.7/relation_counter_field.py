# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/db/fields/relation_counter_field.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import threading, weakref
from contextlib import contextmanager
import django
from django.db.models import F, Q
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete
from django.utils import six
from djblets.db.fields.counter_field import CounterField

class InstanceState(weakref.ref):
    """Tracks state for a RelationCounterField instance assocation.

    State instances are bound to the lifecycle of a model instance.
    They're a type of weak reference for model instances that contain
    additional state needed for the tracking and update process.

    These are used for looking up the proper instance and
    RelationCounterFields on the other end of a reverse relation, given
    a model, relation name, and IDs, through the
    :py:attr:`RelationCounterField._saved_instance_states` or
    :py:attr:`RelationCounterField._unsaved_instance_states` or
    dictionaries.

    Instance states can either represent saved instances or unsaved
    instances. Unsaved instance states represent instances that haven't yet
    been saved to the database (with a primary key of ``None``). While saved
    instance states exist per-instance/relation name, there's only one
    unsaved instance state per instance.

    Once an unsaved instance is saved, new instance states will be stored
    for each field associated (which many turn into multiple states, as
    there's one per relation name). The old unsaved instance state is then
    discarded.
    """

    def __init__(self, model_instance):
        """Set up the state.

        Args:
            model_instance (django.db.models.Model):
                The model instance that this state tracks.
        """
        super(InstanceState, self).__init__(model_instance)
        self.to_clear = set()
        self.field_names = set()
        self._model_cls = type(model_instance)

    @property
    def model_instance(self):
        """The model instance being tracked.

        This will be ``None`` if the instance has been destroyed.
        """
        return self()

    def track_field(self, field):
        """Track information on a field referencing this state.

        Args:
            field (django.db.models.Field):
                The field to track.
        """
        self.field_names.add(field.attname)

    def __repr__(self):
        """Return a string representation of the instance state.

        Returns:
            unicode:
            A string representation listing the instance information.
        """
        model_instance = self.model_instance
        if model_instance is not None:
            return b'<InstanceState for %s.pk=%s>' % (
             model_instance.__class__.__name__,
             model_instance.pk)
        else:
            return b'<InstanceState for %r (destroyed)>' % self.model_cls
            return


class RelationTracker(object):
    """Tracks relations and updates state for all affected CounterFields.

    This class is responsible for all the hard work of updating
    RelationCounterFields refererring to a relation, based on updates
    to that relation. It's really the meat of RelationCounterField.

    Each RelationTracker is responsible for a given model/relation name
    pairing, across all instances of a model and across all
    RelationCounterFields following that relation name.

    The main reason the code lives here instead of in each
    RelationCounterField is to keep state better in sync and to ensure
    we're only ever dealing with one set of queries per relation name.
    We're also simplifying signal registration, helping to make things
    less error-prone.
    """

    def __init__(self, model_cls, rel_field_name):
        self._rel_field_name = rel_field_name
        if django.VERSION >= (1, 8):
            self._rel_field = model_cls._meta.get_field(rel_field_name)
            rel_model = self._rel_field.model
            is_rel_direct = not self._rel_field.auto_created or self._rel_field.concrete
            is_m2m = self._rel_field.many_to_many
        else:
            self._rel_field, rel_model, is_rel_direct, is_m2m = model_cls._meta.get_field_by_name(rel_field_name)
        self._is_rel_reverse = not is_rel_direct
        if not is_m2m and is_rel_direct:
            raise ValueError(b"RelationCounterField cannot work with the forward end of a ForeignKey ('%s')" % rel_field_name)
        dispatch_uid = b'%s-%s.%s-related-save' % (
         id(self),
         self.__class__.__module__,
         self.__class__.__name__)
        if is_m2m:
            if is_rel_direct:
                m2m_field = self._rel_field
                self._related_name = m2m_field.rel.related_name
            else:
                m2m_field = self._rel_field.field
                self._related_name = m2m_field.attname
            m2m_changed.connect(self._on_m2m_changed, weak=False, sender=m2m_field.rel.through, dispatch_uid=dispatch_uid)
        else:
            assert not is_rel_direct
            model = self._get_rel_field_related_model(self._rel_field)
            self._related_name = self._rel_field.field.attname
            post_delete.connect(self._on_related_delete, weak=False, sender=model, dispatch_uid=dispatch_uid)
            post_save.connect(self._on_related_save, weak=False, sender=model, dispatch_uid=dispatch_uid)

    def _increment_fields(self, states, by=1):
        """Increment all associated fields' counters on instance states.

        Args:
            states (list of InstanceState):
                The instance states containing the model instance fields to
                increment.

            by (int, optional):
                The value to increment by.
        """
        with self._update_sync_fields(states) as (model_instance, field_names):
            RelationCounterField.increment_many(model_instance, {field_name:by for field_name in field_names})

    def _decrement_fields(self, states, by=1):
        """Decrement all associated fields' counters on instance states.

        Args:
            states (list of InstanceState):
                The instance states containing the model instance fields to
                decrement.

            by (int, optional):
                The value to decrement by.
        """
        with self._update_sync_fields(states) as (model_instance, field_names):
            RelationCounterField.decrement_many(model_instance, {field_name:by for field_name in field_names})

    def _zero_fields(self, states):
        """Zero out all associated fields' counters on instance states.

        Args:
            states (list of InstanceState):
                The instance states containing the model instance fields to
                zero out.
        """
        with self._update_sync_fields(states) as (model_instance, field_names):
            RelationCounterField._set_values(model_instance, {field_name:0 for field_name in field_names})

    def _reload_fields(self, states):
        """Reload all associated fields' counters on instance states.

        Args:
            states (list of InstanceState):
                The instance states containing the model instance fields to
                reload.
        """
        with self._update_sync_fields(states) as (model_instance, field_names):
            RelationCounterField._reload_model_instance(model_instance, field_names)

    @contextmanager
    def _update_sync_fields(self, states):
        """Update field values and synchronize them to other model instances.

        This calculates a main state from the list of instance states,
        gathering the model instance and field names and yielding them as
        context to the calling method. After that method makes the field
        changes needed, this will synchronize those values to all other model
        instances from the other states passed.

        Args:
            states (list of InstanceState):
                The list of states to update.

        Yields:
            tuple of (InstanceState, list of unicode):
            The main model instance to work on, and the list of field names
            to update.
        """
        main_state = states[0]
        model_instance = main_state.model_instance
        if model_instance is not None:
            yield (
             model_instance, main_state.field_names)
            if len(states) > 1:
                self._sync_fields_from_main_state(main_state, states[1:])
        return

    def _on_m2m_changed(self, instance, action, reverse, model, pk_set, **kwargs):
        """Handler for when a M2M relation has been updated.

        This will figure out the necessary operations that may need to be
        performed, given the update.

        For post_add/post_remove operations, it's pretty simple. We see
        if there are any instances (by way of stored state) for any of the
        affected IDs, and we re-initialize them.

        For clear operations, it's more tricky. We have to fetch all
        instances on the other side of the relation before any database
        changes are made, cache them in the InstanceState, and then update
        them all in post_clear.
        """
        if reverse != self._is_rel_reverse:
            return
        is_post_clear = action == b'post_clear'
        is_post_add = action == b'post_add'
        is_post_remove = action == b'post_remove'
        if is_post_clear or is_post_add or is_post_remove:
            states = RelationCounterField._get_saved_states(type(instance), instance.pk, self._rel_field_name)
            if states:
                if pk_set and is_post_add:
                    self._increment_fields(states, by=len(pk_set))
                elif pk_set and is_post_remove:
                    self._decrement_fields(states, by=len(pk_set))
                elif is_post_clear:
                    self._zero_fields(states)
                if not pk_set and is_post_clear:
                    main_state = states[0]
                    pk_set = main_state.to_clear
                    main_state.to_clear = set()
            if pk_set:
                if is_post_add:
                    update_by = 1
                else:
                    update_by = -1
                self._update_counts(model, pk_set, b'_related_name', update_by)
                for pk in pk_set:
                    states = RelationCounterField._get_saved_states(model, pk, self._related_name)
                    if states:
                        self._reload_fields(states)

        elif action == b'pre_clear':
            states = RelationCounterField._get_saved_states(instance.__class__, instance.pk, self._rel_field_name)
            if states:
                main_state = states[0]
                mgr = getattr(instance, self._rel_field_name)
                main_state.to_clear.update(mgr.values_list(b'pk', flat=True))

    def _on_related_delete(self, instance, **kwargs):
        """Handler for when a ForeignKey relation is deleted.

        This will check if a model entry that has a ForeignKey relation
        to this field's parent model entry has been deleted from the
        database. If so, any associated counter fields on this end will be
        decremented.
        """
        states = self._get_reverse_foreign_key_states(instance)
        if states:
            self._decrement_fields(states)
        else:
            self._update_unloaded_fkey_rel_counts(instance, -1)

    def _on_related_save(self, instance=None, created=False, raw=False, **kwargs):
        """Handler for when a ForeignKey relation is created.

        This will check if a model entry has been created that has a
        ForeignKey relation to this field's parent model entry. If so, any
        associated counter fields on this end will be decremented.
        """
        if raw or not created:
            return
        states = self._get_reverse_foreign_key_states(instance)
        if states:
            self._increment_fields(states)
        else:
            self._update_unloaded_fkey_rel_counts(instance, 1)

    def _update_unloaded_fkey_rel_counts(self, instance, by):
        """Updates unloaded model entry counters for a ForeignKey relation.

        This will get the ID of the model being referenced by the
        matching ForeignKey in the provided instance. If set, it will
        update all RelationCounterFields on that model that are tracking
        the ForeignKey.
        """
        rel_pk = getattr(instance, self._rel_field.field.attname)
        if rel_pk is not None:
            self._update_counts(self._get_rel_field_parent_model(self._rel_field), [
             rel_pk], b'_rel_field_name', by)
        return

    def _update_counts(self, model_cls, pks, rel_attname, update_by):
        """Updates counts on all model entries matching the given criteria.

        This will update counts on all RelationCounterFields on all entries
        of the given model in the database that are tracking the given
        relation.
        """
        values = dict((field.attname, F(field.attname) + update_by) for field in model_cls._meta.local_fields if isinstance(field, RelationCounterField) and getattr(field._relation_tracker, rel_attname) == self._rel_field_name)
        if values:
            if len(pks) == 1:
                q = Q(pk=list(pks)[0])
            else:
                q = Q(pk__in=pks)
            model_cls.objects.filter(q).update(**values)

    def _sync_fields_from_main_state(self, main_state, other_states):
        """Synchronize field values across instances.

        This will take a main instance containing up-to-date values and
        synchronize those values to all other instances.

        Args:
            main_state (InstanceState):
                The main state to take values from.

            other_states (list of InstanceState):
                The other states to synchronize values to.
        """
        main_instance = main_state.model_instance
        if main_instance is not None:
            for other_state in other_states:
                other_instance = other_state.model_instance
                if other_instance is not None:
                    for field_name in other_state.field_names:
                        setattr(other_instance, field_name, getattr(main_instance, field_name))

        else:
            for other_state in other_states:
                self._reload_fields(other_state)

        return

    def _get_reverse_foreign_key_states(self, instance):
        """Return InstanceStates for the other end of a ForeignKey.

        This is used when listening to changes on models that establish a
        ForeignKey to this counter field's parent model. Given the instance
        on that end, we can get the state for this end.

        Args:
            instance (django.db.model.Model):
                The instance on the other end of the relation.

        Returns:
            list of InstanceState:
            The list of :py:class:`InstanceState`s for each instance on this
            end of the relation.
        """
        return RelationCounterField._get_saved_states(self._get_rel_field_parent_model(self._rel_field), getattr(instance, self._rel_field.field.attname), self._rel_field_name)

    def _get_rel_field_parent_model(self, rel_field):
        """Return the model owning a relation field.

        This provides compatibility across different versions of Django.
        """
        if hasattr(rel_field, b'parent_model'):
            return rel_field.parent_model
        else:
            return rel_field.model

    def _get_rel_field_related_model(self, rel_field):
        """Return the model on the other side of a relation field.

        This provides compatibility across different versions of Django.
        """
        if hasattr(rel_field, b'related_model'):
            return rel_field.related_model
        else:
            return rel_field.model


class RelationCounterField(CounterField):
    """A field that provides an atomic count of a relation.

    RelationCounterField is a specialization of CounterField that tracks
    how many objects there are on the other side of a ManyToManyField or
    ForeignKey relation.

    RelationCounterField takes the name of a relation (either a field name,
    for a forward ManyToManyField relation, or the "related_name" for
    the reverse relation of another model's ForeignKey or ManyToManyField.
    (Note that using a forward ForeignKey relation is considered invalid,
    as the count can only be 1 or 0.)

    The counter will be initialized with the number of objects on the
    other side of the relation, and this will be kept updated so long as
    all updates to the table are made using standard create/save/delete
    operations on models.

    Note that updating a relation outside of a model's regular API (such as
    through raw SQL or something like an update() call) will cause the
    counters to get out of sync. They would then need to be reset using
    ``reinit_{field_name}``.
    """
    _saved_instance_states = {}
    _unsaved_instance_states = {}
    _relation_trackers = {}
    _state_lock = threading.RLock()
    _signals_setup = False

    @classmethod
    def has_tracked_states(cls):
        """Return whether there are currently any states being tracked.

        This will begin by cleaning up any expired states whose instances
        have been destroyed, if there are any. Then it will check if there
        are any remaining states still being tracked and return a result.

        Returns:
            bool:
            ``True`` if there are any states still being tracked.
            ``False`` if not.
        """
        cls._cleanup_state()
        return bool(cls._saved_instance_states) or bool(cls._unsaved_instance_states)

    @classmethod
    def _cleanup_state(cls, instance_cls=None, instance_pk=None, instance_id=None):
        """Clean up state for one or more instances.

        This will clear away any state tied to a destroyed instance, an
        instance with a given reference ID, or an instance with a given class
        and database ID. It's used to ensure that any old, removed entries
        (say, from a previous unit test, or when transitioning from an unsaved
        instance to saved) are cleared away before storing new state.

        Args:
            instance_cls (type, optional):
                The model class of the instance being removed.

            instance_pk (int, optional):
                The database ID of the instance (if known and if saved).

            instance_id (int, optional):
                The reference ID of the instance.
        """
        with cls._state_lock:
            cls._cleanup_state_for_dict(cls._unsaved_instance_states, instance_cls=instance_cls, instance_pk=instance_pk, instance_id=instance_id)
            to_remove = []
            for key, states in six.iteritems(cls._saved_instance_states):
                cls._cleanup_state_for_dict(states, instance_cls=instance_cls, instance_pk=instance_pk, instance_id=instance_id)
                if not states:
                    to_remove.append(key)

            for key in to_remove:
                cls._saved_instance_states.pop(key, None)

        return

    @classmethod
    def _cleanup_state_for_dict(cls, states, instance_cls, instance_pk, instance_id):
        """Clean up state in a states dictionary.

        This is a utility function used by :py:meth:`_cleanup_state` for
        clearing out any state entries matching the given instance information
        or for those states that are no longer active.

        Args:
            states (list of InstanceState):
                The list of instance states to clean up.

            instance_cls (type, optional):
                The model class of the instance being removed.

            instance_pk (int, optional):
                The database ID of the instance (if known and if saved).

            instance_id (int, optional):
                The reference ID of the instance.
        """
        to_remove = []
        for key, state in six.iteritems(states):
            model_instance = state.model_instance
            if model_instance is None or id(model_instance) == instance_id or type(model_instance) is instance_cls and model_instance.pk == instance_pk:
                to_remove.append(key)

        for key in to_remove:
            states.pop(key, None)

        return

    @classmethod
    def _store_state(cls, instance, field):
        """Store state for a model instance and field.

        This constructs an :py:class:`InstanceState` instance for the given
        model instance and :py:class:`RelationCounterField`. It then associates
        it with the model instance and stores it.

        If the instance has not yet been saved, the constructed state will be
        tied to the instance and stored in :py:attr:`_unsaved_instance_states`.
        If the instance has been saved, the constructed state will be tied to
        a combination of the instance and field relation name and stoerd in
        :py:attr:`_saved_instance_states`.

        Saved instances will have a :samp:`_{fieldname}_state` attribute stored
        that points to the :py:class:`InstanceState`, keeping the state's
        reference alive as long as the instance is alive.
        """
        cls._cleanup_state()
        with cls._state_lock:
            if instance.pk is None:
                states = cls._unsaved_instance_states
            else:
                main_key = (
                 type(instance), instance.pk, field._rel_field_name)
                states = cls._saved_instance_states.setdefault(main_key, {})
            key = id(instance)
            try:
                state = states[key]
            except KeyError:
                state = InstanceState(instance)
                states[key] = state

            state.track_field(field)
            instance._tracks_relcounterfield_states = True
            if instance.pk is not None:
                setattr(instance, b'_%s_instance_state' % field.attname, state)
        return

    @classmethod
    def _get_saved_states(cls, model_cls, instance_pk, rel_field_name):
        """Return instance states for the given parameters.

        The returned dictionary will contain a mapping of object IDs for
        each instance to the :py:class:`InstanceState` for each saved instance
        matching the model class, primary key, and field name.

        Args:
            model_cls (type):
                The model class of the instances to look up.

            instance_pk (int):
                The database ID of the instances to look up.

            rel_field_name (unicode):
                The name of the field relationship associated with the
                instances.

        Returns:
            list of InstanceState:
            A list of all alive instance states for the given criteria. The
            first is considered the "main" state for an operation.

            If no suitable instances are found, this will return ``None``.
        """
        key = (
         model_cls, instance_pk, rel_field_name)
        with cls._state_lock:
            states = cls._saved_instance_states.get(key)
            if states is not None:
                return [ state for state in six.itervalues(states) if state.model_instance is not None
                       ]
        return

    @classmethod
    def _on_instance_first_save(cls, instance=None, created=False, **kwargs):
        """Handler for the first save on a newly created instance.

        This will reset information on this instance, removing this
        existing state, and will then add new instance states for each
        field relation.

        Args:
            instance (django.db.models.Model):
                The model instance being saved.

            created (bool):
                Whether the object was created. This must always be
                true for this handler.

            **kwargs (dict):
                Extra keyword arguments passed to the handler.

        Returns:
            bool:
            ``True`` if this instance was handled. ``False`` if it was ignored.
        """
        if instance is None or not instance.pk or not created or not getattr(instance, b'_tracks_relcounterfield_states', False):
            return False
        instance_id = id(instance)
        try:
            state = cls._unsaved_instance_states[instance_id]
        except KeyError:
            return

        model_instance = state.model_instance
        if model_instance is None:
            return False
        else:
            assert instance is model_instance
            with cls._state_lock:
                cls._unsaved_instance_states.pop(instance_id, None)
            for field in type(instance)._meta.local_fields:
                if isinstance(field, cls):
                    cls._store_state(instance, field)

            return True

    @classmethod
    def _on_instance_pre_delete(cls, instance=None, **kwargs):
        """Handler for when an instance is about to be deleted.

        This will reset the state of the instance, unregistering it from
        lists, and removing any pending signal connections.

        Args:
            instance (django.db.models.Model):
                The instance being deleted.

            **kwargs (dict):
                Extra keyword arguments passed to the handler.

        Returns:
            bool:
            ``True`` if this instance was handled. ``False`` if it was ignored.
        """
        if instance is None or not getattr(instance, b'_tracks_relcounterfield_states', False):
            return False
        instance_id = id(instance)
        assert instance_id not in cls._unsaved_instance_states
        cls._cleanup_state(instance_cls=type(instance), instance_pk=instance.pk, instance_id=instance_id)
        return True

    def __init__(self, rel_field_name=None, *args, **kwargs):

        def _initializer(model_instance):
            if model_instance.pk:
                return getattr(model_instance, rel_field_name).count()
            else:
                return 0

        kwargs[b'initializer'] = _initializer
        super(RelationCounterField, self).__init__(*args, **kwargs)
        self._rel_field_name = rel_field_name
        self._relation_tracker = None
        return

    def _do_post_init(self, instance):
        """Handle initialization of an instance of the parent model.

        This will begin the process of storing state about the model
        instance and listening to signals coming from the model on the
        other end of the relation.

        Args:
            instance (django.db.models.Model):
                The model instance being initialized.
        """
        super(RelationCounterField, self)._do_post_init(instance)
        cls = type(self)
        if not cls._signals_setup:
            dispatch_uid = b'%s.%s' % (cls.__module__, cls.__name__)
            post_save.connect(cls._on_instance_first_save, dispatch_uid=dispatch_uid)
            pre_delete.connect(cls._on_instance_pre_delete, dispatch_uid=dispatch_uid)
            cls._signals_setup = True
        cls._store_state(instance, self)
        if not self._relation_tracker:
            instance_cls = type(instance)
            key = (instance_cls, self._rel_field_name)
            try:
                self._relation_tracker = cls._relation_trackers[key]
            except KeyError:
                self._relation_tracker = RelationTracker(instance_cls, self._rel_field_name)
                cls._relation_trackers[key] = self._relation_tracker