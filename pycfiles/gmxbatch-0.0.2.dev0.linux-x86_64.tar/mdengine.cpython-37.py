# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/mdengine.py
# Compiled at: 2020-03-26 04:07:37
# Size of source mod 2**32: 24817 bytes
"""Molecular dynamics engine"""
import io, os, shutil, subprocess, sys
from typing import Optional, List, Tuple
import numpy as np

class GMXError(Exception):
    stdout: str
    stderr: str
    cmdline: List[str]

    def __init__(self, message, stdout, stderr, cmdline):
        super().__init__(message)
        self.stdout = stdout
        self.stderr = stderr
        self.cmdline = cmdline


class MDEngine:
    __doc__ = 'Low-level interface to the GROMACS molecular dynamics engine'
    gmx: str
    verbose: bool
    backoff: bool
    echo: bool
    prefer_tng: bool

    def __init__(self, gmx: str, verbose: bool=False, backoff: bool=False, echo: bool=True):
        """Create an instance of MDEngine

        :param gmx: gmx executable path
        :type gmx: str
        :param verbose: equivalent of the -noquiet / -quiet command line switch
        :type verbose: bool
        :param backoff: equivalent of the -backup / -nobackup command line switch
        :type backoff: bool
        :param echo: stdout and stderr of the gmx command should be written to the stdout/stderr (True) or returned
            by the function call (False).
        :type echo: bool
        """
        self.gmx = gmx
        self.verbose = verbose
        self.backoff = backoff
        self.echo = echo
        self.prefer_tng = False

    @property
    def gmxprefix(self):
        """Return the installation prefix

        First the GMXPREFIX environment variable is checked. If it does not exist, the prefix is determined from the
        path of the 'gmx' executable."""
        try:
            return os.environ['GMXPREFIX']
        except KeyError:
            gmx = shutil.which(self.gmx)
            gmxbin = os.path.dirname(gmx)
            gmxprefix = os.path.dirname(gmxbin)
            return gmxprefix

    @property
    def gmxbin(self):
        """Return the bin directory.

        First the environment variable GMXBIN is checked. If it does not exist, the directory is constructed from the
        gmx prefix found by `gmxprefix`."""
        try:
            return os.environ['GMXBIN']
        except KeyError:
            return os.path.join(self.gmxprefix, 'bin')

    @property
    def gmxldlib(self):
        """Return the lib directory.

        First the environment variable GMXLDLIB is checked. If it does not exist, the directory is constructed from the
        gmx prefix found by `gmxprefix`."""
        try:
            return os.environ['GMXLDLIB']
        except KeyError:
            return os.path.join(self.gmxprefix, 'lib')

    @property
    def gmxman(self):
        """Return the man directory.

        First the environment variable GMXMAN is checked. If it does not exist, the directory is constructed from the
        gmx prefix found by `gmxprefix`."""
        try:
            return os.environ['GMXMAN']
        except KeyError:
            return os.path.join(self.gmxprefix, 'share', 'man')

    @property
    def gmxdata(self):
        """Return the data directory.

        First the environment variable GMXDATA is checked. If it does not exist, the directory is constructed from the
        gmx prefix found by `gmxprefix`."""
        try:
            return os.environ['GMXDATA']
        except KeyError:
            return os.path.join(self.gmxprefix, 'share', 'gromacs')

    @property
    def gmxtoolchaindir(self):
        """Return the CMake toolchain directory.

        First the environment variable GMXTOOLCHAINDIR is checked. If it does not exist, the directory is constructed
        from the gmx prefix found by `gmxprefix`."""
        try:
            return os.environ['GMXTOOLCHAINDIR']
        except KeyError:
            return os.path.join(self.gmxprefix, 'share', 'cmake')

    def grompp(self, mdpfile: str, conffile: str, topolfile: str, tprfile: str, restrfile: Optional[str]=None, contfile: Optional[str]=None, indexfile: Optional[str]=None, maxwarn: int=0) -> Tuple[(str, str)]:
        """Run "gmx grompp"

        :param mdpfile: molecular dynamics parameter file name (.mdp; for the '-f' switch)
        :type mdpfile: str
        :param conffile: current state file (.gro, .g96 etc.; for the '-c' switch)
        :type conffile: str
        :param topolfile: topology file (.top; for the '-p' switch)
        :type topolfile: str
        :param tprfile: tpr output file (.tpr; for the '-o' switch)
        :type tprfile: str
        :param restrfile: state file to read restraints from (optional, .gro, .g96; for the '-r' switch)
        :type restrfile: str
        :param contfile: continuation file (.trr, .cpt; for the '-t' switch
        :type contfile: str
        :param indexfile: index group file (.ndx; for the -n switch)
        :type indexfile: str
        :param maxwarn: maximum number of tolerable warnings ('-maxwarn' switch). Only set if you are really sure.
        :type maxwarn: int
        :return: stdout and stderr
        :rtype: Tuple[str, str]
        """
        return self.rungmx([
         'grompp', '-f', mdpfile, '-c', conffile, '-p', topolfile, '-o', tprfile, '-pp', os.path.splitext(tprfile)[0] + '_pp.top'] + (['-r', restrfile] if restrfile is not None else []) + (['-t', contfile] if contfile is not None else []) + (['-n', indexfile] if indexfile is not None else []) + ['-maxwarn', str(maxwarn)])

    def mdrun(self, deffnm: str, cont: bool=False, verbose: bool=False, pin: Optional[bool]=None) -> Tuple[(str, str)]:
        """Run "gmx mdrun".
        :param deffnm: base name of the .tpr file
        :type deffnm: str
        :param cont: True if continuation of a previous run (from a checkpoint file) should be attempted
        :type cont: bool
        :param verbose: the '-v' switch
        :type verbose: bool
        :param pin: cpu pinning: True, False or None (auto)
        :type pin: bool or None
        :return: stdout and stderr
        :rtype: Tuple[str, str]
        """
        return self.rungmx([
         'mdrun', '-deffnm', deffnm, '-o', f"{deffnm}.tng" if self.prefer_tng else f"{deffnm}.trr", '-pin', 'auto' if pin is None else 'on' if pin else 'off'] + (['-cpi', '-append'] if cont else []) + (['-v'] if verbose else []))

    def rebox(self, infile: str, outfile: str, boxtype: str='dodecahedron', dist: float=1.2) -> Tuple[(str, str)]:
        """Re-adjust the box size using "gmx editconf"

        :param infile: input file (.g96, .gro; for the '-f' switch)
        :type infile: str
        :param outfile: output file (.g96, .gro; for the '-o' switch)
        :type outfile: str
        :param boxtype: box type supported by editconf: triclinic, cubic, dodecahedron, octahedron
        :type boxtype: str
        :param dist: minimum distance between the solute and the box
        :type dist: str
        :return: stdout and stderr
        :rtype: Tuple[str, str]
        """
        return self.rungmx([
         'editconf', '-f', infile, '-o', outfile, '-bt', boxtype, '-d', str(dist), '-c'])

    def rungmx(self, arguments: List[str], inputstr: Optional[str]=None) -> Tuple[(str, str)]:
        """Helper function to call "gmx" tools

        :param arguments: arguments, including the subcommand name
        :type arguments: list of str
        :param inputstr: std input to be passed to the command
        :type inputstr: str
        :return: stdout, stderr
        :rtype: Tuple[str, str]
        """
        cmdline = [
         self.gmx] + arguments + ['-backup' if self.backoff else '-nobackup',
         '-noquiet' if self.verbose else '-quiet']
        print('Running cmdline: {}'.format(' '.join(cmdline)))
        result = subprocess.run(cmdline,
          input=inputstr, check=False, capture_output=(not self.echo),
          text=True)
        if result.returncode != 0:
            print('GMX call failed.')
            print('command line: {}'.format(' '.join(cmdline)))
            print('STDOUT:\n-------')
            print((result.stdout), file=(sys.stdout))
            print('STDERR:\n-------')
            print((result.stderr), file=(sys.stderr))
            raise GMXError('GMX program failed', stderr=(result.stderr), stdout=(result.stdout), cmdline=cmdline)
        return (
         result.stdout, result.stderr)

    def genconf(self, infile: str, outfile: str, nx: int=10, ny: int=10, nz: int=10, rot: bool=True) -> Tuple[(
 str, str)]:
        """Repeat the current conformation in a grid, using gmx genconf

        :param infile: file containing the conformation to be multiplied (.gro, .g96'; switch '-f')
        :type infile: str
        :param outfile: output file name (.gro, .g96; switch '-o')
        :type outfile: str
        :param nx: repeat count along the X axis
        :type nx: int
        :param ny: repeat count along the Y axis
        :type ny: int
        :param nz: repeat count along the Z axis
        :type nz: int
        :param rot: randomly rotate conformations
        :type rot: bool
        :return: stdout, stderr
        :rtype: Tuple[str, str]
        """
        return self.rungmx([
         'genconf', '-f', infile, '-nbox', str(nx), str(ny), str(nz), '-rot' if rot else '-norot', '-o', outfile])

    def generateDefaultIndex(self, conffile: str, outfile: str) -> Tuple[(str, str)]:
        """Create default index groups using "gmx make_ndx"

        :param conffile: conf file (.g96, .gro; switch '-f')
        :type conffile: str
        :param outfile: output file (.ndx; switch '-o')
        :type outfile: str
        :return: stdout, stderr
        :rtype: Tuple[str, str]
        """
        return self.rungmx(['make_ndx', '-f', conffile, '-o', outfile], inputstr='q\n')

    def energy(self, tprfile: str, edrfile: str, outfile: str, terms: List[str]=None) -> Tuple[(str, str)]:
        """Extract energy terms using "gmx energy"

        :param tprfile: run input file (.tpr; switch '-s')
        :type tprfile: str
        :param edrfile: energy file (.edr; switch '-f')
        :type edrfile: str
        :param outfile: output file (.xvg; switch '-o')
        :type outfile: str
        :param terms: energy terms to list (None if all)
        :type terms: list of str
        :return: stdout, stderr
        :rtype: Tuple[str, str]
        """
        if not terms:
            terms = [str(x) for x in range(1, 100)] + ['0']
        return self.rungmx(['energy', '-f', edrfile, '-s', tprfile, '-o', outfile], inputstr=('\n'.join(terms)))

    def genion(self, tprfile: str, indexfile: str, outputfile: str, solventgroup: str, pname: str, nname: str, conc: float, pq: int=1, nq: int=-1, neutralize: bool=True):
        """Run gmx genion

        :param tprfile: run input file (.tpr; switch '-s')
        :type tprfile: str
        :param indexfile: index file (.ndx; switch '-n')
        :type indexfile: str
        :param outputfile: output structure file (.gro, .g96; switch '-o')
        :type outputfile: str
        :param solventgroup: index group to replace elements with ions
        :type solventgroup: str
        :param pname: name of the positive ion (switch '-pname')
        :type pname: str
        :param nname: name of the negative ion (switch '-nname')
        :type nname: str
        :param conc: salt concentration in mol/liter (switch '-conc')
        :type conc: float
        :param pq: charge of the positive ion (switch '-pq')
        :type pq: int
        :param nq: charge of the negative ion (switch '-nq')
        :type nq: int
        :param neutralize: add enough ions to neutralize the system (switch '-neutral')
        :type neutralize: bool
        """
        self.rungmx([
         'genion', '-s', tprfile, '-n', indexfile, '-pname', pname, '-nname', nname, '-conc', str(conc), '-pq',
         '{:d}'.format(pq), '-nq', '{:d}'.format(nq), '-neutral' if neutralize else '-noneutral', '-o', outputfile],
          inputstr=(solventgroup + '\n'))

    def trjconv_pbc(self, tprfile: str, intraj: str, outtraj: str, indexfile: str, pbctype: str, clustergroup: str='System', outgroup: str='System', centergroup: Optional[str]=None, fitgroup: Optional[str]=None, fitmode: str='rot+trans'):
        """Periodic boundary condition treatment using "gmx trjconv"

        :param tprfile: run input file (.tpr, switch '-s')
        :type tprfile: str
        :param intraj: input trajectory file (.trr, .xtc but also .gro and .g96, switch '-f')
        :type intraj: str
        :param outtraj: output trajectory file (.trr, .xtc but also .gro and .g96, switch '-o')
        :type outtraj: str
        :param indexfile: index file (.ndx, switch '-n)
        :type indexfile: str
        :param pbctype: periodic boundary condition treatment type: 'mol', 'res', 'atom', 'nojump', 'cluster', 'whole'
        :type pbctype: str
        :param clustergroup: group for clustering
        :type clustergroup: str
        :param outgroup: group for output
        :type outgroup: str
        :param centergroup: group for centering (or None to skip centering)
        :type centergroup: str or None
        :param fitgroup: group for fitting or None if no fitting is desired
        :type fitgroup: str or None
        :param fitmode: fit mode: none, rot+trans, rotxy+transxy, translation, transxy, progressive
        :type fitmode: str
        """
        self.rungmx(([
         'trjconv', '-s', tprfile, '-f', intraj, '-o', outtraj, '-pbc', pbctype, '-n', indexfile,
         '-nocenter' if centergroup is None else '-center'] + (['-fit', fitmode] if fitgroup is not None else [])),
          inputstr=((fitgroup + '\n' if fitgroup is not None else '') + (clustergroup + '\n' if pbctype == 'cluster' else '') + (centergroup + '\n' if centergroup is not None else '') + outgroup + '\n'))

    def solvate(self, conffile: str, solventbox: str, outputfile: str):
        """Solvate a system using "gmx solvate"

        :param conffile: file with the coordinates (.g96, .gro; switch '-cp')
        :type conffile: str
        :param solventbox: solvent box coordinate set (.g96, .gro; switch '-cs')
        :type solventbox: str
        :param outputfile: output coordinates (.g96, .gro; switch '-o')
        :type outputfile: str
        """
        self.rungmx(['solvate', '-cs', solventbox, '-cp', conffile, '-o', outputfile])

    def convert_tpr(self, tprfile: str, tprout: str, group: str, indexfile: Optional[str]=None, extendtime: Optional[float]=None, untiltime: Optional[float]=None, nsteps: Optional[float]=None, zeroq: bool=False):
        """Run "gmx convert-tpr"

        :param tprfile: run input file name
        :type tprfile: str
        :param tprout: output tpr file name
        :type tprout: str
        :param group: index group name
        :type group: str
        :param indexfile: index file name
        :type indexfile: str
        :param extendtime: extend the runtime by this amount (ps)
        :type extendtime: float
        :param untiltime: extend the runtime until this ending time (ps)
        :type untiltime: float
        :param nsteps: set the number of steps (-1 is unlimited)
        :type nsteps: int
        :param zeroq: set the charges of a group (from the index) to zero
        :type zeroq: bool
        """
        self.rungmx(([
         'convert-tpr', '-s', tprfile, '-o', tprout] + (['-n', indexfile] if indexfile is not None else []) + (['-extend', str(extendtime)] if extendtime is not None else []) + (['-until', str(untiltime)] if untiltime is not None else []) + ['-nsteps', str(nsteps) if nsteps is not None else []] + [
         '-zeroq' if zeroq else '-nozeroq']),
          inputstr=(group + '\n'))

    def gyrate(self, tprfile: str, trjfile: str, indexfile: str, outputfile: str, group: str='System', weightbycharge: bool=False):
        """Calculate radius of gyration using "gmx gyrate"

        :param tprfile: run input file name (.tpr, '-s' switch)
        :type tprfile: str
        :param trjfile: trajectory file (.trr or .xtc or .tng, '-f' switch)
        :type trjfile: str
        :param indexfile: index file (.ndx, '-n' switch)
        :type indexfile: str
        :param outputfile: output file (.xvg, '-o' switch)
        :type outputfile: str
        :param group: group for analysis
        :type group: str
        :param weightbycharge: weighting by charge instead of mass
        :type weightbycharge: bool
        """
        self.rungmx(['gyrate', '-s', tprfile, '-f', trjfile, '-n', indexfile, '-o', outputfile,
         '-q' if weightbycharge else '-noq'],
          inputstr=(group + '\n'))

    def distance(self, tprfile: str, trjfile: str, indexfile: str, outputfile: str, selection: str):
        """Calculate distances in the trajectory using 'gmx distance'

        :param tprfile: run input file name (.tpr, '-s' switch)
        :type tprfile: str
        :param trjfile: trajectory file (.trr or .xtc or .tng, '-f' switch)
        :type trjfile: str
        :param indexfile: index file (.ndx, '-n' switch)
        :type indexfile: str
        :param outputfile: output file (.xvg, '-oall' switch)
        :type outputfile: str
        :param selection: selection of pairs
        :type selection: str
        """
        self.rungmx([
         'distance', '-s', tprfile, '-f', trjfile, '-n', indexfile, '-oall', outputfile, '-select', selection])

    def hbond(self, tprfile: str, trjfile: str, indexfile: str, group1: str, group2: str, hbnumfile: str, hbdistfile: Optional[str]=None, hbangfile: Optional[str]=None, hbhelixfile: Optional[str]=None, hbindexfile: Optional[str]=None, hbmapfile: Optional[str]=None, abin: float=1, rbin: float=1, nitacc: bool=True, cutoffangle: float=30, cutoffdistance: float=0.35):
        """Analyze hydrogen bonds in the trajectory using 'gmx hbond'

        :param tprfile: run input file (.tpr, switch '-s')
        :type tprfile: str
        :param trjfile: trajectory file (.xtc, .trr or .tng, switch '-f')
        :type trjfile: str
        :param indexfile: index file (.ndx, switch '-n')
        :type indexfile: str
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
        """
        self.rungmx(([
         'hbond', '-s', tprfile, '-f', trjfile, '-n', indexfile, '-a', str(cutoffangle), '-r', str(cutoffdistance), '-abin', str(abin), '-rbin', str(rbin), '-nitacc' if nitacc else '-nonitacc', '-num', hbnumfile] + (['-dist', hbdistfile] if hbdistfile is not None else []) + (['-ang', hbangfile] if hbangfile is not None else []) + (['-hx', hbhelixfile] if hbhelixfile is not None else []) + (['-hbn', hbindexfile] if hbindexfile is not None else []) + (['-hbm', hbmapfile] if hbmapfile is not None else [])),
          inputstr=f"{group1}\n{group2}\n")

    def trjcheck(self, trjfile: str):
        """Check the length of the trajectory file using 'gmx check'

        :param trjfile: trajectory file (.trr, .tng, .xtc; switch '-f')
        :type trjfile: str
        :return: trajectory format version, atom count, last frame id, last time, table
        :rtype: str, int, int, float, list of (str, int, float) tuples
        """
        echo = self.echo
        self.echo = False
        try:
            stdout, stderr = self.rungmx(['check', '-f', trjfile])
        finally:
            self.echo = echo

        sio = io.StringIO(stderr)
        versionstring = sio.readline().strip()
        table = None
        natoms = None
        lastframeno = None
        lasttime = None
        for line in sio:
            if not line.strip():
                continue
            elif line.startswith('# Atoms'):
                natoms = int(line.split()[(-1)])
            elif line.startswith('Reading frame'):
                continue
            elif line.startswith('Last frame'):
                lastframeno, lasttime = line.replace('Last frame', '').replace('time', '').split()
                lastframeno = int(lastframeno)
                lasttime = float(lasttime)
            else:
                if line.startswith('Item'):
                    table = []
                    continue

        return (
         versionstring, natoms, lastframeno, lasttime, table)

    def pairdist(self, tprfile: str, trjfile: str, indexfile: str, outputfile: str, ref: str, sel: str, cutoff: float=0, selrpos: str='atom', seltype: str='atom', disttype: str='min', refgrouping: str='all', selgrouping: str='all'):
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
        """
        self.rungmx([
         'pairdist', '-f', trjfile, '-s', tprfile, '-n', indexfile, '-o', outputfile, '-ref', ref, '-sel', sel,
         '-cutoff', cutoff, '-selrpos', selrpos, '-seltype', seltype, '-refgrouping', refgrouping, '-selgrouping',
         selgrouping, '-type', disttype])