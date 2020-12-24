# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/voicing/percep_spec.py
# Compiled at: 2008-03-22 09:06:17
"""Perceptual spectrum for speech."""
import Num, math, erb_scale, gpkmisc
PLOT = True
if PLOT:
    try:
        import pylab
    except ImportError:
        pylab = None

else:
    pylab = None
import sys, os
sys.path.insert(0, os.environ['OXIVOICE'])
import voice_misc as VM, power
CBmax = erb_scale.f_to_erb(8000.0)
CBmin = erb_scale.f_to_erb(50.0)
BBSZ = 0.5
E = 0.333
Neural_Tick = 0.0001
DISS_BWF = 0.6
DISS_FREQ = 7.0

def SafeExp(x):
    return Num.exp(Num.maximum(-200.0, x))


def tau_lp(fc):
    """This is the cutoff frequency of the modulation transfer function
        in the ear, as a function of frequency.
        From R. Plomp and M. A. Bouman, JASA 31(6), page 749ff, June 1959
                'Relation of hearing threshold and duration of tone pulses'
                """
    Tau200 = 0.4
    Tau10k = 0.13
    tmp = Tau200 + math.log(fc / 200.0) / math.log(10000.0 / 200.0) * (Tau10k - Tau200)
    assert tmp > 0
    return tmp


def cochlear_filter(fofc):
    """Transfer function taken from "Improved Audio Coding Using a
        Psychoacoustic Model Based on a Cochlear Filter Bank
        IEEE Transactions of Speech and Audio Processing, 10(7) October 2002,
        Pages 495-503.  au=Frank Baumgarte.
        """
    Q = 4.0
    Slp = 25.0 / (20.0 * math.log10(1.2))
    Shp = 8.0 / (20.0 * math.log10(1.2))
    fofc_Shp = fofc ** Shp
    return fofc_Shp / ((1 + fofc ** Slp) * (1 + complex(0.0, 1.0) / Q * fofc ** (Shp / 2) - fofc_Shp))


def threshold(f):
    """IN pressure amplitude.
        Crudely taken from Handbook of Perception vol 4: hearing,
        E.C.Carterette and M.P.Friedman, editors,
        Academic Press 1978, isbn 0-12-161904-4.
        Curve near 70db used."""
    return math.sqrt((200.0 / f) ** 4 + 1 + (f / 8000.0) ** 16)


def accum_abs_sub(a, b, o):
    """This does a little computation in a block-wise fashion
        to keep all the data witin the processor's cache.
        It computes sum( abs(a-b) ).
        """
    BKS = 6000
    n = o.shape[0]
    assert a.shape == (n,)
    assert b.shape == (n,)
    assert o.shape == (n,)
    tmp = Num.zeros((BKS,), Num.Float)
    for i in range(0, n, BKS):
        e = min(i + BKS, n)
        tmpi = tmp[:e - i]
        ai = a[i:e]
        bi = b[i:e]
        oi = o[i:e]
        Num.subtract(ai, bi, tmpi)
        Num.absolute(tmpi, tmpi)
        Num.add(oi, tmpi, oi)

    return o


def list_accum_abs_sub_dly(tk, dly):
    lng = tk[0][dly:].shape[0]
    o = Num.zeros((lng,), Num.Float)
    for tkd in tk:
        a = tkd[:-dly]
        b = tkd[dly:]
        accum_abs_sub(a, b, o)

    return o


def process_voicing(tk, tick, Dt):
    LOWF = 50.0
    HIGHF = 400.0
    lowf = int(round(1.0 / (tick * LOWF)))
    highf = int(round(1.0 / (tick * HIGHF)))
    tmps = None
    tmpmin = None
    tmpn = 0
    for dly in range(highf, lowf):
        dhl = dly // 2
        dhr = dly - dhl
        dlytmp = list_accum_abs_sub_dly(tk, dly)
        assert len(dlytmp.shape) == 1
        al = Num.zeros((dhl,), Num.Float)
        ar = Num.zeros((dhr,), Num.Float)
        tmp1 = Num.concatenate((al, dlytmp, ar))
        (tmp2, t0) = power.smooth(tmp1, tick, Dt, extra=1.0 / (LOWF * math.sqrt(12.0)))
        if tmps is None:
            tmpn = 1
            tmps = tmp2
            tmpmin = Num.array(tmp2, copy=True)
        else:
            tmpn += 1
            Num.add(tmps, tmp2, tmps)
            Num.minimum(tmpmin, tmp2, tmpmin)

    avgmmin = tmps / tmpn - tmpmin
    assert Num.alltrue(Num.greater_equal(avgmmin, 0.0))
    return avgmmin


class dissonance_c(object):
    __module__ = __name__

    def __init__(self):
        self.y = None
        self.n = 0
        self.dt = None
        return

    def add(self, y, dt, diss_bw):
        if self.dt is None:
            assert dt > 0
            self.dt = dt
        else:
            assert abs(dt - self.dt) < 0.0001 * self.dt
        tmp = VM.lowpass_sym_butterworth(y, diss_bw * dt)
        tmp = VM.hipass_first_order(tmp, DISS_FREQ * dt)
        tmp = Num.absolute(tmp)
        if self.y is None:
            self.y = tmp
        else:
            Num.add(self.y, tmp, self.y)
        self.n += 1
        return

    def get(self, Dt):
        (yfilt, t0) = power.smooth(self.y, self.dt, Dt)
        return yfilt / self.n


def perceptual_spec(data, dt, DT, bmin=CBmin, bmax=CBmax, db=BBSZ, do_mod=False, do_dissonance=False, PlompBouman=True):
    """This returns something roughly like the neural signals leaving the ear.
        It filters into 1-erb-wide bins, then takes the cube root of
        the amplitude.
        @return: (channel_info, data, time_offset), where
                - C{time_offset} is the time of the the first output datum
                        relative to the time of the  first input sample.
                - C{channel_info}
                - C{data}
        """
    Neural_Time_Resolution = max(Neural_Tick, dt)
    m = data.shape[0]
    assert m * dt > DT, 'Tiny amount of data: %d*%g=%.2gs < DT=%2g' % (m, dt, m * dt, DT)
    ntau = int(round(m * dt / DT))
    d = VM.dataprep_flat_real(data, dt, DT)
    ss = Num.FFT.real_fft(d)
    f = Num.absolute(VM.real_fft_freq(ss.shape[0], d=dt))
    nbands = int(math.ceil((bmax - bmin) / db))
    if do_mod:
        nbands += 1
        tk = []
    if do_dissonance:
        nbands += 1
        diss = dissonance_c()
    neural = Num.zeros((nbands, ntau), Num.Float)
    bctrs = []
    t0x = []
    iband = 0
    b = bmin
    while b < bmax:
        fc = erb_scale.erb_to_f(b)
        xferfcn = cochlear_filter(f / fc)
        xferfcn[0] = xferfcn[0].real
        xferfcn[-1] = xferfcn[(-1)].real
        filtered_sig = Num.FFT.inverse_real_fft(ss * xferfcn)
        hair_cells = Num.maximum(filtered_sig / threshold(fc), 0.0) ** (2 * E)
        (pwrfilt, t0) = power.smooth(hair_cells, dt, DT)
        t0x.append(t0)
        if PlompBouman:
            pwrfilt = Num.maximum(VM.lopass_first_order(pwrfilt, DT / tau_lp(fc)), 0.0)
        else:
            pwrfilt = Num.maximum(pwrfilt, 0.0)
        neural[iband, :] = pwrfilt[:ntau]
        bctrs.append({'type': 'band', 'smooth': tau_lp(fc), 'fc': fc, 'erb': b, 'E': E, 'id': 'B%.1f' % b})
        if do_mod or do_dissonance:
            (tkfilt, t0) = power.smooth(hair_cells, dt, Neural_Time_Resolution)
        if do_dissonance:
            diss_bw = DISS_BWF * erb_scale.ebw(b)
            diss.add(tkfilt, Neural_Time_Resolution, diss_bw)
        if do_mod:
            tk.append(tkfilt)
        b += db
        iband += 1

    if do_mod:
        avgmmin = process_voicing(tk, Neural_Time_Resolution, DT)
        neural[iband, :] = avgmmin[:ntau] * 0.15
        bctrs.append({'type': 'haspitch', 'id': 'haspitch1', 'variant': 1, 'Fentropy': -math.log(len(tk))})
        iband += 1
        assert len(bctrs) == iband
    if do_dissonance:
        neural[iband, :] = diss.get(DT)[:ntau] * 20.0
        bctrs.append({'type': 'dissonance', 'id': 'dissonance1', 'variant': 1, 'Fentropy': -math.log(diss.n)})
        iband += 1
    assert iband == neural.shape[0]
    return (
     bctrs, neural, gpkmisc.median(t0x))


__version__ = '$Revision: 1.43 $'
__date__ = '$Date: 2007/03/07 23:54:40 $'
if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    else:
        import gpkimgclass
        fname = sys.argv[1]
        data = gpkimgclass.read(fname)
        DT = 0.01
        (bctrs, neural, t0) = perceptual_spec(data.column(0), data.dt(), DT, do_mod=True, do_dissonance=True)
        o = Num.transpose(neural)
        if PLOT and pylab:
            pylab.matshow(Num.transpose(o))
            pylab.show()
        hdr = {'CDELT2': DT, 'CRPIX2': 1, 'CRVAL2': data.start(), 'VERSION': __version__, 'BITPIX': 0, 'FNAME': fname, 'DataSamplingFreq': 1.0 / data.dt(), 'CRPIX1': 1, 'CRVAL1': bctrs[0]['erb'], 'CDELT1': bctrs[1]['erb'] - bctrs[0]['erb']}
        for (i, b) in enumerate(bctrs):
            hdr['TTYPE%d' % i] = b['id']

        gpkimgclass.gpk_img(hdr, o).write('-')