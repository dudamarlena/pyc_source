# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wangwenpei/Codes/nextoa/cabric/cabric/components/update.py
# Compiled at: 2016-11-16 20:36:33
import os, sys, json
from cliez.component import Component
from cabric.utils import get_roots, mirror_put, run, bind_hosts, execute, get_platform, run_block

class UpdateComponent(Component):

    def run(self, options):
        """
        :param options:
        :return:
        """
        self.print_message('plan feature')

    @classmethod
    def add_arguments(cls):
        """
        sub parser document
        """
        return [
         (
          ('--node', '-p'), dict(nargs='+', help='install sub node settings'))]