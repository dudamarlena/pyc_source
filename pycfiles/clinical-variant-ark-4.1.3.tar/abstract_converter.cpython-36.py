# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mdiazmel/code/aramis/clinica/clinica/iotools/abstract_converter.py
# Compiled at: 2019-10-10 04:46:11
# Size of source mod 2**32: 225 bytes
import abc

class Converter:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def convert_images(self, src, dst):
        pass

    @abc.abstractmethod
    def convert_clinical_data(self, src, dst):
        pass