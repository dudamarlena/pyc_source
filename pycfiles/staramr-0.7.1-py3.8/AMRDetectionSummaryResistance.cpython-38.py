# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/results/AMRDetectionSummaryResistance.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 2828 bytes
from collections import OrderedDict
import staramr.results.AMRDetectionSummary as AMRDetectionSummary

class AMRDetectionSummaryResistance(AMRDetectionSummary):

    def __init__(self, files, resfinder_dataframe, quality_module_dataframe, pointfinder_dataframe=None, plasmidfinder_dataframe=None, mlst_dataframe=None):
        """
        Creates a new AMRDetectionSummaryResistance.
        :param files: The list of genome files we have scanned against.
        :param resfinder_dataframe: The pd.DataFrame containing the ResFinder results.
        :param quality_module_dataframe: The pd.DataFrame containing the genome size, N50 value, number of contigs under our user defined minimum length
        as well as the results of our quality metrics (pass or fail) and the corresponding feedback
        :param pointfinder_dataframe: The pd.DataFrame containing the PointFinder results.
        :param plasmidfinder_dataframe: The pd.DataFrame containing the PlasmidFinder results.
        """
        super().__init__(files, resfinder_dataframe, quality_module_dataframe, pointfinder_dataframe, plasmidfinder_dataframe, mlst_dataframe)

    def _aggregate_gene_phenotype(self, dataframe):
        flattened_phenotype_list = [y.strip() for x in dataframe['Predicted Phenotype'].tolist() for y in x.split(self.SEPARATOR)]
        uniq_phenotype = OrderedDict.fromkeys(flattened_phenotype_list)
        return {'Gene':(self.SEPARATOR + ' ').join(dataframe['Gene']), 
         'Predicted Phenotype':(self.SEPARATOR + ' ').join(list(uniq_phenotype))}

    def _compile_results(self, df):
        df_summary = df.copy()
        df_summary['Gene.Lower'] = df['Gene'].str.lower()
        df_summary = df_summary.sort_values(by=[
         'Gene.Lower']).groupby([
         'Isolate ID'],
          sort=True).aggregate(self._aggregate_gene_phenotype)
        return df_summary[['Gene', 'Predicted Phenotype']]

    def _get_detailed_negative_columns(self):
        return [
         'Isolate ID', 'Gene', 'Predicted Phenotype', 'Start', 'End']

    def _get_summary_empty_values(self):
        return {'Genotype':'None', 
         'Predicted Phenotype':'Sensitive'}

    def _get_summary_resistance_columns(self):
        return [
         'Genotype', 'Predicted Phenotype', 'Plasmid']

    def _get_detailed_summary_columns(self):
        return [
         'Gene', 'Data Type', 'Predicted Phenotype', '%Identity', '%Overlap', 'HSP Length/Total Length', 'Contig', 'Start',
         'End', 'Accession']

    def _include_phenotype(self):
        return True