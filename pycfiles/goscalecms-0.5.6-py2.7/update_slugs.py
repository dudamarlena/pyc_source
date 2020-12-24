# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/management/commands/subcommands/update_slugs.py
# Compiled at: 2013-03-18 00:16:35
from django.core.management.base import BaseCommand

class UpdateSlugs(BaseCommand):
    help = 'Update slugs for all posts.'

    def handle(self, *args, **options):
        from goscale.models import Post
        print 'Re-saving all posts...'
        print
        for post in Post.objects.all():
            post.save()
            print 'Post slug: %s' % post.slug

        print
        print 'Slugs updated.'