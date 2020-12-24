# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/core/ProjectGenerator.py
# Compiled at: 2017-01-24 01:10:58
# Size of source mod 2**32: 435 bytes
from core.Generator import Generator
import os
from subprocess import call

class ProjectGenerator(Generator):

    def __init__(self, args):
        self.project = args['project']

    def generate(self):
        print('Creating Project ' + self.project + '...')
        call('meteor create --full ' + self.project, shell=True)
        os.chdir(self.project)
        call(['ls', '-la'])

    def insert_into_file(self):
        pass