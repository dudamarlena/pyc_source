# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/sane.py
# Compiled at: 2019-01-16 17:19:05
# Size of source mod 2**32: 3997 bytes
"""plugin for Sane denoising

This plugin implements the SANE denoising algorithm, 
SANE is inspired from urQRd algorithm, but is improved in several points

- faster on vector length != 2**n
- much more efficient on weak signals
- requires less iterations and less overestimate of rank
- however, a non productive iteration is always performed,
  so processing time for I iterations of SANE should be compared
  with I+1 iterations of urQRd.

associated publications
- Bray, F., Bouclon, J., Chiron, L., Witt, M., Delsuc, M.-A., & Rolando, C. (2017).
  Nonuniform Sampling Acquisition of Two-Dimensional Fourier Transform Ion Cyclotron Resonance Mass Spectrometry for Increased Mass Resolution of Tandem Mass Spectrometry Precursor Ions.
  Analytical Chemistry, acs.analchem.7b01850. http://doi.org/10.1021/acs.analchem.7b01850

- Chiron, L., van Agthoven, M. A., Kieffer, B., Rolando, C., & Delsuc, M.-A. (2014).
  Efficient denoising algorithms for large experimental datasets and their applications in Fourier transform ion cyclotron resonance mass spectrometry.
  PNAS , 111(4), 1385–1390. http://doi.org/10.1073/pnas.1306700111
"""
from __future__ import print_function
import sys, unittest
from spike.NPKData import NPKData_plugin, as_cpx, as_float, _base_fft, _base_ifft, _base_rfft, _base_irfft
import spike.Algo.sane as sane
if sys.version_info[0] < 3:
    pass
else:
    xrange = range

def sane_plugin--- This code section failed: ---

 L.  61         0  LOAD_FAST                'npkd'
                2  LOAD_ATTR                dim
                4  LOAD_CONST               1
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE   120  'to 120'

 L.  62        10  LOAD_FAST                'npkd'
               12  LOAD_ATTR                axis1
               14  LOAD_ATTR                itype
               16  LOAD_CONST               0
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    42  'to 42'

 L.  63        22  LOAD_GLOBAL              as_cpx
               24  LOAD_GLOBAL              _base_ifft
               26  LOAD_GLOBAL              _base_rfft
               28  LOAD_FAST                'npkd'
               30  LOAD_ATTR                buffer
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  STORE_FAST               'buff'
               40  JUMP_FORWARD         50  'to 50'
             42_0  COME_FROM            20  '20'

 L.  65        42  LOAD_FAST                'npkd'
               44  LOAD_METHOD              get_buffer
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  STORE_FAST               'buff'
             50_0  COME_FROM            40  '40'

 L.  66        50  LOAD_GLOBAL              sane
               52  LOAD_FAST                'buff'
               54  LOAD_FAST                'rank'
               56  LOAD_FAST                'orda'
               58  LOAD_FAST                'trick'
               60  LOAD_FAST                'iterations'
               62  LOAD_CONST               ('orda', 'trick', 'iterations')
               64  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               66  STORE_FAST               'sane_result'

 L.  67        68  LOAD_FAST                'npkd'
               70  LOAD_ATTR                axis1
               72  LOAD_ATTR                itype
               74  LOAD_CONST               0
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   108  'to 108'

 L.  68        80  LOAD_GLOBAL              _base_irfft
               82  LOAD_GLOBAL              _base_fft
               84  LOAD_GLOBAL              as_float
               86  LOAD_FAST                'sane_result'
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  STORE_FAST               'buff'

 L.  69        96  LOAD_FAST                'npkd'
               98  LOAD_METHOD              set_buffer
              100  LOAD_FAST                'buff'
              102  CALL_METHOD_1         1  '1 positional argument'
              104  POP_TOP          
              106  JUMP_FORWARD        118  'to 118'
            108_0  COME_FROM            78  '78'

 L.  71       108  LOAD_GLOBAL              as_float
              110  LOAD_FAST                'sane_result'
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  LOAD_FAST                'npkd'
              116  STORE_ATTR               buffer
            118_0  COME_FROM           106  '106'
              118  JUMP_FORWARD        292  'to 292'
            120_0  COME_FROM             8  '8'

 L.  72       120  LOAD_FAST                'npkd'
              122  LOAD_ATTR                dim
              124  LOAD_CONST               2
              126  COMPARE_OP               ==
          128_130  POP_JUMP_IF_FALSE   272  'to 272'

 L.  73       132  LOAD_FAST                'npkd'
              134  LOAD_METHOD              test_axis
              136  LOAD_FAST                'axis'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  STORE_FAST               'todo'

 L.  74       142  LOAD_FAST                'todo'
              144  LOAD_CONST               2
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   206  'to 206'

 L.  75       150  SETUP_LOOP          270  'to 270'
              152  LOAD_GLOBAL              xrange
              154  LOAD_FAST                'npkd'
              156  LOAD_ATTR                size1
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  GET_ITER         
              162  FOR_ITER            202  'to 202'
              164  STORE_FAST               'i'

 L.  76       166  LOAD_FAST                'npkd'
              168  LOAD_METHOD              row
              170  LOAD_FAST                'i'
              172  CALL_METHOD_1         1  '1 positional argument'
              174  LOAD_ATTR                sane
              176  LOAD_FAST                'rank'
              178  LOAD_FAST                'orda'
              180  LOAD_FAST                'iterations'
              182  LOAD_CONST               ('rank', 'orda', 'iterations')
              184  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              186  STORE_FAST               'r'

 L.  77       188  LOAD_FAST                'npkd'
              190  LOAD_METHOD              set_row
              192  LOAD_FAST                'i'
              194  LOAD_FAST                'r'
              196  CALL_METHOD_2         2  '2 positional arguments'
              198  POP_TOP          
              200  JUMP_BACK           162  'to 162'
              202  POP_BLOCK        
              204  JUMP_FORWARD        270  'to 270'
            206_0  COME_FROM           148  '148'

 L.  78       206  LOAD_FAST                'todo'
              208  LOAD_CONST               1
              210  COMPARE_OP               ==
          212_214  POP_JUMP_IF_FALSE   292  'to 292'

 L.  79       216  SETUP_LOOP          292  'to 292'
              218  LOAD_GLOBAL              xrange
              220  LOAD_FAST                'npkd'
              222  LOAD_ATTR                size2
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  GET_ITER         
              228  FOR_ITER            268  'to 268'
              230  STORE_FAST               'i'

 L.  80       232  LOAD_FAST                'npkd'
              234  LOAD_METHOD              col
              236  LOAD_FAST                'i'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  LOAD_ATTR                sane
              242  LOAD_FAST                'rank'
              244  LOAD_FAST                'orda'
              246  LOAD_FAST                'iterations'
              248  LOAD_CONST               ('rank', 'orda', 'iterations')
              250  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              252  STORE_FAST               'r'

 L.  81       254  LOAD_FAST                'npkd'
              256  LOAD_METHOD              set_col
              258  LOAD_FAST                'i'
              260  LOAD_FAST                'r'
              262  CALL_METHOD_2         2  '2 positional arguments'
              264  POP_TOP          
              266  JUMP_BACK           228  'to 228'
              268  POP_BLOCK        
            270_0  COME_FROM_LOOP      216  '216'
            270_1  COME_FROM           204  '204'
            270_2  COME_FROM_LOOP      150  '150'
              270  JUMP_FORWARD        292  'to 292'
            272_0  COME_FROM           128  '128'

 L.  82       272  LOAD_FAST                'npkd'
              274  LOAD_ATTR                dim
              276  LOAD_CONST               3
              278  COMPARE_OP               ==
          280_282  POP_JUMP_IF_FALSE   292  'to 292'

 L.  83       284  LOAD_GLOBAL              Exception
              286  LOAD_STR                 'not implemented yet'
              288  CALL_FUNCTION_1       1  '1 positional argument'
              290  RAISE_VARARGS_1       1  'exception instance'
            292_0  COME_FROM           280  '280'
            292_1  COME_FROM           270  '270'
            292_2  COME_FROM           212  '212'
            292_3  COME_FROM           118  '118'

 L.  84       292  LOAD_FAST                'npkd'
              294  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 270_2


NPKData_plugin('sane', sane_plugin)