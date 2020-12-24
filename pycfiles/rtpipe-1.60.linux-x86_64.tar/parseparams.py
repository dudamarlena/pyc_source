# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbe-master/realfast/anaconda/envs/deployment/lib/python2.7/site-packages/rtpipe/parseparams.py
# Compiled at: 2017-09-19 16:49:27


class Params(object):
    """ Parameter class used as input to define pipeline
    Lets system use python-like file for importing into namespace and same file for oo-like parameter definition.
    Uses 'exec', for which I am not proud.
    Also defines default values for all parameters.
    """

    def __init__(self, paramfile=''):
        self.chans = []
        self.spw = []
        self.nskip = 0
        self.excludeants = []
        self.read_tdownsample = 1
        self.read_fdownsample = 1
        self.selectpol = [
         'RR', 'LL', 'XX', 'YY']
        self.nthread = 1
        self.nchunk = 0
        self.nsegments = 0
        self.scale_nsegments = 1
        self.timesub = ''
        self.dmarr = []
        self.dtarr = [1]
        self.dm_maxloss = 0.05
        self.maxdm = 0
        self.dm_pulsewidth = 3000
        self.searchtype = 'image1'
        self.sigma_image1 = 7.0
        self.sigma_image2 = 7.0
        self.l0 = 0.0
        self.m0 = 0.0
        self.uvres = 0
        self.npix = 0
        self.npix_max = 0
        self.uvoversample = 1.0
        self.flaglist = [
         ('badchtslide', 4.0, 0.0), ('badap', 3.0, 0.2), ('blstd', 3.0, 0.05)]
        self.flagantsol = True
        self.gainfile = ''
        self.bpfile = ''
        self.fileroot = ''
        self.applyonlineflags = True
        self.savenoise = False
        self.savecands = False
        self.logfile = True
        self.loglevel = 'INFO'
        self.writebdfpkl = False
        self.mock = 0
        self.bdfdir = ''
        if len(paramfile):
            self.parse(paramfile)

    def parse(self, paramfile):
        """ Read parameter file and set parameter values.
        File should have python-like syntax. Full file name needed.
        """
        with open(paramfile, 'r') as (f):
            for line in f.readlines():
                line_clean = line.rstrip('\n').split('#')[0]
                if line_clean and '=' in line:
                    attribute, value = line_clean.split('=')
                    try:
                        try:
                            value_eval = eval(value.strip())
                        except NameError:
                            value_eval = value.strip()

                    finally:
                        setattr(self, attribute.strip(), value_eval)

    @property
    def defined(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return self.__dict__[key]

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)