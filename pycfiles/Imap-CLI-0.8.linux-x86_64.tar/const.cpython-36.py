# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/imap_cli/const.py
# Compiled at: 2018-06-03 05:36:57
# Size of source mod 2**32: 1873 bytes
"""Constant used by Imap_CLI packages """
VERSION = 0.7
DEFAULT_DIRECTORY = 'INBOX'
DEFAULT_PORT = 143
DEFAULT_SSL_PORT = 993
STATUS_OK = 'OK'
IMAP_SPECIAL_FLAGS = [
 'ANSWERED',
 'DELETED',
 'DRAFT',
 'FLAGGED',
 'RECENT',
 'SEEN',
 'UNSEEN']
FLAG_DELETED = '\\Deleted'
FLAG_SEEN = '\\Seen'
FLAG_ANSWERED = '\\Answered'
FLAG_FLAGGED = '\\Flagged'
FLAG_DRAFT = '\\Draft'
FLAG_RECENT = '\\Recent'
MESSAGE_PARTS = [
 'BODY',
 'BODYSTRUCTURE',
 'ENVELOPE',
 'FLAGS',
 'INTERNALDATE',
 'RFC822',
 'RFC822.HEADER',
 'RFC822.SIZE',
 'RFC822.TEXT',
 'UID']
SEARH_CRITERION = [
 'ALL',
 'ANSWERED',
 'BCC <string>',
 'BEFORE <date>',
 'BODY <string>',
 'CC <string>',
 'DELETED',
 'DRAFT',
 'FLAGGED',
 'FROM <string>',
 'HEADER <field-name> <string>',
 'KEYWORD <flag>',
 'LARGER <n>',
 'NEW',
 'NOT <search-key>',
 'OLD',
 'ON <date>',
 'OR <search-key1> <search-key2>',
 'RECENT',
 'SEEN',
 'SENTBEFORE <date>',
 'SENTON <date>',
 'SENTSINCE <date>',
 'SINCE <date>',
 'SMALLER <n>',
 'SUBJECT <string>',
 'TEXT <string>',
 'TO <string>',
 'UID <sequence set>',
 'UNANSWERED',
 'UNDELETED',
 'UNDRAFT',
 'UNFLAGGED',
 'UNKEYWORD <flag>',
 'UNSEEN']
SASL_XOAUTH2_IR = 'user={}\x01auth=Bearer {}\x01\x01'
DEFAULT_CONFIG_FILE = '~/.config/imap-cli'