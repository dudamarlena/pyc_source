# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/custom.py
# Compiled at: 2008-06-20 03:40:59
import logging
from pycrud.lib.base import *
from sqlchemistry import Config, Environment
log = logging.getLogger(__name__)

class CustomController(BaseController):

    def index(self):
        self.conf = Config(g.custom_config)
        self.env = Environment(self.conf)
        tbl_names = self.env.tables.keys()
        return tbl_names

    def show_columns(self):
        table = request.params['table']
        self.conf = Config(g.custom_config)
        self.env = Environment(self.conf)
        c.columns = self.env.tables[table].c.keys()
        return c.columns