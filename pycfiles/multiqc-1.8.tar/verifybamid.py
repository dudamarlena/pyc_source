# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/verifybamid/verifybamid.py
# Compiled at: 2019-11-20 10:26:16
""" MultiQC module to parse output from VerifyBAMID """
from __future__ import print_function
from collections import OrderedDict
import logging
from multiqc import config
from multiqc.plots import table
from multiqc.modules.base_module import BaseMultiqcModule
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    """
         module class, parses stderr logs.
        """

    def __init__(self):
        super(MultiqcModule, self).__init__(name='VerifyBAMID', anchor='verifybamid', href='https://genome.sph.umich.edu/wiki/VerifyBamID', info='detects sample contamination and/or sample swaps.')
        self.hide_chip_columns = True
        self.col_config_defaults = {'max': 100, 
           'min': 0, 
           'suffix': '%', 
           'format': '{:,.3f}', 
           'modify': lambda x: x * 100.0 if x != 'NA' else x, 
           'scale': 'OrRd'}
        self.verifybamid_data = dict()
        for f in self.find_log_files('verifybamid/selfsm'):
            parsed_data = self.parse_selfsm(f)
            if parsed_data is not None:
                for s_name in parsed_data:
                    if s_name in self.verifybamid_data:
                        log.debug(('Duplicate sample name found! Overwriting: {}').format(s_name))
                    self.verifybamid_data[s_name] = parsed_data[s_name]

                self.add_data_source(f, s_name)

        self.verifybamid_data = self.ignore_samples(self.verifybamid_data)
        if len(self.verifybamid_data) == 0:
            raise UserWarning
        log.info(('Found {} reports').format(len(self.verifybamid_data)))
        self.write_data_file(self.verifybamid_data, 'multiqc_verifybamid')
        self.verifybamid_general_stats_table()
        self.verifybamid_table()
        return

    def parse_selfsm(self, f):
        """ Go through selfSM file and create a dictionary with the sample name as a key, """
        parsed_data = dict()
        headers = None
        for l in f['f'].splitlines():
            s = l.split('\t')
            if headers is None:
                headers = s
            else:
                s_name = self.clean_s_name(s[0], f['root'])
                parsed_data[s_name] = {}
                for i, v in enumerate(s):
                    if i != 0:
                        if 'CHIP' in [headers[i]] and v != 'NA':
                            self.hide_chip_columns = False
                        try:
                            parsed_data[s_name][headers[i]] = float(v)
                        except ValueError:
                            parsed_data[s_name][headers[i]] = v

        return parsed_data

    def verifybamid_general_stats_table(self):
        """ Take the percentage of contamination from all the parsed *.SELFSM files and add it to the basic stats table at the top of the report """
        headers = OrderedDict()
        if not self.hide_chip_columns:
            headers['CHIPMIX'] = dict(self.col_config_defaults, **{'title': 'Contamination (S+A)', 
               'description': 'VerifyBamID: CHIPMIX -   Sequence+array estimate of contamination (NA if the external genotype is unavailable)'})
        headers['FREEMIX'] = dict(self.col_config_defaults, **{'title': 'Contamination (S)', 
           'description': 'VerifyBamID: FREEMIX -   Sequence-only estimate of contamination.'})
        self.general_stats_addcols(self.verifybamid_data, headers)

    def verifybamid_table(self):
        """
                Create a table with all the columns from verify BAM ID
                """
        headers = OrderedDict()
        headers['RG'] = {'title': 'Read Group', 
           'description': 'ReadGroup ID of sequenced lane.', 
           'hidden': all([ s['RG'] == 'ALL' for s in self.verifybamid_data.values() ])}
        if not self.hide_chip_columns:
            headers['CHIP_ID'] = {'title': 'Chip ID', 'description': 'ReadGroup ID of sequenced lane.'}
        headers['#SNPS'] = {'title': 'SNPS', 
           'description': '# SNPs passing the criteria from the VCF file', 
           'format': '{:,.0f}', 
           'min': 0, 
           'scale': 'BuPu'}
        headers['#READS'] = {'title': ('{} Reads').format(config.read_count_prefix), 
           'description': ('Number of reads loaded from the BAM file ({})').format(config.read_count_desc), 
           'format': '{:,.1f}', 
           'modify': lambda x: x * config.read_count_multiplier if x != 'NA' else x, 
           'shared_key': 'read_count', 
           'min': 0, 
           'scale': 'GnBu'}
        headers['AVG_DP'] = {'title': 'Average Depth', 
           'description': 'Average sequencing depth at the sites in the VCF file', 
           'suffix': ' X', 
           'min': 0, 
           'scale': 'YlGn'}
        headers['FREEMIX'] = dict(self.col_config_defaults, **{'title': 'Contamination (Seq)', 
           'description': 'VerifyBamID: FREEMIX -   Sequence-only estimate of contamination.'})
        headers['FREELK1'] = {'title': 'FREEELK1', 
           'format': '{:,.0f}', 
           'description': 'Maximum log-likelihood of the sequence reads given estimated contamination under sequence-only method', 
           'min': 0, 
           'scale': 'RdYlGn'}
        headers['FREELK0'] = {'title': 'FREELK0', 
           'format': '{:,.0f}', 
           'description': 'Log-likelihood of the sequence reads given no contamination under sequence-only method', 
           'min': 0, 
           'scale': 'RdYlGn'}
        headers['FREE_RH'] = {'title': 'FREE_RH', 
           'description': 'Estimated reference bias parameter Pr(refBase|HET) (when --free-refBias or --free-full is used)', 
           'hidden': all([ s['FREE_RH'] == 'NA' for s in self.verifybamid_data.values() ])}
        headers['FREE_RA'] = {'title': 'FREE_RA', 
           'description': 'Estimated reference bias parameter Pr(refBase|HOMALT) (when --free-refBias or --free-full is used)', 
           'hidden': all([ s['FREE_RA'] == 'NA' for s in self.verifybamid_data.values() ])}
        if not self.hide_chip_columns:
            headers['CHIPMIX'] = dict(self.col_config_defaults, **{'title': 'Contamination S+A', 
               'description': 'VerifyBamID: CHIPMIX -   Sequence+array estimate of contamination (NA if the external genotype is unavailable)'})
            headers['CHIPLK1'] = {'title': 'CHIPLK1', 
               'description': 'Maximum log-likelihood of the sequence reads given estimated contamination under sequence+array method (NA if the external genotypes are unavailable)'}
            headers['CHIPLK0'] = {'title': 'CHIPLK0', 
               'description': ' Log-likelihood of the sequence reads given no contamination under sequence+array method (NA if the external genotypes are unavailable)'}
            headers['CHIP_RH'] = {'title': 'CHIP_RH', 
               'description': 'Estimated reference bias parameter Pr(refBase|HET) (when --chip-refBias or --chip-full is used)'}
            headers['CHIP_RA'] = {'title': 'CHIP_RA', 
               'description': 'Estimated reference bias parameter Pr(refBase|HOMALT) (when --chip-refBias or --chip-full is used)'}
        headers['DPREF'] = {'title': 'DPREF', 
           'description': 'Depth (Coverage) of HomRef site (based on the genotypes of (SELF_SM/BEST_SM), passing mapQ, baseQual, maxDepth thresholds.', 
           'hidden': all([ s['DPREF'] == 'NA' for s in self.verifybamid_data.values() ])}
        headers['RDPHET'] = {'title': 'RDPHET', 
           'description': 'DPHET/DPREF, Relative depth to HomRef site at Heterozygous site.', 
           'hidden': all([ s['RDPHET'] == 'NA' for s in self.verifybamid_data.values() ])}
        headers['RDPALT'] = {'title': 'RDPALT', 
           'description': 'DPHET/DPREF, Relative depth to HomRef site at HomAlt site.', 
           'hidden': all([ s['RDPALT'] == 'NA' for s in self.verifybamid_data.values() ])}
        tconfig = {'namespace': 'VerifyBAMID', 
           'id': 'verifybamid-results'}
        self.add_section(anchor='verifybamid-table', description='The following values provide estimates of sample contamination. Click help for more information.', helptext='\n\t\t\t**Please note that `FREEMIX` is named _Contamination (Seq)_ and `CHIPMIX`\n\t\t\tis named _Contamination (S+A)_ in this MultiQC report.**\n\n\t\t\tVerifyBamID provides a series of information that is informative to determine\n\t\t\twhether the sample is possibly contaminated or swapped, but there is no single\n\t\t\tcriteria that works for every circumstances. There are a few unmodeled factor\n\t\t\tin the estimation of `[SELF-IBD]/[BEST-IBD]` and `[%MIX]`, so please note that the\n\t\t\tMLE estimation may not always exactly match to the true amount of contamination.\n\t\t\tHere we provide a guideline to flag potentially contaminated/swapped samples:\n\n\t\t\t* Each sample or lane can be checked in this way.\n\t\t\t  When `[CHIPMIX] >> 0.02` and/or `[FREEMIX] >> 0.02`, meaning 2% or more of\n\t\t\t  non-reference bases are observed in reference sites, we recommend to examine\n\t\t\t  the data more carefully for the possibility of contamination.\n\t\t\t* We recommend to check each lane for the possibility of sample swaps.\n\t\t\t  When `[CHIPMIX] ~ 1` AND `[FREEMIX] ~ 0`, then it is possible that the sample\n\t\t\t  is swapped with another sample. When `[CHIPMIX] ~ 0` in `.bestSM` file,\n\t\t\t  `[CHIP_ID]` might be actually the swapped sample. Otherwise, the swapped\n\t\t\t  sample may not exist in the genotype data you have compared.\n\t\t\t* When genotype data is not available but allele-frequency-based estimates of\n\t\t\t  `[FREEMIX] >= 0.03` and `[FREELK1]-[FREELK0]` is large, then it is possible\n\t\t\t  that the sample is contaminated with other sample. We recommend to use\n\t\t\t  per-sample data rather than per-lane data for checking this for low coverage\n\t\t\t  data, because the inference will be more confident when there are large number\n\t\t\t  of bases with depth 2 or higher.\n\n\t\t\t_Copied from the [VerifyBAMID documentation](https://genome.sph.umich.edu/wiki/VerifyBamID) - see the link for more details._\n\t\t\t', plot=table.plot(self.verifybamid_data, headers, tconfig))