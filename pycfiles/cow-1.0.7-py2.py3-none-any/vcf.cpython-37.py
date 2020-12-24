# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/joe/devel/covviz/covviz/vcf.py
# Compiled at: 2019-09-12 13:51:12
# Size of source mod 2**32: 2071 bytes
import os, re
from itertools import groupby
from .utils import gzopen
try:
    from itertools import ifilterfalse as filterfalse
except ImportError:
    from itertools import filterfalse

def parse_vcf(path, traces, exclude, regex=None, y_offset=-0.15, track_color='#444'):
    """
    parse a VCFv4.1 file, placing squares per variant
    """
    trace_name = os.path.basename(path)
    with gzopen(path) as (fh):
        cleaned = filterfalse(lambda i: i[0] == '#', fh)
        info_re = None
        if regex:
            info_re = re.compile('%s([^;]*)' % regex)
        for chrom, entries in groupby(cleaned,
          key=(lambda i: i.partition('\t')[0].lstrip('chr'))):
            if exclude.findall(chrom):
                continue
            if chrom not in traces:
                continue
            trace_x = list()
            trace_y = list()
            trace_text = list()
            for line in entries:
                if line.startswith('#'):
                    continue
                toks = line.strip().split('\t')
                x = int(toks[1])
                info = toks[7].replace(';', '<br>')
                if info_re:
                    try:
                        info = info_re.findall(toks[7])[0]
                    except IndexError:
                        info = ''

                trace_x.append(x)
                trace_y.append(y_offset)
                trace_text.append(info)

            trace = dict(x=trace_x,
              y=trace_y,
              mode='markers',
              type='scattergl',
              name=trace_name,
              text=trace_text,
              marker=dict(size=10,
              symbol='square',
              color=track_color,
              line=dict(width=1, color='white')),
              tracktype='vcf')
            traces[chrom].append(trace)

    return traces