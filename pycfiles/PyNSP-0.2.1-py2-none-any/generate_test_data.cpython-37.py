# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryanh/src/pynsot/tests/generate_test_data.py
# Compiled at: 2019-10-16 18:50:31
# Size of source mod 2**32: 2396 bytes
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
import netaddr
from . import util as fx
from pynsot import client
API_URL = 'http://localhost:8000/api'
EMAIL = 'admin@localhost'
api = client.EmailHeaderClient(API_URL, email=EMAIL)
site_obj = api.sites.post({'name': 'Test Site'})['data']['site']
site = api.sites(site_obj['id'])
resource_names = ('Device', 'Network', 'Interface')
attributes = []
for resource_name in resource_names:
    attrs = fx.enumerate_attributes(resource_name)
    attributes.extend(attrs)

site.attributes.post(attributes)
print('Populated Attributes.')
supernet = netaddr.IPNetwork('10.16.32.0/20')
parents = fx.generate_networks(ipv4list=[str(supernet)])
networks = fx.generate_networks(ipv4list=(str(n) for n in supernet.subnet(24)))
addresses = []
for net in supernet.subnet(24):
    hosts = (str(h) for h in net.iter_hosts())
    addresses.extend(fx.generate_networks(ipv4list=hosts))

for items in (parents, networks, addresses):
    site.networks.post(items)

print('Populated Networks.')
devices = fx.generate_devices(16 * len(networks))
site.devices.post(devices)
print('Populated Devices.')
dev_resp = site.devices.get()
device_ids = [dev['id'] for dev in dev_resp['data']['devices']]
ip_list = [a['cidr'] for a in addresses]
ip_iter = iter(ip_list)
interfaces = []
for device_id in device_ids:
    my_ips = fx.take_n(16, ip_iter)
    my_interfaces = fx.generate_interfaces(device_id, address_pool=my_ips)
    interfaces.extend(my_interfaces)

site.interfaces.post(interfaces)
print('Populated Interfaces.')