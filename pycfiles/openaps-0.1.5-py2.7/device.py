# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/devices/device.py
# Compiled at: 2016-02-06 13:50:19
import json, importlib, site
from openaps.configurable import Configurable

class ExtraConfig(Configurable):
    prefix = 'device'


class Device(Configurable):
    vendor = None
    required = ['name', 'vendor']
    optional = []
    prefix = 'device'
    _uses = []

    def __init__(self, name, vendor):
        self.name = name
        self.vendor = vendor
        self.fields = dict(vendor=vendor.__name__)
        self.extra = ExtraConfig(name)

    def read(self, args=None, config=None):
        if args:
            self.name = args.name
            if getattr(args, 'extra', None):
                self.fields['extra'] = args.extra.format(name=self.name, **self.fields)
                self.vendor.set_config(args, self.extra)
            else:
                self.vendor.set_config(args, self)
        if config:
            self.fields.update(dict(config.items(self.section_name())))
            extra_ini = self.fields.get('extra', None)
            if extra_ini:
                extra = config.Read(name=extra_ini)
                self.extra.fields.update(dict(extra.items(self.section_name())))
        return

    def get(self, k, *args):
        return self.fields.get(k, self.extra.get(k, *args))

    def format_url(self):
        parts = [
         ('{0:s}://{1:s}').format(self.vendor.__name__.split('.').pop(), self.name)]
        parts.append(self.vendor.display_device(self))
        return ('').join(parts)

    def register_uses(self, uses):
        for u in uses.usages:
            if u not in self._uses:
                self._uses.append(u)

    def store(self, config):
        extra_ini = self.fields.get('extra', None)
        if extra_ini:
            extra = config.Read(name=extra_ini)
            self.extra.store(extra)
            extra.save()
        super(Device, self).store(config)
        return

    @classmethod
    def FromImport(klass, candidate, config=None):
        name = candidate.get('name')
        fields = candidate.get(name)
        from openaps import vendors
        vendor = vendors.lookup_dotted(fields['vendor'], config)
        inst = klass(name, vendor)
        inst.fields = fields
        inst.extra.fields = candidate['extra']
        return inst

    @classmethod
    def FromConfig(klass, vendors, config):
        devices = []
        for candidate in config.sections():
            if candidate.startswith(klass.prefix):
                name = json.loads(candidate.split(' ').pop())
                vendor = vendors.lookup(config.get(candidate, 'vendor').split('.').pop(), config)
                device = klass(name, vendor)
                device.read(config=config)
                devices.append(device)

        return devices