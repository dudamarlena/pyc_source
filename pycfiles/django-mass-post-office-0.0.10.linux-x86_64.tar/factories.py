# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mass_post_office/tests/factories.py
# Compiled at: 2015-03-06 05:08:58
import factory
from django.contrib.auth.models import User

class UserFactory(factory.Factory):
    FACTORY_FOR = User
    password = 'pbkdf2_sha256$10000$YMFSJlSlzmQT$MVdNVG3SxXrytTDwJ8TuDYl1KmnqCKlFXyP6sEMgV8c='
    username = factory.Sequence(lambda n: 'kanata%s' % n)
    email = 'brandon.walsh@mail.com'
    first_name = 'Brandon'
    last_name = 'Walsh'