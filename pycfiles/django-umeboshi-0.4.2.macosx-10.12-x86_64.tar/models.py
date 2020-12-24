# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/umeboshi/models.py
# Compiled at: 2016-11-01 11:12:10
"""
django-umeboshi.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Umeboshi uses the Event model to repesent a single instance of deferred
computation. It is represented as a reference to a specific class defined
in the application (a Routine), combined with the arguments passed to that
Routine's `_run` function and the details of its scheduling. This includes,
after the computation is processed, the status of the computation.
"""
import hashlib, pickle
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.timezone import now, timedelta
from django_light_enums import enum
from django_extensions.db import fields
from model_utils.managers import QueryManager
from umeboshi.exceptions import RoutineRunException, RoutineRetryException
from umeboshi.triggers import TriggerBehavior

class BaseModel(models.Model):

    class Meta:
        abstract = True

    def get_admin_url(self):

        def view_name_for_model(model):
            return ('admin:{}_{}_change').format(model._meta.app_label, model._meta.model_name)

        return reverse(view_name_for_model(self), args=(self.id,))

    def instance_from_db(self):
        """
        Returns a fresh copy of this object from db.
        """
        return self.__class__.objects.get(pk=self.pk)


class EventManager(QueryManager):

    def get_routine_events(self, routine):
        """
        Return all Events of a given type that are currently scheduled.
        """
        return self.filter(trigger_name=routine.trigger_name, status=Event.Status.CREATED).order_by('datetime_scheduled')


class Event(BaseModel):
    """
    Events are the way that Umeboshi Routines are scheduled to be run. An Event
    object is saved to the database with the `trigger_name` of the Routine, as
    well as the pickled arguments to the Routine and the scheduling details.
    """

    class Meta:
        app_label = 'umeboshi'
        index_together = (
         ('datetime_processed', 'datetime_scheduled'),
         ('data_hash', 'datetime_processed', 'trigger_name'))

    uuid = fields.ShortUUIDField(unique=True, editable=False)
    objects = EventManager()
    trigger_name = models.CharField(db_index=True, max_length=50)
    task_group = models.CharField(db_index=True, max_length=256, null=True)
    data_pickled = models.BinaryField(blank=True, editable=False)
    data_hash = models.CharField(db_index=True, max_length=32)
    datetime_created = models.DateTimeField(null=True, auto_now_add=True)
    datetime_scheduled = models.DateTimeField(db_index=True)
    datetime_processed = models.DateTimeField(db_index=True, null=True)

    class Status(enum.Enum):
        """
        Event statuses are stored with the object. An Event scheduled to be
        processed in the future is `CREATED`; after processing it can be in a
        variety of states.
        """
        CREATED = 0
        FAILED = -1
        CANCELLED = -2
        BROKEN = -3
        SUCCESSFUL = 1

    status = enum.EnumField(Status, default=Status.CREATED)

    @staticmethod
    def marshal_data(data):
        """
        Events use `pickle` to marshal their argument data for storage.
        """
        return pickle.dumps(data)

    @staticmethod
    def unmarshal_data(data):
        return pickle.loads(data)

    @staticmethod
    def hash_data(data):
        """
        Umeboshi calculates an md5 hash of argument data.
        """
        return hashlib.md5(data).hexdigest()

    @property
    def args(self):
        """
        Unmarshaled data is available for inspection on the instantiated Event.
        """
        if not hasattr(self, '_data'):
            self._data = [] if self.has_data else self.unmarshal_data(self.data_pickled)
        return self._data

    @args.setter
    def args(self, value):
        self._data = value

    @property
    def has_data(self):
        return len(self.data_pickled) <= 0

    def process(self):
        """
        When an Event's scheduled datetime comes up, it will be processed.
        """
        from umeboshi.runner import runner
        try:
            try:
                routine_class = runner.get_routine_class(self.trigger_name)
                routine = routine_class(*self.args)
                if not runner.check_validity(routine):
                    self.status = self.Status.CANCELLED
                else:
                    runner.run(routine)
                    self.status = self.Status.SUCCESSFUL
                if routine_class.behavior == TriggerBehavior.DELETE_AFTER_PROCESSING:
                    self.delete()
            except RoutineRunException:
                self.status = self.Status.FAILED
            except RoutineRetryException as e:
                self.status = self.Status.FAILED
                if e.new_datetime:
                    self.retry_schedule(e.new_datetime)
                else:
                    self.retry_schedule()
            except:
                self.status = self.Status.BROKEN
                raise

        finally:
            if self.pk:
                self.datetime_processed = timezone.now()
                self.save()

    def retry_schedule(self, new_datetime=now() + timedelta(hours=1)):
        if self.status in (self.Status.SUCCESSFUL, self.Status.CREATED):
            raise ValidationError('Can only reschedule a failed event.')
        else:
            return Event.objects.create(trigger_name=self.trigger_name, datetime_scheduled=new_datetime, status=Event.Status.CREATED, args=self.args)

    def cancel(self):
        self.datetime_processed = timezone.now()
        self.status = self.Status.CANCELLED
        self.save()

    def save(self, *args, **kwargs):
        self.data_pickled = self.marshal_data(self.args)
        self.data_hash = self.hash_data(self.data_pickled)
        super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return ('Umeboshi Event #{}').format(self.pk)