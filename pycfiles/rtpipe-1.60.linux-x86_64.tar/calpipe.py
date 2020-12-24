# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbe-master/realfast/anaconda/envs/deployment/lib/python2.7/site-packages/rtpipe/calpipe.py
# Compiled at: 2016-10-24 18:03:36
try:
    import tasklib as tl
except ImportError:
    import pwkit.environments.casa.tasks as tl

import rtpipe.parsesdm as ps, os, string, glob, sdmpy
from collections import OrderedDict

class pipe(object):

    def __init__(self, sdmfile, fileroot='', workdir=''):
        self.sdmfile = os.path.abspath(sdmfile)
        if not fileroot:
            self.fileroot = os.path.split(os.path.abspath(sdmfile))[1]
        else:
            self.fileroot = fileroot
        if not workdir:
            self.workdir = os.path.split(self.sdmfile)[0]
        else:
            self.workdir = workdir
        self.scans = ps.read_scans(sdmfile)
        self.sources = ps.read_sources(sdmfile)
        self.gainscans = [ sc for sc in self.scans.keys() if 'PHASE' in self.scans[sc]['intent'] ]
        self.bpscans = [ sc for sc in self.scans.keys() if 'BANDPASS' in self.scans[sc]['intent'] ]
        self.sdm = sdmpy.SDM(self.sdmfile)
        if len(self.gainstr) or len(self.bpstr):
            print 'Found gaincal scans %s and bpcal scans %s.' % (self.gainstr, self.bpstr)
        self.set_fluxinfo()

    @property
    def gainstr(self):
        return string.join([ str(ss) for ss in self.gainscans ], ',')

    @property
    def bpstr(self):
        return string.join([ str(ss) for ss in self.bpscans ], ',')

    @property
    def allstr(self):
        return string.join([ str(ss) for ss in sorted(list(set(self.gainscans + self.bpscans))) ], ',')

    def find_refants(self):
        import numpy as n
        dist = lambda antpos: n.sqrt((antpos[:, 0] - antpos.mean(axis=0)[0]) ** 2 + (antpos[:, 1] - antpos.mean(axis=0)[1]) ** 2 + (antpos[:, 2] - antpos.mean(axis=0)[2]))
        antpos = n.array([ ant['position'].split(' ')[2:] for ant in self.sdm['Station'] if ant['type'] == 'ANTENNA_PAD' ]).astype(float)
        stationnames = [ ant.stationId for ant in self.sdm['Station'] if ant['type'] == 'ANTENNA_PAD' ]
        stationdict = OrderedDict(zip(stationnames, dist(antpos)))
        antdict = OrderedDict(zip([ ant.stationId for ant in self.sdm['Antenna'] ], [ ant.name for ant in self.sdm['Antenna'] ]))
        stations_sorted = sorted(stationdict, key=lambda st: stationdict[st])
        return [ antdict[station] for station in stations_sorted ][:3]

    def genms(self, scans=[]):
        """ Generate an MS that contains all calibrator scans with 1 s integration time.
        """
        if len(scans):
            scanstr = string.join([ str(ss) for ss in sorted(scans) ], ',')
        else:
            scanstr = self.allstr
        print 'Splitting out all cal scans (%s) with 1s int time' % scanstr
        newname = ps.sdm2ms(self.sdmfile, self.sdmfile.rstrip('/') + '.ms', scanstr, inttime='1')
        return newname

    def set_fluxinfo(self):
        """ Uses list of known flux calibrators (with models in CASA) to find full name given in scan.
        """
        knowncals = [
         '3C286', '3C48', '3C147', '3C138']
        sourcenames = [ self.sources[source]['source'] for source in self.sources ]
        calsources = [ cal for src in sourcenames for cal in knowncals if cal in src ]
        calsources_full = [ src for src in sourcenames for cal in knowncals if cal in src ]
        if len(calsources):
            self.band = self.sdm['Receiver'][0].frequencyBand.split('_')[1]
            if len(calsources) > 1:
                print 'Found multiple flux calibrators:', calsources
            self.fluxname = calsources[0]
            self.fluxname_full = calsources_full[0]
            print 'Set flux calibrator to %s and band to %s.' % (self.fluxname_full, self.band)
        else:
            self.fluxname = ''
            self.fluxname_full = ''
            self.band = ''

    def flagdata(self, msfile, flagfile='', flaglist=[]):
        """ Use flagfile (first) or flaglist (alternately) to run CASA flagging tool.
        """
        if not flagfile:
            flagfile = os.path.join(self.workdir, 'flags.txt')
            print 'Writing flaglist to %s.' % flagfile
            if not flaglist:
                flaglist = [
                 "mode='unflag'", "mode='shadow'", "mode='clip' clipzeros=True",
                 "mode='rflag' freqdevscale=4 timedevscale=5",
                 "mode='extend' growaround=True growtime=60 growfreq=40 extendpols=True",
                 "mode='quack' quackinterval=20", "mode='summary'"]
            with open(flagfile, 'w') as (flfile):
                for flag in flags:
                    flfile.write(flag + '\n')

        else:
            print 'Using flags in %s.' % flagfile
        print 'Flagging with these commands:'
        for ff in enumerate(open(flagfile)):
            print ff[1].rstrip()

        cfg = tl.FlaglistConfig()
        cfg.vis = msfile
        cfg.inpfile = flagfile
        tl.flaglist(cfg)

    def run(self, refant=[], antsel=[], uvrange='', fluxname='', fluxname_full='', band='', spw0='', spw1='', flaglist=[]):
        """ Run calibration pipeline. Assumes L-band.
        refant is list of antenna name strings (e.g., ['ea10']). default is to calculate based on distance from array center.
        antsel is list of ants to use (or reject) (e.g., ['!ea08'])
        uvrange is string giving uvrange (e.g., '<5klambda')
        fluxname, fluxname_full, and band are used to find flux calibrator info (e.g., '3C48', '0137+331=3C48', 'L').
        spw0 is spw selection for gain cal before bp cal (e.g., '0~1:60~75')
        spw1 is spw selection for gain cal after bp cal (e.g., '0~1:6~122')
        flaglist is the list of flag commands (e.g., ["mode='unflag'", "mode='shadow'", "mode='manual' antenna='ea11'"])
        """
        os.chdir(self.workdir)
        if not len(refant):
            refant = self.find_refants()
        antposname = self.fileroot + '.antpos'
        delayname = self.fileroot + '.delay'
        g0name = self.fileroot + '.g0'
        b1name = self.fileroot + '.b1'
        g1name = self.fileroot + '.g1'
        g2name = self.fileroot + '.g2'
        if fluxname:
            self.fluxname = fluxname
        if band:
            self.band = band
        if fluxname_full:
            self.fluxname_full = fluxname
        if self.fluxname and self.band:
            if self.band == 'P':
                calband = 'L'
            else:
                calband = self.band
            fluxmodel = '/home/casa/packages/RHEL5/release/casapy-41.0.24668-001-64b/data/nrao/VLA/CalModels/' + self.fluxname + '_' + calband + '.im'
        else:
            fluxmodel = ''
        msfile = self.genms()
        if flaglist:
            self.flagdata(msfile, flaglist=flaglist)
        elif os.path.exists(os.path.join(self.workdir, 'flags.txt')):
            self.flagdata(msfile, flagfile=os.path.join(self.workdir, 'flags.txt'))
        else:
            print 'No flagging.'
        if fluxmodel:
            if not os.path.exists(g0name):
                print 'Applying flux model for BP calibrator...'
                cfg = tl.SetjyConfig()
                cfg.vis = msfile
                cfg.scan = self.bpstr
                cfg.modimage = fluxmodel
                cfg.standard = 'Perley-Butler 2010'
                tl.setjy(cfg)
                print 'Starting initial gain cal...'
                cfg = tl.GaincalConfig()
                cfg.vis = msfile
                cfg.caltable = g0name
                cfg.gaintable = []
                cfg.scan = self.bpstr
                cfg.gaintype = 'G'
                cfg.solint = 'inf'
                cfg.spw = spw0
                cfg.refant = refant
                cfg.minsnr = 5.0
                cfg.calmode = 'p'
                cfg.antenna = antsel
                cfg.uvrange = uvrange
                tl.gaincal(cfg)
            else:
                print '%s exists' % g0name
            if not os.path.exists(b1name):
                print 'Starting bp cal...'
                cfg = tl.GaincalConfig()
                cfg.vis = msfile
                cfg.caltable = b1name
                cfg.gaintable = [g0name]
                cfg.scan = self.bpstr
                cfg.spw = spw1
                cfg.gaintype = 'BPOLY'
                cfg.degamp = 5
                cfg.degphase = 2
                cfg.maskedge = 6
                cfg.solint = 'inf'
                cfg.combine = ['scan']
                cfg.solnorm = True
                cfg.refant = refant
                cfg.antenna = antsel
                cfg.uvrange = uvrange
                tl.gaincal(cfg)
            else:
                print '%s exists' % b1name
            if not os.path.exists(g1name) or not os.path.exists(g2name):
                print 'Starting gain cal...'
                cfg = tl.GaincalConfig()
                cfg.vis = msfile
                cfg.caltable = g1name
                cfg.gaintable = [b1name]
                cfg.scan = self.allstr
                cfg.gaintype = 'G'
                cfg.solint = 'inf'
                cfg.spw = spw1
                cfg.refant = refant
                cfg.minsnr = 5.0
                cfg.calmode = 'ap'
                cfg.antenna = antsel
                cfg.uvrange = uvrange
                tl.gaincal(cfg)
                print 'Transferring flux scale...'
                cfg = tl.FluxscaleConfig()
                cfg.vis = msfile
                cfg.caltable = g1name
                cfg.fluxtable = g2name
                cfg.reference = self.fluxname_full
                tl.fluxscale(cfg)
            else:
                print 'either %s or %s exist' % (g1name, g2name)
        else:
            if not os.path.exists(g0name):
                print 'Starting initial gain cal...'
                cfg = tl.GaincalConfig()
                cfg.vis = msfile
                cfg.caltable = g0name
                cfg.gaintable = []
                cfg.scan = self.bpstr
                cfg.gaintype = 'G'
                cfg.solint = 'inf'
                cfg.spw = spw0
                cfg.refant = refant
                cfg.minsnr = 5.0
                cfg.calmode = 'p'
                cfg.antenna = antsel
                cfg.uvrange = uvrange
                tl.gaincal(cfg)
            else:
                print '%s exists' % g0name
            if not os.path.exists(b1name):
                print 'Starting bp cal...'
                cfg = tl.GaincalConfig()
                cfg.vis = msfile
                cfg.caltable = b1name
                cfg.gaintable = [g0name]
                cfg.scan = self.bpstr
                cfg.spw = spw1
                cfg.gaintype = 'BPOLY'
                cfg.degamp = 5
                cfg.degphase = 2
                cfg.maskedge = 6
                cfg.solint = 'inf'
                cfg.combine = ['scan']
                cfg.solnorm = True
                cfg.refant = refant
                cfg.antenna = antsel
                cfg.uvrange = uvrange
                tl.gaincal(cfg)
            else:
                print '%s exists' % b1name
            if not os.path.exists(g1name):
                print 'Starting gain cal...'
                cfg = tl.GaincalConfig()
                cfg.vis = msfile
                cfg.caltable = g1name
                cfg.gaintable = [b1name]
                cfg.scan = self.allstr
                cfg.gaintype = 'G'
                cfg.solint = 'inf'
                cfg.spw = spw1
                cfg.refant = refant
                cfg.minsnr = 5.0
                cfg.calmode = 'ap'
                cfg.antenna = antsel
                cfg.uvrange = uvrange
                tl.gaincal(cfg)
            else:
                print '%s exists' % g1name
        return 0