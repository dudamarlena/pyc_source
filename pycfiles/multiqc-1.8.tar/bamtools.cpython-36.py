# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/bamtools/bamtools.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 1488 bytes
""" MultiQC module to parse output from Bamtools """
from collections import OrderedDict
import logging
from multiqc.modules.base_module import BaseMultiqcModule
from . import stats
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' Bamtools is a collection of scripts. This MultiQC module\n    supports some but not all. The code for each script is split\n    into its own file and adds a section to the module ooutput if\n    logs are found.'

    def __init__(self):
        super(MultiqcModule, self).__init__(name='Bamtools', anchor='bamtools', href='https://github.com/pezmaster31/bamtools',
          info="provides both a programmer's API and an end-user's toolkit for handling BAM files.")
        self.general_stats_headers = OrderedDict()
        self.general_stats_data = dict()
        n = dict()
        n['stats'] = stats.parse_reports(self)
        if n['stats'] > 0:
            log.info('Found {} bamtools stats reports'.format(n['stats']))
        if sum(n.values()) == 0:
            raise UserWarning
        self.general_stats_addcols(self.general_stats_data, self.general_stats_headers)