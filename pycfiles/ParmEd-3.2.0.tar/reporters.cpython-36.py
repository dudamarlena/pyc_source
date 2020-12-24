# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/openmm/reporters.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 35000 bytes
"""
This module contains a handful of extra reporter classes for OpenMM
simulations
"""
from __future__ import division, print_function
from parmed.amber.asciicrd import AmberMdcrd
from parmed.geometry import box_vectors_to_lengths_and_angles
from parmed.amber.netcdffiles import NetCDFTraj
from parmed.amber.readparm import Rst7
from parmed import unit as u
from parmed.utils.decorators import needs_openmm
from parmed.utils.six.moves import range
from math import isnan, isinf
from time import time
VELUNIT = u.angstrom / u.picosecond
FRCUNIT = u.kilocalorie_per_mole / u.angstrom

class StateDataReporter(object):
    __doc__ = "\n    This class acts as a state data reporter for OpenMM simulations, but it is a\n    little more generalized. Notable differences are:\n\n      -  It allows the units of the output to be specified, with defaults being\n         those used in Amber (e.g., kcal/mol, angstroms^3, etc.)\n      -  It will write to any object containing a 'write' method; not just\n         files. This allows, for instance, writing to a GUI window that\n         implements the desired 'write' attribute.\n\n    Most of this code is copied from the OpenMM StateDataReporter class, with\n    the above-mentioned changes made.\n\n    Parameters\n    ----------\n    f : str or file-like\n        Destination to write the state data (file name or file object)\n    reportInterval : int\n        Number of steps between state data reports\n    step : bool, optional\n        Print out the step number (Default True)\n    time : bool, optional\n        Print out the simulation time (Defaults True)\n    potentialEnergy : bool, optional\n        Print out the potential energy of the structure (Default True)\n    kineticEnergy : bool, optional\n        Print out the kinetic energy of the structure (Default True)\n    totalEnergy : bool, optional\n        Print out the total energy of the system (Default True)\n    temperature : bool, optional\n        Print out the temperature of the system (Default True)\n    volume : bool, optional\n        Print out the volume of the unit cell. If the system is not periodic,\n        the value is meaningless (Default False)\n    density : bool, optional\n        Print out the density of the unit cell. If the system is not periodic,\n        the value is meaningless (Default False)\n    separator : str, optional\n        The string to separate data fields (Default ',')\n    systemMass : float, optional\n        If not None, the density will be computed from this mass, since setting\n        a mass to 0 is used to constrain the position of that particle. (Default\n        None)\n    energyUnit : unit, optional\n        The units to print energies in (default unit.kilocalories_per_mole)\n    timeUnit : unit, optional\n        The units to print time in (default unit.picoseconds)\n    volumeUnit : unit, optional\n        The units print volume in (default unit.angstroms**3)\n    densityUnit : unit, optional\n        The units to print density in (default\n        unit.grams/unit.item/unit.milliliter)\n    "

    @needs_openmm
    def __init__(self, f, reportInterval, step=True, time=True, potentialEnergy=True, kineticEnergy=True, totalEnergy=True, temperature=True, volume=False, density=False, separator=',', systemMass=None, energyUnit=u.kilocalories_per_mole, timeUnit=u.picoseconds, volumeUnit=u.angstroms ** 3, densityUnit=u.grams / u.item / u.milliliter):
        self._reportInterval = reportInterval
        self._openedFile = not hasattr(f, 'write')
        if self._openedFile:
            self._out = open(f, 'w')
        else:
            self._out = f
        self._step = step
        self._time = time
        self._potentialEnergy = potentialEnergy
        self._kineticEnergy = kineticEnergy
        self._totalEnergy = totalEnergy
        self._temperature = temperature
        self._volume = volume
        self._density = density
        self._separator = separator
        self._totalMass = systemMass
        self._hasInitialized = False
        self._needsPositions = False
        self._needsVelocities = False
        self._needsForces = False
        self._needEnergy = potentialEnergy or kineticEnergy or totalEnergy or temperature
        self._energyUnit = energyUnit
        self._densityUnit = densityUnit
        self._timeUnit = timeUnit
        self._volumeUnit = volumeUnit

    def describeNextReport(self, simulation):
        """
        Get information about the next report this object will generate.

        Parameters
        ----------
        simulation : :class:`app.Simulation`
            The simulation to generate a report for

        Returns
        -------
        nsteps, pos, vel, frc, ene : int, bool, bool, bool, bool
            nsteps is the number of steps until the next report
            pos, vel, frc, and ene are flags indicating whether positions,
            velocities, forces, and/or energies are needed from the Context
        """
        steps_left = simulation.currentStep % self._reportInterval
        steps = self._reportInterval - steps_left
        return (steps, self._needsPositions, self._needsVelocities,
         self._needsForces, self._needEnergy)

    def report(self, simulation, state):
        """Generate a report.

        Parameters
        ----------
        simulation : :class:`app.Simulation`
            The Simulation to generate a report for
        state : :class:`mm.State`
            The current state of the simulation
        """
        if not self._hasInitialized:
            self._initializeConstants(simulation)
            headers = self._constructHeaders()
            self._out.write('#"%s"\n' % ('"' + self._separator + '"').join(headers))
            self._hasInitialized = True
        self._checkForErrors(simulation, state)
        values = self._constructReportValues(simulation, state)
        self._out.write(self._separator.join(str(v) for v in values) + '\n')
        hasattr(self._out, 'flush') and self._out.flush()

    def _constructReportValues(self, simulation, state):
        """
        Query the simulation for the current state of our observables of
        interest.

        Parameters
        ----------
        simulation : Simulation
            The Simulation object to generate a report for
        state : State
            The current state of the simulation object

        Returns: A list of values summarizing the current state of
        the simulation, to be printed or saved. Each element in the list
        corresponds to one of the columns in the resulting CSV file.
        """
        values = []
        if self._volume or self._density:
            volume = state.getPeriodicBoxVolume()
        if self._density:
            density = self._totalMass / volume
        ke = state.getKineticEnergy()
        pe = state.getPotentialEnergy()
        if self._temperature:
            temp = 2 * ke / (self._dof * u.MOLAR_GAS_CONSTANT_R)
        time = state.getTime()
        if self._step:
            values.append(simulation.currentStep)
        if self._time:
            values.append(time.value_in_unit(self._timeUnit))
        if self._potentialEnergy:
            values.append(pe.value_in_unit(self._energyUnit))
        if self._kineticEnergy:
            values.append(ke.value_in_unit(self._energyUnit))
        if self._totalEnergy:
            values.append((pe + ke).value_in_unit(self._energyUnit))
        if self._temperature:
            values.append(temp.value_in_unit(u.kelvin))
        if self._volume:
            values.append(volume.value_in_unit(self._volumeUnit))
        if self._density:
            values.append(density.value_in_unit(self._densityUnit))
        return values

    def _initializeConstants(self, simulation):
        """
        Initialize a set of constants required for the reports

        Parameters
        ----------
        simulation : Simulation
            The simulation to generate a report for
        """
        import simtk.openmm as mm
        system = simulation.system
        frclist = system.getForces()
        if self._temperature:
            dof = 0
            for i in range(system.getNumParticles()):
                if system.getParticleMass(i) > 0 * u.dalton:
                    dof += 3

            dof -= system.getNumConstraints()
            if any(isinstance(frc, mm.CMMotionRemover) for frc in frclist):
                dof -= 3
            self._dof = dof
        if self._density:
            if self._totalMass is None:
                self._totalMass = 0 * u.dalton
                for i in range(system.getNumParticles()):
                    self._totalMass += system.getParticleMass(i)

            elif not u.is_quantity(self._totalMass):
                self._totalMass = self._totalMass * u.dalton

    def _constructHeaders(self):
        """Construct the headers for the CSV output

        Returns: a list of strings giving the title of each observable being
                 reported on.
        """
        headers = []
        if self._step:
            headers.append('Step')
        if self._time:
            headers.append('Time (ps)')
        if self._potentialEnergy:
            headers.append('Potential Energy (%s)' % self._energyUnit)
        if self._kineticEnergy:
            headers.append('Kinetic Energy (%s)' % self._energyUnit)
        if self._totalEnergy:
            headers.append('Total Energy (%s)' % self._energyUnit)
        if self._temperature:
            headers.append('Temperature (K)')
        if self._volume:
            headers.append('Box Volume (%s)' % self._volumeUnit)
        if self._density:
            headers.append('Density (%s)' % self._densityUnit)
        return headers

    def _checkForErrors(self, simulation, state):
        """Check for errors in the current state of the simulation

        Parameters
        ----------
        simulation : :class:`app.Simulation`
            The Simulation to generate a report for
        state : :class:`State`
            The current state of the simulation
        """
        if self._needEnergy:
            energy = state.getKineticEnergy() + state.getPotentialEnergy()
            if isnan(energy._value):
                raise ValueError('Energy is NaN')
            if isinf(energy._value):
                raise ValueError('Energy is infinite')

    def __del__(self):
        if hasattr(self, '_openedFile'):
            if self._openedFile:
                self._out.close()

    def finalize(self):
        """ Closes any open file """
        try:
            if self._out is not None:
                if self._openedFile:
                    self._out.close()
        except AttributeError:
            pass


class NetCDFReporter(object):
    __doc__ = ' NetCDFReporter prints a trajectory in NetCDF format '

    @needs_openmm
    def __init__(self, file, reportInterval, crds=True, vels=False, frcs=False):
        """
        Create a NetCDFReporter instance.

        Parameters
        ----------
        file : str
            Name of the file to write the trajectory to
        reportInterval : int
            How frequently to write a frame to the trajectory
        crds : bool=True
            Should we write coordinates to this trajectory? (Default True)
        vels : bool=False
            Should we write velocities to this trajectory? (Default False)
        frcs : bool=False
            Should we write forces to this trajectory? (Default False)
        """
        if not crds:
            if not vels:
                if not frcs:
                    raise ValueError('You must print either coordinates, velocities, or forces in a NetCDFReporter')
        self.crds, self.vels, self.frcs = crds, vels, frcs
        self._reportInterval = reportInterval
        self._out = None
        self.fname = file

    def describeNextReport(self, simulation):
        """
        Get information about the next report this object will generate.

        Parameters
        ----------
        simulation : :class:`app.Simulation`
            The Simulation to generate a report for

        Returns
        -------
        nsteps, pos, vel, frc, ene : int, bool, bool, bool, bool
            nsteps is the number of steps until the next report
            pos, vel, frc, and ene are flags indicating whether positions,
            velocities, forces, and/or energies are needed from the Context
        """
        stepsleft = simulation.currentStep % self._reportInterval
        steps = self._reportInterval - stepsleft
        return (steps, self.crds, self.vels, self.frcs, False)

    def report(self, simulation, state):
        """Generate a report.

        Parameters
        ----------
        simulation : :class:`app.Simulation`
            The Simulation to generate a report for
        state : :class:`mm.State`
            The current state of the simulation
        """
        global FRCUNIT
        global VELUNIT
        if self.crds:
            crds = state.getPositions().value_in_unit(u.angstrom)
        else:
            if self.vels:
                vels = state.getVelocities().value_in_unit(VELUNIT)
            else:
                if self.frcs:
                    frcs = state.getForces().value_in_unit(FRCUNIT)
                else:
                    if self._out is None:
                        if self.crds:
                            atom = len(crds)
                        else:
                            if self.vels:
                                atom = len(vels)
                            else:
                                if self.frcs:
                                    atom = len(frcs)
                        self.uses_pbc = simulation.topology.getUnitCellDimensions() is not None
                        self._out = NetCDFTraj.open_new((self.fname),
                          atom, (self.uses_pbc), (self.crds), (self.vels), (self.frcs),
                          title='ParmEd-created trajectory using OpenMM')
                    if self.uses_pbc:
                        vecs = state.getPeriodicBoxVectors()
                        lengths, angles = box_vectors_to_lengths_and_angles(*vecs)
                        self._out.add_cell_lengths_angles(lengths.value_in_unit(u.angstrom), angles.value_in_unit(u.degree))
                    if self.crds:
                        self._out.add_coordinates(crds)
                if self.vels:
                    self._out.add_velocities(vels)
            if self.frcs:
                self._out.add_forces(frcs)
        self._out.add_time(state.getTime().value_in_unit(u.picosecond))

    def __del__(self):
        try:
            if self._out is not None:
                self._out.close()
        except AttributeError:
            pass

    def finalize(self):
        """ Closes any open file """
        try:
            if self._out is not None:
                self._out.close()
        except AttributeError:
            pass


class MdcrdReporter(object):
    __doc__ = '\n    MdcrdReporter prints a trajectory in ASCII Amber format. This reporter will\n    be significantly slower than binary file reporters (like DCDReporter or\n    NetCDFReporter).\n\n    Parameters\n    ----------\n    file : str\n        Name of the file to write the trajectory to\n    reportInterval : int\n        Number of steps between writing trajectory frames\n    crds : bool=True\n        Write coordinates to this trajectory file?\n    vels : bool=False\n        Write velocities to this trajectory file?\n    frcs : bool=False\n        Write forces to this trajectory file?\n\n    Notes\n    -----\n    You can only write one of coordinates, forces, or velocities to a mdcrd\n    file.\n    '

    @needs_openmm
    def __init__(self, file, reportInterval, crds=True, vels=False, frcs=False):
        ntrue = 0
        if crds:
            ntrue += 1
        if vels:
            ntrue += 1
        if frcs:
            ntrue += 1
        if ntrue != 1:
            raise ValueError('MdcrdReporter must print exactly one of either coordinates, velocities, or forces.')
        self.crds, self.vels, self.frcs = crds, vels, frcs
        self._reportInterval = reportInterval
        self._out = None
        self.fname = file

    def describeNextReport(self, simulation):
        """
        Get information about the next report this object will generate.

        Parameters
        ----------
        simulation : :class:`app.Simulation`
            The Simulation to generate a report for

        Returns
        -------
        nsteps, pos, vel, frc, ene : int, bool, bool, bool, bool
            nsteps is the number of steps until the next report
            pos, vel, frc, and ene are flags indicating whether positions,
            velocities, forces, and/or energies are needed from the Context
        """
        stepsleft = simulation.currentStep % self._reportInterval
        steps = self._reportInterval - stepsleft
        return (steps, self.crds, self.vels, self.frcs, False)

    def report(self, simulation, state):
        """
        Generate a report.

        Parameters:
            - simulation (Simulation) The Simulation to generate a report for
            - state (State) The current state of the simulation
        """
        from parmed.amber.asciicrd import VELSCALE
        if self.crds:
            crds = state.getPositions().value_in_unit(u.angstrom)
        else:
            if self.vels:
                vels = state.getVelocities().value_in_unit(VELUNIT)
            else:
                if self.frcs:
                    frcs = state.getForces().value_in_unit(FRCUNIT)
        if self._out is None:
            if self.crds:
                self.atom = len(crds)
            else:
                if self.vels:
                    self.atom = len(vels)
                else:
                    if self.frcs:
                        self.atom = len(frcs)
            self.uses_pbc = simulation.topology.getUnitCellDimensions() is not None
            self._out = AmberMdcrd((self.fname), (self.atom), (self.uses_pbc), title='ParmEd-created trajectory using OpenMM',
              mode='w')
        if self.crds:
            flatcrd = [0 for i in range(self.atom * 3)]
            for i in range(self.atom):
                i3 = i * 3
                flatcrd[i3], flatcrd[i3 + 1], flatcrd[i3 + 2] = crds[i]

            self._out.add_coordinates(flatcrd)
        if self.vels:
            vels = [v / VELSCALE for v in vels]
            flatvel = [0 for i in range(self.atom * 3)]
            for i in range(self.atom):
                i3 = i * 3
                flatvel[i3], flatvel[i3 + 1], flatvel[i3 + 2] = vels[i]

            self._out.add_coordinates(flatvel)
        if self.frcs:
            flatfrc = [0 for i in range(self.atom * 3)]
            for i in range(self.atom):
                i3 = i * 3
                flatfrc[i3], flatfrc[i3 + 1], flatfrc[i3 + 2] = frcs[i]

            self._out.add_coordinates(flatfrc)
        if self.uses_pbc:
            boxvecs = state.getPeriodicBoxVectors()
            lengths, angles = box_vectors_to_lengths_and_angles(*boxvecs)
            self._out.add_box(lengths.value_in_unit(u.angstroms))

    def __del__(self):
        try:
            if self._out is not None:
                self._out.close()
        except AttributeError:
            pass

    def finalize(self):
        """ Closes any open file """
        try:
            if self._out is not None:
                self._out.close()
        except AttributeError:
            pass


class RestartReporter(object):
    __doc__ = '\n    Use a reporter to handle writing restarts at specified intervals.\n\n    Parameters\n    ----------\n    file : str\n        Name of the file to write the restart to.\n    reportInterval : int\n        Number of steps between writing restart files\n    write_multiple : bool=False\n        Either write a separate restart each time (appending the step number in\n        the format .# to the file name given above) if True, or overwrite the\n        same file each time if False\n    netcdf : bool=False\n        Use the Amber NetCDF restart file format\n    write_velocities : bool=True\n        Write velocities to the restart file. You can turn this off for passing\n        in, for instance, a minimized structure.\n    '

    @needs_openmm
    def __init__(self, file, reportInterval, write_multiple=False, netcdf=False, write_velocities=True):
        self.fname = file
        self._reportInterval = reportInterval
        self.write_multiple = write_multiple
        self.netcdf = netcdf
        self.write_velocities = write_velocities
        self.rst7 = None

    def describeNextReport(self, simulation):
        """
        Get information about the next report this object will generate.

        Parameters
        ----------
        simulation : :class:`app.Simulation`
            The Simulation to generate a report for

        Returns
        -------
        nsteps, pos, vel, frc, ene : int, bool, bool, bool, bool
            nsteps is the number of steps until the next report
            pos, vel, frc, and ene are flags indicating whether positions,
            velocities, forces, and/or energies are needed from the Context
        """
        stepsleft = simulation.currentStep % self._reportInterval
        steps = self._reportInterval - stepsleft
        return (steps, True, True, False, False)

    def report(self, sim, state):
        """Generate a report.

        Parameters
        ----------
        sim : :class:`app.Simulation`
            The Simulation to generate a report for
        state : :class:`mm.State`
            The current state of the simulation
        """
        crds = state.getPositions().value_in_unit(u.angstrom)
        if self.rst7 is None:
            self.uses_pbc = sim.topology.getUnitCellDimensions() is not None
            self.atom = len(crds)
            self.rst7 = Rst7(natom=(self.atom), title='Restart file written by ParmEd with OpenMM')
        else:
            self.rst7.time = state.getTime().value_in_unit(u.picosecond)
            flatcrd = [0.0 for i in range(self.atom * 3)]
            for i in range(self.atom):
                i3 = i * 3
                flatcrd[i3], flatcrd[i3 + 1], flatcrd[i3 + 2] = crds[i]

            self.rst7.coordinates = flatcrd
            if self.write_velocities:
                vels = state.getVelocities().value_in_unit(VELUNIT)
                flatvel = [0.0 for i in range(self.atom * 3)]
                for i in range(self.atom):
                    i3 = i * 3
                    flatvel[i3], flatvel[i3 + 1], flatvel[i3 + 2] = vels[i]

                self.rst7.vels = flatvel
            if self.uses_pbc:
                boxvecs = state.getPeriodicBoxVectors()
                lengths, angles = box_vectors_to_lengths_and_angles(*boxvecs)
                lengths = lengths.value_in_unit(u.angstrom)
                angles = angles.value_in_unit(u.degree)
                self.rst7.box = [lengths[0], lengths[1], lengths[2],
                 angles[0], angles[1], angles[2]]
            if self.write_multiple:
                fname = self.fname + '.%d' % sim.currentStep
            else:
                fname = self.fname
        self.rst7.write(fname, self.netcdf)

    def finalize(self):
        """ No-op here """
        pass


class ProgressReporter(StateDataReporter):
    __doc__ = '\n    A class that prints out a progress report of how much MD (or minimization)\n    has been done, how fast the simulation is running, and how much time is left\n    (similar to the mdinfo file in Amber)\n\n    Parameters\n    ----------\n    f : str\n        The file name of the progress report file (overwritten each time)\n    reportInterval : int\n        The step interval between which to write frames\n    totalSteps : int\n        The total number of steps that will be run in the simulation (used to\n        estimate time remaining)\n    potentialEnergy : bool, optional\n        Whether to print the potential energy (default True)\n    kineticEnergy : bool, optional\n        Whether to print the kinetic energy (default True)\n    totalEnergy : bool, optional\n        Whether to print the total energy (default True)\n    temperature : bool, optional\n        Whether to print the system temperature (default True)\n    volume : bool, optional\n        Whether to print the system volume (default False)\n    density : bool, optional\n        Whether to print the system density (default False)\n    systemMass : float or :class:`unit.Quantity`\n        The mass of the system used when reporting density (useful in instances\n        where masses are set to 0 to constrain their positions)\n\n    See Also\n    --------\n    In addition to the above, ProgressReporter also accepts arguments for\n    StateDataReporter\n    '

    @needs_openmm
    def __init__(self, f, reportInterval, totalSteps, potentialEnergy=True, kineticEnergy=True, totalEnergy=True, temperature=False, volume=False, density=False, systemMass=None, **kwargs):
        kwargs['time'] = kwargs['step'] = True
        (super(ProgressReporter, self).__init__)(
 f, reportInterval, potentialEnergy=potentialEnergy, kineticEnergy=kineticEnergy, 
         totalEnergy=totalEnergy, temperature=temperature, 
         volume=volume, density=density, systemMass=systemMass, **kwargs)
        if not self._openedFile:
            raise ValueError('ProgressReporter requires a file name (not file object)')
        self._out.close()
        del self._out
        self.fname = f
        self._totalSteps = totalSteps
        self._startTime = None
        self._firstStep = None
        self._lastReportTime = None
        self._timeStep = None

    def describeNextReport(self, simulation):
        """
        Get information about the next report this object will generate.

        Parameters
        ----------
        simulation : :class:`app.Simulation`
            The Simulation to generate a report for

        Returns
        -------
        nsteps, pos, vel, frc, ene : int, bool, bool, bool, bool
            nsteps is the number of steps until the next report
            pos, vel, frc, and ene are flags indicating whether positions,
            velocities, forces, and/or energies are needed from the Context
        """
        if self._startTime is None:
            self._startTime = time()
            self._lastReportTime = time()
            self._timeStep = simulation.integrator.getStepSize()
            self._timeStep = self._timeStep.value_in_unit(u.nanosecond)
            self._firstStep = simulation.currentStep
        stepsleft = simulation.currentStep % self._reportInterval
        steps = self._reportInterval - stepsleft
        return (steps, False, False, False, self._needEnergy)

    def report(self, simulation, state):
        """
        Generate a report and predict the time to completion (and
        current/overall MD performance)
        """
        if not self._hasInitialized:
            self._initializeConstants(simulation)
            self._hasInitialized = True
        self._checkForErrors(simulation, state)
        values = self._constructReportValues(simulation, state)
        now = time()
        total_time = now - self._startTime
        partial_time = now - self._lastReportTime
        self._lastReportTime = now
        total_nsperday = (values['step'] - self._firstStep) * self._timeStep / total_time
        partial_nsperday = self._reportInterval * self._timeStep / partial_time
        total_nsperday *= 86400
        partial_nsperday *= 86400
        remaining_steps = self._totalSteps - values['step'] + self._firstStep
        etc = partial_time / self._reportInterval * remaining_steps
        etc, unitstr = _format_time(etc)
        with open(self.fname, 'w') as (f):
            f.write('-+' * 39 + '\n')
            f.write('\n')
            f.write('  On step %d of %d\n' % (values['step'] - self._firstStep,
             self._totalSteps))
            f.write('\n')
            if self._totalEnergy:
                f.write('  Total Energy     = %12.4f\n' % values['totalEnergy'])
            if self._potentialEnergy:
                f.write('  Potential Energy = %12.4f\n' % values['potentialEnergy'])
            if self._kineticEnergy:
                f.write('  Kinetic Energy   = %12.4f\n' % values['kineticEnergy'])
            if self._volume:
                f.write('  Volume           = %12.4f\n' % values['volume'])
            if self._density:
                f.write('  Density          = %12.4f\n' % values['density'])
            if self._temperature:
                f.write('  Temperature      = %12.4f\n' % values['temperature'])
            f.write('\n')
            f.write(' Time for last %8d steps: %10.4f s. (%.3f ns/day)\n' % (
             self._reportInterval, partial_time, partial_nsperday))
            f.write(' Time for all %9d steps: %10.4f s. (%.3f ns/day)\n' % (
             values['step'] - self._firstStep, total_time, total_nsperday))
            f.write('\n')
            f.write(' Estimated time to completion: %.3f %s\n' % (etc, unitstr))
            f.write('\n')
            f.write('-+' * 39 + '\n')
        if remaining_steps == 0:
            self._startTime = None

    def _constructReportValues(self, simulation, state):
        """
        Query the simulation for the current state of our observables of
        interest.

        Parameters:
            - simulation (Simulation) The Simulation to generate a report for
            - state (State) The current state of the simulation

        Returns: A list of values summarizing the current state of the
            simulation, to be printed or saved. Each element in the list
            corresponds to one of the columns in the resulting CSV file.
        """
        values = dict()
        values['step'] = simulation.currentStep
        values['time'] = state.getTime()
        volume = state.getPeriodicBoxVolume()
        pe = state.getPotentialEnergy().value_in_unit(self._energyUnit)
        ke = state.getKineticEnergy()
        if self._temperature:
            temp = 2 * ke / (self._dof * u.MOLAR_GAS_CONSTANT_R)
        ke = ke.value_in_unit(self._energyUnit)
        if self._potentialEnergy:
            values['potentialEnergy'] = pe
        if self._kineticEnergy:
            values['kineticEnergy'] = ke
        if self._totalEnergy:
            values['totalEnergy'] = pe + ke
        if self._temperature:
            values['temperature'] = temp.value_in_unit(u.kelvin)
        if self._volume:
            values['volume'] = volume.value_in_unit(self._volumeUnit)
        if self._density:
            dens = self._totalMass / volume
            values['density'] = dens.value_in_unit(self._densityUnit)
        return values

    def __del__(self):
        """ We already closed the file. """
        pass


class EnergyMinimizerReporter(StateDataReporter):
    __doc__ = "\n    This class acts as a simple energy reporter class for minimizations. This\n    is not meant to be used as a reporter for OpenMM's molecular dynamics\n    routines, but instead passed a simulation object for printing out\n    single-point energies.\n\n    Parameters\n    ----------\n    f : str or file-like\n        File name or object to write energies to\n    volume : bool, optional\n        If True, write the system volume (default is False)\n    "

    def __init__(self, f, volume=False, **kwargs):
        (super(EnergyMinimizerReporter, self).__init__)(f, 1, **kwargs)
        self._volume = volume

    def describeNextReport(self, *args, **kwargs):
        """ Disable this reporter inside MD """
        raise NotImplementedError('EnergyMinimizerReporter is not intended for use in reporting on molecular dynamics')

    def report(self, simulation, frame=None):
        """ Print out the current energy """
        has_pbc = simulation.topology.getUnitCellDimensions() is not None
        state = simulation.context.getState(getEnergy=True, enforcePeriodicBox=has_pbc)
        if frame is not None:
            self._out.write('Frame: %10d\n' % frame)
        e = state.getPotentialEnergy().value_in_unit(self._energyUnit)
        self._out.write('   Potential Energy = %12.4f %s\n' % (e,
         self._energyUnit))
        if has_pbc:
            if self._volume or self._density:
                vol = state.getPeriodicBoxVolume().value_in_unit(self._volumeUnit)
        if has_pbc:
            if self._volume:
                self._out.write('   Volume = %12.4f %s\n' % (vol, self._volumeUnit))
        self._out.write('\n')

    def finalize(self):
        """ Closes any open file """
        try:
            if self._out is not None:
                self._out.close()
        except AttributeError:
            pass


def _format_time(etc):
    """ Formats how time is printed in ProgressReporter """
    if etc > 3600:
        etc /= 3600
        unitstr = 'hr.'
    else:
        if etc > 60:
            etc /= 60
            unitstr = 'min.'
        else:
            unitstr = 'sec.'
    return (
     etc, unitstr)