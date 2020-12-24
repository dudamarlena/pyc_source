# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/check_docking/management/commands/inspectprofile.py
# Compiled at: 2015-02-07 21:17:43
__doc__ = '生成配置文件, 检测依赖该配置文件进行.\n'
__author__ = 'kylinfish@126.com'
__date__ = '2015/02/06'
import os
from django.conf import settings
from django.utils.importlib import import_module
from django.core.management.base import NoArgsCommand
from check_docking.utility import UrlApi

class Command(NoArgsCommand):
    help = 'make data_config.py profile file of inspect request data.'

    def handle_noargs(self, **options):
        setting_module = os.environ.get('DJANGO_SETTINGS_MODULE')
        project_catalog = os.path.dirname(import_module(setting_module).__file__)
        check_config = getattr(settings, 'INSPECT_PROFILE', None)
        if check_config and check_config.count('.') > 0 and not check_config.endswith('.py'):
            gen_file = os.path.join(project_catalog, '%s.py' % check_config.split('.')[(-1)])
        else:
            gen_file = os.path.join(project_catalog, 'check_config.py')
        UrlApi(gen_file).gen_interfaces()
        return