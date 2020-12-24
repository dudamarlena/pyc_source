# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/raton/pycharm_projects/django-hautomation-suite/django_hautomation_suite/ha_cfg/management/commands/backup_config.py
# Compiled at: 2014-06-30 04:15:29
import logging, re, shutil, pytz, os, sys
from ha_cfg import paths
from django.core.management.base import BaseCommand, CommandError
logger = logging.getLogger('backup_config')

class Command(BaseCommand):
    args = ''
    help = 'Create a ready to run Django settings file for Home Automation Python Project'

    def handle(self, *args, **options):
        cwd = os.getcwd()
        logger.info('Backing up settings from every involved module to %s' % cwd)
        shutil.copyfile(paths.x10_plugin_settings(), os.path.join(cwd, 'x10_plugin_settings.bak'))
        shutil.copyfile(paths.django_thermostat_settings(), os.path.join(cwd, 'django_thermostat_settings.bak'))