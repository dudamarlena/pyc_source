# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/sk/recipe/xdv/impl.py
# Compiled at: 2010-05-29 17:42:53
"""XDV compiler recipe for Buildout: implementation."""
import logging, os, os.path, zc.buildout, xdv.compiler, xdv.utils
_truthiness = ('true', 'yes', '1')
_defaultIncludeMode = 'document'

class Recipe(object):
    """This is a Buildout recipe that compiles XDV rules and themes into XSLT using the XDV compiler."""
    __module__ = __name__

    def __init__(self, buildout, name, options):
        """Initialize the recipe."""
        (self.buildout, self.name, self.options, self.logger) = (
         buildout, name, options, logging.getLogger(name))
        if 'rules' not in options:
            raise zc.buildout.UserError('No ``rules`` option specified to XDV recipe; ``rules`` is required')
        if 'theme' not in options:
            raise zc.buildout.UserError('No ``theme`` option specified to XDV recipe; ``theme`` is required')
        if 'output' not in options:
            options['output'] = os.path.join(buildout['buildout']['parts-directory'], name, 'theme.xsl')
        options['includemode'] = options.get('includemode', _defaultIncludeMode)
        if 'network' in options:
            self.networkOK = options['network'].lower() in _truthiness
        else:
            self.networkOK = buildout['buildout']['offline'].lower() not in _truthiness

    def install(self):
        """Compile XDV."""
        gen = xdv.compiler.compile_theme(self.options['rules'], self.options['theme'], includemode=self.options['includemode'], access_control=self.networkOK and xdv.utils.AC_READ_NET or xdv.utils.AC_READ_FILE)
        try:
            os.makedirs(os.path.dirname(self.options['output']))
        except OSError:
            pass

        gen.write(self.options['output'], encoding='utf-8')
        self.options.created(self.options['output'])
        return self.options.created()

    def update(self):
        """Update the XDV. Since the theme or the rules (or anything it XIncludes) may change, we re-do the install."""
        return self.install()