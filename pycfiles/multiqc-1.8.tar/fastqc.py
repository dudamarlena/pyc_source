# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/fastqc/fastqc.py
# Compiled at: 2019-11-20 10:26:16
""" MultiQC module to parse output from FastQC
"""
from __future__ import print_function
from collections import OrderedDict
import io, json, logging, os, re, zipfile
from multiqc import config
from multiqc.plots import linegraph, bargraph, heatmap
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc.utils import report
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='FastQC', anchor='fastqc', href='http://www.bioinformatics.babraham.ac.uk/projects/fastqc/', info='is a quality control tool for high throughput sequence data, written by Simon Andrews at the Babraham Institute in Cambridge.')
        self.fastqc_data = dict()
        for f in self.find_log_files('fastqc/data'):
            s_name = self.clean_s_name(os.path.basename(f['root']), os.path.dirname(f['root']))
            self.parse_fastqc_report(f['f'], s_name, f)

        for f in self.find_log_files('fastqc/zip', filecontents=False):
            s_name = f['fn']
            if s_name.endswith('_fastqc.zip'):
                s_name = s_name[:-11]
            if s_name in self.fastqc_data.keys():
                log.debug(("Skipping '{}' as already parsed '{}'").format(f['fn'], s_name))
                continue
            try:
                fqc_zip = zipfile.ZipFile(os.path.join(f['root'], f['fn']))
            except Exception as e:
                log.warn(("Couldn't read '{}' - Bad zip file").format(f['fn']))
                log.debug(('Bad zip file error:\n{}').format(e))
                continue

            d_name = fqc_zip.namelist()[0]
            try:
                with fqc_zip.open(os.path.join(d_name, 'fastqc_data.txt')) as (fh):
                    r_data = fh.read().decode('utf8')
                    self.parse_fastqc_report(r_data, s_name, f)
            except KeyError:
                log.warning(("Error - can't find fastqc_raw_data.txt in {}").format(f))

        self.fastqc_data = self.ignore_samples(self.fastqc_data)
        if len(self.fastqc_data) == 0:
            raise UserWarning
        log.info(('Found {} reports').format(len(self.fastqc_data)))
        data = dict()
        for s_name in self.fastqc_data:
            data[s_name] = self.fastqc_data[s_name]['basic_statistics']
            data[s_name].update(self.fastqc_data[s_name]['statuses'])

        self.write_data_file(data, 'multiqc_fastqc')
        self.css = {'assets/css/multiqc_fastqc.css': os.path.join(os.path.dirname(__file__), 'assets', 'css', 'multiqc_fastqc.css')}
        self.js = {'assets/js/multiqc_fastqc.js': os.path.join(os.path.dirname(__file__), 'assets', 'js', 'multiqc_fastqc.js')}
        self.status_colours = {'pass': '#5cb85c', 'warn': '#f0ad4e', 'fail': '#d9534f', 'default': '#999'}
        self.fastqc_general_stats()
        statuses = dict()
        for s_name in self.fastqc_data:
            for section, status in self.fastqc_data[s_name]['statuses'].items():
                try:
                    statuses[section][s_name] = status
                except KeyError:
                    statuses[section] = {s_name: status}

        self.intro += ('<script type="application/json" class="fastqc_passfails">{}</script>').format(json.dumps([self.anchor.replace('-', '_'), statuses]))
        self.intro += '<script type="text/javascript">load_fastqc_passfails();</script>'
        self.read_count_plot()
        self.sequence_quality_plot()
        self.per_seq_quality_plot()
        self.sequence_content_plot()
        self.gc_content_plot()
        self.n_content_plot()
        self.seq_length_dist_plot()
        self.seq_dup_levels_plot()
        self.overrepresented_sequences()
        self.adapter_content_plot()
        self.status_heatmap()

    def parse_fastqc_report(self, file_contents, s_name=None, f=None):
        """ Takes contents from a fastq_data.txt file and parses out required
        statistics and data. Returns a dict with keys 'stats' and 'data'.
        Data is for plotting graphs, stats are for top table. """
        fn_search = re.search('Filename\\s+(.+)', file_contents)
        if fn_search:
            s_name = self.clean_s_name(fn_search.group(1), f['root'])
        if s_name in self.fastqc_data.keys():
            log.debug(('Duplicate sample name found! Overwriting: {}').format(s_name))
        self.add_data_source(f, s_name)
        self.fastqc_data[s_name] = {'statuses': dict()}
        section = None
        s_headers = None
        self.dup_keys = []
        for l in file_contents.splitlines():
            if l == '>>END_MODULE':
                section = None
                s_headers = None
            elif l.startswith('>>'):
                section, status = l[2:].split('\t', 1)
                section = section.lower().replace(' ', '_')
                self.fastqc_data[s_name]['statuses'][section] = status
            elif section is not None:
                if l.startswith('#'):
                    s_headers = l[1:].split('\t')
                    if s_headers[0] == 'Total Deduplicated Percentage':
                        self.fastqc_data[s_name]['basic_statistics'].append({'measure': 'total_deduplicated_percentage', 
                           'value': float(s_headers[1])})
                    else:
                        if s_headers[1] == 'Relative count':
                            s_headers[1] = 'Percentage of total'
                        s_headers = [ s.lower().replace(' ', '_') for s in s_headers ]
                        self.fastqc_data[s_name][section] = list()
                elif s_headers is not None:
                    s = l.split('\t')
                    row = dict()
                    for i, v in enumerate(s):
                        v.replace('NaN', '0')
                        try:
                            v = float(v)
                        except ValueError:
                            pass

                        row[s_headers[i]] = v

                    self.fastqc_data[s_name][section].append(row)
                    if section == 'sequence_duplication_levels':
                        try:
                            self.dup_keys.append(float(s[0]))
                        except ValueError:
                            self.dup_keys.append(s[0])

        self.fastqc_data[s_name]['basic_statistics'] = {d['measure']:d['value'] for d in self.fastqc_data[s_name]['basic_statistics']}
        length_bp = 0
        total_count = 0
        for d in self.fastqc_data[s_name].get('sequence_length_distribution', {}):
            length_bp += d['count'] * self.avg_bp_from_range(d['length'])
            total_count += d['count']

        if total_count > 0:
            self.fastqc_data[s_name]['basic_statistics']['avg_sequence_length'] = length_bp / total_count
        return

    def fastqc_general_stats(self):
        """ Add some single-number stats to the basic statistics
        table at the top of the report """
        data = dict()
        for s_name in self.fastqc_data:
            bs = self.fastqc_data[s_name]['basic_statistics']
            data[s_name] = {'percent_gc': bs['%GC'], 
               'avg_sequence_length': bs['avg_sequence_length'], 
               'total_sequences': bs['Total Sequences']}
            try:
                data[s_name]['percent_duplicates'] = 100 - bs['total_deduplicated_percentage']
            except KeyError:
                pass

            num_statuses = 0
            num_fails = 0
            for s in self.fastqc_data[s_name]['statuses'].values():
                num_statuses += 1
                if s == 'fail':
                    num_fails += 1

            data[s_name]['percent_fails'] = float(num_fails) / float(num_statuses) * 100.0

        seq_lengths = [ x['avg_sequence_length'] for x in data.values() ]
        hide_seq_length = False if max(seq_lengths) - min(seq_lengths) > 10 else True
        headers = OrderedDict()
        headers['percent_duplicates'] = {'title': '% Dups', 
           'description': '% Duplicate Reads', 
           'max': 100, 
           'min': 0, 
           'suffix': '%', 
           'scale': 'RdYlGn-rev'}
        headers['percent_gc'] = {'title': '% GC', 
           'description': 'Average % GC Content', 
           'max': 100, 
           'min': 0, 
           'suffix': '%', 
           'scale': 'Set1', 
           'format': '{:,.0f}'}
        headers['avg_sequence_length'] = {'title': 'Length', 
           'description': 'Average Sequence Length (bp)', 
           'min': 0, 
           'suffix': ' bp', 
           'scale': 'RdYlGn', 
           'format': '{:,.0f}', 
           'hidden': hide_seq_length}
        headers['percent_fails'] = {'title': '% Failed', 
           'description': 'Percentage of modules failed in FastQC report (includes those not plotted here)', 
           'max': 100, 
           'min': 0, 
           'suffix': '%', 
           'scale': 'Reds', 
           'format': '{:,.0f}', 
           'hidden': True}
        headers['total_sequences'] = {'title': ('{} Seqs').format(config.read_count_prefix), 
           'description': ('Total Sequences ({})').format(config.read_count_desc), 
           'min': 0, 
           'scale': 'Blues', 
           'modify': lambda x: x * config.read_count_multiplier, 
           'shared_key': 'read_count'}
        self.general_stats_addcols(data, headers)

    def read_count_plot(self):
        """ Stacked bar plot showing counts of reads """
        pconfig = {'id': 'fastqc_sequence_counts_plot', 
           'title': 'FastQC: Sequence Counts', 
           'ylab': 'Number of reads', 
           'cpswitch_counts_label': 'Number of reads', 
           'hide_zero_cats': False}
        pdata = dict()
        has_dups = False
        has_total = False
        for s_name in self.fastqc_data:
            pd = self.fastqc_data[s_name]['basic_statistics']
            pdata[s_name] = dict()
            try:
                pdata[s_name]['Duplicate Reads'] = int((100.0 - float(pd['total_deduplicated_percentage'])) / 100.0 * pd['Total Sequences'])
                pdata[s_name]['Unique Reads'] = pd['Total Sequences'] - pdata[s_name]['Duplicate Reads']
                has_dups = True
            except KeyError:
                pdata[s_name] = {'Total Sequences': pd['Total Sequences']}
                has_total = True

        pcats = list()
        duptext = ''
        if has_total:
            pcats.append('Total Sequences')
        if has_dups:
            pcats.extend(['Unique Reads', 'Duplicate Reads'])
            duptext = ' Duplicate read counts are an estimate only.'
        if has_total and not has_dups:
            pconfig['use_legend'] = False
            pconfig['cpswitch'] = False
        self.add_section(name='Sequence Counts', anchor='fastqc_sequence_counts', description='Sequence counts for each sample.' + duptext, helptext='\n            This plot show the total number of reads, broken down into unique and duplicate\n            if possible (only more recent versions of FastQC give duplicate info).\n\n            You can read more about duplicate calculation in the\n            [FastQC documentation](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/8%20Duplicate%20Sequences.html).\n            A small part has been copied here for convenience:\n\n            _Only sequences which first appear in the first 100,000 sequences\n            in each file are analysed. This should be enough to get a good impression\n            for the duplication levels in the whole file. Each sequence is tracked to\n            the end of the file to give a representative count of the overall duplication level._\n\n            _The duplication detection requires an exact sequence match over the whole length of\n            the sequence. Any reads over 75bp in length are truncated to 50bp for this analysis._\n            ', plot=bargraph.plot(pdata, pcats, pconfig))

    def sequence_quality_plot(self):
        """ Create the HTML for the phred quality score plot """
        data = dict()
        for s_name in self.fastqc_data:
            try:
                data[s_name] = {self.avg_bp_from_range(d['base']):d['mean'] for d in self.fastqc_data[s_name]['per_base_sequence_quality']}
            except KeyError:
                pass

        if len(data) == 0:
            log.debug('sequence_quality not found in FastQC reports')
            return
        else:
            pconfig = {'id': 'fastqc_per_base_sequence_quality_plot', 'title': 'FastQC: Mean Quality Scores', 
               'ylab': 'Phred Score', 
               'xlab': 'Position (bp)', 
               'ymin': 0, 
               'xDecimals': False, 
               'tt_label': '<b>Base {point.x}</b>: {point.y:.2f}', 
               'colors': self.get_status_cols('per_base_sequence_quality'), 
               'yPlotBands': [{'from': 28, 'to': 100, 'color': '#c3e6c3'}, {'from': 20, 'to': 28, 'color': '#e6dcc3'}, {'from': 0, 'to': 20, 'color': '#e6c3c3'}]}
            self.add_section(name='Sequence Quality Histograms', anchor='fastqc_per_base_sequence_quality', description='The mean quality value across each base position in the read.', helptext='\n            To enable multiple samples to be plotted on the same graph, only the mean quality\n            scores are plotted (unlike the box plots seen in FastQC reports).\n\n            Taken from the [FastQC help](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/2%20Per%20Base%20Sequence%20Quality.html):\n\n            _The y-axis on the graph shows the quality scores. The higher the score, the better\n            the base call. The background of the graph divides the y axis into very good quality\n            calls (green), calls of reasonable quality (orange), and calls of poor quality (red).\n            The quality of calls on most platforms will degrade as the run progresses, so it is\n            common to see base calls falling into the orange area towards the end of a read._\n            ', plot=linegraph.plot(data, pconfig))
            return

    def per_seq_quality_plot(self):
        """ Create the HTML for the per sequence quality score plot """
        data = dict()
        for s_name in self.fastqc_data:
            try:
                data[s_name] = {d['quality']:d['count'] for d in self.fastqc_data[s_name]['per_sequence_quality_scores']}
            except KeyError:
                pass

        if len(data) == 0:
            log.debug('per_seq_quality not found in FastQC reports')
            return
        else:
            pconfig = {'id': 'fastqc_per_sequence_quality_scores_plot', 'title': 'FastQC: Per Sequence Quality Scores', 
               'ylab': 'Count', 
               'xlab': 'Mean Sequence Quality (Phred Score)', 
               'ymin': 0, 
               'xmin': 0, 
               'xDecimals': False, 
               'colors': self.get_status_cols('per_sequence_quality_scores'), 
               'tt_label': '<b>Phred {point.x}</b>: {point.y} reads', 
               'xPlotBands': [{'from': 28, 'to': 100, 'color': '#c3e6c3'}, {'from': 20, 'to': 28, 'color': '#e6dcc3'}, {'from': 0, 'to': 20, 'color': '#e6c3c3'}]}
            self.add_section(name='Per Sequence Quality Scores', anchor='fastqc_per_sequence_quality_scores', description='The number of reads with average quality scores. Shows if a subset of reads has poor quality.', helptext='\n            From the [FastQC help](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/3%20Per%20Sequence%20Quality%20Scores.html):\n\n            _The per sequence quality score report allows you to see if a subset of your\n            sequences have universally low quality values. It is often the case that a\n            subset of sequences will have universally poor quality, however these should\n            represent only a small percentage of the total sequences._\n            ', plot=linegraph.plot(data, pconfig))
            return

    def sequence_content_plot(self):
        """ Create the epic HTML for the FastQC sequence content heatmap """
        data = OrderedDict()
        for s_name in sorted(self.fastqc_data.keys()):
            try:
                data[s_name] = {self.avg_bp_from_range(d['base']):d for d in self.fastqc_data[s_name]['per_base_sequence_content']}
            except KeyError:
                pass

            for b in data[s_name]:
                tot = sum([ data[s_name][b][base] for base in ['a', 'c', 't', 'g'] ])
                if tot == 100.0:
                    break
                else:
                    for base in ['a', 'c', 't', 'g']:
                        data[s_name][b][base] = float(data[s_name][b][base]) / float(tot) * 100.0

        if len(data) == 0:
            log.debug('sequence_content not found in FastQC reports')
            return
        else:
            html = ('<div id="fastqc_per_base_sequence_content_plot_div">\n            <div class="alert alert-info">\n               <span class="glyphicon glyphicon-hand-up"></span>\n               Click a sample row to see a line plot for that dataset.\n            </div>\n            <h5><span class="s_name text-primary"><span class="glyphicon glyphicon-info-sign"></span> Rollover for sample name</span></h5>\n            <button id="fastqc_per_base_sequence_content_export_btn"><span class="glyphicon glyphicon-download-alt"></span> Export Plot</button>\n            <div class="fastqc_seq_heatmap_key">\n                Position: <span id="fastqc_seq_heatmap_key_pos">-</span>\n                <div><span id="fastqc_seq_heatmap_key_t"> %T: <span>-</span></span></div>\n                <div><span id="fastqc_seq_heatmap_key_c"> %C: <span>-</span></span></div>\n                <div><span id="fastqc_seq_heatmap_key_a"> %A: <span>-</span></span></div>\n                <div><span id="fastqc_seq_heatmap_key_g"> %G: <span>-</span></span></div>\n            </div>\n            <div id="fastqc_seq_heatmap_div" class="fastqc-overlay-plot">\n                <div id="{id}" class="fastqc_per_base_sequence_content_plot hc-plot has-custom-export">\n                    <canvas id="fastqc_seq_heatmap" height="100%" width="800px" style="width:100%;"></canvas>\n                </div>\n            </div>\n            <div class="clearfix"></div>\n        </div>\n        <script type="application/json" class="fastqc_seq_content">{d}</script>\n        ').format(id=report.save_htmlid('fastqc_per_base_sequence_content_plot'), d=json.dumps([self.anchor.replace('-', '_'), data]))
            self.add_section(name='Per Base Sequence Content', anchor='fastqc_per_base_sequence_content', description='The proportion of each base position for which each of the four normal DNA bases has been called.', helptext="\n            To enable multiple samples to be shown in a single plot, the base composition data\n            is shown as a heatmap. The colours represent the balance between the four bases:\n            an even distribution should give an even muddy brown colour. Hover over the plot\n            to see the percentage of the four bases under the cursor.\n\n            **To see the data as a line plot, as in the original FastQC graph, click on a sample track.**\n\n            From the [FastQC help](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/4%20Per%20Base%20Sequence%20Content.html):\n\n            _Per Base Sequence Content plots out the proportion of each base position in a\n            file for which each of the four normal DNA bases has been called._\n\n            _In a random library you would expect that there would be little to no difference\n            between the different bases of a sequence run, so the lines in this plot should\n            run parallel with each other. The relative amount of each base should reflect\n            the overall amount of these bases in your genome, but in any case they should\n            not be hugely imbalanced from each other._\n\n            _It's worth noting that some types of library will always produce biased sequence\n            composition, normally at the start of the read. Libraries produced by priming\n            using random hexamers (including nearly all RNA-Seq libraries) and those which\n            were fragmented using transposases inherit an intrinsic bias in the positions\n            at which reads start. This bias does not concern an absolute sequence, but instead\n            provides enrichement of a number of different K-mers at the 5' end of the reads.\n            Whilst this is a true technical bias, it isn't something which can be corrected\n            by trimming and in most cases doesn't seem to adversely affect the downstream\n            analysis._\n            ", content=html)
            return

    def gc_content_plot(self):
        """ Create the HTML for the FastQC GC content plot """
        data = dict()
        data_norm = dict()
        for s_name in self.fastqc_data:
            try:
                data[s_name] = {d['gc_content']:d['count'] for d in self.fastqc_data[s_name]['per_sequence_gc_content']}
            except KeyError:
                pass

            data_norm[s_name] = dict()
            total = sum([ c for c in data[s_name].values() ])
            for gc, count in data[s_name].items():
                data_norm[s_name][gc] = count / total * 100

        if len(data) == 0:
            log.debug('per_sequence_gc_content not found in FastQC reports')
            return
        else:
            pconfig = {'id': 'fastqc_per_sequence_gc_content_plot', 'title': 'FastQC: Per Sequence GC Content', 
               'xlab': '% GC', 
               'ymin': 0, 
               'xmax': 100, 
               'xmin': 0, 
               'yDecimals': False, 
               'tt_label': '<b>{point.x}% GC</b>: {point.y}', 
               'colors': self.get_status_cols('per_sequence_gc_content'), 
               'data_labels': [{'name': 'Percentages', 'ylab': 'Percentage'}, {'name': 'Counts', 'ylab': 'Count'}]}
            theoretical_gc = None
            theoretical_gc_raw = None
            theoretical_gc_name = None
            for f in self.find_log_files('fastqc/theoretical_gc'):
                if theoretical_gc_raw is not None:
                    log.warn(('Multiple FastQC Theoretical GC Content files found, now using {}').format(f['fn']))
                theoretical_gc_raw = f['f']
                theoretical_gc_name = f['fn']

            if theoretical_gc_raw is None:
                tgc = getattr(config, 'fastqc_config', {}).get('fastqc_theoretical_gc', None)
                if tgc is not None:
                    theoretical_gc_name = os.path.basename(tgc)
                    tgc_fn = ('fastqc_theoretical_gc_{}.txt').format(tgc)
                    tgc_path = os.path.join(os.path.dirname(__file__), 'fastqc_theoretical_gc', tgc_fn)
                    if not os.path.isfile(tgc_path):
                        tgc_path = tgc
                    try:
                        with io.open(tgc_path, 'r', encoding='utf-8') as (f):
                            theoretical_gc_raw = f.read()
                    except IOError:
                        log.warn(("Couldn't open FastQC Theoretical GC Content file {}").format(tgc_path))
                        theoretical_gc_raw = None

            if theoretical_gc_raw is not None:
                theoretical_gc = list()
                for l in theoretical_gc_raw.splitlines():
                    if '# FastQC theoretical GC content curve:' in l:
                        theoretical_gc_name = l[39:]
                    elif not l.startswith('#'):
                        s = l.split()
                        try:
                            theoretical_gc.append([float(s[0]), float(s[1])])
                        except (TypeError, IndexError):
                            pass

            desc = 'The average GC content of reads. Normal random library typically have a\n        roughly normal distribution of GC content.'
            if theoretical_gc is not None:
                max_total = max([ sum(d.values()) for d in data.values() ])
                esconfig = {'name': 'Theoretical GC Content', 
                   'dashStyle': 'Dash', 
                   'lineWidth': 2, 
                   'color': '#000000', 
                   'marker': {'enabled': False}, 'enableMouseTracking': False, 
                   'showInLegend': False}
                pconfig['extra_series'] = [
                 [
                  dict(esconfig)], [dict(esconfig)]]
                pconfig['extra_series'][0][0]['data'] = theoretical_gc
                pconfig['extra_series'][1][0]['data'] = [ [d[0], d[1] / 100.0 * max_total] for d in theoretical_gc ]
                desc = (' **The dashed black line shows theoretical GC content:** `{}`').format(theoretical_gc_name)
            self.add_section(name='Per Sequence GC Content', anchor='fastqc_per_sequence_gc_content', description=desc, helptext="\n            From the [FastQC help](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/5%20Per%20Sequence%20GC%20Content.html):\n\n            _This module measures the GC content across the whole length of each sequence\n            in a file and compares it to a modelled normal distribution of GC content._\n\n            _In a normal random library you would expect to see a roughly normal distribution\n            of GC content where the central peak corresponds to the overall GC content of\n            the underlying genome. Since we don't know the the GC content of the genome the\n            modal GC content is calculated from the observed data and used to build a\n            reference distribution._\n\n            _An unusually shaped distribution could indicate a contaminated library or\n            some other kinds of biased subset. A normal distribution which is shifted\n            indicates some systematic bias which is independent of base position. If there\n            is a systematic bias which creates a shifted normal distribution then this won't\n            be flagged as an error by the module since it doesn't know what your genome's\n            GC content should be._\n            ", plot=linegraph.plot([data_norm, data], pconfig))
            return

    def n_content_plot(self):
        """ Create the HTML for the per base N content plot """
        data = dict()
        for s_name in self.fastqc_data:
            try:
                data[s_name] = {self.avg_bp_from_range(d['base']):d['n-count'] for d in self.fastqc_data[s_name]['per_base_n_content']}
            except KeyError:
                pass

        if len(data) == 0:
            log.debug('per_base_n_content not found in FastQC reports')
            return
        else:
            pconfig = {'id': 'fastqc_per_base_n_content_plot', 'title': 'FastQC: Per Base N Content', 
               'ylab': 'Percentage N-Count', 
               'xlab': 'Position in Read (bp)', 
               'yCeiling': 100, 
               'yMinRange': 5, 
               'ymin': 0, 
               'xmin': 0, 
               'xDecimals': False, 
               'colors': self.get_status_cols('per_base_n_content'), 
               'tt_label': '<b>Base {point.x}</b>: {point.y:.2f}%', 
               'yPlotBands': [{'from': 20, 'to': 100, 'color': '#e6c3c3'}, {'from': 5, 'to': 20, 'color': '#e6dcc3'}, {'from': 0, 'to': 5, 'color': '#c3e6c3'}]}
            self.add_section(name='Per Base N Content', anchor='fastqc_per_base_n_content', description='The percentage of base calls at each position for which an `N` was called.', helptext="\n            From the [FastQC help](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/6%20Per%20Base%20N%20Content.html):\n\n            _If a sequencer is unable to make a base call with sufficient confidence then it will\n            normally substitute an `N` rather than a conventional base call. This graph shows the\n            percentage of base calls at each position for which an `N` was called._\n\n            _It's not unusual to see a very low proportion of Ns appearing in a sequence, especially\n            nearer the end of a sequence. However, if this proportion rises above a few percent\n            it suggests that the analysis pipeline was unable to interpret the data well enough to\n            make valid base calls._\n            ", plot=linegraph.plot(data, pconfig))
            return

    def seq_length_dist_plot(self):
        """ Create the HTML for the Sequence Length Distribution plot """
        data = dict()
        seq_lengths = set()
        multiple_lenths = False
        for s_name in self.fastqc_data:
            try:
                data[s_name] = {self.avg_bp_from_range(d['length']):d['count'] for d in self.fastqc_data[s_name]['sequence_length_distribution']}
                seq_lengths.update(data[s_name].keys())
                if len(set(data[s_name].keys())) > 1:
                    multiple_lenths = True
            except KeyError:
                pass

        if len(data) == 0:
            log.debug('sequence_length_distribution not found in FastQC reports')
            return
        else:
            if not multiple_lenths:
                lengths = ('bp , ').join([ str(l) for l in list(seq_lengths) ])
                desc = ('All samples have sequences of a single length ({}bp).').format(lengths)
                if len(seq_lengths) > 1:
                    desc += ' See the <a href="#general_stats">General Statistics Table</a>.'
                self.add_section(name='Sequence Length Distribution', anchor='fastqc_sequence_length_distribution', description=('<div class="alert alert-info">{}</div>').format(desc))
            else:
                pconfig = {'id': 'fastqc_sequence_length_distribution_plot', 'title': 'FastQC: Sequence Length Distribution', 
                   'ylab': 'Read Count', 
                   'xlab': 'Sequence Length (bp)', 
                   'ymin': 0, 
                   'yMinTickInterval': 0.1, 
                   'xDecimals': False, 
                   'colors': self.get_status_cols('sequence_length_distribution'), 
                   'tt_label': '<b>{point.x} bp</b>: {point.y}'}
                self.add_section(name='Sequence Length Distribution', anchor='fastqc_sequence_length_distribution', description='The distribution of fragment sizes (read lengths) found.\n                    See the [FastQC help](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/7%20Sequence%20Length%20Distribution.html)', plot=linegraph.plot(data, pconfig))
            return

    def seq_dup_levels_plot(self):
        """ Create the HTML for the Sequence Duplication Levels plot """
        data = dict()
        max_dupval = 0
        for s_name in self.fastqc_data:
            try:
                thisdata = {}
                for d in self.fastqc_data[s_name]['sequence_duplication_levels']:
                    thisdata[d['duplication_level']] = d['percentage_of_total']
                    max_dupval = max(max_dupval, d['percentage_of_total'])

                data[s_name] = OrderedDict()
                for k in self.dup_keys:
                    try:
                        data[s_name][k] = thisdata[k]
                    except KeyError:
                        pass

            except KeyError:
                pass

        if len(data) == 0:
            log.debug('sequence_length_distribution not found in FastQC reports')
            return
        else:
            pconfig = {'id': 'fastqc_sequence_duplication_levels_plot', 
               'title': 'FastQC: Sequence Duplication Levels', 
               'categories': True, 
               'ylab': '% of Library', 
               'xlab': 'Sequence Duplication Level', 
               'ymax': 100 if max_dupval <= 100.0 else None, 
               'ymin': 0, 
               'yMinTickInterval': 0.1, 
               'colors': self.get_status_cols('sequence_duplication_levels'), 
               'tt_label': '<b>{point.x}</b>: {point.y:.1f}%'}
            self.add_section(name='Sequence Duplication Levels', anchor='fastqc_sequence_duplication_levels', description='The relative level of duplication found for every sequence.', helptext='\n            From the [FastQC Help](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/8%20Duplicate%20Sequences.html):\n\n            _In a diverse library most sequences will occur only once in the final set.\n            A low level of duplication may indicate a very high level of coverage of the\n            target sequence, but a high level of duplication is more likely to indicate\n            some kind of enrichment bias (eg PCR over amplification). This graph shows\n            the degree of duplication for every sequence in a library: the relative\n            number of sequences with different degrees of duplication._\n\n            _Only sequences which first appear in the first 100,000 sequences\n            in each file are analysed. This should be enough to get a good impression\n            for the duplication levels in the whole file. Each sequence is tracked to\n            the end of the file to give a representative count of the overall duplication level._\n\n            _The duplication detection requires an exact sequence match over the whole length of\n            the sequence. Any reads over 75bp in length are truncated to 50bp for this analysis._\n\n            _In a properly diverse library most sequences should fall into the far left of the\n            plot in both the red and blue lines. A general level of enrichment, indicating broad\n            oversequencing in the library will tend to flatten the lines, lowering the low end\n            and generally raising other categories. More specific enrichments of subsets, or\n            the presence of low complexity contaminants will tend to produce spikes towards the\n            right of the plot._\n            ', plot=linegraph.plot(data, pconfig))
            return

    def overrepresented_sequences(self):
        """Sum the percentages of overrepresented sequences and display them in a bar plot"""
        data = dict()
        for s_name in self.fastqc_data:
            data[s_name] = dict()
            try:
                max_pcnt = max([ float(d['percentage']) for d in self.fastqc_data[s_name]['overrepresented_sequences'] ])
                total_pcnt = sum([ float(d['percentage']) for d in self.fastqc_data[s_name]['overrepresented_sequences'] ])
                data[s_name]['total_overrepresented'] = total_pcnt
                data[s_name]['top_overrepresented'] = max_pcnt
                data[s_name]['remaining_overrepresented'] = total_pcnt - max_pcnt
            except KeyError:
                if self.fastqc_data[s_name]['statuses']['overrepresented_sequences'] == 'pass':
                    data[s_name]['total_overrepresented'] = 0
                    data[s_name]['top_overrepresented'] = 0
                    data[s_name]['remaining_overrepresented'] = 0
                else:
                    log.debug(("Couldn't find data for {}, invalid Key").format(s_name))

        cats = OrderedDict()
        cats['top_overrepresented'] = {'name': 'Top over-represented sequence'}
        cats['remaining_overrepresented'] = {'name': 'Sum of remaining over-represented sequences'}
        pconfig = {'id': 'fastqc_overrepresented_sequencesi_plot', 
           'title': 'FastQC: Overrepresented sequences', 
           'ymin': 0, 
           'yCeiling': 100, 
           'yMinRange': 20, 
           'tt_decimals': 2, 
           'tt_suffix': '%', 
           'tt_percentages': False, 
           'ylab_format': '{value}%', 
           'cpswitch': False, 
           'ylab': 'Percentage of Total Sequences'}
        if max([ x['total_overrepresented'] for x in data.values() ]) < 1:
            plot_html = ('<div class="alert alert-info">{} samples had less than 1% of reads made up of overrepresented sequences</div>').format(len(data))
        else:
            plot_html = bargraph.plot(data, cats, pconfig)
        self.add_section(name='Overrepresented sequences', anchor='fastqc_overrepresented_sequences', description='The total amount of overrepresented sequences found in each library.', helptext="\n            FastQC calculates and lists overrepresented sequences in FastQ files. It would not be\n            possible to show this for all samples in a MultiQC report, so instead this plot shows\n            the _number of sequences_ categorized as over represented.\n\n            Sometimes, a single sequence  may account for a large number of reads in a dataset.\n            To show this, the bars are split into two: the first shows the overrepresented reads\n            that come from the single most common sequence. The second shows the total count\n            from all remaining overrepresented sequences.\n\n            From the [FastQC Help](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/9%20Overrepresented%20Sequences.html):\n\n            _A normal high-throughput library will contain a diverse set of sequences, with no\n            individual sequence making up a tiny fraction of the whole. Finding that a single\n            sequence is very overrepresented in the set either means that it is highly biologically\n            significant, or indicates that the library is contaminated, or not as diverse as you expected._\n\n            _FastQC lists all of the sequences which make up more than 0.1% of the total.\n            To conserve memory only sequences which appear in the first 100,000 sequences are tracked\n            to the end of the file. It is therefore possible that a sequence which is overrepresented\n            but doesn't appear at the start of the file for some reason could be missed by this module._\n            ", plot=plot_html)

    def adapter_content_plot(self):
        """ Create the HTML for the FastQC adapter plot """
        data = dict()
        for s_name in self.fastqc_data:
            try:
                for d in self.fastqc_data[s_name]['adapter_content']:
                    pos = self.avg_bp_from_range(d['position'])
                    for r in self.fastqc_data[s_name]['adapter_content']:
                        pos = self.avg_bp_from_range(r['position'])
                        for a in r.keys():
                            k = ('{} - {}').format(s_name, a)
                            if a != 'position':
                                try:
                                    data[k][pos] = r[a]
                                except KeyError:
                                    data[k] = {pos: r[a]}

            except KeyError:
                pass

        if len(data) == 0:
            log.debug('adapter_content not found in FastQC reports')
            return
        else:
            data = {k:d for k, d in data.items() if max(data[k].values()) >= 0.1}
            pconfig = {'id': 'fastqc_adapter_content_plot', 
               'title': 'FastQC: Adapter Content', 
               'ylab': '% of Sequences', 
               'xlab': 'Position (bp)', 
               'yCeiling': 100, 
               'yMinRange': 5, 
               'ymin': 0, 
               'xDecimals': False, 
               'tt_label': '<b>Base {point.x}</b>: {point.y:.2f}%', 
               'hide_empty': True, 
               'yPlotBands': [{'from': 20, 'to': 100, 'color': '#e6c3c3'}, {'from': 5, 'to': 20, 'color': '#e6dcc3'}, {'from': 0, 'to': 5, 'color': '#c3e6c3'}]}
            if len(data) > 0:
                plot_html = linegraph.plot(data, pconfig)
            else:
                plot_html = '<div class="alert alert-info">No samples found with any adapter contamination > 0.1%</div>'
            self.add_section(name='Adapter Content', anchor='fastqc_adapter_content', description='The cumulative percentage count of the proportion of your\n            library which has seen each of the adapter sequences at each position.', helptext='\n            Note that only samples with &ge; 0.1% adapter contamination are shown.\n\n            There may be several lines per sample, as one is shown for each adapter\n            detected in the file.\n\n            From the [FastQC Help](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/10%20Adapter%20Content.html):\n\n            _The plot shows a cumulative percentage count of the proportion\n            of your library which has seen each of the adapter sequences at each position.\n            Once a sequence has been seen in a read it is counted as being present\n            right through to the end of the read so the percentages you see will only\n            increase as the read length goes on._\n            ', plot=plot_html)
            return

    def status_heatmap(self):
        """ Heatmap showing all statuses for every sample """
        status_numbers = {'pass': 1, 
           'warn': 0.5, 
           'fail': 0.25}
        data = []
        s_names = []
        status_cats = OrderedDict()
        for s_name in sorted(self.fastqc_data.keys()):
            s_names.append(s_name)
            for status_cat, status in self.fastqc_data[s_name]['statuses'].items():
                if status_cat not in status_cats:
                    status_cats[status_cat] = status_cat.replace('_', ' ').title().replace('Gc', 'GC')

        for s_name in s_names:
            row = []
            for status_cat in status_cats:
                try:
                    row.append(status_numbers[self.fastqc_data[s_name]['statuses'][status_cat]])
                except KeyError:
                    row.append(0)

            data.append(row)

        pconfig = {'id': 'fastqc-status-check-heatmap', 
           'title': 'FastQC: Status Checks', 
           'xTitle': 'Section Name', 
           'yTitle': 'Sample', 
           'min': 0, 
           'max': 1, 
           'square': False, 
           'colstops': [
                      [
                       0, '#ffffff'],
                      [
                       0.25, '#d9534f'],
                      [
                       0.5, '#fee391'],
                      [
                       1, '#5cb85c']], 
           'decimalPlaces': 1, 
           'legend': False, 
           'datalabels': False}
        self.add_section(name='Status Checks', anchor='fastqc_status_checks', description='\n            Status for each FastQC section showing whether results seem entirely normal (green),\n            slightly abnormal (orange) or very unusual (red).\n            ', helptext="\n            FastQC assigns a status for each section of the report.\n            These give a quick evaluation of whether the results of the analysis seem\n            entirely normal (green), slightly abnormal (orange) or very unusual (red).\n\n            It is important to stress that although the analysis results appear to give a pass/fail result,\n            these evaluations must be taken in the context of what you expect from your library.\n            A 'normal' sample as far as FastQC is concerned is random and diverse.\n            Some experiments may be expected to produce libraries which are biased in particular ways.\n            You should treat the summary evaluations therefore as pointers to where you should concentrate\n            your attention and understand why your library may not look random and diverse.\n\n            Specific guidance on how to interpret the output of each module can be found in the relevant\n            report section, or in the [FastQC help](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/).\n\n            In this heatmap, we summarise all of these into a single heatmap for a quick overview.\n            Note that not all FastQC sections have plots in MultiQC reports, but all status checks\n            are shown in this heatmap.\n            ", plot=heatmap.plot(data, list(status_cats.values()), s_names, pconfig))

    def avg_bp_from_range(self, bp):
        """ Helper function - FastQC often gives base pair ranges (eg. 10-15)
        which are not helpful when plotting. This returns the average from such
        ranges as an int, which is helpful. If not a range, just returns the int """
        try:
            if '-' in bp:
                maxlen = float(bp.split('-', 1)[1])
                minlen = float(bp.split('-', 1)[0])
                bp = (maxlen - minlen) / 2 + minlen
        except TypeError:
            pass

        return int(bp)

    def get_status_cols(self, section):
        """ Helper function - returns a list of colours according to the FastQC
        status of this module for each sample. """
        colours = dict()
        for s_name in self.fastqc_data:
            status = self.fastqc_data[s_name]['statuses'].get(section, 'default')
            colours[s_name] = self.status_colours[status]

        return colours