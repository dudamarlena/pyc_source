# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ad254919/aiida_plugin/aiida-bigdft/aiida_bigdft/PyBigDFT/BigDFT/BZ.py
# Compiled at: 2019-07-30 07:30:05
import numpy
from futile.Utils import write as safe_print

def get_ev(ev, keys=None, ikpt=1):
    """Get the correct list of the energies for this eigenvalue."""
    res = False
    if keys is None:
        ener = ev.get('e')
        spin = ev.get('s')
        kpt = ev.get('k')
        if not kpt and ikpt == 1:
            kpt = True
        elif kpt and kpt != ikpt:
            kpt = False
        if ener and (spin == 1 or not spin):
            if kpt:
                res = [ener]
        elif ener and spin == -1:
            if kpt:
                res = [None, ener]
    else:
        for k in keys:
            if k in ev:
                res = ev[k]
                if type(res) != type([]):
                    res = [res]
                break

    return res


def astruct_to_cell(astruct):
    """ 
    Convert the astruct information as parsed from the module Logfiles into 
    the cell structure as needed from spglib    
    """
    import spglib, numpy
    celltmp = [ a if a != float('inf') else 1.0 for a in astruct['cell'] ]
    lattice = numpy.diag(celltmp)
    pos = [ [ a / b if b != float('inf') else 0.0 for a, b in zip(at.values()[0], celltmp) ] for at in astruct['positions'] ]
    atoms = [ at.keys()[0] for at in astruct['positions'] ]
    ianames, iatype = numpy.unique(atoms, return_inverse=True)
    return (lattice, pos, iatype)


class BandArray(numpy.ndarray):
    """Defines the array of data for one band. It is a dictionary which contains a numpy array for both spin channels."""

    def __new__(cls, *args, **kwargs):
        """Takes the data from the logfile and convert it"""
        datain = kwargs.get('data', None)
        if datain is not None:
            evs = datain
            shape0 = len(evs)
            norbs = map(len, evs)
            if len(norbs) == 1:
                norbs = [norbs[0], 0]
        else:
            evs = [[], []]
            logdata = kwargs.get('logdata', args[0])
            ikpt = kwargs.get('ikpt', 1 if len(args) < 2 else args[1])
            prev_vrt = True
            cur_ikpt = 0
            for ev in logdata:
                occ = get_ev(ev, ['e_occ', 'e_occupied'], ikpt=ikpt)
                vrt = get_ev(ev, ['e_vrt', 'e_virt'], ikpt=ikpt)
                eigen = occ or vrt
                if occ and prev_vrt:
                    cur_ikpt += 1
                prev_vrt = vrt
                if eigen and cur_ikpt != ikpt:
                    continue
                if not eigen:
                    eigen = get_ev(ev, ikpt=ikpt)
                if not eigen:
                    continue
                for i, e in enumerate(eigen):
                    if e:
                        evs[i].append(e)

            shape0 = 2 if len(evs[1]) > 0 else 1
            norbs = map(len, evs)
        data = numpy.ndarray.__new__(cls, shape=(shape0, max(norbs)), dtype=numpy.float)
        data.fill(numpy.nan)
        data[0, :len(evs[0])] = evs[0]
        if norbs[1] > 0:
            data[1, :len(evs[1])] = evs[1]
        data.info = norbs
        return data

    def __init__(self, *args, **kwargs):
        ikpt = kwargs.get('ikpt', 1 if len(args) < 2 else args[1])
        kpt = kwargs.get('kpt', (0.0, 0.0, 0.0) if len(args) < 3 else args[2])
        kwgt = kwargs.get('kwgt', 1.0)
        self.set_kpt(ikpt, kpt, kwgt)

    def set_kpt(self, ikpt, kpt, kwgt=1.0):
        if not isinstance(ikpt, int):
            raise TypeError('ikpt should be a integer')
        if len(kpt) != 3:
            raise TypeError('kpt should be a object of len 3')
        self.ikpt = ikpt
        self.kpt = kpt
        self.kwgt = kwgt

    def __add__(self, b):
        if hasattr(b, 'kpt') and b.kpt != self.kpt:
            raise ValueError('cannot sum BandArray with different kpoints')
        if hasattr(b, 'kwgt') and b.kwgt != self.kwgt:
            raise ValueError('cannot sum BandArray with different kweights')
        c = super(type(self), self).__add__(b)
        return BandArray(data=c, ikpt=self.ikpt, kpt=self.kpt, kwgt=self.kwgt)


class BZPath:
    """Defines a set of points which are associated to a path in the reduced Brillouin Zone."""

    def __init__(self, lattice, path, special_points, npts=50):
        import ase.dft.kpoints
        self.special_points = special_points
        path_tmp = []
        self.symbols = []
        for p in path:
            if isinstance(p, str):
                path_tmp.append(self.special_points[p])
                self.symbols.append(p.replace('G', '$\\Gamma$'))
            else:
                path_tmp.append(p.values()[0])
                self.symbols.append(p.keys()[0])

        self.path, self.xaxis, self.xlabel = ase.get_bandpath(path_tmp, lattice, npts)


class BrillouinZone:

    def __init__(self, astruct, mesh, evals, fermi_energy):
        import spglib, numpy
        cell = astruct_to_cell(astruct)
        self.lattice = cell[0]
        safe_print('spacegroup', spglib.get_spacegroup(cell, symprec=1e-05))
        import ase.dft.kpoints
        cell_tmp = astruct['cell']
        if numpy.allclose(cell_tmp, [cell_tmp[0]] * len(cell_tmp)):
            lattice_string = 'cubic'
        else:
            lattice_string = 'orthorhombic'
        safe_print('Lattice found:', lattice_string)
        self.special_points = ase.get_special_points(lattice_string, self.lattice, eps=0.0001)
        self.special_paths = ase.parse_path_string(ase.special_paths[lattice_string])
        self.fermi_energy = fermi_energy
        mapping, grid = spglib.get_ir_reciprocal_mesh(mesh, cell, is_shift=[0, 0, 0])
        lookup = []
        for ikpt in numpy.unique(mapping):
            ltmp = []
            for ind, (m, g) in enumerate(zip(mapping, grid)):
                if m == ikpt:
                    ltmp.append((g, ind))

            lookup.append(ltmp)

        safe_print('irreductible k-points', len(lookup))
        coords = numpy.array(grid, dtype=numpy.float) / mesh
        kp = numpy.array([ k.kpt for k in evals ])
        ourkpt = numpy.rint(kp * numpy.array(mesh)).astype(int)
        bz = numpy.ndarray((coords.shape[0], evals[0].size), dtype=float)
        shift = (numpy.array(mesh) - 1) / 2
        for ik in lookup:
            irrk = None
            for orbs, bzk in zip(evals, ourkpt):
                for kt, ind in ik:
                    if (bzk == kt).all():
                        irrk = orbs
                        break

                if irrk is not None:
                    break

            if irrk is None:
                safe_print('error in ik', ik)
                safe_print('our', ourkpt)
                safe_print('spglib', grid)
                safe_print('mapping', mapping)
            for kt, ind in ik:
                bz[ind, :] = irrk.reshape(irrk.size)

        bztmp = bz
        ndup = 7
        duplicates = [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1]]
        bztot = numpy.ndarray((ndup, bztmp.shape[0], bztmp.shape[1]))
        bztot[0, :, :] = bztmp
        ctot = numpy.ndarray((ndup, coords.shape[0], coords.shape[1]))
        ctot[0, :, :] = coords
        for i, sh in enumerate(duplicates):
            bztot[i + 1, :, :] = bztmp
            ctot[i + 1, :, :] = coords + sh

        bztot = bztot.reshape((ndup * bztmp.shape[0], -1))
        ctot = ctot.reshape((ndup * coords.shape[0], -1))
        import scipy.interpolate.interpnd as interpnd
        self.interpolator = interpnd.LinearNDInterpolator(ctot, bztot)
        sanity = 0.0
        for kpt in evals:
            diff = numpy.ravel(numpy.ravel(kpt) - numpy.ravel(self.interpolator([kpt.kpt])))
            sanity = max(sanity, numpy.dot(diff, diff))

        print (
         'Interpolation bias', sanity)
        return

    def plot(self, path=None, npts=50):
        if path is None:
            ppath = BZPath(self.lattice, self.special_paths[0], self.special_points, npts)
        else:
            ppath = path
        toto = self.interpolator(ppath.path)
        import matplotlib.pyplot as plt
        for b in toto.transpose():
            plt.plot(ppath.xaxis, b)

        plt.axhline(self.fermi_energy, color='k', linestyle='--')
        for p in ppath.xlabel:
            plt.axvline(p, color='k', linestyle='-')
            plt.xticks(ppath.xlabel, ppath.symbols)

        plt.show()
        return