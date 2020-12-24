# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_samba.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import samba
from insights.tests import context_wrap
from doctest import testmod
SAMBA_CONFIG_DOCUMENTATION = '\n# This is the main Samba configuration file. You should read the\n# smb.conf(5) manual page in order to understand the options listed\n#...\n#======================= Global Settings =====================================\n\n[global]\n    workgroup = MYGROUP\n    server string = Samba Server Version %v\n    max log size = 50\n\n[homes]\n    comment = Home Directories\n    browseable = no\n    writable = yes\n;   valid users = %S\n;   valid users = MYDOMAIN\\%S\n\n[printers]\n    comment = All Printers\n    path = /var/spool/samba\n    browseable = no\n    guest ok = no\n    writable = no\n    printable = yes\n\n# A publicly accessible directory, but read only, except for people in\n# the "staff" group\n[public]\n   comment = Public Stuff\n   path = /home/samba\n   public = yes\n   writable = yes\n   printable = no\n   write list = +staff\n'

def test_documentation():
    failed, total = testmod(samba, globs={'conf': samba.SambaConfig(context_wrap(SAMBA_CONFIG_DOCUMENTATION))})
    assert failed == 0


SAMBA_CONFIG = '\n# This is the main Samba configuration file. You should read the\n# smb.conf(5) manual page in order to understand the options listed\n#...\n#======================= Global Settings =====================================\n\n# By running `testparm`, it is apparent that options outside the [global]\n# section before the [global] section are treated as if they were in the\n# [global] section.\n# `testparm` is a program from the samba package.\n\nthis option should be in global = yes\n\n[global]\n\n#...\n# Hosts Allow/Hosts Deny lets you restrict who can connect, and you can\n# specifiy it as a per share option as well\n#\n    workgroup = MYGROUP\n    server string = Samba Server Version %v\n\n;   netbios name = MYSERVER\n\n;   interfaces = lo eth0 192.168.12.2/24 192.168.13.2/24\n;   hosts allow = 127. 192.168.12. 192.168.13.\n\n# --------------------------- Logging Options -----------------------------\n#\n# Log File let you specify where to put logs and how to split them up.\n#\n# Max Log Size let you specify the max size log files should reach\n\n    # logs split per machine\n    log file = /var/log/samba/log.%m\n    # max 50KB per log file, then rotate\n    max log size = 50\n\n# ----------------------- Standalone Server Options ------------------------\n#\n# Scurity can be set to user, share(deprecated) or server(deprecated)\n#\n# Backend to store user information in. New installations should\n# use either tdbsam or ldapsam. smbpasswd is available for backwards\n# compatibility. tdbsam requires no further configuration.\n\n    security = user\n    passdb backend = tdbsam\n\n#...\n# --------------------------- Printing Options -----------------------------\n#\n# Load Printers let you load automatically the list of printers rather\n# than setting them up individually\n#\n# Cups Options let you pass the cups libs custom options, setting it to raw\n# for example will let you use drivers on your Windows clients\n#\n# Printcap Name let you specify an alternative printcap file\n#\n# You can choose a non default printing system using the Printing option\n\n    load printers = yes\n    cups options = raw\n\n;   printcap name = /etc/printcap\n    #obtain list of printers automatically on SystemV\n;   printcap name = lpstat\n;   printing = cups\n\n# --------------------------- Filesystem Options ---------------------------\n#\n# The following options can be uncommented if the filesystem supports\n# Extended Attributes and they are enabled (usually by the mount option\n# user_xattr). Thess options will let the admin store the DOS attributes\n# in an EA and make samba not mess with the permission bits.\n#\n# Note: these options can also be set just per share, setting them in global\n# makes them the default for all shares\n\n;   map archive = no\n;   map hidden = no\n;   map read only = no\n;   map system = no\n;   store dos attributes = yes\n\n\n#============================ Share Definitions ==============================\n\n[homes]\n    comment = Home Directories\n    browseable = no\n    writable = yes\n;   valid users = %S\n;   valid users = MYDOMAIN\\%S\n\n[printers]\n    comment = All Printers\n    path = /var/spool/samba\n    browseable = no\n    guest ok = no\n    writable = no\n    printable = yes\n\n# Un-comment the following and create the netlogon directory for Domain Logons\n;   [netlogon]\n;   comment = Network Logon Service\n;   path = /var/lib/samba/netlogon\n;   guest ok = yes\n;   writable = no\n;   share modes = no\n\n\n# Un-comment the following to provide a specific roving profile share\n# the default is to use the user\'s home directory\n;   [Profiles]\n;   path = /var/lib/samba/profiles\n;   browseable = no\n;   guest ok = yes\n\n\n# A publicly accessible directory, but read only, except for people in\n# the "staff" group\n;   [public]\n;   comment = Public Stuff\n;   path = /home/samba\n;   public = yes\n;   writable = yes\n;   printable = no\n;   write list = +staff\n\n[ GlObAl  ]\n\n# Samba also automatically treats non-lowercase section names as lowercase and strips whitespace.\n# This behavior can be checked with `testparm` again.\nthis option should also be in global = true\n\n[ GlObAl  ]\n\n# This tests specifically that two same-named sections are automatically merged in case the\n# RawConfigParser\'s behavior ever changes.\nthis another option should also be in global = 1\n'

def test_match():
    config = samba.SambaConfig(context_wrap(SAMBA_CONFIG))
    assert config.get('global', 'this option should be in global') == 'yes'
    assert config.get('global', 'this option should also be in global') == 'true'
    assert config.get('global', 'this another option should also be in global') == '1'
    assert config.get('global', 'workgroup') == 'MYGROUP'
    assert config.get('global', 'workgroup') == 'MYGROUP'
    assert config.get('global', 'server string') == 'Samba Server Version %v'
    assert not config.has_option('global', 'netbios name')
    assert config.get('global', 'log file') == '/var/log/samba/log.%m'
    assert config.get('global', 'max log size') == '50'
    assert config.get('global', 'security') == 'user'
    assert config.get('global', 'passdb backend') == 'tdbsam'
    assert config.get('global', 'load printers') == 'yes'
    assert config.get('global', 'cups options') == 'raw'
    assert not config.has_option('global', 'printcap name')
    assert config.get('homes', 'comment') == 'Home Directories'
    assert config.get('homes', 'browseable') == 'no'
    assert config.get('homes', 'writable') == 'yes'
    assert not config.has_option('homes', 'valid users')
    assert config.get('printers', 'comment') == 'All Printers'
    assert config.get('printers', 'path') == '/var/spool/samba'
    assert config.get('printers', 'browseable') == 'no'
    assert config.get('printers', 'guest ok') == 'no'
    assert config.get('printers', 'writable') == 'no'
    assert config.get('printers', 'printable') == 'yes'
    assert 'netlogin' not in config
    assert 'Profiles' not in config
    assert 'public' not in config