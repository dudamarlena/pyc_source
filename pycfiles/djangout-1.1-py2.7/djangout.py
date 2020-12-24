# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djangout.py
# Compiled at: 2013-07-16 05:55:19
"""
Buildout recipes for Buildout.

"""
from os import path
from logging import getLogger
from pkg_resources import working_set
from zc.recipe.egg import Eggs
_LOGGER = getLogger(__name__)

class AdminMediaRecipe(object):
    """
    Recipe to make available the path to the media files in Django Admin.
    
    """

    def __init__(self, buildout, name, options):
        if 'eggs' not in options:
            options['eggs'] = ''
            _LOGGER.debug("Set the 'eggs' option to an empty string")
        ws = Eggs(buildout, name, options).working_set(['django >= 1.4'])[1]
        for dist in ws:
            working_set.add(dist)

        from django import __file__ as django_file
        django_root = path.dirname(django_file)
        admin_media = path.join(django_root, 'contrib', 'admin', 'static', 'admin')
        options['admin_media_root'] = admin_media

    def install(self):
        return ()

    def update(self):
        return ()