# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-easy-contact/easy_contact/version.py
# Compiled at: 2016-07-22 06:25:44
VERSION = (0, 3, 9)
APPLICATION_NAME = 'django-easy-contact'
VERSION_str = str(VERSION).strip('()').replace(',', '.').replace(' ', '')
VERSION_INFO = '\n"Version: %s\n\nApplication description: "A small contact form application".\n- Works together with django-contact-form-setup app\n- Translated in to german\n\n\n0.3.9 meta-data update\n0.3.3 src folder removed so readme is on the toplevel\n0.3.2 Flexible sending methodes\n0.3.1 Use smtplib directly instead of django.mail\n\nTODO:\n    - write unittests\n' % (VERSION_str,)