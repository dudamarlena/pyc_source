# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/friends/management/commands/find_duplicate_memberfriend.py
# Compiled at: 2015-04-21 15:32:12
from optparse import make_option
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q
from friends.models import MemberFriend

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
     make_option('--delete', action='store_true', dest='delete', help='Delete duplicate records'),)
    help = 'Finds duplicate friendships, optionally deletes them'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute("SELECT GREATEST(member_id, friend_id) AS member1,\n            LEAST(member_id, friend_id) AS member2, min(id) FROM friends_memberfriend\n            WHERE state = 'accepted' GROUP BY member1, member2 HAVING count(id) > 1")
        duplicates = cursor.fetchall()
        print 'There are %d duplicates' % len(duplicates)
        if options['delete']:
            print 'Deleting duplicates...'
            for d in duplicates:
                MemberFriend.objects.filter(Q(member=d[0], friend=d[1]) | Q(member=d[1], friend=d[0]), ~Q(pk=d[2]), state='accepted').delete()

            print 'Duplicates deleted'