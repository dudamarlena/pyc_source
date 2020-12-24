# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tcsv2png/tcsv2png.py
# Compiled at: 2011-04-14 03:20:05
"""Produces a png from timed csv file (csv file with a time column)
Scales the data to show all of the data sets in the same chart.
"""
import sys, os, re
from math import log10, ceil
from tempfile import mkdtemp
from commands import getstatusoutput
from optparse import OptionParser, TitledHelpFormatter
USAGE = 'tcsv2png [Options] CSV_FILE [COL0 [COLi ...]]\n\n        tcsv2png uses gnuplot to convert a csv file with a time column\n\tformat %H:%m:%S into a chart in png format.\n\n\tIt scales the data to show all of the data sets in the same\n\tpng chart.\n\n        You can select the columns of interest. The tool uses gnuplot\n        to generate the chart, so you can customize the script to your\n        need.\n\n        CSV_FILE: a csv file with TAB fields separator\n        COL0:     the column indice that contains the time formated H:M:S\n        COLi:     column indice to plot\n\n        Note that column indice starts with 0 and that the first line\n        should contains columns headers.\n\nExamples\n========\n  tcsv2png data.csv \n          Creates data.png file with all the columns, assuming\n          column 0 is the time column.\n\n  tcsv2png -v -c -t "Foo title" -o foo.png  data.csv 0 3 5\n          Creates foo.png chart with "Foo title" title, column 0 is\n\t  the time column, plotting column 3 and 5 using smooth\n\t  csplines rendering.\n\n  tcsv2png -h\n          Gives you the available options.\n'

def get_version():
    """Retrun the FunkLoad package version."""
    from pkg_resources import get_distribution
    return get_distribution('tcsv2png').version


def command(cmd, do_raise=True, verbose=False):
    """Return the status, output as a line list."""
    extra = 'LC_ALL=C '
    if verbose:
        print 'Run: ' + extra + cmd
    (status, output) = getstatusoutput(extra + cmd)
    if status:
        if do_raise:
            print 'ERROR: [%s] return status: [%d], output: [%s]' % (
             extra + cmd, status, output)
            raise RuntimeError('Invalid return code: %s' % status)
        elif verbose:
            print 'return status: [%d]' % status
    if output:
        output = output.split('\n')
    return (
     status, output)


def to_float(text):
    """Filter input to float format."""
    if text == 'Infinity':
        return 0
    try:
        x = float(text.replace(',', '.'))
    except ValueError:
        x = 0

    return x


def scale(s):
    if not s:
        return 1
    sc = ceil(log10(abs(s) / 110.0))
    res = 1
    for x in range(int(abs(sc))):
        res = res * 10

    if sc < 0:
        ret = res
    else:
        ret = 1.0 / res
    if int(ret) == ret:
        return int(ret)
    return ret


class GnuPlotScript:
    csv_path = None
    cols = []
    tmp_dir = None
    script_path = None
    script_header_tpl = 'set terminal png size 1024,768\nset output "%s"\nset title "%s"\nset xdata time\nset timefmt "%%H:%%M:%%S"\nset format x "%%H:%%M"\nset yrange [0:105]\nset grid\nset datafile missing "NaN"\nset datafile missing "Infinity"\ncd "%s"\n'
    script_line_tpl = '"%s" using %s:(%s*$%s) with lines title "%s * %s" %s'

    def __init__(self, csv_path, cols, options):
        self.csv_path = csv_path
        self.cols = cols
        self.png_path = options.output
        self.verbose = options.verbose
        tmp_dir = mkdtemp(prefix='tcsv2png_')
        if not os.access(tmp_dir, os.W_OK):
            os.mkdir(tmp_dir, 509)
        if self.verbose:
            print 'Using tmp dir: ' + tmp_dir
        self.tmp_dir = tmp_dir
        self.script_path = os.path.join(tmp_dir, 'script.gplot')
        self.script_file = open(self.script_path, 'w')
        self.script_file.write(self.script_header_tpl % (self.png_path,
         options.title,
         tmp_dir))
        if options.bezier:
            self.smooth = 'smooth bezier'
        elif options.csplines:
            self.smooth = 'smooth csplines'
        else:
            self.smooth = ''

    def process(self):
        csv_path = self.csv_path
        if self.verbose:
            print 'Processing: ' + csv_path
        cols = self.cols
        script_file = self.script_file
        csv = open(csv_path)
        titles = None
        data_path = os.path.join(self.tmp_dir, ('.').join([
         os.path.splitext(os.path.basename(csv_path))[0], 'dat']))
        data_file = open(data_path, 'w')
        maxes = []
        for x in cols[1:]:
            maxes.append(0)

        lines = []
        count = 0
        line = csv.readline()
        last_hour = 0
        while line:
            count += 1
            if line is None:
                break
            row = re.split('[\\ \t;]+', line)
            if len(cols) == 0:
                cols = range(len(row))
                for x in cols[1:]:
                    maxes.append(0)

            try:
                values = [ row[x].strip() for x in cols ]
            except IndexError:
                print 'WARN: Skip invalid line %d: %s' % (count, line)
                line = csv.readline()
                continue

            if titles is None:
                titles = values
            else:
                hour = int(values[0][:2])
                if hour < last_hour:
                    hour += 24
                    values[0] = str(hour) + values[0][2:]
                last_hour = hour
                data_file.write((' ').join(values) + '\n')
                maxes = [ max(maxes[i], to_float(x)) for (i, x) in enumerate(values[1:])
                        ]
            line = csv.readline()

        data_file.close()
        script_file.write('# cols  ' + str(titles[1:]) + '\n')
        script_file.write('# maxes ' + str(maxes) + '\n')
        i = 0
        lines = []
        for title in titles[1:]:
            lines.append(self.script_line_tpl % (data_path,
             cols[0] + 1,
             scale(maxes[i]), i + 2,
             scale(maxes[i]), title,
             self.smooth))
            i += 1

        script_file.write('plot ' + (',').join(lines) + '\n')
        script_file.close()
        command('gnuplot %s' % self.script_path, self.verbose)
        print '%s done.' % os.path.abspath(self.png_path)
        return


def main():
    """Main test"""
    global USAGE
    parser = OptionParser(USAGE, formatter=TitledHelpFormatter(), version='tcsv2png %s' % get_version())
    parser.add_option('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_option('-o', '--output', type='string', help='PNG output file')
    parser.add_option('-t', '--title', type='string', help='Chart title')
    parser.add_option('-b', '--bezier', action='store_true', help='Smooth bezier')
    parser.add_option('-c', '--csplines', action='store_true', help='Smooth csplines')
    (options, args) = parser.parse_args(sys.argv)
    if len(args) in (1, 3):
        parser.error('Missing options')
        return
    if not options.output:
        options.output = os.path.splitext(args[1])[0] + '.png'
    if not options.title:
        options.title = args[1]
    try:
        cols = [ int(col) for col in args[2:] ]
    except ValueError:
        parser.error('ERROR: Expecting indices for column parameters Got: ' + str(args[2:]))
        return

    script = GnuPlotScript(args[1], cols, options)
    script.process()


if __name__ == '__main__':
    main()