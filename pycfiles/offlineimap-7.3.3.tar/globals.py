# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/official_packages/gitrepos/offlineimap/test/OLItest/globals.py
# Compiled at: 2019-02-02 10:37:08
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

default_conf = StringIO("[general]\n#will be set automatically\nmetadata = \naccounts = test\nui = quiet\n\n[Account test]\nlocalrepository = Maildir\nremoterepository = IMAP\n\n[Repository Maildir]\nType = Maildir\n# will be set automatically during tests\nlocalfolders = \n\n[Repository IMAP]\ntype=IMAP\n# Don't hammer the server with too many connection attempts:\nmaxconnections=1\nfolderfilter= lambda f: f.startswith('INBOX.OLItest') or f.startswith('INBOX/OLItest')\n")