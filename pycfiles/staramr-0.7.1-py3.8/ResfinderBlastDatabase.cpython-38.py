# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/blast/resfinder/ResfinderBlastDatabase.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 550 bytes
import logging
import staramr.blast.AbstractBlastDatabase as AbstractBlastDatabase
logger = logging.getLogger('ResfinderBlastDatabase')

class ResfinderBlastDatabase(AbstractBlastDatabase):

    def __init__(self, database_dir):
        super().__init__(database_dir)

    def get_name(self):
        return 'resfinder'