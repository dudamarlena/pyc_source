# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/core/GeneratorFactory.py
# Compiled at: 2017-01-24 01:10:58
# Size of source mod 2**32: 528 bytes
from core.ProjectGenerator import ProjectGenerator
from core.ModelGenerator import ModelGenerator
from core.ModelTestsGenerator import ModelTestsGenerator
from core.MethodsGenerator import MethodsGenerator
from core.MethodsTestsGenerator import MethodsTestsGenerator
from core.PublicationGenerator import PublicationGenerator
from core.PublicationTestsGenerator import PublicationTestsGenerator

class GeneratorFactory(object):

    def generate_file(self, object_type, args):
        return eval(object_type)(args).generate()