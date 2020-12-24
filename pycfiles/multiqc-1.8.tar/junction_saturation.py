# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/rseqc/junction_saturation.py
# Compiled at: 2019-11-15 08:06:12
""" MultiQC submodule to parse output from RSeQC junction_saturation.py
http://rseqc.sourceforge.net/#junction-saturation-py """
from collections import OrderedDict
import logging, re
from multiqc.plots import linegraph
log = logging.getLogger(__name__)

def parse_reports(self):
    """ Find RSeQC junction_saturation frequency reports and parse their data """
    self.junction_saturation_all = dict()
    self.junction_saturation_known = dict()
    self.junction_saturation_novel = dict()
    for f in self.find_log_files('rseqc/junction_saturation'):
        parsed = dict()
        for l in f['f'].splitlines():
            r = re.search('^([xyzw])=c\\(([\\d,]+)\\)$', l)
            if r:
                parsed[r.group(1)] = [ float(i) for i in r.group(2).split(',') ]

        if len(parsed) == 4:
            if parsed['z'][(-1)] == 0:
                log.warn(("Junction saturation data all zeroes, skipping: '{}'").format(f['s_name']))
            else:
                if f['s_name'] in self.junction_saturation_all:
                    log.debug(('Duplicate sample name found! Overwriting: {}').format(f['s_name']))
                self.add_data_source(f, section='junction_saturation')
                self.junction_saturation_all[f['s_name']] = OrderedDict()
                self.junction_saturation_known[f['s_name']] = OrderedDict()
                self.junction_saturation_novel[f['s_name']] = OrderedDict()
                for k, v in enumerate(parsed['x']):
                    self.junction_saturation_all[f['s_name']][v] = parsed['z'][k]
                    self.junction_saturation_known[f['s_name']][v] = parsed['y'][k]
                    self.junction_saturation_novel[f['s_name']][v] = parsed['w'][k]

    self.junction_saturation_all = self.ignore_samples(self.junction_saturation_all)
    self.junction_saturation_known = self.ignore_samples(self.junction_saturation_known)
    self.junction_saturation_novel = self.ignore_samples(self.junction_saturation_novel)
    if len(self.junction_saturation_all) > 0:
        pconfig = {'id': 'rseqc_junction_saturation_plot', 
           'title': 'RSeQC: Junction Saturation', 
           'ylab': 'Number of Junctions', 
           'ymin': 0, 
           'xlab': 'Percent of reads', 
           'xmin': 0, 
           'xmax': 100, 
           'tt_label': '<strong>{point.x}% of reads</strong>: {point.y:.2f}', 
           'data_labels': [{'name': 'All Junctions'}, {'name': 'Known Junctions'}, {'name': 'Novel Junctions'}], 'cursor': 'pointer', 
           'click_func': plot_single()}
        self.add_section(name='Junction Saturation', anchor='rseqc-junction_saturation', description='<a href="http://rseqc.sourceforge.net/#junction-saturation-py" target="_blank">Junction Saturation</a>\n                counts the number of known splicing junctions that are observed\n                in each dataset. If sequencing depth is sufficient, all (annotated) splice junctions should\n                be rediscovered, resulting in a curve that reaches a plateau. Missing low abundance splice\n                junctions can affect downstream analysis.</p>\n                <div class="alert alert-info" id="rseqc-junction_sat_single_hint">\n                  <span class="glyphicon glyphicon-hand-up"></span>\n                  Click a line to see the data side by side (as in the original RSeQC plot).\n                </div><p>', plot=linegraph.plot([
         self.junction_saturation_all,
         self.junction_saturation_known,
         self.junction_saturation_novel], pconfig))
    return len(self.junction_saturation_all)


def plot_single():
    """ Return JS code required for plotting a single sample
    RSeQC plot. Attempt to make it look as much like the original as possible.
    Note: this code is injected by `eval(str)`, not <script type="text/javascript"> """
    return '\n    function(e){\n        // In case of repeated modules: #rseqc_junction_saturation_plot, #rseqc_junction_saturation_plot-1, ..\n        var rseqc_junction_saturation_plot = $(e.currentTarget).closest(\'.hc-plot\');\n        var rseqc_junction_saturation_plot_id = rseqc_junction_saturation_plot.attr(\'id\');\n        var junction_sat_single_hint = rseqc_junction_saturation_plot.closest(\'.mqc-section\').find(\'#junction_sat_single_hint\');\n\n\n        // Get the three datasets for this sample\n        var data = [\n            {\'name\': \'All Junctions\'},\n            {\'name\': \'Known Junctions\'},\n            {\'name\': \'Novel Junctions\'}\n        ];\n        var k = 0;\n        for (var i = 0; i < 3; i++) {\n            var ds = mqc_plots[rseqc_junction_saturation_plot_id][\'datasets\'][i];\n            for (k = 0; k < ds.length; k++){\n                if(ds[k][\'name\'] == this.series.name){\n                    data[i][\'data\'] = JSON.parse(JSON.stringify(ds[k][\'data\']));\n                    break;\n                }\n            }\n        }\n\n        // Create single plot div, and hide overview\n        var newplot = $(\'<div id="rseqc_junction_saturation_single">             <div id="rseqc_junction_saturation_single_controls">               <button class="btn btn-primary btn-sm" id="rseqc-junction_sat_single_return">                 Return to overview               </button>               <div class="btn-group btn-group-sm">                 <button class="btn btn-default rseqc-junction_sat_single_prevnext" data-action="prev">&laquo; Prev</button>                 <button class="btn btn-default rseqc-junction_sat_single_prevnext" data-action="next">Next &raquo;</button>               </div>             </div>             <div class="hc-plot-wrapper">               <div class="hc-plot hc-line-plot">                 <small>loading..</small>               </div>             </div>           </div>\');\n        var pwrapper = rseqc_junction_saturation_plot.parent().parent();\n        newplot.insertAfter(pwrapper).hide().slideDown();\n        pwrapper.slideUp();\n        junction_sat_single_hint.slideUp();\n\n        // Listener to return to overview\n        newplot.find(\'#rseqc-junction_sat_single_return\').click(function(e){\n          e.preventDefault();\n          newplot.slideUp(function(){\n            $(this).remove();\n          });\n          pwrapper.slideDown();\n          junction_sat_single_hint.slideDown();\n        });\n\n        // Listeners for previous / next plot\n        newplot.find(\'.rseqc-junction_sat_single_prevnext\').click(function(e){\n          e.preventDefault();\n          if($(this).data(\'action\') == \'prev\'){\n            k--;\n            if(k < 0){\n              k = mqc_plots[rseqc_junction_saturation_plot_id][\'datasets\'][0].length - 1;\n            }\n          } else {\n            k++;\n            if(k >= mqc_plots[rseqc_junction_saturation_plot_id][\'datasets\'][0].length){\n              k = 0;\n            }\n          }\n          var hc = newplot.find(\'.hc-plot\').highcharts();\n          for (var i = 0; i < 3; i++) {\n              hc.series[i].setData(mqc_plots[rseqc_junction_saturation_plot_id][\'datasets\'][i][k][\'data\'], false);\n          }\n          var ptitle = \'RSeQC Junction Saturation: \'+mqc_plots[rseqc_junction_saturation_plot_id][\'datasets\'][0][k][\'name\'];\n          hc.setTitle({text: ptitle});\n          hc.redraw({ duration: 200 });\n        });\n\n        // Plot the single data\n        newplot.find(\'.hc-plot\').highcharts({\n          chart: {\n            type: \'line\',\n            zoomType: \'x\'\n          },\n          colors: [\'blue\',\'red\',\'green\'],\n          title: {\n            text: \'RSeQC Junction Saturation: \'+this.series.name,\n            x: 30 // fudge to center over plot area rather than whole plot\n          },\n          xAxis: {\n            title: { text: \'Percent of total reads\' },\n            allowDecimals: false,\n          },\n          yAxis: {\n            title: { text: \'Number of observed splicing junctions\' },\n            min: 0,\n          },\n          legend: {\n            floating: true,\n            layout: \'vertical\',\n            align: \'left\',\n            verticalAlign: \'top\',\n            x: 60,\n            y: 40\n          },\n          tooltip: {\n            shared: true,\n            crosshairs: true,\n            headerFormat: \'<strong>{point.key}% of reads</strong><br/>\'\n          },\n          plotOptions: {\n            series: {\n              animation: false,\n              lineWidth: 1,\n              marker: {\n                lineColor: null,\n                fillColor: \'transparent\',\n                lineWidth: 1,\n                symbol: \'circle\'\n              },\n            }\n          },\n          exporting: { buttons: { contextButton: {\n            menuItems: window.HCDefaults.exporting.buttons.contextButton.menuItems,\n            onclick: window.HCDefaults.exporting.buttons.contextButton.onclick\n          } } },\n          series: data\n        });\n    }\n    '