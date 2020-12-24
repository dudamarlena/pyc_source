# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /share/data3/lianlin/soft/bin/wes/module-develop/bin/annotation_filter.py
# Compiled at: 2019-05-13 03:25:09


class Filter(object):

    def __init__(self, info_dict):
        self.info_dict = info_dict

    def filter_arg(self):
        clinvar = self.info_dict['CLINSIG'].split('|')
        clinvar = list(set(clinvar))
        freq1 = self.info_dict['gnomAD_exome_EAS']
        freq2 = self.info_dict['ExAC_EAS']
        Func_refGene = self.info_dict['Func.refGene']
        if self.clinvar_filter(clinvar):
            return True
        else:
            if self.Pathogenic(clinvar):
                return False
            if self.population_freq(freq1, freq2):
                return True
            if self.Func(Func_refGene):
                return True
            return False

    def clinvar_filter(self, clinvar):
        """other|Benign"""
        length = len(clinvar)
        if length == 1 and (clinvar[0] == 'Benign' or clinvar[0] == 'Likely_benign'):
            return True
        if length == 2 and (clinvar[0] == 'Benign' or clinvar[1] == 'Likely_benign' or clinvar[0] == 'Likely_benign' or clinvar[1] == 'Benign'):
            return True
        False

    def Pathogenic(self, clinvar):
        for _, x in enumerate(clinvar):
            if x.find('Pathogenic') != -1:
                return True
            else:
                return False

    def population_freq(self, freq1, freq2):
        if freq1 == '.':
            freq1 = 0
        if freq2 == '.':
            freq2 = 0
        freq = max(float(freq1), float(freq2))
        if freq < 0.01:
            return False
        else:
            return True

    def Func(self, Func_refGene):
        if Func_refGene == 'UTR3' or Func_refGene == 'UTR5' or Func_refGene == 'ncRNA':
            return True
        return False