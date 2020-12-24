# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/clickatell/constants.py
# Compiled at: 2010-05-24 09:08:22
"""
Final or intermediary statuses are passed back by the API depending on the 
callback value set in the original post. The callback URL and optional 
"Username" and "Password" authentication parameters can be set in the 
preferences section of the particular API product within your client account, 
after logging in online. The URL must begin with either http:// (non-encrypted) 
or https:// (encrypted). These are NOT your Clickatell username and password 
but are a username and password of your choice to add additional security.
The variables returned are apiMsgId, cliMsgId, to, timestamp, from, 
status and charge.
"""
CALLBACK_NONE = 0
CALLBACK_INTERMEDIATE = 1
CALLBACK_FINAL = 2
CALLBACK_ALL = 3
NO = 0
YES = 1
FEAT_TEXT = 1
FEAT_8BIT = 2
FEAT_UDH = 4
FEAT_UCS2 = 8
FEAT_ALPHA = 16
FEAT_NUMER = 32
FEAT_FLASH = 512
FEAT_DELIVACK = 8192
FEAT_CONCAT = 16384
QUEUE_HIGH = 1
QUEUE_MEDIUM = 2
QUEUE_LOW = 3
SMS_TEXT = 'SMS_TEXT'
SMS_FLASH = 'SMS_FLASH'
SMS_NOKIA_OLOGO = 'SMS_NOKIA_OLOGO'
SMS_NOKIA_GLOGO = 'SMS_NOKIA_GLOGO'
SMS_NOKIA_PICTURE = 'SMS_NOKIA_PICTURE'
SMS_NOKIA_RINGTONE = 'SMS_NOKIA_RINGTONE'
SMS_NOKIA_RTTL = 'SMS_NOKIA_RTTL'
SMS_NOKIA_CLEAN = 'SMS_NOKIA_CLEAN'
SMS_NOKIA_VCARD = 'SMS_NOKIA_VCARD'
SMS_NOKIA_VCAL = 'SMS_NOKIA_VCAL'
SMS_DEFAULT = SMS_TEXT