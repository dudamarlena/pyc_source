# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-easy-contact-setup/easy_contact_setup/version.py
# Compiled at: 2016-07-22 06:26:26
VERSION = (0, 3, 9)
APPLICATION_NAME = 'contact-form-setup'
VERSION_str = str(VERSION).strip('()').replace(',', '.').replace(' ', '')
Application_description = 'App for setting up the email-host'
VERSION_INFO = '\n"Version: %s\nModification date: 15.08.2011\n\n\n0.3.9 meta-data update\n0.3.3 Readme and license in root dir moved. EmailField now unencrypted.\n      src folder removed so readme is on the toplevel.\n0.3.1 Mail host can also be set.\n0.3.0 Now data encrypted saved in to database\n\nTODO:\n    - write unittests\n' % (VERSION_str,)