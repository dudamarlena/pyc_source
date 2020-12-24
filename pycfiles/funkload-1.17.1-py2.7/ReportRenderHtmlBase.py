# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/ReportRenderHtmlBase.py
# Compiled at: 2015-05-06 05:03:08
"""Html rendering

$Id$
"""
import os
from shutil import copyfile
from ReportRenderRst import RenderRst, rst_title

class RenderHtmlBase(RenderRst):
    """Render stats in html.

    Simply render stuff in ReST then ask docutils to build an html doc.
    """
    chart_size = (350, 250)
    big_chart_size = (640, 480)

    def __init__(self, config, stats, error, monitor, monitorconfig, options, css_file=None):
        RenderRst.__init__(self, config, stats, error, monitor, monitorconfig, options)
        self.css_file = css_file
        self.quiet = options.quiet
        self.report_dir = self.css_path = self.rst_path = self.html_path = None
        return

    def getChartSize(self, cvus):
        """Compute the right size lenght depending on the number of cvus."""
        size = list(self.chart_size)
        len_cvus = len(cvus)
        chart_size = self.chart_size
        big_chart_size = self.big_chart_size
        if len_cvus * 50 > chart_size[0]:
            if len_cvus * 50 < big_chart_size:
                return (len_cvus * 50, big_chart_size[1])
            return big_chart_size
        return chart_size

    def generateReportDirectory(self, output_dir):
        """Generate a directory name for a report."""
        config = self.config
        stamp = config['time'][:19].replace(':', '')
        stamp = stamp.replace('-', '')
        if config.get('label', None) is None:
            report_dir = os.path.join(output_dir, '%s-%s' % (
             config['id'], stamp))
        else:
            report_dir = os.path.join(output_dir, '%s-%s-%s' % (
             config['id'], stamp, config.get('label')))
        return report_dir

    def prepareReportDirectory(self):
        """Create a report directory."""
        if self.options.report_dir:
            report_dir = os.path.abspath(self.options.report_dir)
        else:
            output_dir = os.path.abspath(self.options.output_dir)
            if not os.access(output_dir, os.W_OK):
                os.mkdir(output_dir, 509)
            report_dir = self.generateReportDirectory(output_dir)
        if not os.access(report_dir, os.W_OK):
            os.mkdir(report_dir, 509)
        self.report_dir = report_dir

    def createRstFile(self):
        """Create the ReST file."""
        rst_path = os.path.join(self.report_dir, 'index.rst')
        f = open(rst_path, 'w')
        f.write(unicode(self).encode('utf-8'))
        f.close()
        self.rst_path = rst_path

    def copyCss(self):
        """Copy the css to the report dir."""
        css_file = self.css_file
        if css_file is not None:
            css_filename = os.path.split(css_file)[(-1)]
            css_dest_path = os.path.join(self.report_dir, css_filename)
            copyfile(css_file, css_dest_path)
        else:
            from pkg_resources import resource_string
            css_content = resource_string('funkload', 'data/funkload.css')
            css_dest_path = os.path.join(self.report_dir, 'funkload.css')
            f = open(css_dest_path, 'w')
            f.write(css_content)
            f.close()
        self.css_path = css_dest_path
        return

    def copyXmlResult(self):
        """Make a copy of the xml result."""
        xml_src_path = self.options.xml_file
        xml_dest_path = os.path.join(self.report_dir, 'funkload.xml')
        copyfile(xml_src_path, xml_dest_path)

    def generateHtml(self):
        """Ask docutils to convert our rst file into html."""
        from docutils.core import publish_cmdline
        html_path = os.path.join(self.report_dir, 'index.html')
        cmdline = []
        if self.quiet:
            cmdline.append('-q')
        cmdline.extend(['-t', '--stylesheet-path', self.css_path,
         self.rst_path, html_path])
        publish_cmdline(writer_name='html', argv=cmdline)
        self.html_path = html_path

    def render(self):
        """Create the html report."""
        self.prepareReportDirectory()
        self.createRstFile()
        self.copyCss()
        try:
            self.generateHtml()
        except ImportError:
            print 'WARNING docutils not found, no html output.'
            return ''

        self.createCharts()
        self.copyXmlResult()
        return os.path.abspath(self.html_path)

    __call__ = render

    def createCharts(self):
        """Create all charts."""
        self.createTestChart()
        self.createPageChart()
        self.createAllResponseChart()
        for step_name in self.steps:
            self.createResponseChart(step_name)

    def createMonitorCharts(self):
        """Create all montirored server charts."""
        if not self.monitor or not self.with_chart:
            return
        self.append(rst_title('Monitored hosts', 2))
        charts = {}
        for host in self.monitor.keys():
            charts[host] = self.createMonitorChart(host)

        return charts

    def createTestChart(self):
        """Create the test chart."""
        pass

    def createPageChart(self):
        """Create the page chart."""
        pass

    def createAllResponseChart(self):
        """Create global responses chart."""
        pass

    def createResponseChart(self, step):
        """Create responses chart."""
        pass

    def createMonitorChart(self, host):
        """Create monitrored server charts."""
        pass