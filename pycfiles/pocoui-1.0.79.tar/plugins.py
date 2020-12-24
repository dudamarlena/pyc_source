# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/pony/plugins.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.pkg.pony.plugins\n    ~~~~~~~~~~~~~~~~~~~~~~\n\n    Display information about packages and components.\n\n    :copyright: 2006 by Armin Ronacher, Georg Brandl.\n    :license: GNU GPL, see LICENSE for more details.\n'
from os.path import abspath
from pocoo import Component
from pocoo.application import RequestHandler
from pocoo.http import Response, TemplateResponse

class PluginPony(RequestHandler):
    __module__ = __name__
    handler_regexes = [
     'pony/plugins/$']

    def handle_request(self, req):
        pkgname = req.args.pop('pkg', '')
        compname = req.args.pop('comp', '')
        if pkgname and compname:
            return Response(pkgname)
        elif pkgname:
            return Response(compname + 'x')
        else:
            packages = []
            for pkgname in sorted(self.ctx.pkgmanager.pkgs):
                pkg = {'name': pkgname, 'loaded': pkgname in self.ctx.packages, 'path': abspath(self.ctx.pkgmanager.pkgs[pkgname])}
                if pkg['loaded']:
                    pkg.update(self.ctx.packagemeta[pkgname])
                packages.append(pkg)

            plugintypes = []
            for comp_type in Component.__subclasses__():
                plugintypes.append({'name': comp_type.__name__, 'module': comp_type.__module__.replace(self.ctx.pkg_prefix, 'pocoo.pkg'), 
                   'plugins': [ comp.__module__.split('.')[2] + '::' + comp.__class__.__name__ for comp in self.ctx.get_components(comp_type) ], 'doc': comp_type.__doc__})

            plugintypes.sort(key=lambda x: x['name'].lower())
            plugins = {}
            for comp_type in Component.__subclasses__():
                for comp in self.ctx.get_components(comp_type):
                    plugins[comp] = {'name': comp.__class__.__name__, 'package': comp.__module__.split('.')[2], 'types': [ c.__name__ for c in comp.__class__.comptypes ], 'doc': comp.__class__.__doc__}

            plugins = plugins.values()
            plugins.sort(key=lambda x: x['name'].lower())
            regexes = []
            for comp in self.ctx.get_components(RequestHandler):
                for regex in comp.handler_regexes:
                    if not isinstance(regex, basestring):
                        (regex, _) = regex
                    regexes.append({'regex': regex, 'component': comp.__class__.__name__, 'package': comp.__module__.split('.')[2]})

            regexes.sort(key=lambda x: x['regex'].lower())
            return TemplateResponse('plugins.html', packages=packages, plugins=plugins, regexes=regexes, plugintypes=plugintypes)