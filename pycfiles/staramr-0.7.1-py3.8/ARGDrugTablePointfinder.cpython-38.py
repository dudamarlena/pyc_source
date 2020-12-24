# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/databases/resistance/pointfinder/ARGDrugTablePointfinder.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 1489 bytes
import logging
from os import path
import staramr.databases.resistance.ARGDrugTable as ARGDrugTable
logger = logging.getLogger('ARGDrugTablePointfinder')

class ARGDrugTablePointfinder(ARGDrugTable):
    DEFAULT_FILE = path.join(ARGDrugTable.DEFAULT_DATA_DIR, 'ARG_drug_key_pointfinder.tsv')

    def __init__(self, file=DEFAULT_FILE):
        """
        Builds a new ARGDrugTablePointfinder from the given file.
        :param file: The file containing the gene/drug mappings.
        """
        super().__init__(file=file)

    def get_drug(self, organism, gene, position):
        """
        Gets the drug given the organism, gene, and position of point mutation.
        :param organism: The organism.
        :param gene: The gene.
        :param position: The position of the point mutation (may be codon position or nucleotide position depending on gene).
        :return: The drug this mutation causes resistance to, or None if no such drug.
        """
        table = self._data
        drug = table[((table['Organism'] == organism) & (table['Gene'] == gene) & (table['Codon Pos.'] == position))]['Drug']
        if drug.empty:
            logger.warning('No drug found for organism=%s, gene=%s, position=%s', organism, gene, position)
            return None
        return self._drug_string_to_correct_separators(drug.iloc[0])