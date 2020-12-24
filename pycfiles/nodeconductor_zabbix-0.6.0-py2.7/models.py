# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/models.py
# Compiled at: 2016-09-21 16:06:28
from __future__ import unicode_literals
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from nodeconductor.core import models as core_models
from nodeconductor.structure import models as structure_models
from . import managers

class ZabbixService(structure_models.Service):
    projects = models.ManyToManyField(structure_models.Project, related_name=b'zabbix_services', through=b'ZabbixServiceProjectLink')

    @classmethod
    def get_url_name(cls):
        return b'zabbix'


class ZabbixServiceProjectLink(structure_models.ServiceProjectLink):
    service = models.ForeignKey(ZabbixService)

    @classmethod
    def get_url_name(cls):
        return b'zabbix-spl'


@python_2_unicode_compatible
class Host(structure_models.NewResource):
    VISIBLE_NAME_MAX_LENGTH = 64
    MONITORING_ITEMS_CONFIGS = [
     {b'zabbix_item_key': b'application.status', 
        b'monitoring_item_name': b'application_state', 
        b'after_creation_update': True, 
        b'after_creation_update_terminate_values': [
                                                  b'1']}]

    class Statuses(object):
        MONITORED = b'0'
        UNMONITORED = b'1'
        CHOICES = (
         (
          MONITORED, b'monitored'), (UNMONITORED, b'unmonitored'))

    service_project_link = models.ForeignKey(ZabbixServiceProjectLink, related_name=b'hosts', on_delete=models.PROTECT)
    visible_name = models.CharField(_(b'visible name'), max_length=VISIBLE_NAME_MAX_LENGTH)
    interface_parameters = JSONField(blank=True)
    host_group_name = models.CharField(_(b'host group name'), max_length=64, blank=True)
    error = models.CharField(max_length=500, blank=True, help_text=b'Error text if Zabbix agent is unavailable.')
    status = models.CharField(max_length=30, choices=Statuses.CHOICES, default=Statuses.MONITORED)
    templates = models.ManyToManyField(b'Template', related_name=b'hosts')
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    scope = GenericForeignKey(b'content_type', b'object_id')
    objects = managers.HostManager(b'scope')

    def __str__(self):
        return b'%s (%s)' % (self.name, self.visible_name)

    @classmethod
    def get_url_name(cls):
        return b'zabbix-host'

    def clean(self):
        same_service_hosts = Host.objects.filter(service_project_link__service=self.service_project_link.service)
        if same_service_hosts.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError(b'Host with name "%s" already exists at this service. Host name should be unique.' % self.name)
        if same_service_hosts.filter(visible_name=self.visible_name).exclude(pk=self.pk).exists():
            raise ValidationError(b'Host with visible_name "%s" already exists at this service. Host name should be unique.' % self.visible_name)

    @classmethod
    def get_visible_name_from_scope(cls, scope):
        """ Generate visible name based on host scope """
        return (b'%s-%s' % (scope.uuid.hex, scope.name))[:64]


Host._meta.get_field(b'name').max_length = 64

class Template(structure_models.ServiceProperty):
    parents = models.ManyToManyField(b'Template', related_name=b'children')

    @classmethod
    def get_url_name(cls):
        return b'zabbix-template'


@python_2_unicode_compatible
class Item(models.Model):

    class ValueTypes:
        FLOAT = 0
        CHAR = 1
        LOG = 2
        INTEGER = 3
        TEXT = 4
        CHOICES = (
         (
          FLOAT, b'Numeric (float)'),
         (
          CHAR, b'Character'),
         (
          LOG, b'Log'),
         (
          INTEGER, b'Numeric (unsigned)'),
         (
          TEXT, b'Text'))

    key = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    template = models.ForeignKey(Template, related_name=b'items')
    backend_id = models.CharField(max_length=64)
    value_type = models.IntegerField(choices=ValueTypes.CHOICES)
    units = models.CharField(max_length=255)
    history = models.IntegerField()
    delay = models.IntegerField()

    def is_byte(self):
        return self.units == b'B'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Trigger(structure_models.ServiceProperty):
    template = models.ForeignKey(Template, related_name=b'triggers')

    @classmethod
    def get_url_name(cls):
        return b'zabbix-trigger'

    def __str__(self):
        return b'%s-%s | %s' % (self.template.name, self.name, self.settings)


Trigger._meta.get_field(b'name').max_length = 255

class ITService(structure_models.NewResource):

    class Algorithm:
        SKIP = 0
        ANY = 1
        ALL = 2
        CHOICES = (
         (
          SKIP, b'do not calculate'),
         (
          ANY, b'problem, if at least one child has a problem'),
         (
          ALL, b'problem, if all children have problems'))

    service_project_link = models.ForeignKey(ZabbixServiceProjectLink, related_name=b'itservices', on_delete=models.PROTECT)
    host = models.ForeignKey(Host, related_name=b'itservices', blank=True, null=True)
    is_main = models.BooleanField(default=True, help_text=b'Main IT service SLA will be added to hosts resource as monitoring item.')
    algorithm = models.PositiveSmallIntegerField(choices=Algorithm.CHOICES, default=Algorithm.SKIP)
    sort_order = models.PositiveSmallIntegerField(default=1)
    agreed_sla = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    backend_trigger_id = models.CharField(max_length=64, null=True, blank=True)
    trigger = models.ForeignKey(Trigger, null=True, blank=True)

    class Meta(object):
        unique_together = ('host', 'is_main')

    @classmethod
    def get_url_name(cls):
        return b'zabbix-itservice'


@python_2_unicode_compatible
class SlaHistory(models.Model):
    itservice = models.ForeignKey(ITService)
    period = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True)

    class Meta:
        verbose_name = b'SLA history'
        verbose_name_plural = b'SLA histories'
        unique_together = ('itservice', 'period')

    def __str__(self):
        return b'SLA for %s during %s: %s' % (self.itservice, self.period, self.value)


@python_2_unicode_compatible
class SlaHistoryEvent(models.Model):
    EVENTS = (
     ('U', 'DOWN'),
     ('D', 'UP'))
    history = models.ForeignKey(SlaHistory, related_name=b'events')
    timestamp = models.IntegerField()
    state = models.CharField(max_length=1, choices=EVENTS)

    def __str__(self):
        return b'%s - %s' % (self.timestamp, self.state)


class UserGroup(structure_models.ServiceProperty):

    @classmethod
    def get_url_name(cls):
        return b'zabbix-user-group'

    def get_backend(self):
        return self.settings.get_backend()


@python_2_unicode_compatible
class User(core_models.StateMixin, structure_models.ServiceProperty):

    class Types(object):
        DEFAULT = b'1'
        ADMIN = b'2'
        SUPERADMIN = b'3'
        CHOICES = (
         (
          DEFAULT, b'default'), (ADMIN, b'admin'), (SUPERADMIN, b'superadmin'))

    alias = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    type = models.CharField(max_length=30, choices=Types.CHOICES, default=Types.DEFAULT)
    groups = models.ManyToManyField(UserGroup, related_name=b'users')
    password = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30, blank=True)

    class Meta(object):
        unique_together = ('alias', 'settings')

    def __str__(self):
        return b'%s | %s' % (self.alias, self.settings)

    @classmethod
    def get_url_name(cls):
        return b'zabbix-user'

    def get_backend(self):
        return self.settings.get_backend()