# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_ls_parser.py
# Compiled at: 2019-05-16 13:41:33
import six
from insights.core.ls_parser import parse
SINGLE_DIRECTORY = '\ntotal 32\ndrwxr-xr-x.  5 root root  4096 Jun 28  2017 .\ndrwxr-xr-x. 15 root root  4096 Aug 10 09:42 ..\nlrwxrwxrwx.  1 root root    49 Jun 28  2017 cert.pem -> /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem\ndrwxr-xr-x.  2 root root  4096 Jun 28  2017 certs\ndrwxr-xr-x.  2 root root  4096 Mar 29  2017 misc\n-rw-r--r--.  1 root root 10923 Feb  7  2017 openssl.cnf\ndrwxr-xr-x.  2 root root  4096 Feb  7  2017 private\n'
MULTIPLE_DIRECTORIES = '\n/etc/sysconfig:\ntotal 96\ndrwxr-xr-x.  7 0 0 4096 Jul  6 23:41 .\ndrwxr-xr-x. 77 0 0 8192 Jul 13 03:55 ..\ndrwxr-xr-x.  2 0 0   41 Jul  6 23:32 cbq\ndrwxr-xr-x.  2 0 0    6 Sep 16  2015 console\n-rw-------.  1 0 0 1390 Mar  4  2014 ebtables-config\n-rw-r--r--.  1 0 0   72 Sep 15  2015 firewalld\nlrwxrwxrwx.  1 0 0   17 Jul  6 23:32 grub -> /etc/default/grub\n\n/etc/rc.d/rc3.d:\ntotal 4\ndrwxr-xr-x.  2 0 0   58 Jul  6 23:32 .\ndrwxr-xr-x. 10 0 0 4096 Sep 16  2015 ..\nlrwxrwxrwx.  1 0 0   20 Jul  6 23:32 K50netconsole -> ../init.d/netconsole\nlrwxrwxrwx.  1 0 0   17 Jul  6 23:32 S10network -> ../init.d/network\nlrwxrwxrwx.  1 0 0   15 Jul  6 23:32 S97rhnsd -> ../init.d/rhnsd\n'
MULTIPLE_DIRECTORIES_WITH_BREAK = '\n/etc:\ntotal 1652\ndrwxr-xr-x. 102   0   0  12288 Nov  6 09:12 .\ndr-xr-xr-x.  21   0   0   4096 Oct 23 10:12 ..\n-rw-------.   1   0   0      0 Oct  2 13:46 .pwd.lock\n-rw-r--r--    1   0   0    163 Oct  2 13:45 .updated\n-rw-r--r--.   1   0   0   1059 Oct  2 13:56 chrony.conf\n-rw-r--r--.   1   0   0   1100 Dec  5  2017 chrony.conf.20180210135613\n\n-rw-r-----.   1   0 993    481 Sep 14  2017 chrony.keys\ndrwxr-xr-x.   2   0   0   4096 Nov  1 03:34 cifs-utils\n\n/etc/sysconfig:\ntotal 96\ndrwxr-xr-x.  7 0 0 4096 Jul  6 23:41 .\ndrwxr-xr-x. 77 0 0 8192 Jul 13 03:55 ..\ndrwxr-xr-x.  2 0 0   41 Jul  6 23:32 cbq\ndrwxr-xr-x.  2 0 0    6 Sep 16  2015 console\n-rw-------.  1 0 0 1390 Mar  4  2014 ebtables-config\n-rw-r--r--.  1 0 0   72 Sep 15  2015 firewalld\nlrwxrwxrwx.  1 0 0   17 Jul  6 23:32 grub -> /etc/default/grub\n\n/etc/rc.d/rc3.d:\ntotal 4\ndrwxr-xr-x.  2 0 0   58 Jul  6 23:32 .\ndrwxr-xr-x. 10 0 0 4096 Sep 16  2015 ..\nlrwxrwxrwx.  1 0 0   20 Jul  6 23:32 K50netconsole -> ../init.d/netconsole\nlrwxrwxrwx.  1 0 0   17 Jul  6 23:32 S10network -> ../init.d/network\nlrwxrwxrwx.  1 0 0   15 Jul  6 23:32 S97rhnsd -> ../init.d/rhnsd\n'
COMPLICATED_FILES = '\n/tmp:\ntotal 16\ndr-xr-xr-x.  2 0 0     4096 Mar  4 16:19 .\ndr-xr-xr-x. 10 0 0     4096 Mar  4 16:19 ..\n-rw-r--r--.  1 0 0   123891 Aug 25  2015 config-3.10.0-229.14.1.el7.x86_64\nlrwxrwxrwx.  1 0 0       11 Aug  4  2014 menu.lst -> ./grub.conf\nbrw-rw----.  1 0 6 253,  10 Aug  4 16:56 dm-10\ncrw-------.  1 0 0 10,  236 Jul 25 10:00 control\nsrw-------.  1 26214 17738 0 Oct 19 08:48 geany_socket.c46453c2\n-rw-rw-r--.  1 24306 24306 13895 Oct 21 15:42 File name with spaces in it!\n-rw-rw-r--.  1 24306 24306 13895 Oct 21 15:42 Unicode ÅÍÎÏÓÔ\uf8ffÒÚÆ☃ madness.txt\ndrwxr-xr-x+  2 0 0       41 Jul  6 23:32 additional_ACLs\nbrw-rw----.  1 0 6  1048576 Aug  4 16:56 block dev with no comma also valid\n-rwxr-xr-x.  2 0 0     1024 Jul  6 23:32 file_name_ending_with_colon:\nlrwxrwxrwx.  1 0 0       11 Aug  4  2014 link with spaces -> ../file with spaces\n'
COMPLICATED_FILES_BAD_LINE = "\n/tmp:\ntotal 16\ndr-xr-xr-x.  2 0 0     4096 Mar  4 16:19 .\ndr-xr-xr-x. 10 0 0     4096 Mar  4 16:19 ..\n-rw-r--r--.  1 0 0   123891 Aug 25  2015 config-3.10.0-229.14.1.el7.x86_64\nls: cannot open directory '/etc/audisp': Permission denied\nlrwxrwxrwx.  1 0 0       11 Aug  4  2014 menu.lst -> ./grub.conf\nbrw-rw----.  1 0 6 253,  10 Aug  4 16:56 dm-10\ncrw-------.  1 0 0 10,  236 Jul 25 10:00 control\nsrw-------.  1 26214 17738 0 Oct 19 08:48 geany_socket.c46453c2\n-rw-rw-r--.  1 24306 24306 13895 Oct 21 15:42 File name with spaces in it!\n-rw-rw-r--.  1 24306 24306 13895 Oct 21 15:42 Unicode ÅÍÎÏÓÔ\uf8ffÒÚÆ☃ madness.txt\ndrwxr-xr-x+  2 0 0       41 Jul  6 23:32 additional_ACLs\nbrw-rw----.  1 0 6  1048576 Aug  4 16:56 block dev with no comma also valid\n-rwxr-xr-x.  2 0 0     1024 Jul  6 23:32 file_name_ending_with_colon:\nlrwxrwxrwx.  1 0 0       11 Aug  4  2014 link with spaces -> ../file with spaces\n"
SELINUX_DIRECTORY = '\n/boot:\ntotal 3\n-rw-r--r--. root root system_u:object_r:boot_t:s0      config-3.10.0-267\ndrwxr-xr-x. root root system_u:object_r:boot_t:s0      grub2\n-rw-r--r--. root root system_u:object_r:boot_t:s0      initramfs-0-rescue\n'
RHEL8_SELINUX_DIRECTORY = '\n/var/lib/nova/instances:\ntotal 0\ndrwxr-xr-x. 3 root root unconfined_u:object_r:var_lib_t:s0 50 Apr  8 16:41 .\ndrwxr-xr-x. 3 root root unconfined_u:object_r:var_lib_t:s0 23 Apr  8 16:29 ..\ndrwxr-xr-x. 2 root root unconfined_u:object_r:var_lib_t:s0 54 Apr  8 16:41 abcd-efgh-ijkl-mnop\n'
FILES_CREATED_WITH_SELINUX_DISABLED = '\n/dev/mapper:\ntotal 2\nlrwxrwxrwx 1 0 0 7 Apr 27 05:34 lv_cpwtk001_data01 -> ../dm-7\nlrwxrwxrwx 1 0 0 7 Apr 27 05:34 lv_cpwtk001_redo01 -> ../dm-8\n'
BAD_DIRECTORY_ENTRIES = '\ndr-xr-xr-x.  2 0 0     4096 Mar  4 16:19 dir entry with no dir header\ntotal 3\n\n/badness:\n    -rwxr-xr-x. 0 0    1 Sep 12 2010 indented entry\nxr-xr--r--. 0 0        1 Sep 12  2010 bad file type\n-rxr-xr-x.  0 0        1 Sep 12  2010 missing user w permission\n-rwxr-xr-x  0 0        1 Sep 12  2010 missing ACL dot\n-rw-r--r--. user with spaces group 2 Oct 3 2011 user with spaces\n-rw-r--r--. user group with spaces 2 Oct 3 2011 group with spaces\ndr-xr-xr-x. -42 -63 1271 Jan  6  2008 Negative user and group numbers\ndr-xr-xr-x. 1 7 123, 124, 125 Jan 6 2008 Three comma blocks in size\nbrw-rw----. 1 0 6 123456 Aug 4 16:56 two size blocks\nprw-rw----. 1000 1000  0  6 2007 Month missing\nprw-rw----. 1000 1000  0 No 6 2007 Month too short\nprw-rw----. 1000 1000  0 November 6 2007 Month too long\nprw-rw----. 1000 1000  0 Nov  2007 Day too long\nprw-rw----. 1000 1000  0 Nov 126 2007 Day too long\nprw-rw----. 1000 1000  0 Nov 126  Year missing\nprw-rw----. 1000 1000  0 Nov 126 20107 Year too long\nprw-rw----. 1000 1000  0 Nov 12 :56 Missing hour\nprw-rw----. 1000 1000  0 Nov 12 723:56 Hour too long\nprw-rw----. 1000 1000  0 Nov 12 23: Missing minute\nprw-rw----. 1000 1000  0 Nov 12 23:3 Minute too short\nprw-rw----. 1000 1000  0 Nov 12 23:357 Minute too long\n-rw------ 1 root root 762 Sep 23 002 permission too short\nbash: ls: command not found\n-rw------ 1 root root 762 Se\n-rw------- 1 ro:t root 762 Sep 23 002 colon in uid\n-rw------- 1 root r:ot 762 Sep 23 002 colon in gid\n-rwasdfas- 1 root root 762 Sep 23 002 bad permissions block\n-rwx/----- 1 root root 762 Sep 23 002 slash in permissions block\n-rwx------ 1 root root 762 Sep 23 002 /slashes/in/filename\n/rwasdfas- 1 root root 762 Sep 23 002 slash in file type and no colon on end\n/usr/bin/ls: cannot access /boot/grub2/grub.cfg: No such file or directory\ncannot access /boot/grub2/grub.cfg: No such file or directory\nNo such file or directory\nadsf\n'

def test_parse_selinux():
    results = parse(SELINUX_DIRECTORY.splitlines(), '/boot')
    stanza = results['/boot']
    assert stanza['name'] == '/boot'
    assert stanza['total'] == 3
    assert len(stanza['entries']) == 3
    res = stanza['entries']['config-3.10.0-267']
    assert res['type'] == '-'
    assert res['owner'] == 'root'
    assert res['group'] == 'root'
    assert res['se_user'] == 'system_u'
    assert res['se_role'] == 'object_r'
    assert res['se_type'] == 'boot_t'
    assert res['se_mls'] == 's0'
    assert res['name'] == 'config-3.10.0-267'


def test_parse_single_directory():
    results = parse(SINGLE_DIRECTORY.splitlines(), '/etc')
    stanza = results['/etc']
    assert stanza['name'] == '/etc'
    assert stanza['total'] == 32
    assert len(stanza['entries']) == 7
    res = stanza['entries']['cert.pem']
    assert res['type'] == 'l'
    assert res['owner'] == 'root'
    assert res['group'] == 'root'
    assert res['date'] == 'Jun 28  2017'
    assert res['name'] == 'cert.pem'
    assert res['link'] == '/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem'
    assert res['links'] == 1
    assert res['dir'] == '/etc'


def test_parse_multiple_directories():
    results = parse(MULTIPLE_DIRECTORIES.splitlines(), None)
    assert len(results) == 2, len(results)
    assert results['/etc/sysconfig']['name'] == '/etc/sysconfig'
    assert results['/etc/sysconfig']['total'] == 96
    assert results['/etc/rc.d/rc3.d']['name'] == '/etc/rc.d/rc3.d'
    assert results['/etc/rc.d/rc3.d']['total'] == 4
    res = results['/etc/sysconfig']['entries']['ebtables-config']
    assert res['type'] == '-'
    assert res['links'] == 1
    assert res['owner'] == '0'
    assert res['group'] == '0'
    assert res['size'] == 1390
    assert res['date'] == 'Mar  4  2014'
    assert res['name'] == 'ebtables-config'
    assert res['dir'] == '/etc/sysconfig'
    return


def test_parse_multiple_directories_with_break():
    results = parse(MULTIPLE_DIRECTORIES_WITH_BREAK.splitlines(), None)
    assert len(results) == 3, len(results)
    assert len(results.values()) == 3
    assert len(results.items()) == 3
    assert len(list(six.iteritems(results))) == 3
    assert results['/etc']['name'] == '/etc'
    assert results['/etc']['total'] == 1652
    assert results['/etc/rc.d/rc3.d']['name'] == '/etc/rc.d/rc3.d'
    assert results['/etc/rc.d/rc3.d']['total'] == 4
    res = results['/etc']['entries']['chrony.conf.20180210135613']
    assert res['type'] == '-'
    assert res['links'] == 1
    assert res['owner'] == '0'
    assert res['group'] == '0'
    assert res['size'] == 1100
    assert res['date'] == 'Dec  5  2017'
    assert res['name'] == 'chrony.conf.20180210135613'
    assert res['dir'] == '/etc'
    return


def test_complicated_files():
    results = parse(COMPLICATED_FILES.splitlines(), '/tmp')
    assert len(results) == 1
    assert results['/tmp']['total'] == 16, results['/tmp']['total']
    assert results['/tmp']['name'] == '/tmp', results['/tmp']['name']
    res = results['/tmp']['entries']['dm-10']
    assert res['type'] == 'b'
    assert res['links'] == 1
    assert res['owner'] == '0'
    assert res['group'] == '6'
    assert res['major'] == 253
    assert res['minor'] == 10
    assert res['date'] == 'Aug  4 16:56'
    assert res['name'] == 'dm-10'
    assert res['dir'] == '/tmp'


def test_files_with_selinux_disabled():
    results = parse(FILES_CREATED_WITH_SELINUX_DISABLED.splitlines(), '/dev/mapper')
    assert len(results) == 1
    assert results['/dev/mapper']['total'] == 2
    assert results['/dev/mapper']['name'] == '/dev/mapper', results[0]['name']
    res = results['/dev/mapper']['entries']['lv_cpwtk001_data01']
    assert res['type'] == 'l'
    assert res['links'] == 1
    assert res['owner'] == '0'
    assert res['group'] == '0'
    assert res['size'] == 7
    assert res['date'] == 'Apr 27 05:34'
    assert res['name'] == 'lv_cpwtk001_data01'
    assert res['link'] == '../dm-7'
    assert res['dir'] == '/dev/mapper'


def test_bad_line():
    results = parse(COMPLICATED_FILES_BAD_LINE.splitlines(), '/tmp')
    assert len(results) == 1
    assert results['/tmp']['total'] == 16, results['/tmp']['total']
    assert results['/tmp']['name'] == '/tmp', results['/tmp']['name']
    res = results['/tmp']['entries']['dm-10']
    assert res['type'] == 'b'
    assert res['links'] == 1
    assert res['owner'] == '0'
    assert res['group'] == '6'
    assert res['major'] == 253
    assert res['minor'] == 10
    assert res['date'] == 'Aug  4 16:56'
    assert res['name'] == 'dm-10'
    assert res['dir'] == '/tmp'


def test_rhel8_selinux():
    results = parse(RHEL8_SELINUX_DIRECTORY.splitlines(), '/var/lib/nova/instances')
    assert len(results) == 1
    assert results['/var/lib/nova/instances']['name'] == '/var/lib/nova/instances', results['/var/lib/nova/instances']['name']
    res = results['/var/lib/nova/instances']['entries']['abcd-efgh-ijkl-mnop']
    assert results['/var/lib/nova/instances']['total'] == 0, results['/var/lib/nova/instances']['total']
    assert res['type'] == 'd'
    assert res['links'] == 2
    assert res['owner'] == 'root'
    assert res['group'] == 'root'
    assert res['se_user'] == 'unconfined_u'
    assert res['se_role'] == 'object_r'
    assert res['se_type'] == 'var_lib_t'
    assert res['se_mls'] == 's0'
    assert res['date'] == 'Apr  8 16:41'
    assert res['name'] == 'abcd-efgh-ijkl-mnop'
    assert res['dir'] == '/var/lib/nova/instances'