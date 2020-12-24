# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/settings.py
# Compiled at: 2016-06-16 16:03:55
import os
login = os.environ['OC_LOGIN']
password = os.environ['OC_PASSWD']
email = os.environ['OC_EMAIL']
name = os.environ['OC_NAME']
surname = os.environ['OC_SURNAME']
address = os.environ['OC_ADDRESS']
additional_login = os.environ['OC_ADDITIONAL_LOGIN']
additional_password = os.environ['OC_ADDITIONAL_PASSWD']
additional_email = os.environ['OC_ADDITIONAL_EMAIL']
additional_name = os.environ['OC_ADDITIONAL_NAME']
additional_surname = os.environ['OC_ADDITIONAL_SURNAME']
admin_name = os.environ['OC_ADMIN_NAME']
admin_passwd = os.environ['OC_ADMIN_PASSWD']
nodes = os.environ['OC_NODES'].split(' ')
storages = os.environ['OC_STORAGES'].split(' ')