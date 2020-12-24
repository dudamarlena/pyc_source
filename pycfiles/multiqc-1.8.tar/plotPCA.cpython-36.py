# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/deeptools/plotPCA.py
# Compiled at: 2019-11-15 09:30:51
# Size of source mod 2**32: 2586 bytes
""" MultiQC submodule to parse output from deepTools plotPCA """
import logging
from multiqc.plots import scatter
log = logging.getLogger(__name__)

class plotPCAMixin:

    def parse_plotPCA(self):
        """Find plotPCA output"""
        self.deeptools_plotPCAData = dict()
        for f in self.find_log_files('deeptools/plotPCAData', filehandles=False):
            parsed_data = self.parsePlotPCAData(f)
            for k, v in parsed_data.items():
                if k in self.deeptools_plotPCAData:
                    log.warning('Replacing duplicate sample {}.'.format(k))
                self.deeptools_plotPCAData[k] = v

            if len(parsed_data) > 0:
                self.add_data_source(f, section='plotPCA')

        if len(self.deeptools_plotPCAData) > 0:
            config = {'id':'deeptools_pca_plot',  'title':'deeptools: PCA Plot', 
             'xlab':'PC1', 
             'ylab':'PC2', 
             'tt_label':'PC1 {point.x:.2f}: PC2 {point.y:.2f}'}
            data = dict()
            for s_name in self.deeptools_plotPCAData:
                try:
                    data[s_name] = {'x':self.deeptools_plotPCAData[s_name][1], 
                     'y':self.deeptools_plotPCAData[s_name][2]}
                except KeyError:
                    pass

            if len(data) == 0:
                log.debug('No valid data for PCA plot')
                return
            self.add_section(name='PCA plot',
              anchor='deeptools_pca',
              description='PCA plot with the top two principal components calculated based on genome-wide distribution of sequence reads',
              plot=(scatter.plot(data, config)))
        return len(self.deeptools_plotPCAData)

    def parsePlotPCAData(self, f):
        d = dict()
        samples = []
        for line in f['f'].splitlines():
            cols = line.strip().split('\t')
            if cols[0] == '#plotPCA --outFileNameData':
                continue
            elif cols[0] == 'Component':
                for c in cols[1:len(cols) - 1]:
                    c = str(c).strip("'")
                    s_name = self.clean_s_name(c, f['root'])
                    d[s_name] = {}
                    samples.append(s_name)

            else:
                idx = 0
                compo = cols[0]
                for c in cols[1:len(cols) - 1]:
                    d[samples[idx]][self._int(compo)] = float(c)
                    idx += 1

        return d