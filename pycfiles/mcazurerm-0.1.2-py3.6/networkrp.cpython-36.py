# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\networkrp.py
# Compiled at: 2017-08-11 23:27:04
# Size of source mod 2**32: 15594 bytes
from .restfns import do_delete, do_get, do_put
from .settings import azure_rm_endpoint, NETWORK_API

def create_nic(access_token, subscription_id, resource_group, nic_name, public_ip_id, subnet_id, location):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/networkInterfaces/', nic_name,
     '?api-version=', NETWORK_API])
    body = ''.join(['{ "location": "', location,
     '", "properties": { "ipConfigurations": [{ "name": "ipconfig1", "properties": {',
     '"privateIPAllocationMethod": "Dynamic", "publicIPAddress": {',
     '"id": "', public_ip_id,
     '" }, "subnet": { "id": "', subnet_id,
     '" } } } ] } }'])
    return do_put(endpoint, body, access_token)


def create_nsg(access_token, subscription_id, resource_group, nsg_name, location):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
     '?api-version=', NETWORK_API])
    body = ''.join(['{ "location":"', location, '" }'])
    return do_put(endpoint, body, access_token)


def create_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name, description, protocol='Tcp', source_range='*', destination_range='*', source_prefix='Internet', destination_prefix='*', access='Allow', priority=100, direction='Inbound'):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
     '/securityRules/', nsg_rule_name,
     '?api-version=', NETWORK_API])
    body = ''.join(['{ "properties":{ "description":"', description,
     '", "protocol":"', protocol,
     '", "sourcePortRange":"', source_range,
     '", "destinationPortRange":"', destination_range,
     '", "sourceAddressPrefix": "', source_prefix,
     '", "destinationAddressPrefix": "', destination_prefix,
     '", "sourceAddressPrefix":"*", "destinationAddressPrefix":"*", "access":"', access,
     '", "priority":', str(priority),
     ', "direction":"', direction, '" }}'])
    return do_put(endpoint, body, access_token)


def create_public_ip(access_token, subscription_id, resource_group, public_ip_name, dns_label, location):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/publicIPAddresses/', public_ip_name,
     '?api-version=', NETWORK_API])
    body = ''.join(['{"location": "', location,
     '", "properties": {"publicIPAllocationMethod": "Dynamic", "dnsSettings": {',
     '"domainNameLabel": "', dns_label, '"}}}'])
    return do_put(endpoint, body, access_token)


def create_vnet(access_token, subscription_id, resource_group, name, location, address_prefix='10.0.0.0/16', nsg_id=None):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/virtualNetworks/', name,
     '?api-version=', NETWORK_API])
    if nsg_id is not None:
        nsg_reference = ''.join([', "networkSecurityGroup": { "id": "', nsg_id, '"} '])
    else:
        nsg_reference = ''
    body = ''.join(['{   "location": "', location, '", "properties": ',
     '{"addressSpace": {"addressPrefixes": ["', address_prefix, '"]}, ',
     '"subnets": [ { "name": "subnet", "properties": { "addressPrefix": "', address_prefix,
     '"', nsg_reference, '}}]}}'])
    return do_put(endpoint, body, access_token)


def delete_nic(access_token, subscription_id, resource_group, nic_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/networkInterfaces/', nic_name,
     '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_nsg(access_token, subscription_id, resource_group, nsg_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
     '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/networkSecurityGroups/', nsg_name,
     '/securityRules/', nsg_rule_name,
     '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_public_ip(access_token, subscription_id, resource_group, public_ip_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/publicIPAddresses/', public_ip_name,
     '?api-version=', NETWORK_API])
    return do_delete(endpoint, access_token)


def delete_vnet(access_token, subscription_id, resource_group, name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/virtualNetworks/', name,
     '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


def get_lb_nat_rule(access_token, subscription_id, resource_group, lb_name, rule_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/loadBalancers/', lb_name,
     '/inboundNatRules/', rule_name,
     '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_load_balancer(access_token, subscription_id, resource_group, lb_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/loadBalancers/', lb_name,
     '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_network_usage(access_token, subscription_id, location):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Network/locations/', location,
     '/usages?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_public_ip(access_token, subscription_id, resource_group, ip_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/',
     'publicIPAddresses/', ip_name,
     '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def get_vnet(access_token, subscription_id, resource_group, vnet_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/virtualNetworks/', vnet_name,
     '?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_lb_nat_rules(access_token, subscription_id, resource_group, lb_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/loadBalancers/', lb_name,
     'inboundNatRules?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_load_balancers(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Network/',
     '/loadBalancers?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_load_balancers_rg(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/',
     '/loadBalancers?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_nics(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Network/',
     '/networkInterfaces?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_nics_rg(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/',
     '/networkInterfaces?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_public_ips(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/',
     'publicIPAddresses?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_vnets(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Network/',
     '/virtualNetworks?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def list_vnets_rg(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/',
     '/virtualNetworks?api-version=', NETWORK_API])
    return do_get(endpoint, access_token)


def update_load_balancer(access_token, subscription_id, resource_group, lb_name, body):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Network/loadBalancers/', lb_name,
     '?api-version=', NETWORK_API])
    return do_put(endpoint, body, access_token)