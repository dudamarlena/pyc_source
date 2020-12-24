# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lance/.virtualenvs/wolverine/lib/python3.5/site-packages/wolverine/web/jinja.py
# Compiled at: 2016-02-11 15:10:12
# Size of source mod 2**32: 627 bytes
import os, sys
from wolverine.module import MicroModule
try:
    import jinja2
    from aiohttp_jinja2 import setup
except:
    pass

__all__ = ('JinjaModule', )

class JinjaModule(MicroModule):

    def __init__(self):
        super().__init__()
        self.name = 'jinja'
        self.template_folder = '/tmp/templates'

    def run(self):
        self.read_config()
        setup(self.app.web, loader=jinja2.FileSystemLoader(self.template_folder))

    def read_config(self):
        config = self.app.config[self.name.upper()]
        self.template_folder = config.get('templates', '/tmp/templates')