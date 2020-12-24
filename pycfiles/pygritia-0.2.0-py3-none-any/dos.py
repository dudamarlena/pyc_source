# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/estructure/dos.py
# Compiled at: 2019-02-22 23:25:00
import os, h5py, glob, sys
from math import pi, sqrt
import numpy as np
try:
    from builtins import zip
except:
    pass

from pygrisb.basic import units
import matplotlib.pyplot as plt

class DOS:

    def __init__(self, w_k, e_skn, width=0.1, window=None, npts=201):
        """Electronic Density Of States object.

        width: float
          Width of guassian smearing.
        window: tuple of two float
          Use ``window=(emin, emax)``.  If not specified, a window
          big enough to hold all the eigenvalues will be used.
        npts: int
          Number of points.

        """
        self.npts = npts
        self.width = width
        self.w_k = w_k
        self.e_skn = e_skn
        if window is None:
            emin = self.e_skn.min() - 5 * self.width
            emax = self.e_skn.max() + 5 * self.width
        else:
            emin, emax = window
        self.energies = np.linspace(emin, emax, npts)
        return

    def delta(self, energy):
        """
        Return a delta-function centered at energy.
        """
        x = -((self.energies - energy) / self.width) ** 2
        return np.exp(x) / (sqrt(pi) * self.width)

    def get_energies(self):
        """"
        return energy mesh.
        """
        return self.energies

    def get_dos_component(self, psi_skn_w):
        """
        Get array of DOS values.
        """
        dos_list = []
        for e_kn, psi_kn_w in zip(self.e_skn, psi_skn_w):
            dos = np.zeros(self.npts, dtype=np.complex)
            for w, e_n, psi_n_w in zip(self.w_k, e_kn, psi_kn_w):
                for e, psi_w in zip(e_n, psi_n_w):
                    dos += w * self.delta(e) * psi_w

            dos_list.append(dos)

        return np.array(dos_list)

    def get_dos_t(self):
        """
        Get array of DOS values.
        """
        dos_list = []
        for e_kn in self.e_skn:
            dos = np.zeros(self.npts)
            for w, e_n in zip(self.w_k, e_kn):
                for e in e_n:
                    dos += w * self.delta(e)

            dos_list.append(dos)

        return np.array(dos_list)


def get_bands(coherentonly=False):
    """get band anergies and the correlated orbital characters.
    """
    with h5py.File('GPARAMBANDS.h5', 'r') as (f):
        nsym = f['/symnop'][0]
        nkp = f['/kptdim'][0]
        nbmax = f['/nbmax'][0]
        bnd_ne = []
        if '/NE_LIST_SPIN1' in f:
            bnd_ne.append(f['/NE_LIST_SPIN1'][()])
        elif '/NE_LIST' in f:
            bnd_ne.append(f['/NE_LIST'][()])
        else:
            bnd_ne.append([ [nbmax, 1, nbmax] for k in range(nkp) ])
        if '/NE_LIST_SPIN2' in f:
            bnd_ne.append(f['/NE_LIST_SPIN2'][()])
    with h5py.File('GLOG.h5', 'r') as (f):
        e_fermi = f['/e_fermi'][0]
        nspin = f['/nspin'][0]
        nasotot = f['/nasotot'][0]
        if coherentonly:
            rmat = f['/BND_R'][()].swapaxes(1, 2)
    if os.path.isfile('ginit.h5'):
        with h5py.File('ginit.h5', 'r') as (f):
            use_rydberg = 'ryd' in f['/usrqa/unit'][()]
    else:
        use_rydberg = False
    e_skn = np.zeros((nspin, nkp, nbmax), dtype=np.float)
    if not coherentonly:
        psi_sksna = np.zeros((nspin, nkp, nsym, nbmax, nasotot), dtype=np.complex)
    else:
        psi_sksna = np.zeros((nspin, nkp, nsym, nbmax, nbmax), dtype=np.complex)
    for fname in glob.glob('GBANDS_*h5'):
        with h5py.File(fname, 'r') as (f):
            for isp in range(nspin):
                for k in range(f['/IKP_START'][0] - 1, f['/IKP_END'][0]):
                    e_n = f[('/ISPIN_{}/IKP_{}/ek').format(isp + 1, k + 1)][...]
                    e_n = e_n - e_fermi
                    if use_rydberg:
                        e_n *= units.Ryd_eV
                    nbands = len(e_n)
                    e_skn[isp, k, :nbands] = e_n
                    e_skn[isp, k, nbands:] = 100.0
                    for isym in range(nsym):
                        if not coherentonly:
                            v = f[('/ISPIN_{}/IKP_{}/ISYM_{}/EVEC').format(isp + 1, k + 1, isym + 1)][:, :nasotot]
                            psi_sksna[isp, k, isym, bnd_ne[isp][(k, 1)] - 1:bnd_ne[isp][(k, 1)] + v.shape[0] - 1, :] = v
                        else:
                            v = f[('/ISPIN_{}/IKP_{}/ISYM_{}/EVEC').format(isp + 1, k + 1, isym + 1)][()].T
                            v[:nasotot, :] = rmat[isp].T.conj().dot(v[:nasotot, :])
                            psi_sksna[isp, k, isym, bnd_ne[isp][(k, 1)] - 1:bnd_ne[isp][(k, 1)] + v.shape[1] - 1, bnd_ne[isp][(k, 1)] - 1:bnd_ne[isp][(k, 1)] + v.shape[1] - 1] = v.T

    return (
     e_skn, psi_sksna)


def h5get_dos(ewin=(-3.0, 5.0), delta=0.05, npts=1001, coherentonly=False):
    """
    get total dos and the total correlated orbital component.
    """
    with h5py.File('GPARAMBANDS.h5', 'r') as (f):
        w_k = f['/kptwt'][...]
    with h5py.File('GLOG.h5', 'r') as (f):
        nasotot = f['/nasotot'][0]
    e_skn, psi_sksna = get_bands(coherentonly=coherentonly)
    dos = DOS(w_k, e_skn, width=delta, window=ewin, npts=npts)
    energies = dos.get_energies()
    if not coherentonly:
        dos_t = dos.get_dos_t()
    else:
        psi_skn_coh = np.einsum('...ijk,...ijk->...j', psi_sksna[..., :, :, :], psi_sksna.conj()[..., :, :, :]) / psi_sksna.shape[2]
        dos_t = dos.get_dos_component(psi_skn_coh)
    psi_skn_f = np.einsum('...ijk,...ijk->...j', psi_sksna[..., :, :, :nasotot], psi_sksna.conj()[..., :, :, :nasotot]) / psi_sksna.shape[2]
    dos_f = dos.get_dos_component(psi_skn_f)
    return (
     energies, dos_t, dos_f)


def plot_dos_tf(energies, dos_t, dos_f):
    """plot total dos and total correlated component
    and save in file `dos.pdf`.
    """
    fig, ax = plt.subplots()
    if len(dos_t) == 1:
        ax.fill_between(energies, 0, dos_t[0], facecolor='grey', alpha=0.5)
        ax.plot(energies, dos_t[0], color='grey', label='tot')
        ax.plot(energies, dos_f[0], color='red', label='$corr. orb.$')
        ax.set_ylim(0.0)
    else:
        ax.fill_between(energies, 0, dos_t[0], facecolor='grey', alpha=0.5)
        ax.fill_between(energies, 0, -dos_t[1], facecolor='grey', alpha=0.5)
        ax.plot(energies, dos_t[0], color='grey', label='tot-up')
        ax.plot(energies, -dos_t[1], color='grey', label='tot-dn')
        ax.plot(energies, dos_f[0], color='red', label='$corr-orb-up$')
        ax.plot(energies, -dos_f[1], color='blue', label='$corr-orb-dn$')
        ax.axhline(y=0, ls='-', color='black', linewidth=0.5)
    ax.set_xlim(np.min(energies), np.max(energies))
    ax.axvline(x=0, ls='--')
    ax.set_ylabel('DOS (states/f.u.)')
    ax.set_xlabel('E (eV)')
    plt.title('DOS with correlated orbital-component')
    plt.legend()
    fig.tight_layout()
    plt.show()
    fig.savefig('dos.pdf')


def driver_plot_dos():
    msg = '\n    Script to plot total density of states with\n    overall correlated orbital character.\n\n    inline options:\n\n        -el emin: set energy mesh minimuim\n        -eh emax: set energy mesh miaximum\n        -d delta: set Gaussian smearing factor\n        -n nmesh: set energy mesh size\n    '
    emin = -5.0
    emax = 5.0
    delta = 0.05
    npts = 1001
    if '-h' in sys.argv:
        print msg
        sys.exit()
    else:
        if '-el' in sys.argv:
            emin = float(sys.argv[(sys.argv.index('-el') + 1)])
        if '-eh' in sys.argv:
            emax = float(sys.argv[(sys.argv.index('-eh') + 1)])
        if '-d' in sys.argv:
            delta = float(sys.argv[(sys.argv.index('-d') + 1)])
        if '-n' in sys.argv:
            npts = int(sys.argv[(sys.argv.index('-n') + 1)])
        if '-ch' in sys.argv:
            coherentonly = True
        else:
            coherentonly = False
    energies, dos_t, dos_f = h5get_dos(ewin=(emin, emax), delta=delta, npts=npts, coherentonly=coherentonly)
    plot_dos_tf(energies, dos_t, dos_f)


if __name__ == '__main__':
    energies, dos_t, dos_f = h5get_dos(ewin=(-8.0, 5.0))
    plot_dos_tf(energies, dos_t, dos_f)