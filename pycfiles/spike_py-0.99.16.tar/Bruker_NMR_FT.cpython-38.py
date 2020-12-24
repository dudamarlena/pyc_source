# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/Bruker_NMR_FT.py
# Compiled at: 2020-01-30 08:36:55
# Size of source mod 2**32: 9221 bytes
"""This plugin implement the set of Fourier Transform used for NMR

and some other related utilities
commands starting with bk_ emulates (kind of) the topspin commands

MAD September 2015

"""
from __future__ import print_function
import unittest
from spike import NPKError
from spike.NPKData import NPKData_plugin, as_float, as_cpx
import sys
if sys.version_info[0] < 3:
    pass
else:
    xrange = range

def check_real(data, axis):
    if data.axes(axis).itype != 0:
        raise NPKError(('Axis %d should be real' % axis), data=data)


def check_cpx(data, axis):
    if data.axes(axis).itype != 1:
        raise NPKError(('Axis %d should be complex' % axis), data=data)


def ft_sim(data):
    """performs the fourier transform of a data-set acquired on a Bruker in
    simultaneous mode
    Processing is performed only along the F2 (F3) axis if in 2D (3D)

    (Bruker QSIM mode)"""
    todo = data.dim
    data.revf().fft(axis=todo)
    return data


NPKData_plugin('ft_sim', ft_sim)

def ft_seq(data):
    """performs the fourier transform of a data-set acquired on a Bruker in simultaneous mode
    Processing is performed only along the F2 (F3) axis if in 2D (3D)

    (Bruker QSIM mode)"""
    todo = data.dim
    data.revf().rfft(axis=todo)
    return data


NPKData_plugin('ft_seq', ft_seq)

def ft_tppi(data, axis='F1'):
    """TPPI F1 Fourier transform"""
    if data.dim == 1:
        raise NPKError('Not implemented in 1D', data=data)
    todo = data.test_axis(axis)
    data.revf(axis=todo).rfft(axis=todo)
    return data


NPKData_plugin('ft_tppi', ft_tppi)

def ft_sh(data, axis='F1'):
    """ States-Haberkorn F1 Fourier transform"""
    if data.dim == 1:
        raise NPKError('Not implemented in 1D', data=data)
    todo = data.test_axis(axis)
    data.revf(axis=todo).fft(axis=todo)
    return data


NPKData_plugin('ft_sh', ft_sh)

def ft_sh_tppi(data, axis='F1'):
    """ States-Haberkorn / TPPI F1 Fourier Transform """
    if data.dim == 1:
        raise NPKError('Not implemented in 1D', data=data)
    todo = data.test_axis(axis)
    data.fft(axis=todo)
    return data


NPKData_plugin('ft_sh_tppi', ft_sh_tppi)

def ft_phase_modu(data, axis='F1'):
    """F1-Fourier transform for phase-modulated 2D"""
    if data.dim != 2:
        raise NPKError('implemented only in 2D', data=data)
    data.flip().revf('F1').fft('F1').flop().reverse('F1')
    return data


NPKData_plugin('ft_phase_modu', ft_phase_modu)

def ft_n_p(data, axis='F1'):
    """F1-Fourier transform for N+P (echo/antiecho) 2D"""
    data.conv_n_p().ft_sh()
    return data


NPKData_plugin('ft_n_p', ft_n_p)

def bruker_corr(self):
    """
    applies a correction on the spectrum for the time offset in the FID.
    time offset is stored in the axis property zerotime
    """
    delay = self.axes(self.dim).zerotime
    self.phase(0, (-360.0 * delay), axis=0)
    return self


NPKData_plugin('bruker_corr', bruker_corr)
NPKData_plugin('bk_corr', bruker_corr)

def bruker_proc_phase(self):
    """
    applies a correction on the spectrum for the time offset in the FID and from proc file parameters.
    """
    ph1 = -float(self.params['proc']['$PHC1'])
    ph0 = -float(self.params['proc']['$PHC0']) + ph1 / 2
    zero = -360 * self.axes(self.dim).zerotime
    self.phase(ph0, ph1 + zero)
    self.axis1.P0 = ph0
    self.axis1.P1 = ph1
    return self


NPKData_plugin('bruker_proc_phase', bruker_proc_phase)
NPKData_plugin('bk_xf2p', bruker_proc_phase)
NPKData_plugin('bk_pk', bruker_proc_phase)

def conv_n_p(self):
    """
    realises the n+p to SH conversion
    """
    self.check2D()
    for k in xrange(0, self.size1, 2):
        a = self.row(k)
        b = self.row(k + 1)
        self.set_row(k, a.copy().add(b))
        a.buffer += -b.buffer
        a.buffer = as_float(complex(0.0, 1.0) * as_cpx(a.buffer))
        self.set_row(k + 1, a)
    else:
        self.axis1.itype = 1
        return self


NPKData_plugin('conv_n_p', conv_n_p)

def wdw(data, axis=1):
    """emulates Bruker window function"""

    def _sine(ssb):
        """computes maxi for sine(ssb)"""
        if ssb == '0':
            return 0.5
        if ssb == '2':
            return 0.0
        if ssb == '3':
            return 0.25
        if ssb == '4':
            return 0.333
        if ssb == '5':
            return 0.375
        if ssb == '6':
            return 0.4
        return 0.5

    def _wdw(data, pp, axis):
        if pp['$WDW'] == '0':
            pass
        elif pp['$WDW'] == '1':
            data.apod_em((float(pp['$LB'])), axis=axis)
        else:
            if pp['$WDW'] == '2':
                data.apod_gm((float(pp['$GB'])), axis=axis)
            else:
                if pp['$WDW'] == '3':
                    data.apod_sin((_sine(pp['$SSB'])), axis=axis)
                else:
                    if pp['$WDW'] == '4':
                        data.apod_sq_sin((_sine(pp['$SSB'])), axis=axis)
                    else:
                        if pp['$WDW'] == '5':
                            data.apod_tm((int(pp['$TM1'])), (int(pp['$TM2'])), axis=axis)
                        else:
                            raise Exception('WDW not implemented')
        return data

    if data.dim == 1:
        data = _wdw(data, data.params['proc'], 1)
    else:
        if data.dim == 2:
            if axis == 2:
                data = _wdw(data, data.params['proc'], 2)
            else:
                data = _wdw(data, data.params['proc2'], 1)
    return data


NPKData_plugin('bk_wdw', wdw)

def ftF2(data):
    """emulates Bruker ft of a 2D in F1 depending on FnMode"""
    if data.dim != 2:
        NPKError('Command available in 2D only', data=data)
    elif data.axis2.itype == 1:
        data.ft_sim()
    else:
        data.ft_seq()
    return data


NPKData_plugin('bk_ftF2', ftF2)

def ftF1(data):
    """emulates Bruker ft of a 2D in F1 depending on FnMode
    
    None    0
    QF      1
    QSEQ    2
    TPPI    3
    States  4
    States-TPPI 5
    Echo-AntiEcho   6
    """
    typ = data.params['acqu2']['$FnMODE']
    if typ == '0':
        pass
    elif typ == '1':
        data.ft_phase_modu()
    else:
        if typ == '2':
            data.rfft()
        else:
            if typ == '3':
                data.ft_tppi()
            else:
                if typ == '4':
                    data.ft_sh()
                else:
                    if typ == '5':
                        data.ft_sh_tppi()
                    else:
                        if typ == '6':
                            data.ft_n_p()
    if data.params['proc2']['$REVERSE'] == 'yes':
        data.reverse(axis='F1')
    return data


NPKData_plugin('bk_ftF1', ftF1)

def xf2(data):
    """emulates xf2 command from topspin"""
    data.bk_wdw(axis=2).bk_ftF2()
    return data


NPKData_plugin('bk_xf2', xf2)

def xf1(data):
    """emulates xf1 command from topspin"""
    data.bk_wdw(axis=1).bk_ftF1()
    return data


NPKData_plugin('bk_xf1', xf1)

def xfb(data):
    """emulates xfb command from topspin"""
    return data.bk_xf2().bk_xf1()


NPKData_plugin('bk_xfb', xfb)

class Bruker_NMR_FT(unittest.TestCase):

    def test_1D(self):
        """Test mostly syntax"""
        from ..NMR import NMRData
        d1 = NMRData(dim=1)
        d1.axis1.itype = 0
        d1.ft_seq()
        d1.axis1.itype = 1
        d1.ft_sim().bruker_corr()

    def test_2D(self):
        """Test mostly syntax"""
        from ..NMR import NMRData
        d1 = NMRData(dim=2)
        d1.axis2.itype = 0
        d1.ft_seq()
        d1.axis2.itype = 1
        d1.ft_sim()
        d1.axis1.itype = 0
        d1.ft_tppi()
        d1.axis1.itype = 1
        d1.ft_sh()
        d1.axis1.itype = 1
        d1.ft_sh_tppi()
        d1.axis1.itype = 1
        d1.ft_n_p()
        d1.axis2.itype = 1
        d1.axis1.itype = 0
        d1.ft_phase_modu()