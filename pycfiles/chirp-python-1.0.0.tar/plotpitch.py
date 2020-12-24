# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\misc\plotpitch.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = '\nPlot spectrograms and overlaid pitch traces of a collection of signals.\n\nUsage:\ncplotpitch [-c CONFIG] [-p PITCHDIR] [-@] FILES OUTFILE\n\nFILES   a collection of wave files to plot. If a plg file with the same\n        basename exists in PITCHDIR, plots the overlaid pitch trace\n\nOptional arguments:\n\n-c       specify a chirp.cfg file with configurable options\n-@       plot files from standard in (separated by newlines)\n         instead of command line (useful for pipes from find, etc)\n-p       look for pitch files in PITCHDIR (default same directory as each file)\n'
_scriptname = 'cplotpitch'
import os, numpy as nx, matplotlib
from chirp.common.config import configoptions, _configurable
from chirp.common import postfilter, _tools
figparams = {'dpi': 300}
matplotlib.rc('font', size=10)
matplotlib.rc('xtick', labelsize=8)
matplotlib.rc('ytick', labelsize=8)
matplotlib.rc('axes', labelsize=10, titlesize=10)
matplotlib.rc('ytick.major', size=2)
matplotlib.rc('xtick.major', size=2)
matplotlib.rc('figure.subplot', top=0.95, hspace=0.35)
_figsize = (11, 6)
_nrows = 6
_ncols = 3

def load_data(basename, filterer=None, pitchdir=None):
    """
    Load data from wav and plg files. If filterer is not None, filters
    pitch trace.
    """
    from ewave import wavfile
    from chirp.common import plg
    fp = wavfile(basename + '.wav')
    signal, Fs = fp.read(), fp.sampling_rate
    if isinstance(pitchdir, basestring):
        plgfile = os.path.join(pitchdir, os.path.split(basename)[1] + '.plg')
    else:
        plgfile = basename + '.plg'
    if not os.path.exists(plgfile):
        return (signal, Fs / 1000.0, None, None)
    else:
        pitch = plg.read(plgfile)
        if filterer is not None:
            ind = postfilter.ind_endpoints(filterer(pitch))
            if ind is None:
                return (signal, Fs / 1000.0, None, None)
            pitch = pitch[ind[0]:ind[1] + 1]
        t = pitch['time']
        if 'p.map' in pitch.dtype.names:
            p = pitch['p.map']
        else:
            p = pitch['p.mmse']
        return (signal, Fs / 1000.0, t, p)


class plotter(_configurable):
    options = dict(colormap='Greys', dynrange=60, freq_range=(750.0, 10000.0), pitch_color='r')
    config_sections = ('spectrogram', 'cplotpitch')

    def __init__(self, configfile=None):
        self.readconfig(configfile)

    def plot_spectrogram(self, ax, spec, extent):
        from matplotlib import cm
        cmap = getattr(cm, self.options['colormap'])
        img = ax.imshow(spec, extent=extent, cmap=cmap, origin='lower')
        Smax = spec.max()
        img.set_clim((Smax - self.options['dynrange'] / 10, Smax))
        ax.set_ylim(tuple(f / 1000.0 for f in self.options['freq_range']))
        return img

    def plot_trace(self, ax, t, p):
        ax.hold(True)
        p = ax.plot(t, p, self.options['pitch_color'])
        ax.hold(False)
        return p


@_tools.consumer
def multiplotter(outfile, config, cout=None, show_pitch=True, pitchdir=None):
    """
    A coroutine for plotting a bunch of motifs on the same page. A
    useful entry point for scripts that want to do something similar
    to cplotpitch, but with control over which motifs get plotted.
    """
    matplotlib.use('PDF')
    from matplotlib.backends.backend_pdf import PdfPages as multipdf
    from matplotlib.pyplot import close as close_figure
    from chirp.version import version
    from chirp.common.graphics import axgriditer
    from chirp.common.signal import spectrogram

    def gridfun(**kwargs):
        from matplotlib.pyplot import subplots
        return subplots(_nrows, _ncols, sharex=True, sharey=True, figsize=_figsize)

    def figfun(fig):
        maxx = max(ax.dataLim.x1 for ax in fig.axes)
        ax = fig.axes[0]
        ax.set_xticklabels('')
        ax.set_yticklabels('')
        ax.set_xlim(0, maxx)
        for ax in fig.axes:
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')

        fig.subplots_adjust(left=0.05, right=0.95, wspace=0)
        pp.savefig(fig)
        close_figure(fig)

    pp = multipdf(outfile)
    axg = axgriditer(gridfun, figfun)
    spectrogram = spectrogram(configfile=config)
    plt = plotter(configfile=config)
    filt = postfilter.pitchfilter(configfile=config)
    print >> cout, filt.options_str()
    print >> cout, '* Plotting signals:'
    try:
        ax = None
        while 1:
            basename = yield ax
            ax = axg.next()
            try:
                signal, Fs, t, p = load_data(basename, filt, pitchdir)
                print >> cout, '** %s' % basename
            except Exception as e:
                print >> cout, '** %s: error loading data (%s)' % (basename, e)
                continue

            spec, extent = spectrogram.dbspect(signal, Fs)
            plt.plot_spectrogram(ax, spec, extent)
            if show_pitch and t is not None:
                plt.plot_trace(ax, t, p)

    finally:
        axg.close()
        pp.close()

    return


def main(argv=None, cout=None):
    import sys, getopt, glob
    from chirp.version import version
    if argv is None:
        argv = sys.argv[1:]
    if cout is None:
        cout = sys.stdout
    signals = None
    pitchdir = None
    config = configoptions()
    opts, args = getopt.getopt(sys.argv[1:], 'c:p:hv@')
    for o, a in opts:
        if o == '-h':
            print __doc__
            return -1
        if o == '-v':
            print '%s version %s' % (_scriptname, version)
            return -1
        if o == '-p':
            pitchdir = a
        elif o == '-c':
            if not os.path.exists(a):
                print >> cout, "ERROR: config file %s doesn't exist" % a
                return -1
            config.read(a)
        elif o == '-@':
            signals = (f.strip() for f in sys.stdin.readlines())

    if len(args) < 1:
        print __doc__
        sys.exit(-1)
    if not signals:
        if len(args) < 2:
            print __doc__
            sys.exit(-1)
        signals = args[:-1]
    print >> cout, '* Program: cplotpitch'
    print >> cout, '** Version: %s' % version
    print >> cout, '** Loading pitch from %s' % (pitchdir or 'same directory as signal')
    print >> cout, '** Output file: %s' % args[(-1)]
    plotter = multiplotter(args[(-1)], config, cout, pitchdir=pitchdir)
    for fname in signals:
        basename = os.path.splitext(fname)[0]
        ax = plotter.send(basename)
        ax.set_title(basename, ha='left', position=(0.0, 1.0), fontsize=4)

    return 0