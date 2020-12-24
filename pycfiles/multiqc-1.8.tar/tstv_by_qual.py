# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/vcftools/tstv_by_qual.py
# Compiled at: 2019-02-06 06:32:56
""" MultiQC module to parse TsTv by quality output from vcftools TsTv-by-qual """
import logging
from multiqc.plots import linegraph
log = logging.getLogger(__name__)

class TsTvByQualMixin:

    def parse_tstv_by_qual(self):
        """ Create the HTML for the TsTv by quality linegraph plot. """
        self.vcftools_tstv_by_qual = dict()
        for f in self.find_log_files('vcftools/tstv_by_qual', filehandles=True):
            d = {}
            for line in f['f'].readlines()[1:]:
                key = float(line.split()[0])
                val = float(line.split()[6])
                if val == float('inf') or val == float('-inf'):
                    val = float('nan')
                d[key] = val

            self.vcftools_tstv_by_qual[f['s_name']] = d

        self.vcftools_tstv_by_qual = self.ignore_samples(self.vcftools_tstv_by_qual)
        if len(self.vcftools_tstv_by_qual) == 0:
            return 0
        pconfig = {'id': 'vcftools_tstv_by_qual', 
           'title': 'VCFTools: TsTv by Qual', 
           'ylab': 'TsTv Ratio', 
           'xlab': 'SNP Quality Threshold', 
           'xmin': 0, 
           'ymin': 0, 
           'smooth_points': 400, 
           'smooth_points_sumcounts': False}
        helptext = "\n        `Transition` is a purine-to-purine or pyrimidine-to-pyrimidine point mutations.\n        `Transversion` is a purine-to-pyrimidine or pyrimidine-to-purine point mutation.\n        `Quality` here is the Phred-scaled quality score as given in the QUAL column of VCF.\n        Note: only bi-allelic SNPs are used (multi-allelic sites and INDELs are skipped.)\n        Refer to Vcftools's manual (https://vcftools.github.io/man_latest.html) on `--TsTv-by-qual`\n        "
        self.add_section(name='TsTv by Qual', anchor='vcftools-tstv-by-qual', description='Plot of `TSTV-BY-QUAL` - the transition to transversion ratio as a function of SNP quality from the output of vcftools TsTv-by-qual.', helptext=helptext, plot=linegraph.plot(self.vcftools_tstv_by_qual, pconfig))
        return len(self.vcftools_tstv_by_qual)