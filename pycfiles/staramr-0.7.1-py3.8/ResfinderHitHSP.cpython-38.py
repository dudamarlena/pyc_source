# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/blast/results/resfinder/ResfinderHitHSP.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 1893 bytes
import logging, re
import staramr.blast.results.AMRHitHSP as AMRHitHSP
logger = logging.getLogger('ResfinderHitHSP')

class ResfinderHitHSP(AMRHitHSP):

    def __init__(self, file, blast_record):
        super().__init__(file, blast_record)
        logger.debug('record=%s', self._blast_record)
        re_search = re.search('^([^_]+)_([^_]+)_(\\S+)', self.get_amr_gene_id())
        if not re_search:
            raise Exception('Could not split up seq name for [' + self.get_amr_gene_id() + ']')
        self._gene = re_search.group(1)
        self._gene_variant = re_search.group(2)
        self._accession = re_search.group(3)

    def get_amr_gene_name(self):
        """
        Gets the gene name for the ResFinder hit.
        :return: The gene name.
        """
        return self._gene

    def get_amr_gene_name_with_variant(self):
        """
        Gets the gene name + variant number for the ResFinder hit.
        :return: The gene name + variant number.
        """
        return self.get_amr_gene_name() + '_' + self._gene_variant

    def get_amr_gene_variant_accession(self):
        """
        Gets the gene name + variant number + accession for the ResFinder hit.
        :return: The gene name + variant number + accession.
        """
        return self.get_amr_gene_name() + '_' + self._gene_variant + '_' + self._accession

    def get_amr_gene_accession(self):
        """
        Gets the accession for the ResFinder hit.
        :return: The accession.
        """
        return self._accession