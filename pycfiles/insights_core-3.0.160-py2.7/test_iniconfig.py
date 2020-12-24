# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/configtree/tests/test_iniconfig.py
# Compiled at: 2019-05-16 13:41:33
from insights.configtree.iniconfig import parse_doc
CONF1 = ("\n# See smb.conf.example for a more detailed config file or\n# read the smb.conf manpage.\n# Run 'testparm' to verify the config is correct after\n# you modified it.\n\n[global]\n\tworkgroup = SAMBA\n\tsecurity = user\n\n\tpassdb backend = tdbsam\n\n\tprinting = cups\n\tprintcap name = cups\n\tload printers = yes\n\tcups options = raw\n\n[homes]\n\tcomment = Home Directories\n\tvalid users = %S, %D%w%S\n\tbrowseable = No\n\tread only = No\n\tinherit acls = Yes\n\n[printers]\n\tcomment = All Printers\n\tpath = /var/tmp\n\tprintable = Yes\n\tcreate mask = 0600\n\tbrowseable = No\n\n[print$]\n\tcomment = Printer Drivers\n\tpath = /var/lib/samba/drivers\n\twrite list = @printadmin root\n\tforce group = @printadmin\n\tcreate mask = 0664\n\tdirectory mask = 0775\n").strip().splitlines()

def test_smb_conf():
    conf = parse_doc(CONF1)
    assert conf['global']['workgroup'][0].value == 'SAMBA'