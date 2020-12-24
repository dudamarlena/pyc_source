# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/monobot/sync/tickettest/simpletickets/api/serializers.py
# Compiled at: 2016-09-18 18:13:24
from rest_framework import serializers
from simpletickets.models import Ticket

class UserTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ('ticket_type', 'severity', 'description')


class StaffTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ('staff', 'ticket_type', 'severity', 'state', 'resolution_text')