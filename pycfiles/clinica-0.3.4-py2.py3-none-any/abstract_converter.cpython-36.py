# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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