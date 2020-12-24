# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/picard/OxoGMetrics.py
# Compiled at: 2019-07-03 11:21:10
""" MultiQC submodule to parse output from Picard OxoGMetrics """
import logging, os, re
log = logging.getLogger(__name__)

def parse_reports(self):
    """ Find Picard OxoGMetrics reports and parse their data """
    self.picard_OxoGMetrics_data = dict()
    for f in self.find_log_files('picard/oxogmetrics', filehandles=True):
        parsed_data = list()
        sample_names = list()
        s_files = list()
        s_name = None
        keys = None
        for l in f['f']:
            if ('CollectOxoGMetrics' in l or 'ConvertSequencingArtifactToOxoG' in l) and 'INPUT' in l:
                s_name = None
                keys = None
                context_col = None
                fn_search = re.search('INPUT(?:=|\\s+)(\\[?[^\\s]+\\]?)', l, flags=re.IGNORECASE)
                if fn_search:
                    s_name = os.path.basename(fn_search.group(1).strip('[]'))
                    s_name = self.clean_s_name(s_name, f['root'])
                    parsed_data.append(dict())
                    sample_names.append(s_name)
                    s_files.append(f)
            if s_name is not None:
                if 'CollectOxoGMetrics$CpcgMetrics' in l and '## METRICS CLASS' in l:
                    keys = f['f'].readline().strip('\n').split('\t')
                    context_col = keys.index('CONTEXT')
                elif keys:
                    vals = l.strip('\n').split('\t')
                    if len(vals) == len(keys) and context_col is not None:
                        context = vals[context_col]
                        parsed_data[(-1)][context] = dict()
                        for i, k in enumerate(keys):
                            k = k.strip()
                            try:
                                parsed_data[(-1)][context][k] = float(vals[i])
                            except ValueError:
                                vals[i] = vals[i].strip()
                                parsed_data[(-1)][context][k] = vals[i]

                    else:
                        s_name = None
                        keys = None

        for idx, s_name in enumerate(sample_names):
            if len(parsed_data[idx]) > 0:
                if s_name in self.picard_OxoGMetrics_data:
                    log.debug(('Duplicate sample name found in {}! Overwriting: {}').format(s_files[idx], s_name))
                self.add_data_source(s_files[idx], s_name, section='OxoGMetrics')
                self.picard_OxoGMetrics_data[s_name] = parsed_data[idx]

    self.picard_OxoGMetrics_data = self.ignore_samples(self.picard_OxoGMetrics_data)
    if len(self.picard_OxoGMetrics_data) > 0:
        print_data = {('{}_{}').format(s, c):v for s in self.picard_OxoGMetrics_data.keys() for c, v in self.picard_OxoGMetrics_data[s].items()}
        self.write_data_file(print_data, 'multiqc_picard_OxoGMetrics')
        data = dict()
        for s_name in self.picard_OxoGMetrics_data:
            data[s_name] = dict()
            try:
                data[s_name]['CCG_OXIDATION_ERROR_RATE'] = self.picard_OxoGMetrics_data[s_name]['CCG']['OXIDATION_ERROR_RATE']
            except KeyError:
                log.warn(("Couldn't find picard CCG oxidation error rate for {}").format(s_name))

        self.general_stats_headers['CCG_OXIDATION_ERROR_RATE'] = {'title': 'CCG Oxidation', 'description': 'CCG-CAG Oxidation Error Rate', 
           'max': 1, 
           'min': 0, 
           'suffix': '%', 
           'format': '{:,.0f}', 
           'scale': 'RdYlGn-rev', 
           'modify': lambda x: self.multiply_hundred(x)}
        for s_name in data:
            if s_name not in self.general_stats_data:
                self.general_stats_data[s_name] = dict()
            self.general_stats_data[s_name].update(data[s_name])

    return len(self.picard_OxoGMetrics_data)