# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /share/data3/lianlin/soft/bin/wes/module-develop/bin/hgvs.py
# Compiled at: 2019-05-13 03:25:09


class AA_change(object):

    def __init__(self, value, variant_type):
        self.value = value
        self.variant_type = variant_type

    def std(self, match_transcript):
        gene = match_transcript[0]
        transcipt_number = match_transcript[1]
        cDNA = match_transcript[3]
        protein = match_transcript[4]
        if self.variant_type == 'snp':
            _ = cDNA.split('.')[1]
            ori = _[0]
            bed = _[1:-1]
            change = _[(-1)]
            cDNA = 'c.' + bed + ori + '>' + change
            match_transcript = transcipt_number + '(' + gene + ')' + ':' + cDNA + '(' + protein + ')'
        else:
            match_transcript = transcipt_number + '(' + gene + ')' + ':' + cDNA + '(' + protein + ')'
        return match_transcript

    def get_NM_min(self, value):
        _ = []
        for nm in value:
            transcipts = nm.split(':')
            number = transcipts[1].split('_')[1]
            pos = [ i for i, v in enumerate(number) if v != '0' ][0]
            _.append(float(number[pos:]))

        nm_pos = _.index(min(_))
        match_transcript = value[nm_pos]
        return match_transcript

    def std_AA(self):
        if self.value == '.' or self.value == 'UNKNOWN':
            match_transcript = '.'
        else:
            value = self.value.split('/')
            if len(value) == 1:
                match_transcript = value[0].split(':')
                match_transcript = self.std(match_transcript)
            else:
                match_transcript = self.get_NM_min(value).split(':')
                match_transcript = self.std(match_transcript)
        return match_transcript