# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hammr/utils/publish_utils.py
# Compiled at: 2016-12-15 07:34:25
from ussclicore.utils import printer
from uforge.objects.uforge import *

def publish_vcd(pimage, builder):
    if 'orgName' not in builder:
        printer.out('orgName in vcd builder not found', printer.ERROR)
        return
    if 'catalogName' not in builder:
        printer.out('catalogName in vcd builder not found', printer.ERROR)
        return
    if 'imageName' not in builder:
        printer.out('imageName in vcd builder not found', printer.ERROR)
        return
    pimage.credAccount.organizationName = builder['orgName']
    pimage.credAccount.catalogId = builder['catalogName']
    pimage.credAccount.displayName = builder['imageName']
    return pimage


def publish_vcenter(builder):
    pimage = PublishImageVSphere()
    if 'datastore' not in builder:
        printer.out('datastore in vcenter builder not found', printer.ERROR)
        return
    if 'datacenterName' not in builder:
        printer.out('datacenterName in vcenter builder not found', printer.ERROR)
        return
    if 'clusterName' not in builder:
        printer.out('clusterName in vcenter builder not found', printer.ERROR)
        return
    if 'displayName' not in builder:
        printer.out('displayName in vcenter builder not found', printer.ERROR)
        return
    if 'network' not in builder:
        printer.out('network in vcenter builder not found', printer.ERROR)
        return
    pimage.datastore = builder['datastore']
    pimage.datacenterName = builder['datacenterName']
    pimage.clusterName = builder['clusterName']
    pimage.displayName = builder['displayName']
    pimage.network = builder['network']
    return pimage


def publish_cloudstack(pimage, builder):
    if 'imageName' not in builder:
        printer.out('imageName in cloudstack builder not found', printer.ERROR)
        return
    if 'zone' not in builder:
        printer.out('zone in cloudstack builder not found', printer.ERROR)
        return
    if 'publicImage' in builder:
        pimage.credAccount.publicImage = True if builder['publicImage'] == 'true' else False
    if 'featured' in builder:
        pimage.credAccount.featuredEnabled = True if builder['featured'] == 'true' else False
    pimage.credAccount.displayName = builder['imageName']
    pimage.credAccount.zoneName = builder['zone']
    return pimage


def publish_cloudstack_qcow2(pimage, builder):
    return publish_cloudstack(pimage, builder)


def publish_cloudstack_vhd(pimage, builder):
    return publish_cloudstack(pimage, builder)


def publish_cloudstack_ova(pimage, builder):
    return publish_cloudstack(pimage, builder)


def publish_susecloud(pimage, builder):
    if 'imageName' not in builder:
        printer.out('imageName in susecloud builder not found', printer.ERROR)
        return
    if 'tenant' not in builder:
        printer.out('tenant in susecloud builder not found', printer.ERROR)
        return
    if 'description' in builder:
        pimage.credAccount.description = builder['description']
    pimage.credAccount.displayName = builder['imageName']
    pimage.credAccount.tenantName = builder['tenant']
    if 'publicImage' in builder:
        pimage.credAccount.publicImage = True if builder['publicImage'] == 'true' else False
    return pimage


def publish_openstack(builder):
    pimage = PublishImageOpenStack()
    if 'displayName' not in builder:
        printer.out('displayName in openstack builder not found', printer.ERROR)
        return
    if 'tenantName' not in builder:
        printer.out('TenantName in openstack builder not found', printer.ERROR)
        return
    pimage.displayName = builder['displayName']
    pimage.tenantName = builder['tenantName']
    if 'publicImage' in builder:
        pimage.credAccount.publicImage = True if builder['publicImage'] == 'true' else False
    if 'keystoneDomain' in builder:
        pimage.keystoneDomain = builder['keystoneDomain']
        return
    if 'keystoneProject' in builder:
        pimage.keystoneProject = builder['keystoneProject']
        return
    return pimage


def publish_openstackqcow2(builder):
    return publish_openstack(builder)


def publish_openstackvhd(pimage, builder):
    return publish_openstack(pimage, builder)


def publish_openstackvmdk(pimage, builder):
    return publish_openstack(pimage, builder)


def publish_openstackvdi(pimage, builder):
    return publish_openstack(pimage, builder)


def publish_aws(builder):
    pimage = PublishImageAws()
    if 'bucket' not in builder:
        printer.out('bucket in AWS builder not found', printer.ERROR)
        return
    if 'region' not in builder:
        printer.out('region in AMI builder not found', printer.ERROR)
        return
    pimage.bucket = builder['bucket']
    pimage.region = builder['region']
    return pimage


def publish_azure(builder):
    pimage = PublishImageAzure()
    if 'storageAccount' not in builder:
        printer.out('storageAccount in Microsoft Azure not found', printer.ERROR)
        return
    if 'region' not in builder:
        printer.out('region in Microsoft Azure not found', printer.ERROR)
        return
    pimage.storageAccount = builder['storageAccount']
    pimage.region = builder['region']
    return pimage


def publish_flexiant(builder):
    pimage = PublishImageFlexiant()
    if 'diskOffering' not in builder:
        printer.out('diskOffering in flexiant builder not found', printer.ERROR)
        return
    if 'virtualDatacenterName' not in builder:
        printer.out('virtualDatacenterName in flexiant builder not found', printer.ERROR)
        return
    if 'machineImageName' not in builder:
        printer.out('machineImageName in flexiant builder not found', printer.ERROR)
        return
    pimage.diskOffering = builder['diskOffering']
    pimage.virtualDatacenterName = builder['virtualDatacenterName']
    pimage.machineImageName = builder['machineImageName']
    return pimage


def publish_flexiant_kvm(pimage, builder):
    return publish_flexiant(pimage, builder)


def publish_flexiant_ova(pimage, builder):
    return publish_flexiant(pimage, builder)


def publish_flexiantraw(builder):
    return publish_flexiant(builder)


def publish_abiquo(pimage, builder):
    if 'enterprise' not in builder:
        printer.out('enterprise in abiquo builder not found', printer.ERROR)
        return
    if 'datacenter' not in builder:
        printer.out('datacenter in abiquo builder not found', printer.ERROR)
        return
    if 'productName' not in builder:
        printer.out('productName in abiquo builder not found', printer.ERROR)
        return
    if 'category' not in builder:
        printer.out('category in abiquo builder not found', printer.ERROR)
        return
    if 'description' not in builder:
        printer.out('description in abiquo builder not found', printer.ERROR)
        return
    pimage.credAccount.datacenterName = builder['datacenter']
    pimage.credAccount.displayName = builder['productName']
    pimage.credAccount.category = builder['category']
    pimage.credAccount.organizationName = builder['enterprise']
    pimage.credAccount.description = builder['description']
    return pimage


def publish_nimbula(pimage, builder):
    if 'imageListName' not in builder:
        printer.out('imageListName in nimbula builder not found', printer.ERROR)
        return
    if 'imageVersion' not in builder:
        printer.out('imageVersion in nimbula builder not found', printer.ERROR)
        return
    if 'description' not in builder:
        printer.out('description in nimbula builder not found', printer.ERROR)
        return
    pimage.credAccount.imageVersion = builder['imageVersion']
    pimage.credAccount.description = builder['description']
    pimage.credAccount.listName = builder['imageListName']
    return pimage


def publish_nimbula_kvm(pimage, builder):
    return publish_nimbula(pimage, builder)


def publish_nimbula_esx(pimage, builder):
    return publish_nimbula(pimage, builder)


def publish_eucalyptus(pimage, builder):
    if 'imageName' not in builder:
        printer.out('imageName in Eucalyptus builder not found', printer.ERROR)
        return
    if 'description' not in builder:
        printer.out('description in Eucalyptus builder not found', printer.ERROR)
        return
    if 'bucket' not in builder:
        printer.out('bucket in Eucalyptus builder not found', printer.ERROR)
        return
    pimage.credAccount.displayName = builder['imageName']
    pimage.credAccount.bucket = builder['bucket']
    pimage.credAccount.description = builder['description']
    if 'ramdisk' in builder and 'kernelId' in builder:
        pimage.credAccount.ramdiskId = builder['ramdisk']
        pimage.credAccount.kernelId = builder['kernelId']
    return pimage


def publish_eucalyptus_kvm(pimage, builder):
    return publish_eucalyptus(pimage, builder)


def publish_eucalyptus_xen(pimage, builder):
    return publish_eucalyptus(pimage, builder)


def publish_gce(pimage, builder):
    if 'computeZone' not in builder:
        printer.out('computeZone in GCE builder not found', printer.ERROR)
        return
    if 'bucketLocation' not in builder:
        printer.out('bucketLocation in GCE builder not found', printer.ERROR)
        return
    if 'bucket' not in builder:
        printer.out('bucket in GCE builder not found', printer.ERROR)
        return
    if 'projectId' not in builder:
        printer.out('projectId in GCE builder not found', printer.ERROR)
        return
    if 'storageClass' not in builder:
        printer.out('storageClass in GCE builder not found', printer.ERROR)
        return
    if 'diskNamePrefix' not in builder:
        printer.out('diskNamePrefix in AMI builder not found', printer.ERROR)
        return
    if 'description' in builder:
        pimage.credAccount.description = builder['description']
    pimage.credAccount.bucket = builder['bucket']
    pimage.credAccount.tenantName = builder['projectId']
    pimage.credAccount.category = builder['storageClass']
    pimage.credAccount.displayName = builder['diskNamePrefix']
    pimage.credAccount.zoneName = builder['computeZone']
    pimage.publishLocation = builder['bucketLocation']
    return pimage


def publish_outscale(pimage, builder):
    if 'zone' not in builder:
        printer.out('zone in outscale builder not found', printer.ERROR)
        return
    if 'description' not in builder:
        pimage.credAccount.description = builder['description']
    pimage.credAccount.zoneName = builder['zone']
    return pimage