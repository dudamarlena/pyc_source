# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/estructure/bandstruct.py
# Compiled at: 2019-02-22 23:25:00
from __future__ import print_function
import h5py, numpy, sys, glob
try:
    from builtins import range
except:
    pass

from pygrisb.estructure.dos import get_bands
import matplotlib.pyplot as plt

def get_greek_label(kname):
    """return the possible greek label.
    """
    if kname.upper() in ('LAMBDA', 'GAMMA', 'DELTA', 'SIGMA', 'THETA', 'XI', 'PI',
                         'UPSILON', 'PHI', 'PSI', 'OMEGA'):
        return ('$\\{}{}$').format(kname[0].upper(), kname[1:].lower())
    else:
        return ('${}$').format(kname)


def get_k_info():
    """get the k distance list, special k-point label and position for
    the band structure plot.
    """
    with h5py.File('GPARAMBANDS.h5', 'r') as (f):
        kx = f['/kptx'][()]
        ky = f['/kpty'][()]
        kz = f['/kptz'][()]
        kn = f['/kptname'][()]
        br = f['/recip_prim_vec'][()]
    ktick_pos = []
    ktick_label = []
    for i in range(len(kn)):
        if i == 0:
            klist = [
             0.0]
        else:
            dk = numpy.array([kx[i] - kx[(i - 1)], ky[i] - ky[(i - 1)], kz[i] - kz[(i - 1)]])
            dl = dk.dot(br).dot(br.T).dot(dk)
            klist.append(klist[(i - 1)] + numpy.sqrt(dl))
        klabel = kn[i].strip()
        if klabel != '':
            ktick_pos.append(klist[i])
            ktick_label.append(get_greek_label(klabel))

    return (
     klist, ktick_pos, ktick_label)


def get_estimated_gap(nocc=None):
    """Given the number of occupied bands and the band energy file,
    estimate the band gap.
    """
    evmax = -10000000000.0
    ecmin = 10000000000.0
    if nocc is None:
        with h5py.File('GLOG.h5') as (f):
            e_fermi = f['/e_fermi'][0]
    for fband in glob.glob('GBANDS_*.h5'):
        with h5py.File(fband, 'r') as (f):
            for ik in range(f['/IKP_START'][()], f['/IKP_END'][()] + 1):
                ek = f[('/ISPIN_1/IKP_{}/ek').format(ik)][()]
                if nocc is None:
                    noccp = numpy.argwhere(ek < e_fermi)[(-1)] + 1
                    nocc = noccp[0]
                    print((' number of occupied bands = {}').format(nocc))
                evmax = max(ek[(nocc - 1)], evmax)
                ecmin = min(ek[nocc], ecmin)

    return max(ecmin - evmax, 0.0)


def get_estimated_gaps(nocc=None):
    """Given the number of occupied bands and the band energy file,
    estimate the direct/indirect band gap with associated k-index.
    """
    evmax = -10000000000.0
    kvmax = -1
    ecmin = 10000000000.0
    kcmin = -1
    dgap = 1000.0
    kdgap = -1
    if nocc is None:
        with h5py.File('GLOG.h5') as (f):
            e_fermi = f['/e_fermi'][0]
    for fband in glob.glob('GBANDS_*.h5'):
        with h5py.File(fband, 'r') as (f):
            for ik in range(f['/IKP_START'][()], f['/IKP_END'][()] + 1):
                ek = f[('/ISPIN_1/IKP_{}/ek').format(ik)][()]
                if nocc is None:
                    noccp = numpy.argwhere(ek < e_fermi)[(-1)] + 1
                    nocc = noccp[0]
                    print((' number of occupied bands = {}').format(nocc))
                if ek[(nocc - 1)] > evmax:
                    evmax = ek[(nocc - 1)]
                    kvmax = ik - 1
                if ek[nocc] < ecmin:
                    ecmin = ek[nocc]
                    kcmin = ik - 1
                if ek[nocc] - ek[(nocc - 1)] < dgap:
                    dgap = ek[nocc] - ek[(nocc - 1)]
                    kdgap = ik - 1

    idgap = max(ecmin - evmax, 0.0)
    return (idgap, kvmax, kcmin, dgap, kdgap)


def driver_get_estimated_gaps():
    """script to print estimated direct/indirect band gaps.
    """
    msg = '\n    Script to print estimated direct/indirect band gaps.\n\n    inline options:\n\n        -n n: occupied number of bands.\n    '
    nocc = None
    if '-h' in sys.argv:
        print(msg)
        sys.exit()
    if '-n' in sys.argv:
        nocc = int(sys.argv[(sys.argv.index('-n') + 1)])
    with h5py.File('GPARAMBANDS.h5', 'r') as (f):
        kname = f['/kptname'][()]
    idgap, kvmax, kcmin, dgap, kdgap = get_estimated_gaps(nocc=nocc)
    print((' Direct gap = {} with k = {} {}').format(dgap, kdgap, kname[kdgap]))
    print((' Inirect gap = {} with kv = {} {} kc = {} {}').format(idgap, kvmax, kname[kvmax], kcmin, kname[kcmin]))
    return


def plot_band_sturture(emin=-10.0, emax=10.0):
    """plot band structure with overall correlated orbital character
    in the assigned energy window [emin, emax] in the file `bands.pdf`.
    """
    klist, ktick_pos, ktick_label = get_k_info()
    e_skn, psi_sksna = get_bands()
    psi_skn_f = numpy.einsum('...ijk,...ijk->...j', psi_sksna[..., :, :, :], psi_sksna.conj()[..., :, :, :]) / psi_sksna.shape[2].real
    psi_skn_f *= 20.0
    fig, ax = plt.subplots()
    for n in range(e_skn.shape[2]):
        ax.plot(klist, e_skn[0, :, n], 'k-')
        ax.scatter(klist, e_skn[0, :, n], s=psi_skn_f[0, :, n], c='r', edgecolors='r')

    if len(e_skn) == 2:
        for n in range(e_skn.shape[2]):
            ax.plot(klist, e_skn[1, :, n], 'k--')
            ax.scatter(klist, e_skn[1, :, n], s=psi_skn_f[1, :, n], c='b', edgecolors='b')

    ax.axhline(y=0, ls=':', lw=2)
    for x1 in ktick_pos[1:-1]:
        ax.axvline(x=x1, ls='--')

    ax.set_xticks(ktick_pos)
    ax.set_xticklabels(ktick_label)
    ax.set_ylabel('E (eV)')
    ax.set_xlim(klist[0], klist[(-1)])
    ax.set_ylim(emin, emax)
    plt.title('Band structure with corr-orb-character')
    plt.show()
    fig.savefig('bands.pdf')


def driver_plot_bands():
    msg = '\n    Script to plot band structure with\n    overall correlated orbital character.\n\n    inline options:\n\n        -el emin: set energy mesh minimuim\n        -eh emax: set energy mesh miaximum\n    '
    emin = -3.3
    emax = 5.8
    if '-h' in sys.argv:
        print(msg)
        sys.exit()
    else:
        if '-el' in sys.argv:
            emin = float(sys.argv[(sys.argv.index('-el') + 1)])
        if '-eh' in sys.argv:
            emax = float(sys.argv[(sys.argv.index('-eh') + 1)])
    plot_band_sturture(emin=emin, emax=emax)


if __name__ == '__main__':
    plot_band_sturture(emin=-3.3, emax=5.8)