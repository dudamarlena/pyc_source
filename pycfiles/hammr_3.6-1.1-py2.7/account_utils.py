# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hammr/utils/account_utils.py
# Compiled at: 2016-12-15 07:34:25
import ntpath
from uforge.objects.uforge import *
from ussclicore.utils import generics_utils, printer
from pyxb.utils import domutils

def openstack(account):
    myCredAccount = CredAccountOpenStack()
    if 'name' not in account:
        printer.out('name for openstack account not found', printer.ERROR)
        return
    if 'glanceUrl' not in account:
        printer.out('glanceUrl for openstack account not found', printer.ERROR)
        return
    if 'keystoneUrl' not in account:
        printer.out('KeystoneUrl for openstack account not found', printer.ERROR)
        return
    if 'keystoneVersion' not in account:
        printer.out('keystoneVersion for openstack account not found', printer.ERROR)
        return
    if 'login' not in account:
        printer.out('login in openstack account not found', printer.ERROR)
        return
    if 'password' not in account:
        printer.out('password in openstack account not found', printer.ERROR)
        return
    myCredAccount.name = account['name']
    myCredAccount.glanceUrl = account['glanceUrl']
    myCredAccount.keystoneUrl = account['keystoneUrl']
    myCredAccount.keystoneVersion = account['keystoneVersion']
    myCredAccount.login = account['login']
    myCredAccount.password = account['password']
    return myCredAccount


def susecloud(account):
    myCredAccount = SuseCloud()
    if 'username' not in account:
        printer.out('username in susecloud account not found', printer.ERROR)
        return
    if 'password' not in account:
        printer.out('catalogName in susecloud account not found', printer.ERROR)
        return
    if 'endpoint' not in account:
        printer.out('endpoint for susecloud account not found', printer.ERROR)
        return
    if 'keystoneEndpoint' not in account:
        printer.out('keystoneEndpoint for susecloud account not found', printer.ERROR)
        return
    if 'name' not in account:
        printer.out('name for susecloud account not found', printer.ERROR)
        return
    myCredAccount.login = account['username']
    myCredAccount.password = account['password']
    myCredAccount.serverUrl = account['endpoint']
    myCredAccount.keystoneUrl = account['keystoneEndpoint']
    myCredAccount.name = account['name']
    return myCredAccount


def cloudstack(account):
    myCredAccount = CredAccountCloudStack()
    if 'name' not in account:
        printer.out('name for cloudstack account not found', printer.ERROR)
        return
    if 'publicApiKey' not in account:
        printer.out('publicApiKey in cloudstack account not found', printer.ERROR)
        return
    if 'secretApiKey' not in account:
        printer.out('secretApiKey in cloudstack account not found', printer.ERROR)
        return
    if 'endpointUrl' not in account:
        printer.out('endpointUrl for cloudstack account not found', printer.ERROR)
        return
    myCredAccount.name = account['name']
    myCredAccount.publicApiKey = account['publicApiKey']
    myCredAccount.secretApiKey = account['secretApiKey']
    myCredAccount.endpointUrl = account['endpointUrl']
    return myCredAccount


def aws(account):
    myCredAccount = CredAccountAws()
    if 'accountNumber' not in account:
        printer.out('accountNumber for ami account not found', printer.ERROR)
        return
    if 'name' not in account:
        printer.out('name for ami account not found', printer.ERROR)
        return
    if 'accessKeyId' not in account:
        printer.out('accessKey in ami account not found', printer.ERROR)
        return
    if 'secretAccessKeyId' not in account:
        printer.out('secretAccessKey in ami account not found', printer.ERROR)
        return
    if 'x509Cert' not in account:
        printer.out('x509Cert in ami account not found', printer.ERROR)
        return
    if 'x509PrivateKey' not in account:
        printer.out('x509PrivateKey in ami account not found', printer.ERROR)
        return
    myCredAccount.accountNumber = account['accountNumber']
    myCredAccount.name = account['name']
    myCredAccount.accessKeyId = account['accessKeyId']
    myCredAccount.secretAccessKeyId = account['secretAccessKeyId']
    myCredAccount.certificates = pyxb.BIND()
    myCredAccount.certificates._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Certificates')
    try:
        cert = certificate()
        with open(account['x509Cert'], 'r') as (myfile):
            cert.content_ = myfile.read()
        cert.type = 'x509'
        cert.type._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'string')
        cert.name = ntpath.basename(account['x509Cert'])
        myCredAccount.certificates.append(cert)
        cert = certificate()
        with open(account['x509PrivateKey'], 'r') as (myfile):
            cert.content_ = myfile.read()
        cert.type = 'ec2PrivateKey'
        cert.type._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'string')
        cert.name = ntpath.basename(account['x509PrivateKey'])
        myCredAccount.certificates.append(cert)
    except IOError as e:
        printer.out('File error: ' + str(e), printer.ERROR)
        return

    return myCredAccount


def azure(account):
    myCredAccount = CredAccountAzure()
    if 'name' not in account:
        printer.out('name for azure account not found', printer.ERROR)
        return
    if 'publishsettings' not in account:
        printer.out('publishsettings in azure account not found', printer.ERROR)
        return
    myCredAccount.name = account['name']
    myCredAccount.publishsettings = account['publishsettings']
    myCredAccount.certificates = pyxb.BIND()
    myCredAccount.certificates._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Certificates')
    try:
        cert = certificate()
        with open(account['publishsettings'], 'r') as (myfile):
            cert.content_ = myfile.read()
        cert.type = 'azurePublishSettings'
        cert.type._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'string')
        cert.name = ntpath.basename(account['publishsettings'])
        myCredAccount.certificates.append(cert)
    except IOError as e:
        printer.out('File error: ' + str(e), printer.ERROR)
        return

    return myCredAccount


def eucalyptus(account):
    myCredAccount = CredAccountEws()
    if 'secretKey' not in account:
        printer.out('secretKey in eucalyptus account not found', printer.ERROR)
        return
    if 'queryId' not in account:
        printer.out('queryId in eucalyptus account not found', printer.ERROR)
        return
    if 'endpoint' not in account:
        printer.out('endpoint in eucalyptus account not found', printer.ERROR)
        return
    if 'cloudCert' not in account:
        printer.out('cloudCert in eucalyptus account not found', printer.ERROR)
        return
    if 'x509Cert' not in account:
        printer.out('x509Cert in eucalyptus account not found', printer.ERROR)
        return
    if 'x509PrivateKey' not in account:
        printer.out('x509PrivateKey in azure eucalyptus not found', printer.ERROR)
        return
    if 'accountNumber' not in account:
        printer.out('accountNumber for eucalyptus account not found', printer.ERROR)
        return
    if 'name' not in account:
        printer.out('name for eucalyptus account not found', printer.ERROR)
        return
    myCredAccount.accountNumber = account['accountNumber']
    myCredAccount.name = account['name']
    myCredAccount.hostname = account['endpoint']
    myCredAccount.secretAccessKeyID = account['secretKey']
    myCredAccount.accessKeyID = account['queryId']
    myCertificates = certificates()
    myCredAccount.certificates = myCertificates
    try:
        myCertificate = certificate()
        with open(account['x509Cert'], 'r') as (myfile):
            myCertificate.certStr = myfile.read()
        myCertificate.type_ = 'x509'
        myCertificate.name = ntpath.basename(account['x509Cert'])
        myCertificates.add_certificate(myCertificate)
        myCertificate = certificate()
        with open(account['x509PrivateKey'], 'r') as (myfile):
            myCertificate.certStr = myfile.read()
        myCertificate.type_ = 'ec2PrivateKey'
        myCertificate.name = ntpath.basename(account['x509PrivateKey'])
        myCertificates.add_certificate(myCertificate)
        myCertificate = certificate()
        with open(account['cloudCert'], 'r') as (myfile):
            myCertificate.certStr = myfile.read()
        myCertificate.type_ = 'eucCert'
        myCertificate.name = ntpath.basename(account['cloudCert'])
        myCertificates.add_certificate(myCertificate)
    except IOError as e:
        printer.out('File error: ' + str(e), printer.ERROR)
        return

    return myCredAccount


def abiquo(account):
    myCredAccount = CredAccountAbiquo()
    if 'password' not in account:
        printer.out('password in abiquo account not found', printer.ERROR)
        return
    if 'username' not in account:
        printer.out('username in abiquo account not found', printer.ERROR)
        return
    if 'hostname' not in account:
        printer.out('hostname for abiquo account not found', printer.ERROR)
        return
    if 'name' not in account:
        printer.out('name for abiquo account not found', printer.ERROR)
        return
    myCredAccount.login = account['username']
    myCredAccount.password = account['password']
    myCredAccount.hostname = account['hostname']
    myCredAccount.name = account['name']
    return myCredAccount


def nimbula(account):
    myCredAccount = CredAccountNimbula()
    if 'password' not in account:
        printer.out('password in nimbula account not found', printer.ERROR)
        return
    if 'username' not in account:
        printer.out('username in nimbula account not found', printer.ERROR)
        return
    if 'endpoint' not in account:
        printer.out('endpoint for nimbula account not found', printer.ERROR)
        return
    if 'name' not in account:
        printer.out('name for nimbula account not found', printer.ERROR)
        return
    myCredAccount.login = account['username']
    myCredAccount.password = account['password']
    myCredAccount.serverUrl = account['endpoint']
    myCredAccount.name = account['name']
    return myCredAccount


def flexiant(account):
    myCredAccount = CredAccountFlexiant()
    if 'apiUsername' not in account:
        printer.out('apiUsername in flexiant account not found', printer.ERROR)
        return
    if 'password' not in account:
        printer.out('password in flexiant account not found', printer.ERROR)
        return
    if 'wsdlUrl' not in account:
        printer.out('wsdlURL for flexiant account not found', printer.ERROR)
        return
    if 'name' not in account:
        printer.out('name for flexiant account not found', printer.ERROR)
        return
    myCredAccount.apiUsername = account['apiUsername']
    myCredAccount.password = account['password']
    myCredAccount.wsdlUrl = account['wsdlUrl']
    myCredAccount.name = account['name']
    try:
        myCredAccount.userUUID = myCredAccount.apiUsername.split('/')[1]
    except:
        printer.out(account['apiUsername'] + ' is not a valid Flexiant username', printer.ERROR)
        return

    return myCredAccount


def vclouddirector(account):
    myCredAccount = CredAccountVCloudDirector()
    if 'name' not in account:
        printer.out('name in vcd account not found', printer.ERROR)
        return
    if 'hostname' not in account:
        printer.out('hostname in vcd account not found', printer.ERROR)
        return
    if 'login' not in account:
        printer.out('login in vcd account not found', printer.ERROR)
        return
    if 'password' not in account:
        printer.out('password in vcd account not found', printer.ERROR)
        return
    if 'organizationName' not in account:
        printer.out('organizationName in vcd account not found', printer.ERROR)
        return
    if 'port' in account:
        port = int(account['port'])
    else:
        port = 443
    myCredAccount.name = account['name']
    myCredAccount.hostname = account['hostname']
    myCredAccount.login = account['login']
    myCredAccount.password = account['password']
    myCredAccount.organizationName = account['organizationName']
    myCredAccount.port = port
    return myCredAccount


def vsphere(account):
    myCredAccount = CredAccountVSphere()
    if 'name' not in account:
        printer.out('name in vcenter account not found', printer.ERROR)
        return
    if 'login' not in account:
        printer.out('login in vcenter account not found', printer.ERROR)
        return
    if 'password' not in account:
        printer.out('password in vcenter account not found', printer.ERROR)
        return
    if 'hostname' not in account:
        printer.out('hostname in vcenter account not found', printer.ERROR)
        return
    if 'proxyHostname' in account:
        myCredAccount.proxyHost = account['proxyHostname']
    if 'proxyPort' in account:
        myCredAccount.proxyPort = account['proxyPort']
    if 'port' in account:
        port = int(account['port'])
    else:
        port = 443
    myCredAccount.name = account['name']
    myCredAccount.login = account['login']
    myCredAccount.password = account['password']
    myCredAccount.hostname = account['hostname']
    myCredAccount.port = port
    return myCredAccount


def gce(account):
    myCredAccount = CredAccountGoogle()
    if 'username' not in account:
        printer.out('username in gce account not found', printer.ERROR)
        return
    if 'certPassword' not in account:
        printer.out('certPassword in gce account not found', printer.ERROR)
        return
    if 'cert' not in account:
        printer.out('cert in gce account not found', printer.ERROR)
        return
    if 'name' not in account:
        printer.out('name for gce account not found', printer.ERROR)
        return
    myCredAccount.type_ = 'google'
    myCredAccount.login = account['username']
    myCredAccount.password = account['certPassword']
    myCredAccount.name = account['name']
    myCertificates = certificates()
    myCredAccount.certificates = myCertificates
    try:
        myCertificate = certificate()
        with open(account['cert'], 'r') as (myfile):
            myCertificate.certStr = myfile.read()
        myCertificate.type_ = 'googleCertificate'
        myCertificate.name = ntpath.basename(account['cert'])
        myCertificates.add_certificate(myCertificate)
    except IOError as e:
        printer.out('File error: ' + str(e), printer.ERROR)
        return

    return myCredAccount


def outscale(account):
    myCredAccount = CredAccountOutscale()
    if 'name' not in account:
        printer.out('name for outscale account not found', printer.ERROR)
        return
    if 'accessKey' not in account:
        printer.out('accessKey in outscale account not found', printer.ERROR)
        return
    if 'secretAccessKey' not in account:
        printer.out('secretAccessKey in outscale account not found', printer.ERROR)
        return
    myCredAccount.secretAccessKeyID = account['secretAccessKey']
    myCredAccount.accessKeyID = account['accessKey']
    myCredAccount.name = account['name']
    return myCredAccount


def get_target_platform_object(api, login, targetPlatformName):
    targetPlatformsUser = api.Users(login).Targetplatforms.Getall()
    if targetPlatformsUser is None or len(targetPlatformsUser.targetPlatforms.targetPlatform) == 0:
        return
    for item in targetPlatformsUser.targetPlatforms.targetPlatform:
        if item.name == targetPlatformName:
            return item

    return


def assign_target_platform_account(credAccount, targetPlatformName):
    myTargetPlatform = targetPlatform()
    myTargetPlatform.name = targetPlatformName
    credAccount.targetPlatform = myTargetPlatform
    return credAccount