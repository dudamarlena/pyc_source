# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_facter.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.facter import Facter
from insights.tests import context_wrap
FACTS = ('\nCOMMAND> facter\n\narchitecture => x86_64\naugeasversion => 1.1.0\nbios_release_date => 04/14/2014\nbios_vendor => Phoenix Technologies LTD\nbios_version => 6.00\nblockdevice_fd0_size => 4096\nblockdevice_sda_model => Virtual disk\nblockdevice_sda_size => 53687091200\nblockdevice_sda_vendor => VMware\nblockdevice_sdb_model => Virtual disk\nblockdevice_sdb_size => 214748364800\nblockdevice_sdb_vendor => VMware\nblockdevice_sdc_model => Virtual disk\nblockdevice_sdc_size => 32212254720\nblockdevice_sdc_vendor => VMware\nblockdevice_sr0_model => VMware IDE CDR10\nblockdevice_sr0_size => 64784384\nblockdevice_sr0_vendor => NECVMWar\nblockdevices => fd0,sda,sdb,sdc,sr0\nboardmanufacturer => Intel Corporation\nboardproductname => 440BX Desktop Reference Platform\nboardserialnumber => None\ndomain => example.com\nfacterversion => 1.7.6\nfilesystems => btrfs,ext2,ext3,ext4,msdos,vfat,xfs\nfqdn => plin-w1rhns01.example.com\nhardwareisa => x86_64\nhardwaremodel => x86_64\nhostname => plin-w1rhns01\nid => root\ninterfaces => ens192,lo\nipaddress => 172.23.27.50\nipaddress_ens192 => 172.23.27.50\nipaddress_lo => 127.0.0.1\nis_virtual => true\nkernel => Linux\nkernelmajversion => 3.10\nkernelrelease => 3.10.0-229.7.2.el7.x86_64\nkernelversion => 3.10.0\nmacaddress => 00:50:56:b0:38:95\nmacaddress_ens192 => 00:50:56:b0:38:95\nmanufacturer => VMware, Inc.\nmemoryfree => 5.30 GB\nmemoryfree_mb => 5423.56\nmemorysize => 11.58 GB\nmemorysize_mb => 11855.77\nmemorytotal => 11.58 GB\nnetmask => 255.255.255.240\nnetmask_ens192 => 255.255.255.240\nnetmask_lo => 255.0.0.0\nnetwork_ens192 => 172.23.27.48\nnetwork_lo => 127.0.0.0\noperatingsystem => RedHat\noperatingsystemmajrelease => 7\noperatingsystemrelease => 7.1\nosfamily => RedHat\npath => /usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin\nphysicalprocessorcount => 1\nprocessor0 => Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz\nprocessor1 => Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz\nprocessor2 => Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz\nprocessor3 => Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz\nprocessorcount => 4\nproductname => VMware Virtual Platform\nps => ps -ef\npuppetversion => 3.6.2\nrubysitedir => /usr/local/share/ruby/site_ruby/\nrubyversion => 2.0.0\nselinux => false\nserialnumber => VMware-42 30 64 8e 9c 94 23 5f-10 74 90 7c 43 38 71 72\nsshecdsakey => thisisakey\nsshfp_ecdsa => SSHFP 3 1 fingerprint1\nSSHFP 3 2 fingerprint2\nsshfp_rsa => SSHFP 1 1 fingerprint3\nSSHFP 1 2 fingerprint4\nsshrsakey => thersapublickey\nswapfree => 0.00 MB\nswapfree_mb => 0.00\nswapsize => 0.00 MB\nswapsize_mb => 0.00\ntimezone => CDT\ntype => Other\nuniqueid => 17ac321b\nsystem_uptime => {"seconds"=>3663199, "hours"=>1017, "days"=>42, "uptime"=>"42 days"}\nuptime => 42 days\nuptime_days => 42\nuptime_hours => 1017\nuptime_seconds => 3663199\nuuid => 4230648E-9C94-235F-1074-907C43387172\nvirtual => vmware\n').strip()

def test_facter():
    fc = Facter(context_wrap(FACTS))
    assert fc.uptime_days == '42'
    assert fc.fqdn == 'plin-w1rhns01.example.com'
    assert fc.uuid == '4230648E-9C94-235F-1074-907C43387172'
    assert hasattr(fc, 'no_test') is False
    assert hasattr(fc, 'swapfree') is True
    assert fc.get('uptime') == '42 days'
    assert fc.get('dummy') is None
    return