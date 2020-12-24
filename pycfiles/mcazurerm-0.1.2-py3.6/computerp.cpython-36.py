# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\computerp.py
# Compiled at: 2017-08-12 03:57:37
# Size of source mod 2**32: 26224 bytes
from .restfns import do_delete, do_get, do_get_next, do_patch, do_post, do_put
from .settings import azure_rm_endpoint, COMP_API

def create_vm(access_token, subscription_id, resource_group, vm_name, vm_size, publisher, offer, sku, version, storage_account, os_uri, username, password, nic_id, location):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachines/', vm_name,
     '?api-version=', COMP_API])
    body = ''.join(['{"name": "', vm_name,
     '","location": "', location,
     '","properties": { "hardwareProfile": {',
     '"vmSize": "', vm_size,
     '"},"storageProfile": { "imageReference": { "publisher": "', publisher,
     '","offer": "', offer,
     '","sku": "', sku,
     '","version": "', version,
     '"},"osDisk": { "name": "myosdisk1","vhd": {',
     '"uri": "', os_uri,
     '" }, "caching": "ReadWrite", "createOption": "fromImage" }},"osProfile": {',
     '"computerName": "', vm_name,
     '", "adminUsername": "', username,
     '", "adminPassword": "', password,
     '" }, "networkProfile": {',
     '"networkInterfaces": [{"id": "', nic_id,
     '", "properties": {"primary": true}}]}}}'])
    return do_put(endpoint, body, access_token)


def deallocate_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachines/', vm_name,
     '/deallocate',
     '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


def delete_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachines/', vm_name,
     '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


def delete_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


def delete_vmss_vms(access_token, subscription_id, resource_group, vmss_name, vm_ids):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/delete?api-version=', COMP_API])
    body = '{"instanceIds" : ' + vm_ids + '}'
    return do_post(endpoint, body, access_token)


def get_compute_usage(access_token, subscription_id, location):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.compute/locations/', location,
     '/usages?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachines/', vm_name,
     '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vm_extension(access_token, subscription_id, resource_group, vm_name, extension_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachines/', vm_name,
     '/extensions/', extension_name,
     '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_instance_view(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/instanceView?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_nics(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/networkInterfaces?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_vm(access_token, subscription_id, resource_group, vmss_name, instance_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/virtualMachines/', str(instance_id),
     '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name, instance_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/virtualMachines/', str(instance_id),
     '/instanceView?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def get_vmss_vm_nics(access_token, subscription_id, resource_group, vmss_name, instance_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/virtualMachines/', str(instance_id),
     '/networkInterfaces?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_as(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/availabilitySets',
     '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_as_sub(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/availabilitySets',
     '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vm_images_sub(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/images',
     '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vms(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachines',
     '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_vms_sub(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/virtualMachines',
     '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vmss(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets',
     '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vmss_sub(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/virtualMachineScaleSets',
     '?api-version=', COMP_API])
    return do_get_next(endpoint, access_token)


def list_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/virtualMachines?$expand=instanceView&$select=instanceView&api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_vmss_vms(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/virtualMachines',
     '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def poweroff_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/powerOff?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


def poweroff_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/powerOff?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


def reimage_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/reimage?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


def restart_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachines/',
     vm_name,
     '/restart',
     '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


def restart_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/restart?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


def restart_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/restart?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


def scale_vmss(access_token, subscription_id, resource_group, vmss_name, size, tier, capacity):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '?api-version=', COMP_API])
    body = '{"sku":{ "name":"' + size + '", "tier":"' + tier + '", "capacity":"' + str(capacity) + '"}}'
    return do_patch(endpoint, body, access_token)


def start_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachines/',
     vm_name,
     '/start',
     '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


def start_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/start?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


def start_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/start?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


def stopdealloc_vmss(access_token, subscription_id, resource_group, vmss_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/deallocate?api-version=', COMP_API])
    body = '{"instanceIds" : ["*"]}'
    return do_post(endpoint, body, access_token)


def stopdealloc_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/deallocate?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


def stop_vm(access_token, subscription_id, resource_group, vm_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachines/',
     vm_name,
     '/stop',
     '?api-version=', COMP_API])
    return do_post(endpoint, '', access_token)


def update_vm(access_token, subscription_id, resource_group, vm_name, body):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachines/', vm_name,
     '?api-version=', COMP_API])
    return do_put(endpoint, body, access_token)


def update_vmss(access_token, subscription_id, resource_group, vmss_name, body):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '?api-version=', COMP_API])
    return do_put(endpoint, body, access_token)


def upgrade_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/virtualMachineScaleSets/', vmss_name,
     '/manualupgrade?api-version=', COMP_API])
    body = '{"instanceIds" : ' + instance_ids + '}'
    return do_post(endpoint, body, access_token)


def create_manageddisk(access_token, subscription_id, resource_group, disk_name, location, createOption, disksize_GB):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/disks/', disk_name,
     '?api-version=', COMP_API])
    body = ''.join(['{"location": "', location,
     '", "properties": {"creationData": {',
     '"createOption": "', createOption, '"},',
     '"diskSizeGB": ', disksize_GB, '}}'])
    return do_put(endpoint, body, access_token)


def delete_manageddisk(access_token, subscription_id, resource_group, disk_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/disks/', disk_name,
     '?api-version=', COMP_API])
    return do_delete(endpoint, access_token)


def get_managedisk_rg(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/Microsoft.Compute/disks/',
     '?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_manageddisk_sub(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/disks/',
     '?api-version=', COMP_API])
    return do_get(endpoint, access_token)