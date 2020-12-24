# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/plots/heatmap.py
# Compiled at: 2018-10-20 18:34:54
# Size of source mod 2**32: 2565 bytes
""" MultiQC functions to plot a heatmap """
from __future__ import print_function
import logging, random
from multiqc.utils import config, report
logger = logging.getLogger(__name__)
letters = 'abcdefghijklmnopqrstuvwxyz'

def plot(data, xcats, ycats=None, pconfig=None):
    """ Plot a 2D heatmap.
    :param data: List of lists, each a representing a row of values.
    :param xcats: Labels for x axis
    :param ycats: Labels for y axis. Defaults to same as x.
    :param pconfig: optional dict with config key:value pairs.
    :return: HTML and JS, ready to be inserted into the page
    """
    if pconfig is None:
        pconfig = {}
    if 'id' in pconfig:
        if pconfig['id']:
            if pconfig['id'] in config.custom_plot_config:
                for k, v in config.custom_plot_config[pconfig['id']].items():
                    pconfig[k] = v

    if ycats is None:
        ycats = xcats
    return highcharts_heatmap(data, xcats, ycats, pconfig)


def highcharts_heatmap(data, xcats, ycats, pconfig=None):
    """
    Build the HTML needed for a HighCharts line graph. Should be
    called by plot_xy_data, which properly formats input data.
    """
    if pconfig is None:
        pconfig = {}
    pdata = []
    for i, arr in enumerate(data):
        for j, val in enumerate(arr):
            pdata.append([j, i, val])

    if pconfig.get('id') is None:
        pconfig['id'] = 'mqc_hcplot_' + ''.join(random.sample(letters, 10))
    pconfig['id'] = report.save_htmlid(pconfig['id'])
    html = '<div class="mqc_hcplot_plotgroup">'
    html += '<div class="btn-group hc_switch_group">\n        <button type="button" class="mqc_heatmap_sortHighlight btn btn-default btn-sm" data-target="#{id}" disabled="disabled">\n            <span class="glyphicon glyphicon-sort-by-attributes-alt"></span> Sort by highlight\n        </button>\n    </div>'.format(id=(pconfig['id']))
    html += '<div class="hc-plot-wrapper"><div id="{id}" class="hc-plot not_rendered hc-heatmap"><small>loading..</small></div></div></div> \n'.format(id=(pconfig['id']))
    report.num_hc_plots += 1
    report.plot_data[pconfig['id']] = {'plot_type':'heatmap', 
     'data':pdata, 
     'xcats':xcats, 
     'ycats':ycats, 
     'config':pconfig}
    return html