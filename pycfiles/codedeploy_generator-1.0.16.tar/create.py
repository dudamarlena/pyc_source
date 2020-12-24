# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/abito/Repos/Pyton_Repos/deplyment-scripts-creator/codedeploy_generator/commands/create.py
# Compiled at: 2016-05-16 11:40:17
"""The scaffholder command."""
from json import dumps
import codedeploy_generator
from .base import Base

class Create(Base):
    """Say hello, world!"""

    def run(self):
        import os
        from distutils.dir_util import copy_tree
        path = os.path.abspath(codedeploy_generator.__file__)
        dir_path = os.path.dirname(path)
        directory = os.getcwd() + '/src'
        if not os.path.exists(directory):
            os.makedirs(directory)
        copy_tree(dir_path + '/extra/', os.getcwd())