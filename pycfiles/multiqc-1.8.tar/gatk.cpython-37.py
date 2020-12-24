# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/gatk/gatk.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 3453 bytes
""" MultiQC module to parse output from GATK """
from __future__ import print_function
from collections import OrderedDict
import logging
from multiqc.modules.base_module import BaseMultiqcModule
from .varianteval import VariantEvalMixin
from .base_recalibrator import BaseRecalibratorMixin
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule, BaseRecalibratorMixin, VariantEvalMixin):
    __doc__ = ' GATK has a number of different commands and outputs.\n    This MultiQC module supports some but not all. The code for\n    each script is split into its own file and adds a section to\n    the module output if logs are found. '

    def __init__(self):
        super(MultiqcModule, self).__init__(name='GATK',
          anchor='gatk',
          target='GATK',
          href='https://www.broadinstitute.org/gatk/',
          info=' is a toolkit offering a wide variety of tools with a primary focus on variant discovery and genotyping.')
        self.general_stats_headers = OrderedDict()
        self.general_stats_data = dict()
        n_reports_found = 0
        n_reports_found += self.parse_gatk_base_recalibrator()
        n_reports_found += self.parse_gatk_varianteval()
        if n_reports_found == 0:
            raise UserWarning
        self.general_stats_addcols(self.general_stats_data, self.general_stats_headers)

    def parse_report(self, lines, table_names):
        """ Parse a GATK report https://software.broadinstitute.org/gatk/documentation/article.php?id=1244

        Only GATTable entries are parsed.  Tables are returned as a dict of tables.
        Each table is a dict of arrays, where names correspond to column names, and arrays
        correspond to column values.

        Args:
            lines (file handle): an iterable over the lines of a GATK report.
            table_names (dict): a dict with keys that are GATK report table names
                (e.g. "#:GATKTable:Quantized:Quality quantization map"), and values that are the
                keys in the returned dict.

        Returns:
            {
                table_1:
                    {
                        col_1: [ val_1, val_2, ... ]
                        col_2: [ val_1, val_2, ... ]
                        ...
                    }
                table_2:
                    ...
            }
        """
        report = dict()
        lines = (l for l in lines)
        for line in lines:
            line = line.rstrip()
            if line in table_names.keys():
                report[table_names[line]] = self.parse_gatk_report_table(lines)

        return report

    def parse_gatk_report_table(self, lines):
        headers = next(lines).rstrip().split()
        table = OrderedDict([(h, []) for h in headers])
        for line in lines:
            line = line.rstrip()
            if line == '':
                break
            for index, value in enumerate(line.split()):
                table[headers[index]].append(value)

        return table