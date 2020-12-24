# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/databases/resistance/resfinder/ARGDrugTableResfinder.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 1611 bytes
import logging
from os import path
import staramr.databases.resistance.ARGDrugTable as ARGDrugTable
logger = logging.getLogger('ARGDrugTableResfinder')

class ARGDrugTableResfinder(ARGDrugTable):
    DEFAULT_FILE = path.join(ARGDrugTable.DEFAULT_DATA_DIR, 'ARG_drug_key_resfinder.tsv')

    def __init__(self, file=DEFAULT_FILE):
        """
        Builds a new ARGDrugTableResfinder from the given file.
        :param file: The file containing the gene/drug mappings.
        """
        super().__init__(file=file)

    def get_drug(self, drug_class, gene_plus_variant, accession):
        """
        Gets the drug given the drug class, gene (plus variant of gene encoded in ResFinder database) and accession.
        :param drug_class: The drug class.
        :param gene_plus_variant: The gene plus variant (e.g., {gene}_{variant} = {blaIMP-58}_{1}).
        :param accession: The accession in the resfinder database (e.g., KU647281).
        :return: The particular drug, or None if no matching drug was found.
        """
        table = self._data
        drug = table[((table['Class'] == drug_class) & (table['Gene'] == gene_plus_variant) & (table['Accession'] == accession))]['Drug']
        if drug.empty:
            logger.warning('No drug found for drug_class=%s, gene=%s, accession=%s', drug_class, gene_plus_variant, accession)
            return None
        return self._drug_string_to_correct_separators(drug.iloc[0])