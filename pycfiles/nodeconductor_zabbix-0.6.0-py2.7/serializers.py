# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/serializers.py
# Compiled at: 2016-09-21 16:06:28
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from nodeconductor.core.fields import MappedChoiceField, JsonField
from nodeconductor.core.serializers import GenericRelatedField, HyperlinkedRelatedModelSerializer, AugmentedSerializerMixin
from nodeconductor.core.utils import datetime_to_timestamp, pwgen
from nodeconductor.monitoring.utils import get_period
from nodeconductor.structure import serializers as structure_serializers, models as structure_models
from . import models, apps

class ServiceSerializer(structure_serializers.BaseServiceSerializer):
    SERVICE_ACCOUNT_FIELDS = {'backend_url': 'Zabbix API URL (e.g. http://example.com/zabbix/api_jsonrpc.php)', 
       'username': 'Zabbix user username (e.g. admin)', 
       'password': 'Zabbix user password (e.g. zabbix)'}
    SERVICE_ACCOUNT_EXTRA_FIELDS = {'host_group_name': 'Zabbix host group name for registered hosts', 
       'templates_names': 'List of Zabbix hosts templates', 
       'database_parameters': 'Zabbix database parameters', 
       'interface_parameters': 'Default parameters for hosts interface (will be used if interface is not specified)'}

    class Meta(structure_serializers.BaseServiceSerializer.Meta):
        model = models.ZabbixService
        view_name = 'zabbix-detail'
        required_fields = ('backend_url', 'username', 'password')


class ServiceProjectLinkSerializer(structure_serializers.BaseServiceProjectLinkSerializer):

    class Meta(structure_serializers.BaseServiceProjectLinkSerializer.Meta):
        model = models.ZabbixServiceProjectLink
        view_name = 'zabbix-spl-detail'
        extra_kwargs = {'service': {'lookup_field': 'uuid', 'view_name': 'zabbix-detail'}}


class TemplateSerializer(structure_serializers.BasePropertySerializer):
    items = serializers.SerializerMethodField()
    triggers = serializers.SerializerMethodField()

    class Meta(object):
        model = models.Template
        view_name = 'zabbix-template-detail'
        fields = ('url', 'uuid', 'name', 'items', 'triggers', 'settings', 'children')
        extra_kwargs = {'url': {'lookup_field': 'uuid'}, 'children': {'lookup_field': 'uuid', 'view_name': 'zabbix-template-detail'}, 'settings': {'lookup_field': 'uuid'}}

    def get_items(self, template):
        items = template.items.all().values('name', 'key', 'units', 'value_type')
        for item in items:
            item['value_type'] = dict(models.Item.ValueTypes.CHOICES)[item['value_type']]

        return items

    def get_triggers(self, template):
        return template.triggers.all().values_list('name', flat=True)


class NestedTemplateSerializer(TemplateSerializer, HyperlinkedRelatedModelSerializer):

    class Meta(TemplateSerializer.Meta):
        pass


class HostSerializer(structure_serializers.BaseResourceSerializer):
    service = serializers.HyperlinkedRelatedField(source='service_project_link.service', view_name='zabbix-detail', read_only=True, lookup_field='uuid')
    service_project_link = serializers.HyperlinkedRelatedField(view_name='zabbix-spl-detail', queryset=models.ZabbixServiceProjectLink.objects.all())
    visible_name = serializers.CharField(required=False, max_length=models.Host.VISIBLE_NAME_MAX_LENGTH)
    scope = GenericRelatedField(related_models=structure_models.ResourceMixin.get_all_models(), required=False)
    templates = NestedTemplateSerializer(queryset=models.Template.objects.all().prefetch_related('items', 'children'), many=True, required=False)
    status = MappedChoiceField(choices={v:v for _, v in models.Host.Statuses.CHOICES}, choice_mappings={v:k for k, v in models.Host.Statuses.CHOICES}, read_only=True)
    interface_ip = serializers.IPAddressField(allow_blank=True, required=False, write_only=True, help_text='IP of host interface.')
    interface_parameters = JsonField(read_only=True)

    class Meta(structure_serializers.BaseResourceSerializer.Meta):
        model = models.Host
        view_name = 'zabbix-host-detail'
        fields = structure_serializers.BaseResourceSerializer.Meta.fields + ('visible_name',
                                                                             'host_group_name',
                                                                             'scope',
                                                                             'templates',
                                                                             'error',
                                                                             'status',
                                                                             'interface_ip',
                                                                             'interface_parameters')
        read_only_fields = structure_serializers.BaseResourceSerializer.Meta.read_only_fields + ('error',
                                                                                                 'interface_parameters')
        protected_fields = structure_serializers.BaseResourceSerializer.Meta.protected_fields + ('interface_ip',
                                                                                                 'visible_name')

    def get_resource_fields(self):
        return super(HostSerializer, self).get_resource_fields() + ['scope']

    def validate(self, attrs):
        if self.instance is not None:
            for name, value in attrs.items():
                setattr(self.instance, name, value)

            self.instance.clean()
        else:
            if not attrs.get('visible_name'):
                if 'scope' not in attrs:
                    raise serializers.ValidationError('Visible name or scope should be defined.')
                attrs['visible_name'] = models.Host.get_visible_name_from_scope(attrs['scope'])
            spl = attrs['service_project_link']
            if models.Host.objects.filter(service_project_link__service__settings=spl.service.settings, visible_name=attrs['visible_name']).exists():
                raise serializers.ValidationError({'visible_name': 'Visible name should be unique.'})
            instance = models.Host(**{k:v for k, v in attrs.items() if k not in ('templates',
                                                                                 'interface_ip') if k not in ('templates',
                                                                                                              'interface_ip')})
            instance.clean()
        spl = attrs.get('service_project_link') or self.instance.service_project_link
        templates = attrs.get('templates', [])
        for template in templates:
            if template.settings != spl.service.settings:
                raise serializers.ValidationError({'templates': 'Template "%s" and host belong to different service settings.' % template.name})
            for child in template.children.all():
                if child in templates:
                    message = 'Template "%s" is already registered as child of template "%s"' % (
                     child.name, template.name)
                    raise serializers.ValidationError({'templates': message})

        return attrs

    def create(self, validated_data):
        spl = validated_data['service_project_link']
        interface_parameters = spl.service.settings.get_option('interface_parameters')
        scope = validated_data.get('scope')
        interface_ip = validated_data.pop('interface_ip', None) or getattr(scope, 'internal_ips', None)
        if interface_ip:
            interface_parameters['ip'] = interface_ip
        validated_data['interface_parameters'] = interface_parameters
        templates = validated_data.pop('templates', None)
        with transaction.atomic():
            host = super(HostSerializer, self).create(validated_data)
            if templates is None:
                templates = models.Template.objects.filter(settings=host.service_project_link.service.settings, name__in=host.service_project_link.service.settings.get_option('templates_names'))
            for template in templates:
                host.templates.add(template)

        return host

    def update(self, host, validated_data):
        templates = validated_data.pop('templates', None)
        with transaction.atomic():
            host = super(HostSerializer, self).update(host, validated_data)
            if templates is not None:
                host.templates.clear()
                for template in templates:
                    host.templates.add(template)

        return host


class ITServiceSerializer(structure_serializers.BaseResourceSerializer):
    service = serializers.HyperlinkedRelatedField(source='service_project_link.service', view_name='zabbix-detail', read_only=True, lookup_field='uuid')
    service_project_link = serializers.HyperlinkedRelatedField(view_name='zabbix-spl-detail', queryset=models.ZabbixServiceProjectLink.objects.all())
    host = serializers.HyperlinkedRelatedField(view_name='zabbix-host-detail', queryset=models.Host.objects.all(), lookup_field='uuid')
    trigger = serializers.HyperlinkedRelatedField(view_name='zabbix-trigger-detail', queryset=models.Trigger.objects.order_by('name').select_related('settings'), lookup_field='uuid')
    algorithm = MappedChoiceField(choices={v:v for _, v in models.ITService.Algorithm.CHOICES}, choice_mappings={v:k for k, v in models.ITService.Algorithm.CHOICES})
    trigger_name = serializers.ReadOnlyField(source='trigger.name')
    actual_sla = serializers.SerializerMethodField()

    class Meta(structure_serializers.BaseResourceSerializer.Meta):
        model = models.ITService
        view_name = 'zabbix-itservice-detail'
        fields = structure_serializers.BaseResourceSerializer.Meta.fields + ('host',
                                                                             'algorithm',
                                                                             'sort_order',
                                                                             'agreed_sla',
                                                                             'actual_sla',
                                                                             'trigger',
                                                                             'trigger_name',
                                                                             'is_main')

    def get_actual_sla(self, itservice):
        key = 'itservice_sla_map'
        if key not in self.context:
            qs = models.SlaHistory.objects.filter(period=get_period(self.context['request']))
            if isinstance(self.instance, list):
                qs = qs.filter(itservice__in=self.instance)
            else:
                qs = qs.filter(itservice=self.instance)
            self.context[key] = {q.itservice_id:q.value for q in qs}
        return self.context[key].get(itservice.id)

    def validate(self, attrs):
        host = attrs.get('host')
        if host:
            trigger = attrs['trigger']
            if host and not host.templates.filter(id=trigger.template_id).exists():
                raise serializers.ValidationError("Host templates should contain trigger's template")
            if host.service_project_link != attrs['service_project_link']:
                raise serializers.ValidationError('Host and IT service should belong to the same SPL.')
        return attrs


class TriggerSerializer(structure_serializers.BasePropertySerializer):
    template = serializers.HyperlinkedRelatedField(view_name='zabbix-template-detail', read_only=True, lookup_field='uuid')

    class Meta(structure_serializers.BasePropertySerializer.Meta):
        model = models.Trigger
        fields = ('url', 'uuid', 'name', 'template')
        extra_kwargs = {'url': {'lookup_field': 'uuid', 'view_name': 'zabbix-trigger-detail'}}


class SlaHistoryEventSerializer(serializers.Serializer):
    timestamp = serializers.IntegerField()
    state = serializers.CharField()


class ItemsAggregatedValuesSerializer(serializers.Serializer):
    """ Validate input parameters for items_aggregated_values action. """
    start = serializers.IntegerField(default=lambda : datetime_to_timestamp(timezone.now() - timedelta(hours=1)))
    end = serializers.IntegerField(default=lambda : datetime_to_timestamp(timezone.now()))
    method = serializers.ChoiceField(default='MAX', choices=('MIN', 'MAX'))

    def validate(self, data):
        """
        Check that the start is before the end.
        """
        if 'start' in data and 'end' in data and data['start'] >= data['end']:
            raise serializers.ValidationError('End must occur after start')
        return data


class UserGroupSerializer(structure_serializers.BasePropertySerializer):

    class Meta(object):
        model = models.UserGroup
        fields = ('url', 'name', 'settings')
        read_only_fields = ('url', 'backend_id')
        extra_kwargs = {'url': {'lookup_field': 'uuid', 'view_name': 'zabbix-user-group-detail'}, 'settings': {'lookup_field': 'uuid'}}


class NestedUserGroupSerializer(UserGroupSerializer, HyperlinkedRelatedModelSerializer):

    class Meta(UserGroupSerializer.Meta):
        pass


class UserSerializer(AugmentedSerializerMixin, structure_serializers.BasePropertySerializer):
    groups = NestedUserGroupSerializer(queryset=models.UserGroup.objects.all(), many=True)
    state = MappedChoiceField(choices={v:v for _, v in models.User.States.CHOICES}, choice_mappings={v:k for k, v in models.User.States.CHOICES}, read_only=True)
    type = MappedChoiceField(choices={v:v for _, v in models.User.Types.CHOICES}, choice_mappings={v:k for k, v in models.User.Types.CHOICES})
    password = serializers.SerializerMethodField(help_text='Password is visible only after user creation or if user has type "default".')

    class Meta(object):
        model = models.User
        fields = ('url', 'alias', 'name', 'surname', 'type', 'groups', 'backend_id',
                  'settings', 'state', 'phone', 'password')
        read_only_fields = ('url', 'backend_id')
        protected_fields = ('settings', )
        extra_kwargs = {'url': {'lookup_field': 'uuid', 'view_name': 'zabbix-user-detail'}, 'settings': {'lookup_field': 'uuid'}}

    def get_password(self, user):
        show_password = self.context['request'].method == 'POST' and user is None or user.type == models.User.Types.DEFAULT
        if show_password:
            return user.password
        else:
            return

    def get_fields(self):
        fields = super(UserSerializer, self).get_fields()
        fields['settings'].queryset = structure_models.ServiceSettings.objects.filter(type=apps.ZabbixConfig.service_name)
        return fields

    def validate_type(self, value):
        user = self.context['request'].user
        if not user.is_staff and value != models.User.Types.DEFAULT:
            raise serializers.ValidationError('Cannot create not default user.')
        return value

    def validate(self, attrs):
        settings = attrs.get('settings') or self.instance.settings
        groups = attrs.get('groups', [])
        if any([ group.settings != settings for group in groups ]):
            raise serializers.ValidationError('User groups and user should belong to the same service settings')
        return attrs

    def create(self, attrs):
        groups = attrs.pop('groups', [])
        attrs['password'] = pwgen()
        user = super(UserSerializer, self).create(attrs)
        user.groups.add(*groups)
        return user

    def update(self, user, attrs):
        new_groups = set(attrs.pop('groups', []))
        old_groups = set(user.groups.all())
        user = super(UserSerializer, self).update(user, attrs)
        user.groups.remove(*(old_groups - new_groups))
        user.groups.add(*(new_groups - old_groups))
        return user