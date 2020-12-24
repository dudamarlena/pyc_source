# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/ReportRenderDiff.py
# Compiled at: 2015-05-06 05:03:08
"""Classes that render a differential report

$Id$
"""
import os
from ReportRenderRst import rst_title
from ReportRenderHtmlBase import RenderHtmlBase
from ReportRenderHtmlGnuPlot import gnuplot

def getReadableDiffReportName(a, b):
    """Return a readeable diff report name using 2 reports"""
    a = os.path.basename(a)
    b = os.path.basename(b)
    if a == b:
        return 'diff_' + a + '_vs_idem'
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            break

    for i in range(i, 0, -1):
        if a[i] not in '_-0123456789':
            i += 1
            break

    r = b[:i] + '_' + b[i:] + '_vs_' + a[i:]
    if r.startswith('test_'):
        r = r[5:]
    r = r.replace('-_', '_')
    r = r.replace('_-', '_')
    r = r.replace('__', '_')
    return 'diff_' + r


def getRPath(a, b):
    """Return a relative path of b from a."""
    a_path = a.split('/')
    b_path = b.split('/')
    for i in range(min(len(a_path), len(b_path))):
        if a_path[i] != b_path[i]:
            break

    return '../' * len(a_path[i:]) + ('/').join(b_path[i:])


class RenderDiff(RenderHtmlBase):
    """Differential report."""
    report_dir1 = None
    report_dir2 = None
    header = None
    sep = ', '
    data_file = None
    output_dir = None
    script_file = None

    def __init__(self, report_dir1, report_dir2, options, css_file=None):
        self.report_dir1 = os.path.abspath(report_dir1).replace('\\', '/')
        self.report_dir2 = os.path.abspath(report_dir2).replace('\\', '/')
        self.options = options
        self.css_file = css_file
        self.quiet = options.quiet

    def generateReportDirectory(self, output_dir):
        """Generate a directory name for a report."""
        output_dir = os.path.abspath(output_dir)
        report_dir = os.path.join(output_dir, getReadableDiffReportName(self.report_dir1, self.report_dir2))
        if not os.access(report_dir, os.W_OK):
            os.mkdir(report_dir, 509)
        return report_dir

    def createCharts(self):
        """Render stats."""
        self.createGnuplotData()
        self.createGnuplotScript()
        gnuplot(self.script_file)

    def createRstFile(self):
        """Create the ReST file."""
        rst_path = os.path.join(self.report_dir, 'index.rst')
        lines = []
        b1 = os.path.basename(self.report_dir1)
        b2 = os.path.basename(self.report_dir2)
        b1_rpath = getRPath(self.report_dir.replace('\\', '/'), os.path.join(self.report_dir1, 'index.html').replace('\\', '/'))
        b2_rpath = getRPath(self.report_dir.replace('\\', '/'), os.path.join(self.report_dir2, 'index.html').replace('\\', '/'))
        if b1 == b2:
            b2 = b2 + '(2)'
        lines.append(rst_title('FunkLoad_ differential report', level=0))
        lines.append('')
        lines.append('.. sectnum::    :depth: 2')
        lines.append('')
        lines.append(rst_title('%s vs %s' % (b2, b1), level=1))
        lines.append(' * Reference bench report **B1**: `' + b1 + ' <' + b1_rpath + '>`_ [#]_')
        lines.append(' * Challenger bench report **B2**: `' + b2 + ' <' + b2_rpath + '>`_ [#]_')
        lines.append('')
        lines.append(rst_title('Requests', level=2))
        lines.append(' .. image:: rps_diff.png')
        lines.append(' .. image:: request.png')
        lines.append(rst_title('Pages', level=2))
        lines.append(' .. image:: spps_diff.png')
        escapeReportDir = lambda rd: rd.replace('\\', '/').replace('_', '\\_')
        lines.append(' .. [#] B1 path: ' + escapeReportDir(self.report_dir1))
        lines.append(' .. [#] B2 path: ' + escapeReportDir(self.report_dir2))
        lines.append(' .. _FunkLoad: http://funkload.nuxeo.org/')
        lines.append('')
        f = open(rst_path, 'w')
        f.write(('\n').join(lines))
        f.close()
        self.rst_path = rst_path

    def copyXmlResult(self):
        pass

    def __repr__(self):
        return self.render()

    def extract_stat(self, tag, report_dir):
        """Extract stat from the ReST index file."""
        lines = open(os.path.join(report_dir, 'index.rst')).readlines()
        try:
            idx = lines.index('%s stats\n' % tag)
        except ValueError:
            print 'ERROR tag %s not found in rst report %s' % (tag, report_dir)
            return []

        delim = 0
        ret = []
        for line in lines[idx:]:
            if line.startswith(' ====='):
                delim += 1
                continue
            if delim == 1:
                self.header = line.strip().split()
            if delim < 2:
                continue
            if delim == 3:
                break
            ret.append([ x.replace('%', '') for x in line.strip().split() ])

        return ret

    def createGnuplotData(self):
        """Render rst stat."""

        def output_stat(tag, rep):
            stat = self.extract_stat(tag, rep)
            text = []
            text.append('# ' + tag + ' stat for: ' + rep)
            text.append('# ' + (' ').join(self.header))
            for line in stat:
                text.append((' ').join(line))

            return ('\n').join(text)

        def output_stat_diff(tag, rep1, rep2):
            stat1 = self.extract_stat(tag, rep1)
            stat2 = self.extract_stat(tag, rep2)
            text = []
            text.append('# ' + tag + ' stat for: ' + rep1 + ' and ' + rep2)
            text.append('# ' + (' ').join(self.header) + ' ' + (' ').join([ x + '-2' for x in self.header ]))
            for s1 in stat1:
                for s2 in stat2:
                    if s1[0] == s2[0]:
                        text.append((' ').join(s1) + ' ' + (' ').join(s2))
                        break

                if s1[0] != s2[0]:
                    text.append((' ').join(s1))

            return ('\n').join(text)

        rep1 = self.report_dir1
        rep2 = self.report_dir2
        data_file = os.path.join(self.report_dir, 'diffbench.dat')
        self.data_file = data_file
        f = open(data_file, 'w')
        f.write('# ' + rep1 + ' vs ' + rep2 + '\n')
        for tag, rep in (('Page', rep1), ('Page', rep2),
         (
          'Request', rep1), ('Request', rep2)):
            f.write(output_stat(tag, rep) + '\n\n\n')

        f.write(output_stat_diff('Page', rep1, rep2) + '\n\n\n')
        f.write(output_stat_diff('Request', rep1, rep2))
        f.close()

    def createGnuplotScript(self):
        """Build gnuplot script"""
        script_file = os.path.join(self.report_dir, 'script.gplot')
        self.script_file = script_file
        f = open(script_file, 'w')
        rep1 = self.report_dir1
        rep2 = self.report_dir2
        f.write('# ' + rep1 + ' vs ' + rep2 + '\n')
        f.write('# COMMON SETTINGS\nset grid  back\nset xlabel "Concurrent Users"\nset boxwidth 0.9 relative\nset style fill solid 1\n\n# SPPS\nset output "spps_diff.png"\nset terminal png size 640,380\nset title "Successful Pages Per Second"\nset ylabel "SPPS"\nplot "diffbench.dat" i 4 u 1:4:19 w filledcurves above t "B2<B1", "" i 4 u 1:4:19 w filledcurves below t "B2>B1", "" i 4 u 1:4 w lines lw 2 t "B1", "" i 4 u 1:19 w lines lw 2 t "B2"\n\n# RPS\nset output "rps_diff.png"\nset terminal png size 640,380\nset multiplot title "Requests Per Second (Scalability)"\nset title "Requests Per Second" offset 0, -2\nset size 1, 0.67\nset origin 0, 0.3\nset ylabel ""\nset format x ""\nset xlabel ""\nplot "diffbench.dat" i 5 u 1:4:19 w filledcurves above t "B2<B1", "" i 5 u 1:4:19 w filledcurves below t "B2>B1", "" i 5 u 1:4 w lines lw 2 t "B1", "" i 5 u 1:19 w lines lw 2 t "B2"\n\n# % RPS\nset title "RPS B2/B1 %"  offset 0, -2\nset size 1, 0.33\nset origin 0, 0\nset format y "% g%%"\nset format x "% g"\nset xlabel "Concurrent Users"\n\nplot "diffbench.dat" i 5 u 1:($19<$4?((($19*100)/$4) - 100): 0) w boxes notitle, "" i 5 u 1:($19>=$4?((($19*100)/$4)-100): 0) w boxes notitle\nunset multiplot\n\n\n# RESPONSE TIMES\nset output "request.png"\nset terminal png size 640,640\nset multiplot title "Request Response time (Velocity)"\n\n# AVG\nset title "Average"  offset 0, -2\nset size 0.5, 0.67\nset origin 0, 0.30\nset ylabel ""\nset format y "% gs"\nset xlabel ""\nset format x ""\nplot "diffbench.dat" i 5 u 1:25:10 w filledcurves above t "B2<B1", "" i 5 u 1:25:10 w filledcurves below t "B2>B1", "" i 5 u 1:10 w lines lw 2 t "B1", "" i 5 u 1:25 w lines lw 2 t "B2\n\n# % AVG\nset title "Average B1/B2 %"  offset 0, -2\nset size 0.5, 0.31\nset origin 0, 0\nset format y "% g%%"\nset format x "% g"\nset xlabel "Concurrent Users"\nplot "diffbench.dat" i 5 u 1:($25>$10?((($10*100)/$25) - 100): 0) w boxes notitle, "" i 5 u 1:($25<=$10?((($10*100)/$25) - 100): 0) w boxes notitle\n\n# MEDIAN\nset size 0.5, 0.31\nset format y "% gs"\nset xlabel ""\nset format x ""\n\nset title "Median"\nset origin 0.5, 0.66\nplot "diffbench.dat" i 5 u 1:28:13 w filledcurves above notitle, "" i 5 u 1:28:13 w filledcurves below notitle, "" i 5 u 1:13 w lines lw 2 notitle, "" i 5 u 1:28 w lines lw 2 notitle\n\n# P90\nset title "p90"\nset origin 0.5, 0.33\nplot "diffbench.dat" i 5 u 1:29:14 w filledcurves above notitle, "" i 5 u 1:29:14 w filledcurves below notitle, "" i 5 u 1:14 w lines lw 2 notitle, "" i 5 u 1:29 w lines lw 2 notitle\n\n# MAX\nset title "Max"\nset origin 0.5, 0\nset format x "% g"\nset xlabel "Concurrent Users"\nplot "diffbench.dat" i 5 u 1:26:11 w filledcurves above notitle, "" i 5 u 1:26:11 w filledcurves below notitle, "" i 5 u 1:11 w lines lw 2 notitle, "" i 5 u 1:26 w lines lw 2 notitle\nunset multiplot\n')
        f.close()