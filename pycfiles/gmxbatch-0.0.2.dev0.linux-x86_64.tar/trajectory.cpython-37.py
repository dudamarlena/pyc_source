# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/trajectory.py
# Compiled at: 2020-03-23 06:02:12
# Size of source mod 2**32: 12522 bytes
import os
from typing import Optional, Dict, Sequence
from .indexgroups import IndexGroups
from .mdengine import MDEngine
from .xvgfile import XVGFile

class Trajectory:
    __doc__ = 'Trajectory object\n\n    This class encapsulates a GROMACS trajectory and exposes some common operations on them.\n\n    As running GMX programs can sometimes be expensive, a caching/lazy mechanism is implemented. If the result files\n    of a call to a GROMACS subprogram are all present and newer than the base files (run input file, trajectory, index\n    file), running the program will be skipped. This behaviour can be overridden by the `forcererun` attribute (False\n    by default).\n    '
    filename: str
    tprfile: str
    edrfile = None
    edrfile: Optional[str]
    engine: MDEngine
    indexgroups: IndexGroups
    forcererun: bool

    def __init__(self, filename: str, tprfile: str, engine: MDEngine, indexgroups: IndexGroups, forcererun: bool=False, edrfile: Optional[str]=None):
        """Initialize the trajectory object

        :param filename: trajectory file name (.trr, .xtc or .tng)
        :type filename: str
        :param tprfile: run input file matching the trajectory (.tpr)
        :type tprfile: str
        :param engine: GROMACS engine
        :type engine: MDEngine
        :param indexgroups: index group instance, matching the trajectory
        :type indexgroups: str
        :param forcererun: force re-running GMX commands, i.e. override the caching mechanism
        :type forcererun: bool
        :param edrfile: energy terms file (.edr)
        :type edrfile: str
        """
        self.filename = filename
        self.tprfile = tprfile
        self.edrfile = edrfile
        self.engine = engine
        self.indexgroups = indexgroups
        self.forcererun = forcererun

    def adjustPBC(self, mode: str='mol', clustergroup: str='System', centergroup: Optional[str]=None, fitgroup: Optional[str]=None, fitmode: str='rot+trans'):
        """Adjust representation of the unit cell with respect to periodic boundary conditions using 'gmx trjconv'

        :param mode: PBC mode, the '-pbc' switch of gmx trjconv
        :type mode: str
        :param centergroup: index group to center
        :type centergroup: str or None
        :param clustergroup: index group for clustering if mode='cluster' is specified
        :type clustergroup: str
        :param fitgroup: group for fitting atoms to reference structures or None if no fitting is desired
        :type fitgroup: str or None
        :param fitmode: fitting mode: none, rot+tran, rotxy+transxy, translation, transxy, progressive
        :type fitmode: str
        """
        fname, ext = os.path.splitext(self.filename)
        newname = fname + '_pbc' + ext
        if self._rerunneeded(newname):
            self.engine.trjconv_pbc(self.tprfile, self.filename, newname, self.indexgroups.filename, mode, clustergroup, 'System', centergroup, fitgroup, fitmode)
        self.filename = newname

    def reduce(self, indexgroup: str, namesuffix: str='red'):
        """Reduce trajectory (e.g. eliminate solvent atoms) using 'gmx trjconv' and 'gmx convert-tpr'

        :param indexgroup: index group to write
        :type indexgroup: str
        :param namesuffix: output tpr and trr files will have this appended before the extension, e.g.
                           'red' -> 'md_red.trr'
        :type namesuffix: str
        """
        fname, ext = os.path.splitext(self.filename)
        newbasename = f"{fname}_{namesuffix}"
        if self._rerunneeded(f"{newbasename}.tpr"):
            self.engine.convert_tpr(self.tprfile, f"{newbasename}.tpr", indexgroup, self.indexgroups.filename)
        if self._rerunneeded(f"{newbasename}{ext}"):
            self.engine.trjconv_pbc((self.tprfile), (self.filename), f"{newbasename}{ext}", (self.indexgroups.filename), outgroup=indexgroup,
              pbctype='none')
        self.tprfile = f"{newbasename}.tpr"
        self.filename = f"{newbasename}{ext}"

    def gyrate(self, group: str, outputfile='gyrate.xvg', weightbycharge: bool=False) -> XVGFile:
        """Calculate the radius of gyration

        :param group: index group to calculate the radius of gyration of
        :type group: str
        :param outputfile: output file (.xvg)
        :type outputfile: str
        :param weightbycharge: do weighting by total charge instead of mass
        :type weightbycharge: bool
        :return: XVG file
        :rtype: XVGFile
        """
        if self._rerunneeded(outputfile):
            self.engine.gyrate((self.tprfile), (self.filename), (self.indexgroups.filename), outputfile,
              group=group, weightbycharge=weightbycharge)
        return XVGFile(outputfile)

    def distance(self, selection: str, outputfile='distall.xvg'):
        """Calculate distances between atom pairs

        :param selection: GROMACS-style selection suitable for 'gmx select'
        :type selection: str
        :param outputfile: output file name (.xvg)
        :type outputfile: str
        :return: XVG file data
        :rtype: XVGFile
        """
        if self._rerunneeded(outputfile):
            self.engine.distance(self.tprfile, self.filename, self.indexgroups.filename, outputfile, selection)
        return XVGFile(outputfile)

    def hbond(self, group1: str, group2: str, hbnumfile: str='hbnum.xvg', hbdistfile: Optional[str]=None, hbangfile: Optional[str]=None, hbhelixfile: Optional[str]=None, hbindexfile: Optional[str]=None, hbmapfile: Optional[str]=None, abin: float=1, rbin: float=1, nitacc: bool=True, cutoffangle: float=30, cutoffdistance: float=0.35) -> Dict[(str, XVGFile)]:
        """Analyze hydrogen bonds in the trajectory using 'gmx hbond'

        :param group1: first group
        :type group1: str
        :param group2: second group
        :type group2: str
        :param hbnumfile: file for writing the number of hydrogen bonds vs time (.xvg, switch '-num')
        :type hbnumfile: str
        :param hbdistfile: file for writing distance distribution (.xvg, switch '-dist')
        :type hbdistfile: str or None
        :param hbangfile: file for writing angle distribution (.xvg, switch '-ang')
        :type hbangfile: str or None
        :param hbhelixfile: file for writing i -> i+n bond counts (.xvg, switch '-hx')
        :type hbhelixfile: str or None
        :param hbindexfile: file for writing an index file for hydrogen bonds (.ndx, switch '-hbn')
        :type hbindexfile: str or None
        :param hbmapfile: existence matrix for all hydrogen bonds (.xpm, switch '-hbm')
        :type hbmapfile: str or None
        :param abin: binwidth of angle distribution (degrees, switch '-abin')
        :type abin: float
        :param rbin: binwidth of distance distribution (nm, switch '-rbin')
        :type rbin: float
        :param nitacc: treat nitrogen atoms as acceptors (switch '-nitacc' and '-nonitacc')
        :type nitacc: bool
        :param cutoffangle: angle cut-off (degrees, switch '-a')
        :type cutoffangle: float
        :param cutoffdistance: distance cut-off (degrees, switch '-r')
        :type cutoffdistance: float
        :return: a dictionary of XVG files
        :rtype: dictionary of XVGFile instances
        """
        if (self._rerunneeded)(*[fn for fn in [hbnumfile, hbdistfile, hbangfile, hbhelixfile, hbindexfile, hbmapfile] if fn is not None]):
            self.engine.hbond(tprfile=(self.tprfile), trjfile=(self.filename), indexfile=(self.indexgroups.filename), group1=group1,
              group2=group2,
              hbnumfile=hbnumfile,
              hbdistfile=hbdistfile,
              hbangfile=hbangfile,
              hbhelixfile=hbhelixfile,
              hbindexfile=hbindexfile,
              hbmapfile=hbmapfile,
              abin=abin,
              rbin=rbin,
              nitacc=nitacc,
              cutoffangle=cutoffangle,
              cutoffdistance=cutoffdistance)
        return {'hbnum':XVGFile(hbnumfile), 
         'hbdist':XVGFile(hbdistfile) if hbdistfile is not None else None, 
         'hbang':XVGFile(hbangfile) if hbangfile is not None else None, 
         'hbhelix':XVGFile(hbhelixfile) if hbhelixfile is not None else None, 
         'hbindex':XVGFile(hbindexfile) if hbindexfile is not None else None}

    def _rerunneeded(self, *filenames) -> bool:
        """Check if running a GROMACS program is really needed.

        Running GMX programs can be expensive, especially on large trajectories or when the underlying file system is
        slow. This method decides if, given a list of file names, the run must be done again or can be skipped safely.
        If all of those files are newer (modification time) than the base files (the .tpr file, the trajectory and the
        index file), the GMX program will not be run, the alredy existing files will be used. If any of the files is
        older than any of the base files, or one of the files does not exist, rerunning will needed. The attribute
        `forcererun` overrides this mechanism. When it is True, GMX programs will always be run.
        """
        if self.forcererun:
            return True
        basemtimes = [os.path.getmtime(bf) for bf in [self.filename, self.indexgroups.filename, self.tprfile] + ([self.edrfile] if self.edrfile is not None else [])]
        for f in filenames:
            if not os.path.exists(f):
                return True
                mtime = os.path.getmtime(f)
                if any([bmt > mtime for bmt in basemtimes]):
                    return True

        return False

    def check(self):
        """Check the length of the trajectory file using 'gmx check'

        :return: trajectory format version, atom count, last frame id, last time, table
        :rtype: str, int, int, float, list of (str, int, float) tuples
        """
        return self.engine.trjcheck(self.filename)

    def extractenergy(self, outputfile: str, energyterms: Optional[Sequence[str]]=None) -> XVGFile:
        if self.edrfile is None:
            raise ValueError('Cannot extract energy: edr file attribute is empty.')
        if self._rerunneeded(outputfile):
            self.engine.energy((self.tprfile), (self.edrfile), outputfile, terms=energyterms)
        return XVGFile(outputfile)

    def pairdist(self, outputfile: str, ref: str, sel: str, cutoff: float=0, selrpos: str='atom', seltype: str='atom', disttype: str='min', refgrouping: str='all', selgrouping: str='all') -> XVGFile:
        """Calculate pair distances using 'gmx pairdist'

        Distances are calculated between atoms of two selections: the "reference" and the "target".

        Atoms can be grouped in both selections by the `refgrouping` and `selgrouping` arguments.

        :param tprfile: run input file (.tpr; switch '-s')
        :type tprfile: str
        :param trjfile: trajectory file (.tng, .xtc, .trr; switch '-f')
        :type trjfile: str
        :param indexfile: index file (.ndx; switch '-n')
        :type indexfile: str
        :param outputfile: output file (.xvg; switch '-o')
        :type outputfile: str
        :param ref: GROMACS selection containing reference atoms
        :type ref: str
        :param sel: GROMACS selection containing target atoms
        :type sel: str
        :param cutoff: cut-off distance (default: no cut-off)
        :type cutoff: float
        :param selrpos: Selection reference positions (switch '-selrpos')
        :type selrpos: str
        :param seltype: Default selection output positions (switch '-seltype')
        :type seltype: str
        :param disttype: 'min' for minimum distance, 'max' for maximum distance
        :type disttype: str
        :param refgrouping: grouping of the reference selection: 'all', 'res', 'mol', 'none'
        :type refgrouping: str
        :param selgrouping: grouping of the target selection: 'all', 'res', 'mol', 'none'
        :type selgrouping: str
        :return: XVG data
        :rtype: XVGFile
        """
        if self._rerunneeded(outputfile):
            self.engine.pairdist(self.tprfile, self.filename, self.indexgroups.filename, outputfile, ref, sel, str(cutoff), selrpos, seltype, disttype, refgrouping, selgrouping)
        return XVGFile(outputfile)