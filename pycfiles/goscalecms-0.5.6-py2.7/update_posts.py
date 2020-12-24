# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/management/commands/subcommands/update_posts.py
# Compiled at: 2013-03-18 00:56:55
from django.core.management.base import BaseCommand

class UpdatePosts(BaseCommand):
    help = 'Updates posts for all plugins.'

    def handle(self, *args, **options):
        from goscale import utils
        sites = []
        if options['site']:
            from django.contrib.sites.models import Site
            sites.append(Site.objects.get(pk=int(options['site'])))
        else:
            if options['theme']:
                from goscale.themes.models import Theme
                sites.extend(Theme.objects.get(name=options['theme']).get_sites())
            for plugin in utils.get_plugins(sites):
                print 'Updating GoScale plugin: %s (%s)' % (plugin, plugin.id)
                instance, count = utils.update_plugin(plugin.id)
                print 'Updated %d posts for %s (%d)' % (count, plugin, plugin.id)