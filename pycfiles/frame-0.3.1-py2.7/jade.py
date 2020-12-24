# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/extensions/jade.py
# Compiled at: 2013-08-10 12:52:27
from frame.extensions.templates import Jinja2Driver, TemplateDriver
from frame.dotdict import DotDict
from jinja2 import Environment, ChoiceLoader, PackageLoader, FileSystemLoader
jade_config = DotDict({'environment': None})

class JadeDriver(Jinja2Driver):

    def __init__(self, **options):
        TemplateDriver.__init__(self, **options)
        loaders = list(options['loaders'])
        loaders.insert(0, FileSystemLoader(options['directory']))
        if jade_config.environment:
            self.environment = jade_config.environment
        else:
            self.environment = Environment(loader=ChoiceLoader(loaders), extensions=options['extensions'] + ['pyjade.ext.jinja.PyJadeExtension'])


def register_config(config):
    config.templates.jade = jade_config


def register_driver(drivers):
    drivers.register('template', 'jade', JadeDriver)