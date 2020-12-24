# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_file_listing.py
# Compiled at: 2019-05-16 13:41:33
from insights.core import FileListing
from insights.tests import context_wrap
SINGLE_DIRECTORY = '\ntotal 32\ndrwxr-xr-x.  5 root root  4096 Jun 28  2017 .\ndrwxr-xr-x. 15 root root  4096 Aug 10 09:42 ..\nlrwxrwxrwx.  1 root root    49 Jun 28  2017 cert.pem -> /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem\ndrwxr-xr-x.  2 root root  4096 Jun 28  2017 certs\ndrwxr-xr-x.  2 root root  4096 Mar 29  2017 misc\n-rw-r--r--.  1 root root 10923 Feb  7  2017 openssl.cnf\ndrwxr-xr-x.  2 root root  4096 Feb  7  2017 private\n'
MULTIPLE_DIRECTORIES = '\n/etc/sysconfig:\ntotal 96\ndrwxr-xr-x.  7 0 0 4096 Jul  6 23:41 .\ndrwxr-xr-x. 77 0 0 8192 Jul 13 03:55 ..\ndrwxr-xr-x.  2 0 0   41 Jul  6 23:32 cbq\ndrwxr-xr-x.  2 0 0    6 Sep 16  2015 console\n-rw-------.  1 0 0 1390 Mar  4  2014 ebtables-config\n-rw-r--r--.  1 0 0   72 Sep 15  2015 firewalld\nlrwxrwxrwx.  1 0 0   17 Jul  6 23:32 grub -> /etc/default/grub\n\n/etc/rc.d/rc3.d:\ntotal 4\ndrwxr-xr-x.  2 0 0   58 Jul  6 23:32 .\ndrwxr-xr-x. 10 0 0 4096 Sep 16  2015 ..\nlrwxrwxrwx.  1 0 0   20 Jul  6 23:32 K50netconsole -> ../init.d/netconsole\nlrwxrwxrwx.  1 0 0   17 Jul  6 23:32 S10network -> ../init.d/network\nlrwxrwxrwx.  1 0 0   15 Jul  6 23:32 S97rhnsd -> ../init.d/rhnsd\n'
COMPLICATED_FILES = '\n/tmp:\ntotal 16\ndr-xr-xr-x.  2 0 0     4096 Mar  4 16:19 .\ndr-xr-xr-x. 10 0 0     4096 Mar  4 16:19 ..\n-rw-r--r--.  1 0 0   123891 Aug 25  2015 config-3.10.0-229.14.1.el7.x86_64\nlrwxrwxrwx.  1 0 0       11 Aug  4  2014 menu.lst -> ./grub.conf\nbrw-rw----.  1 0 6 253,  10 Aug  4 16:56 dm-10\ncrw-------.  1 0 0 10,  236 Jul 25 10:00 control\nsrw-------.  1 26214 17738 0 Oct 19 08:48 geany_socket.c46453c2\n-rw-rw-r--.  1 24306 24306 13895 Oct 21 15:42 File name with spaces in it!\n-rw-rw-r--.  1 24306 24306 13895 Oct 21 15:42 Unicode ÅÍÎÏÓÔ\uf8ffÒÚÆ☃ madness.txt\ndrwxr-xr-x+  2 0 0       41 Jul  6 23:32 additional_ACLs\n-rw-rw----.  1 0 6 253,  10 Aug  4 16:56 comma in size currently valid\nbrw-rw----.  1 0 6  1048576 Aug  4 16:56 block dev with no comma also valid\n-rwxr-xr-x.  2 0 0     1024 Jul  6 23:32 file_name_ending_with_colon:\nlrwxrwxrwx.  1 0 0       11 Aug  4  2014 link with spaces -> ../file with spaces\n'
SELINUX_DIRECTORY = '\n/boot:\ntotal 3\n-rw-r--r--. root root system_u:object_r:boot_t:s0      config-3.10.0-267\ndrwxr-xr-x. root root system_u:object_r:boot_t:s0      grub2\n-rw-r--r--. root root system_u:object_r:boot_t:s0      initramfs-0-rescue\n'
FILES_CREATED_WITH_SELINUX_DISABLED = '\n/dev/mapper:\ntotal 2\nlrwxrwxrwx 1 0 0 7 Apr 27 05:34 lv_cpwtk001_data01 -> ../dm-7\nlrwxrwxrwx 1 0 0 7 Apr 27 05:34 lv_cpwtk001_redo01 -> ../dm-8\n'
BAD_DIRECTORY_ENTRIES = '\ndr-xr-xr-x.  2 0 0     4096 Mar  4 16:19 dir entry with no dir header\ntotal 3\n\n/badness:\n    -rwxr-xr-x. 0 0    1 Sep 12 2010 indented entry\nxr-xr--r--. 0 0        1 Sep 12  2010 bad file type\n-rxr-xr-x.  0 0        1 Sep 12  2010 missing user w permission\n-rwxr-xr-x  0 0        1 Sep 12  2010 missing ACL dot\n-rw-r--r--. user with spaces group 2 Oct 3 2011 user with spaces\n-rw-r--r--. user group with spaces 2 Oct 3 2011 group with spaces\ndr-xr-xr-x. -42 -63 1271 Jan  6  2008 Negative user and group numbers\ndr-xr-xr-x. 1 7 123, 124, 125 Jan 6 2008 Three comma blocks in size\nbrw-rw----. 1 0 6 123456 Aug 4 16:56 two size blocks\nprw-rw----. 1000 1000  0  6 2007 Month missing\nprw-rw----. 1000 1000  0 No 6 2007 Month too short\nprw-rw----. 1000 1000  0 November 6 2007 Month too long\nprw-rw----. 1000 1000  0 Nov  2007 Day too long\nprw-rw----. 1000 1000  0 Nov 126 2007 Day too long\nprw-rw----. 1000 1000  0 Nov 126  Year missing\nprw-rw----. 1000 1000  0 Nov 126 20107 Year too long\nprw-rw----. 1000 1000  0 Nov 12 :56 Missing hour\nprw-rw----. 1000 1000  0 Nov 12 723:56 Hour too long\nprw-rw----. 1000 1000  0 Nov 12 23: Missing minute\nprw-rw----. 1000 1000  0 Nov 12 23:3 Minute too short\nprw-rw----. 1000 1000  0 Nov 12 23:357 Minute too long\n-rw------ 1 root root 762 Sep 23 002 permission too short\nbash: ls: command not found\n-rw------ 1 root root 762 Se\n-rw------- 1 ro:t root 762 Sep 23 002 colon in uid\n-rw------- 1 root r:ot 762 Sep 23 002 colon in gid\n-rwasdfas- 1 root root 762 Sep 23 002 bad permissions block\n-rwx/----- 1 root root 762 Sep 23 002 slash in permissions block\n-rwx------ 1 root root 762 Sep 23 002 /slashes/in/filename\n/rwasdfas- 1 root root 762 Sep 23 002 slash in file type and no colon on end\n/usr/bin/ls: cannot access /boot/grub2/grub.cfg: No such file or directory\ncannot access /boot/grub2/grub.cfg: No such file or directory\nNo such file or directory\nadsf\n'

def test_single_directory():
    ctx = context_wrap(SINGLE_DIRECTORY, path='ls_-la_.etc.pki.tls')
    dirs = FileListing(ctx)
    assert '/etc/pki/tls' in dirs
    assert '/etc/pki/tls' in dirs.listings
    assert '/etc/pki/tls/certs' not in dirs
    assert '/etc/pki' not in dirs
    assert '/etc' not in dirs
    assert dirs.listings['/etc/pki/tls']['name'] == '/etc/pki/tls'
    assert dirs.files_of('/etc/pki/tls') == ['cert.pem', 'openssl.cnf']
    assert dirs.dirs_of('/etc/pki/tls') == ['.', '..', 'certs', 'misc', 'private']
    assert dirs.total_of('/etc/pki/tls') == 32


def test_multiple_directories():
    dirs = FileListing(context_wrap(MULTIPLE_DIRECTORIES, path='ls_-la_.etc'))
    assert '/etc/sysconfig' in dirs
    assert '/etc/sysconfig' in dirs.listings
    assert '/etc/rc.d/rc3.d' in dirs
    assert '/etc/rc.d/rc4.d' not in dirs
    esc = dirs.listings['/etc/sysconfig']
    assert sorted(esc.keys()) == sorted(['entries', 'files', 'dirs', 'specials', 'total', 'name'])
    assert dirs.files_of('/etc/sysconfig') == ['ebtables-config', 'firewalld', 'grub']
    assert dirs.dirs_of('/etc/sysconfig') == ['.', '..', 'cbq', 'console']
    assert dirs.specials_of('/etc/sysconfig') == []
    listing = dirs.listing_of('/etc/sysconfig')
    assert listing['..'] == {'type': 'd', 
       'perms': 'rwxr-xr-x.', 'links': 77, 'owner': '0', 'group': '0', 
       'size': 8192, 'date': 'Jul 13 03:55', 'name': '..', 'raw_entry': 'drwxr-xr-x. 77 0 0 8192 Jul 13 03:55 ..', 
       'dir': '/etc/sysconfig'}
    assert listing['cbq'] == {'type': 'd', 
       'perms': 'rwxr-xr-x.', 'links': 2, 'owner': '0', 'group': '0', 
       'size': 41, 'date': 'Jul  6 23:32', 'name': 'cbq', 'raw_entry': 'drwxr-xr-x.  2 0 0   41 Jul  6 23:32 cbq', 
       'dir': '/etc/sysconfig'}
    assert listing['firewalld'] == {'type': '-', 
       'perms': 'rw-r--r--.', 'links': 1, 'owner': '0', 'group': '0', 
       'size': 72, 'date': 'Sep 15  2015', 'name': 'firewalld', 
       'raw_entry': '-rw-r--r--.  1 0 0   72 Sep 15  2015 firewalld', 
       'dir': '/etc/sysconfig'}
    assert listing['grub'] == {'type': 'l', 
       'perms': 'rwxrwxrwx.', 'links': 1, 'owner': '0', 'group': '0', 
       'size': 17, 'date': 'Jul  6 23:32', 'name': 'grub', 'link': '/etc/default/grub', 
       'raw_entry': 'lrwxrwxrwx.  1 0 0   17 Jul  6 23:32 grub -> /etc/default/grub', 
       'dir': '/etc/sysconfig'}
    listing = dirs.listing_of('/etc/rc.d/rc3.d')
    assert listing['..'] == {'type': 'd', 
       'perms': 'rwxr-xr-x.', 'links': 10, 'owner': '0', 'group': '0', 
       'size': 4096, 'date': 'Sep 16  2015', 'name': '..', 'raw_entry': 'drwxr-xr-x. 10 0 0 4096 Sep 16  2015 ..', 
       'dir': '/etc/rc.d/rc3.d'}
    assert listing['K50netconsole'] == {'type': 'l', 
       'perms': 'rwxrwxrwx.', 'links': 1, 'owner': '0', 'group': '0', 
       'size': 20, 'date': 'Jul  6 23:32', 'name': 'K50netconsole', 
       'link': '../init.d/netconsole', 'raw_entry': 'lrwxrwxrwx.  1 0 0   20 Jul  6 23:32 K50netconsole -> ../init.d/netconsole', 
       'dir': '/etc/rc.d/rc3.d'}
    assert dirs.total_of('/etc/sysconfig') == 96
    assert dirs.total_of('/etc/rc.d/rc3.d') == 4
    assert dirs.dir_contains('/etc/sysconfig', 'firewalld')
    assert dirs.dir_entry('/etc/sysconfig', 'grub') == {'type': 'l', 
       'perms': 'rwxrwxrwx.', 'links': 1, 'owner': '0', 'group': '0', 
       'size': 17, 'date': 'Jul  6 23:32', 'name': 'grub', 'link': '/etc/default/grub', 
       'raw_entry': 'lrwxrwxrwx.  1 0 0   17 Jul  6 23:32 grub -> /etc/default/grub', 
       'dir': '/etc/sysconfig'}
    assert dirs.path_entry('/etc/sysconfig/cbq') == {'type': 'd', 
       'perms': 'rwxr-xr-x.', 'links': 2, 'owner': '0', 'group': '0', 
       'size': 41, 'date': 'Jul  6 23:32', 'name': 'cbq', 'raw_entry': 'drwxr-xr-x.  2 0 0   41 Jul  6 23:32 cbq', 
       'dir': '/etc/sysconfig'}
    assert dirs.path_entry('no_slash') is None
    assert dirs.path_entry('/') is None
    assert dirs.path_entry('/foo') is None
    assert dirs.path_entry('/etc/sysconfig/notfound') is None
    return


def test_complicated_directory():
    dirs = FileListing(context_wrap(COMPLICATED_FILES))
    listing = dirs.listing_of('/tmp')
    assert listing['config-3.10.0-229.14.1.el7.x86_64']['type'] == '-'
    assert listing['menu.lst']['type'] == 'l'
    assert listing['menu.lst']['link'] == './grub.conf'
    assert dirs.dir_entry('/tmp', 'dm-10') == {'type': 'b', 
       'perms': 'rw-rw----.', 'links': 1, 'owner': '0', 'group': '6', 
       'major': 253, 'minor': 10, 'date': 'Aug  4 16:56', 'name': 'dm-10', 
       'dir': '/tmp', 'raw_entry': 'brw-rw----.  1 0 6 253,  10 Aug  4 16:56 dm-10'}
    assert listing['dm-10']['type'] == 'b'
    assert listing['dm-10']['major'] == 253
    assert listing['dm-10']['minor'] == 10
    assert listing['control']['type'] == 'c'
    assert listing['control']['major'] == 10
    assert listing['control']['minor'] == 236
    assert listing['geany_socket.c46453c2']['type'] == 's'
    assert listing['geany_socket.c46453c2']['size'] == 0
    assert listing['link with spaces']['type'] == 'l'
    assert listing['link with spaces']['link'] == '../file with spaces'
    assert 'size' not in listing['dm-10']
    assert 'size' not in listing['control']
    assert 'File name with spaces in it!' in listing
    assert 'Unicode ÅÍÎÏÓÔ\uf8ffÒÚÆ☃ madness.txt' in listing
    assert 'file_name_ending_with_colon:' in listing
    assert dirs.dir_contains('/tmp', 'File name with spaces in it!')
    assert dirs.dir_contains('/tmp', 'Unicode ÅÍÎÏÓÔ\uf8ffÒÚÆ☃ madness.txt')
    assert dirs.dir_contains('/tmp', 'file_name_ending_with_colon:')
    assert 'block dev with no comma also valid' in listing
    assert listing['block dev with no comma also valid']['size'] == 1048576
    assert 'major' not in listing['block dev with no comma also valid']
    assert 'minor' not in listing['block dev with no comma also valid']
    assert 'additional_ACLs' in listing
    assert listing['additional_ACLs']['perms'] == 'rwxr-xr-x+'


def test_selinux_directory():
    dirs = FileListing(context_wrap(SELINUX_DIRECTORY))
    expected = {'type': 'd', 
       'perms': 'rwxr-xr-x.', 'owner': 'root', 'group': 'root', 'se_user': 'system_u', 
       'se_role': 'object_r', 'se_type': 'boot_t', 'se_mls': 's0', 
       'name': 'grub2', 'raw_entry': 'drwxr-xr-x. root root system_u:object_r:boot_t:s0      grub2', 
       'dir': '/boot'}
    actual = dirs.dir_entry('/boot', 'grub2')
    assert actual == expected


def test_files_created_with_selinux_disabled():
    dirs = FileListing(context_wrap(FILES_CREATED_WITH_SELINUX_DISABLED))
    assert dirs.dir_entry('/dev/mapper', 'lv_cpwtk001_data01') == {'group': '0', 
       'name': 'lv_cpwtk001_data01', 'links': 1, 'perms': 'rwxrwxrwx', 'raw_entry': 'lrwxrwxrwx 1 0 0 7 Apr 27 05:34 lv_cpwtk001_data01 -> ../dm-7', 
       'owner': '0', 'link': '../dm-7', 
       'date': 'Apr 27 05:34', 'type': 'l', 'dir': '/dev/mapper', 'size': 7}


def test_single_directory_with_special_path():

    def _content_asserts(dirs, path):
        assert path in dirs
        assert path in dirs.listings
        assert '/etc/pki/tls/certs' not in dirs
        assert '/etc' not in dirs
        assert dirs.listings[path]['name'] == path
        assert dirs.files_of(path) == ['cert.pem', 'openssl.cnf']
        assert dirs.dirs_of(path) == ['.', '..', 'certs', 'misc', 'private']

    ctx = context_wrap(SINGLE_DIRECTORY, path='ls_-la_.etc.pki.tls')
    _content_asserts(FileListing(ctx), '/etc/pki/tls')
    ctx = context_wrap(SINGLE_DIRECTORY, path='ls_-la_.etc.pki')
    _content_asserts(FileListing(ctx), '/etc/pki')
    ctx = context_wrap(SINGLE_DIRECTORY, path='ls_-la_.')
    _content_asserts(FileListing(ctx), '/')
    ctx = context_wrap(SINGLE_DIRECTORY, path='ls_-la_')
    _content_asserts(FileListing(ctx), '/')
    ctx = context_wrap(SINGLE_DIRECTORY, path='ls_-la')
    _content_asserts(FileListing(ctx), '/')