# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/optimalgrouping/optimalgrouping.py
# Compiled at: 2020-03-04 12:59:13
# Size of source mod 2**32: 19386 bytes
from __future__ import print_function
import os
import astropy.io.fits as pf
import numpy as np, subprocess
try:
    import commands
except:
    pass

def run(cmd, verbose=True):
    print
    print('------------------------------------------------------------------------------------------------')
    print('running ', cmd)
    try:
        out = subprocess.getstatusoutput(cmd)
    except:
        out = commands.getstatusoutput(cmd)

    if verbose == True:
        print(out[1])
    print('------------------------------------------------------------------------------------------------')
    print


def get_resolution_array--- This code section failed: ---

 L.  37         0  LOAD_CONST               -1
                2  STORE_FAST               'ind_matrix'

 L.  38         4  LOAD_CONST               -1
                6  STORE_FAST               'ind_ebounds'

 L.  40         8  LOAD_GLOBAL              pf
               10  LOAD_METHOD              open
               12  LOAD_FAST                'rmf'
               14  CALL_METHOD_1         1  '1 positional argument'
               16  STORE_FAST               'pf_buffer'

 L.  43        18  SETUP_LOOP          144  'to 144'
               20  LOAD_GLOBAL              range
               22  LOAD_CONST               1
               24  LOAD_GLOBAL              len
               26  LOAD_FAST                'pf_buffer'
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  CALL_FUNCTION_2       2  '2 positional arguments'
               32  GET_ITER         
             34_0  COME_FROM           126  '126'
               34  FOR_ITER            142  'to 142'
               36  STORE_FAST               'i'

 L.  44        38  LOAD_FAST                'pf_buffer'
               40  LOAD_FAST                'i'
               42  BINARY_SUBSCR    
               44  LOAD_ATTR                header
               46  LOAD_STR                 'EXTNAME'
               48  BINARY_SUBSCR    
               50  STORE_FAST               'extname'

 L.  45        52  LOAD_GLOBAL              print
               54  LOAD_FAST                'extname'
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  POP_TOP          

 L.  46        60  LOAD_FAST                'extname'
               62  LOAD_STR                 'MATRIX'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_TRUE     92  'to 92'
               68  LOAD_FAST                'extname'
               70  LOAD_STR                 'SPI.-RMF.-RSP'
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_TRUE     92  'to 92'
               76  LOAD_FAST                'extname'
               78  LOAD_STR                 'ISGR-RMF.RSP'
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_TRUE     92  'to 92'
               84  LOAD_FAST                'extname'
               86  LOAD_STR                 'SPECRESP MATRIX'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   104  'to 104'
             92_0  COME_FROM            82  '82'
             92_1  COME_FROM            74  '74'
             92_2  COME_FROM            66  '66'

 L.  47        92  LOAD_GLOBAL              print
               94  LOAD_STR                 'Found matrix'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  POP_TOP          

 L.  48       100  LOAD_FAST                'i'
              102  STORE_FAST               'ind_matrix'
            104_0  COME_FROM            90  '90'

 L.  49       104  LOAD_FAST                'extname'
              106  LOAD_STR                 'EBOUNDS'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_TRUE    128  'to 128'
              112  LOAD_FAST                'extname'
              114  LOAD_STR                 'SPI.-EBDS-MOD'
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_TRUE    128  'to 128'
              120  LOAD_FAST                'extname'
              122  LOAD_STR                 'ISGR-EBDS-MOD'
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE    34  'to 34'
            128_0  COME_FROM           118  '118'
            128_1  COME_FROM           110  '110'

 L.  50       128  LOAD_GLOBAL              print
              130  LOAD_STR                 'Found energy boundaries'
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  POP_TOP          

 L.  51       136  LOAD_FAST                'i'
              138  STORE_FAST               'ind_ebounds'
              140  JUMP_BACK            34  'to 34'
              142  POP_BLOCK        
            144_0  COME_FROM_LOOP       18  '18'

 L.  53       144  LOAD_FAST                'ind_matrix'
              146  LOAD_CONST               0
              148  COMPARE_OP               <
              150  POP_JUMP_IF_TRUE    160  'to 160'
              152  LOAD_FAST                'ind_ebounds'
              154  LOAD_CONST               0
              156  COMPARE_OP               <
              158  POP_JUMP_IF_FALSE   176  'to 176'
            160_0  COME_FROM           150  '150'

 L.  54       160  LOAD_GLOBAL              print
              162  LOAD_STR                 'Could not find Extensions in matrix, exit'
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  POP_TOP          

 L.  55       168  LOAD_GLOBAL              RuntimeError
              170  LOAD_STR                 'Error'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  RAISE_VARARGS_1       1  'exception instance'
            176_0  COME_FROM           158  '158'

 L.  58       176  LOAD_FAST                'pf_buffer'
              178  LOAD_FAST                'ind_ebounds'
              180  BINARY_SUBSCR    
              182  LOAD_ATTR                data
              184  STORE_FAST               'buffer'

 L.  59       186  LOAD_FAST                'buffer'
              188  LOAD_STR                 'CHANNEL'
              190  BINARY_SUBSCR    
              192  STORE_FAST               'channel'

 L.  61       194  LOAD_FAST                'buffer'
              196  LOAD_STR                 'E_MIN'
              198  BINARY_SUBSCR    
              200  STORE_FAST               'emin'

 L.  62       202  LOAD_FAST                'buffer'
              204  LOAD_STR                 'E_MAX'
              206  BINARY_SUBSCR    
              208  STORE_FAST               'emax'

 L.  64       210  LOAD_GLOBAL              int
              212  LOAD_FAST                'pf_buffer'
              214  LOAD_FAST                'ind_matrix'
              216  BINARY_SUBSCR    
              218  LOAD_ATTR                header
              220  LOAD_STR                 'TLMIN4'
              222  BINARY_SUBSCR    
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  STORE_FAST               'chan_offset'

 L.  65       228  LOAD_FAST                'pf_buffer'
              230  LOAD_FAST                'ind_matrix'
              232  BINARY_SUBSCR    
              234  LOAD_ATTR                data
              236  STORE_FAST               'buffer'

 L.  67       238  LOAD_FAST                'buffer'
              240  LOAD_STR                 'MATRIX'
              242  BINARY_SUBSCR    
              244  STORE_FAST               'matrix'

 L.  68       246  LOAD_FAST                'buffer'
              248  LOAD_STR                 'ENERG_LO'
              250  BINARY_SUBSCR    
              252  STORE_FAST               'emin_rmf'

 L.  69       254  LOAD_FAST                'buffer'
              256  LOAD_STR                 'ENERG_HI'
              258  BINARY_SUBSCR    
              260  STORE_FAST               'emax_rmf'

 L.  70       262  LOAD_FAST                'buffer'
              264  LOAD_STR                 'N_GRP'
              266  BINARY_SUBSCR    
              268  STORE_FAST               'n_grp'

 L.  71       270  LOAD_FAST                'buffer'
              272  LOAD_STR                 'F_CHAN'
              274  BINARY_SUBSCR    
              276  STORE_FAST               'f_chan'

 L.  72       278  LOAD_FAST                'buffer'
              280  LOAD_STR                 'N_CHAN'
              282  BINARY_SUBSCR    
              284  STORE_FAST               'n_chan'

 L.  74       286  LOAD_GLOBAL              np
              288  LOAD_METHOD              zeros
              290  LOAD_GLOBAL              len
              292  LOAD_FAST                'emin_rmf'
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  CALL_METHOD_1         1  '1 positional argument'
              298  STORE_FAST               'res_array'

 L.  76   300_302  SETUP_LOOP         1010  'to 1010'
              304  LOAD_GLOBAL              range
              306  LOAD_GLOBAL              len
              308  LOAD_FAST                'emin_rmf'
              310  CALL_FUNCTION_1       1  '1 positional argument'
              312  CALL_FUNCTION_1       1  '1 positional argument'
              314  GET_ITER         
          316_318  FOR_ITER           1008  'to 1008'
              320  STORE_FAST               'i'

 L.  77       322  LOAD_FAST                'n_grp'
              324  LOAD_FAST                'i'
              326  BINARY_SUBSCR    
              328  LOAD_CONST               0
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_FALSE   360  'to 360'

 L.  79       336  LOAD_FAST                'emax_rmf'
              338  LOAD_FAST                'i'
              340  BINARY_SUBSCR    
              342  LOAD_FAST                'emin_rmf'
              344  LOAD_FAST                'i'
              346  BINARY_SUBSCR    
              348  BINARY_SUBTRACT  
              350  LOAD_FAST                'res_array'
              352  LOAD_FAST                'i'
              354  STORE_SUBSCR     

 L.  80   356_358  CONTINUE            316  'to 316'
            360_0  COME_FROM           332  '332'

 L.  81       360  LOAD_GLOBAL              np
              362  LOAD_METHOD              max
              364  LOAD_FAST                'matrix'
              366  LOAD_FAST                'i'
              368  BINARY_SUBSCR    
              370  CALL_METHOD_1         1  '1 positional argument'
              372  STORE_FAST               'max_rsp_local'

 L.  82       374  LOAD_FAST                'max_rsp_local'
              376  LOAD_CONST               0
              378  COMPARE_OP               ==
          380_382  POP_JUMP_IF_FALSE   408  'to 408'

 L.  83       384  LOAD_FAST                'emax_rmf'
              386  LOAD_FAST                'i'
              388  BINARY_SUBSCR    
              390  LOAD_FAST                'emin_rmf'
              392  LOAD_FAST                'i'
              394  BINARY_SUBSCR    
              396  BINARY_SUBTRACT  
              398  LOAD_FAST                'res_array'
              400  LOAD_FAST                'i'
              402  STORE_SUBSCR     

 L.  84   404_406  CONTINUE            316  'to 316'
            408_0  COME_FROM           380  '380'

 L.  93       408  LOAD_GLOBAL              isinstance
              410  LOAD_FAST                'f_chan'
              412  LOAD_FAST                'i'
              414  BINARY_SUBSCR    
              416  LOAD_GLOBAL              list
              418  LOAD_GLOBAL              tuple
              420  LOAD_GLOBAL              np
              422  LOAD_ATTR                ndarray
              424  BUILD_TUPLE_3         3 
              426  CALL_FUNCTION_2       2  '2 positional arguments'
          428_430  POP_JUMP_IF_FALSE   672  'to 672'

 L.  94       432  LOAD_FAST                'emin'
              434  LOAD_FAST                'f_chan'
              436  LOAD_FAST                'i'
              438  BINARY_SUBSCR    
              440  LOAD_CONST               0
              442  BINARY_SUBSCR    
              444  LOAD_FAST                'chan_offset'
              446  BINARY_SUBTRACT  
              448  LOAD_FAST                'f_chan'
              450  LOAD_FAST                'i'
              452  BINARY_SUBSCR    
              454  LOAD_CONST               0
              456  BINARY_SUBSCR    
              458  LOAD_FAST                'chan_offset'
              460  BINARY_SUBTRACT  
              462  LOAD_FAST                'n_chan'
              464  LOAD_FAST                'i'
              466  BINARY_SUBSCR    
              468  LOAD_CONST               0
              470  BINARY_SUBSCR    
              472  BINARY_ADD       
              474  BUILD_SLICE_2         2 
              476  BINARY_SUBSCR    
              478  STORE_FAST               'emin_local'

 L.  95       480  LOAD_FAST                'emax'
              482  LOAD_FAST                'f_chan'
              484  LOAD_FAST                'i'
              486  BINARY_SUBSCR    
              488  LOAD_CONST               0
              490  BINARY_SUBSCR    
              492  LOAD_FAST                'chan_offset'
              494  BINARY_SUBTRACT  
              496  LOAD_FAST                'f_chan'
              498  LOAD_FAST                'i'
              500  BINARY_SUBSCR    
              502  LOAD_CONST               0
              504  BINARY_SUBSCR    
              506  LOAD_FAST                'chan_offset'
              508  BINARY_SUBTRACT  
              510  LOAD_FAST                'n_chan'
              512  LOAD_FAST                'i'
              514  BINARY_SUBSCR    
              516  LOAD_CONST               0
              518  BINARY_SUBSCR    
              520  BINARY_ADD       
              522  BUILD_SLICE_2         2 
              524  BINARY_SUBSCR    
              526  STORE_FAST               'emax_local'

 L.  97       528  SETUP_LOOP          670  'to 670'
              530  LOAD_GLOBAL              range
              532  LOAD_CONST               1
              534  LOAD_FAST                'n_grp'
              536  LOAD_FAST                'i'
              538  BINARY_SUBSCR    
              540  CALL_FUNCTION_2       2  '2 positional arguments'
              542  GET_ITER         
              544  FOR_ITER            668  'to 668'
              546  STORE_FAST               'j'

 L.  99       548  LOAD_GLOBAL              np
              550  LOAD_METHOD              concatenate
              552  LOAD_FAST                'emin_local'
              554  LOAD_FAST                'emin'
              556  LOAD_FAST                'f_chan'
              558  LOAD_FAST                'i'
              560  BINARY_SUBSCR    
              562  LOAD_FAST                'j'
              564  BINARY_SUBSCR    
              566  LOAD_FAST                'chan_offset'
              568  BINARY_SUBTRACT  
              570  LOAD_FAST                'f_chan'
              572  LOAD_FAST                'i'
              574  BINARY_SUBSCR    
              576  LOAD_FAST                'j'
              578  BINARY_SUBSCR    
              580  LOAD_FAST                'chan_offset'
              582  BINARY_SUBTRACT  
              584  LOAD_FAST                'n_chan'
              586  LOAD_FAST                'i'
              588  BINARY_SUBSCR    
              590  LOAD_FAST                'j'
              592  BINARY_SUBSCR    
              594  BINARY_ADD       
              596  BUILD_SLICE_2         2 
              598  BINARY_SUBSCR    
              600  BUILD_LIST_2          2 
              602  CALL_METHOD_1         1  '1 positional argument'
              604  STORE_FAST               'emin_local'

 L. 100       606  LOAD_GLOBAL              np
              608  LOAD_METHOD              concatenate
              610  LOAD_FAST                'emax_local'
              612  LOAD_FAST                'emax'
              614  LOAD_FAST                'f_chan'
              616  LOAD_FAST                'i'
              618  BINARY_SUBSCR    
              620  LOAD_FAST                'j'
              622  BINARY_SUBSCR    
              624  LOAD_FAST                'chan_offset'
              626  BINARY_SUBTRACT  
              628  LOAD_FAST                'f_chan'
              630  LOAD_FAST                'i'
              632  BINARY_SUBSCR    
              634  LOAD_FAST                'j'
              636  BINARY_SUBSCR    
              638  LOAD_FAST                'chan_offset'
              640  BINARY_SUBTRACT  
              642  LOAD_FAST                'n_chan'
              644  LOAD_FAST                'i'
              646  BINARY_SUBSCR    
              648  LOAD_FAST                'j'
              650  BINARY_SUBSCR    
              652  BINARY_ADD       
              654  BUILD_SLICE_2         2 
              656  BINARY_SUBSCR    
              658  BUILD_LIST_2          2 
              660  CALL_METHOD_1         1  '1 positional argument'
              662  STORE_FAST               'emax_local'
          664_666  JUMP_BACK           544  'to 544'
              668  POP_BLOCK        
            670_0  COME_FROM_LOOP      528  '528'
              670  JUMP_FORWARD        862  'to 862'
            672_0  COME_FROM           428  '428'

 L. 103       672  LOAD_FAST                'emin'
              674  LOAD_FAST                'f_chan'
              676  LOAD_FAST                'i'
              678  BINARY_SUBSCR    
              680  LOAD_FAST                'chan_offset'
              682  BINARY_SUBTRACT  
              684  LOAD_FAST                'f_chan'
              686  LOAD_FAST                'i'
              688  BINARY_SUBSCR    
              690  LOAD_FAST                'chan_offset'
              692  BINARY_SUBTRACT  
              694  LOAD_FAST                'n_chan'
              696  LOAD_FAST                'i'
              698  BINARY_SUBSCR    
              700  BINARY_ADD       
              702  BUILD_SLICE_2         2 
              704  BINARY_SUBSCR    
              706  STORE_FAST               'emin_local'

 L. 104       708  LOAD_FAST                'emax'
              710  LOAD_FAST                'f_chan'
              712  LOAD_FAST                'i'
              714  BINARY_SUBSCR    
              716  LOAD_FAST                'chan_offset'
              718  BINARY_SUBTRACT  
              720  LOAD_FAST                'f_chan'
              722  LOAD_FAST                'i'
              724  BINARY_SUBSCR    
              726  LOAD_FAST                'chan_offset'
              728  BINARY_SUBTRACT  
              730  LOAD_FAST                'n_chan'
              732  LOAD_FAST                'i'
              734  BINARY_SUBSCR    
              736  BINARY_ADD       
              738  BUILD_SLICE_2         2 
              740  BINARY_SUBSCR    
              742  STORE_FAST               'emax_local'

 L. 106       744  SETUP_LOOP          862  'to 862'
              746  LOAD_GLOBAL              range
              748  LOAD_CONST               1
              750  LOAD_FAST                'n_grp'
              752  LOAD_FAST                'i'
              754  BINARY_SUBSCR    
              756  CALL_FUNCTION_2       2  '2 positional arguments'
              758  GET_ITER         
              760  FOR_ITER            860  'to 860'
              762  STORE_FAST               'j'

 L. 108       764  LOAD_GLOBAL              np
              766  LOAD_METHOD              concatenate
              768  LOAD_FAST                'emin_local'
              770  LOAD_FAST                'emin'
              772  LOAD_FAST                'f_chan'
              774  LOAD_FAST                'i'
              776  BINARY_SUBSCR    
              778  LOAD_FAST                'chan_offset'
              780  BINARY_SUBTRACT  
              782  LOAD_FAST                'f_chan'
              784  LOAD_FAST                'i'
              786  BINARY_SUBSCR    
              788  LOAD_FAST                'chan_offset'
              790  BINARY_SUBTRACT  
              792  LOAD_FAST                'n_chan'
              794  LOAD_FAST                'i'
              796  BINARY_SUBSCR    
              798  BINARY_ADD       
              800  BUILD_SLICE_2         2 
              802  BINARY_SUBSCR    
              804  BUILD_LIST_2          2 
              806  CALL_METHOD_1         1  '1 positional argument'
              808  STORE_FAST               'emin_local'

 L. 109       810  LOAD_GLOBAL              np
              812  LOAD_METHOD              concatenate
              814  LOAD_FAST                'emax_local'
              816  LOAD_FAST                'emax'
              818  LOAD_FAST                'f_chan'
              820  LOAD_FAST                'i'
              822  BINARY_SUBSCR    
              824  LOAD_FAST                'chan_offset'
              826  BINARY_SUBTRACT  
              828  LOAD_FAST                'f_chan'
              830  LOAD_FAST                'i'
              832  BINARY_SUBSCR    
              834  LOAD_FAST                'chan_offset'
              836  BINARY_SUBTRACT  
              838  LOAD_FAST                'n_chan'
              840  LOAD_FAST                'i'
              842  BINARY_SUBSCR    
              844  BINARY_ADD       
              846  BUILD_SLICE_2         2 
              848  BINARY_SUBSCR    
              850  BUILD_LIST_2          2 
              852  CALL_METHOD_1         1  '1 positional argument'
              854  STORE_FAST               'emax_local'
          856_858  JUMP_BACK           760  'to 760'
              860  POP_BLOCK        
            862_0  COME_FROM_LOOP      744  '744'
            862_1  COME_FROM           670  '670'

 L. 113       862  LOAD_GLOBAL              len
              864  LOAD_FAST                'matrix'
              866  LOAD_FAST                'i'
              868  BINARY_SUBSCR    
              870  CALL_FUNCTION_1       1  '1 positional argument'
              872  LOAD_GLOBAL              len
              874  LOAD_FAST                'emin_local'
              876  CALL_FUNCTION_1       1  '1 positional argument'
              878  COMPARE_OP               !=
          880_882  POP_JUMP_IF_FALSE   924  'to 924'

 L. 114       884  LOAD_GLOBAL              print
              886  LOAD_STR                 'Inconsistency with matrix and binning, something has gone wrong, aborting'
              888  CALL_FUNCTION_1       1  '1 positional argument'
              890  POP_TOP          

 L. 115       892  LOAD_GLOBAL              print
              894  LOAD_FAST                'i'
              896  LOAD_GLOBAL              len
              898  LOAD_FAST                'emin_local'
              900  CALL_FUNCTION_1       1  '1 positional argument'
              902  LOAD_GLOBAL              len
              904  LOAD_FAST                'matrix'
              906  LOAD_FAST                'i'
              908  BINARY_SUBSCR    
              910  CALL_FUNCTION_1       1  '1 positional argument'
              912  CALL_FUNCTION_3       3  '3 positional arguments'
              914  POP_TOP          

 L. 116       916  LOAD_GLOBAL              RuntimeError
              918  LOAD_STR                 'Error'
              920  CALL_FUNCTION_1       1  '1 positional argument'
              922  RAISE_VARARGS_1       1  'exception instance'
            924_0  COME_FROM           880  '880'

 L. 118       924  LOAD_FAST                'matrix'
              926  LOAD_FAST                'i'
              928  BINARY_SUBSCR    
              930  LOAD_FAST                'max_rsp_local'
              932  LOAD_CONST               2.0
              934  BINARY_TRUE_DIVIDE
              936  COMPARE_OP               >
              938  STORE_FAST               'ind_fwhm'

 L. 119       940  LOAD_GLOBAL              np
              942  LOAD_METHOD              count_nonzero
              944  LOAD_FAST                'ind_fwhm'
              946  CALL_METHOD_1         1  '1 positional argument'
              948  LOAD_CONST               0
              950  COMPARE_OP               ==
          952_954  POP_JUMP_IF_FALSE   972  'to 972'

 L. 120       956  LOAD_GLOBAL              print
              958  LOAD_STR                 'There are no bins larger than half the response, something wrong'
              960  CALL_FUNCTION_1       1  '1 positional argument'
              962  POP_TOP          

 L. 121       964  LOAD_GLOBAL              RuntimeError
              966  LOAD_STR                 'Error'
              968  CALL_FUNCTION_1       1  '1 positional argument'
              970  RAISE_VARARGS_1       1  'exception instance'
            972_0  COME_FROM           952  '952'

 L. 123       972  LOAD_GLOBAL              np
              974  LOAD_METHOD              max
              976  LOAD_FAST                'emax_local'
              978  LOAD_FAST                'ind_fwhm'
              980  BINARY_SUBSCR    
              982  CALL_METHOD_1         1  '1 positional argument'
              984  LOAD_GLOBAL              np
              986  LOAD_METHOD              min
              988  LOAD_FAST                'emin_local'
              990  LOAD_FAST                'ind_fwhm'
              992  BINARY_SUBSCR    
              994  CALL_METHOD_1         1  '1 positional argument'
              996  BINARY_SUBTRACT  
              998  LOAD_FAST                'res_array'
             1000  LOAD_FAST                'i'
             1002  STORE_SUBSCR     
         1004_1006  JUMP_BACK           316  'to 316'
             1008  POP_BLOCK        
           1010_0  COME_FROM_LOOP      300  '300'

 L. 125      1010  LOAD_FAST                'pf_buffer'
             1012  LOAD_METHOD              close
             1014  CALL_METHOD_0         0  '0 positional arguments'
             1016  POP_TOP          

 L. 127      1018  LOAD_GLOBAL              np
             1020  LOAD_METHOD              interp
             1022  LOAD_FAST                'emin'
             1024  LOAD_FAST                'emax'
             1026  BINARY_ADD       
             1028  LOAD_CONST               2
             1030  BINARY_TRUE_DIVIDE
             1032  LOAD_FAST                'emin_rmf'
             1034  LOAD_FAST                'emax_rmf'
             1036  BINARY_ADD       
             1038  LOAD_CONST               2
             1040  BINARY_TRUE_DIVIDE
             1042  LOAD_FAST                'res_array'
             1044  CALL_METHOD_3         3  '3 positional arguments'
             1046  STORE_FAST               'res_array_resampled'

 L. 145      1048  LOAD_FAST                'channel'
             1050  LOAD_FAST                'emin'
             1052  LOAD_FAST                'emax'
             1054  LOAD_FAST                'res_array_resampled'
             1056  BUILD_TUPLE_4         4 
             1058  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 104_0


help = "\nPURPOSE:\nGroup the spectra using Kaastra & Bleeker's recipe plus an option for a minimal number of counts\n"
help += 'the input spectrum file is grouped using grppha and the output has the _rbn.pi extension added to the root file name\n'
help += 'It is recommended not to set a minimum number of counts for spectral fitting of high-resolution spectra\n'
help += 'with a line-rich spectrum to avoid large bins that would bias the line centroid determination.\n'
help += 'However, it should be noted that Xspec has a problem with C-statistics when there are empmty bins.\n\n'
help += 'REFERENCE: Kaastra & Bleeker, 2016, A&A, 587, 151, Sect.5.3\n\n'
help += 'The response and background files are taken from the keywords in the input spectrum, but can be overriden by setting the optional parameters.\n\n'
help += 'The following parameters can be provided for a custom resolution, otherwise the optimal resolution is derived from the RMF file:\n'
help += 'eref = reference energy for energy resolution (keV)\n'
help += 'res = resolution at the reference energy (keV)\n'
help += 'en_dep = dependence of the resolution on energy (power-law index)\n'
help += '\n\nExamples:\noptimal_binning.py PNspectrum.fits -e 1.7 -E 11 -m 10\n'
help += 'optimal_binning.py -r acisf_heg_p1.rmf -a acisf_heg_p1.arf heg_p1.fits -e 2.0\n'
help += 'optimal_binning.py hxd_pin_sr.fits -e 12.  -E 60.\n'
help += 'optimal_binning.py xi0.pi -e 0.4 -E 11\n'
help += 'optimal_binning.py xi0_rbn.pi -e 0.4 -E 11. --eref 6 --en_dep -0.5 --res 0.6\n'
help += '\n\n'
help += 'To mimic the typical resolution of current instrumewnts, we provide the following suggestions\n'
help += 'Suzaku XIS1 eref=6 res=0.168 en_dep = -0.5\n'
help += 'Suzaku XIS0,XIS3 eref=6 res=0.153 en_dep = -0.5\n'
help += 'Suzaku PIN eref=15 res=4.125 en_dep = 0\n'
help += 'XMM EpicPN eref=6 res=0.175 en_dep = -0.5\n'
help += 'XMM EpicMOS eref=6 res=0.155 en_dep = -0.5\n'
help += '\n\nFor bugs and requests email to carlo.ferrigno AT unige.ch\n'
help += 'The script can be downloaded from the page http://www.isdc.unige.ch/~ferrigno/index.php/optimal-binning-script\n'

def execute_binning(spectrum, bkg, rmf, arf, mine=-10, maxe=10000000000.0, min_counts=0, eref=-1, res=-1, en_dep=-1):
    if mine >= maxe:
        raise RuntimeError('MinE > = MaxE (%f,%f)' % (mine, maxe))
    elif eref <= 0:
        if res >= 0 or eref >= 0:
            if res <= 0:
                raise RuntimeError('Optional arguments must be provided with positive reference energy and resolution\n\n' + help)
        elif os.environ.get('HEADAS') is None:
            raise RuntimeError('Please, initialize the Heasoft environemnt, we use the "grppha" program for grouping the spectrum')
        else:
            if not os.path.isfile(spectrum):
                raise RuntimeError('Error: file %s does not exist' % spectrum)
            else:
                buffer = pf.open(spectrum)
                ind_spectrum = -1
                for i in range(1, len(buffer)):
                    extname = buffer[i].header['EXTNAME']
                    print(extname)
                    if extname in ('SPECTRUM', 'ISGR-EVTS-SPE', 'ISGR-PHA1-SPE', 'JMX1-PHA1-SPE',
                                   'JMX2-PHA1-SPE'):
                        ind_spectrum = i

                if ind_spectrum < 0:
                    raise RuntimeError('Cannot find spectrum')
                src_exposure = float(buffer[ind_spectrum].header['EXPOSURE'])
                try:
                    src_counts = buffer[ind_spectrum].data['COUNTS']
                except:
                    try:
                        src_counts = buffer[ind_spectrum].data['RATE'] * src_exposure
                    except KeyError:
                        raise RuntimeError('No COUNTS or RATE column in spectrum')

            try:
                src_backscal = float(buffer[ind_spectrum].header['BACKSCAL'])
            except KeyError:
                print('No BACKSCAL keyword in %s defaulting to 1' % spectrum)
                src_backscal = 1

            try:
                quality = buffer[ind_spectrum].data['QUALITY']
            except KeyError:
                quality = np.zeros(len(src_counts))

            if rmf == 'none':
                rmf = buffer[ind_spectrum].header['RESPFILE']
            if arf == 'none':
                arf = buffer[ind_spectrum].header['ANCRFILE']
            if bkg == 'none':
                bkg = buffer[ind_spectrum].header['BACKFILE']
            buffer.close
            os.path.isfile(rmf) or print('The response file %s does not exist, check if you provided a custom resolution' % rmf)
            if eref <= 0 or res <= 0:
                raise RuntimeError('The values of "eref"=%f or "res"=%f are negative and you have not provided a valid RMF, the script cannot be used with this input' % (eref, res))
            else:
                channel, emin, emax, res_array = get_resolution_array(rmf)
        energy = (emin + emax) / 2.0
        if energy[0] > energy[(-1)]:
            energy *= -1
            tmp = mine
            mine = -maxe
            maxe = -tmp
        if mine == -10 or mine == -10000000000.0:
            mine = energy.min
        if maxe == 10000000000.0 or maxe == -10:
            maxe = energy.max
        if mine < energy.min:
            mine = energy.min
        if maxe > energy.max:
            maxe = energy.max
        parameter_string = '\nWe will use the following input parameters:\n'
        parameter_string += 'spectrum   = %s\n' % spectrum
        if eref > 0 and res > 0:
            parameter_string += 'res        = %g keV\n' % res
            parameter_string += 'E_ref      = %g keV\n' % eref
            parameter_string += 'E_dep      = %g\n' % en_dep
    else:
        parameter_string += 'RMF        = %s\n' % rmf
    parameter_string += 'ARF        = %s\n' % arf
    parameter_string += 'background = %s\n' % bkg
    parameter_string += 'min_counts = %g\n' % min_counts
    parameter_string += 'Emin       = %g\n' % mine
    parameter_string += 'Emax       = %g\n' % maxe
    parameter_string += '\n'
    print(parameter_string)
    bkg_counts = np.zeros(len(src_counts))
    bkg_exposure = 1
    bkg_backscal = 1
    bkg_test = bkg
    print(bkg_test)
    if bkg_test.lower != 'none':
        buffer = pf.open(bkg)
        try:
            bkg_exposure = float(buffer[1].header['EXPOSURE'])
        except:
            print('Not found background exposure, defaulting to the source exposure %g s' % src_exposure)
            bkg_exposure = src_exposure

        try:
            bkg_backscal = float(buffer[1].header['BACKSCAL'])
        except KeyError:
            print('No BACKSCAL keyword in %s defaulting to 1' % bkg)
            bkg_backscal = 1

        bkg_channel = buffer[1].data['CHANNEL']
        try:
            bkg_counts = buffer[1].data['COUNTS']
            bkg_err = np.sqrt(bkg_counts)
        except:
            try:
                bkg_rate = buffer[1].data['RATE']
                bkg_rate_err = buffer[1].data['STAT_ERR']
                bkg_counts = bkg_rate * bkg_exposure
                bkg_err = bkg_rate_err * bkg_exposure
            except:
                print('ERROR: Impossible to read COUNTS or RATE from background')
                os.exit(1)

        buffer.close
    r = (maxe - mine) / res
    if r > 10000.0:
        print('Warning: the resolution is not accurate')
    net_counts = src_counts - bkg_counts * src_backscal / bkg_backscal
    summed_net_counts = np.zeros(len(net_counts))
    ind = net_counts <= 0
    net_counts[ind] = 1
    for i, de in enumerate(res_array):
        ind1 = emin >= emin[i] - res_array[i] / 2
        ind2 = emax <= emax[i] + res_array[i] / 2
        ind = np.logical_and(ind1, ind2)
        summed_net_counts[i] = np.sum(net_counts[ind]) * 1.314

    r_vec = (emax - emin) / res_array
    r = np.sum(r_vec)
    print('resolution elements %g' % r)
    x = np.log(summed_net_counts * (1 + 0.2 * np.log(r)))
    oversample = np.ones(len(x))
    ind = x > 2.119
    oversample[ind] = (0.08 + 7.0 / x[ind] + 1.8 / x[ind] ** 2) / (1 + 5.9 / x[ind])
    outfile = '.'.join(spectrum.split('.')[:-1]) + '.rbn'
    outspectrum = '.'.join(spectrum.split('.')[:-1]) + '_rbn.pi'
    lun = open(outfile, 'w')
    nbins = 0
    ind_start = np.abs(energy - mine).argmin
    ind_stop = np.abs(energy - maxe).argmin
    chanmin = channel[ind_start]
    energymin = mine
    energymax = mine
    ind_min = ind_start
    while energymax < maxe:
        this_energy = (energymin + energymax) / 2.0
        ind_energy = np.abs(energy - this_energy).argmin
        if eref > 0:
            if res > 0:
                this_resolution = res * (this_energy / eref) ** en_dep
            else:
                this_resolution = res_array[ind_energy]
            energymax = energymin + this_resolution * oversample[ind_energy]
            if ind_energy < len(energy) - 1:
                if energymax <= energy[(ind_energy + 1)]:
                    energymax = energy[(ind_energy + 1)]
        else:
            energymax = energy.max
        ind_max = np.argmin(np.abs(energy - energymax))
        chanmax = channel[ind_max]
        bs_totcounts = 0
        nbins = 1
        while chanmax <= np.max(channel):
            if np.sum(quality[ind_min:ind_max]) > 0:
                print('Interval of channels with index %d-%d has bad quality, skip' % (ind_min, ind_max))
                quality[ind_min:ind_max] = quality[ind_min:ind_max] * 0 + 1
                chanmin = chanmax + 1
                ind_min = ind_max
                energymin = energymax
                nbins = 1
                break
            src_totcounts = np.sum(src_counts[ind_min:ind_max])
            bkg_totcounts = np.sum(bkg_counts[ind_min:ind_max])
            bs_totcounts = src_totcounts - bkg_totcounts * (src_exposure / bkg_exposure) * (src_backscal / bkg_backscal)
            if bs_totcounts >= min_counts:
                lun.write('%d %d %d\n' % (chanmin, chanmax, chanmax - chanmin + 1))
                chanmin = chanmax + 1
                ind_min = ind_max
                energymin = energymax
                nbins = 1
                break
            else:
                chanmax = chanmin + nbins
                ind_max = ind_min + nbins
                if chanmax >= np.max(channel) or ind_min + nbins >= len(energy):
                    lun.write('%d %d %d\n' % (chanmin, chanmax, chanmax - chanmin + 1))
                    print('Got to the end, exiting loop')
                    energymax = maxe
                    break
                else:
                    energymax = energy[(ind_min + nbins)]
                    nbins += 1

    lun.close
    print('Rebinning file: ' + outfile)
    print('Applying rebinning via grppha ...')
    os.system('/bin/rm -rf ' + outspectrum + ' > /dev/null')
    cmd = 'grppha infile=' + spectrum + ' outfile=' + outspectrum + ' comm="reset grouping & bad %d-%d %d-%d & group ' % (channel.min, channel[ind_start], channel[ind_stop], channel.max) + outfile + ' & chkey RESPFILE ' + os.path.basename(rmf) + ' & chkey ANCRFILE ' + os.path.basename(arf) + ' & chkey BACKFILE ' + os.path.basename(bkg) + ' & exit" > /dev/null'
    if run(cmd):
        print('Attention: probable error with "grppha" program execution')
    os.system('/bin/rm -rf ' + outfile + ' > /dev/null')
    if np.sum(quality) > 0:
        print('Update the quality column with the new values discard 0-%d, %d-' % (ind_start, ind_stop))
        quality[0:ind_start] = 1
        quality[ind_stop:] = 1
        outptr = pf.open(outspectrum, 'update')
        outptr[1].data['QUALITY'] = quality
        outptr.close