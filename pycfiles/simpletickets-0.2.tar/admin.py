# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/monobot/sync/tickettest/simpletickets/admin.py
# Compiled at: 2016-09-18 19:05:36
from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'user', 'staff', 'state', 'severity', 'ticket_type',
                    'creation_date')
    list_filter = ('user', 'staff', 'severity', 'creation_date', 'ticket_type', 'creation_date')