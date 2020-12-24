# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ad254919/aiida_plugin/aiida-bigdft/aiida_bigdft/PyBigDFT/BigDFT/Logfiles.py
# Compiled at: 2019-08-13 04:02:39
__doc__ = '\nThis module is useful to process a logfile of BigDFT run, in yaml format.\nIt also provides some tools to extract typical informations about the run,\nlike the energy, the eigenvalues and so on.\n'
EVAL = 'eval'
SETUP = 'let'
INITIALIZATION = 'globals'
PATH = 'path'
PRINT = 'print'
GLOBAL = 'global'
FLOAT_SCALAR = 'scalar'
PRE_POST = [
 EVAL, SETUP, INITIALIZATION]
BUILTIN = {'n_orb': {PATH: [['Total Number of Orbitals']], PRINT: 'Total Number of Orbitals', 
             GLOBAL: True}, 
   'astruct': {PATH: [['Atomic structure']]}, 'data_directory': {PATH: [['Data Writing directory']]}, 'dipole': {PATH: [['Electric Dipole Moment (AU)', 'P vector']], PRINT: 'Dipole (AU)'}, 
   'electrostatic_multipoles': {PATH: [['Multipole coefficients']]}, 'energy': {PATH: [['Last Iteration', 'FKS'], ['Last Iteration', 'EKS'], ['Energy (Hartree)']], PRINT: 'Energy', 
              GLOBAL: False}, 
   'evals': {PATH: [['Complete list of energy eigenvalues'], ['Ground State Optimization', -1, 'Orbitals'],
                  [
                   'Ground State Optimization', -1, 'Hamiltonian Optimization', -1, 'Subspace Optimization', 'Orbitals']]}, 
   'fermi_level': {PATH: [['Ground State Optimization', -1, 'Fermi Energy'], ['Ground State Optimization', -1, 'Hamiltonian Optimization', -1, 'Subspace Optimization', 'Fermi Energy']], PRINT: True, 
                   GLOBAL: False}, 
   'forcemax': {PATH: [['Geometry', 'FORCES norm(Ha/Bohr)', 'maxval'], ['Clean forces norm (Ha/Bohr)', 'maxval']], PRINT: 'Max val of Forces'}, 
   'forcemax_cv': {PATH: [['geopt', 'forcemax']], PRINT: 'Convergence criterion on forces', GLOBAL: True, FLOAT_SCALAR: True}, 'force_fluct': {PATH: [['Geometry', 'FORCES norm(Ha/Bohr)', 'fluct']], PRINT: 'Threshold fluctuation of Forces'}, 'forces': {PATH: [['Atomic Forces (Ha/Bohr)']]}, 'gnrm_cv': {PATH: [['dft', 'gnrm_cv']], PRINT: 'Convergence criterion on Wfn. Residue', GLOBAL: True}, 'kpts': {PATH: [['K points']], PRINT: False, 
            GLOBAL: True}, 
   'kpt_mesh': {PATH: [['kpt', 'ngkpt']], PRINT: True, GLOBAL: True}, 'magnetization': {PATH: [['Ground State Optimization', -1, 'Total magnetization'],
                          [
                           'Ground State Optimization', -1, 'Hamiltonian Optimization', -1, 'Subspace Optimization', 'Total magnetization']], 
                     PRINT: 'Total magnetization of the system'}, 
   'memory_run': {PATH: [['Accumulated memory requirements during principal run stages (MiB.KiB)']]}, 'memory_quantities': {PATH: [['Memory requirements for principal quantities (MiB.KiB)']]}, 'memory_peak': {PATH: [['Estimated Memory Peak (MB)']]}, 'nat': {PATH: [['Atomic System Properties', 'Number of atoms']], PRINT: 'Number of Atoms', 
           GLOBAL: True}, 
   'pressure': {PATH: [['Pressure', 'GPa']], PRINT: True}, 'sdos': {PATH: [['SDos files']], GLOBAL: True}, 'support_functions': {PATH: [['Gross support functions moments', 'Multipole coefficients', 'values']]}, 'symmetry': {PATH: [['Atomic System Properties', 'Space group']], PRINT: 'Symmetry group', 
                GLOBAL: True}}

def get_logs(files):
    """
    Return a list of loaded logfiles from files, which is a list
    of paths leading to logfiles.

    :param files: List of filenames indicating the logfiles
    :returns: List of Logfile instances associated to filename
    """
    from futile import YamlIO
    logs = []
    for filename in files:
        logs += YamlIO.load(filename, doc_lists=True, safe_mode=True)

    return logs


def floatify(scalar):
    """
    Useful to make float from strings compatible from fortran

    Args:
       scalar (str, float): When string representing a float that might be given in fortran notation,
       otherwise it might be a floating point
    Returns:
       float. The value associated to scalar as a floating point number

    Example:
       >>> floatify('1.d-4') #this would be the same with "1.e-4" or with 0.0001
       1.e-4

    """
    import numpy
    if isinstance(scalar, str):
        return float(scalar.replace('d', 'e').replace('D', 'E'))
    else:
        return scalar


def document_quantities(doc, to_extract):
    """
    Extract information from the runs.

    .. warning::
        This routine was designed for the previous parse_log.py script and it is here only for
        backward compatibility purposes.
    """
    analysis = {}
    for quantity in to_extract:
        if quantity in PRE_POST:
            continue
        field = to_extract[quantity]
        if type(field) is not type([]) is not type({}) and field in BUILTIN:
            paths = BUILTIN[field][PATH]
        else:
            paths = [
             field]
        for path in paths:
            value = doc
            for key in path:
                try:
                    value = value[key]
                except:
                    value = None
                    break

            if value is not None:
                break

        analysis[quantity] = value

    return analysis


def perform_operations(variables, ops, debug=False):
    """
    Perform operations given by 'ops'.
    'variables' is a dictionary of variables i.e. key=value.

    .. warning::
       This routine was designed for the previous parse_log.py script and it is here only for
       backward compatibility purposes.
    """
    for key in variables:
        command = key + '=' + str(variables[key])
        if debug:
            print command
        exec command

    if debug:
        print ops
    exec ops in globals(), locals()


def process_logfiles(files, instructions, debug=False):
    """
    Process the logfiles in files with the dictionary 'instructions'.

    .. warning::
       This routine was designed for the previous parse_log.py script and it is here only for
       backward compatibility purposes.
    """
    import sys
    glstr = 'global __LAST_FILE__ \n'
    glstr += '__LAST_FILE__=' + str(len(files)) + '\n'
    if INITIALIZATION in instructions:
        for var in instructions[INITIALIZATION]:
            glstr += 'global ' + var + '\n'
            glstr += var + ' = ' + str(instructions[INITIALIZATION][var]) + '\n'

    exec glstr in globals(), locals()
    for f in files:
        sys.stderr.write('#########processing ' + f + '\n')
        datas = get_logs([f])
        for doc in datas:
            doc_res = document_quantities(doc, instructions)
            if EVAL in instructions:
                perform_operations(doc_res, instructions[EVAL], debug=debug)


def find_iterations(log):
    """
    Identify the different block of the iterations of the wavefunctions optimization.

    .. todo::
       Should be generalized and checked for mixing calculation and O(N) logfiles

    :param log: logfile load
    :type log: dictionary
    :returns: wavefunction residue per iterations, per each subspace diagonalization
    :rtype: numpy array of rank two
    """
    import numpy
    for itrp in log['Ground State Optimization']:
        rpnrm = []
        for itsp in itrp['Hamiltonian Optimization']:
            gnrm_sp = []
            for it in itsp['Subspace Optimization']['Wavefunctions Iterations']:
                if 'gnrm' in it:
                    gnrm_sp.append(it['gnrm'])

            rpnrm.append(numpy.array(gnrm_sp))

    rpnrm = numpy.array(rpnrm)
    return rpnrm


def plot_wfn_convergence(wfn_it, gnrm_cv, label=None):
    """
    Plot the convergence of the wavefunction coming from the find_iterations function.
    Cumulates the plot in matplotlib.pyplot module

    :param wfn_it: list coming from :func:`find_iterations`
    :param gnrm_cv: convergence criterion for the residue of the wfn_it list
    :param label: label for the given plot
    """
    import matplotlib.pyplot as plt, numpy
    plt.semilogy(numpy.ravel(wfn_it), label=label)
    plt.legend(loc='upper right')
    plt.axhline(gnrm_cv, color='k', linestyle='--')
    it = 0
    for itrp in wfn_it:
        it += len(itrp)
        plt.axvline(it, color='k', linestyle='--')


class Logfile():
    """
    Import a Logfile from a filename in yaml format, a list of filenames,
    an archive (compressed tar file), a dictionary or a list of dictionaries.

    :param args: logfile names to be parsed
    :type args: strings
    :param kwargs: keyword arguments

       * archive: name of the archive from which retrieve the logfiles
       * member: name of the logfile within the archive. If absent, all the files of the archive will be considered as args
       * label: the label of the logfile instance
       * dictionary: parsed logfile given as a dictionary, serialization of the yaml logfile

    :Example:
       >>> l = Logfile('one.yaml','two.yaml')
       >>> l = Logfile(archive='calc.tgz')
       >>> l = Logfile(archive='calc.tgz',member='one.yaml')
       >>> l = Logfile(dictionary=dict1)
       >>> l = Logfile(dictionary=[dict1, dict2])

    .. todo::
       Document the automatically generated attributes, perhaps via an inner function
       in futile python module

    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the class
        """
        import os
        dicts = []
        arch = kwargs.get('archive')
        member = kwargs.get('member')
        label = kwargs.get('label')
        dictionary = kwargs.get('dictionary')
        if arch:
            import tarfile
            from futile import YamlIO
            tar = tarfile.open(arch)
            members = [tar.getmember(member)] if member else tar.getmembers()
            for memb in members:
                f = tar.extractfile(memb)
                dicts.append(YamlIO.load(stream=f.read()))

            srcdir = os.path.dirname(arch)
            label = label if label is not None else arch
        elif dictionary:
            dicts = [dictionary] if isinstance(dictionary, dict) else [ d for d in dictionary ]
            srcdir = ''
            label = label if label is not None else 'dict'
        elif args:
            dicts = get_logs(args)
            label = label if label is not None else args[0]
            srcdir = os.path.dirname(args[0])
        self.label = label
        self.srcdir = os.path.abspath('.' if srcdir == '' else srcdir)
        if not dicts:
            raise ValueError('No log information provided.')
        self._initialize_class(dicts[0])
        if len(dicts) > 1:
            self._instances = []
            for i, d in enumerate(dicts):
                label = 'log' + str(i)
                dtmp = dicts[0]
                instance = Logfile(dictionary=dtmp, label=label)
                instance._initialize_class(d)
                self._instances.append(instance)

            print ('Found', len(self._instances), 'different runs')
            import numpy
            ens = [ l.energy if hasattr(l, 'energy') else 1e+100 for l in self._instances ]
            self.reference_log = numpy.argmin(ens)
            self._initialize_class(dicts[self.reference_log])
        return

    def __getitem__(self, index):
        if hasattr(self, '_instances'):
            return self._instances[index]
        raise ValueError('This instance of Logfile has no multiple instances')

    def __str__(self):
        """Display short information about the logfile"""
        return self._print_information()

    def __len__(self):
        if hasattr(self, '_instances'):
            return len(self._instances)
        else:
            return 0

    def _initialize_class(self, d):
        import numpy
        self.log = d
        sublog = document_quantities(self.log, {val:val for val in BUILTIN})
        for att, val in sublog.items():
            if val is not None:
                val_tmp = floatify(val) if BUILTIN[att].get(FLOAT_SCALAR) else val
                setattr(self, att, val_tmp)
            elif hasattr(self, att) and not BUILTIN[att].get(GLOBAL):
                delattr(self, att)

        if not hasattr(self, 'fermi_level') and hasattr(self, 'evals'):
            self._fermi_level_from_evals(self.evals)
        if hasattr(self, 'kpts'):
            self.nkpt = len(self.kpts)
            if hasattr(self, 'evals'):
                self.evals = self._get_bz(self.evals, self.kpts)
            if hasattr(self, 'forces') and hasattr(self, 'astruct'):
                self.astruct.update({'forces': self.forces})
                delattr(self, 'forces')
        else:
            if hasattr(self, 'evals'):
                import BZ
                self.evals = [BZ.BandArray(self.evals)]
            if hasattr(self, 'sdos'):
                import os
                sd = []
                for f in self.sdos:
                    try:
                        data = numpy.loadtxt(os.path.join(self.srcdir, f))
                    except:
                        data = None

                    if data is not None:
                        xs = []
                        ba = [[], []]
                        for line in data:
                            xs.append(line[0])
                            ss = self._sdos_line_to_orbitals(line)
                            for ispin in [0, 1]:
                                ba[ispin].append(ss[ispin])

                        sd.append({'coord': xs, 'dos': ba})
                    else:
                        sd.append(None)

                self.sdos = sd
            self.memory = {}
            for key in ['memory_run', 'memory_quantities', 'memory_peak']:
                if hasattr(self, key):
                    title = BUILTIN[key][PATH][0][0]
                    self.memory[title] = getattr(self, key)
                    if key != 'memory_peak':
                        delattr(self, key)

        return

    def _fermi_level_from_evals(self, evals):
        import numpy
        fl = None
        for iorb, ev in enumerate(evals):
            e = ev.get('e')
            if e is not None:
                fref = ev['f'] if iorb == 0 else fref
                fl = e
                if ev['f'] < 0.5 * fref:
                    break
            e = ev.get('e_occ', ev.get('e_occupied'))
            if e is not None:
                fl = e if not isinstance(e, list) else numpy.max(numpy.array(e))
            e = ev.get('e_vrt', ev.get('e_virt'))
            if e is not None:
                break

        self.fermi_level = fl
        return

    def _sdos_line_to_orbitals_old(self, sorbs):
        import BZ
        evals = []
        iorb = 1
        kpts = self.kpts if hasattr(self, 'kpts') else [{'Rc': [0.0, 0.0, 0.0], 'Wgt': 1.0}]
        for i, kp in enumerate(kpts):
            ev = []
            for ispin, norb in enumerate(self.evals[0].info):
                for iorbk in range(norb):
                    ev.append({'e': sorbs[(iorb + iorbk)], 's': 1 - 2 * ispin, 'k': i + 1})

                iorb += norb

            evals.append(BZ.BandArray(ev, ikpt=i + 1, kpt=kp['Rc'], kwgt=kp['Wgt']))

        return evals

    def _sdos_line_to_orbitals(self, sorbs):
        import BZ, numpy as np
        evals = []
        iorb = 1
        sdos = [[], []]
        for ikpt, band in enumerate(self.evals):
            sdoskpt = [[], []]
            for ispin, norb in enumerate(band.info):
                if norb == 0:
                    continue
                bands = band[ispin]
                for i in range(norb):
                    val = sorbs[iorb]
                    e = bands[i]
                    iorb += 1
                    sdoskpt[ispin].append(val)

                sdos[ispin].append(np.array(sdoskpt[ispin]))

        return sdos

    def _get_bz(self, ev, kpts):
        """Get the Brillouin Zone."""
        evals = []
        import BZ
        for i, kp in enumerate(kpts):
            evals.append(BZ.BandArray(ev, ikpt=i + 1, kpt=kp['Rc'], kwgt=kp['Wgt']))

        return evals

    def get_dos(self, label=None, npts=2500):
        """
        Get the density of states from the logfile.

        :param label: id of the density of states.
        :type label: string
        :param npts: number of points of the DoS curve
        :type npts: int
        :returns: Instance of the DoS class
        :rtype: :class:`BigDFT.DoS.DoS`
        """
        import DoS
        lbl = self.label if label is None else label
        sdos = self.sdos if hasattr(self, 'sdos') else None
        return DoS.DoS(bandarrays=self.evals, label=lbl, units='AU', fermi_level=self.fermi_level, npts=npts, sdos=sdos)

    def get_brillouin_zone(self):
        """
        Return an instance of the BrillouinZone class, useful for band structure.
        :returns: Brillouin Zone of the logfile
        :rtype: :class:`BigDFT.BZ.BrillouinZone`
        """
        import BZ
        if self.nkpt == 1:
            print 'WARNING: Brillouin Zone plot cannot be defined properly with only one k-point'
        mesh = self.kpt_mesh
        if isinstance(mesh, int):
            mesh = [mesh] * 3
        if self.astruct['cell'][1] == float('inf'):
            mesh[1] = 1
        return BZ.BrillouinZone(self.astruct, mesh, self.evals, self.fermi_level)

    def wfn_plot(self):
        """
        Plot the wavefunction convergence.
        :Example:
           >>> tt=Logfile('log-with-wfn-optimization.yaml',label='a label')
           >>> tt.wfn_plot()
        """
        wfn_it = find_iterations(self.log)
        plot_wfn_convergence(wfn_it, self.gnrm_cv, label=self.label)

    def geopt_plot(self):
        """
        For a set of logfiles construct the convergence plot if available.
        Plot the Maximum value of the forces against the difference between the minimum value of the energy
        and the energy of the iteration. Also an errorbar is given indicating
        the noise on the forces for a given point.
        Show the plot as per plt.show() with matplotlib.pyplots as plt

        :Example:
           >>> tt=Logfile('log-with-geometry-optimization.yaml')
           >>> tt.geopt_plot()
        """
        import numpy
        energies = []
        forces = []
        ferr = []
        if not hasattr(self, '_instances'):
            print 'ERROR: No geopt plot possible, single point run'
            return
        for l in self._instances:
            if hasattr(l, 'forcemax') and hasattr(l, 'energy'):
                forces.append(l.forcemax)
                energies.append(l.energy - self.energy)
                ferr.append(0.0 if not hasattr(l, 'force_fluct') else (self.force_fluct if hasattr(self, 'force_fluct') else 0.0))

        if len(forces) > 1:
            import matplotlib.pyplot as plt
            plt.errorbar(energies, forces, yerr=ferr, fmt='.-', label=self.label)
            plt.legend(loc='upper right')
            plt.loglog()
            plt.xlabel('Energy - min(Energy)')
            plt.ylabel('Forcemax')
            if hasattr(self, 'forcemax_cv'):
                plt.axhline(self.forcemax_cv, color='k', linestyle='--')
            plt.show()
        else:
            print 'No plot necessary, less than two points found'

    def _print_information(self):
        """Display short information about the logfile (used by str)."""
        import yaml, numpy
        summary = [{'Atom types': self.log['Atomic System Properties']['Types of atoms']},
         {'cell': self.astruct.get('cell', 'Free BC')}]
        for field in BUILTIN:
            name = BUILTIN[field].get(PRINT)
            if name == True:
                name = field
            if not name or not hasattr(self, field):
                continue
            summary.append({name: getattr(self, field)})

        if hasattr(self, 'evals'):
            nspin = self.log['dft']['nspin']
            if nspin == 4:
                nspin = 1
            cmt = ' per k-point' if hasattr(self, 'kpts') else ''
            summary.append({'No. of KS orbitals' + cmt: self.evals[0].info[0:nspin]})
        return yaml.dump(summary, default_flow_style=False)


if __name__ == '__main__':
    l = Logfile()