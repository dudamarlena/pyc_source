# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/django_setuptest_recipe/recipe.py
# Compiled at: 2011-10-14 09:57:32
import logging, os, sys, zc.buildout
from djangorecipe.recipe import Recipe as BaseRecipe

class Recipe(BaseRecipe):
    __module__ = __name__

    def install(self):
        extra_paths = self.get_extra_paths()
        (requirements, ws) = self.egg.working_set(['django_setuptest_recipe'])
        return self.create_test_script(extra_paths, ws)

    def create_test_script(self, extra_paths, ws):
        return zc.buildout.easy_install.scripts([(self.options.get('control-script', self.name), 'django_setuptest_recipe.recipe', 'main')], ws, self.options['executable'], self.options['bin-directory'], extra_paths=extra_paths)


def main():
    if len(sys.argv) < 2:
        print 'Usage: %s setup.py test [args,]' % sys.argv[0]
        sys.exit(-1)
    f = open(sys.argv[1], 'r')
    try:
        buf = f.read()
    finally:
        f.close()
    del sys.argv[1]
    exec buf