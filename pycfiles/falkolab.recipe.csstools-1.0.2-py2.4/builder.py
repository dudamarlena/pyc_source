# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/recipe/csstools/builder.py
# Compiled at: 2009-06-04 04:46:11
from falkolab.recipe.csstools import combiner
from warnings import warn

class CSSBuilder(object):
    __module__ = __name__

    def __init__(self, buildout, name, options):
        self.defaults = {'resource-dir': options.get('resource-dir')}
        self.options = {'targetencoding': 'utf-8', 'compress': False}
        self.options.update(options)
        self.defaults.update(self.options)
        self.buildout = buildout
        if self.options.get('output-name') is not None:
            assert self.options.get('section'), ValueError('output-name var requires "section" var to select config section')
        self.minify = self.options.get('compress', False)
        if self.minify not in ('True', 'true', '1'):
            self.minify = False
        else:
            self.minify = True
        self.section = self.options.get('section', None)
        self.sourceencoding = self.options.get('sourceencoding', None)
        self.targetencoding = self.options.get('targetencoding', None)
        return

    def install(self):
        self.combiner = combiner.Combiner.getCombinerFromConfig(self.options.get('config'), output_dir=self.options.get('output-dir'), defaults=self.defaults, printer=self.buildout._logger.info)
        files = self.combiner.run(minify=self.minify, section=self.section, sourceencoding=self.sourceencoding, targetencoding=self.targetencoding)
        return files

    update = install