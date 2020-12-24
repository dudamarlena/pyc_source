# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jsb/recipe/jsonbot/install.py
# Compiled at: 2011-04-09 13:05:06
"""
jsb.recipe.jsonbot:install
----------------------

Installs the jsonbot.

"""
import logging, os, zc.recipe.egg
from jsb.recipe import get_relative_path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.realpath(__file__))))))

class Recipe(zc.recipe.egg.Scripts):

    def __init__(self, buildout, name, opts):
        self.parts_dir = buildout['buildout']['parts-directory']
        self.buildout_dir = buildout['buildout']['directory']
        join = os.path.join
        defaults = {'sdk-directory': join(self.parts_dir, 'jsonbot'), 
           'config-file': join(self.buildout_dir, 'jsonbot.cfg'), 
           'interpreter': 'python', 
           'extra-paths': '', 
           'eggs': 'jsb'}
        defaults.update(opts)
        opts = defaults
        self.config_file = os.path.abspath(opts['config-file'])
        self.sdk_dir = os.path.abspath(opts['sdk-directory'])
        scripts = [
         'jsb',
         'jsb-irc',
         'jsb-xmpp',
         'jsb-fleet']
        self.scripts = [ (s, opts.get(s + '-script', s)) for s in scripts ]
        opts['extra-paths'] += '\n%s\n%s' % (BASE, self.sdk_dir)
        self.use_rel_paths = opts.get('relative-paths', buildout['buildout'].get('relative-paths', 'false')) == 'true'
        super(Recipe, self).__init__(buildout, name, opts)

    def install(self):
        """Creates the scripts."""
        entry_points = [ '%s=jsb.recipe.jsonbot.scripts:%s' % (scriptname, function) for (function, scriptname) in self.scripts
                       ]
        if self.use_rel_paths is not True:
            initialization = ['base = %r' % self.buildout_dir]
        else:
            initialization = []
        initialization.append('gae = %s' % self.get_path(self.sdk_dir))
        initialization.append('cfg = %s' % self.get_path(self.config_file))
        self.options.update({'entry-points': (' ').join(entry_points), 
           'initialization': ('\n').join(initialization), 
           'arguments': 'base, gae, cfg'})
        return super(Recipe, self).install()

    def get_path(self, path):
        if self.use_rel_paths is True:
            return get_relative_path(path, self.buildout['buildout']['directory'])
        else:
            return '%r' % os.path.abspath(path)

    update = install