# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/base/management/commands/load_tendenci2018_defaults.py
# Compiled at: 2020-03-16 17:04:52
# Size of source mod 2**32: 2759 bytes
from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Insert default data'

    def add_arguments(self, parser):
        parser.add_argument('--reset-nav', action='store_true',
          dest='reset_nav',
          default=False,
          help='Reset the navigation')

    def handle(self, **options):
        """
        Load data from tendenci2018 fixtures
        """
        reset_nav = options.get('reset_nav', None)
        self.number_used = []
        self.call_loaddata(reset_nav)

    def call_loaddata(self, reset_nav=False):
        """
        This calls the loaddata command on all creative fixtures.
        """
        if reset_nav:
            from tendenci.apps.navs.models import NavItem
            try:
                main_nav_items = NavItem.objects.filter(nav_id=1)
                main_nav_items.delete()
            except:
                pass

        print('tendenci2018_default_auth_user.json')
        call_command('loaddata', 'tendenci2018_default_auth_user.json')
        print('tendenci2018_default_auth_groups.json')
        call_command('loaddata', 'tendenci2018_default_auth_groups.json')
        print('tendenci2018_default_entities.json')
        call_command('loaddata', 'tendenci2018_default_entities.json')
        print('tendenci2018_default_user_groups.json')
        call_command('loaddata', 'tendenci2018_default_user_groups.json')
        print('tendenci2018_default_files.json')
        call_command('loaddata', 'tendenci2018_default_files.json')
        print('load tendenci2018_default_paymentmethod.json')
        call_command('loaddata', 'tendenci2018_default_paymentmethod.json')
        print('load tendenci2018_default_forums.json')
        call_command('loaddata', 'tendenci2018_default_forums.json')
        print('load tendenci2018_default_regions_region.json')
        call_command('loaddata', 'tendenci2018_default_regions_region.json')
        print('load tendenci2018_default_directories_pricings.json')
        call_command('loaddata', 'tendenci2018_default_directories_pricings.json')
        suffix_list = [
         'profiles_profile',
         'explorer',
         'events',
         'jobs',
         'memberships',
         'corporate_memberships',
         'articles',
         'forms',
         'forums',
         'news',
         'photos',
         'boxes',
         'pages',
         'navs',
         'stories',
         'videos']
        for suffix in suffix_list:
            filename = 'tendenci2018_default_%s.json' % suffix
            print(filename)
            call_command('loaddata', filename)