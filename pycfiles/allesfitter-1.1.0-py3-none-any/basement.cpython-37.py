# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/basement.py
# Compiled at: 2020-03-31 06:03:32
# Size of source mod 2**32: 79602 bytes
"""
Created on Fri Oct  5 00:17:06 2018

@author:
Maximilian N. Günther
MIT Kavli Institute for Astrophysics and Space Research, 
Massachusetts Institute of Technology,
77 Massachusetts Avenue,
Cambridge, MA 02109, 
USA
Email: maxgue@mit.edu
Web: www.mnguenther.com
"""
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np
import matplotlib.pyplot as plt
import os, sys, collections
from datetime import datetime
from multiprocessing import cpu_count
import warnings
warnings.filterwarnings('ignore', category=(np.VisibleDeprecationWarning))
warnings.filterwarnings('ignore', category=(np.RankWarning))
from scipy.special import ndtri
from scipy.stats import truncnorm
from exoworlds_rdx.lightcurves.index_transits import index_transits, index_eclipses, get_first_epoch, get_tmid_observed_transits
import priors.simulate_PDF as simulate_PDF

class Basement:
    __doc__ = "\n    The 'Basement' class contains all the data, settings, etc.\n    "

    def __init__(self, datadir):
        """
        Inputs:
        -------
        datadir : str
            the working directory for allesfitter
            must contain all the data files
            output directories and files will also be created inside datadir
        fast_fit : bool (optional; default is False)
            if False: 
                use all photometric data for the plot
            if True: 
                only use photometric data in an 8h window around the transit 
                requires a good initial guess of the epoch and period
                
        Returns:
        --------
        All the variables needed for allesfitter
        """
        self.now = datetime.now().isoformat()
        self.datadir = datadir
        self.outdir = os.path.join(datadir, 'results')
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        self.load_settings()
        self.load_params()
        self.load_data()
        if self.settings['shift_epoch']:
            try:
                self.change_epoch()
            except:
                warnings.warn('\nCould not shift epoch (ignore if no period was given)\n')

        if self.settings['fit_ttvs']:
            self.prepare_ttv_fit()
        self.external_priors = {}
        self.load_stellar_priors()
        self.ldcode_to_ldstr = [
         'none',
         'lin',
         'quad',
         'sing',
         'claret',
         'log',
         'sqrt',
         'exp',
         'power-2',
         'mugrid']
        for inst in self.settings['inst_phot']:
            key = 'flux'
            if (self.settings[('baseline_' + key + '_' + inst)] in ('sample_GP_Matern32',
                                                                    'sample_GP_SHO')) & (self.settings[('error_' + key + '_' + inst)] != 'sample'):
                raise ValueError('If you want to use ' + self.settings[('baseline_' + key + '_' + inst)] + ', you will want to sample the jitters, too!')

    def logprint(self, *text):
        print(*text)
        original = sys.stdout
        with open(os.path.join(self.outdir, 'logfile_' + self.now + '.log'), 'a') as (f):
            sys.stdout = f
            print(*text)
        sys.stdout = original

    def load_settings--- This code section failed: ---

 L. 226         0  LOAD_CODE                <code_object set_bool>
                2  LOAD_STR                 'Basement.load_settings.<locals>.set_bool'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'set_bool'

 L. 232         8  LOAD_CODE                <code_object unique>
               10  LOAD_STR                 'Basement.load_settings.<locals>.unique'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  STORE_FAST               'unique'

 L. 236        16  LOAD_GLOBAL              np
               18  LOAD_ATTR                genfromtxt
               20  LOAD_GLOBAL              os
               22  LOAD_ATTR                path
               24  LOAD_METHOD              join
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                datadir
               30  LOAD_STR                 'settings.csv'
               32  CALL_METHOD_2         2  '2 positional arguments'
               34  LOAD_CONST               None
               36  LOAD_STR                 'utf-8'
               38  LOAD_STR                 ','
               40  LOAD_CONST               ('dtype', 'encoding', 'delimiter')
               42  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               44  STORE_FAST               'rows'

 L. 239        46  SETUP_LOOP          216  'to 216'
               48  LOAD_GLOBAL              enumerate
               50  LOAD_FAST                'rows'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  GET_ITER         
             56_0  COME_FROM           156  '156'
               56  FOR_ITER            214  'to 214'
               58  UNPACK_SEQUENCE_2     2 
               60  STORE_FAST               'i'
               62  STORE_FAST               'row'

 L. 241        64  LOAD_FAST                'row'
               66  LOAD_CONST               0
               68  BINARY_SUBSCR    
               70  STORE_FAST               'name'

 L. 242        72  LOAD_FAST                'name'
               74  LOAD_CONST               None
               76  LOAD_CONST               7
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  LOAD_STR                 'planets'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   142  'to 142'

 L. 243        88  LOAD_STR                 'companions'
               90  LOAD_FAST                'name'
               92  LOAD_CONST               7
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  BINARY_ADD       
              102  LOAD_FAST                'rows'
              104  LOAD_FAST                'i'
              106  BINARY_SUBSCR    
              108  LOAD_CONST               0
              110  STORE_SUBSCR     

 L. 244       112  LOAD_GLOBAL              warnings
              114  LOAD_METHOD              warn
              116  LOAD_STR                 'Deprecation warning. You are using outdated keywords. Automatically renaming '
              118  LOAD_FAST                'name'
              120  BINARY_ADD       
              122  LOAD_STR                 ' ---> '
              124  BINARY_ADD       
              126  LOAD_FAST                'rows'
              128  LOAD_FAST                'i'
              130  BINARY_SUBSCR    
              132  LOAD_CONST               0
              134  BINARY_SUBSCR    
              136  BINARY_ADD       
              138  CALL_METHOD_1         1  '1 positional argument'
              140  POP_TOP          
            142_0  COME_FROM            86  '86'

 L. 245       142  LOAD_FAST                'name'
              144  LOAD_CONST               None
              146  LOAD_CONST               6
              148  BUILD_SLICE_2         2 
              150  BINARY_SUBSCR    
              152  LOAD_STR                 'ld_law'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE    56  'to 56'

 L. 246       158  LOAD_STR                 'host_ld_law'
              160  LOAD_FAST                'name'
              162  LOAD_CONST               6
              164  LOAD_CONST               None
              166  BUILD_SLICE_2         2 
              168  BINARY_SUBSCR    
              170  BINARY_ADD       
              172  LOAD_FAST                'rows'
              174  LOAD_FAST                'i'
              176  BINARY_SUBSCR    
              178  LOAD_CONST               0
              180  STORE_SUBSCR     

 L. 247       182  LOAD_GLOBAL              warnings
              184  LOAD_METHOD              warn
              186  LOAD_STR                 'Deprecation warning. You are using outdated keywords. Automatically renaming '
              188  LOAD_FAST                'name'
              190  BINARY_ADD       
              192  LOAD_STR                 ' ---> '
              194  BINARY_ADD       
              196  LOAD_FAST                'rows'
              198  LOAD_FAST                'i'
              200  BINARY_SUBSCR    
              202  LOAD_CONST               0
              204  BINARY_SUBSCR    
              206  BINARY_ADD       
              208  CALL_METHOD_1         1  '1 positional argument'
              210  POP_TOP          
              212  JUMP_BACK            56  'to 56'
              214  POP_BLOCK        
            216_0  COME_FROM_LOOP       46  '46'

 L. 250       216  LOAD_GLOBAL              collections
              218  LOAD_METHOD              OrderedDict
              220  LOAD_CONST               ('user-given:', '')
              222  BUILD_LIST_1          1 
              224  LOAD_LISTCOMP            '<code_object <listcomp>>'
              226  LOAD_STR                 'Basement.load_settings.<locals>.<listcomp>'
              228  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              230  LOAD_FAST                'rows'
              232  GET_ITER         
              234  CALL_FUNCTION_1       1  '1 positional argument'
              236  BINARY_ADD       
              238  LOAD_CONST               ('automatically set:', '')
              240  BUILD_LIST_1          1 
              242  BINARY_ADD       
              244  CALL_METHOD_1         1  '1 positional argument'
              246  LOAD_FAST                'self'
              248  STORE_ATTR               settings

 L. 256       250  SETUP_LOOP          344  'to 344'
              252  LOAD_CONST               ('companions_phot', 'companions_rv', 'inst_phot', 'inst_rv')
              254  GET_ITER         
              256  FOR_ITER            342  'to 342'
              258  STORE_FAST               'key'

 L. 257       260  LOAD_FAST                'key'
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                settings
              266  COMPARE_OP               not-in
          268_270  POP_JUMP_IF_FALSE   284  'to 284'

 L. 258       272  BUILD_LIST_0          0 
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                settings
              278  LOAD_FAST                'key'
              280  STORE_SUBSCR     
              282  JUMP_BACK           256  'to 256'
            284_0  COME_FROM           268  '268'

 L. 259       284  LOAD_GLOBAL              len
              286  LOAD_FAST                'self'
              288  LOAD_ATTR                settings
              290  LOAD_FAST                'key'
              292  BINARY_SUBSCR    
              294  CALL_FUNCTION_1       1  '1 positional argument'
          296_298  POP_JUMP_IF_FALSE   328  'to 328'

 L. 260       300  LOAD_GLOBAL              str
              302  LOAD_FAST                'self'
              304  LOAD_ATTR                settings
              306  LOAD_FAST                'key'
              308  BINARY_SUBSCR    
              310  CALL_FUNCTION_1       1  '1 positional argument'
              312  LOAD_METHOD              split
              314  LOAD_STR                 ' '
              316  CALL_METHOD_1         1  '1 positional argument'
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                settings
              322  LOAD_FAST                'key'
              324  STORE_SUBSCR     
              326  JUMP_BACK           256  'to 256'
            328_0  COME_FROM           296  '296'

 L. 262       328  BUILD_LIST_0          0 
              330  LOAD_FAST                'self'
              332  LOAD_ATTR                settings
              334  LOAD_FAST                'key'
              336  STORE_SUBSCR     
          338_340  JUMP_BACK           256  'to 256'
              342  POP_BLOCK        
            344_0  COME_FROM_LOOP      250  '250'

 L. 264       344  LOAD_GLOBAL              list
              346  LOAD_GLOBAL              np
              348  LOAD_METHOD              unique
              350  LOAD_FAST                'self'
              352  LOAD_ATTR                settings
              354  LOAD_STR                 'companions_phot'
              356  BINARY_SUBSCR    
              358  LOAD_FAST                'self'
              360  LOAD_ATTR                settings
              362  LOAD_STR                 'companions_rv'
              364  BINARY_SUBSCR    
              366  BINARY_ADD       
              368  CALL_METHOD_1         1  '1 positional argument'
              370  CALL_FUNCTION_1       1  '1 positional argument'
              372  LOAD_FAST                'self'
              374  LOAD_ATTR                settings
              376  LOAD_STR                 'companions_all'
              378  STORE_SUBSCR     

 L. 265       380  LOAD_GLOBAL              list
              382  LOAD_FAST                'unique'
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                settings
              388  LOAD_STR                 'inst_phot'
              390  BINARY_SUBSCR    
              392  LOAD_FAST                'self'
              394  LOAD_ATTR                settings
              396  LOAD_STR                 'inst_rv'
              398  BINARY_SUBSCR    
              400  BINARY_ADD       
              402  CALL_FUNCTION_1       1  '1 positional argument'
              404  CALL_FUNCTION_1       1  '1 positional argument'
              406  LOAD_FAST                'self'
              408  LOAD_ATTR                settings
              410  LOAD_STR                 'inst_all'
              412  STORE_SUBSCR     

 L. 271       414  LOAD_STR                 'print_progress'
              416  LOAD_FAST                'self'
              418  LOAD_ATTR                settings
              420  COMPARE_OP               in
          422_424  POP_JUMP_IF_FALSE   448  'to 448'

 L. 272       426  LOAD_FAST                'set_bool'
              428  LOAD_FAST                'self'
              430  LOAD_ATTR                settings
              432  LOAD_STR                 'print_progress'
              434  BINARY_SUBSCR    
              436  CALL_FUNCTION_1       1  '1 positional argument'
              438  LOAD_FAST                'self'
              440  LOAD_ATTR                settings
              442  LOAD_STR                 'print_progress'
              444  STORE_SUBSCR     
              446  JUMP_FORWARD        458  'to 458'
            448_0  COME_FROM           422  '422'

 L. 274       448  LOAD_CONST               True
              450  LOAD_FAST                'self'
              452  LOAD_ATTR                settings
              454  LOAD_STR                 'print_progress'
              456  STORE_SUBSCR     
            458_0  COME_FROM           446  '446'

 L. 280       458  LOAD_STR                 'shift_epoch'
              460  LOAD_FAST                'self'
              462  LOAD_ATTR                settings
              464  COMPARE_OP               in
          466_468  POP_JUMP_IF_FALSE   492  'to 492'

 L. 281       470  LOAD_FAST                'set_bool'
              472  LOAD_FAST                'self'
              474  LOAD_ATTR                settings
              476  LOAD_STR                 'shift_epoch'
              478  BINARY_SUBSCR    
              480  CALL_FUNCTION_1       1  '1 positional argument'
              482  LOAD_FAST                'self'
              484  LOAD_ATTR                settings
              486  LOAD_STR                 'shift_epoch'
              488  STORE_SUBSCR     
              490  JUMP_FORWARD        502  'to 502'
            492_0  COME_FROM           466  '466'

 L. 283       492  LOAD_CONST               False
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                settings
              498  LOAD_STR                 'shift_epoch'
              500  STORE_SUBSCR     
            502_0  COME_FROM           490  '490'

 L. 286       502  SETUP_LOOP          698  'to 698'
              504  LOAD_FAST                'self'
              506  LOAD_ATTR                settings
              508  LOAD_STR                 'companions_all'
              510  BINARY_SUBSCR    
              512  GET_ITER         
              514  FOR_ITER            696  'to 696'
              516  STORE_FAST               'companion'

 L. 287       518  LOAD_STR                 'inst_for_'
              520  LOAD_FAST                'companion'
              522  BINARY_ADD       
              524  LOAD_STR                 '_epoch'
              526  BINARY_ADD       
              528  LOAD_FAST                'self'
              530  LOAD_ATTR                settings
              532  COMPARE_OP               not-in
          534_536  POP_JUMP_IF_FALSE   556  'to 556'

 L. 288       538  LOAD_STR                 'all'
              540  LOAD_FAST                'self'
              542  LOAD_ATTR                settings
              544  LOAD_STR                 'inst_for_'
              546  LOAD_FAST                'companion'
              548  BINARY_ADD       
              550  LOAD_STR                 '_epoch'
              552  BINARY_ADD       
              554  STORE_SUBSCR     
            556_0  COME_FROM           534  '534'

 L. 290       556  LOAD_FAST                'self'
              558  LOAD_ATTR                settings
              560  LOAD_STR                 'inst_for_'
              562  LOAD_FAST                'companion'
              564  BINARY_ADD       
              566  LOAD_STR                 '_epoch'
              568  BINARY_ADD       
              570  BINARY_SUBSCR    
              572  LOAD_CONST               ('all', 'none')
              574  COMPARE_OP               in
          576_578  POP_JUMP_IF_FALSE   606  'to 606'

 L. 291       580  LOAD_FAST                'self'
              582  LOAD_ATTR                settings
              584  LOAD_STR                 'inst_all'
              586  BINARY_SUBSCR    
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                settings
              592  LOAD_STR                 'inst_for_'
              594  LOAD_FAST                'companion'
              596  BINARY_ADD       
              598  LOAD_STR                 '_epoch'
              600  BINARY_ADD       
              602  STORE_SUBSCR     
              604  JUMP_BACK           514  'to 514'
            606_0  COME_FROM           576  '576'

 L. 293       606  LOAD_GLOBAL              len
              608  LOAD_FAST                'self'
              610  LOAD_ATTR                settings
              612  LOAD_STR                 'inst_for_'
              614  LOAD_FAST                'companion'
              616  BINARY_ADD       
              618  LOAD_STR                 '_epoch'
              620  BINARY_ADD       
              622  BINARY_SUBSCR    
              624  CALL_FUNCTION_1       1  '1 positional argument'
          626_628  POP_JUMP_IF_FALSE   674  'to 674'

 L. 294       630  LOAD_GLOBAL              str
              632  LOAD_FAST                'self'
              634  LOAD_ATTR                settings
              636  LOAD_STR                 'inst_for_'
              638  LOAD_FAST                'companion'
              640  BINARY_ADD       
              642  LOAD_STR                 '_epoch'
              644  BINARY_ADD       
              646  BINARY_SUBSCR    
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  LOAD_METHOD              split
              652  LOAD_STR                 ' '
              654  CALL_METHOD_1         1  '1 positional argument'
              656  LOAD_FAST                'self'
              658  LOAD_ATTR                settings
              660  LOAD_STR                 'inst_for_'
              662  LOAD_FAST                'companion'
              664  BINARY_ADD       
              666  LOAD_STR                 '_epoch'
              668  BINARY_ADD       
              670  STORE_SUBSCR     
              672  JUMP_BACK           514  'to 514'
            674_0  COME_FROM           626  '626'

 L. 296       674  BUILD_LIST_0          0 
              676  LOAD_FAST                'self'
              678  LOAD_ATTR                settings
              680  LOAD_STR                 'inst_for_'
              682  LOAD_FAST                'companion'
              684  BINARY_ADD       
              686  LOAD_STR                 '_epoch'
              688  BINARY_ADD       
              690  STORE_SUBSCR     
          692_694  JUMP_BACK           514  'to 514'
              696  POP_BLOCK        
            698_0  COME_FROM_LOOP      502  '502'

 L. 302       698  LOAD_FAST                'set_bool'
              700  LOAD_FAST                'self'
              702  LOAD_ATTR                settings
              704  LOAD_STR                 'multiprocess'
              706  BINARY_SUBSCR    
              708  CALL_FUNCTION_1       1  '1 positional argument'
              710  LOAD_FAST                'self'
              712  LOAD_ATTR                settings
              714  LOAD_STR                 'multiprocess'
              716  STORE_SUBSCR     

 L. 304       718  LOAD_STR                 'multiprocess_cores'
              720  LOAD_FAST                'self'
              722  LOAD_ATTR                settings
              724  LOAD_METHOD              keys
              726  CALL_METHOD_0         0  '0 positional arguments'
              728  COMPARE_OP               not-in
          730_732  POP_JUMP_IF_FALSE   752  'to 752'

 L. 305       734  LOAD_GLOBAL              cpu_count
              736  CALL_FUNCTION_0       0  '0 positional arguments'
              738  LOAD_CONST               1
              740  BINARY_SUBTRACT  
              742  LOAD_FAST                'self'
              744  LOAD_ATTR                settings
              746  LOAD_STR                 'multiprocess_cores'
              748  STORE_SUBSCR     
              750  JUMP_FORWARD        950  'to 950'
            752_0  COME_FROM           730  '730'

 L. 306       752  LOAD_FAST                'self'
              754  LOAD_ATTR                settings
              756  LOAD_STR                 'multiprocess_cores'
              758  BINARY_SUBSCR    
              760  LOAD_STR                 'all'
              762  COMPARE_OP               ==
          764_766  POP_JUMP_IF_FALSE   786  'to 786'

 L. 307       768  LOAD_GLOBAL              cpu_count
              770  CALL_FUNCTION_0       0  '0 positional arguments'
              772  LOAD_CONST               1
              774  BINARY_SUBTRACT  
              776  LOAD_FAST                'self'
              778  LOAD_ATTR                settings
              780  LOAD_STR                 'multiprocess_cores'
              782  STORE_SUBSCR     
              784  JUMP_FORWARD        950  'to 950'
            786_0  COME_FROM           764  '764'

 L. 309       786  LOAD_GLOBAL              int
              788  LOAD_FAST                'self'
              790  LOAD_ATTR                settings
              792  LOAD_STR                 'multiprocess_cores'
              794  BINARY_SUBSCR    
              796  CALL_FUNCTION_1       1  '1 positional argument'
              798  LOAD_FAST                'self'
              800  LOAD_ATTR                settings
              802  LOAD_STR                 'multiprocess_cores'
              804  STORE_SUBSCR     

 L. 310       806  LOAD_FAST                'self'
              808  LOAD_ATTR                settings
              810  LOAD_STR                 'multiprocess_cores'
              812  BINARY_SUBSCR    
              814  LOAD_GLOBAL              cpu_count
              816  CALL_FUNCTION_0       0  '0 positional arguments'
              818  COMPARE_OP               ==
          820_822  POP_JUMP_IF_FALSE   870  'to 870'

 L. 311       824  LOAD_STR                 'You are pushing your luck: you want to run on '
              826  LOAD_GLOBAL              str
              828  LOAD_FAST                'self'
              830  LOAD_ATTR                settings
              832  LOAD_STR                 'multiprocess_cores'
              834  BINARY_SUBSCR    
              836  CALL_FUNCTION_1       1  '1 positional argument'
              838  BINARY_ADD       
              840  LOAD_STR                 ' cores, but your computer has only '
              842  BINARY_ADD       
              844  LOAD_GLOBAL              str
              846  LOAD_GLOBAL              cpu_count
              848  CALL_FUNCTION_0       0  '0 positional arguments'
              850  CALL_FUNCTION_1       1  '1 positional argument'
              852  BINARY_ADD       
              854  LOAD_STR                 '. I will let you go through with it this time...'
              856  BINARY_ADD       
              858  STORE_FAST               'string'

 L. 312       860  LOAD_GLOBAL              warnings
              862  LOAD_METHOD              warn
              864  LOAD_FAST                'string'
              866  CALL_METHOD_1         1  '1 positional argument'
              868  POP_TOP          
            870_0  COME_FROM           820  '820'

 L. 313       870  LOAD_FAST                'self'
              872  LOAD_ATTR                settings
              874  LOAD_STR                 'multiprocess_cores'
              876  BINARY_SUBSCR    
              878  LOAD_GLOBAL              cpu_count
              880  CALL_FUNCTION_0       0  '0 positional arguments'
              882  COMPARE_OP               >
          884_886  POP_JUMP_IF_FALSE   950  'to 950'

 L. 314       888  LOAD_STR                 'Oops, you want to run on '
              890  LOAD_GLOBAL              str
              892  LOAD_FAST                'self'
              894  LOAD_ATTR                settings
              896  LOAD_STR                 'multiprocess_cores'
              898  BINARY_SUBSCR    
              900  CALL_FUNCTION_1       1  '1 positional argument'
              902  BINARY_ADD       
              904  LOAD_STR                 ' cores, but your computer has only '
              906  BINARY_ADD       
              908  LOAD_GLOBAL              str
              910  LOAD_GLOBAL              cpu_count
              912  CALL_FUNCTION_0       0  '0 positional arguments'
              914  CALL_FUNCTION_1       1  '1 positional argument'
              916  BINARY_ADD       
              918  LOAD_STR                 '. Maybe try running on '
              920  BINARY_ADD       
              922  LOAD_GLOBAL              str
              924  LOAD_GLOBAL              cpu_count
              926  CALL_FUNCTION_0       0  '0 positional arguments'
              928  LOAD_CONST               1
              930  BINARY_SUBTRACT  
              932  CALL_FUNCTION_1       1  '1 positional argument'
              934  BINARY_ADD       
              936  LOAD_STR                 '?'
              938  BINARY_ADD       
              940  STORE_FAST               'string'

 L. 315       942  LOAD_GLOBAL              ValueError
              944  LOAD_FAST                'string'
              946  CALL_FUNCTION_1       1  '1 positional argument'
              948  RAISE_VARARGS_1       1  'exception instance'
            950_0  COME_FROM           884  '884'
            950_1  COME_FROM           784  '784'
            950_2  COME_FROM           750  '750'

 L. 321       950  LOAD_STR                 'phase_variations'
              952  LOAD_FAST                'self'
              954  LOAD_ATTR                settings
              956  LOAD_METHOD              keys
              958  CALL_METHOD_0         0  '0 positional arguments'
              960  COMPARE_OP               in
          962_964  POP_JUMP_IF_FALSE  1008  'to 1008'
              966  LOAD_GLOBAL              len
              968  LOAD_FAST                'self'
              970  LOAD_ATTR                settings
              972  LOAD_STR                 'phase_variations'
              974  BINARY_SUBSCR    
              976  CALL_FUNCTION_1       1  '1 positional argument'
          978_980  POP_JUMP_IF_FALSE  1008  'to 1008'

 L. 322       982  LOAD_GLOBAL              warnings
              984  LOAD_METHOD              warn
              986  LOAD_STR                 '\nDeprecation warning. You are using outdated keywords. Automatically renaming "phase_variations" ---> "phase_curve".\n'
              988  CALL_METHOD_1         1  '1 positional argument'
              990  POP_TOP          

 L. 323       992  LOAD_FAST                'self'
              994  LOAD_ATTR                settings
              996  LOAD_STR                 'phase_variations'
              998  BINARY_SUBSCR    
             1000  LOAD_FAST                'self'
             1002  LOAD_ATTR                settings
             1004  LOAD_STR                 'phase_curve'
             1006  STORE_SUBSCR     
           1008_0  COME_FROM           978  '978'
           1008_1  COME_FROM           962  '962'

 L. 325      1008  LOAD_STR                 'phase_curve'
             1010  LOAD_FAST                'self'
             1012  LOAD_ATTR                settings
             1014  LOAD_METHOD              keys
             1016  CALL_METHOD_0         0  '0 positional arguments'
             1018  COMPARE_OP               in
         1020_1022  POP_JUMP_IF_FALSE  1098  'to 1098'
             1024  LOAD_GLOBAL              len
             1026  LOAD_FAST                'self'
             1028  LOAD_ATTR                settings
             1030  LOAD_STR                 'phase_curve'
             1032  BINARY_SUBSCR    
             1034  CALL_FUNCTION_1       1  '1 positional argument'
         1036_1038  POP_JUMP_IF_FALSE  1098  'to 1098'

 L. 326      1040  LOAD_FAST                'set_bool'
             1042  LOAD_FAST                'self'
             1044  LOAD_ATTR                settings
             1046  LOAD_STR                 'phase_curve'
             1048  BINARY_SUBSCR    
             1050  CALL_FUNCTION_1       1  '1 positional argument'
             1052  LOAD_FAST                'self'
             1054  LOAD_ATTR                settings
             1056  LOAD_STR                 'phase_curve'
             1058  STORE_SUBSCR     

 L. 327      1060  LOAD_FAST                'self'
             1062  LOAD_ATTR                settings
             1064  LOAD_STR                 'phase_curve'
             1066  BINARY_SUBSCR    
             1068  LOAD_CONST               True
             1070  COMPARE_OP               ==
         1072_1074  POP_JUMP_IF_FALSE  1108  'to 1108'

 L. 329      1076  LOAD_STR                 'False'
             1078  LOAD_FAST                'self'
             1080  LOAD_ATTR                settings
             1082  LOAD_STR                 'fast_fit'
             1084  STORE_SUBSCR     

 L. 330      1086  LOAD_STR                 'True'
             1088  LOAD_FAST                'self'
             1090  LOAD_ATTR                settings
             1092  LOAD_STR                 'secondary_eclipse'
             1094  STORE_SUBSCR     
             1096  JUMP_FORWARD       1108  'to 1108'
           1098_0  COME_FROM          1036  '1036'
           1098_1  COME_FROM          1020  '1020'

 L. 332      1098  LOAD_CONST               False
             1100  LOAD_FAST                'self'
             1102  LOAD_ATTR                settings
             1104  LOAD_STR                 'phase_curve'
             1106  STORE_SUBSCR     
           1108_0  COME_FROM          1096  '1096'
           1108_1  COME_FROM          1072  '1072'

 L. 338      1108  LOAD_STR                 'fast_fit'
             1110  LOAD_FAST                'self'
             1112  LOAD_ATTR                settings
             1114  LOAD_METHOD              keys
             1116  CALL_METHOD_0         0  '0 positional arguments'
             1118  COMPARE_OP               in
         1120_1122  POP_JUMP_IF_FALSE  1162  'to 1162'
             1124  LOAD_GLOBAL              len
             1126  LOAD_FAST                'self'
             1128  LOAD_ATTR                settings
             1130  LOAD_STR                 'fast_fit'
             1132  BINARY_SUBSCR    
             1134  CALL_FUNCTION_1       1  '1 positional argument'
         1136_1138  POP_JUMP_IF_FALSE  1162  'to 1162'

 L. 339      1140  LOAD_FAST                'set_bool'
             1142  LOAD_FAST                'self'
             1144  LOAD_ATTR                settings
             1146  LOAD_STR                 'fast_fit'
             1148  BINARY_SUBSCR    
             1150  CALL_FUNCTION_1       1  '1 positional argument'
             1152  LOAD_FAST                'self'
             1154  LOAD_ATTR                settings
             1156  LOAD_STR                 'fast_fit'
             1158  STORE_SUBSCR     
             1160  JUMP_FORWARD       1172  'to 1172'
           1162_0  COME_FROM          1136  '1136'
           1162_1  COME_FROM          1120  '1120'

 L. 341      1162  LOAD_CONST               False
             1164  LOAD_FAST                'self'
             1166  LOAD_ATTR                settings
             1168  LOAD_STR                 'fast_fit'
             1170  STORE_SUBSCR     
           1172_0  COME_FROM          1160  '1160'

 L. 343      1172  LOAD_STR                 'fast_fit_width'
             1174  LOAD_FAST                'self'
             1176  LOAD_ATTR                settings
             1178  LOAD_METHOD              keys
             1180  CALL_METHOD_0         0  '0 positional arguments'
             1182  COMPARE_OP               in
         1184_1186  POP_JUMP_IF_FALSE  1228  'to 1228'
             1188  LOAD_GLOBAL              len
             1190  LOAD_FAST                'self'
             1192  LOAD_ATTR                settings
             1194  LOAD_STR                 'fast_fit_width'
             1196  BINARY_SUBSCR    
             1198  CALL_FUNCTION_1       1  '1 positional argument'
         1200_1202  POP_JUMP_IF_FALSE  1228  'to 1228'

 L. 344      1204  LOAD_GLOBAL              np
             1206  LOAD_METHOD              float
             1208  LOAD_FAST                'self'
             1210  LOAD_ATTR                settings
             1212  LOAD_STR                 'fast_fit_width'
             1214  BINARY_SUBSCR    
             1216  CALL_METHOD_1         1  '1 positional argument'
             1218  LOAD_FAST                'self'
             1220  LOAD_ATTR                settings
             1222  LOAD_STR                 'fast_fit_width'
             1224  STORE_SUBSCR     
             1226  JUMP_FORWARD       1238  'to 1238'
           1228_0  COME_FROM          1200  '1200'
           1228_1  COME_FROM          1184  '1184'

 L. 346      1228  LOAD_CONST               0.3333333333333333
             1230  LOAD_FAST                'self'
             1232  LOAD_ATTR                settings
             1234  LOAD_STR                 'fast_fit_width'
             1236  STORE_SUBSCR     
           1238_0  COME_FROM          1226  '1226'

 L. 352      1238  LOAD_STR                 'use_host_density_prior'
             1240  LOAD_FAST                'self'
             1242  LOAD_ATTR                settings
             1244  COMPARE_OP               in
         1246_1248  POP_JUMP_IF_FALSE  1272  'to 1272'

 L. 353      1250  LOAD_FAST                'set_bool'
             1252  LOAD_FAST                'self'
             1254  LOAD_ATTR                settings
             1256  LOAD_STR                 'use_host_density_prior'
             1258  BINARY_SUBSCR    
             1260  CALL_FUNCTION_1       1  '1 positional argument'
             1262  LOAD_FAST                'self'
             1264  LOAD_ATTR                settings
             1266  LOAD_STR                 'use_host_density_prior'
             1268  STORE_SUBSCR     
             1270  JUMP_FORWARD       1282  'to 1282'
           1272_0  COME_FROM          1246  '1246'

 L. 355      1272  LOAD_CONST               True
             1274  LOAD_FAST                'self'
             1276  LOAD_ATTR                settings
             1278  LOAD_STR                 'use_host_density_prior'
             1280  STORE_SUBSCR     
           1282_0  COME_FROM          1270  '1270'

 L. 361      1282  LOAD_STR                 'fit_ttvs'
             1284  LOAD_FAST                'self'
             1286  LOAD_ATTR                settings
             1288  LOAD_METHOD              keys
             1290  CALL_METHOD_0         0  '0 positional arguments'
             1292  COMPARE_OP               in
         1294_1296  POP_JUMP_IF_FALSE  1376  'to 1376'
             1298  LOAD_GLOBAL              len
             1300  LOAD_FAST                'self'
             1302  LOAD_ATTR                settings
             1304  LOAD_STR                 'fit_ttvs'
             1306  BINARY_SUBSCR    
             1308  CALL_FUNCTION_1       1  '1 positional argument'
         1310_1312  POP_JUMP_IF_FALSE  1376  'to 1376'

 L. 362      1314  LOAD_FAST                'set_bool'
             1316  LOAD_FAST                'self'
             1318  LOAD_ATTR                settings
             1320  LOAD_STR                 'fit_ttvs'
             1322  BINARY_SUBSCR    
             1324  CALL_FUNCTION_1       1  '1 positional argument'
             1326  LOAD_FAST                'self'
             1328  LOAD_ATTR                settings
             1330  LOAD_STR                 'fit_ttvs'
             1332  STORE_SUBSCR     

 L. 363      1334  LOAD_FAST                'self'
             1336  LOAD_ATTR                settings
             1338  LOAD_STR                 'fit_ttvs'
             1340  BINARY_SUBSCR    
             1342  LOAD_CONST               True
             1344  COMPARE_OP               ==
         1346_1348  POP_JUMP_IF_FALSE  1386  'to 1386'
             1350  LOAD_FAST                'self'
             1352  LOAD_ATTR                settings
             1354  LOAD_STR                 'fast_fit'
             1356  BINARY_SUBSCR    
             1358  LOAD_CONST               False
             1360  COMPARE_OP               ==
         1362_1364  POP_JUMP_IF_FALSE  1386  'to 1386'

 L. 364      1366  LOAD_GLOBAL              ValueError
             1368  LOAD_STR                 'fit_ttvs==True, but fast_fit==False. Currently, you can only fit for TTVs if fast_fit==True. Please choose different settings.'
             1370  CALL_FUNCTION_1       1  '1 positional argument'
             1372  RAISE_VARARGS_1       1  'exception instance'
             1374  JUMP_FORWARD       1386  'to 1386'
           1376_0  COME_FROM          1310  '1310'
           1376_1  COME_FROM          1294  '1294'

 L. 366      1376  LOAD_CONST               False
             1378  LOAD_FAST                'self'
             1380  LOAD_ATTR                settings
             1382  LOAD_STR                 'fit_ttvs'
             1384  STORE_SUBSCR     
           1386_0  COME_FROM          1374  '1374'
           1386_1  COME_FROM          1362  '1362'
           1386_2  COME_FROM          1346  '1346'

 L. 372      1386  LOAD_STR                 'secondary_eclipse'
             1388  LOAD_FAST                'self'
             1390  LOAD_ATTR                settings
             1392  LOAD_METHOD              keys
             1394  CALL_METHOD_0         0  '0 positional arguments'
             1396  COMPARE_OP               in
         1398_1400  POP_JUMP_IF_FALSE  1440  'to 1440'
             1402  LOAD_GLOBAL              len
             1404  LOAD_FAST                'self'
             1406  LOAD_ATTR                settings
             1408  LOAD_STR                 'secondary_eclipse'
             1410  BINARY_SUBSCR    
             1412  CALL_FUNCTION_1       1  '1 positional argument'
         1414_1416  POP_JUMP_IF_FALSE  1440  'to 1440'

 L. 373      1418  LOAD_FAST                'set_bool'
             1420  LOAD_FAST                'self'
             1422  LOAD_ATTR                settings
             1424  LOAD_STR                 'secondary_eclipse'
             1426  BINARY_SUBSCR    
             1428  CALL_FUNCTION_1       1  '1 positional argument'
             1430  LOAD_FAST                'self'
             1432  LOAD_ATTR                settings
             1434  LOAD_STR                 'secondary_eclipse'
             1436  STORE_SUBSCR     
             1438  JUMP_FORWARD       1450  'to 1450'
           1440_0  COME_FROM          1414  '1414'
           1440_1  COME_FROM          1398  '1398'

 L. 375      1440  LOAD_CONST               False
             1442  LOAD_FAST                'self'
             1444  LOAD_ATTR                settings
             1446  LOAD_STR                 'secondary_eclipse'
             1448  STORE_SUBSCR     
           1450_0  COME_FROM          1438  '1438'

 L. 381      1450  LOAD_STR                 'mcmc_pre_run_loops'
             1452  LOAD_FAST                'self'
             1454  LOAD_ATTR                settings
             1456  COMPARE_OP               not-in
         1458_1460  POP_JUMP_IF_FALSE  1472  'to 1472'

 L. 382      1462  LOAD_CONST               0
             1464  LOAD_FAST                'self'
             1466  LOAD_ATTR                settings
             1468  LOAD_STR                 'mcmc_pre_run_loops'
             1470  STORE_SUBSCR     
           1472_0  COME_FROM          1458  '1458'

 L. 383      1472  LOAD_STR                 'mcmc_pre_run_steps'
             1474  LOAD_FAST                'self'
             1476  LOAD_ATTR                settings
             1478  COMPARE_OP               not-in
         1480_1482  POP_JUMP_IF_FALSE  1494  'to 1494'

 L. 384      1484  LOAD_CONST               0
             1486  LOAD_FAST                'self'
             1488  LOAD_ATTR                settings
             1490  LOAD_STR                 'mcmc_pre_run_steps'
             1492  STORE_SUBSCR     
           1494_0  COME_FROM          1480  '1480'

 L. 385      1494  LOAD_STR                 'mcmc_nwalkers'
             1496  LOAD_FAST                'self'
             1498  LOAD_ATTR                settings
             1500  COMPARE_OP               not-in
         1502_1504  POP_JUMP_IF_FALSE  1516  'to 1516'

 L. 386      1506  LOAD_CONST               100
             1508  LOAD_FAST                'self'
             1510  LOAD_ATTR                settings
             1512  LOAD_STR                 'mcmc_nwalkers'
             1514  STORE_SUBSCR     
           1516_0  COME_FROM          1502  '1502'

 L. 387      1516  LOAD_STR                 'mcmc_total_steps'
             1518  LOAD_FAST                'self'
             1520  LOAD_ATTR                settings
             1522  COMPARE_OP               not-in
         1524_1526  POP_JUMP_IF_FALSE  1538  'to 1538'

 L. 388      1528  LOAD_CONST               2000
             1530  LOAD_FAST                'self'
             1532  LOAD_ATTR                settings
             1534  LOAD_STR                 'mcmc_total_steps'
             1536  STORE_SUBSCR     
           1538_0  COME_FROM          1524  '1524'

 L. 389      1538  LOAD_STR                 'mcmc_burn_steps'
             1540  LOAD_FAST                'self'
             1542  LOAD_ATTR                settings
             1544  COMPARE_OP               not-in
         1546_1548  POP_JUMP_IF_FALSE  1560  'to 1560'

 L. 390      1550  LOAD_CONST               1000
             1552  LOAD_FAST                'self'
             1554  LOAD_ATTR                settings
             1556  LOAD_STR                 'mcmc_burn_steps'
             1558  STORE_SUBSCR     
           1560_0  COME_FROM          1546  '1546'

 L. 391      1560  LOAD_STR                 'mcmc_thin_by'
             1562  LOAD_FAST                'self'
             1564  LOAD_ATTR                settings
             1566  COMPARE_OP               not-in
         1568_1570  POP_JUMP_IF_FALSE  1582  'to 1582'

 L. 392      1572  LOAD_CONST               1
             1574  LOAD_FAST                'self'
             1576  LOAD_ATTR                settings
             1578  LOAD_STR                 'mcmc_thin_by'
             1580  STORE_SUBSCR     
           1582_0  COME_FROM          1568  '1568'

 L. 394      1582  SETUP_LOOP         1618  'to 1618'
             1584  LOAD_CONST               ('mcmc_nwalkers', 'mcmc_pre_run_loops', 'mcmc_pre_run_steps', 'mcmc_total_steps', 'mcmc_burn_steps', 'mcmc_thin_by')
             1586  GET_ITER         
             1588  FOR_ITER           1616  'to 1616'
             1590  STORE_FAST               'key'

 L. 395      1592  LOAD_GLOBAL              int
             1594  LOAD_FAST                'self'
             1596  LOAD_ATTR                settings
             1598  LOAD_FAST                'key'
             1600  BINARY_SUBSCR    
             1602  CALL_FUNCTION_1       1  '1 positional argument'
             1604  LOAD_FAST                'self'
             1606  LOAD_ATTR                settings
             1608  LOAD_FAST                'key'
             1610  STORE_SUBSCR     
         1612_1614  JUMP_BACK          1588  'to 1588'
             1616  POP_BLOCK        
           1618_0  COME_FROM_LOOP     1582  '1582'

 L. 414      1618  LOAD_STR                 'ns_modus'
             1620  LOAD_FAST                'self'
             1622  LOAD_ATTR                settings
             1624  COMPARE_OP               not-in
         1626_1628  POP_JUMP_IF_FALSE  1640  'to 1640'

 L. 415      1630  LOAD_STR                 'static'
             1632  LOAD_FAST                'self'
             1634  LOAD_ATTR                settings
             1636  LOAD_STR                 'ns_modus'
             1638  STORE_SUBSCR     
           1640_0  COME_FROM          1626  '1626'

 L. 416      1640  LOAD_STR                 'ns_nlive'
             1642  LOAD_FAST                'self'
             1644  LOAD_ATTR                settings
             1646  COMPARE_OP               not-in
         1648_1650  POP_JUMP_IF_FALSE  1662  'to 1662'

 L. 417      1652  LOAD_CONST               500
             1654  LOAD_FAST                'self'
             1656  LOAD_ATTR                settings
             1658  LOAD_STR                 'ns_nlive'
             1660  STORE_SUBSCR     
           1662_0  COME_FROM          1648  '1648'

 L. 418      1662  LOAD_STR                 'ns_bound'
             1664  LOAD_FAST                'self'
             1666  LOAD_ATTR                settings
             1668  COMPARE_OP               not-in
         1670_1672  POP_JUMP_IF_FALSE  1684  'to 1684'

 L. 419      1674  LOAD_STR                 'single'
             1676  LOAD_FAST                'self'
             1678  LOAD_ATTR                settings
             1680  LOAD_STR                 'ns_bound'
             1682  STORE_SUBSCR     
           1684_0  COME_FROM          1670  '1670'

 L. 420      1684  LOAD_STR                 'ns_sample'
             1686  LOAD_FAST                'self'
             1688  LOAD_ATTR                settings
             1690  COMPARE_OP               not-in
         1692_1694  POP_JUMP_IF_FALSE  1706  'to 1706'

 L. 421      1696  LOAD_STR                 'rwalk'
             1698  LOAD_FAST                'self'
             1700  LOAD_ATTR                settings
             1702  LOAD_STR                 'ns_sample'
             1704  STORE_SUBSCR     
           1706_0  COME_FROM          1692  '1692'

 L. 422      1706  LOAD_STR                 'ns_tol'
             1708  LOAD_FAST                'self'
             1710  LOAD_ATTR                settings
             1712  COMPARE_OP               not-in
         1714_1716  POP_JUMP_IF_FALSE  1728  'to 1728'

 L. 423      1718  LOAD_CONST               0.01
             1720  LOAD_FAST                'self'
             1722  LOAD_ATTR                settings
             1724  LOAD_STR                 'ns_tol'
             1726  STORE_SUBSCR     
           1728_0  COME_FROM          1714  '1714'

 L. 425      1728  LOAD_GLOBAL              int
             1730  LOAD_FAST                'self'
             1732  LOAD_ATTR                settings
             1734  LOAD_STR                 'ns_nlive'
             1736  BINARY_SUBSCR    
             1738  CALL_FUNCTION_1       1  '1 positional argument'
             1740  LOAD_FAST                'self'
             1742  LOAD_ATTR                settings
             1744  LOAD_STR                 'ns_nlive'
             1746  STORE_SUBSCR     

 L. 426      1748  LOAD_GLOBAL              float
             1750  LOAD_FAST                'self'
             1752  LOAD_ATTR                settings
             1754  LOAD_STR                 'ns_tol'
             1756  BINARY_SUBSCR    
             1758  CALL_FUNCTION_1       1  '1 positional argument'
             1760  LOAD_FAST                'self'
             1762  LOAD_ATTR                settings
             1764  LOAD_STR                 'ns_tol'
             1766  STORE_SUBSCR     

 L. 443  1768_1770  SETUP_LOOP         2164  'to 2164'
             1772  LOAD_FAST                'self'
             1774  LOAD_ATTR                settings
             1776  LOAD_STR                 'companions_all'
             1778  BINARY_SUBSCR    
             1780  GET_ITER         
         1782_1784  FOR_ITER           2162  'to 2162'
             1786  STORE_FAST               'companion'

 L. 444  1788_1790  SETUP_LOOP         2158  'to 2158'
             1792  LOAD_FAST                'self'
             1794  LOAD_ATTR                settings
             1796  LOAD_STR                 'inst_all'
             1798  BINARY_SUBSCR    
             1800  GET_ITER         
           1802_0  COME_FROM          2130  '2130'
         1802_1804  FOR_ITER           2156  'to 2156'
             1806  STORE_FAST               'inst'

 L. 446      1808  LOAD_STR                 'host_grid_'
             1810  LOAD_FAST                'inst'
             1812  BINARY_ADD       
             1814  LOAD_FAST                'self'
             1816  LOAD_ATTR                settings
             1818  COMPARE_OP               not-in
         1820_1822  POP_JUMP_IF_FALSE  1838  'to 1838'

 L. 447      1824  LOAD_STR                 'default'
             1826  LOAD_FAST                'self'
             1828  LOAD_ATTR                settings
             1830  LOAD_STR                 'host_grid_'
             1832  LOAD_FAST                'inst'
             1834  BINARY_ADD       
             1836  STORE_SUBSCR     
           1838_0  COME_FROM          1820  '1820'

 L. 449      1838  LOAD_FAST                'companion'
             1840  LOAD_STR                 '_grid_'
             1842  BINARY_ADD       
             1844  LOAD_FAST                'inst'
             1846  BINARY_ADD       
             1848  LOAD_FAST                'self'
             1850  LOAD_ATTR                settings
             1852  COMPARE_OP               not-in
         1854_1856  POP_JUMP_IF_FALSE  1876  'to 1876'

 L. 450      1858  LOAD_STR                 'default'
             1860  LOAD_FAST                'self'
             1862  LOAD_ATTR                settings
             1864  LOAD_FAST                'companion'
             1866  LOAD_STR                 '_grid_'
             1868  BINARY_ADD       
             1870  LOAD_FAST                'inst'
             1872  BINARY_ADD       
             1874  STORE_SUBSCR     
           1876_0  COME_FROM          1854  '1854'

 L. 452      1876  LOAD_STR                 'host_ld_law_'
             1878  LOAD_FAST                'inst'
             1880  BINARY_ADD       
             1882  LOAD_FAST                'self'
             1884  LOAD_ATTR                settings
             1886  COMPARE_OP               not-in
         1888_1890  POP_JUMP_IF_TRUE   1956  'to 1956'
             1892  LOAD_FAST                'self'
             1894  LOAD_ATTR                settings
             1896  LOAD_STR                 'host_ld_law_'
             1898  LOAD_FAST                'inst'
             1900  BINARY_ADD       
             1902  BINARY_SUBSCR    
             1904  LOAD_CONST               None
             1906  COMPARE_OP               is
         1908_1910  POP_JUMP_IF_TRUE   1956  'to 1956'
             1912  LOAD_GLOBAL              len
             1914  LOAD_FAST                'self'
             1916  LOAD_ATTR                settings
             1918  LOAD_STR                 'host_ld_law_'
             1920  LOAD_FAST                'inst'
             1922  BINARY_ADD       
             1924  BINARY_SUBSCR    
             1926  CALL_FUNCTION_1       1  '1 positional argument'
             1928  LOAD_CONST               0
             1930  COMPARE_OP               ==
         1932_1934  POP_JUMP_IF_TRUE   1956  'to 1956'
             1936  LOAD_FAST                'self'
             1938  LOAD_ATTR                settings
             1940  LOAD_STR                 'host_ld_law_'
             1942  LOAD_FAST                'inst'
             1944  BINARY_ADD       
             1946  BINARY_SUBSCR    
             1948  LOAD_STR                 'None'
             1950  COMPARE_OP               ==
         1952_1954  POP_JUMP_IF_FALSE  1970  'to 1970'
           1956_0  COME_FROM          1932  '1932'
           1956_1  COME_FROM          1908  '1908'
           1956_2  COME_FROM          1888  '1888'

 L. 453      1956  LOAD_CONST               None
             1958  LOAD_FAST                'self'
             1960  LOAD_ATTR                settings
             1962  LOAD_STR                 'host_ld_law_'
             1964  LOAD_FAST                'inst'
             1966  BINARY_ADD       
             1968  STORE_SUBSCR     
           1970_0  COME_FROM          1952  '1952'

 L. 455      1970  LOAD_FAST                'companion'
             1972  LOAD_STR                 '_ld_law_'
             1974  BINARY_ADD       
             1976  LOAD_FAST                'inst'
             1978  BINARY_ADD       
             1980  LOAD_FAST                'self'
             1982  LOAD_ATTR                settings
             1984  COMPARE_OP               not-in
         1986_1988  POP_JUMP_IF_TRUE   2066  'to 2066'
             1990  LOAD_FAST                'self'
             1992  LOAD_ATTR                settings
             1994  LOAD_FAST                'companion'
             1996  LOAD_STR                 '_ld_law_'
             1998  BINARY_ADD       
             2000  LOAD_FAST                'inst'
             2002  BINARY_ADD       
             2004  BINARY_SUBSCR    
             2006  LOAD_CONST               None
             2008  COMPARE_OP               is
         2010_2012  POP_JUMP_IF_TRUE   2066  'to 2066'
             2014  LOAD_GLOBAL              len
             2016  LOAD_FAST                'self'
             2018  LOAD_ATTR                settings
             2020  LOAD_FAST                'companion'
             2022  LOAD_STR                 '_ld_law_'
             2024  BINARY_ADD       
             2026  LOAD_FAST                'inst'
             2028  BINARY_ADD       
             2030  BINARY_SUBSCR    
             2032  CALL_FUNCTION_1       1  '1 positional argument'
             2034  LOAD_CONST               0
             2036  COMPARE_OP               ==
         2038_2040  POP_JUMP_IF_TRUE   2066  'to 2066'
             2042  LOAD_FAST                'self'
             2044  LOAD_ATTR                settings
             2046  LOAD_FAST                'companion'
             2048  LOAD_STR                 '_ld_law_'
             2050  BINARY_ADD       
             2052  LOAD_FAST                'inst'
             2054  BINARY_ADD       
             2056  BINARY_SUBSCR    
             2058  LOAD_STR                 'None'
             2060  COMPARE_OP               ==
         2062_2064  POP_JUMP_IF_FALSE  2084  'to 2084'
           2066_0  COME_FROM          2038  '2038'
           2066_1  COME_FROM          2010  '2010'
           2066_2  COME_FROM          1986  '1986'

 L. 456      2066  LOAD_CONST               None
             2068  LOAD_FAST                'self'
             2070  LOAD_ATTR                settings
             2072  LOAD_FAST                'companion'
             2074  LOAD_STR                 '_ld_law_'
             2076  BINARY_ADD       
             2078  LOAD_FAST                'inst'
             2080  BINARY_ADD       
             2082  STORE_SUBSCR     
           2084_0  COME_FROM          2062  '2062'

 L. 458      2084  LOAD_STR                 'host_shape_'
             2086  LOAD_FAST                'inst'
             2088  BINARY_ADD       
             2090  LOAD_FAST                'self'
             2092  LOAD_ATTR                settings
             2094  COMPARE_OP               not-in
         2096_2098  POP_JUMP_IF_FALSE  2114  'to 2114'

 L. 459      2100  LOAD_STR                 'sphere'
             2102  LOAD_FAST                'self'
             2104  LOAD_ATTR                settings
             2106  LOAD_STR                 'host_shape_'
             2108  LOAD_FAST                'inst'
             2110  BINARY_ADD       
             2112  STORE_SUBSCR     
           2114_0  COME_FROM          2096  '2096'

 L. 461      2114  LOAD_FAST                'companion'
             2116  LOAD_STR                 '_shape_'
             2118  BINARY_ADD       
             2120  LOAD_FAST                'inst'
             2122  BINARY_ADD       
             2124  LOAD_FAST                'self'
             2126  LOAD_ATTR                settings
             2128  COMPARE_OP               not-in
         2130_2132  POP_JUMP_IF_FALSE  1802  'to 1802'

 L. 462      2134  LOAD_STR                 'sphere'
             2136  LOAD_FAST                'self'
             2138  LOAD_ATTR                settings
             2140  LOAD_FAST                'companion'
             2142  LOAD_STR                 '_shape_'
             2144  BINARY_ADD       
             2146  LOAD_FAST                'inst'
             2148  BINARY_ADD       
             2150  STORE_SUBSCR     
         2152_2154  JUMP_BACK          1802  'to 1802'
             2156  POP_BLOCK        
           2158_0  COME_FROM_LOOP     1788  '1788'
         2158_2160  JUMP_BACK          1782  'to 1782'
             2162  POP_BLOCK        
           2164_0  COME_FROM_LOOP     1768  '1768'

 L. 465      2164  SETUP_LOOP         2284  'to 2284'
             2166  LOAD_FAST                'self'
             2168  LOAD_ATTR                settings
             2170  LOAD_STR                 'companions_rv'
             2172  BINARY_SUBSCR    
             2174  GET_ITER         
             2176  FOR_ITER           2282  'to 2282'
             2178  STORE_FAST               'companion'

 L. 466      2180  SETUP_LOOP         2278  'to 2278'
             2182  LOAD_FAST                'self'
             2184  LOAD_ATTR                settings
             2186  LOAD_STR                 'inst_rv'
             2188  BINARY_SUBSCR    
             2190  GET_ITER         
             2192  FOR_ITER           2276  'to 2276'
             2194  STORE_FAST               'inst'

 L. 467      2196  LOAD_FAST                'companion'
             2198  LOAD_STR                 '_flux_weighted_'
             2200  BINARY_ADD       
             2202  LOAD_FAST                'inst'
             2204  BINARY_ADD       
             2206  LOAD_FAST                'self'
             2208  LOAD_ATTR                settings
             2210  COMPARE_OP               in
         2212_2214  POP_JUMP_IF_FALSE  2254  'to 2254'

 L. 468      2216  LOAD_FAST                'set_bool'
             2218  LOAD_FAST                'self'
             2220  LOAD_ATTR                settings
             2222  LOAD_FAST                'companion'
             2224  LOAD_STR                 '_flux_weighted_'
             2226  BINARY_ADD       
             2228  LOAD_FAST                'inst'
             2230  BINARY_ADD       
             2232  BINARY_SUBSCR    
             2234  CALL_FUNCTION_1       1  '1 positional argument'
             2236  LOAD_FAST                'self'
             2238  LOAD_ATTR                settings
             2240  LOAD_FAST                'companion'
             2242  LOAD_STR                 '_flux_weighted_'
             2244  BINARY_ADD       
             2246  LOAD_FAST                'inst'
             2248  BINARY_ADD       
             2250  STORE_SUBSCR     
             2252  JUMP_BACK          2192  'to 2192'
           2254_0  COME_FROM          2212  '2212'

 L. 470      2254  LOAD_CONST               False
             2256  LOAD_FAST                'self'
             2258  LOAD_ATTR                settings
             2260  LOAD_FAST                'companion'
             2262  LOAD_STR                 '_flux_weighted_'
             2264  BINARY_ADD       
             2266  LOAD_FAST                'inst'
             2268  BINARY_ADD       
             2270  STORE_SUBSCR     
         2272_2274  JUMP_BACK          2192  'to 2192'
             2276  POP_BLOCK        
           2278_0  COME_FROM_LOOP     2180  '2180'
         2278_2280  JUMP_BACK          2176  'to 2176'
             2282  POP_BLOCK        
           2284_0  COME_FROM_LOOP     2164  '2164'

 L. 473      2284  LOAD_STR                 'exact_grav'
             2286  LOAD_FAST                'self'
             2288  LOAD_ATTR                settings
             2290  COMPARE_OP               in
         2292_2294  POP_JUMP_IF_FALSE  2318  'to 2318'

 L. 474      2296  LOAD_FAST                'set_bool'
             2298  LOAD_FAST                'self'
             2300  LOAD_ATTR                settings
             2302  LOAD_STR                 'exact_grav'
             2304  BINARY_SUBSCR    
             2306  CALL_FUNCTION_1       1  '1 positional argument'
             2308  LOAD_FAST                'self'
             2310  LOAD_ATTR                settings
             2312  LOAD_STR                 'exact_grav'
             2314  STORE_SUBSCR     
             2316  JUMP_FORWARD       2328  'to 2328'
           2318_0  COME_FROM          2292  '2292'

 L. 476      2318  LOAD_CONST               False
             2320  LOAD_FAST                'self'
             2322  LOAD_ATTR                settings
             2324  LOAD_STR                 'exact_grav'
             2326  STORE_SUBSCR     
           2328_0  COME_FROM          2316  '2316'

 L. 482      2328  SETUP_LOOP         2418  'to 2418'
             2330  LOAD_CONST               ('flux', 'rv')
             2332  GET_ITER         
           2334_0  COME_FROM          2394  '2394'
             2334  FOR_ITER           2416  'to 2416'
             2336  STORE_FAST               'key'

 L. 483      2338  LOAD_STR                 'stellar_var_'
             2340  LOAD_FAST                'key'
             2342  BINARY_ADD       
             2344  LOAD_FAST                'self'
             2346  LOAD_ATTR                settings
             2348  COMPARE_OP               not-in
         2350_2352  POP_JUMP_IF_TRUE   2398  'to 2398'
             2354  LOAD_FAST                'self'
             2356  LOAD_ATTR                settings
             2358  LOAD_STR                 'stellar_var_'
             2360  LOAD_FAST                'key'
             2362  BINARY_ADD       
             2364  BINARY_SUBSCR    
             2366  LOAD_CONST               None
             2368  COMPARE_OP               is
         2370_2372  POP_JUMP_IF_TRUE   2398  'to 2398'
             2374  LOAD_FAST                'self'
             2376  LOAD_ATTR                settings
             2378  LOAD_STR                 'stellar_var_'
             2380  LOAD_FAST                'key'
             2382  BINARY_ADD       
             2384  BINARY_SUBSCR    
             2386  LOAD_METHOD              lower
             2388  CALL_METHOD_0         0  '0 positional arguments'
             2390  LOAD_STR                 'none'
             2392  COMPARE_OP               ==
         2394_2396  POP_JUMP_IF_FALSE  2334  'to 2334'
           2398_0  COME_FROM          2370  '2370'
           2398_1  COME_FROM          2350  '2350'

 L. 484      2398  LOAD_STR                 'none'
             2400  LOAD_FAST                'self'
             2402  LOAD_ATTR                settings
             2404  LOAD_STR                 'stellar_var_'
             2406  LOAD_FAST                'key'
             2408  BINARY_ADD       
             2410  STORE_SUBSCR     
         2412_2414  JUMP_BACK          2334  'to 2334'
             2416  POP_BLOCK        
           2418_0  COME_FROM_LOOP     2328  '2328'

 L. 490      2418  SETUP_LOOP         2564  'to 2564'
             2420  LOAD_FAST                'self'
             2422  LOAD_ATTR                settings
             2424  LOAD_STR                 'inst_phot'
             2426  BINARY_SUBSCR    
             2428  GET_ITER         
             2430  FOR_ITER           2562  'to 2562'
             2432  STORE_FAST               'inst'

 L. 491      2434  SETUP_LOOP         2558  'to 2558'
             2436  LOAD_CONST               ('flux',)
             2438  GET_ITER         
           2440_0  COME_FROM          2516  '2516'
             2440  FOR_ITER           2556  'to 2556'
             2442  STORE_FAST               'key'

 L. 492      2444  LOAD_STR                 'baseline_'
             2446  LOAD_FAST                'key'
             2448  BINARY_ADD       
             2450  LOAD_STR                 '_'
             2452  BINARY_ADD       
             2454  LOAD_FAST                'inst'
             2456  BINARY_ADD       
             2458  LOAD_FAST                'self'
             2460  LOAD_ATTR                settings
             2462  COMPARE_OP               not-in
         2464_2466  POP_JUMP_IF_FALSE  2492  'to 2492'

 L. 493      2468  LOAD_STR                 'none'
             2470  LOAD_FAST                'self'
             2472  LOAD_ATTR                settings
             2474  LOAD_STR                 'baseline_'
             2476  LOAD_FAST                'key'
             2478  BINARY_ADD       
             2480  LOAD_STR                 '_'
             2482  BINARY_ADD       
             2484  LOAD_FAST                'inst'
             2486  BINARY_ADD       
             2488  STORE_SUBSCR     
             2490  JUMP_BACK          2440  'to 2440'
           2492_0  COME_FROM          2464  '2464'

 L. 495      2492  LOAD_FAST                'self'
             2494  LOAD_ATTR                settings
             2496  LOAD_STR                 'baseline_'
             2498  LOAD_FAST                'key'
             2500  BINARY_ADD       
             2502  LOAD_STR                 '_'
             2504  BINARY_ADD       
             2506  LOAD_FAST                'inst'
             2508  BINARY_ADD       
             2510  BINARY_SUBSCR    
             2512  LOAD_STR                 'sample_GP'
             2514  COMPARE_OP               ==
         2516_2518  POP_JUMP_IF_FALSE  2440  'to 2440'

 L. 496      2520  LOAD_GLOBAL              warnings
             2522  LOAD_METHOD              warn
             2524  LOAD_STR                 'Deprecation warning. You are using outdated keywords. Automatically renaming sample_GP ---> sample_GP_Matern32.'
             2526  CALL_METHOD_1         1  '1 positional argument'
             2528  POP_TOP          

 L. 497      2530  LOAD_STR                 'sample_GP_Matern32'
             2532  LOAD_FAST                'self'
             2534  LOAD_ATTR                settings
             2536  LOAD_STR                 'baseline_'
             2538  LOAD_FAST                'key'
             2540  BINARY_ADD       
             2542  LOAD_STR                 '_'
             2544  BINARY_ADD       
             2546  LOAD_FAST                'inst'
             2548  BINARY_ADD       
             2550  STORE_SUBSCR     
         2552_2554  JUMP_BACK          2440  'to 2440'
             2556  POP_BLOCK        
           2558_0  COME_FROM_LOOP     2434  '2434'
         2558_2560  JUMP_BACK          2430  'to 2430'
             2562  POP_BLOCK        
           2564_0  COME_FROM_LOOP     2418  '2418'

 L. 499      2564  SETUP_LOOP         2710  'to 2710'
             2566  LOAD_FAST                'self'
             2568  LOAD_ATTR                settings
             2570  LOAD_STR                 'inst_rv'
             2572  BINARY_SUBSCR    
             2574  GET_ITER         
             2576  FOR_ITER           2708  'to 2708'
             2578  STORE_FAST               'inst'

 L. 500      2580  SETUP_LOOP         2704  'to 2704'
             2582  LOAD_CONST               ('rv',)
             2584  GET_ITER         
           2586_0  COME_FROM          2662  '2662'
             2586  FOR_ITER           2702  'to 2702'
             2588  STORE_FAST               'key'

 L. 501      2590  LOAD_STR                 'baseline_'
             2592  LOAD_FAST                'key'
             2594  BINARY_ADD       
             2596  LOAD_STR                 '_'
             2598  BINARY_ADD       
             2600  LOAD_FAST                'inst'
             2602  BINARY_ADD       
             2604  LOAD_FAST                'self'
             2606  LOAD_ATTR                settings
             2608  COMPARE_OP               not-in
         2610_2612  POP_JUMP_IF_FALSE  2638  'to 2638'

 L. 502      2614  LOAD_STR                 'none'
             2616  LOAD_FAST                'self'
             2618  LOAD_ATTR                settings
             2620  LOAD_STR                 'baseline_'
             2622  LOAD_FAST                'key'
             2624  BINARY_ADD       
             2626  LOAD_STR                 '_'
             2628  BINARY_ADD       
             2630  LOAD_FAST                'inst'
             2632  BINARY_ADD       
             2634  STORE_SUBSCR     
             2636  JUMP_BACK          2586  'to 2586'
           2638_0  COME_FROM          2610  '2610'

 L. 504      2638  LOAD_FAST                'self'
             2640  LOAD_ATTR                settings
             2642  LOAD_STR                 'baseline_'
             2644  LOAD_FAST                'key'
             2646  BINARY_ADD       
             2648  LOAD_STR                 '_'
             2650  BINARY_ADD       
             2652  LOAD_FAST                'inst'
             2654  BINARY_ADD       
             2656  BINARY_SUBSCR    
             2658  LOAD_STR                 'sample_GP'
             2660  COMPARE_OP               ==
         2662_2664  POP_JUMP_IF_FALSE  2586  'to 2586'

 L. 505      2666  LOAD_GLOBAL              warnings
             2668  LOAD_METHOD              warn
             2670  LOAD_STR                 'Deprecation warning. You are using outdated keywords. Automatically renaming sample_GP ---> sample_GP_Matern32.'
             2672  CALL_METHOD_1         1  '1 positional argument'
             2674  POP_TOP          

 L. 506      2676  LOAD_STR                 'sample_GP_Matern32'
             2678  LOAD_FAST                'self'
             2680  LOAD_ATTR                settings
             2682  LOAD_STR                 'baseline_'
             2684  LOAD_FAST                'key'
             2686  BINARY_ADD       
             2688  LOAD_STR                 '_'
             2690  BINARY_ADD       
             2692  LOAD_FAST                'inst'
             2694  BINARY_ADD       
             2696  STORE_SUBSCR     
         2698_2700  JUMP_BACK          2586  'to 2586'
             2702  POP_BLOCK        
           2704_0  COME_FROM_LOOP     2580  '2580'
         2704_2706  JUMP_BACK          2576  'to 2576'
             2708  POP_BLOCK        
           2710_0  COME_FROM_LOOP     2564  '2564'

 L. 512      2710  SETUP_LOOP         2794  'to 2794'
             2712  LOAD_FAST                'self'
             2714  LOAD_ATTR                settings
             2716  LOAD_STR                 'inst_phot'
             2718  BINARY_SUBSCR    
             2720  GET_ITER         
             2722  FOR_ITER           2792  'to 2792'
             2724  STORE_FAST               'inst'

 L. 513      2726  SETUP_LOOP         2788  'to 2788'
             2728  LOAD_CONST               ('flux',)
             2730  GET_ITER         
           2732_0  COME_FROM          2756  '2756'
             2732  FOR_ITER           2786  'to 2786'
             2734  STORE_FAST               'key'

 L. 514      2736  LOAD_STR                 'error_'
             2738  LOAD_FAST                'key'
             2740  BINARY_ADD       
             2742  LOAD_STR                 '_'
             2744  BINARY_ADD       
             2746  LOAD_FAST                'inst'
             2748  BINARY_ADD       
             2750  LOAD_FAST                'self'
             2752  LOAD_ATTR                settings
             2754  COMPARE_OP               not-in
         2756_2758  POP_JUMP_IF_FALSE  2732  'to 2732'

 L. 515      2760  LOAD_STR                 'sample'
             2762  LOAD_FAST                'self'
             2764  LOAD_ATTR                settings
             2766  LOAD_STR                 'error_'
             2768  LOAD_FAST                'key'
             2770  BINARY_ADD       
             2772  LOAD_STR                 '_'
             2774  BINARY_ADD       
             2776  LOAD_FAST                'inst'
             2778  BINARY_ADD       
             2780  STORE_SUBSCR     
         2782_2784  JUMP_BACK          2732  'to 2732'
             2786  POP_BLOCK        
           2788_0  COME_FROM_LOOP     2726  '2726'
         2788_2790  JUMP_BACK          2722  'to 2722'
             2792  POP_BLOCK        
           2794_0  COME_FROM_LOOP     2710  '2710'

 L. 517      2794  SETUP_LOOP         2878  'to 2878'
             2796  LOAD_FAST                'self'
             2798  LOAD_ATTR                settings
             2800  LOAD_STR                 'inst_rv'
             2802  BINARY_SUBSCR    
             2804  GET_ITER         
             2806  FOR_ITER           2876  'to 2876'
             2808  STORE_FAST               'inst'

 L. 518      2810  SETUP_LOOP         2872  'to 2872'
             2812  LOAD_CONST               ('rv',)
             2814  GET_ITER         
           2816_0  COME_FROM          2840  '2840'
             2816  FOR_ITER           2870  'to 2870'
             2818  STORE_FAST               'key'

 L. 519      2820  LOAD_STR                 'error_'
             2822  LOAD_FAST                'key'
             2824  BINARY_ADD       
             2826  LOAD_STR                 '_'
             2828  BINARY_ADD       
             2830  LOAD_FAST                'inst'
             2832  BINARY_ADD       
             2834  LOAD_FAST                'self'
             2836  LOAD_ATTR                settings
             2838  COMPARE_OP               not-in
         2840_2842  POP_JUMP_IF_FALSE  2816  'to 2816'

 L. 520      2844  LOAD_STR                 'sample'
             2846  LOAD_FAST                'self'
             2848  LOAD_ATTR                settings
             2850  LOAD_STR                 'error_'
             2852  LOAD_FAST                'key'
             2854  BINARY_ADD       
             2856  LOAD_STR                 '_'
             2858  BINARY_ADD       
             2860  LOAD_FAST                'inst'
             2862  BINARY_ADD       
             2864  STORE_SUBSCR     
         2866_2868  JUMP_BACK          2816  'to 2816'
             2870  POP_BLOCK        
           2872_0  COME_FROM_LOOP     2810  '2810'
         2872_2874  JUMP_BACK          2806  'to 2806'
             2876  POP_BLOCK        
           2878_0  COME_FROM_LOOP     2794  '2794'

 L. 526      2878  LOAD_STR                 'color_plot'
             2880  LOAD_FAST                'self'
             2882  LOAD_ATTR                settings
             2884  LOAD_METHOD              keys
             2886  CALL_METHOD_0         0  '0 positional arguments'
             2888  COMPARE_OP               not-in
         2890_2892  POP_JUMP_IF_FALSE  2904  'to 2904'

 L. 527      2894  LOAD_CONST               False
             2896  LOAD_FAST                'self'
             2898  LOAD_ATTR                settings
             2900  LOAD_STR                 'color_plot'
             2902  STORE_SUBSCR     
           2904_0  COME_FROM          2890  '2890'

 L. 534      2904  SETUP_LOOP         2956  'to 2956'
             2906  LOAD_GLOBAL              enumerate
             2908  LOAD_FAST                'self'
             2910  LOAD_ATTR                settings
             2912  LOAD_STR                 'companions_all'
             2914  BINARY_SUBSCR    
             2916  CALL_FUNCTION_1       1  '1 positional argument'
             2918  GET_ITER         
             2920  FOR_ITER           2954  'to 2954'
             2922  UNPACK_SEQUENCE_2     2 
             2924  STORE_FAST               'i'
             2926  STORE_FAST               'companion'

 L. 535      2928  LOAD_GLOBAL              sns
             2930  LOAD_METHOD              color_palette
             2932  CALL_METHOD_0         0  '0 positional arguments'
             2934  LOAD_FAST                'i'
             2936  BINARY_SUBSCR    
             2938  LOAD_FAST                'self'
             2940  LOAD_ATTR                settings
             2942  LOAD_FAST                'companion'
             2944  LOAD_STR                 '_color'
             2946  BINARY_ADD       
             2948  STORE_SUBSCR     
         2950_2952  JUMP_BACK          2920  'to 2920'
             2954  POP_BLOCK        
           2956_0  COME_FROM_LOOP     2904  '2904'

 L. 541  2956_2958  SETUP_LOOP         3282  'to 3282'
             2960  LOAD_FAST                'self'
             2962  LOAD_ATTR                settings
             2964  LOAD_STR                 'inst_all'
             2966  BINARY_SUBSCR    
             2968  GET_ITER         
         2970_2972  FOR_ITER           3280  'to 3280'
             2974  STORE_FAST               'inst'

 L. 543      2976  LOAD_STR                 't_exp_'
             2978  LOAD_FAST                'inst'
             2980  BINARY_ADD       
             2982  LOAD_FAST                'self'
             2984  LOAD_ATTR                settings
             2986  LOAD_METHOD              keys
             2988  CALL_METHOD_0         0  '0 positional arguments'
             2990  COMPARE_OP               in
         2992_2994  POP_JUMP_IF_FALSE  3108  'to 3108'
             2996  LOAD_GLOBAL              len
             2998  LOAD_FAST                'self'
             3000  LOAD_ATTR                settings
             3002  LOAD_STR                 't_exp_'
             3004  LOAD_FAST                'inst'
             3006  BINARY_ADD       
             3008  BINARY_SUBSCR    
             3010  CALL_FUNCTION_1       1  '1 positional argument'
         3012_3014  POP_JUMP_IF_FALSE  3108  'to 3108'

 L. 544      3016  LOAD_FAST                'self'
             3018  LOAD_ATTR                settings
             3020  LOAD_STR                 't_exp_'
             3022  LOAD_FAST                'inst'
             3024  BINARY_ADD       
             3026  BINARY_SUBSCR    
             3028  LOAD_METHOD              split
             3030  LOAD_STR                 ' '
             3032  CALL_METHOD_1         1  '1 positional argument'
             3034  STORE_FAST               't_exp'

 L. 546      3036  LOAD_GLOBAL              len
             3038  LOAD_FAST                't_exp'
             3040  CALL_FUNCTION_1       1  '1 positional argument'
             3042  LOAD_CONST               1
             3044  COMPARE_OP               ==
         3046_3048  POP_JUMP_IF_FALSE  3076  'to 3076'

 L. 547      3050  LOAD_GLOBAL              np
             3052  LOAD_METHOD              float
             3054  LOAD_FAST                't_exp'
             3056  LOAD_CONST               0
             3058  BINARY_SUBSCR    
             3060  CALL_METHOD_1         1  '1 positional argument'
             3062  LOAD_FAST                'self'
             3064  LOAD_ATTR                settings
             3066  LOAD_STR                 't_exp_'
             3068  LOAD_FAST                'inst'
             3070  BINARY_ADD       
             3072  STORE_SUBSCR     
             3074  JUMP_FORWARD       3106  'to 3106'
           3076_0  COME_FROM          3046  '3046'

 L. 550      3076  LOAD_GLOBAL              np
             3078  LOAD_METHOD              array
             3080  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3082  LOAD_STR                 'Basement.load_settings.<locals>.<listcomp>'
             3084  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3086  LOAD_FAST                't_exp'
             3088  GET_ITER         
             3090  CALL_FUNCTION_1       1  '1 positional argument'
             3092  CALL_METHOD_1         1  '1 positional argument'
             3094  LOAD_FAST                'self'
             3096  LOAD_ATTR                settings
             3098  LOAD_STR                 't_exp_'
             3100  LOAD_FAST                'inst'
             3102  BINARY_ADD       
             3104  STORE_SUBSCR     
           3106_0  COME_FROM          3074  '3074'
             3106  JUMP_FORWARD       3122  'to 3122'
           3108_0  COME_FROM          3012  '3012'
           3108_1  COME_FROM          2992  '2992'

 L. 553      3108  LOAD_CONST               None
             3110  LOAD_FAST                'self'
             3112  LOAD_ATTR                settings
             3114  LOAD_STR                 't_exp_'
             3116  LOAD_FAST                'inst'
             3118  BINARY_ADD       
             3120  STORE_SUBSCR     
           3122_0  COME_FROM          3106  '3106'

 L. 556      3122  LOAD_STR                 't_exp_'
             3124  LOAD_FAST                'inst'
             3126  BINARY_ADD       
             3128  LOAD_FAST                'self'
             3130  LOAD_ATTR                settings
             3132  COMPARE_OP               in
         3134_3136  POP_JUMP_IF_FALSE  3262  'to 3262'

 L. 557      3138  LOAD_STR                 't_exp_n_int_'
             3140  LOAD_FAST                'inst'
             3142  BINARY_ADD       
             3144  LOAD_FAST                'self'
             3146  LOAD_ATTR                settings
             3148  COMPARE_OP               in
         3150_3152  POP_JUMP_IF_FALSE  3262  'to 3262'

 L. 558      3154  LOAD_GLOBAL              len
             3156  LOAD_FAST                'self'
             3158  LOAD_ATTR                settings
             3160  LOAD_STR                 't_exp_n_int_'
             3162  LOAD_FAST                'inst'
             3164  BINARY_ADD       
             3166  BINARY_SUBSCR    
             3168  CALL_FUNCTION_1       1  '1 positional argument'
         3170_3172  POP_JUMP_IF_FALSE  3262  'to 3262'

 L. 560      3174  LOAD_GLOBAL              int
             3176  LOAD_FAST                'self'
             3178  LOAD_ATTR                settings
             3180  LOAD_STR                 't_exp_n_int_'
             3182  LOAD_FAST                'inst'
             3184  BINARY_ADD       
             3186  BINARY_SUBSCR    
             3188  CALL_FUNCTION_1       1  '1 positional argument'
             3190  LOAD_FAST                'self'
             3192  LOAD_ATTR                settings
             3194  LOAD_STR                 't_exp_n_int_'
             3196  LOAD_FAST                'inst'
             3198  BINARY_ADD       
             3200  STORE_SUBSCR     

 L. 561      3202  LOAD_FAST                'self'
             3204  LOAD_ATTR                settings
             3206  LOAD_STR                 't_exp_n_int_'
             3208  LOAD_FAST                'inst'
             3210  BINARY_ADD       
             3212  BINARY_SUBSCR    
             3214  LOAD_CONST               1
             3216  COMPARE_OP               <
         3218_3220  POP_JUMP_IF_FALSE  3276  'to 3276'

 L. 562      3222  LOAD_GLOBAL              ValueError
             3224  LOAD_STR                 '"t_exp_n_int_'
             3226  LOAD_FAST                'inst'
             3228  BINARY_ADD       
             3230  LOAD_STR                 '" must be >= 1, but is given as '
             3232  BINARY_ADD       
             3234  LOAD_GLOBAL              str
             3236  LOAD_FAST                'self'
             3238  LOAD_ATTR                settings
             3240  LOAD_STR                 't_exp_n_int_'
             3242  LOAD_FAST                'inst'
             3244  BINARY_ADD       
             3246  BINARY_SUBSCR    
             3248  CALL_FUNCTION_1       1  '1 positional argument'
             3250  BINARY_ADD       
             3252  LOAD_STR                 ' in params.csv'
             3254  BINARY_ADD       
             3256  CALL_FUNCTION_1       1  '1 positional argument'
             3258  RAISE_VARARGS_1       1  'exception instance'
             3260  JUMP_BACK          2970  'to 2970'
           3262_0  COME_FROM          3170  '3170'
           3262_1  COME_FROM          3150  '3150'
           3262_2  COME_FROM          3134  '3134'

 L. 564      3262  LOAD_CONST               None
             3264  LOAD_FAST                'self'
             3266  LOAD_ATTR                settings
             3268  LOAD_STR                 't_exp_n_int_'
             3270  LOAD_FAST                'inst'
             3272  BINARY_ADD       
             3274  STORE_SUBSCR     
           3276_0  COME_FROM          3218  '3218'
         3276_3278  JUMP_BACK          2970  'to 2970'
             3280  POP_BLOCK        
           3282_0  COME_FROM_LOOP     2956  '2956'

 L. 570      3282  SETUP_LOOP         3482  'to 3482'
             3284  LOAD_FAST                'self'
             3286  LOAD_ATTR                settings
             3288  LOAD_STR                 'inst_all'
             3290  BINARY_SUBSCR    
             3292  GET_ITER         
             3294  FOR_ITER           3480  'to 3480'
             3296  STORE_FAST               'inst'

 L. 571      3298  LOAD_STR                 'host_N_spots_'
             3300  LOAD_FAST                'inst'
             3302  BINARY_ADD       
             3304  LOAD_FAST                'self'
             3306  LOAD_ATTR                settings
             3308  COMPARE_OP               in
         3310_3312  POP_JUMP_IF_FALSE  3364  'to 3364'
             3314  LOAD_GLOBAL              len
             3316  LOAD_FAST                'self'
             3318  LOAD_ATTR                settings
             3320  LOAD_STR                 'host_N_spots_'
             3322  LOAD_FAST                'inst'
             3324  BINARY_ADD       
             3326  BINARY_SUBSCR    
             3328  CALL_FUNCTION_1       1  '1 positional argument'
         3330_3332  POP_JUMP_IF_FALSE  3364  'to 3364'

 L. 572      3334  LOAD_GLOBAL              int
             3336  LOAD_FAST                'self'
             3338  LOAD_ATTR                settings
             3340  LOAD_STR                 'host_N_spots_'
             3342  LOAD_FAST                'inst'
             3344  BINARY_ADD       
             3346  BINARY_SUBSCR    
             3348  CALL_FUNCTION_1       1  '1 positional argument'
             3350  LOAD_FAST                'self'
             3352  LOAD_ATTR                settings
             3354  LOAD_STR                 'host_N_spots_'
             3356  LOAD_FAST                'inst'
             3358  BINARY_ADD       
             3360  STORE_SUBSCR     
             3362  JUMP_FORWARD       3378  'to 3378'
           3364_0  COME_FROM          3330  '3330'
           3364_1  COME_FROM          3310  '3310'

 L. 574      3364  LOAD_CONST               0
             3366  LOAD_FAST                'self'
             3368  LOAD_ATTR                settings
             3370  LOAD_STR                 'host_N_spots_'
             3372  LOAD_FAST                'inst'
             3374  BINARY_ADD       
             3376  STORE_SUBSCR     
           3378_0  COME_FROM          3362  '3362'

 L. 576      3378  SETUP_LOOP         3476  'to 3476'
             3380  LOAD_FAST                'self'
             3382  LOAD_ATTR                settings
             3384  LOAD_STR                 'companions_all'
             3386  BINARY_SUBSCR    
             3388  GET_ITER         
             3390  FOR_ITER           3474  'to 3474'
             3392  STORE_FAST               'companion'

 L. 577      3394  LOAD_FAST                'companion'
             3396  LOAD_STR                 '_N_spots'
             3398  BINARY_ADD       
             3400  LOAD_FAST                'inst'
             3402  BINARY_ADD       
             3404  LOAD_FAST                'self'
             3406  LOAD_ATTR                settings
             3408  COMPARE_OP               in
         3410_3412  POP_JUMP_IF_FALSE  3452  'to 3452'

 L. 578      3414  LOAD_GLOBAL              int
             3416  LOAD_FAST                'self'
             3418  LOAD_ATTR                settings
             3420  LOAD_FAST                'companion'
             3422  LOAD_STR                 '_N_spots_'
             3424  BINARY_ADD       
             3426  LOAD_FAST                'inst'
             3428  BINARY_ADD       
             3430  BINARY_SUBSCR    
             3432  CALL_FUNCTION_1       1  '1 positional argument'
             3434  LOAD_FAST                'self'
             3436  LOAD_ATTR                settings
             3438  LOAD_FAST                'companion'
             3440  LOAD_STR                 '_N_spots_'
             3442  BINARY_ADD       
             3444  LOAD_FAST                'inst'
             3446  BINARY_ADD       
             3448  STORE_SUBSCR     
             3450  JUMP_BACK          3390  'to 3390'
           3452_0  COME_FROM          3410  '3410'

 L. 580      3452  LOAD_CONST               0
             3454  LOAD_FAST                'self'
             3456  LOAD_ATTR                settings
             3458  LOAD_FAST                'companion'
             3460  LOAD_STR                 '_N_spots_'
             3462  BINARY_ADD       
             3464  LOAD_FAST                'inst'
             3466  BINARY_ADD       
             3468  STORE_SUBSCR     
         3470_3472  JUMP_BACK          3390  'to 3390'
             3474  POP_BLOCK        
           3476_0  COME_FROM_LOOP     3378  '3378'
         3476_3478  JUMP_BACK          3294  'to 3294'
             3480  POP_BLOCK        
           3482_0  COME_FROM_LOOP     3282  '3282'

 L. 586      3482  LOAD_STR                 'N_flares'
             3484  LOAD_FAST                'self'
             3486  LOAD_ATTR                settings
             3488  COMPARE_OP               in
         3490_3492  POP_JUMP_IF_FALSE  3536  'to 3536'
             3494  LOAD_GLOBAL              len
             3496  LOAD_FAST                'self'
             3498  LOAD_ATTR                settings
             3500  LOAD_STR                 'N_flares'
             3502  BINARY_SUBSCR    
             3504  CALL_FUNCTION_1       1  '1 positional argument'
             3506  LOAD_CONST               0
             3508  COMPARE_OP               >
         3510_3512  POP_JUMP_IF_FALSE  3536  'to 3536'

 L. 587      3514  LOAD_GLOBAL              int
             3516  LOAD_FAST                'self'
             3518  LOAD_ATTR                settings
             3520  LOAD_STR                 'N_flares'
             3522  BINARY_SUBSCR    
             3524  CALL_FUNCTION_1       1  '1 positional argument'
             3526  LOAD_FAST                'self'
             3528  LOAD_ATTR                settings
             3530  LOAD_STR                 'N_flares'
             3532  STORE_SUBSCR     
             3534  JUMP_FORWARD       3546  'to 3546'
           3536_0  COME_FROM          3510  '3510'
           3536_1  COME_FROM          3490  '3490'

 L. 589      3536  LOAD_CONST               0
             3538  LOAD_FAST                'self'
             3540  LOAD_ATTR                settings
             3542  LOAD_STR                 'N_flares'
             3544  STORE_SUBSCR     
           3546_0  COME_FROM          3534  '3534'

Parse error at or near `COME_FROM' instruction at offset 1970_0

    def load_params(self):
        r"""
        #name   value   fit     bounds  label   unit
        #b_: companion name; _key : flux/rv/centd; _inst : instrument name                                      
        #dilution per instrument                                        
        dil_TESS        0       0       none    $D_\mathrm{TESS}$       
        dil_HATS        0.14    1       trunc_normal 0 1 0.14 0.1       $D_\mathrm{HATS}$       
        dil_FTS_i       0       0       none    $D_\mathrm{FTS_i}$      
        dil_GROND_g     0       0       none    $D_\mathrm{GROND_g}$    
        dil_GROND_r     0       0       none    $D_\mathrm{GROND_r}$    
        dil_GROND_i     0       0       none    $D_\mathrm{GROND_i}$    
        dil_GROND_z     0       0       none    $D_\mathrm{GROND_i}$    
        #limb darkening coefficients per instrument                                     
        ldc_q1_TESS     0.5     1       uniform 0 1     $q_{1;\mathrm{TESS}}$   
        ldc_q2_TESS     0.5     1       uniform 0 1     $q_{1;\mathrm{TESS}}$   
        ldc_q1_HATS     0.5     1       uniform 0 1     $q_{1;\mathrm{HATS}}$   
        ldc_q2_HATS     0.5     1       uniform 0 1     $q_{2;\mathrm{HATS}}$   
        ldc_q1_FTS_i    0.5     1       uniform 0 1     $q_{1;\mathrm{FTS_i}}$  
        ldc_q2_FTS_i    0.5     1       uniform 0 1     $q_{2;\mathrm{FTS_i}}$  
        ldc_q1_GROND_g  0.5     1       uniform 0 1     $q_{1;\mathrm{GROND_g}}$        
        ldc_q2_GROND_g  0.5     1       uniform 0 1     $q_{2;\mathrm{GROND_g}}$        
        ldc_q1_GROND_r  0.5     1       uniform 0 1     $q_{1;\mathrm{GROND_r}}$        
        ldc_q2_GROND_r  0.5     1       uniform 0 1     $q_{2;\mathrm{GROND_r}}$        
        ldc_q1_GROND_i  0.5     1       uniform 0 1     $q_{1;\mathrm{GROND_i}}$        
        ldc_q2_GROND_i  0.5     1       uniform 0 1     $q_{2;\mathrm{GROND_i}}$        
        ldc_q1_GROND_z  0.5     1       uniform 0 1     $q_{1;\mathrm{GROND_z}}$        
        ldc_q2_GROND_z  0.5     1       uniform 0 1     $q_{2;\mathrm{GROND_z}}$        
        #brightness per instrument per companion                                        
        b_sbratio_TESS  0       0       none    $J_{b;\mathrm{TESS}}$   
        b_sbratio_HATS  0       0       none    $J_{b;\mathrm{HATS}}$   
        b_sbratio_FTS_i 0       0       none    $J_{b;\mathrm{FTS_i}}$  
        b_sbratio_GROND_g       0       0       none    $J_{b;\mathrm{GROND_g}}$        
        b_sbratio_GROND_r       0       0       none    $J_{b;\mathrm{GROND_r}}$        
        b_sbratio_GROND_i       0       0       none    $J_{b;\mathrm{GROND_i}}$        
        b_sbratio_GROND_z       0       0       none    $J_{b;\mathrm{GROND_z}}$        
        #companion b astrophysical params                                       
        b_rsuma 0.178   1       trunc_normal 0 1 0.178 0.066    $(R_\star + R_b) / a_b$ 
        b_rr    0.1011  1       trunc_normal 0 1 0.1011 0.0018  $R_b / R_\star$ 
        b_cosi  0.099   1       trunc_normal 0 1 0.099 0.105    $\cos{i_b}$     
        b_epoch 2456155.967     1       trunc_normal 0 1e12 2456155.96734 0.00042       $T_{0;b}$       $\mathrm{BJD}$
        b_period        3.547851        1       trunc_normal 0 1e12 3.547851 1.5e-5     $P_b$   $\mathrm{d}$
        b_K     0.1257  1       trunc_normal 0 1 0.1257 0.0471  $K_b$   $\mathrm{km/s}$
        b_q     1       0       none    $M_b / M_\star$ 
        b_f_c   0       0       none    $\sqrt{e_b} \cos{\omega_b}$     
        b_f_s   0       0       none    $\sqrt{e_b} \sin{\omega_b}$     
        #TTVs                                   
        ...
        #Period changes                                 
        b_pv_TESS       0       0       trunc_normal -0.04 0.04 0 0.0007        $PV_\mathrm{TESS}$      $\mathrm{d}$
        b_pv_HATS       0       0       trunc_normal -0.04 0.04 0 0.0007        $PV_\mathrm{HATS}$      $\mathrm{d}$
        b_pv_FTS_i      0       0       trunc_normal -0.04 0.04 0 0.0007        $PV_\mathrm{FTS_i}$     $\mathrm{d}$
        b_pv_GROND_g    0       0       trunc_normal -0.04 0.04 0 0.0007        $PV_\mathrm{GROND_g}$   $\mathrm{d}$
        b_pv_GROND_r    0       0       trunc_normal -0.04 0.04 0 0.0007        $PV_\mathrm{GROND_r}$   $\mathrm{d}$
        b_pv_GROND_i    0       0       trunc_normal -0.04 0.04 0 0.0007        $PV_\mathrm{GROND_i}$   $\mathrm{d}$
        b_pv_GROND_z    0       0       trunc_normal -0.04 0.04 0 0.0007        $PV_\mathrm{GROND_i}$   $\mathrm{d}$
        #errors (overall scaling) per instrument                                        
        log_err_flux_TESS       -5.993  1       trunc_normal -23 0 -5.993 0.086 $\log{\sigma} (F_\mathrm{TESS})$        $\log{\mathrm{(rel. flux)}}$
        log_err_flux_HATS       -4.972  1       trunc_normal -23 0 -4.972 0.099 $\log{\sigma} (F_\mathrm{HATS})$        $\log{\mathrm{(rel. flux)}}$
        log_err_flux_FTS_i      -6      1       trunc_normal -23 0 -6.0 0.19    $\log{\sigma} (F_\mathrm{FTS_i})$       $\log{\mathrm{(rel. flux)}}$
        log_err_flux_GROND_g    -7.2    1       trunc_normal -23 0 -7.20 0.26   $\log{\sigma} (F_\mathrm{GROND_g})$     $\log{\mathrm{(rel. flux)}}$
        log_err_flux_GROND_r    -7.49   1       trunc_normal -23 0 -7.49 0.26   $\log{\sigma} (F_\mathrm{GROND_r})$     $\log{\mathrm{(rel. flux)}}$
        log_err_flux_GROND_i    -7.47   1       trunc_normal -23 0 -7.47 0.28   $\log{\sigma} (F_\mathrm{GROND_i})$     $\log{\mathrm{(rel. flux)}}$
        log_err_flux_GROND_z    -7.09   1       trunc_normal -23 0 -7.09 0.27   $\log{\sigma} (F_\mathrm{GROND_z})$     $\log{\mathrm{(rel. flux)}}$
        log_jitter_rv_AAT       -2.7    1       trunc_normal -23 0 -2.7 1.8     $\log{\sigma_\mathrm{jitter}} (RV_\mathrm{AAT})$        $\log{\mathrm{km/s}}$
        log_jitter_rv_Coralie   -2.7    1       trunc_normal -23 0 -2.7 1.5     $\log{\sigma_\mathrm{jitter}} (RV_\mathrm{Coralie})$    $\log{\mathrm{km/s}}$
        log_jitter_rv_FEROS     -5      1       trunc_normal -23 0 -5 15        $\log{\sigma_\mathrm{jitter}} (RV_\mathrm{FEROS})$      $\log{\mathrm{km/s}}$
        """
        buf = np.genfromtxt((os.path.join(self.datadir, 'params.csv')), delimiter=',', comments='#', dtype=None, encoding='utf-8', names=True)
        for i, name in enumerate(np.atleast_1d(buf['name'])):
            if name[:7] == 'light_3':
                buf['name'][i] = 'dil_' + name[8:]

        for i, name in enumerate(np.atleast_1d(buf['name'])):
            if name[:3] == 'ldc':
                buf['name'][i] = 'host_' + name

        self.allkeys = np.atleast_1d(buf['name'])
        self.labels = np.atleast_1d(buf['label'])
        self.units = np.atleast_1d(buf['unit'])
        if 'truth' in buf.dtype.names:
            self.truths = np.atleast_1d(buf['truth'])
        else:
            self.truths = np.nan * np.ones(len(self.allkeys))
        self.params = collections.OrderedDict()
        self.params['user-given:'] = ''
        for i, key in enumerate(self.allkeys):
            if np.atleast_1d(buf['value'])[i] not in self.allkeys:
                self.params[key] = np.float(np.atleast_1d(buf['value'])[i])
            else:
                self.params[key] = np.atleast_1d(buf['value'])[i]

        self.params['automatically set:'] = ''
        for companion in self.settings['companions_all']:
            for inst in self.settings['inst_all']:
                if 'dil_' + inst not in self.params:
                    self.params['dil_' + inst] = 0.0
                if companion + '_rr' not in self.params:
                    self.params[companion + '_rr'] = None
                if companion + '_rsuma' not in self.params:
                    self.params[companion + '_rsuma'] = None
                if companion + '_cosi' not in self.params:
                    self.params[companion + '_cosi'] = 0.0
                if companion + '_epoch' not in self.params:
                    self.params[companion + '_epoch'] = None
                if companion + '_period' not in self.params:
                    self.params[companion + '_period'] = None
                    self.settings['do_not_phase_fold'] = True
                if companion + '_sbratio_' + inst not in self.params:
                    self.params[companion + '_sbratio_' + inst] = 0.0
                if companion + '_a' not in self.params:
                    self.params[companion + '_a'] = None
                if companion + '_q' not in self.params:
                    self.params[companion + '_q'] = 1.0
                if companion + '_K' not in self.params:
                    self.params[companion + '_K'] = 0.0
                if companion + '_f_c' not in self.params:
                    self.params[companion + '_f_c'] = 0.0
                if companion + '_f_s' not in self.params:
                    self.params[companion + '_f_s'] = 0.0
                if 'host_ldc_' + inst not in self.params:
                    self.params['host_ldc_' + inst] = None
                if companion + '_ldc_' + inst not in self.params:
                    self.params[companion + '_ldc_' + inst] = None
                if 'host_gdc_' + inst not in self.params:
                    self.params['host_gdc_' + inst] = None
                if companion + '_gdc_' + inst not in self.params:
                    self.params[companion + '_gdc_' + inst] = None
                if 'didt_' + inst not in self.params:
                    self.params['didt_' + inst] = None
                if 'domdt_' + inst not in self.params:
                    self.params['domdt_' + inst] = None
                if 'host_rotfac_' + inst not in self.params:
                    self.params['host_rotfac_' + inst] = 1.0
                if companion + '_rotfac_' + inst not in self.params:
                    self.params[companion + '_rotfac_' + inst] = 1.0
                if 'host_hf_' + inst not in self.params:
                    self.params['host_hf_' + inst] = 1.5
                if companion + '_hf_' + inst not in self.params:
                    self.params[companion + '_hf_' + inst] = 1.5
                if 'host_bfac_' + inst not in self.params:
                    self.params['host_bfac_' + inst] = None
                if companion + '_bfac_' + inst not in self.params:
                    self.params[companion + '_bfac_' + inst] = None
                if 'host_atmo_' + inst not in self.params:
                    self.params['host_atmo_' + inst] = None
                if companion + '_atmo_' + inst not in self.params:
                    self.params[companion + '_atmo_' + inst] = None
                if 'host_lambda_' + inst not in self.params:
                    self.params['host_lambda_' + inst] = None
                if companion + '_lambda_' + inst not in self.params:
                    self.params[companion + '_lambda_' + inst] = None
                if 'host_vsini' not in self.params:
                    self.params['host_vsini'] = None
                if companion + '_vsini' not in self.params:
                    self.params[companion + '_vsini'] = None
                if 'host_spots_' + inst not in self.params:
                    self.params['host_spots_' + inst] = None
                if companion + '_spots_' + inst not in self.params:
                    self.params[companion + '_spots_' + inst] = None
                if companion + '_phase_curve_beaming_' + inst not in self.params:
                    self.params[companion + '_phase_curve_beaming_' + inst] = None
                if companion + '_phase_curve_atmospheric_' + inst not in self.params:
                    self.params[companion + '_phase_curve_atmospheric_' + inst] = None
                if companion + '_phase_curve_ellipsoidal_' + inst not in self.params:
                    self.params[companion + '_phase_curve_ellipsoidal_' + inst] = None
                if self.params[(companion + '_atmo_' + inst)] is not None:
                    if self.params[(companion + '_sbratio_' + inst)] == 0:
                        if self.params[(companion + '_atmo_' + inst)] > 0:
                            self.params[companion + '_sbratio_' + inst] = 1e-15
                    if self.params[(companion + '_sbratio_' + inst)] > 0:
                        if self.params[(companion + '_atmo_' + inst)] == 0:
                            self.params[companion + '_atmo_' + inst] = 1e-15
                    if np.abs(self.params[(companion + '_f_c')]) > 0.8:
                        raise ValueError(companion + '_f_c is ' + str(self.params[(companion + '_f_c')]) + ', but needs to lie within [-0.8,0.8]')
                    if np.abs(self.params[(companion + '_f_s')]) > 0.8:
                        raise ValueError(companion + '_f_s is ' + str(self.params[(companion + '_f_s')]) + ', but needs to lie within [-0.8,0.8]')

        for inst in self.settings['inst_all']:
            if inst in self.settings['inst_phot']:
                kkey = 'flux'
            else:
                if inst in self.settings['inst_rv']:
                    kkey = 'rv'
                if 'baseline_gp1_' + kkey + '_' + inst in self.params:
                    self.params['baseline_gp_matern32_lnsigma_' + kkey + '_' + inst] = 1.0 * self.params[('baseline_gp1_' + kkey + '_' + inst)]
                    warnings.warn('Deprecation warning. You are using outdated keywords. Automatically renaming baseline_gp1_' + kkey + '_' + inst + ' ---> ' + 'baseline_gp_matern32_lnsigma_' + kkey + '_' + inst)
                if 'baseline_gp2_' + kkey + '_' + inst in self.params:
                    self.params['baseline_gp_matern32_lnrho_' + kkey + '_' + inst] = 1.0 * self.params[('baseline_gp2_' + kkey + '_' + inst)]
                    warnings.warn('Deprecation warning. You are using outdated keywords. Automatically renaming baseline_gp2_' + kkey + '_' + inst + ' ---> ' + 'baseline_gp_matern32_lnrho_' + kkey + '_' + inst)
                if 'host_geom_albedo_' + inst in self.params:
                    warnings.warn('Deprecation warning. You are using outdated keywords. Automatically renaming host_geom_albedo_' + inst + ' ---> ' + 'host_atmo_' + inst)
                    self.params['host_atmo_' + inst] = self.params[('host_geom_albedo_' + inst)]
                if companion + '_geom_albedo_' + inst in self.params:
                    warnings.warn('Deprecation warning. You are using outdated keywords. Automatically renaming ' + companion + '_geom_albedo_' + inst + ' ---> ' + companion + '_atmo_' + inst)
                    self.params[companion + '_atmo_' + inst] = self.params[(companion + '_geom_albedo_' + inst)]
                if 'host_heat_' + inst in self.params:
                    warnings.warn('Deprecation warning. You are using outdated keywords. Automatically renaming host_heat_' + inst + ' ---> ' + 'host_atmo_' + inst)
                    self.params['host_atmo_' + inst] = self.params[('host_heat_' + inst)]
            if companion + '_heat_' + inst in self.params:
                warnings.warn('Deprecation warning. You are using outdated keywords. Automatically renaming ' + companion + '_heat_' + inst + ' ---> ' + companion + '_atmo_' + inst)
                self.params[companion + '_atmo_' + inst] = self.params[(companion + '_heat_' + inst)]

        if 'coupled_with' in buf.dtype.names:
            self.coupled_with = buf['coupled_with']
        else:
            self.coupled_with = [
             None] * len(self.allkeys)
        for i, key in enumerate(self.allkeys):
            if isinstance(self.coupled_with[i], str) and len(self.coupled_with[i]) > 0:
                self.params[key] = self.params[self.coupled_with[i]]
                buf['fit'][i] = 0

        self.ind_fit = buf['fit'] == 1
        self.fitkeys = buf['name'][self.ind_fit]
        self.fitlabels = self.labels[self.ind_fit]
        self.fitunits = self.units[self.ind_fit]
        self.fittruths = self.truths[self.ind_fit]
        self.theta_0 = buf['value'][self.ind_fit]
        if 'init_err' in buf.dtype.names:
            self.init_err = buf['init_err'][self.ind_fit]
        else:
            self.init_err = 1e-08
        self.bounds = [str(item).split(' ') for item in buf['bounds'][self.ind_fit]]
        for i, item in enumerate(self.bounds):
            if item[0] in ('uniform', 'normal'):
                self.bounds[i] = [
                 item[0], np.float(item[1]), np.float(item[2])]
            elif item[0] in ('trunc_normal', ):
                self.bounds[i] = [
                 item[0], np.float(item[1]), np.float(item[2]), np.float(item[3]), np.float(item[4])]
            else:
                raise ValueError('Bounds have to be "uniform", "normal" or "trunc_normal". Input from "params.csv" was "' + self.bounds[i][0] + '".')

        self.ndim = len(self.theta_0)
        for th, b, key in zip(self.theta_0, self.bounds, self.fitkeys):
            if '_f_c' in key and b[0] == 'uniform':
                if b[1] < -0.9 or b[2] > 0.9:
                    raise ValueError('Eccentricity bounds are [' + str(b[1]) + ',' + str(b[2]) + '], but have to be in [-0.9, 0.9]')
                if '_f_s' in key:
                    if b[0] == 'uniform' and not b[1] < -0.9:
                        if b[2] > 0.9:
                            raise ValueError('Eccentricity bounds are [' + str(b[1]) + ',' + str(b[2]) + '], but have to be in [-0.9, 0.9]')
                        if '_f_c' in key:
                            if b[0] == 'normal':
                                raise ValueError('Normal priors on eccentricity are not allowed. Please use "trunc_normal" constrained within [-0.9, 0.9]')
                        if '_f_s' in key:
                            if b[0] == 'normal':
                                raise ValueError('Normal priors on eccentricity are not allowed. Please use "trunc_normal" constrained within [-0.9, 0.9]')
                        if '_f_c' in key and b[0] == 'trunc_normal' and not b[1] < -0.9:
                            if b[2] > 0.9:
                                raise ValueError('Eccentricity bounds are [' + str(b[1]) + ',' + str(b[2]) + '], but have to be in [-0.9, 0.9]')
                        if '_f_s' in key:
                            if b[0] == 'trunc_normal' and not b[1] < -0.9:
                                if b[2] > 0.9:
                                    raise ValueError('Eccentricity bounds are [' + str(b[1]) + ',' + str(b[2]) + '], but have to be in [-0.9, 0.9]')
                                if b[0] == 'uniform':
                                    if not b[1] <= th <= b[2]:
                                        raise ValueError('The initial guess for ' + key + ' lies outside of its bounds.')
                                if b[0] == 'normal':
                                    if np.abs(th - b[1]) > 3 * b[2]:
                                        answer = input('The initial guess for ' + key + ' lies more than 3 sigma from its prior\n' + 'What do you want to do?\n' + '1 : continue at any sacrifice \n' + '2 : stop and let me fix the params.csv file \n')
                                        if answer == 1:
                                            pass
                                        else:
                                            raise ValueError('User aborted the run.')
                                if b[0] == 'trunc_normal':
                                    if not b[1] <= th <= b[2]:
                                        raise ValueError('The initial guess for ' + key + ' lies outside of its bounds.')
                                if b[0] == 'trunc_normal':
                                    if np.abs(th - b[3]) > 3 * b[4]:
                                        answer = input('The initial guess for ' + key + ' lies more than 3 sigma from its prior\n' + 'What do you want to do?\n' + '1 : continue at any sacrifice \n' + '2 : stop and let me fix the params.csv file \n')
                                        if answer == 1:
                                            continue
                                    raise ValueError('User aborted the run.')

    def load_data(self):
        """
        Example: 
        -------
            A lightcurve is stored as
                data['TESS']['time'], data['TESS']['flux']
            A RV curve is stored as
                data['HARPS']['time'], data['HARPS']['flux']
        """
        self.fulldata = {}
        self.data = {}
        for inst in self.settings['inst_phot']:
            time, flux, flux_err = np.genfromtxt((os.path.join(self.datadir, inst + '.csv')), delimiter=',', dtype=float, unpack=True)[0:3]
            if not any(np.isnan(time)):
                if any(np.isnan(flux)) or any(np.isnan(flux_err)):
                    raise ValueError('There are NaN values in "' + inst + '.csv". Please exclude these rows from the file and restart.')
                if not all(np.diff(time) >= 0):
                    raise ValueError('The time array in "' + inst + '.csv" is not sorted. Please make sure the file is not corrupted, then sort it by time and restart.')
                else:
                    if not all(np.diff(time) > 0):
                        warnings.warn('There are repeated time stamps in the time array in "' + inst + '.csv". Please make sure the file is not corrupted (e.g. insuffiecient precision in your time stamps).')
                    else:
                        self.fulldata[inst] = {'time':time, 
                         'flux':flux, 
                         'err_scales_flux':flux_err / np.nanmean(flux_err)}
                        if self.settings['fast_fit'] and len(self.settings['inst_phot']) > 0:
                            time, flux, flux_err = self.reduce_phot_data(time, flux, flux_err, inst=inst)
                self.data[inst] = {'time':time, 
                 'flux':flux, 
                 'err_scales_flux':flux_err / np.nanmean(flux_err)}

        for inst in self.settings['inst_rv']:
            time, rv, rv_err = np.genfromtxt((os.path.join(self.datadir, inst + '.csv')), delimiter=',', dtype=float, unpack=True)
            if not all(np.diff(time) > 0):
                raise ValueError('Your time array in "' + inst + '.csv" is not sorted. You will want to check that...')
            self.data[inst] = {'time':time,  'rv':rv, 
             'white_noise_rv':rv_err}

        self.data['inst_phot'] = {'time':[],  'flux':[],  'flux_err':[],  'inst':[]}
        for inst in self.settings['inst_phot']:
            self.data['inst_phot']['time'] += list(self.data[inst]['time'])
            self.data['inst_phot']['flux'] += list(self.data[inst]['flux'])
            self.data['inst_phot']['flux_err'] += [inst] * len(self.data[inst]['time'])
            self.data['inst_phot']['inst'] += [inst] * len(self.data[inst]['time'])

        ind_sort = np.argsort(self.data['inst_phot']['time'])
        self.data['inst_phot']['ind_sort'] = ind_sort
        self.data['inst_phot']['time'] = np.array(self.data['inst_phot']['time'])[ind_sort]
        self.data['inst_phot']['flux'] = np.array(self.data['inst_phot']['flux'])[ind_sort]
        self.data['inst_phot']['flux_err'] = np.array(self.data['inst_phot']['flux_err'])[ind_sort]
        self.data['inst_phot']['inst'] = np.array(self.data['inst_phot']['inst'])[ind_sort]
        self.data['inst_rv'] = {'time':[],  'rv':[],  'rv_err':[],  'inst':[]}
        for inst in self.settings['inst_rv']:
            self.data['inst_rv']['time'] += list(self.data[inst]['time'])
            self.data['inst_rv']['rv'] += list(self.data[inst]['rv'])
            self.data['inst_rv']['rv_err'] += list(np.nan * self.data[inst]['rv'])
            self.data['inst_rv']['inst'] += [inst] * len(self.data[inst]['time'])

        ind_sort = np.argsort(self.data['inst_rv']['time'])
        self.data['inst_rv']['ind_sort'] = ind_sort
        self.data['inst_rv']['time'] = np.array(self.data['inst_rv']['time'])[ind_sort]
        self.data['inst_rv']['rv'] = np.array(self.data['inst_rv']['rv'])[ind_sort]
        self.data['inst_rv']['rv_er'] = np.array(self.data['inst_rv']['rv_err'])[ind_sort]
        self.data['inst_rv']['inst'] = np.array(self.data['inst_rv']['inst'])[ind_sort]

    def my_truncnorm_isf(q, a, b, mean, std):
        a_scipy = 1.0 * (a - mean) / std
        b_scipy = 1.0 * (b - mean) / std
        return truncnorm.isf(q, a_scipy, b_scipy, loc=mean, scale=std)

    def change_epoch(self):
        """
        change epoch entry from params.csv to set epoch into the middle of the range
        """
        for companion in self.settings['companions_all']:
            alldata = []
            for inst in self.settings[('inst_for_' + companion + '_epoch')]:
                alldata += list(self.data[inst]['time'])

            start = np.nanmin(alldata)
            end = np.nanmax(alldata)
            user_epoch = 1.0 * self.params[(companion + '_epoch')]
            period = 1.0 * self.params[(companion + '_period')]
            if 'fast_fit_width' in self.settings:
                if self.settings['fast_fit_width'] is not None:
                    width = self.settings['fast_fit_width']
                else:
                    width = 0
                first_epoch = get_first_epoch(alldata, (self.params[(companion + '_epoch')]), (self.params[(companion + '_period')]), width=width)
                N = int(np.round((end - start) / 2.0 / period))
                self.settings['mid_epoch'] = first_epoch + N * period
                N_shift = int(np.round((self.settings['mid_epoch'] - user_epoch) / period))
                self.params[companion + '_epoch'] = 1.0 * self.settings['mid_epoch']
                try:
                    ind_e = np.where(self.fitkeys == companion + '_epoch')[0][0]
                    ind_p = np.where(self.fitkeys == companion + '_period')[0][0]
                    N_truth_shift = int(np.round((self.settings['mid_epoch'] - self.fittruths[ind_e]) / self.fittruths[ind_p]))
                    self.fittruths[ind_e] += N_truth_shift * self.fittruths[ind_p]
                except:
                    pass

                if N_shift != 0 and companion + '_epoch' in self.fitkeys:
                    ind_e = np.where(self.fitkeys == companion + '_epoch')[0][0]
                    ind_p = np.where(self.fitkeys == companion + '_period')[0][0]
                    self.theta_0[ind_e] = 1.0 * self.settings['mid_epoch']
                    if (self.bounds[ind_e][0] == 'uniform') & (self.bounds[ind_p][0] == 'uniform'):
                        if N_shift > 0:
                            self.bounds[ind_e][1] = self.bounds[ind_e][1] + N_shift * self.bounds[ind_p][1]
                            self.bounds[ind_e][2] = self.bounds[ind_e][2] + N_shift * self.bounds[ind_p][2]
            if N_shift < 0:
                self.bounds[ind_e][1] = self.bounds[ind_e][1] + N_shift * self.bounds[ind_p][2]
                self.bounds[ind_e][2] = self.bounds[ind_e][2] + N_shift * self.bounds[ind_p][1]
            elif (self.bounds[ind_e][0] == 'normal') & (self.bounds[ind_p][0] == 'normal'):
                self.bounds[ind_e][1] = self.bounds[ind_e][1] + N_shift * self.bounds[ind_p][1]
                self.bounds[ind_e][2] = np.sqrt(self.bounds[ind_e][2] ** 2 + N_shift ** 2 * self.bounds[ind_p][2] ** 2)
            elif (self.bounds[ind_e][0] == 'trunc_normal') & (self.bounds[ind_p][0] == 'trunc_normal'):
                if N_shift > 0:
                    self.bounds[ind_e][1] = self.bounds[ind_e][1] + N_shift * self.bounds[ind_p][1]
                    self.bounds[ind_e][2] = self.bounds[ind_e][2] + N_shift * self.bounds[ind_p][2]
                else:
                    if N_shift < 0:
                        self.bounds[ind_e][1] = self.bounds[ind_e][1] + N_shift * self.bounds[ind_p][2]
                        self.bounds[ind_e][2] = self.bounds[ind_e][2] + N_shift * self.bounds[ind_p][1]
                    self.bounds[ind_e][3] = self.bounds[ind_e][3] + N_shift * self.bounds[ind_p][3]
                    self.bounds[ind_e][4] = np.sqrt(self.bounds[ind_e][4] ** 2 + N_shift ** 2 * self.bounds[ind_p][4] ** 2)
            elif (self.bounds[ind_e][0] == 'uniform') & (self.bounds[ind_p][0] == 'normal'):
                self.bounds[ind_e][1] = self.bounds[ind_e][1] + N_shift * (period + self.bounds[ind_p][2])
                self.bounds[ind_e][2] = self.bounds[ind_e][2] + N_shift * (period + self.bounds[ind_p][2])
            elif (self.bounds[ind_e][0] == 'uniform') & (self.bounds[ind_p][0] == 'trunc_normal'):
                self.bounds[ind_e][1] = self.bounds[ind_e][1] + N_shift * (period + self.bounds[ind_p][4])
                self.bounds[ind_e][2] = self.bounds[ind_e][2] + N_shift * (period + self.bounds[ind_p][4])
            elif (self.bounds[ind_e][0] == 'normal') & (self.bounds[ind_p][0] == 'uniform'):
                raise ValueError('shift_epoch with different priors for epoch and period is not yet implemented.')
            elif (self.bounds[ind_e][0] == 'normal') & (self.bounds[ind_p][0] == 'trunc_normal'):
                raise ValueError('shift_epoch with different priors for epoch and period is not yet implemented.')
            elif (self.bounds[ind_e][0] == 'trunc_normal') & (self.bounds[ind_p][0] == 'uniform'):
                raise ValueError('shift_epoch with different priors for epoch and period is not yet implemented.')
            elif (self.bounds[ind_e][0] == 'trunc_normal') & (self.bounds[ind_p][0] == 'normal'):
                raise ValueError('shift_epoch with different priors for epoch and period is not yet implemented.')
            else:
                raise ValueError('Parameters "bounds" have to be "uniform", "normal" or "trunc_normal".')

    def reduce_phot_data(self, time, flux, flux_err, inst=None):
        ind_in = []
        for companion in self.settings['companions_phot']:
            epoch = self.params[(companion + '_epoch')]
            period = self.params[(companion + '_period')]
            width = self.settings['fast_fit_width']
            if self.settings['secondary_eclipse']:
                ind_ecl1x, ind_ecl2x, ind_outx = index_eclipses(time, epoch, period, width, width)
                ind_in += list(ind_ecl1x)
                ind_in += list(ind_ecl2x)
                self.fulldata[inst][companion + '_ind_ecl1'] = ind_ecl1x
                self.fulldata[inst][companion + '_ind_ecl2'] = ind_ecl2x
                self.fulldata[inst][companion + '_ind_out'] = ind_outx
            else:
                ind_inx, ind_outx = index_transits(time, epoch, period, width)
                ind_in += list(ind_inx)
                self.fulldata[inst][companion + '_ind_in'] = ind_inx
                self.fulldata[inst][companion + '_ind_out'] = ind_outx

        ind_in = np.sort(np.unique(ind_in))
        self.fulldata[inst]['all_ind_in'] = ind_in
        self.fulldata[inst]['all_ind_out'] = np.delete(np.arange(len(self.fulldata[inst]['time'])), ind_in)
        if len(ind_in) == 0:
            raise ValueError(inst + '.csv does not contain any in-transit data. Check that your epoch and period guess are correct.')
        time = time[ind_in]
        flux = flux[ind_in]
        flux_err = flux_err[ind_in]
        return (time, flux, flux_err)

    def prepare_ttv_fit(self):
        """
        this must be run *after* reduce_phot_data()
        """
        for companion in self.settings['companions_phot']:
            all_times = []
            all_flux = []
            for inst in self.settings['inst_phot']:
                all_times += list(self.data[inst]['time'])
                all_flux += list(self.data[inst]['flux'])

            self.data[companion + '_tmid_observed_transits'] = get_tmid_observed_transits(all_times, self.params[(companion + '_epoch')], self.params[(companion + '_period')], self.settings['fast_fit_width'])
            width = self.settings['fast_fit_width']
            for inst in self.settings['inst_phot']:
                time = self.data[inst]['time']
                for i, t in enumerate(self.data[(companion + '_tmid_observed_transits')]):
                    ind = np.where((time >= t - width / 2.0) & (time <= t + width / 2.0))[0]
                    self.data[inst][companion + '_ind_time_transit_' + str(i + 1)] = ind
                    self.data[inst][companion + '_time_transit_' + str(i + 1)] = time[ind]

    def load_stellar_priors(self, N_samples=10000):
        if os.path.exists(os.path.join(self.datadir, 'params_star.csv')):
            if self.settings['use_host_density_prior'] is True:
                buf = np.genfromtxt((os.path.join(self.datadir, 'params_star.csv')), delimiter=',', names=True, dtype=None, encoding='utf-8', comments='#')
                radius = simulate_PDF((buf['R_star']), (buf['R_star_lerr']), (buf['R_star_uerr']), size=N_samples, plot=False) * 69570000000.0
                mass = simulate_PDF((buf['M_star']), (buf['M_star_lerr']), (buf['M_star_uerr']), size=N_samples, plot=False) * 1.9884754153381438e+33
                volume = 1.3333333333333333 * np.pi * radius ** 3
                density = mass / volume
                self.params_star = {'R_star_median':buf['R_star'],  'R_star_lerr':buf['R_star_lerr'], 
                 'R_star_uerr':buf['R_star_uerr'], 
                 'M_star_median':buf['M_star'], 
                 'M_star_lerr':buf['M_star_lerr'], 
                 'M_star_uerr':buf['M_star_uerr']}
                self.external_priors['host_density'] = [
                 'normal', np.median(density), np.max([np.median(density) - np.percentile(density, 16), np.percentile(density, 84) - np.median(density)])]