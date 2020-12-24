# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/django-ninecms/ninecms/management/commands/check_updates.py
# Compiled at: 2016-04-06 06:07:34
# Size of source mod 2**32: 1221 bytes
""" Management command for checking updates """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django.core.management import BaseCommand
from django.core.cache import caches
from django.core.mail import mail_admins
from django.template import loader
from django.utils.translation import ugettext as _
from ninecms.utils.status import Capturing
import pip

class Command(BaseCommand):
    help = 'Check for updates, store the results to cache and send email to admins.'

    def handle(self, *args, **options):
        """ Core function
        :param args: None
        :param options: None
        :return: None
        """
        with Capturing() as (updates):
            pip.main(['list', '--outdated', '--retries', '1'])
        cache = caches['default']
        if not updates:
            cache.delete('updates')
        else:
            cache.set('updates', updates, 604800)
            t = loader.get_template('ninecms/mail_updates.txt')
            mail_admins(_('New updates available'), t.render({'updates': updates}))