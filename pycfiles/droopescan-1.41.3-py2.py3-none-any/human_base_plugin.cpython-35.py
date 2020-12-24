# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/droopescan/dscan/plugins/internal/human_base_plugin.py
# Compiled at: 2019-06-14 01:34:00
# Size of source mod 2**32: 356 bytes
from __future__ import print_function
from cement.core import handler, controller
from distutils.util import strtobool
import dscan.common.functions as f, sys

class HumanBasePlugin(controller.CementBaseController):

    def error(self, *args, **kwargs):
        f.error(*args, **kwargs)

    def msg(self, msg, end='\n'):
        print(msg, end=end)