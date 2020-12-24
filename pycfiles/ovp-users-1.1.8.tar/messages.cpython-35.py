# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/messages.py
# Compiled at: 2017-04-27 14:06:03
# Size of source mod 2**32: 658 bytes
from ovp_users import serializers
from ovp_users import emails
from rest_framework import decorators
from rest_framework import mixins
from rest_framework import response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination

class UserMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    email = ''
    locale = ''

    def mailing(self, async_mail=None):
        return emails.UserMail(self, async_mail)

    def create(self, request, *args, **kwargs):
        self.email = request.data['emailTo']
        self.mailing().sendMessageToAnotherVolunteer(request.data)
        return response.Response(True)