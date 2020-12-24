# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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