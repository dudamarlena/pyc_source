# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/samtools/idxstats.py
# Compiled at: 2018-06-13 05:46:25
# Size of source mod 2**32: 7531 bytes
""" MultiQC submodule to parse output from Samtools idxstats """
import logging
from collections import OrderedDict, defaultdict
from multiqc import config
from multiqc.plots import bargraph, linegraph
log = logging.getLogger(__name__)

class IdxstatsReportMixin:

    def parse_samtools_idxstats(self):
        """ Find Samtools idxstats logs and parse their data """
        self.samtools_idxstats = dict()
        for f in self.find_log_files('samtools/idxstats'):
            parsed_data = parse_single_report(f['f'])
            if len(parsed_data) > 0:
                if f['s_name'] in self.samtools_idxstats:
                    log.debug('Duplicate sample name found! Overwriting: {}'.format(f['s_name']))
                self.add_data_source(f, section='idxstats')
                self.samtools_idxstats[f['s_name']] = parsed_data

        self.samtools_idxstats = self.ignore_samples(self.samtools_idxstats)
        if len(self.samtools_idxstats) > 0:
            self.write_data_file(self.samtools_idxstats, 'multiqc_samtools_idxstats')
            keys = list()
            pdata = dict()
            pdata_norm = dict()
            xy_counts = dict()
            chrs_mapped = defaultdict(lambda : 0)
            sample_mapped = defaultdict(lambda : 0)
            total_mapped = 0
            cutoff = float(getattr(config, 'samtools_idxstats_fraction_cutoff', 0.001))
            if cutoff != 0.001:
                log.info('Setting idxstats cutoff to: {}%'.format(cutoff * 100.0))
            for s_name in self.samtools_idxstats:
                for chrom in self.samtools_idxstats[s_name]:
                    chrs_mapped[chrom] += self.samtools_idxstats[s_name][chrom]
                    sample_mapped[s_name] += self.samtools_idxstats[s_name][chrom]
                    total_mapped += self.samtools_idxstats[s_name][chrom]

            req_reads = float(total_mapped) * cutoff
            chr_always = getattr(config, 'samtools_idxstats_always', [])
            if len(chr_always) > 0:
                log.info('Trying to include these chromosomes in idxstats: {}'.format(', '.join(chr_always)))
            chr_ignore = getattr(config, 'samtools_idxstats_ignore', [])
            if len(chr_ignore) > 0:
                log.info('Excluding these chromosomes from idxstats: {}'.format(', '.join(chr_ignore)))
            xchr = getattr(config, 'samtools_idxstats_xchr', False)
            if xchr:
                log.info('Using "{}" as X chromosome name'.format(xchr))
            ychr = getattr(config, 'samtools_idxstats_ychr', False)
            if ychr:
                log.info('Using "{}" as Y chromosome name'.format(ychr))
            for s_name in self.samtools_idxstats:
                x_count = False
                y_count = False
                for chrom in self.samtools_idxstats[s_name]:
                    if not float(chrs_mapped[chrom]) > req_reads:
                        if chrom in chr_always:
                            if chrom not in chr_ignore:
                                if chrom not in keys:
                                    keys.append(chrom)
                        mapped = self.samtools_idxstats[s_name][chrom]
                        if xchr is not False:
                            if str(xchr) == str(chrom):
                                x_count = mapped
                        else:
                            if chrom.lower() == 'x' or chrom.lower() == 'chrx':
                                x_count = mapped
                        if ychr is not False:
                            if str(ychr) == str(chrom):
                                y_count = mapped

                if x_count and y_count:
                    xy_counts[s_name] = {'x':x_count, 
                     'y':y_count}

            for s_name in self.samtools_idxstats:
                pdata[s_name] = OrderedDict()
                pdata_norm[s_name] = OrderedDict()
                for k in keys:
                    try:
                        pdata[s_name][k] = self.samtools_idxstats[s_name][k]
                        pdata_norm[s_name][k] = float(self.samtools_idxstats[s_name][k]) / sample_mapped[s_name]
                    except (KeyError, ZeroDivisionError):
                        pdata[s_name][k] = 0
                        pdata_norm[s_name][k] = 0

            if len(xy_counts) > 0:
                xy_keys = OrderedDict()
                xy_keys['x'] = {'name': xchr if xchr else 'Chromosome X'}
                xy_keys['y'] = {'name': ychr if ychr else 'Chromosome Y'}
                pconfig = {'id':'samtools-idxstats-xy-plot', 
                 'title':'Samtools idxstats: chrXY mapped reads', 
                 'ylab':'Percent of X+Y Reads', 
                 'cpswitch_counts_label':'Number of Reads', 
                 'cpswitch_percent_label':'Percent of X+Y Reads', 
                 'cpswitch_c_active':False}
                self.add_section(name='XY counts',
                  anchor='samtools-idxstats-xy-counts',
                  plot=(bargraph.plot(xy_counts, xy_keys, pconfig)))
            pconfig = {'id':'samtools-idxstats-mapped-reads-plot', 
             'title':'Samtools idxstats: Mapped reads per contig', 
             'ylab':'# mapped reads', 
             'xlab':'Chromosome Name', 
             'categories':True, 
             'tt_label':'<strong>{point.category}:</strong> {point.y:.2f}', 
             'data_labels':[
              {'name':'Normalised Counts', 
               'ylab':'Fraction of total count'},
              {'name':'Counts', 
               'ylab':'# mapped reads'}]}
            self.add_section(name='Mapped reads per contig',
              anchor='samtools-idxstats',
              description=('The <code>samtools idxstats</code> tool counts the number of mapped reads per chromosome / contig. ' + 'Chromosomes with &lt; {}% of the total aligned reads are omitted from this plot.'.format(cutoff * 100)),
              plot=(linegraph.plot([pdata_norm, pdata], pconfig)))
        return len(self.samtools_idxstats)


def parse_single_report(f):
    """ Parse a samtools idxstats idxstats """
    parsed_data = OrderedDict()
    for l in f.splitlines():
        s = l.split('\t')
        try:
            parsed_data[s[0]] = int(s[2])
        except (IndexError, ValueError):
            pass

    return parsed_data