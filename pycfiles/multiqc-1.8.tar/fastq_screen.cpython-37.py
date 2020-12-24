# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/fastq_screen/fastq_screen.py
# Compiled at: 2019-10-28 10:24:54
# Size of source mod 2**32: 12151 bytes
""" MultiQC module to parse output from FastQ Screen """
from __future__ import print_function
from collections import OrderedDict
import json, logging, re
from multiqc import config
from multiqc.plots import bargraph
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc.utils import report
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        super(MultiqcModule, self).__init__(name='FastQ Screen', anchor='fastq_screen', href='http://www.bioinformatics.babraham.ac.uk/projects/fastq_screen/',
          info='allows you to screen a library of sequences in FastQ format against a set of sequence databases so you can see if the composition of the library matches with what you expect.')
        self.fq_screen_data = dict()
        self.num_orgs = 0
        for f in self.find_log_files('fastq_screen', filehandles=True):
            parsed_data = self.parse_fqscreen(f)
            if parsed_data is not None:
                if f['s_name'] in self.fq_screen_data:
                    log.debug('Duplicate sample name found! Overwriting: {}'.format(f['s_name']))
                self.add_data_source(f)
                self.fq_screen_data[f['s_name']] = parsed_data

        self.fq_screen_data = self.ignore_samples(self.fq_screen_data)
        if len(self.fq_screen_data) == 0:
            raise UserWarning
        else:
            log.info('Found {} reports'.format(len(self.fq_screen_data)))
            if len(self.fq_screen_data) * self.num_orgs <= 160:
                config.plots_force_flat or getattr(config, 'fastqscreen_simpleplot', False) or self.add_section(content=(self.fqscreen_plot()))
            else:
                self.add_section(plot=(self.fqscreen_simple_plot()))
        self.write_data_file(self.parse_csv(), 'multiqc_fastq_screen')

    def parse_fqscreen(self, f):
        """ Parse the FastQ Screen output into a 3D dict """
        parsed_data = OrderedDict()
        reads_processed = None
        nohits_pct = None
        for l in f['f']:
            if l.startswith('%Hit_no_genomes:') or l.startswith('%Hit_no_libraries:'):
                nohits_pct = float(l.split(':', 1)[1])
                parsed_data['No hits'] = {'percentages': {'one_hit_one_library': nohits_pct}}
            else:
                fqs = re.search('^(\\S+)\\s+(\\d+)\\s+(\\d+)\\s+([\\d\\.]+)\\s+(\\d+)\\s+([\\d\\.]+)\\s+(\\d+)\\s+([\\d\\.]+)\\s+(\\d+)\\s+([\\d\\.]+)\\s+(\\d+)\\s+([\\d\\.]+)$', l)
            if fqs:
                org = fqs.group(1)
                parsed_data[org] = {'percentages':{},  'counts':{}}
                reads_processed = int(fqs.group(2))
                parsed_data[org]['counts']['reads_processed'] = int(fqs.group(2))
                parsed_data[org]['counts']['unmapped'] = int(fqs.group(3))
                parsed_data[org]['percentages']['unmapped'] = float(fqs.group(4))
                parsed_data[org]['counts']['one_hit_one_library'] = int(fqs.group(5))
                parsed_data[org]['percentages']['one_hit_one_library'] = float(fqs.group(6))
                parsed_data[org]['counts']['multiple_hits_one_library'] = int(fqs.group(7))
                parsed_data[org]['percentages']['multiple_hits_one_library'] = float(fqs.group(8))
                parsed_data[org]['counts']['one_hit_multiple_libraries'] = int(fqs.group(9))
                parsed_data[org]['percentages']['one_hit_multiple_libraries'] = float(fqs.group(10))
                parsed_data[org]['counts']['multiple_hits_multiple_libraries'] = int(fqs.group(11))
                parsed_data[org]['percentages']['multiple_hits_multiple_libraries'] = float(fqs.group(12))
                parsed_data['total_reads'] = int(fqs.group(2))

        if len(parsed_data) == 0:
            return
        if reads_processed and nohits_pct:
            parsed_data['No hits']['counts'] = {'one_hit_one_library': int(nohits_pct / 100.0 * float(reads_processed))}
        else:
            log.warn("Couldn't find number of reads with no hits for '{}'".format(f['s_name']))
        self.num_orgs = max(len(parsed_data), self.num_orgs)
        return parsed_data

    def parse_csv(self):
        totals = OrderedDict()
        for s in sorted(self.fq_screen_data.keys()):
            totals[s] = OrderedDict()
            for org in self.fq_screen_data[s]:
                if org == 'total_reads':
                    totals[s]['total_reads'] = self.fq_screen_data[s][org]
                    continue
                try:
                    k = '{} counts'.format(org)
                    totals[s][k] = self.fq_screen_data[s][org]['counts']['one_hit_one_library']
                    totals[s][k] += self.fq_screen_data[s][org]['counts'].get('multiple_hits_one_library', 0)
                    totals[s][k] += self.fq_screen_data[s][org]['counts'].get('one_hit_multiple_libraries', 0)
                    totals[s][k] += self.fq_screen_data[s][org]['counts'].get('multiple_hits_multiple_libraries', 0)
                except KeyError:
                    pass

                try:
                    k = '{} percentage'.format(org)
                    totals[s][k] = self.fq_screen_data[s][org]['percentages']['one_hit_one_library']
                    totals[s][k] += self.fq_screen_data[s][org]['percentages'].get('multiple_hits_one_library', 0)
                    totals[s][k] += self.fq_screen_data[s][org]['percentages'].get('one_hit_multiple_libraries', 0)
                    totals[s][k] += self.fq_screen_data[s][org]['percentages'].get('multiple_hits_multiple_libraries', 0)
                except KeyError:
                    pass

        return totals

    def fqscreen_plot(self):
        """ Makes a fancy custom plot which replicates the plot seen in the main
        FastQ Screen program. Not useful if lots of samples as gets too wide. """
        categories = list()
        getCats = True
        data = list()
        p_types = OrderedDict()
        p_types['multiple_hits_multiple_libraries'] = {'col':'#7f0000',  'name':'Multiple Hits, Multiple Genomes'}
        p_types['one_hit_multiple_libraries'] = {'col':'#ff0000',  'name':'One Hit, Multiple Genomes'}
        p_types['multiple_hits_one_library'] = {'col':'#00007f',  'name':'Multiple Hits, One Genome'}
        p_types['one_hit_one_library'] = {'col':'#0000ff',  'name':'One Hit, One Genome'}
        for k, t in p_types.items():
            first = True
            for s in sorted(self.fq_screen_data.keys()):
                thisdata = list()
                if len(categories) > 0:
                    getCats = False
                else:
                    for org in sorted(self.fq_screen_data[s]):
                        if org == 'total_reads':
                            continue
                        try:
                            thisdata.append(self.fq_screen_data[s][org]['percentages'][k])
                        except KeyError:
                            thisdata.append(None)

                        if getCats:
                            categories.append(org)

                    td = {'name':t['name'], 
                     'stack':s, 
                     'data':thisdata, 
                     'color':t['col']}
                    if first:
                        first = False
                    else:
                        td['linkedTo'] = ':previous'
                data.append(td)

        plot_id = report.save_htmlid('fq_screen_plot')
        html = '<div id={plot_id} class="fq_screen_plot hc-plot"></div>\n        <script type="application/json" class="fq_screen_dict">{dict}</script>\n        '.format(plot_id=(json.dumps(plot_id)),
          dict=(json.dumps({'plot_id':plot_id,  'data':data,  'categories':categories})))
        html += '<script type="text/javascript">\n            fq_screen_dict = { }; // { <plot_id>: data, categories }\n            $(\'.fq_screen_dict\').each(function (i, elem) {\n                var dict = JSON.parse(elem.innerHTML);\n                fq_screen_dict[dict.plot_id] = dict;\n            });\n\n            $(function () {\n                // In case of repeated modules: #fq_screen_plot, #fq_screen_plot-1, ..\n                $(".fq_screen_plot").each(function () {\n                    var plot_id = $(this).attr(\'id\');\n\n                    $(this).highcharts({\n                        chart: { type: "column", backgroundColor: null },\n                        title: { text: "FastQ Screen Results" },\n                        xAxis: { categories: fq_screen_dict[plot_id].categories },\n                        yAxis: {\n                            max: 100,\n                            min: 0,\n                            title: { text: "Percentage Aligned" }\n                        },\n                        tooltip: {\n                            formatter: function () {\n                                return "<b>" + this.series.stackKey.replace("column","") + " - " + this.x + "</b><br/>" +\n                                    this.series.name + ": " + this.y + "%<br/>" +\n                                    "Total Alignment: " + this.point.stackTotal + "%";\n                            },\n                        },\n                        plotOptions: {\n                            column: {\n                                pointPadding: 0,\n                                groupPadding: 0.02,\n                                stacking: "normal"\n                            }\n                        },\n                        series: fq_screen_dict[plot_id].data\n                    });\n                });\n            });\n        </script>'
        return html

    def fqscreen_simple_plot(self):
        """ Makes a simple bar plot with summed alignment counts for
        each species, stacked. """
        data = OrderedDict()
        cats = OrderedDict()
        for s_name in sorted(self.fq_screen_data):
            data[s_name] = OrderedDict()
            sum_alignments = 0
            for org in self.fq_screen_data[s_name]:
                if org == 'total_reads':
                    continue
                try:
                    data[s_name][org] = self.fq_screen_data[s_name][org]['counts']['one_hit_one_library']
                except KeyError:
                    log.error("No counts found for '{}' ('{}'). Could be malformed or very old FastQ Screen results.".format(org, s_name))
                    continue

                try:
                    data[s_name][org] += self.fq_screen_data[s_name][org]['counts']['multiple_hits_one_library']
                except KeyError:
                    pass

                sum_alignments += data[s_name][org]
                if org not in cats and org != 'No hits':
                    cats[org] = {'name': org}

            if 'total_reads' in self.fq_screen_data[s_name]:
                data[s_name]['Multiple Genomes'] = self.fq_screen_data[s_name]['total_reads'] - sum_alignments

        for s_name in list(data.keys()):
            if len(data[s_name]) == 0:
                del data[s_name]

        pconfig = {'id':'fastq_screen',  'title':'FastQ Screen', 
         'cpswitch_c_active':False, 
         'hide_zero_cats':False}
        cats['Multiple Genomes'] = {'name':'Multiple Genomes', 
         'color':'#820000'}
        cats['No hits'] = {'name':'No hits',  'color':'#cccccc'}
        return bargraph.plot(data, cats, pconfig)