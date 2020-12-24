# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/bbmap/plot_bqhist.py
# Compiled at: 2017-12-06 12:57:29
from itertools import chain
from multiqc.plots import linegraph

def plot_bqhist(samples, file_type, **plot_args):
    """ Create line graph plot of histogram data for BBMap 'bqhist' output.

    The 'samples' parameter could be from the bbmap mod_data dictionary:
    samples = bbmap.MultiqcModule.mod_data[file_type]
    """
    all_x = set()
    for item in sorted(chain(*[ samples[sample]['data'].items() for sample in samples
                              ])):
        all_x.add(item[0])

    columns_to_plot = {'Read 1 averages': {3: 'Mean'}, 
       'Read 2 averages': {12: 'Mean'}}
    plot_data = []
    for column_type in columns_to_plot:
        plot_data.append({sample + '.' + column_name:{x:(samples[sample]['data'][x][column] if x in samples[sample]['data'] else 0) for x in all_x} for sample in samples for column, column_name in columns_to_plot[column_type].items()})

    plot_params = {'id': 'bbmap-' + file_type + '_plot', 
       'title': 'BBTools: ' + plot_args['plot_title'], 
       'xlab': 'Read position', 
       'ylab': 'Average quality score', 
       'data_labels': [{'name': 'Read 1'}, {'name': 'Read 2'}]}
    plot_params.update(plot_args['plot_params'])
    plot = linegraph.plot(plot_data, plot_params)
    return plot