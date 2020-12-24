# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /a/lib/python3.6/site-packages/bibtools/config.py
# Compiled at: 2017-03-31 15:34:25
# Size of source mod 2**32: 1016 bytes
"""
Configuration subsystem
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import codecs
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from .util import bibpath, datastream, die
__all__ = [
 'BibConfig Error']
RCP = configparser.RawConfigParser
Error = configparser.Error

class BibConfig(RCP):

    def __init__(self):
        RCP.__init__(self)
        self.readfp(codecs.getreader('utf-8')(datastream('defaults.cfg')))
        self.read(bibpath('bib.cfg'))

    def get_or_die(self, section, option):
        try:
            return self.get(section, option)
        except Error:
            die('cannot find required configuration key %s/%s', section, option)