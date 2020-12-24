# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/core/sequence.py
# Compiled at: 2020-03-08 13:23:53
# Size of source mod 2**32: 1084 bytes
"""
Base class that defines Artella Shot for Solstice
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import logging, artellapipe.register
from artellapipe.core import defines, sequence
LOGGER = logging.getLogger()

class SolsticeSequence(sequence.ArtellaSequence, object):

    def __init__(self, project, sequence_data):
        self._name_dict = dict()
        super(SolsticeSequence, self).__init__(project=project, sequence_data=sequence_data)

    def open_master_layout(self):
        """
        Function that opens mater layout file of this sequence in current DCC
        :return: bool
        """
        file_type = self.get_file_type('master')
        if not file_type:
            return False
        else:
            valid_open = file_type.open_file(status=(defines.ArtellaFileStatus.WORKING))
            return valid_open


artellapipe.register.register_class('Sequence', SolsticeSequence)