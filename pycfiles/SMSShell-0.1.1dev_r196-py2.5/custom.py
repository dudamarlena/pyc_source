# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/smsshell/controllers/custom.py
# Compiled at: 2008-05-07 05:10:17
import logging
from smsshell.lib.base import *
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