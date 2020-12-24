# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/bibstract/config.py
# Compiled at: 2020-04-26 00:14:33
# Size of source mod 2**32: 452 bytes
"""Application configuration class.

"""
__author__ = 'Paul Landes'
from zensols.config import CommandLineConfig, ExtendedInterpolationConfig

class AppConfig(ExtendedInterpolationConfig, CommandLineConfig):

    def __init__(self, *args, **kwargs):
        (super(AppConfig, self).__init__)(args, default_expect=True, **kwargs)

    def set_defaults(self, master_bib: str=None):
        self.set_default('master_bib', None, master_bib)