# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/vcftools/tstv_by_count.py
# Compiled at: 2017-09-23 10:30:24
# Size of source mod 2**32: 2405 bytes
""" MultiQC module to parse TsTv by alternative allele count from vcftools TsTv-by-count """
import logging
from multiqc.plots import linegraph
log = logging.getLogger(__name__)

class TsTvByCountMixin:

    def parse_tstv_by_count(self):
        """ Create the HTML for the TsTv by alternative allele count linegraph plot. """
        self.vcftools_tstv_by_count = dict()
        for f in self.find_log_files('vcftools/tstv_by_count', filehandles=True):
            d = {}
            for line in f['f'].readlines()[1:]:
                key = float(line.split()[0])
                val = float(line.split()[3])
                d[key] = val

            self.vcftools_tstv_by_count[f['s_name']] = d

        self.vcftools_tstv_by_count = self.ignore_samples(self.vcftools_tstv_by_count)
        if len(self.vcftools_tstv_by_count) == 0:
            return 0
        pconfig = {'id':'vcftools_tstv_by_count', 
         'title':'VCFTools: TsTv by Count', 
         'ylab':'TsTv Ratio', 
         'xlab':'Alternative Allele Count', 
         'xmin':0, 
         'ymin':0, 
         'smooth_points':400, 
         'smooth_points_sumcounts':False}
        helptext = "\n        `Transition` is a purine-to-purine or pyrimidine-to-pyrimidine point mutations.\n        `Transversion` is a purine-to-pyrimidine or pyrimidine-to-purine point mutation.\n        `Alternative allele count` is the number of alternative alleles at the site.\n        Note: only bi-allelic SNPs are used (multi-allelic sites and INDELs are skipped.)\n        Refer to Vcftools's manual (https://vcftools.github.io/man_latest.html) on `--TsTv-by-count`\n        "
        self.add_section(name='TsTv by Count',
          anchor='vcftools-tstv-by-count',
          description='Plot of `TSTV-BY-COUNT` - the transition to transversion ratio as a function of alternative allele count from the output of vcftools TsTv-by-count.',
          helptext=helptext,
          plot=(linegraph.plot(self.vcftools_tstv_by_count, pconfig)))
        return len(self.vcftools_tstv_by_count)