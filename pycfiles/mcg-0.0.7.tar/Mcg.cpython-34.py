# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/cli/Mcg.py
# Compiled at: 2017-01-24 16:17:40
# Size of source mod 2**32: 293 bytes
from cement.core.foundation import CementApp
from cli.BaseController import BaseController

class Mcg(CementApp):

    class Meta:
        label = 'mcg'
        base_controller = BaseController
        config_files = [
         '/etc/mcg/mcg.conf',
         'C:/mcg/mcg.conf']