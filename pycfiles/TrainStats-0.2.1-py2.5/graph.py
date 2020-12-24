# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/trainstats/graph.py
# Compiled at: 2009-02-03 08:38:42
import os, subprocess, Gnuplot

class Graph(object):
    PNG_SIZE = (640, 480)
    GDFONTPATH = '/usr/share/fonts/TTF/'
    FONT = ('DejaVuSans', 10)

    def __init__(self):
        if not os.path.isdir(self.GDFONTPATH):
            print 'WARNING: GDFONTPATH points to a non-existant directory'
        os.environ['GDFONTPATH'] = self.GDFONTPATH

    def _initGnuplot(self, output_file):
        g = Gnuplot.Gnuplot()
        if self.FONT is not None:
            g('set terminal png font %s size %s enhanced' % ((' ').join([ str(i) for i in self.FONT ]), (',').join([ str(i) for i in self.PNG_SIZE ])))
        else:
            g('set terminal png size %s enhanced' % (',').join([ str(i) for i in self.PNG_SIZE ]))
        g('set output "%s"' % output_file)
        return g

    def daily(self, tid, day, data, output_file):
        g = self._initGnuplot(output_file)
        g('set data style linespoints')
        g('set nokey')
        g('set grid')
        title = 'Ritardo treno %s - %s' % (tid, day.strftime('%A %d %B %Y'))
        g.title(title)
        g('set xtics rotate')
        g('set xzeroaxis linetype -1 linewidth .5')
        g.ylabel('Ritardo (min)')
        xtics = []
        for tic in [ tup[0] for tup in data ]:
            tup = '"%s" %d' % (tic, len(xtics))
            xtics.append(tup)

        g('set xtics (%s)' % (',').join(xtics))
        vals = [ tup[3] for tup in data ]
        g.plot(vals)

    def aggregate_delay(self, tid, data_min, data_avg, data_max, output_file):
        g = self._initGnuplot(output_file)
        g('set data style linespoints')
        g('set pointsize 1.5')
        g('set key box')
        g('set grid')
        g('set xtics rotate')
        g('set xzeroaxis linetype -1 linewidth .5')
        assert len(data_min) == len(data_avg)
        assert len(data_min) == len(data_max)
        xtics = []
        for tic in [ tup[0] for tup in data_min ]:
            tup = '"%s" %d' % (tic, len(xtics))
            xtics.append(tup)

        g('set xtics (%s)' % (',').join(xtics))
        g.ylabel('Ritardo (min)')
        if data_min is not None:
            vals = [ tup[1] for tup in data_min ]
            pi_min = Gnuplot.Data(vals, title='Ritardo minimo')
        if data_avg is not None:
            vals = [ tup[1] for tup in data_avg ]
            pi_avg = Gnuplot.Data(vals, title='Ritardo medio')
        if data_max is not None:
            vals = [ tup[1] for tup in data_max ]
            pi_max = Gnuplot.Data(vals, title='Ritardo massimo')
        g.replot(pi_min, pi_avg, pi_max)
        return


if __name__ == '__main__':
    import datetime, locale
    try:
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
    except Exception, e:
        print 'Cannot set locale: %s' % e.message
    else:
        g = Graph()
        g.daily(400, datetime.date.today(), [('milano', 10), ('roma', 5)], 'test.png')