# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/deeptools/plotCorrelation.py
# Compiled at: 2019-11-13 05:22:42
""" MultiQC submodule to parse output from deepTools plotCorrelation """
import logging
from multiqc.plots import heatmap
log = logging.getLogger(__name__)

class plotCorrelationMixin:

    def parse_plotCorrelation(self):
        """Find plotCorrelation output"""
        self.deeptools_plotCorrelationData = dict()
        for f in self.find_log_files('deeptools/plotCorrelationData', filehandles=False):
            parsed_data, samples = self.parsePlotCorrelationData(f)
            for k, v in parsed_data.items():
                if k in self.deeptools_plotCorrelationData:
                    log.warning(('Replacing duplicate sample {}.').format(k))
                self.deeptools_plotCorrelationData[k] = v

            if len(parsed_data) > 0:
                self.add_data_source(f, section='plotCorrelation')

        if len(self.deeptools_plotCorrelationData) > 0:
            config = {'id': 'deeptools_correlation_plot', 'title': 'deeptools: Correlation Plot'}
            data = []
            for s_name in samples:
                try:
                    data.append(self.deeptools_plotCorrelationData[s_name])
                except KeyError:
                    pass

            if len(data) == 0:
                log.debug('No valid data for correlation plot')
                return None
            self.add_section(name='Correlation heatmap', anchor='deeptools_correlation', description='Pairwise correlations of samples based on distribution of sequence reads', plot=heatmap.plot(data, samples, samples, config))
        return len(self.deeptools_plotCorrelationData)

    def parsePlotCorrelationData(self, f):
        d = dict()
        samples = []
        for line in f['f'].splitlines():
            cols = line.split('\t')
            if cols[0] == '#plotCorrelation --outFileCorMatrix':
                continue
            elif cols[0] == '':
                continue
            else:
                c = str(cols[0]).strip("'")
                s_name = self.clean_s_name(c, f['root'])
                samples.append(s_name)
                d[s_name] = []
                for c in cols[1:len(cols)]:
                    d[s_name].append(float(c))

        return (
         d, samples)