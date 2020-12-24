# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/pg_sane.py
# Compiled at: 2018-06-03 16:45:05
# Size of source mod 2**32: 11884 bytes
"""plugin for PG_Sane algorithm,  used for NUS processing

It takes a NUS acquired transient, and fill it by estimating the missing values.

associated publications

- Lionel Chiron, Afef Cherni, Christian Rolando, Emilie Chouzenoux, Marc-André Delsuc
  Fast Analysis of Non Uniform Sampled DataSets in 2D-FT-ICR-MS. - in progress

- Bray, F., Bouclon, J., Chiron, L., Witt, M., Delsuc, M.-A., & Rolando, C. (2017).
  Nonuniform Sampling Acquisition of Two-Dimensional Fourier Transform Ion Cyclotron Resonance Mass Spectrometry for Increased Mass Resolution of Tandem Mass Spectrometry Precursor Ions.
  Anal. Chem., acs.analchem.7b01850. http://doi.org/10.1021/acs.analchem.7b01850

- Chiron, L., van Agthoven, M. A., Kieffer, B., Rolando, C., & Delsuc, M.-A. (2014).
  Efficient denoising algorithms for large experimental datasets and their applications in Fourier transform ion cyclotron resonance mass spectrometry.
  PNAS , 111(4), 1385–1390. http://doi.org/10.1073/pnas.1306700111

"""
from __future__ import print_function
import unittest, numpy as np
from numpy.fft import fft, ifft, rfft, irfft
from spike.NPKData import NPKData_plugin, as_cpx, as_float, _base_fft, _base_ifft, _base_rfft, _base_irfft
import spike.Algo.sane as sane
from spike.util.signal_tools import filtering
import sys
if sys.version_info[0] < 3:
    pass
else:
    xrange = range

def noise(data, iterations=10, tresh=3.0):
    """Simple noise evaluation """
    b = data.copy()
    for i in range(iterations):
        b = b[(b - b.mean() < tresh * b.std())]

    return b.std()


def HT(x, thresh):
    """
    returns the Hard Thresholding of x,
    i.e. all points such as x_i <= thresh are set to 0.0
    """
    ax = abs(x)
    tx = np.where(ax > thresh, x, 0.0)
    return tx


def HTproj(x, k):
    r"""
    returns the Hard Thresholding of x, on the ball of radius \ell_o = k
    i.e. the k largest values are kept, all other are set to 0
    """
    ax = abs(x)
    N = len(ax) - k
    tx = np.argpartition(ax, N)
    hpx = np.zeros_like(x)
    hpx[tx[N:]] = x[tx[N:]]
    return hpx


def pg_sane--- This code section failed: ---

 L.  95         0  LOAD_CLOSURE             'HTmode'
                2  LOAD_CLOSURE             'Lthresh'
                4  LOAD_CLOSURE             'Ndata'
                6  LOAD_CLOSURE             'directFT'
                8  LOAD_CLOSURE             'idirectFT'
               10  BUILD_TUPLE_5         5 
               12  LOAD_CODE                <code_object PG>
               14  LOAD_STR                 'pg_sane.<locals>.PG'
               16  MAKE_FUNCTION_8          'closure'
               18  STORE_FAST               'PG'

 L. 104        20  LOAD_FAST                'npkd'
               22  LOAD_ATTR                dim
               24  LOAD_CONST               1
               26  COMPARE_OP               ==
            28_30  POP_JUMP_IF_FALSE   492  'to 492'

 L. 105        32  LOAD_FAST                'sampling'
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    84  'to 84'

 L. 106        40  LOAD_FAST                'npkd'
               42  LOAD_ATTR                axis1
               44  LOAD_ATTR                sampled
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L. 107        48  LOAD_GLOBAL              Exception
               50  LOAD_STR                 'this function works only on NUS datasets'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L. 108        56  LOAD_FAST                'npkd'
               58  LOAD_METHOD              copy
               60  CALL_METHOD_0         0  '0 positional arguments'
               62  LOAD_METHOD              zf
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  LOAD_METHOD              get_buffer
               68  CALL_METHOD_0         0  '0 positional arguments'
               70  STORE_DEREF              'fiditer'

 L. 109        72  LOAD_FAST                'npkd'
               74  LOAD_ATTR                axis1
               76  LOAD_METHOD              get_sampling
               78  CALL_METHOD_0         0  '0 positional arguments'
               80  STORE_FAST               'lsampling'
               82  JUMP_FORWARD         96  'to 96'
             84_0  COME_FROM            38  '38'

 L. 111        84  LOAD_FAST                'npkd'
               86  LOAD_METHOD              get_buffer
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  STORE_DEREF              'fiditer'

 L. 112        92  LOAD_FAST                'sampling'
               94  STORE_FAST               'lsampling'
             96_0  COME_FROM            82  '82'

 L. 114        96  LOAD_DEREF               'fiditer'
               98  LOAD_FAST                'lsampling'
              100  BINARY_SUBSCR    
              102  STORE_FAST               'GoodOnes'

 L. 115       104  LOAD_GLOBAL              float
              106  LOAD_GLOBAL              len
              108  LOAD_FAST                'GoodOnes'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  LOAD_GLOBAL              len
              116  LOAD_DEREF               'fiditer'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  BINARY_TRUE_DIVIDE
              122  STORE_FAST               'RATIO'

 L. 116       124  LOAD_GLOBAL              np
              126  LOAD_ATTR                linalg
              128  LOAD_METHOD              norm
              130  LOAD_DEREF               'fiditer'
              132  CALL_METHOD_1         1  '1 positional argument'
              134  LOAD_GLOBAL              np
              136  LOAD_METHOD              sqrt
              138  LOAD_FAST                'RATIO'
              140  CALL_METHOD_1         1  '1 positional argument'
              142  BINARY_TRUE_DIVIDE
              144  STORE_FAST               'power'

 L. 117       146  LOAD_FAST                'size'
              148  LOAD_CONST               None
              150  COMPARE_OP               is-not
              152  POP_JUMP_IF_FALSE   210  'to 210'
              154  LOAD_FAST                'size'
              156  LOAD_GLOBAL              len
              158  LOAD_DEREF               'fiditer'
              160  CALL_FUNCTION_1       1  '1 positional argument'
              162  COMPARE_OP               >
              164  POP_JUMP_IF_FALSE   210  'to 210'

 L. 118       166  LOAD_GLOBAL              np
              168  LOAD_ATTR                zeros
              170  LOAD_FAST                'size'
              172  LOAD_DEREF               'fiditer'
              174  LOAD_ATTR                dtype
              176  LOAD_CONST               ('dtype',)
              178  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              180  STORE_FAST               'fidzf'

 L. 119       182  LOAD_DEREF               'fiditer'
              184  LOAD_CONST               None
              186  LOAD_CONST               None
              188  BUILD_SLICE_2         2 
              190  BINARY_SUBSCR    
              192  LOAD_FAST                'fidzf'
              194  LOAD_CONST               None
              196  LOAD_GLOBAL              len
              198  LOAD_DEREF               'fiditer'
              200  CALL_FUNCTION_1       1  '1 positional argument'
              202  BUILD_SLICE_2         2 
              204  STORE_SUBSCR     

 L. 120       206  LOAD_FAST                'fidzf'
              208  STORE_DEREF              'fiditer'
            210_0  COME_FROM           164  '164'
            210_1  COME_FROM           152  '152'

 L. 121       210  LOAD_FAST                'HTratio'
              212  LOAD_CONST               None
              214  COMPARE_OP               is
              216  POP_JUMP_IF_FALSE   232  'to 232'

 L. 122       218  LOAD_GLOBAL              len
              220  LOAD_DEREF               'fiditer'
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  LOAD_CONST               100
              226  BINARY_FLOOR_DIVIDE
              228  STORE_DEREF              'Ndata'
              230  JUMP_FORWARD        248  'to 248'
            232_0  COME_FROM           216  '216'

 L. 124       232  LOAD_GLOBAL              int
              234  LOAD_FAST                'HTratio'
              236  LOAD_GLOBAL              len
              238  LOAD_DEREF               'fiditer'
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  BINARY_MULTIPLY  
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  STORE_DEREF              'Ndata'
            248_0  COME_FROM           230  '230'

 L. 126       248  LOAD_DEREF               'fiditer'
              250  LOAD_ATTR                dtype
              252  LOAD_STR                 'complex128'
              254  COMPARE_OP               ==
              256  STORE_FAST               'cpx'

 L. 127       258  LOAD_FAST                'cpx'
          260_262  POP_JUMP_IF_FALSE   274  'to 274'

 L. 128       264  LOAD_GLOBAL              fft
              266  STORE_DEREF              'directFT'

 L. 129       268  LOAD_GLOBAL              ifft
              270  STORE_DEREF              'idirectFT'
              272  JUMP_FORWARD        290  'to 290'
            274_0  COME_FROM           260  '260'

 L. 131       274  LOAD_GLOBAL              rfft
              276  STORE_DEREF              'directFT'

 L. 132       278  LOAD_CLOSURE             'fiditer'
              280  BUILD_TUPLE_1         1 
              282  LOAD_LAMBDA              '<code_object <lambda>>'
              284  LOAD_STR                 'pg_sane.<locals>.<lambda>'
              286  MAKE_FUNCTION_8          'closure'
              288  STORE_DEREF              'idirectFT'
            290_0  COME_FROM           272  '272'

 L. 135       290  SETUP_LOOP          418  'to 418'
              292  LOAD_GLOBAL              range
              294  LOAD_FAST                'iterations'
              296  CALL_FUNCTION_1       1  '1 positional argument'
              298  GET_ITER         
            300_0  COME_FROM           396  '396'
            300_1  COME_FROM           374  '374'
              300  FOR_ITER            416  'to 416'
              302  STORE_FAST               'i'

 L. 136       304  LOAD_FAST                'GoodOnes'
              306  LOAD_DEREF               'fiditer'
              308  LOAD_FAST                'lsampling'
              310  STORE_SUBSCR     

 L. 137       312  LOAD_GLOBAL              sane
              314  LOAD_DEREF               'fiditer'
              316  LOAD_FAST                'rank'
              318  CALL_FUNCTION_2       2  '2 positional arguments'
              320  STORE_DEREF              'fiditer'

 L. 138       322  LOAD_FAST                'i'
              324  LOAD_CONST               0
              326  COMPARE_OP               ==
          328_330  POP_JUMP_IF_FALSE   352  'to 352'

 L. 139       332  LOAD_DEREF               'fiditer'
              334  LOAD_FAST                'power'
              336  LOAD_GLOBAL              np
              338  LOAD_ATTR                linalg
              340  LOAD_METHOD              norm
              342  LOAD_DEREF               'fiditer'
              344  CALL_METHOD_1         1  '1 positional argument'
              346  BINARY_TRUE_DIVIDE
              348  INPLACE_MULTIPLY 
              350  STORE_DEREF              'fiditer'
            352_0  COME_FROM           328  '328'

 L. 140       352  LOAD_FAST                'GoodOnes'
              354  LOAD_DEREF               'fiditer'
              356  LOAD_FAST                'lsampling'
              358  STORE_SUBSCR     

 L. 141       360  LOAD_FAST                'PG'
              362  LOAD_DEREF               'fiditer'
              364  CALL_FUNCTION_1       1  '1 positional argument'
              366  STORE_DEREF              'fiditer'

 L. 142       368  LOAD_FAST                'i'
              370  LOAD_CONST               0
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   300  'to 300'

 L. 143       378  LOAD_GLOBAL              np
              380  LOAD_ATTR                linalg
              382  LOAD_METHOD              norm
              384  LOAD_DEREF               'fiditer'
              386  CALL_METHOD_1         1  '1 positional argument'
              388  STORE_FAST               'fidnorm'

 L. 144       390  LOAD_FAST                'fidnorm'
              392  LOAD_CONST               0.0
              394  COMPARE_OP               >
          396_398  POP_JUMP_IF_FALSE   300  'to 300'

 L. 145       400  LOAD_DEREF               'fiditer'
              402  LOAD_FAST                'power'
              404  LOAD_FAST                'fidnorm'
              406  BINARY_TRUE_DIVIDE
              408  INPLACE_MULTIPLY 
              410  STORE_DEREF              'fiditer'
          412_414  JUMP_BACK           300  'to 300'
              416  POP_BLOCK        
            418_0  COME_FROM_LOOP      290  '290'

 L. 147       418  LOAD_FAST                'final'
              420  LOAD_STR                 'SANE'
              422  COMPARE_OP               ==
          424_426  POP_JUMP_IF_FALSE   440  'to 440'

 L. 148       428  LOAD_GLOBAL              sane
              430  LOAD_DEREF               'fiditer'
              432  LOAD_FAST                'rank'
              434  CALL_FUNCTION_2       2  '2 positional arguments'
              436  STORE_DEREF              'fiditer'
              438  JUMP_FORWARD        480  'to 480'
            440_0  COME_FROM           424  '424'

 L. 149       440  LOAD_FAST                'final'
              442  LOAD_STR                 'PG'
              444  COMPARE_OP               ==
          446_448  POP_JUMP_IF_FALSE   452  'to 452'

 L. 150       450  JUMP_FORWARD        480  'to 480'
            452_0  COME_FROM           446  '446'

 L. 151       452  LOAD_FAST                'final'
              454  LOAD_STR                 'Reinject'
              456  COMPARE_OP               ==
          458_460  POP_JUMP_IF_FALSE   472  'to 472'

 L. 152       462  LOAD_FAST                'GoodOnes'
              464  LOAD_DEREF               'fiditer'
              466  LOAD_FAST                'lsampling'
              468  STORE_SUBSCR     
              470  JUMP_FORWARD        480  'to 480'
            472_0  COME_FROM           458  '458'

 L. 154       472  LOAD_GLOBAL              Exception
              474  LOAD_STR                 'wrong mode for "final", choose "SANE", "PG", or "Reinject"'
              476  CALL_FUNCTION_1       1  '1 positional argument'
              478  RAISE_VARARGS_1       1  'exception instance'
            480_0  COME_FROM           470  '470'
            480_1  COME_FROM           450  '450'
            480_2  COME_FROM           438  '438'

 L. 156       480  LOAD_FAST                'npkd'
              482  LOAD_METHOD              set_buffer
              484  LOAD_DEREF               'fiditer'
              486  CALL_METHOD_1         1  '1 positional argument'
              488  POP_TOP          
              490  JUMP_FORWARD        682  'to 682'
            492_0  COME_FROM            28  '28'

 L. 157       492  LOAD_FAST                'npkd'
              494  LOAD_ATTR                dim
              496  LOAD_CONST               2
              498  COMPARE_OP               ==
          500_502  POP_JUMP_IF_FALSE   662  'to 662'

 L. 158       504  LOAD_FAST                'npkd'
              506  LOAD_METHOD              test_axis
              508  LOAD_FAST                'axis'
              510  CALL_METHOD_1         1  '1 positional argument'
              512  STORE_FAST               'todo'

 L. 159       514  LOAD_FAST                'todo'
              516  LOAD_CONST               2
              518  COMPARE_OP               ==
          520_522  POP_JUMP_IF_FALSE   588  'to 588'

 L. 160       524  SETUP_LOOP          660  'to 660'
              526  LOAD_GLOBAL              xrange
              528  LOAD_FAST                'npkd'
              530  LOAD_ATTR                size1
              532  CALL_FUNCTION_1       1  '1 positional argument'
              534  GET_ITER         
              536  FOR_ITER            584  'to 584'
              538  STORE_FAST               'i'

 L. 161       540  LOAD_FAST                'npkd'
              542  LOAD_METHOD              row
              544  LOAD_FAST                'i'
              546  CALL_METHOD_1         1  '1 positional argument'
              548  LOAD_ATTR                pg_sane
              550  LOAD_FAST                'rank'
              552  LOAD_FAST                'iterations'
              554  LOAD_DEREF               'Lthresh'
              556  LOAD_FAST                'sampling'
              558  LOAD_FAST                'final'
              560  LOAD_FAST                'size'
              562  LOAD_CONST               ('rank', 'iterations', 'Lthresh', 'sampling', 'final', 'size')
              564  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              566  STORE_FAST               'r'

 L. 162       568  LOAD_FAST                'npkd'
              570  LOAD_METHOD              set_row
              572  LOAD_FAST                'i'
              574  LOAD_FAST                'r'
              576  CALL_METHOD_2         2  '2 positional arguments'
              578  POP_TOP          
          580_582  JUMP_BACK           536  'to 536'
              584  POP_BLOCK        
              586  JUMP_FORWARD        660  'to 660'
            588_0  COME_FROM           520  '520'

 L. 163       588  LOAD_FAST                'todo'
              590  LOAD_CONST               1
              592  COMPARE_OP               ==
          594_596  POP_JUMP_IF_FALSE   682  'to 682'

 L. 164       598  SETUP_LOOP          682  'to 682'
              600  LOAD_GLOBAL              xrange
              602  LOAD_FAST                'npkd'
              604  LOAD_ATTR                size2
              606  CALL_FUNCTION_1       1  '1 positional argument'
              608  GET_ITER         
              610  FOR_ITER            658  'to 658'
              612  STORE_FAST               'i'

 L. 165       614  LOAD_FAST                'npkd'
              616  LOAD_METHOD              col
              618  LOAD_FAST                'i'
              620  CALL_METHOD_1         1  '1 positional argument'
              622  LOAD_ATTR                pg_sane
              624  LOAD_FAST                'rank'
              626  LOAD_FAST                'iterations'
              628  LOAD_DEREF               'Lthresh'
              630  LOAD_FAST                'sampling'
              632  LOAD_FAST                'final'
              634  LOAD_FAST                'size'
              636  LOAD_CONST               ('rank', 'iterations', 'Lthresh', 'sampling', 'final', 'size')
              638  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              640  STORE_FAST               'r'

 L. 166       642  LOAD_FAST                'npkd'
              644  LOAD_METHOD              set_col
              646  LOAD_FAST                'i'
              648  LOAD_FAST                'r'
              650  CALL_METHOD_2         2  '2 positional arguments'
              652  POP_TOP          
          654_656  JUMP_BACK           610  'to 610'
              658  POP_BLOCK        
            660_0  COME_FROM_LOOP      598  '598'
            660_1  COME_FROM           586  '586'
            660_2  COME_FROM_LOOP      524  '524'
              660  JUMP_FORWARD        682  'to 682'
            662_0  COME_FROM           500  '500'

 L. 167       662  LOAD_FAST                'npkd'
              664  LOAD_ATTR                dim
              666  LOAD_CONST               3
              668  COMPARE_OP               ==
          670_672  POP_JUMP_IF_FALSE   682  'to 682'

 L. 168       674  LOAD_GLOBAL              Exception
              676  LOAD_STR                 'not implemented yet'
              678  CALL_FUNCTION_1       1  '1 positional argument'
              680  RAISE_VARARGS_1       1  'exception instance'
            682_0  COME_FROM           670  '670'
            682_1  COME_FROM           660  '660'
            682_2  COME_FROM           594  '594'
            682_3  COME_FROM           490  '490'

 L. 169       682  LOAD_CONST               None
              684  LOAD_FAST                'npkd'
              686  LOAD_METHOD              axes
              688  LOAD_FAST                'axis'
              690  CALL_METHOD_1         1  '1 positional argument'
              692  STORE_ATTR               sampling

 L. 170       694  LOAD_FAST                'npkd'
              696  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 660_2


class sane_pgTests(unittest.TestCase):

    def test_NUS_sampling(self):
        """
        NUS example
        removing the sampling noise 
        """
        from ..Tests import filename, directory
        import spike.Display.testplot as testplot
        plt = testplot.plot()
        import spike.util.signal_tools as u
        import numpy.fft as fft
        from spike.Tests import filename
        import spike.NPKData as NPKData
        samplingfile = filename('Sampling_file.list')
        e = NPKData(dim=1)
        e.axis1.load_sampling(samplingfile)
        size = 20000
        signal = u.SIGNAL_NOISE(lenfid=size, nbpeaks=10, amplitude=100, noise=50, shift=7000)
        signal.fid
        echant = signal.fid[e.axis1.sampling]
        f = NPKData(buffer=echant)
        f.axis1.load_sampling(samplingfile)
        h = f.copy()
        h.pg_sane()
        pgdb = u.SNR_dB(signal.fid0, h.get_buffer())
        print('PG_SANE reconstruction is %.1fdB should be greater than 19dB' % pgdb)
        f.zf().fft().modulus().display(label='NUS : FFT with sampling noise')
        h.fft().modulus().display(label='NUS : processed with PG_SANE', new_fig=False, show=True)
        self.assertTrue(pgdb > 19.0)

    def test_NUS_sampling2(self):
        """
        NUS larger example
        removing the sampling noise 
        """
        import spike.NPKData as NPKData
        import spike.Display.testplot as testplot
        plt = testplot.plot()
        import time

        def build(tp):
            np.random.seed(123)
            freq = 300000.0 * np.random.rand(10)
            amp = range(1, 11)
            fid = np.zeros(N, dtype=complex)
            for a, nu in zip(amp, freq):
                fid += a * np.exp(-tp / tau) * np.exp(complex(0.0, 2.0) * np.pi * nu * tp)

            return fid

        def FT(v):
            """ Fourier transform, with a simple cosine-bell apodisation"""
            vapod = v * np.cos(np.linspace(0, np.pi / 2, len(v)))
            return np.fft.fftshift(np.fft.fft(vapod))

        def gene_sampling(ratio):
            np.random.seed(1234)
            perm = np.random.permutation(N - 1)
            sampling = sorted(perm[:int(round(N * ratio)) - 2])
            sampling.insert(0, 0)
            sampling.append(N - 1)
            return sampling

        def noise(data):
            """ estimate noise in the spectrum by iteratively removing all signals above 3 sigma """
            b = data.copy()
            for i in range(10):
                b = b[(b - b.mean() < 3 * b.std())]

            return b.std()

        N = 64000
        SR = 1000000.0
        tau = 0.1
        dt = 1 / SR
        tp = np.arange(0, N) * dt
        fq = np.linspace(0, SR, N)
        fid0 = build(tp)
        NOISE = 5
        np.random.seed(12345)
        nfid = fid0 + NOISE * np.random.randn(len(fid0)) + complex(0.0, 1.0) * NOISE * np.random.randn(len(fid0))
        RATIO = 0.125
        sampling = gene_sampling(RATIO)
        f = NPKData(buffer=(nfid[sampling]))
        f.axis1.sampling = sampling
        t0 = time.time()
        g = f.copy().pg_sane(iterations=20, rank=15)
        elaps = time.time() - t0
        SNR = -20 * np.log10(np.linalg.norm(g.get_buffer() - fid0) / np.linalg.norm(fid0))
        print('test_NUS_sampling2: elaps %.2f sec  SNR: %.1f dB should be larger than 30dB' % (elaps, SNR))
        self.assertTrue(SNR > 30.0)
        ax1 = plt.subplot(211)
        f.copy().apod_sin().zf(2).fft().display(title='spectrum original data with sampling noise', figure=ax1)
        ax2 = plt.subplot(212)
        g.copy().apod_sin().zf(2).fft().display(title='spectrum after pg_sane cleaning', figure=ax2)


NPKData_plugin('pg_sane', pg_sane)