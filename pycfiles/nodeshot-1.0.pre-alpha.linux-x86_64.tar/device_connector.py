# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/connectors/models/device_connector.py
# Compiled at: 2014-09-02 11:45:33
import inspect
from importlib import import_module
from netengine.exceptions import NetEngineError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django_hstore.fields import DictionaryField
from nodeshot.core.base.models import BaseDate, BaseOrdered
from nodeshot.core.base.managers import HStoreNodeshotManager
from nodeshot.networking.net.models import *
from nodeshot.networking.net.models.choices import DEVICE_STATUS
from nodeshot.core.base.utils import now
from ..settings import settings, NETENGINE_BACKENDS
if 'nodeshot.networking.hardware' in settings.INSTALLED_APPS:
    HARDWARE_INSTALLED = True
    from nodeshot.networking.hardware.models import DeviceModel, Manufacturer, DeviceToModelRel
else:
    HARDWARE_INSTALLED = False

class DeviceConnector(BaseDate, BaseOrdered):
    """
    DeviceConnector Model
    """
    backend = models.CharField(_('backend'), max_length=128, choices=NETENGINE_BACKENDS, help_text=_('select the operating system / protocol to use to retrieve info from device'))
    node = models.ForeignKey('nodes.Node', verbose_name=_('node'))
    host = models.CharField(_('host'), max_length=128)
    config = DictionaryField(_('config'), blank=True, null=True, help_text=_('backend specific parameters, eg: username/password (SSH), community (SNMP)'))
    port = models.IntegerField(_('port'), blank=True, null=True, help_text=_('leave blank to use the default port for the protocol in use'))
    store = models.BooleanField(_('store in DB?'), default=True, help_text=_('is adviced to store read-only credentials only'))
    device = models.ForeignKey(Device, verbose_name=_('device'), blank=True, null=True, help_text=_('leave blank, will be created automatically'))
    objects = HStoreNodeshotManager()
    __netengine = None
    __backend_class = None

    class Meta:
        ordering = [
         'order']
        app_label = 'connectors'
        verbose_name = _('device connector')
        verbose_name_plural = _('device connectors')

    def __unicode__(self):
        if self.host:
            return self.host
        else:
            return _('Unsaved Device Connector')

    def save(self, *args, **kwargs):
        """
        Custom save does the following:
            * strip trailing whitespace from host attribute
            * create device and all other related objects
            * store connection config in DB if store attribute is True
        """
        self.host = self.host.strip()
        if not self.id:
            self.device = self.__create_device()
        if self.store is True:
            super(DeviceConnector, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        """ validation """
        self._validate_backend()
        self._validate_config()
        self._validate_netengine()
        self._validate_duplicates()

    @property
    def REQUIRED_CONFIG_KEYS(self):
        return self._get_netengine_arguments(required=True)

    @property
    def AVAILABLE_CONFIG_KEYS(self):
        return self._get_netengine_arguments()

    @property
    def backend_class(self):
        """
        returns python netengine backend class, importing it if needed
        """
        if not self.backend:
            return None
        else:
            if not self.__backend_class:
                self.__backend_class = self._get_netengine_backend()
            return self.__backend_class

    @property
    def netengine(self):
        """ access netengine instance """
        if not self.backend:
            return None
        else:
            if not self.__netengine:
                NetengineBackend = self.backend_class
                arguments = self._build_netengine_arguments()
                self.__netengine = NetengineBackend(**arguments)
            return self.__netengine

    def _validate_backend(self):
        """ ensure backend string representation is correct """
        try:
            self.backend_class
        except (ImportError, AttributeError) as e:
            raise ValidationError(_('No valid backend found, got the following python exception: "%s"') % e)

    def _validate_config(self):
        """ ensure REQUIRED_CONFIG_KEYS are filled """
        if not self.backend:
            return
        if len(self.REQUIRED_CONFIG_KEYS) < 1:
            return
        self.config = self.config or {}
        required_keys_set = set(self.REQUIRED_CONFIG_KEYS)
        config_keys_set = set(self.config.keys())
        missing_required_keys = required_keys_set - config_keys_set
        unrecognized_keys = config_keys_set - required_keys_set
        if len(missing_required_keys) > 0:
            missing_keys_string = (', ').join(missing_required_keys)
            raise ValidationError(_('Missing required config keys: "%s"') % missing_keys_string)
        elif len(unrecognized_keys) > 0:
            unrecognized_keys_string = (', ').join(unrecognized_keys)
            raise ValidationError(_('Unrecognized config keys: "%s"') % unrecognized_keys_string)

    def _validate_netengine(self):
        """
        call netengine validate() method
        verifies connection parameters are correct
        """
        if self.backend:
            try:
                self.netengine.validate()
            except NetEngineError as e:
                raise ValidationError(e)

    def _validate_duplicates(self):
        """
        Ensure we're not creating a device that already exists
        Runs only when the DeviceConnector object is created, not when is updated
        """
        if not self.id:
            duplicates = []
            self.netengine_dict = self.netengine.to_dict()
            for interface in self.netengine_dict['interfaces']:
                if interface['mac_address'] in duplicates:
                    continue
                if Interface.objects.filter(mac__iexact=interface['mac_address']).count() > 0:
                    duplicates.append(interface['mac_address'])

            if len(duplicates) > 0:
                mac_address_string = (', ').join(duplicates)
                raise ValidationError(_('interfaces with the following mac addresses already exist: %s') % mac_address_string)

    def _get_netengine_arguments(self, required=False):
        """
        returns list of available config params
        returns list of required config params if required is True
        for internal use only
        """
        backend_class = self._get_netengine_backend()
        argspec = inspect.getargspec(backend_class.__init__)
        args = argspec.args
        for argument_name in ['self', 'host', 'port']:
            args.remove(argument_name)

        if required:
            default_values = list(argspec.defaults)
            default_values = default_values[0:-1]
            args = args[0:len(args) - len(default_values)]
        return args

    def _get_netengine_backend(self):
        """
        returns the netengine backend specified in self.backend
        for internal use only
        """
        backend_class_name = self.backend.split('.')[(-1)]
        backend_path = self.backend.lower()
        module = import_module(backend_path)
        BackendClass = getattr(module, backend_class_name)
        return BackendClass

    def _build_netengine_arguments(self):
        """
        returns a python dictionary representing arguments
        that will be passed to a netengine backend
        for internal use only
        """
        arguments = {'host': self.host}
        if self.config is not None:
            for key, value in self.config.iteritems():
                arguments[key] = value

        if self.port:
            arguments['port'] = self.port
        return arguments

    def get_auto_order_queryset(self):
        """
        Overriding a method of BaseOrdered Abstract Model
        """
        return self.__class__.objects.filter(device=self.device)

    def __create_device(self):
        """
        creates device, internal use only
        """
        device_dict = getattr(self, 'netengine_dict', self.netengine.to_dict())
        device = Device()
        device.node_id = self.node_id
        device.name = device_dict['name']
        device.type = device_dict['type']
        device.status = DEVICE_STATUS.get('reachable')
        device.os = device_dict['os']
        device.os_version = device_dict['os_version']
        device.first_seen = now()
        device.last_seen = now()
        device.full_clean()
        device.save()
        for routing_protocol in device_dict['routing_protocols']:
            try:
                rp = RoutingProtocol.objects.filter(name__iexact=routing_protocol['name'], version__iexact=routing_protocol['version'])[0]
            except IndexError:
                rp = RoutingProtocol(name=routing_protocol['name'], version=routing_protocol['version'])
                rp.full_clean()
                rp.save()

            device.routing_protocols.add(rp)

        for interface in device_dict['interfaces']:
            interface_object = False
            vap_object = False
            if interface['type'] == 'ethernet':
                interface_object = Ethernet(**{'device': device, 
                   'name': interface['name'], 
                   'mac': interface['mac_address'], 
                   'mtu': interface['mtu'], 
                   'standard': interface['standard'], 
                   'duplex': interface['duplex'], 
                   'tx_rate': interface['tx_rate'], 
                   'rx_rate': interface['rx_rate']})
            elif interface['type'] == 'wireless':
                interface_object = Wireless(**{'device': device, 
                   'name': interface['name'], 
                   'mac': interface['mac_address'], 
                   'mtu': interface['mtu'], 
                   'mode': interface['mode'], 
                   'standard': interface['standard'], 
                   'channel': interface['channel'], 
                   'channel_width': interface['channel_width'], 
                   'output_power': interface['output_power'], 
                   'dbm': interface['dbm'], 
                   'noise': interface['noise'], 
                   'tx_rate': interface['tx_rate'], 
                   'rx_rate': interface['rx_rate']})
                for vap in interface['vap']:
                    vap_object = Vap(essid=vap['essid'], bssid=vap['bssid'], encryption=vap['encryption'])

            if interface_object:
                interface_object.full_clean()
                interface_object.save()
                if vap_object:
                    vap_object.interface = interface_object
                    vap_object.full_clean()
                    vap_object.save()
                for ip in interface['ip']:
                    ip_object = Ip(**{'interface': interface_object, 
                       'address': ip['address']})
                    ip_object.full_clean()
                    ip_object.save()

        if HARDWARE_INSTALLED:
            try:
                device_model = DeviceModel.objects.filter(name__iexact=device_dict['model'])[0]
            except IndexError as e:
                try:
                    manufacturer = Manufacturer.objects.filter(name__iexact=device_dict['manufacturer'])[0]
                except IndexError as e:
                    manufacturer = Manufacturer(name=device_dict['manufacturer'])
                    manufacturer.full_clean()
                    manufacturer.save()

                device_model = DeviceModel(manufacturer=manufacturer, name=device_dict['model'])
                device_model.ram = device_dict['RAM_total']

            device_model.full_clean()
            device_model.save()
            rel = DeviceToModelRel(device=device, model=device_model)
            rel.full_clean()
            rel.save()
        return device