# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/templates.py
# Compiled at: 2013-04-11 17:47:52
"""
A default Jinja2 environment for the rendering of html in print previews
and others.

The `loader` loads its templates from the camelot/art/templates
folder.  As it is a :class:`jinja2.loaders.ChoiceLoader` object, other
loaders can be appended or prepended to it :attr:`loaders` attribute, to
customize the look of the print previews or reuse the existing style

The `environment` is a :class:`jinja2.environment.Environment` which uses
the `loader` and that can be used with
the :class:`camelot.view.action_steps.print_preview.PrintJinjaTemplate` action
step.
"""
from jinja2.environment import Environment
from jinja2.loaders import ChoiceLoader, PackageLoader
loader = ChoiceLoader([PackageLoader('camelot.art')])

class DefaultEnvironment(Environment):

    def __repr__(self):
        return '<camelot.core.templates.environment>'


environment = DefaultEnvironment(loader=loader)