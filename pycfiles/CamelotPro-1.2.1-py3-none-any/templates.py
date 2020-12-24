# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/templates.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nA default Jinja2 environment for the rendering of html in print previews\nand others.\n\nThe `loader` loads its templates from the camelot/art/templates\nfolder.  As it is a :class:`jinja2.loaders.ChoiceLoader` object, other\nloaders can be appended or prepended to it :attr:`loaders` attribute, to\ncustomize the look of the print previews or reuse the existing style\n\nThe `environment` is a :class:`jinja2.environment.Environment` which uses\nthe `loader` and that can be used with\nthe :class:`camelot.view.action_steps.print_preview.PrintJinjaTemplate` action\nstep.\n'
from jinja2.environment import Environment
from jinja2.loaders import ChoiceLoader, PackageLoader
loader = ChoiceLoader([PackageLoader('camelot.art')])

class DefaultEnvironment(Environment):

    def __repr__(self):
        return '<camelot.core.templates.environment>'


environment = DefaultEnvironment(loader=loader)