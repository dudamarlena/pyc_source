# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/monkey.py
# Compiled at: 2018-03-27 03:51:51
import logging
from django.utils.module_loading import import_string
from django.conf import settings
from django.contrib.staticfiles import finders
logger = logging.getLogger('logger')

def my_get_finder(import_path):
    Finder = import_string(import_path)
    if not issubclass(Finder, finders.BaseFinder):
        raise ImproperlyConfigured('Finder "%s" is not a subclass of "%s"' % (
         Finder, finders.BaseFinder))
    return Finder()


my_get_finder.cache_clear = lambda : True

def apply_monkey(force=False):
    setting = getattr(settings, 'LAYERS', {})
    if 'current' not in setting or 'layers' not in setting or force:
        logger.info('Patching django.contrib.staticfiles.finders.get_finder')
        finders.get_finder = my_get_finder


apply_monkey()