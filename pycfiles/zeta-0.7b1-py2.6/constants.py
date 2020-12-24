# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/constants.py
# Compiled at: 2010-03-20 06:14:31
"""Avoid using magic numbers. Instead use contants."""
LEN_SYSFIELD = 64
LEN_SYSVALUE = 256
LEN_NAME = 32
LEN_NAME1 = 64
LEN_SUMMARY = 128
LEN_256 = 256
LEN_DESCRIBE = 65536
LEN_EMAILID = 64
LEN_TZ = 32
LEN_ADDRLINE = 64
LEN_PINCODE = 8
LEN_TAGNAME = 256
LEN_RESOURCEURL = 512
LEN_LICENSENAME = 64
LEN_LICENSESOURCE = 128
LEN_QUERYSTRING = 1024
LEN_1K = 1024
LEN_ATTACHSIZE = 10485760
DUMMY_EMAIL = 'email.id@host.name'
DUMMY_PASSWORD = 'admin123'
ADMIN_EMAIL = 'admin.email@host.name'
ADMIN_PASSWORD = 'admin123'
ANONYMOUS_EMAIL = 'anonymous.id@host.name'
ANONYMOUS_PASSWORD = 'anonymous123'
DEFAULT_TIMEZONE = 'UTC'
ATTACH_DIR = 'fileattach'
DIR_STATICWIKI = 'staticfiles'
PROJHOMEPAGE = 'homepage'
ACCOUNTS_ACTIONS = [
 'newaccount', 'signin', 'signout', 'forgotpass']
ERROR_FLASH = 'error ::'
MESSAGE_FLASH = 'message ::'
MAX_BREADCRUMBS = 6
IFRAME_RET = '<html> <body> <textarea>{ result : "OK" }</textarea> </body> </html>'
RE_UNAME = '^[a-z0-9_]{3,32}$'
RE_EMAIL = '^.*@.*$'
RE_PASSWD = '^.{4,64}$'
RE_PNAME = '^[A-Za-z0-9_.]{1,32}$'
RE_TNAME = '^[A-Za-z0-9_.!]{1,256}$'
TLCOUNT = 100
MAIL_STARTCOUNT = 1