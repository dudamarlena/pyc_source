# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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