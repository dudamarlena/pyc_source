# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/mdp/mdp.py
# Compiled at: 2020-02-28 03:51:25
# Size of source mod 2**32: 8144 bytes
import textwrap
from typing import Optional, List
from .sections import RunControl, OutputControl, NeighbourSearch, ElectroStatics, VanderWaals, Constraints, Thermostat, Barostat, VelocityGeneration
from .. import environment
from ..templating import jinjaenv

class MDP:
    __doc__ = 'Represents the structure of an MDP file, with the following attributes corresponding to sections:\n        - runcontrol\n        - outputcontrol\n        - neighboursearch\n        - electrostatics\n        - vanderwaals\n        - constraints\n        - thermostat\n        - barostat\n        - velocitygeneration\n\n    Additionally, `defines` is a list of strings with the #define macros, except those required for position restraints\n    during NVT and NpT equilibration. Those should be stored in the `posresdefines` list.\n\n    This is implemented like a finite state machine. Whenever the user wants to generate an MDP file for a specific\n    MD run (energy minimization, equilibration etc.), the appropriate methods can be used to set the parameters\n    accordingly. The actual state can be written to a file by the `save()` method, and visualized in an user-friendly\n    format by repr() (or simply print()-ing it).\n    '
    runcontrol: RunControl
    outputcontrol: OutputControl
    neighboursearch: NeighbourSearch
    electrostatics: ElectroStatics
    vanderwaals: VanderWaals
    constraints: Constraints
    thermostat: Thermostat
    barostat: Barostat
    velocitygeneration: VelocityGeneration
    defines: List[str]
    posresdefines: List[str]

    def __init__(self, runcontrol: Optional[RunControl]=None, outputcontrol: Optional[OutputControl]=None, neighboursearch: Optional[NeighbourSearch]=None, electrostatics: Optional[ElectroStatics]=None, vanderwaals: Optional[VanderWaals]=None, constraints: Optional[Constraints]=None, thermostat: Optional[Thermostat]=None, barostat: Optional[Barostat]=None, velocitygeneration: Optional[VelocityGeneration]=None, defines: Optional[List[str]]=None):
        self.runcontrol = runcontrol if runcontrol is not None else RunControl()
        self.outputcontrol = outputcontrol if outputcontrol is not None else OutputControl()
        self.neighboursearch = neighboursearch if neighboursearch is not None else NeighbourSearch()
        self.electrostatics = electrostatics if electrostatics is not None else ElectroStatics()
        self.vanderwaals = vanderwaals if vanderwaals is not None else VanderWaals()
        self.constraints = constraints if constraints is not None else Constraints()
        self.thermostat = thermostat if thermostat is not None else Thermostat()
        self.barostat = barostat if barostat is not None else Barostat()
        self.velocitygeneration = velocitygeneration if velocitygeneration is not None else VelocityGeneration()
        self.defines = [] if defines is None else defines
        self.posresdefines = []

    def energyMinimization(self, nsteps: int=50000, emtol: float=100.0, emstep: float=0.01):
        """Set up for energy minimization with the steepest descent algorithm

        :param nsteps: number of steps
        :type nsteps: int
        :param emtol: force tolerance (kJ/mol/nm)
        :type emtol: float
        :param emstep: minimization step size (nm)
        :type emstep: float
        """
        self.runcontrol.integrator = 'steep'
        self.runcontrol.nsteps = nsteps
        self.runcontrol.emtol = emtol
        self.runcontrol.emstep = emstep
        self.thermostat.tcoupl = 'no'
        self.barostat.pcoupl = 'no'

    def ionize(self):
        """Set up for ionization using "gmx genion". Currently the same as `energyMinimization()` with its default
        parameters"""
        self.energyMinimization()

    def nvt(self, env: environment.Environment, runtime: float=100.0):
        """Set-up for equilibration in the NVT ensemble.

        Regardless of the coupling algorithm in `env.thermostat`, the Berendsen-type weak coupling algorithm is used.

        :param env: environment, containing a thermostat and a barostat
        :type env: gmxbatch.environment.Environment
        :param runtime: run time in ps
        :type runtime: float
        """
        self.runcontrol.integrator = 'md'
        self.runcontrol.nsteps = int(round(runtime / self.runcontrol.dt))
        self.thermostat.tcoupl = 'Berendsen'
        self.thermostat.tc_grps = env.thermostat.groups
        self.thermostat.ref_t = [env.thermostat.ref_temperature] * len(env.thermostat.groups)
        self.thermostat.tau_t = [env.thermostat.tau] * len(env.thermostat.groups)
        self.barostat.pcoupl = 'no'
        self.velocitygeneration.gen_vel = True
        self.velocitygeneration.gen_temp = env.thermostat.ref_temperature
        self.constraints.continuation = False

    def npt(self, env: environment.Environment, runtime: float=500):
        """Set-up for equilibration in the NpT ensemble.

        Regardless of the coupling algorithm in `env.thermostat` and `env.barostat`, the Berendsen-type weak coupling
        algorithm is used in both the thermostat and the barostat.

        :param env: environment, containing a thermostat and a barostat
        :type env: gmxbatch.environment.Environment
        :param runtime: run time in ps
        :type runtime: float
        """
        self.nvt(env, runtime=runtime)
        self.barostat.pcoupl = 'Berendsen'
        self.barostat.pcoupltype = env.barostat.couplingtype
        if env.barostat.couplingtype.lower() == 'isotropic':
            npars = 1
        else:
            if env.barostat.couplingtype.lower() == 'semiisotropic':
                npars = 2
            else:
                if env.barostat.couplingtype.lower() == 'anisotropic':
                    npars = 3
                else:
                    if env.barostat.couplingtype.lower() == 'surface-tension':
                        npars = 2
                    else:
                        raise ValueError('Invalid pressure coupling type: {}'.format(env.barostat.couplingtype))
        self.velocitygeneration.gen_vel = False
        self.constraints.continuation = True
        self.barostat.compressibility = [env.barostat.compressibility] * npars
        self.barostat.ref_p = [env.barostat.ref_pressure] * npars
        self.barostat.tau_p = env.barostat.tau
        self.barostat.refcoord_scaling = 'com'

    def md(self, env: environment.Environment, runtime: float=10000):
        """Set up for MD production run

        :param env: Environment instance, containing a thermostat and a barostat
        :type env: gmxbatch.environment.Environment
        :param runtime: requested run time (ps)
        :type runtime: float
        """
        self.npt(env, runtime)
        self.thermostat.tcoupl = env.thermostat.algorithm
        self.barostat.pcoupl = env.barostat.algorithm

    def save(self, filename: str):
        """Save the present state in an MDP file.

        :param filename: file name to save to
        :type filename: str
        """
        template = jinjaenv.get_template('mdp/base.mdp.jinja2')
        with open(filename, 'wt') as (f):
            for chunk in template.generate(mdp=self):
                f.write(chunk)

    def __repr__(self) -> str:
        return 'Molecular dynamics parameters\n  Defines: ' + ', '.join(self.defines) + '\n' + textwrap.indent(repr(self.runcontrol), '  ') + textwrap.indent(repr(self.outputcontrol), '  ') + textwrap.indent(repr(self.neighboursearch), '  ') + textwrap.indent(repr(self.electrostatics), '  ') + textwrap.indent(repr(self.vanderwaals), '  ') + textwrap.indent(repr(self.constraints), '  ') + textwrap.indent(repr(self.thermostat), '  ') + textwrap.indent(repr(self.barostat), '  ') + textwrap.indent(repr(self.velocitygeneration), '  ')