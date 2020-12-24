# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/vcftools/relatedness2.py
# Compiled at: 2017-12-07 11:58:18
# Size of source mod 2**32: 2780 bytes
""" MultiQC module to parse relatedness output from vcftools relatedness """
import csv, logging
from collections import defaultdict
from multiqc.plots import heatmap
log = logging.getLogger(__name__)

class Relatedness2Mixin:

    def parse_relatedness2(self):
        matrices = {}
        for f in self.find_log_files('vcftools/relatedness2', filehandles=True):
            m = _Relatedness2Matrix(f)
            if m.data and m.x_labels and m.y_labels:
                matrices[f['s_name']] = m

        matrices = self.ignore_samples(matrices)
        if len(matrices) == 0:
            return 0
        log.info('Found {} valid relatedness2 matrices'.format(len(matrices)))
        helptext = '\n        `RELATEDNESS_PHI` gives a relatedness score between two samples. A higher score indicates a higher degree of\n        relatedness, up to a maximum of 0.5. Samples are sorted alphabetically on each axis, and specific IDs can be\n        found in the graph with the Highlight tab.\n        '
        idx = 0
        for name, m in matrices.items():
            idx += 1
            self.add_section(name='Relatedness2',
              anchor=('vcftools-relatedness2-{}'.format(idx)),
              description=('**Input:** `{}`.\n\n Heatmap of `RELATEDNESS_PHI` values from the output of vcftools relatedness2.'.format(name)),
              helptext=helptext,
              plot=heatmap.plot((m.data),
              xcats=(m.x_labels),
              ycats=(m.y_labels),
              pconfig={'id':'vcftools-relatedness2-heatmap-{}'.format(idx), 
             'title':'VCFTools: Relatedness2', 
             'square':True, 
             'decimalPlaces':7}))

        return len(matrices)


class _Relatedness2Matrix:

    def __init__(self, relatedness_file):
        self.data = []
        self.x_labels = set()
        self.y_labels = set()
        self.parse(relatedness_file['f'])

    def parse(self, f):
        rels = defaultdict(dict)
        r = csv.DictReader(f, delimiter='\t')
        for line in r:
            self.x_labels.add(line['INDV1'])
            self.y_labels.add(line['INDV2'])
            rels[line['INDV1']][line['INDV2']] = float(line['RELATEDNESS_PHI'])

        self.x_labels = sorted(self.x_labels)
        self.y_labels = sorted(self.y_labels)
        for x in self.x_labels:
            line = []
            for y in self.y_labels:
                line.append(rels[x][y])

            self.data.append(line)