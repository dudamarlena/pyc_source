# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chirp\misc\pitchstats.py
# Compiled at: 2013-12-11 23:17:46
"""
calculate summary statistics from plg files

Copyright (C) 2011 Daniel Meliza <dan // meliza.org>
Created 2010-04-27
"""
_scriptdoc = 'cpitchstats [-c <config.cfg>] <plg-files>\n\nCalculate summary statistics about pitch for each of <plg-files>\n\nOutput is to stdout. See documentation for config file details.\n'
import os
from chirp.common.config import _configurable

class summary(_configurable):
    options = dict(estimator='p.map')
    config_options = ('pitchstats', )
    template = ('%(file)s', '%(nelements)d', '%(duration)3.2f', '%(pitch.mean)3.4f',
                '%(pitch.std)3.4f', '%(pitch.median)3.4f', '%(pitch.max)3.4f', '%(pitch.min)3.4f',
                '%(pow.mean)3.4f', '%(dropped.points)d')
    header = ('file', 'nelements', 'duration', 'mean', 'std', 'median', 'max', 'min',
              'pow', 'dropped')

    def __init__(self, configfile=None, **kwargs):
        """ Initialize the object with a config file """
        from chirp.common import postfilter
        self.readconfig(configfile)
        self.options.update(kwargs)
        self.postfilter = postfilter.pitchfilter(configfile, **kwargs)

    def __call__(self, plgfile):
        """
        Calculate summary statistics for the input file.  Returns a
        dictionary if the operation succeeded; raises a ValueError object if
        not.
        """
        import numpy as nx
        from chirp.common import plg
        estimator = self.options['estimator']
        p = plg.read(plgfile)
        if estimator not in p.dtype.names:
            raise ValueError, 'estimator %s is missing' % estimator
        ind = self.postfilter(p)
        ind &= nx.isfinite(p[estimator])
        pfilt = p[ind]
        pitch = pfilt[estimator]
        if pfilt.size == 0:
            raise ValueError('no valid points after filtering')
        return {'nelements': nx.unique(pfilt['element']).size, 'duration': pfilt['time'].max() - pfilt['time'].min(), 
           'pitch.mean': nx.mean(pitch), 
           'pitch.std': nx.std(pitch), 
           'pitch.median': nx.median(pitch), 
           'pitch.max': nx.max(pitch), 
           'pitch.min': nx.min(pitch), 
           'pow.mean': nx.mean(pfilt['stim.pow']), 
           'dropped.points': p.size - pfilt.size}

    def summarize(self, files, cout, delim='\t', header=True):
        """
        Calculate summary statistics for a bunch of files and output to a stream.
        """
        if header:
            cout.write(delim.join(self.header))
            cout.write('\n')
        for f in files:
            basename = os.path.split(os.path.splitext(f)[0])[1]
            try:
                pstats = self(f)
                pstats['file'] = basename
                cout.write(delim.join(self.template) % pstats)
                cout.write('\n')
            except Exception as e:
                if delim == ',':
                    cout.write('%s, ERROR,%s\n' % (basename, e))
                else:
                    cout.write('# Error in %s: %s\n' % (basename, e))


def main(argv=None, cout=None, cerr=None, **kwargs):
    import sys
    from chirp.version import version
    if argv is None:
        argv = sys.argv[1:]
    if cout is None:
        cout = sys.stdout
    if cerr is None:
        cerr = sys.stderr
    import getopt
    from chirp.common.config import configoptions
    config = configoptions()
    opts, args = getopt.getopt(argv, 'hvc:m:')
    if len(args) < 1:
        print _scriptdoc
        return -1
    else:
        for o, a in opts:
            if o == '-h':
                print _scriptdoc
                return -1
            if o == '-v':
                print 'cpitchstats version %s' % version
                return -1
            if o == '-c':
                config.read(a)

        print >> cout, '* Program: cpitchstats'
        print >> cout, '** Version: %s' % version
        summary(config).summarize(args, cout, header=True)
        return 0