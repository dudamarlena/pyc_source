# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_installed_rpms.py
# Compiled at: 2019-11-14 13:57:46
import pytest
from insights.parsers.installed_rpms import InstalledRpms, InstalledRpm, pad_version
from insights.tests import context_wrap
RPMS_PACKAGE = ('\nopenjpeg-libs-1.3-9.el6_3.x86_64\nopenldap-2.4.23-31.el6.x86_64\nopenobex-1.4-7.el6.x86_64\nopenssh-server-5.3p1-104.el6.x86_64\nopenssh-askpass-5.3p1-84.1.el6.x86_64\nopenssl-1.0.0-27.el6.x86_64\n').strip()
RPMS_PACKAGE_WITH_GARBAGE = ('\nopenjpeg-libs-1.3-9.el6_3.x86_64\nopenldap-2.4.23-31.el6.x86_64\nopenobex-1.4-7.el6.x86_64\nopenssh-server#$%^5.3p1$%^104.el6.x86_64\nopenssh-askpass-5.3p1-84.1.el6.x86_64\nopenssl-1.0.0-27.el6.x86_64\n').strip()
RPMS_LINE = ('\nCOMMAND> rpm xxxxx\nBESAgent-9.2.5.130-rhe5.x86_64                              Wed Jan 27 09:18:52 2016\t1453904332\tIBM Corp.\trhel5x64bs\t(none)\t(none)\nConsoleKit-0.4.1-3.el6.x86_64                               Wed Sep 17 11:34:25 2014\nkernel-2.6.32-573.el6.x86_64                                Wed May 18 14:17:17 2016\nzisofs-tools-1.0.6-3.2.2.x86_64                             Wed May 18 14:15:26 2016\ntftp-server-5.2-12.el7.x86_64\nyum-3.2.29-69.el6.noarch                                    Wed May 18 14:16:21 2016\t1410968065\tRed Hat, Inc.\ths20-bc2-4.build.redhat.com\t8902150305004c6955c9199e2f91fd431d51010853c80ffb05f6916ea5f2980314b1766656aeb544777db76296173ffc16708d725e7b691e4ad9aef3dbe9c544a5d33264c9b4bf36464bec32ae6960be72c0175d710333f7aa52e24fc774d1c8809c2730d381593214b51abf7a455354e56993eac5a536fbdda1f1530ca8a9b5816bb47f0a5cf60081462aef48c8a68c761cd15d01f53eabc10aa4b90f47fac18ee8094d1613195277120a85efc6a0c9e2dbbb619f520c59ee74a7be84b2ae4177ece2e10f18617bfb926eade8537993f16fbd28e4a95e3bf7acf381b847171e0a03c241c5c20b5cfb021f69903b9afa4ce40d2bf17b5b439b1014bb974becca815b268f209833dce8cdd4052020aee680a56d1eff7214fb36bbcd35a0674374df2a64e3c3f13c10f23c7d33d035f3a7c7525e7037868ef86681ce0f41d9376f0ac4b1176a939752e1b63cb5a49e9004ee6b9d797ee16dd7b5b97496b3c1f5c0fd792e28117887af78026eb8422077e27d32fb0dba7025d870e8db7fa4e6abfb221abe9b1997ab808c07220329e0ec7863dfcf0c1c1931c4f0061015b902a6d65e59ca8a9252dcf4eeeac3cdfbbf4664a356d6f05e031bcd9cc3223d10425a03bacbe2f49d3f54bd2288f64c9812a5c255e6c11a4dd46255c3a9f2bed34b61bbd849bcf1f007d5f4e3f6e60064b372e0ac6ab301163393adb10d9aa47fe6be211b3576ff37da7e12e2285358267495ac48a437d4eefb3213\tRSA/8, Mon Aug 16 11:14:17 2010, Key ID 199e2f91fd431d51\n').strip()
RPM_MANIFEST = '\ngpg-pubkey-0608b895-4bd22942                  Sat Aug 29 19:29:30 2015\ncapacity-osms-0.0.1-1.noarch                  Sat Aug 29 19:17:55 2015\nHPOvGlanc-11.14.014-1.x86_64                  Sat Aug 29 19:17:01 2015\nHPOvPerfAgt-11.14.014-1.x86_64                Sat Aug 29 19:16:39 2015\nHPOvPerfMI-11.14.014-1.x86_64                 Sat Aug 29 19:16:32 2015\nHPOvAgtLc-11.14.014-1.x86_64                  Sat Aug 29 19:16:02 2015\nvmware-tools-8.3.19-1310361.el6.x86_64        Sat Aug 29 19:10:11 2015\nvmware-open-vm-tools-xorg-utilities-8.3.19-1310361.el6.x86_64 Sat Aug 29 19:10:11 2015\nvmware-open-vm-tools-8.3.19-1310361.el6.x86_64 Sat Aug 29 19:10:11 2015\nvmware-tools-nox-8.3.19-1310361.el6.x86_64    Sat Aug 29 19:10:10 2015\nvmware-tools-common-8.3.19-1310361.el6.x86_64 Sat Aug 29 19:10:10 2015\nvmware-open-vm-tools-xorg-drv-display-11.0.1.0-0.1310361.el6.x86_64 Sat Aug 29 19:10:10 2015\nvmware-open-vm-tools-nox-8.3.19-1310361.el6.x86_64 Sat Aug 29 19:10:10 2015\nvmware-open-vm-tools-common-8.3.19-1310361.el6.x86_64 Sat Aug 29 19:10:09 2015\nvmware-open-vm-tools-xorg-drv-mouse-12.6.7.0-0.1310361.el6.x86_64 Sat Aug 29 19:10:08 2015\n'
RPMS_JSON = ('\n{"name": "util-linux","version": "2.23.2","epoch": "(none)","release": "26.el7_2.2","arch": "x86_64","installtime": "Fri 24 Jun 2016 04:17:58 PM EDT","buildtime": "1458159298","rsaheader": "RSA/SHA256, Sun 20 Mar 2016 10:00:45 PM EDT, Key ID 199e2f91fd431d51","dsaheader": "(none)","srpm": "util-linux-2.23.2-26.el7_2.2.src.rpm"}\n{"name": "libestr","version": "0.1.9","epoch": "(none)","release": "2.el7","arch": "x86_64","installtime": "Fri 06 May 2016 03:53:26 PM EDT","buildtime": "1390734694","rsaheader": "RSA/SHA256, Tue 01 Apr 2014 04:49:20 PM EDT, Key ID 199e2f91fd431d51","dsaheader": "(none)","srpm": "libestr-0.1.9-2.el7.src.rpm"}\n{"name": "log4j","version": "1.2.17","epoch": "0","release": "15.el7","arch": "noarch","installtime": "Thu 02 Jun 2016 05:10:29 PM EDT","buildtime": "1388247429","rsaheader": "RSA/SHA256, Wed 02 Apr 2014 11:25:59 AM EDT, Key ID 199e2f91fd431d51","dsaheader": "(none)","srpm": "log4j-1.2.17-15.el7.src.rpm"}\n{"name": "kbd-misc","version": "1.15.5","epoch": "(none)","release": "11.el7","arch": "noarch","installtime": "Fri 06 May 2016 03:52:06 PM EDT","buildtime": "1412004323","rsaheader": "RSA/SHA256, Tue 16 Dec 2014 10:02:15 AM EST, Key ID 199e2f91fd431d51","dsaheader": "(none)","srpm": "kbd-1.15.5-11.el7.src.rpm"}\n{"name": "grub2-tools","version": "2.02","epoch": "1","release": "0.34.el7_2","arch": "x86_64","installtime": "Fri 24 Jun 2016 04:18:01 PM EDT","buildtime": "1450199819","rsaheader": "RSA/SHA256, Wed 23 Dec 2015 04:22:27 AM EST, Key ID 199e2f91fd431d51","dsaheader": "(none)","srpm": "grub2-2.02-0.34.el7_2.src.rpm"}\n{"name": "kbd-legacy","version": "1.15.5","epoch": "(none)","release": "11.el7","arch": "noarch","installtime": "Fri 06 May 2016 03:53:32 PM EDT","buildtime": "1412004323","rsaheader": "RSA/SHA256, Tue 16 Dec 2014 10:02:14 AM EST, Key ID 199e2f91fd431d51","dsaheader": "(none)","srpm": "kbd-1.15.5-11.el7.src.rpm"}\n{"name": "jboss-servlet-3.0-api","version": "1.0.1","epoch": "(none)","release": "9.el7","arch": "noarch","installtime": "Thu 02 Jun 2016 05:10:30 PM EDT","buildtime": "1388211302","rsaheader": "RSA/SHA256, Tue 01 Apr 2014 02:51:30 PM EDT, Key ID 199e2f91fd431d51","dsaheader": "(none)","srpm": "jboss-servlet-3.0-api-1.0.1-9.el7.src.rpm"}\n{"name": "bash","version": "4.2.46","epoch": "(none)","release": "19.el7","arch": "x86_64","installtime": "Fri 06 May 2016 03:52:13 PM EDT","buildtime": "1436354006","rsaheader": "RSA/SHA256, Wed 07 Oct 2015 01:14:10 PM EDT, Key ID 199e2f91fd431d51","dsaheader": "(none)","srpm": "bash-4.2.46-19.el7.src.rpm"}\n{"name": "ca-certificates","version": "2015.2.6","epoch": "(none)","release": "70.1.el7_2","arch": "noarch","installtime": "Fri 24 Jun 2016 04:18:04 PM EDT","buildtime": "1453976868","rsaheader": "RSA/SHA256, Tue 02 Feb 2016 09:45:04 AM EST, Key ID 199e2f91fd431d51","dsaheader": "(none)","srpm": "ca-certificates-2015.2.6-70.1.el7_2.src.rpm"}\n{"name": "jline","version": "1.0","epoch": "(none)","release": "8.el7","arch": "noarch","installtime": "Thu 02 Jun 2016 05:10:32 PM EDT","buildtime": "1388212830","rsaheader": "RSA/SHA256, Tue 01 Apr 2014 02:54:16 PM EDT, Key ID 199e2f91fd431d51","dsaheader": "(none)","srpm": "jline-1.0-8.el7.src.rpm"}\n{"name": "libteam","version": "1.17","epoch": "(none)","release": "6.el7_2","arch": "x86_64","installtime": "Fri 24 Jun 2016 04:18:17 PM EDT","buildtime": "1454604485","rsaheader": "RSA/SHA256, Wed 17 Feb 2016 02:25:16 AM EST, Key ID 199e2f91fd431d51","dsaheader": "(none)","srpm": "libteam-1.17-6.el7_2.src.rpm"}\n').strip()
RPMS_MULTIPLE = '\nyum-3.4.3-132.el7.noarch\nyum-3.4.2-132.el7.noarch\n'
RPMS_MULTIPLE_KERNEL = '\nkernel-3.10.0-327.el7.x86_64\nkernel-3.10.0-327.36.1.el7.x86_64\nkernel-devel-3.10.0-327.el7.x86_64\nkernel-devel-3.10.0-327.36.1.el7.x86_64\n'
ERROR_DB = ('\nerror: rpmdbNextIterator: skipping h#     753 Header V3 DSA signature: BAD, key ID db42a6\nyum-security-1.1.16-21.el5.noarch\n').strip()
ORACLEASM_RPMS = ('\noracleasm-2.6.18-164.el5-2.0.5-1.el5.x86_64\noracleasmlib-2.0.4-1.el5.x86_64\noracleasm-support-2.1.3-1.el5.x86_64\noracle-validated-1.0.0-18.el5.x86_64\n').strip()
NON_ORACLEASM_RPMS = ('\noracleasmlib-2.0.4-1.el5.x86_64\noracleasm-support-2.1.3-1.el5.x86_64\noracle-validated-1.0.0-18.el5.x86_64\n').strip()
RHV_HYPERVISOR_RPMS = ('\nvdsm-jsonrpc-4.18.15.3-1.el7ev.noarch\nvdsm-hook-vmfex-dev-4.18.15.3-1.el7ev.noarch\nvdsm-cli-4.18.15.3-1.el7ev.noarch\nvdsm-4.18.15.3-1.el7ev.x86_64\n').strip()
RPMS_PACKAGE_WITH_UNICODE = ('\nopenjpeg-libs-1.3-9.el6_3.x86_64\nopenldap-2.4.23-31.el6.x86_64\nopenobexƎ-1.4-7.el6.x86_64\nopenssh-server-5.3p1-104.el6.x86_64\nopenssh-askpass-5.3p1-84.1.el6.x86_64\nopenssl-1.0.0-27.el6.x86_64\n').strip()
RPMS_GPG_PUBKEY = ('\n{"name":"gpg-pubkey","epoch":"(none)","version":"2fa658e0","release":"45700c69","arch":"(none)","installtime":"Thu Apr 25 08:21:00 2019","buildtime":"1556194860","vendor":"(none)","buildhost":"localhost","sigpgp":"(none)"}\n').strip()
RPMS_VMAAS = ('\ncompat-libstdc++-296-2.96-138\ncompat-libstdc++-296-2.96-144.el6\ncompat-libstdc++-33-3.2.3-47.3\ncompat-libstdc++-33-3.2.3-61\ncompat-libstdc++-33-3.2.3-69.el6\ncompat-libstdc++-33-3.2.3-72.el7\nflash-plugin-11.2.202.635-release\nflash-plugin-31.0.0.148-1.el6_10\nflash-plugin-32.0.0.156-release\nflash-plugin-32.0.0.171-1.el6_10\nglibc-2.12-1.149.el6_6.5\nglibc-2.5-81\ninfinipath-psm-3.0.1-115.1015_open.2.el6\ninfinipath-psm-3.3-1.7.git05f6f14_open.el6\ninfinipath-psm-3.3-19_g67c0807_open.el6\nkmod-fnic-1.5.0.45-1.el6\nkmod-fnic-1.6.0.12b-rhel6u6.el6\nkrb5-libs-1.10.3-42z1.el6_7\nkrb5-libs-1.10.3-65.el6\nlibaio-devel-0.3.106-5\nlibaio-devel-0.3.107-10.el6\nmdadm-4.0-13.el7\nmdadm-4.1-rc1_2.el7\nnagios-plugins-disk-2.2.1-16.20180725git3429dad.el7\nnagios-plugins-disk-2.2.1-9git5c7eb5b9.el7\nTaniumClient-6.0.314.1321-1\nTaniumClient-6.0.314.1579_1.rhe7-1\nTaniumClient-7.2.314.2962_1.oel6-1\nTaniumClient-7.2.314.2962-1.rhe6\nTaniumClient-7.2.314.3211-1.rhe7\nxymon-4.3.11-11.1\nxymon-4.3.25-1.el6\nxz-5.1.2-12alpha.el7\nxz-5.2.2-1.el7\nxz-libs-5.1.2-12alpha.el7\nxz-libs-5.2.2-1.el7\n').strip()

def test_from_package():
    rpms = InstalledRpms(context_wrap(RPMS_PACKAGE))
    assert not rpms.is_hypervisor
    pkg_rpm = rpms.packages['openssh-server'][0]
    rpm = InstalledRpm.from_package(pkg_rpm.package)
    assert rpm.package == 'openssh-server-5.3p1-104.el6'
    assert pkg_rpm.package == 'openssh-server-5.3p1-104.el6'
    assert rpm == pkg_rpm
    assert rpm.epoch == '0'
    rpm = InstalledRpm.from_package('bash-1:4.1.2-12.el7.x86_64')
    assert rpm.epoch == '1'


def test_from_line():
    rpms = InstalledRpms(context_wrap(RPMS_LINE))
    assert rpms.get_max('ConsoleKit').arch == 'x86_64'
    assert rpms.get_max('kernel').version == '2.6.32'
    assert rpms.get_max('yum').release == '69.el6'
    assert rpms.get_max('tftp-server').version == '5.2'
    assert rpms.get_max('yum').package == 'yum-3.2.29-69.el6'
    assert rpms.get_max('tftp-server').redhat_signed is None
    assert rpms.get_max('yum').redhat_signed
    assert rpms.corrupt is False
    return


def test_from_json():
    rpms = InstalledRpms(context_wrap(RPMS_JSON))
    assert isinstance(rpms.get_max('log4j').source, InstalledRpm)
    assert len(rpms.packages) == len(RPMS_JSON.splitlines())
    assert rpms.get_max('log4j').source.name == 'log4j'
    assert rpms.get_max('util-linux').epoch == '0'
    assert rpms.get_max('jboss-servlet-3.0-api').redhat_signed


def test_garbage():
    rpms = InstalledRpms(context_wrap(RPMS_PACKAGE_WITH_GARBAGE))
    assert 'openssh-server' not in rpms


def test_corrupt_db():
    rpms = InstalledRpms(context_wrap(ERROR_DB))
    assert 'yum-security' in rpms.packages
    assert rpms.corrupt is True


def test_rpm_manifest():
    rpms = InstalledRpms(context_wrap(RPM_MANIFEST))
    assert 'gpg-pubkey' in rpms
    assert rpms.packages['vmware-tools'][0].package == 'vmware-tools-8.3.19-1310361.el6'
    assert rpms.packages['vmware-tools'][0].installtime == 'Sat Aug 29 19:10:11 2015'


def test_package_property_aliases():
    rpms = InstalledRpms(context_wrap(RPMS_JSON))
    rpm = rpms.get_max('grub2-tools')
    assert rpm.package == 'grub2-tools-2.02-0.34.el7_2'
    assert rpm.nvr == 'grub2-tools-2.02-0.34.el7_2'
    assert rpm.nvra == 'grub2-tools-2.02-0.34.el7_2.x86_64'


def test_max_min():
    rpms = InstalledRpms(context_wrap(RPMS_MULTIPLE))
    assert rpms.get_min('yum').package == 'yum-3.4.2-132.el7'
    assert rpms.get_max('yum').package == 'yum-3.4.3-132.el7'


def test_max_min_not_found():
    rpms = InstalledRpms(context_wrap(RPMS_MULTIPLE_KERNEL))
    assert rpms.get_min('abc') is None
    assert rpms.get_max('abc') is None
    return


def test_max_min_kernel():
    rpms = InstalledRpms(context_wrap(RPMS_MULTIPLE_KERNEL))
    assert rpms.get_min('kernel').package == 'kernel-3.10.0-327.el7'
    assert rpms.get_max('kernel').package == 'kernel-3.10.0-327.36.1.el7'
    assert rpms.get_min('kernel-devel').package == 'kernel-devel-3.10.0-327.el7'
    assert rpms.get_max('kernel-devel').package == 'kernel-devel-3.10.0-327.36.1.el7'


def test_release_compare():
    rpm1 = InstalledRpm.from_package('kernel-rt-debug-3.10.0-327.rt56.204.el7_2.1')
    rpm2 = InstalledRpm.from_package('kernel-rt-debug-3.10.0-327.rt56.204.el7_2.2')
    rpm3 = InstalledRpm.from_package('kernel-3.10.0-327.10.1.el7')
    rpm4 = InstalledRpm.from_package('kernel-3.10.0-327.el7')
    rpm5 = InstalledRpm.from_package('kernel-3.10.0-327.el7_1')
    rpm6 = InstalledRpm.from_package('kernel-3.10.0-327')
    rpm7 = InstalledRpm.from_package('kernel-3.10.0-327.1')
    rpm8 = InstalledRpm.from_package('kernel-3.10.0-327.x86_64')
    rpm9 = InstalledRpm.from_package('kernel-3.10.0-327.1.x86_64')
    with pytest.raises(ValueError) as (ve):
        rpm1 > rpm7
    assert 'differing names' in str(ve)
    with pytest.raises(ValueError) as (ve):
        rpm1 <= rpm7
    assert 'differing names' in str(ve)
    with pytest.raises(ValueError) as (ve):
        rpm1 != rpm7
    assert 'differing names' in str(ve)
    assert rpm1 < rpm2
    assert rpm1 != rpm2
    assert rpm3 > rpm4
    assert rpm5 > rpm4
    assert rpm5 >= rpm4
    assert not rpm5 <= rpm4
    assert rpm6 < rpm7
    assert rpm8 < rpm9
    assert rpm6 < rpm9
    assert rpm6 <= rpm9
    assert rpm6 == rpm8
    assert rpm6 <= rpm8
    assert rpm6 >= rpm8
    assert not rpm7 != rpm9


def test_version_compare():
    d1 = {'name': 'bash', 
       'version': '4.2.46', 
       'epoch': '0', 
       'release': '19.el7', 
       'arch': 'x86_64', 
       'installtime': 'Fri 06 May 2016 03:52:13 PM EDT', 
       'buildtime': '1436354006', 
       'rsaheader': 'RSA/SHA256,Wed 07 Oct 2015 01:14:10 PM EDT,Key ID 199e2f91fd431d51', 
       'dsaheader': '(none)', 
       'srpm': 'bash-4.2.46-19.el7.src.rpm'}
    d2 = d1.copy()
    d2['epoch'] = '1'
    rpm1, rpm2 = InstalledRpm(d1), InstalledRpm(d2)
    assert rpm2 > rpm1
    assert rpm2.source > rpm1.source
    assert rpm1 == rpm1
    assert not rpm1 < rpm1
    assert rpm2 != rpm1
    assert rpm2 >= rpm1
    assert rpm1 <= rpm2
    assert not rpm1 < None
    assert not rpm1 <= None
    assert not rpm1 > None
    assert not rpm1 >= None
    assert not rpm1.__eq__(None)
    assert not [
     rpm1, rpm2] > rpm2
    assert not rpm1 > ''
    assert not rpm1 > 4
    assert not rpm1 > {}
    assert not rpm1 > set()
    assert not rpm1 > []
    return


def test_formatting():
    rpm = InstalledRpm.from_package('kernel-3.10.0-327.el7.x86_64')
    assert str(rpm) == '0:kernel-3.10.0-327.el7'
    assert repr(rpm) == '0:kernel-3.10.0-327.el7'


def test_exceptions():
    rpm1 = InstalledRpm.from_package('kernel-3.10.0-327.el7.x86_64')
    rpm2 = InstalledRpm.from_package('plevel-3.10.0-327.el7.x86_64')
    with pytest.raises(ValueError):
        assert rpm1 > rpm2


def test_different_arch_sep():
    rpm1 = InstalledRpm.from_package('yum-3.4.3-132.el7.noarch')
    rpm2 = InstalledRpm.from_package('yum-3.4.3-132.el7-noarch')
    assert rpm1 == rpm2
    assert rpm1.arch == rpm2.arch
    assert rpm1['arch'] == rpm2.arch


def test_no_suffixes():
    rpms = InstalledRpms(context_wrap(RPMS_PACKAGE))
    assert 'openssh-askpass' in rpms
    assert 'askpass' not in rpms
    assert 'openobex' in rpms
    assert 'penobex' not in rpms


def test_oracleasmrpms():
    ora_rpms = InstalledRpms(context_wrap(ORACLEASM_RPMS))
    assert ora_rpms is not None
    assert 'oracleasm' in ora_rpms.packages
    assert ora_rpms.get_max('oracleasm').version == '2.6.18-164.el5-2.0.5'
    assert ora_rpms.get_max('oracleasm').release == '1.el5'
    assert 'oracleasmlib' in ora_rpms.packages
    assert ora_rpms.get_max('oracleasmlib').version == '2.0.4'
    assert ora_rpms.get_max('oracleasmlib').release == '1.el5'
    assert 'oracleasm-support' in ora_rpms.packages
    assert ora_rpms.get_max('oracleasm-support').version == '2.1.3'
    assert ora_rpms.get_max('oracleasm-support').release == '1.el5'
    return


def test_is_hypervisor():
    rpms = InstalledRpms(context_wrap(RHV_HYPERVISOR_RPMS))
    assert 'vdsm' in rpms.packages
    assert rpms.is_hypervisor


def test_unicode_char_in_rpms():
    rpms = InstalledRpms(context_wrap(RPMS_PACKAGE_WITH_UNICODE))
    assert 'openobexƎ' in rpms.packages
    rpm = rpms.get_max('openobexƎ')
    assert rpm.package == 'openobexƎ-1.4-7.el6'


def test_pad_version_uneven_sections():
    assert pad_version('1.el7', '1.el7_4.ngx') == ([1, 'el', 7, 0, ''], [1, 'el', 7, 4, 'ngx'])


def test_epoch():
    rpms = InstalledRpms(context_wrap(RPMS_PACKAGE))
    rpm = rpms.get_max('openldap')
    assert rpm.package_with_epoch == 'openldap-0:2.4.23-31.el6'
    assert rpm.nevra == 'openldap-0:2.4.23-31.el6.x86_64'
    rpms = InstalledRpms(context_wrap(RPMS_JSON))
    rpm = rpms.get_max('log4j')
    assert rpm.package_with_epoch == 'log4j-0:1.2.17-15.el7'
    assert rpm.nevra == 'log4j-0:1.2.17-15.el7.noarch'
    rpm = rpms.get_max('kbd-misc')
    assert rpm.package_with_epoch == 'kbd-misc-0:1.15.5-11.el7'
    assert rpm.nevra == 'kbd-misc-0:1.15.5-11.el7.noarch'
    rpm = rpms.get_max('grub2-tools')
    assert rpm.package_with_epoch == 'grub2-tools-1:2.02-0.34.el7_2'
    assert rpm.nevra == 'grub2-tools-1:2.02-0.34.el7_2.x86_64'


def test_rpm_object_hashing():
    rpm_yum1 = InstalledRpm.from_package('yum-3.4.3-132.el7')
    assert rpm_yum1.arch is None
    rpm_yum2 = InstalledRpm.from_package('yum-3.4.3-132.el7')
    assert rpm_yum2.arch is None
    rpm_kernel = InstalledRpm.from_package('kernel-3.10.0-327')
    assert rpm_kernel.arch is None
    assert rpm_yum1.__hash__() == rpm_yum2.__hash__()
    assert rpm_yum1.__hash__() != rpm_kernel.__hash__()
    assert rpm_yum2.__hash__() != rpm_kernel.__hash__()
    rpm1 = InstalledRpm.from_package('yum-3.4.3-132.el7.i686')
    assert rpm1.arch == 'i686'
    rpm2 = InstalledRpm.from_package('yum-3.4.3-132.el7.i686')
    assert rpm2.arch == 'i686'
    rpm3 = InstalledRpm.from_package('kernel-3.10.0-327.x86_64')
    assert rpm3.arch == 'x86_64'
    assert rpm1.__hash__() == rpm2.__hash__()
    assert rpm1.__hash__() != rpm3.__hash__()
    assert rpm2.__hash__() != rpm3.__hash__()
    rpm1 = InstalledRpm.from_package('yum-3.4.3-132.el7')
    assert rpm1.arch is None
    rpm2 = InstalledRpm.from_package('yum-3.4.3-132.el7.ppc64le')
    assert rpm2.arch == 'ppc64le'
    assert rpm1.__hash__() != rpm2.__hash__()
    return


def test_gpgkey():
    rpms = InstalledRpms(context_wrap(RPMS_GPG_PUBKEY))
    assert isinstance(rpms.get_max('gpg-pubkey'), InstalledRpm)
    assert len(rpms.packages) == 1
    assert rpms.get_max('gpg-pubkey').name == 'gpg-pubkey'


def test_vmaas():
    rpms = InstalledRpms(context_wrap(RPMS_VMAAS))
    rpm = rpms.get_max('compat-libstdc++-296')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '2.96'
    assert rpm.release == '144.el6'
    rpm = rpms.get_max('compat-libstdc++-33')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '3.2.3'
    assert rpm.release == '72.el7'
    rpm = rpms.get_max('flash-plugin')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '32.0.0.171'
    assert rpm.release == '1.el6_10'
    rpm = rpms.get_max('glibc')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '2.12'
    assert rpm.release == '1.149.el6_6.5'
    rpm = rpms.get_max('infinipath-psm')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '3.3'
    assert rpm.release == '19_g67c0807_open.el6'
    rpm = rpms.get_max('kmod-fnic')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '1.6.0.12b'
    assert rpm.release == 'rhel6u6.el6'
    rpm = rpms.get_max('krb5-libs')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '1.10.3'
    assert rpm.release == '65.el6'
    rpm = rpms.get_max('libaio-devel')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '0.3.107'
    assert rpm.release == '10.el6'
    rpm = rpms.get_max('mdadm')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '4.1'
    assert rpm.release == 'rc1_2.el7'
    rpm = rpms.get_max('nagios-plugins-disk')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '2.2.1'
    assert rpm.release == '16.20180725git3429dad.el7'
    rpm = rpms.get_max('TaniumClient')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '7.2.314.3211'
    assert rpm.release == '1.rhe7'
    rpm = rpms.get_max('xymon')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '4.3.25'
    assert rpm.release == '1.el6'
    rpm = rpms.get_max('xz')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '5.2.2'
    assert rpm.release == '1.el7'
    rpm = rpms.get_max('xz-libs')
    assert isinstance(rpm, InstalledRpm)
    assert rpm.version == '5.2.2'
    assert rpm.release == '1.el7'