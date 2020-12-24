# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/fgbio/fgbio.py
# Compiled at: 2019-10-28 10:24:54
# Size of source mod 2**32: 1228 bytes
""" MultiQC module to parse output from fgbio """
import logging
from multiqc.modules.base_module import BaseMultiqcModule
from .groupreadsbyumi import GroupReadsByUmiMixin
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule, GroupReadsByUmiMixin):
    __doc__ = ' fgbio has a number of different commands and outputs.\n    This MultiQC module supports some but not all. The code for\n    each script is split into its own file and adds a section to\n    the module output if logs are found. '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='fgbio',
          anchor='fgbio',
          target='fgbio',
          href='http://fulcrumgenomics.github.io/fgbio/',
          info='  is a command line toolkit for working with genomic and particularly next generation sequencing data..')
        n = dict()
        n['groupreadsbyumi'] = self.parse_groupreadsbyumi()
        if n['groupreadsbyumi'] > 0:
            log.info('Found {} groupreadsbyumi reports'.format(n['groupreadsbyumi']))
        if sum(n.values()) == 0:
            raise UserWarning