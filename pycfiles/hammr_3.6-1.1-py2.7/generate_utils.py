# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hammr/utils/generate_utils.py
# Compiled at: 2016-12-16 11:09:34
from uforge.objects.uforge import *
from ussclicore.utils import printer

def generate_vcd(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        if 'hwType' in builder['hardwareSettings']:
            installProfile.hwType = builder['hardwareSettings']['hwType']
        image.compress = False
        return (image, installProfile)


def generate_nimbula(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        image.compress = True
        return (image, installProfile)


def generate_nimbulaesx(image, builder, installProfile, api, login):
    return generate_nimbula(image, builder, installProfile, api, login)


def generate_nimbulakvm(image, builder, installProfile, api, login):
    return generate_nimbula(image, builder, installProfile, api, login)


def generate_openstackqcow2(image, builder, installProfile, api, login):
    image.compress = False
    return (image, installProfile)


def generate_openstackvhd(image, builder, installProfile, api, login):
    image.compress = False
    return (image, installProfile)


def generate_openstackvmdk(image, builder, installProfile, api, login):
    image.compress = False
    return (image, installProfile)


def generate_openstackvdi(image, builder, installProfile, api, login):
    image.compress = False
    return (image, installProfile)


def generate_susecloud(image, builder, installProfile, api, login):
    image.compress = False
    return (image, installProfile)


def generate_eucalyptus(image, builder, installProfile, api, login):
    if 'account' not in builder:
        printer.out('Account not found in builder', printer.ERROR)
        return (None, None, None)
    else:
        accounts = api.Users(login).Accounts.Getall()
        if accounts is None or not accounts.get_credAccount():
            printer.out('No accounts available', printer.ERROR)
            return (None, None, None)
        for account in accounts.get_credAccount():
            if account.name == builder['account']['name']:
                image.credAccount = account
                break

        if 'disableRootLogin' in builder:
            myrootUser = osUser()
            if builder['disableRootLogin'] == 'true':
                val = True
            elif builder['disableRootLogin'] == 'false':
                val = False
            else:
                printer.out("Unknown value for 'disableRootLogin' in builder [ami]", printer.ERROR)
                return (None, None, None)
            myrootUser.disablePasswordLogin = val
            installProfile.rootUser = myrootUser
        image.compress = False
        return (image, installProfile)


def generate_eucalyptusxen(image, builder, installProfile, api, login):
    return generate_eucalyptus(image, builder, installProfile, api, login)


def generate_eucalyptuskvm(image, builder, installProfile, api, login):
    return generate_eucalyptus(image, builder, installProfile, api, login)


def generate_flexiant(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    image.compress = True
    return (image, installProfile)


def generate_flexiantraw(image, builder, installProfile, api, login):
    return generate_flexiant(image, builder, installProfile, api, login)


def generate_flexiantova(image, builder, installProfile, api, login):
    return generate_flexiant(image, builder, installProfile, api, login)


def generate_flexiantkvm(image, builder, installProfile, api, login):
    return generate_flexiant(image, builder, installProfile, api, login)


def generate_cloudstackqcow2(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        image.compress = True
        return (image, installProfile)


def generate_cloudstackvhd(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        image.compress = True
        return (image, installProfile)


def generate_cloudstackova(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        image.compress = True
        return (image, installProfile)


def generate_abiquo(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        if 'hwType' in builder['hardwareSettings']:
            installProfile.hwType = builder['hardwareSettings']['hwType']
        image.compress = False
        return (image, installProfile)


def generate_azure(image, builder, installProfile, api, login):
    image.compress = False
    return (image, installProfile)


def generate_aws(image, builder, installProfile, api, login):
    image.ebs = True
    if 'diskSize' in builder['installation']:
        image.ebsVolumeSize = builder['installation']['diskSize']
    else:
        printer.out('No disksize set for ebs volume in builder [aws]', printer.ERROR)
        return (None, None)
    if 'disableRootLogin' in builder:
        myrootUser = osUser()
        if builder['disableRootLogin'] == 'true':
            val = True
        elif builder['disableRootLogin'] == 'false':
            val = False
        else:
            printer.out("Unknown value for 'disableRootLogin' in builder [aws]", printer.ERROR)
            return (None, None)
        myrootUser.disablePasswordLogin = val
        installProfile.rootUser = myrootUser
    image.compress = False
    return (image, installProfile)


def generate_gce(image, builder, installProfile, api, login):
    image.compress = True
    return (image, installProfile)


def generate_outscale(image, builder, installProfile, api, login):
    image.compress = False
    return (image, installProfile)


def generate_iso(image, builder, installProfile, api=None, login=None):
    image.compress = True
    return (image, installProfile)


def generate_ovf(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        if 'hwType' in builder['hardwareSettings']:
            installProfile.hwType = builder['hardwareSettings']['hwType']
        image.compress = True
        return (image, installProfile)


def generate_kvm(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        image.compress = True
        return (image, installProfile)


def generate_vbox(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        image.compress = True
        return (image, installProfile)


def generate_raw(image, builder, installProfile, api=None, login=None):
    image.compress = True
    return (image, installProfile)


def generate_hyper_v(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        image.compress = True
        return (image, installProfile)


def generate_qcow2(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        image.compress = True
        return (image, installProfile)


def generate_vhd(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        image.compress = True
        return (image, installProfile)


def generate_xen(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        image.compress = True
        return (image, installProfile)


def generate_vagrant(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        if 'publicBaseBox' in builder and builder['publicBaseBox'] == 'true':
            if 'osUser' not in builder:
                printer.out('osUser not found in vagrant builder', printer.ERROR)
                return (None, None, None)
            if 'sshKey' not in builder:
                printer.out('sshKey not found in vagrant builder', printer.ERROR)
                return (None, None, None)
            sshkey = generics_utils.create_user_ssh_key(self.api, self.login, builder['sshKey'])
            if sshkey == 2:
                return (None, None, None)
            sshKeys = sshKeys()
            sshKeys.add_sshKey(sshkey)
            vagrantUser = osUser()
            vagrantUser.name = builder['osUser']
            vagrantUser.sshKeys = sshKeys
            installProfile.osusers.add_osUser(vagrantUser)
        image.compress = True
        return (image, installProfile)


def generate_xenserver(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        image.compress = True
        return (image, installProfile)


def generate_vmware(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        if 'hwType' in builder['hardwareSettings']:
            installProfile.hwType = builder['hardwareSettings']['hwType']
        image.compress = True
        return (image, installProfile)


def generate_vcenter(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return (None, None, None)
    else:
        if 'hwType' in builder['hardwareSettings']:
            installProfile.hwType = builder['hardwareSettings']['hwType']
        image.compress = False
        return (image, installProfile)


def generate_targz(image, builder, installProfile, api=None, login=None):
    image.compress = True
    return (image, installProfile)


def generate_lxc(image, builder, installProfile, api=None, login=None):
    image.compress = True
    return (image, installProfile)


def get_memory_amount(builder, installProfile, is_mandatory):
    if 'hardwareSettings' in builder and 'memory' in builder['hardwareSettings']:
        installProfile.memorySize = builder['hardwareSettings']['memory']
        return installProfile
    else:
        if is_mandatory:
            printer.out('Error: no hardwareSettings part for builder [' + builder['type'] + ']', printer.ERROR)
            return 2
        return installProfile


def get_target_format_object(api, login, targetFormatName):
    targetFormatsUser = api.Users(login).Targetformats.Getall()
    if targetFormatsUser is None or len(targetFormatsUser.targetFormats.targetFormat) == 0:
        return
    for item in targetFormatsUser.targetFormats.targetFormat:
        if item.name == targetFormatName:
            return item

    return