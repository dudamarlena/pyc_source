# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/django_testing_recipe.py
# Compiled at: 2011-06-28 10:17:42
"""
Buildout recipe to use the Nose plugin
:class:`django_testing.DjangoWsgifiedPlugin`.

"""
from zc.buildout import UserError
from zc.recipe.egg import Scripts

class DjangoWsgifiedRecipe(Scripts):

    def __init__(self, buildout, name, options):
        config_uri = options.pop('paste_config_uri', None)
        if not config_uri:
            raise UserError("Part [%s] must define the PasteDeploy config URI in 'paste_config_uri'" % name)
        options['initialization'] = _INITIALIZATION % config_uri
        options['arguments'] = 'argv=args'
        options['scripts'] = 'nosetests'
        super(DjangoWsgifiedRecipe, self).__init__(buildout, name, options)
        return


_INITIALIZATION = '\nfrom sys import argv\nargs = [argv[0], "--with-django-wsgified=%s"] + argv[1:]\n'