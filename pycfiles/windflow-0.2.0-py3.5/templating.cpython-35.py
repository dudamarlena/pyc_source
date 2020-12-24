# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/windflow/services/templating.py
# Compiled at: 2018-04-18 11:33:58
# Size of source mod 2**32: 535 bytes
import simplejson
from jinja2 import Environment, FileSystemLoader
from windflow.services.base import Service

class Templating(Service):
    __doc__ = '\n    Jinja2 templating service.\n\n    '
    name = 'templating'

    @property
    def loader(self):
        return FileSystemLoader('templates')

    def __init__(self):
        self.env = Environment(loader=self.loader)
        self.env.filters['json'] = simplejson.dumps

    def render(self, name, *args, **kwargs):
        return self.env.get_template(name).render(*args, **kwargs)