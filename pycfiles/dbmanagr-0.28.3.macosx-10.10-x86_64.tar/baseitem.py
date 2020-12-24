# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/model/baseitem.py
# Compiled at: 2015-10-11 07:17:06
import logging
from dbmanagr.formatter import Formatter
from dbmanagr.model import Model
from dbmanagr.logger import LogWith
from dbmanagr.utils import hash_
logger = logging.getLogger(__name__)

class BaseItem(Model):

    def title(self):
        return 'Title'

    def subtitle(self):
        return 'Subtitle'

    def autocomplete(self):
        return 'Autocomplete'

    def validity(self):
        return True

    def icon(self):
        return 'images/icon.png'

    def value(self):
        return self.title()

    @LogWith(logger)
    def uid(self):
        return hash_(self.autocomplete())

    def format(self):
        return Formatter.format(self)