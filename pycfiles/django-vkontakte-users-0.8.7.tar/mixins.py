# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-users/vkontakte_users/mixins.py
# Compiled at: 2015-03-09 12:30:53
from django.utils import timezone
from .models import User

class ParseUsersMixin(object):
    """
    Manager mixin for parsing response with extra cache 'profiles'. Used in vkontakte_wall,vkontakte_board applications
    """

    def parse_response_users(self, response_list):
        users = User.remote.parse_response_list(response_list.get('profiles', []), {'fetched': timezone.now()})
        instances = []
        for instance in users:
            instances += [User.remote.get_or_create_from_instance(instance)]

        return instances