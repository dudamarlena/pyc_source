# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/simulation/simulation.py
# Compiled at: 2020-03-26 05:32:49
# Size of source mod 2**32: 20262 bytes
"""Simulation class"""
import copy, os
from typing import Optional, Dict
from .results import Results
from ..conffiles import Coordinates
from ..environment import Environment
from ..mdengine import MDEngine
from ..moleculetype import MoleculeType
from ..system import System
from ..trajectory import Trajectory
from ..xvgfile import XVGFile

class Simulation:
    __doc__ = 'This class encapsulates all details of an MD simulation.\n\n    Attributes:\n        - `system`: the simulation system (instance of gmxbatch.system.System): topology, force field, current state\n        - `engine`: MD engine (instance of gmxbatch.mdengine.MDEngine\n        - `environment`: environmental parameters (instance of gmxbatch.environment.Environment): thermostat, barostat\n        - `maxwarn`: maximum number of warnings in grompp to tolerate. Use with care!\n    '
    system: System
    engine: MDEngine
    environment: Environment
    lastdeffnm = None
    lastdeffnm: Optional[str]
    maxwarn = 0
    maxwarn: int

    def __init__(self, engine: MDEngine, system: System, environment: Environment):
        self.system = system
        self.engine = engine
        self.environment = environment
        self.reindex()

    def reindex(self):
        """Re-create default index groups"""
        self.system.indexgroups.getDefault(self.system.conf, self.engine, self.system.moleculetypes)

    def sortAtoms(self):
        """Sort atoms in the current state to conform the topology"""
        self.system.conf.sortAgainstTopology(self.system.moleculetypes)
        self.reindex()

    def rebox(self, boxtype: str='dodecahedron', distance: float=1.2):
        """Adjust the box size of the current state.

        :param boxtype: box type supported by `gmx editconf`
        :type boxtype: str
        :param distance: minimum distance from the molecule and the box walls
        :type distance: float
        """
        boxedname = 'boxed_' + os.path.split(self.system.conf.filename)[(-1)]
        self.engine.rebox((self.system.conf.filename), boxedname, boxtype=boxtype, dist=distance)
        self.system.conf.load(boxedname)

    def repeat(self, nx: int=10, ny: int=10, nz: int=10, rot: bool=True):
        """Repeat the current state in a grid, i.e. `gmx genconf`

        :param nx: number of repeats in the X direction
        :type nx:  int
        :param ny: number of repeats in the Y direction
        :type ny: int
        :param nz: number of repeats in the Z direction
        :type nz: int
        :param rot: True if the repeated molecules should be randomly oriented
        :type rot: bool
        """
        repname = 'rep_' + os.path.split(self.system.conf.filename)[(-1)]
        self.engine.genconf(self.system.conf.filename, repname, nx, ny, nz, rot)
        self.system.conf.load(repname)
        for mt in self.system.moleculetypes:
            mt.count *= nx * ny * nz

        self.reindex()

    def em(self, nsteps: int=50000, emtol: float=100.0, emstep: float=0.01, deffnm: str='em', posres: bool=True, noconstraintsinmdp: bool=True, dorun: bool=True) -> Results:
        """Energy minimization

        Energy terms are also extracted using the function `extract_energy(..., runtype='em')`.

        Position restraints on solute molecules will be applied if requested by the `posres` argument.

        After the run, the end state will be loaded as the current coordinate set.

        :param nsteps: number of steps
        :type nsteps: int
        :param emtol: maximum force (kJ/mol)
        :type emtol: float
        :param emstep: minimization step size (nm)
        :type emstep: float
        :param deffnm: basename of the .tpr file
        :type deffnm: str
        :param posres: True if position restraints should be applied
        :type posres: bool
        :param noconstraintsinmdp: set this to True to set 'constraints = none' in the MDP file
        :type noconstraintsinmdp: bool
        :param dorun: True if the actual run has to be done (i.e. gmx mdrun should be called). If False, only the input
                      files are created.
        :type dorun: bool
        :return: a Results object encapsulating the final set of coordinates and the energy data
        :rtype: Results
        """
        self.system.forcefield.mdp.energyMinimization(nsteps=nsteps, emtol=emtol, emstep=emstep)
        if posres:
            self.system.forcefield.mdp.posresdefines = {x.posresdefine for x in self.system.moleculetypes if x.posresdefine if x.kind == 'Solute' if x.kind == 'Solute'}
        else:
            self.system.forcefield.mdp.posresdefines = set()
        constr = self.system.forcefield.mdp.constraints.constraints
        try:
            if noconstraintsinmdp:
                self.system.forcefield.mdp.constraints.constraints = 'none'
            return self._mdrun_helper(deffnm, 'em', restraints=posres, cont=False, dorun=dorun)
        finally:
            self.system.forcefield.mdp.constraints.constraints = constr

    def nvt(self, runtime: float, deffnm: str='nvt', dorun: bool=True) -> Results:
        """Perform an NVT equilibration run.

        All settings in `self.environment.thermostat` are applied, except the algorithm: it will always be 'Berendsen'.
        This temperature coupling scheme relaxes very well, but does not sample the true NVT ensemble. For production
        runs, use e.g. 'Nose-Hoover' or 'V-rescale' instead.

        Energy terms are also extracted using the function `extract_energy(..., runtype='nvt')`.

        Position restraints on solute molecules will be applied.

        After the run, the end state will be loaded as the current coordinate set.

        :param runtime: requested run time (ps)
        :type runtime: float
        :param deffnm: basename of the .tpr file
        :type deffnm: str
        :param dorun: True if the actual run has to be done (i.e. gmx mdrun should be called). If False, only the input
                      files are created.
        :type dorun: bool
        :return: a Results object encapsulating the final set of coordinates and the energy data
        :rtype: Results
        """
        self.system.forcefield.mdp.nvt(env=(self.environment), runtime=runtime)
        self.system.forcefield.mdp.posresdefines = {x.posresdefine for x in self.system.moleculetypes if x.posresdefine if x.kind == 'Solute' if x.kind == 'Solute'}
        return self._mdrun_helper(deffnm, 'nvt', restraints=True, cont=False, dorun=dorun)

    def npt(self, runtime: float, deffnm: str='npt', dorun: bool=True) -> Results:
        """Perform an NpT equilibration run.

        All settings in `self.environment.barostat` are applied, except the algorithm: it will always be 'Berendsen'.
        This pressure coupling scheme relaxes very well, but does not sample the true NpT ensemble. For production
        runs, use e.g. 'Parrinello-Rahman'. The temperature coupling algorithm will also be set to 'Berendsen'

        Energy terms are also extracted using the function `extract_energy(..., runtype='npt')`.

        Position restraints on solute molecules will be applied.

        After the run, the end state will be loaded as the current coordinate set.

        :param runtime: requested run time (ps)
        :type runtime: float
        :param deffnm: basename of the .tpr file
        :type deffnm: str
        :param dorun: True if the actual run has to be done (i.e. gmx mdrun should be called). If False, only the input
                      files are created.
        :type dorun: bool
        :return: a Results object encapsulating the final set of coordinates and the energy data
        :rtype: Results
        """
        self.system.forcefield.mdp.npt(env=(self.environment), runtime=runtime)
        self.system.forcefield.mdp.posresdefines = {x.posresdefine for x in self.system.moleculetypes if x.posresdefine if x.kind == 'Solute' if x.kind == 'Solute'}
        return self._mdrun_helper(deffnm, 'npt', restraints=True, cont=True, dorun=dorun)

    def md(self, runtime: float, deffnm: str='md', dorun: bool=True) -> Results:
        """Perform a production run.

        Energy terms are also extracted using the function `extract_energy(..., runtype='md')`.

        Position restraints won't be applied.

        After the run, the end state will be loaded as the current coordinate set.

        :param runtime: requested run time (ps)
        :type runtime: float
        :param deffnm: basename of the .tpr file
        :type deffnm: str
        :param dorun: True if the actual run has to be done (i.e. gmx mdrun should be called). If False, only the input
                      files are created.
        :type dorun: bool
        :return: a Results object encapsulating the final set of coordinates and the energy data
        :rtype: Results
       """
        self.system.forcefield.mdp.md(env=(self.environment), runtime=runtime)
        self.system.forcefield.mdp.posresdefines = set()
        return self._mdrun_helper(deffnm, 'md', restraints=False, cont=True, dorun=dorun)

    def _mdrun_helper(self, deffnm: str, runtype: str, restraints: bool=True, cont: bool=True, dorun: bool=True) -> Results:
        """Helper function for the common tasks before and after runs with "gmx mdrun"

        The tasks are:
        1) write the topology
        2) write the mdp file (assumed to be in the correct state)
        3) write the index file
        4) run grompp
        5) run mdrun
        6) update the coordinate set with the new conf file.
        7) remove pbc with "gmx trjconv -pbc mol"

        :param deffnm: file base name
        :type deffnm: str
        :param runtype: type of the run: em, nvt, npt, md
        :type runtype: str
        :param restraints: True if restraints should be applied
        :type restraints: bool
        :param cont: True if this is a continuation of a previous run (i.e use the '-t' switch in grompp)
        :type cont: bool
        :param dorun: True if the actual run has to be done (i.e. gmx mdrun should be called). If False, only the input
                      files are created.
        :type dorun: bool
        :return: an instance of Results, containing the final state, extracted energy terms and the trajectory
        :rtype: Results
        """
        self.system.writeTopology(f"{deffnm}.top")
        self.system.conf.write(f"{deffnm}_init.gro")
        self.system.forcefield.mdp.save(f"{deffnm}.mdp")
        self.system.indexgroups.saveNDX(f"{deffnm}.ndx")
        self.engine.grompp(f"{deffnm}.mdp", f"{deffnm}_init.gro", f"{deffnm}.top", f"{deffnm}.tpr", indexfile=f"{deffnm}.ndx",
          restrfile=(f"{deffnm}_init.gro" if restraints else None),
          contfile=f"{self.lastdeffnm}.cpt" if (cont and self.lastdeffnm is not None) else None,
          maxwarn=(self.maxwarn))
        if dorun:
            self.engine.echo = True
            try:
                self.engine.mdrun((f"{deffnm}"), verbose=True, pin=True, cont=False)
            finally:
                self.engine.echo = False

            self.engine.trjconv_pbc(f"{deffnm}.tpr", f"{deffnm}.gro", f"{deffnm}_pbc.gro", f"{deffnm}.ndx", 'mol', 'System', 'System')
            self.system.conf.load(f"{deffnm}_pbc.gro")
            self.lastdeffnm = deffnm
            return Results(deffnm=deffnm,
              conf=(copy.deepcopy(self.system.conf)),
              energy=(self.extract_energy(deffnm, runtype)),
              trajectory=(Trajectory(f"{deffnm}.tng" if self.engine.prefer_tng else f"{deffnm}.trr", f"{deffnm}.tpr", self.engine, self.system.indexgroups)))
        return Results(deffnm=deffnm, conf=Coordinates(f"{deffnm}.gro", lazyload=True), energy={}, trajectory=(Trajectory(f"{deffnm}.tng" if self.engine.prefer_tng else f"{deffnm}.trr", f"{deffnm}.tpr", self.engine, self.system.indexgroups)))

    def extract_energy(self, deffnm, runtype: str) -> Dict[(str, XVGFile)]:
        """Extract energy terms after an MD run

        XVG files are written following the <deffnm>_energy_<type>.xvg scheme. Depending on the `runtype` parameter,
        the following types are written:

        Always:
            - all: all energy terms
            - bonded: bonded terms
            - nonbonded: non-bonded terms
            - interactions: all interaction terms and "Potential"
        'em':
            - potential: "Potential"
        'nvt':
            - temperature
            - energy: Potential, kinetic energy, total energy, conserved energy
        'npt':
            - temperature
            - energy: Potential, kinetic energy, total energy, conserved energy
            - density
            - boxsize: Box-X, Box-Y, Box-Z
            - volume
        'md':
            - temperature
            - energy: Potential, kinetic energy, total energy, conserved energy
            - density
            - boxsize: Box-X, Box-Y, Box-Z
            - volume

        Additionally, if constraints are used in the topology:
            - constraints: "Constr. rmsd"

        :param deffnm: file base name
        :type deffnm: str
        :param runtype: type of the run: 'em', 'nvt', 'npt', 'md
        :type runtype: str
        :return: dictionary of the XVG file data
        :rtype: dict of XVGFile objects
        """
        xvgs = {}
        self.engine.energy(f"{deffnm}.tpr", f"{deffnm}.edr", f"{deffnm}_energy_all.xvg")
        xvgs['all'] = XVGFile(f"{deffnm}_energy_all.xvg", lazyload=False)
        energyterms = xvgs['all'].columntitles[1:]
        energyterms = [et.replace(' ', '-') for et in energyterms]
        try:
            idx_LJ14 = energyterms.index('LJ-14')
        except ValueError:
            idx_LJ14 = energyterms.index('LJ-(SR)')

        idx_Potential = energyterms.index('Potential')
        self.engine.energy(f"{deffnm}.tpr", f"{deffnm}.edr", f"{deffnm}_energy_bonded.xvg", energyterms[:idx_LJ14])
        xvgs['bonded'] = XVGFile(f"{deffnm}_energy_bonded.xvg")
        self.engine.energy(f"{deffnm}.tpr", f"{deffnm}.edr", f"{deffnm}_energy_nonbonded.xvg", energyterms[idx_LJ14:idx_Potential])
        xvgs['nonbonded'] = XVGFile(f"{deffnm}_energy_nonbonded.xvg")
        self.engine.energy(f"{deffnm}.tpr", f"{deffnm}.edr", f"{deffnm}_energy_interactions.xvg", energyterms[:idx_Potential + 1])
        xvgs['interactions'] = XVGFile(f"{deffnm}_energy_interactions.xvg")
        if runtype == 'em':
            self.engine.energy(f"{deffnm}.tpr", f"{deffnm}.edr", f"{deffnm}_energy_potential.xvg", energyterms[idx_Potential:idx_Potential + 1])
            xvgs['potential'] = XVGFile(f"{deffnm}_energy_potential.xvg")
        if runtype in ('nvt', 'npt', 'md'):
            self.engine.energy(f"{deffnm}.tpr", f"{deffnm}.edr", f"{deffnm}_energy_temperature.xvg", ['Temperature'])
            self.engine.energy(f"{deffnm}.tpr", f"{deffnm}.edr", f"{deffnm}_energy_energy.xvg", [
             'Potential', 'Kinetic-En.', 'Total-Energy', 'Conserved-En.'])
            xvgs['temperature'] = XVGFile(f"{deffnm}_energy_temperature.xvg")
            xvgs['energy'] = XVGFile(f"{deffnm}_energy_energy.xvg")
        if runtype in ('npt', 'md'):
            self.engine.energy(f"{deffnm}.tpr", f"{deffnm}.edr", f"{deffnm}_energy_density.xvg", ['Density'])
            self.engine.energy(f"{deffnm}.tpr", f"{deffnm}.edr", f"{deffnm}_energy_boxsize.xvg", [
             'Box-X', 'Box-Y', 'Box-Z'])
            self.engine.energy(f"{deffnm}.tpr", f"{deffnm}.edr", f"{deffnm}_energy_volume.xvg", ['Volume'])
            xvgs['density'] = XVGFile(f"{deffnm}_energy_density.xvg")
            xvgs['boxsize'] = XVGFile(f"{deffnm}_energy_boxsize.xvg")
            xvgs['volume'] = XVGFile(f"{deffnm}_energy_volume.xvg")
        if 'Constr. rmsd' in energyterms:
            self.engine.energy(f"{deffnm}.tpr", f"{deffnm}.edr", f"{deffnm}_energy_constraints.xvg", ['Constr.-rmsd'])
            xvgs['constraints'] = XVGFile(f"{deffnm}_energy_constraints.xvg")
        return xvgs

    def genion(self, pname: str, nname: str, conc: float, solventgroup: str, neutralize: bool=True, pq: int=1, nq: int=-1, deffnm='ionize'):
        """Add ions to the system

        :param pname: name of the cation (molecule type name)
        :type pname: str
        :param nname: name of the anion (molecule type name)
        :type nname: str
        :param conc: concentration of ions to add (mol / liter)
        :type conc: float
        :param solventgroup: group of solvent atom indices
        :type solventgroup: str
        :param neutralize: True if neutral charge is to be ensured
        :type neutralize: bool
        :param pq: charge of the cation
        :type pq: int
        :param nq: charge of the anion
        :type nq: int
        :param deffnm: file base name
        :type deffnm: str
        """
        self.system.forcefield.mdp.ionize()
        self.system.forcefield.mdp.save(f"{deffnm}.mdp")
        self.system.indexgroups.saveNDX(f"{deffnm}.ndx")
        self.system.writeTopology(f"{deffnm}.top")
        self.engine.grompp(f"{deffnm}.mdp", (self.system.conf.filename), f"{deffnm}.top", f"{deffnm}.tpr", (self.system.conf.filename),
          None, f"{deffnm}.ndx", maxwarn=(self.maxwarn))
        self.engine.genion(f"{deffnm}.tpr", f"{deffnm}.ndx", f"{deffnm}.gro", solventgroup, pname, nname, conc, pq, nq, neutralize)
        self.system.conf.load(f"{deffnm}.gro")
        ptype = self.system.forcefield.moleculetype(pname)
        ntype = self.system.forcefield.moleculetype(nname)
        if ptype not in self.system.moleculetypes:
            self.system.moleculetypes.append(ptype)
        if ntype not in self.system.moleculetypes:
            self.system.moleculetypes.append(ntype)
        self.system.countMolecules()
        self.reindex()

    def solvate(self, solventbox: Coordinates, moltype: MoleculeType, deffnm: str='solvate'):
        """Solvate the system

        :param solventbox: equilibrated box of solvent
        :type solventbox: Coordinates instance
        :param moltype: molecule type of the solvent
        :type moltype: MoleculeType instance
        :param deffnm: file basename
        :type deffnm: str
        """
        self.system.conf.write(f"{deffnm}_system.g96")
        solventbox.write(f"{deffnm}_solventbox.g96")
        self.engine.solvate(f"{deffnm}_system.g96", f"{deffnm}_solventbox.g96", f"{deffnm}.g96")
        self.system.conf.load(f"{deffnm}.g96")
        if moltype not in self.system.moleculetypes:
            self.system.moleculetypes.append(moltype)
        self.system.countMolecules()
        self.reindex()