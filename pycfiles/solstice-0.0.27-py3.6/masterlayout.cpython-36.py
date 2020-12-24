# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/files/masterlayout.py
# Compiled at: 2020-05-04 03:27:08
# Size of source mod 2**32: 818 bytes
"""
Module that contains implementations for masater layout sequence files
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import os, tpDcc as tp
from artellapipe.core import sequencefile

class SolsticeMasterLayoutSequenceFile(sequencefile.ArtellaSequenceFile, object):

    def __init__(self, sequence=None):
        super(SolsticeMasterLayoutSequenceFile, self).__init__(file_sequence=sequence)

    def _open_file(self, file_path):
        if not file_path:
            return False
        else:
            if os.path.isfile(file_path):
                if tp.Dcc.scene_name() != file_path:
                    tp.Dcc.open_file(file_path)
            return True