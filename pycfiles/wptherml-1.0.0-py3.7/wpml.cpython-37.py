# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wptherml/wpml.py
# Compiled at: 2019-08-20 10:27:02
# Size of source mod 2**32: 39781 bytes
"""
Created on Sat Nov 10 21:07:22 2018

@author: jay
"""
from wptherml import tmm
from wptherml import colorlib
from wptherml import coolinglib
from wptherml import stpvlib
from wptherml import lightlib
import wptherml.numlib as numlib
import wptherml.datalib as datalib
from matplotlib import pyplot as plt
from scipy import integrate
import numpy as np

class multilayer:

    def __init__--- This code section failed: ---

 L.  29         0  LOAD_CONST               1
                2  LOAD_FAST                'self'
                4  STORE_ATTR               result

 L.  30         6  LOAD_FAST                'args'
                8  LOAD_METHOD              get
               10  LOAD_STR                 'mode'
               12  CALL_METHOD_1         1  '1 positional argument'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               mode

 L.  35        18  LOAD_FAST                'args'
               20  LOAD_METHOD              get
               22  LOAD_STR                 'file'
               24  CALL_METHOD_1         1  '1 positional argument'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               inputfile

 L.  41        30  LOAD_STR                 'p'
               32  LOAD_FAST                'self'
               34  STORE_ATTR               pol

 L.  43        36  LOAD_CONST               0
               38  LOAD_FAST                'self'
               40  STORE_ATTR               theta

 L.  45        42  LOAD_CONST               30
               44  LOAD_GLOBAL              np
               46  LOAD_ATTR                pi
               48  BINARY_MULTIPLY  
               50  LOAD_CONST               180
               52  BINARY_TRUE_DIVIDE
               54  LOAD_FAST                'self'
               56  STORE_ATTR               theta_sun

 L.  47        58  LOAD_CONST               300
               60  LOAD_FAST                'self'
               62  STORE_ATTR               T_ml

 L.  49        64  LOAD_CONST               300
               66  LOAD_FAST                'self'
               68  STORE_ATTR               T_amb

 L.  51        70  LOAD_CONST               2.254e-06
               72  LOAD_FAST                'self'
               74  STORE_ATTR               lbg

 L.  53        76  LOAD_STR                 'InGaAsSb'
               78  LOAD_FAST                'self'
               80  STORE_ATTR               PV

 L.  56        82  LOAD_CONST               298
               84  LOAD_FAST                'self'
               86  STORE_ATTR               T_cell

 L.  58        88  LOAD_CONST               600
               90  LOAD_FAST                'self'
               92  STORE_ATTR               solarconc

 L.  60        94  LOAD_CONST               0
               96  LOAD_FAST                'self'
               98  STORE_ATTR               explicit_angle

 L.  64       100  LOAD_CONST               7
              102  LOAD_FAST                'self'
              104  STORE_ATTR               deg

 L.  67       106  LOAD_CONST               0j
              108  LOAD_FAST                'self'
              110  STORE_ATTR               SPP_Resonance

 L.  68       112  LOAD_CONST               0j
              114  LOAD_FAST                'self'
              116  STORE_ATTR               PA_Resonance

 L.  77       118  LOAD_CONST               0
              120  LOAD_FAST                'self'
              122  STORE_ATTR               stpv_emitter_calc

 L.  78       124  LOAD_CONST               0
              126  LOAD_FAST                'self'
              128  STORE_ATTR               stpv_absorber_calc

 L.  81       130  LOAD_CONST               0
              132  LOAD_FAST                'self'
              134  STORE_ATTR               cooling_calc

 L.  82       136  LOAD_CONST               0
              138  LOAD_FAST                'self'
              140  STORE_ATTR               lightbulb_calc

 L.  83       142  LOAD_CONST               0
              144  LOAD_FAST                'self'
              146  STORE_ATTR               spp_calc

 L.  84       148  LOAD_CONST               0
              150  LOAD_FAST                'self'
              152  STORE_ATTR               color_calc

 L.  85       154  LOAD_CONST               1
              156  LOAD_FAST                'self'
              158  STORE_ATTR               fresnel_calc

 L.  86       160  LOAD_CONST               0
              162  LOAD_FAST                'self'
              164  STORE_ATTR               explicit_angle

 L.  87       166  LOAD_CONST               0
              168  LOAD_FAST                'self'
              170  STORE_ATTR               resonance

 L.  88       172  LOAD_GLOBAL              np
              174  LOAD_METHOD              zeros
              176  LOAD_CONST               3
              178  CALL_METHOD_1         1  '1 positional argument'
              180  LOAD_FAST                'self'
              182  STORE_ATTR               reflective_rgb

 L.  89       184  LOAD_GLOBAL              np
              186  LOAD_METHOD              zeros
              188  LOAD_CONST               3
              190  CALL_METHOD_1         1  '1 positional argument'
              192  LOAD_FAST                'self'
              194  STORE_ATTR               thermal_rgb

 L.  90       196  LOAD_STR                 'None'
              198  LOAD_FAST                'self'
              200  STORE_ATTR               color_name

 L.  94       202  LOAD_FAST                'self'
              204  LOAD_METHOD              inline_structure
              206  LOAD_FAST                'args'
              208  CALL_METHOD_1         1  '1 positional argument'
              210  POP_TOP          

 L.  99       212  LOAD_GLOBAL              np
              214  LOAD_METHOD              zeros
              216  LOAD_GLOBAL              len
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                lambda_array
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  CALL_METHOD_1         1  '1 positional argument'
              226  LOAD_FAST                'self'
              228  STORE_ATTR               reflectivity_array

 L. 100       230  LOAD_GLOBAL              np
              232  LOAD_METHOD              zeros
              234  LOAD_GLOBAL              len
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                lambda_array
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  CALL_METHOD_1         1  '1 positional argument'
              244  LOAD_FAST                'self'
              246  STORE_ATTR               transmissivity_array

 L. 101       248  LOAD_GLOBAL              np
              250  LOAD_METHOD              zeros
              252  LOAD_GLOBAL              len
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                lambda_array
              258  CALL_FUNCTION_1       1  '1 positional argument'
              260  CALL_METHOD_1         1  '1 positional argument'
              262  LOAD_FAST                'self'
              264  STORE_ATTR               emissivity_array

 L. 102       266  LOAD_GLOBAL              np
              268  LOAD_METHOD              zeros
              270  LOAD_GLOBAL              len
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                lambda_array
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  CALL_METHOD_1         1  '1 positional argument'
              280  LOAD_FAST                'self'
              282  STORE_ATTR               thermal_emission_array

 L. 105       284  BUILD_LIST_0          0 
              286  LOAD_FAST                'self'
              288  STORE_ATTR               valid_lambda_array

 L. 106       290  BUILD_LIST_0          0 
              292  LOAD_FAST                'self'
              294  STORE_ATTR               valid_reflectivity_array

 L. 107       296  BUILD_LIST_0          0 
              298  LOAD_FAST                'self'
              300  STORE_ATTR               valid_transmissivity_array

 L. 108       302  BUILD_LIST_0          0 
              304  LOAD_FAST                'self'
              306  STORE_ATTR               valid_emissivity_array

 L. 109       308  BUILD_LIST_0          0 
              310  LOAD_FAST                'self'
              312  STORE_ATTR               vald_theta_array

 L. 110       314  BUILD_LIST_0          0 
              316  LOAD_FAST                'self'
              318  STORE_ATTR               valid_ref_vs_theta

 L. 111       320  BUILD_LIST_0          0 
              322  LOAD_FAST                'self'
              324  STORE_ATTR               valid_trans_vs_theta

 L. 112       326  BUILD_LIST_0          0 
              328  LOAD_FAST                'self'
              330  STORE_ATTR               valid_emiss_vs_theta

 L. 113       332  LOAD_CONST               1
              334  LOAD_FAST                'self'
              336  STORE_ATTR               validation_option

 L. 120       338  LOAD_GLOBAL              np
              340  LOAD_METHOD              zeros
              342  LOAD_CONST               180
              344  CALL_METHOD_1         1  '1 positional argument'
              346  LOAD_FAST                'self'
              348  STORE_ATTR               r_vs_theta

 L. 121       350  LOAD_GLOBAL              np
              352  LOAD_METHOD              zeros
              354  LOAD_CONST               180
              356  CALL_METHOD_1         1  '1 positional argument'
              358  LOAD_FAST                'self'
              360  STORE_ATTR               t_vs_theta

 L. 122       362  LOAD_GLOBAL              np
              364  LOAD_METHOD              zeros
              366  LOAD_CONST               180
              368  CALL_METHOD_1         1  '1 positional argument'
              370  LOAD_FAST                'self'
              372  STORE_ATTR               eps_vs_theta

 L. 123       374  LOAD_GLOBAL              np
              376  LOAD_METHOD              linspace
              378  LOAD_CONST               0
              380  LOAD_CONST               89.5
              382  LOAD_GLOBAL              np
              384  LOAD_ATTR                pi
              386  BINARY_MULTIPLY  
              388  LOAD_CONST               180
              390  BINARY_TRUE_DIVIDE
              392  LOAD_CONST               180
              394  CALL_METHOD_3         3  '3 positional arguments'
              396  LOAD_FAST                'self'
              398  STORE_ATTR               theta_array

 L. 129       400  LOAD_FAST                'self'
              402  LOAD_ATTR                explicit_angle
          404_406  POP_JUMP_IF_FALSE   686  'to 686'

 L. 131       408  LOAD_CONST               0
              410  STORE_FAST               'a'

 L. 132       412  LOAD_GLOBAL              np
              414  LOAD_ATTR                pi
              416  LOAD_CONST               2.0
              418  BINARY_TRUE_DIVIDE
              420  STORE_FAST               'b'

 L. 133       422  LOAD_GLOBAL              np
              424  LOAD_ATTR                polynomial
              426  LOAD_ATTR                legendre
              428  LOAD_METHOD              leggauss
              430  LOAD_FAST                'self'
              432  LOAD_ATTR                deg
              434  CALL_METHOD_1         1  '1 positional argument'
              436  UNPACK_SEQUENCE_2     2 
              438  LOAD_FAST                'self'
              440  STORE_ATTR               x
              442  LOAD_FAST                'self'
              444  STORE_ATTR               w

 L. 134       446  LOAD_CONST               0.5
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                x
              452  LOAD_CONST               1
              454  BINARY_ADD       
              456  BINARY_MULTIPLY  
              458  LOAD_FAST                'b'
              460  LOAD_FAST                'a'
              462  BINARY_SUBTRACT  
              464  BINARY_MULTIPLY  
              466  LOAD_FAST                'a'
              468  BINARY_ADD       
              470  LOAD_FAST                'self'
              472  STORE_ATTR               t

 L. 135       474  LOAD_FAST                'self'
              476  LOAD_ATTR                w
              478  LOAD_CONST               0.5
              480  BINARY_MULTIPLY  
              482  LOAD_FAST                'b'
              484  LOAD_FAST                'a'
              486  BINARY_SUBTRACT  
              488  BINARY_MULTIPLY  
              490  LOAD_FAST                'self'
              492  STORE_ATTR               w

 L. 137       494  LOAD_GLOBAL              np
              496  LOAD_METHOD              zeros
              498  LOAD_FAST                'self'
              500  LOAD_ATTR                deg
              502  LOAD_GLOBAL              len
              504  LOAD_FAST                'self'
              506  LOAD_ATTR                lambda_array
              508  CALL_FUNCTION_1       1  '1 positional argument'
              510  BUILD_TUPLE_2         2 
              512  CALL_METHOD_1         1  '1 positional argument'
              514  LOAD_FAST                'self'
              516  STORE_ATTR               reflectivity_array_p

 L. 138       518  LOAD_GLOBAL              np
              520  LOAD_METHOD              zeros
              522  LOAD_FAST                'self'
              524  LOAD_ATTR                deg
              526  LOAD_GLOBAL              len
              528  LOAD_FAST                'self'
              530  LOAD_ATTR                lambda_array
              532  CALL_FUNCTION_1       1  '1 positional argument'
              534  BUILD_TUPLE_2         2 
              536  CALL_METHOD_1         1  '1 positional argument'
              538  LOAD_FAST                'self'
              540  STORE_ATTR               reflectivity_array_s

 L. 139       542  LOAD_GLOBAL              np
              544  LOAD_METHOD              zeros
              546  LOAD_FAST                'self'
              548  LOAD_ATTR                deg
              550  LOAD_GLOBAL              len
              552  LOAD_FAST                'self'
              554  LOAD_ATTR                lambda_array
              556  CALL_FUNCTION_1       1  '1 positional argument'
              558  BUILD_TUPLE_2         2 
              560  CALL_METHOD_1         1  '1 positional argument'
              562  LOAD_FAST                'self'
              564  STORE_ATTR               transmissivity_array_p

 L. 140       566  LOAD_GLOBAL              np
              568  LOAD_METHOD              zeros
              570  LOAD_FAST                'self'
              572  LOAD_ATTR                deg
              574  LOAD_GLOBAL              len
              576  LOAD_FAST                'self'
              578  LOAD_ATTR                lambda_array
              580  CALL_FUNCTION_1       1  '1 positional argument'
              582  BUILD_TUPLE_2         2 
              584  CALL_METHOD_1         1  '1 positional argument'
              586  LOAD_FAST                'self'
              588  STORE_ATTR               transmissivity_array_s

 L. 141       590  LOAD_GLOBAL              np
              592  LOAD_METHOD              zeros
              594  LOAD_FAST                'self'
              596  LOAD_ATTR                deg
              598  LOAD_GLOBAL              len
              600  LOAD_FAST                'self'
              602  LOAD_ATTR                lambda_array
              604  CALL_FUNCTION_1       1  '1 positional argument'
              606  BUILD_TUPLE_2         2 
              608  CALL_METHOD_1         1  '1 positional argument'
              610  LOAD_FAST                'self'
              612  STORE_ATTR               emissivity_array_p

 L. 142       614  LOAD_GLOBAL              np
              616  LOAD_METHOD              zeros
              618  LOAD_FAST                'self'
              620  LOAD_ATTR                deg
              622  LOAD_GLOBAL              len
              624  LOAD_FAST                'self'
              626  LOAD_ATTR                lambda_array
              628  CALL_FUNCTION_1       1  '1 positional argument'
              630  BUILD_TUPLE_2         2 
              632  CALL_METHOD_1         1  '1 positional argument'
              634  LOAD_FAST                'self'
              636  STORE_ATTR               emissivity_array_s

 L. 143       638  LOAD_GLOBAL              np
              640  LOAD_METHOD              zeros
              642  LOAD_FAST                'self'
              644  LOAD_ATTR                deg
              646  LOAD_GLOBAL              len
              648  LOAD_FAST                'self'
              650  LOAD_ATTR                lambda_array
              652  CALL_FUNCTION_1       1  '1 positional argument'
              654  BUILD_TUPLE_2         2 
              656  CALL_METHOD_1         1  '1 positional argument'
              658  LOAD_FAST                'self'
              660  STORE_ATTR               thermal_emission_array_p

 L. 144       662  LOAD_GLOBAL              np
              664  LOAD_METHOD              zeros
              666  LOAD_FAST                'self'
              668  LOAD_ATTR                deg
              670  LOAD_GLOBAL              len
              672  LOAD_FAST                'self'
              674  LOAD_ATTR                lambda_array
              676  CALL_FUNCTION_1       1  '1 positional argument'
              678  BUILD_TUPLE_2         2 
              680  CALL_METHOD_1         1  '1 positional argument'
              682  LOAD_FAST                'self'
              684  STORE_ATTR               thermal_emission_array_s
            686_0  COME_FROM           404  '404'

 L. 151       686  LOAD_FAST                'self'
              688  LOAD_METHOD              fresnel
              690  CALL_METHOD_0         0  '0 positional arguments'
              692  POP_TOP          

 L. 154       694  LOAD_FAST                'self'
              696  LOAD_ATTR                explicit_angle
          698_700  POP_JUMP_IF_FALSE   718  'to 718'

 L. 157       702  LOAD_FAST                'self'
              704  LOAD_METHOD              fresnel_ea
              706  CALL_METHOD_0         0  '0 positional arguments'
              708  POP_TOP          

 L. 160       710  LOAD_FAST                'self'
              712  LOAD_METHOD              thermal_emission_ea
              714  CALL_METHOD_0         0  '0 positional arguments'
              716  POP_TOP          
            718_0  COME_FROM           698  '698'

 L. 166       718  LOAD_FAST                'self'
              720  LOAD_ATTR                stpv_emitter_calc
          722_724  POP_JUMP_IF_TRUE    758  'to 758'
              726  LOAD_FAST                'self'
              728  LOAD_ATTR                stpv_absorber_calc
          730_732  POP_JUMP_IF_TRUE    758  'to 758'
              734  LOAD_FAST                'self'
              736  LOAD_ATTR                cooling_calc
          738_740  POP_JUMP_IF_TRUE    758  'to 758'
              742  LOAD_FAST                'self'
              744  LOAD_ATTR                lightbulb_calc
          746_748  POP_JUMP_IF_TRUE    758  'to 758'
              750  LOAD_FAST                'self'
              752  LOAD_ATTR                color_calc
          754_756  POP_JUMP_IF_FALSE   766  'to 766'
            758_0  COME_FROM           746  '746'
            758_1  COME_FROM           738  '738'
            758_2  COME_FROM           730  '730'
            758_3  COME_FROM           722  '722'

 L. 169       758  LOAD_FAST                'self'
              760  LOAD_METHOD              thermal_emission
              762  CALL_METHOD_0         0  '0 positional arguments'
              764  POP_TOP          
            766_0  COME_FROM           754  '754'

 L. 175       766  LOAD_FAST                'self'
              768  LOAD_ATTR                stpv_emitter_calc
          770_772  POP_JUMP_IF_FALSE   808  'to 808'
              774  LOAD_FAST                'self'
              776  LOAD_ATTR                explicit_angle
          778_780  POP_JUMP_IF_FALSE   808  'to 808'

 L. 177       782  LOAD_FAST                'self'
              784  LOAD_METHOD              stpv_se_ea
              786  CALL_METHOD_0         0  '0 positional arguments'
              788  POP_TOP          

 L. 178       790  LOAD_FAST                'self'
              792  LOAD_METHOD              stpv_pd_ea
              794  CALL_METHOD_0         0  '0 positional arguments'
              796  POP_TOP          

 L. 179       798  LOAD_FAST                'self'
              800  LOAD_METHOD              stpv_etatpv_ea
              802  CALL_METHOD_0         0  '0 positional arguments'
              804  POP_TOP          
              806  JUMP_FORWARD        840  'to 840'
            808_0  COME_FROM           778  '778'
            808_1  COME_FROM           770  '770'

 L. 181       808  LOAD_FAST                'self'
              810  LOAD_ATTR                stpv_emitter_calc
          812_814  POP_JUMP_IF_FALSE   840  'to 840'

 L. 183       816  LOAD_FAST                'self'
              818  LOAD_METHOD              stpv_se
              820  CALL_METHOD_0         0  '0 positional arguments'
              822  POP_TOP          

 L. 184       824  LOAD_FAST                'self'
              826  LOAD_METHOD              stpv_pd
              828  CALL_METHOD_0         0  '0 positional arguments'
              830  POP_TOP          

 L. 185       832  LOAD_FAST                'self'
              834  LOAD_METHOD              stpv_etatpv
              836  CALL_METHOD_0         0  '0 positional arguments'
              838  POP_TOP          
            840_0  COME_FROM           812  '812'
            840_1  COME_FROM           806  '806'

 L. 187       840  LOAD_FAST                'self'
              842  LOAD_ATTR                stpv_absorber_calc
          844_846  POP_JUMP_IF_FALSE   874  'to 874'

 L. 189       848  LOAD_FAST                'self'
              850  LOAD_ATTR                explicit_angle
          852_854  POP_JUMP_IF_FALSE   866  'to 866'

 L. 190       856  LOAD_FAST                'self'
              858  LOAD_METHOD              stpv_etaabs_ea
              860  CALL_METHOD_0         0  '0 positional arguments'
              862  POP_TOP          
              864  JUMP_FORWARD        874  'to 874'
            866_0  COME_FROM           852  '852'

 L. 192       866  LOAD_FAST                'self'
              868  LOAD_METHOD              stpv_etaabs
              870  CALL_METHOD_0         0  '0 positional arguments'
              872  POP_TOP          
            874_0  COME_FROM           864  '864'
            874_1  COME_FROM           844  '844'

 L. 194       874  LOAD_FAST                'self'
              876  LOAD_ATTR                color_calc
          878_880  POP_JUMP_IF_FALSE   898  'to 898'

 L. 196       882  LOAD_FAST                'self'
              884  LOAD_METHOD              ambient_color
              886  CALL_METHOD_0         0  '0 positional arguments'
              888  POP_TOP          

 L. 197       890  LOAD_FAST                'self'
              892  LOAD_METHOD              thermal_color
              894  CALL_METHOD_0         0  '0 positional arguments'
              896  POP_TOP          
            898_0  COME_FROM           878  '878'

 L. 199       898  LOAD_FAST                'self'
              900  LOAD_ATTR                lightbulb_calc
          902_904  POP_JUMP_IF_FALSE   914  'to 914'

 L. 202       906  LOAD_FAST                'self'
              908  LOAD_METHOD              luminous_efficiency
              910  CALL_METHOD_0         0  '0 positional arguments'
              912  POP_TOP          
            914_0  COME_FROM           902  '902'

 L. 212       914  LOAD_FAST                'self'
              916  LOAD_ATTR                cooling_calc
          918_920  POP_JUMP_IF_FALSE   954  'to 954'

 L. 219       922  LOAD_FAST                'self'
              924  LOAD_METHOD              cooling_power
              926  CALL_METHOD_0         0  '0 positional arguments'
              928  POP_TOP          

 L. 221       930  LOAD_GLOBAL              datalib
              932  LOAD_METHOD              AM
              934  LOAD_FAST                'self'
              936  LOAD_ATTR                lambda_array
              938  CALL_METHOD_1         1  '1 positional argument'
              940  STORE_FAST               'AM'

 L. 222       942  LOAD_GLOBAL              datalib
              944  LOAD_METHOD              ATData
              946  LOAD_FAST                'self'
              948  LOAD_ATTR                lambda_array
              950  CALL_METHOD_1         1  '1 positional argument'
              952  STORE_FAST               'T_atm'
            954_0  COME_FROM           918  '918'

Parse error at or near `COME_FROM' instruction at offset 766_0

    def get_validation_data(self):
        Valid_Dict = datalib.read_validation_dataself.validation_option
        if self.validation_option == 1 or self.validation_option == 3:
            self.valid_lambda_array = Valid_Dict['V_LAM']
            self.valid_reflectivity_array = Valid_Dict['V_REF']
            self.valid_transmissivity_array = Valid_Dict['V_TRANS']
            self.valid_emissivity_array = Valid_Dict['V_EMISS']
        else:
            if self.validation_option == 2:
                self.valid_theta_array = Valid_Dict['V_THETA']
                self.valid_ref_vs_theta = Valid_Dict['V_REF_V_THETA']
                self.valid_trans_vs_theta = Valid_Dict['V_TRANS_V_THETA']
                self.valid_emiss_vs_theta = Valid_Dict['V_EMISS_V_THETA']
        return 1

    def fresnel(self):
        nc = np.zeros((len(self.d)), dtype=complex)
        for i in range(0, len(self.lambda_array)):
            for j in range(0, len(self.d)):
                nc[j] = self.n[j][i]

            k0 = np.pi * 2 / self.lambda_array[i]
            M = tmm.tmm(k0, self.theta, self.pol, nc, self.d)
            t = 1.0 / M['M11']
            ti = M['theta_i']
            tL = M['theta_L']
            fac = nc[(len(self.d) - 1)] * np.costL / (nc[0] * np.costi)
            r = M['M21'] / M['M11']
            self.reflectivity_array[i] = np.real(r * np.conjr)
            self.transmissivity_array[i] = np.real(t * np.conjt * fac)
            self.emissivity_array[i] = 1 - self.reflectivity_array[i] - self.transmissivity_array[i]

        return 1

    def angular_fresnel(self, lambda_0):
        nc = np.zeros((len(self.d)), dtype=complex)
        idx, = np.where(self.lambda_array <= lambda_0)
        idx_val = idx[(len(idx) - 1)]
        for i in range(0, len(self.matlist)):
            nc[i] = self.n[i][idx_val]

        k0 = np.pi * 2 / lambda_0
        i = 0
        for thetai in self.theta_array:
            M = tmm.tmm(k0, thetai, self.pol, nc, self.d)
            t = 1.0 / M['M11']
            ti = M['theta_i']
            tL = M['theta_L']
            fac = nc[(len(self.d) - 1)] * np.costL / (nc[0] * np.costi)
            r = M['M21'] / M['M11']
            self.r_vs_theta[i] = np.real(r * np.conjr)
            self.t_vs_theta[i] = np.real(t * np.conjt * fac)
            self.eps_vs_theta[i] = 1 - self.r_vs_theta[i] - self.t_vs_theta[i]
            i = i + 1

        return 1

    def reflectivity(self):
        nc = np.zeros((len(self.d)), dtype=complex)
        for i in range(0, len(self.lambda_array)):
            for j in range(0, len(self.d)):
                nc[j] = self.n[j][i]

            k0 = np.pi * 2 / self.lambda_array[i]
            self.reflectivity_array[i] = tmm.Reflect(k0, self.theta, self.pol, nc, self.d)

        return 1

    def transmissivity(self):
        nc = np.zeros((len(self.d)), dtype=complex)
        for i in range(0, len(self.lambda_array)):
            for j in range(0, len(self.d)):
                nc[j] = self.n[j][i]

            k0 = np.pi * 2 / self.lambda_array[i]
            self.transmissivity_array[i] = tmm.Trans(k0, self.theta, self.pol, nc, self.d)

        return 1

    def fresnel_ea(self):
        if self.explicit_angle != 1:
            error = 'ERROR: EXPLIT ANGLE OPTION NOT SELECTED! \n'
            error = error + 'RE-INSTANTIATE YOUR MULTILAYER CLASS AND BE SURE \n'
            error = error + 'TO INCLUDE A LINE IN YOUR STRUCTURE DICTIONARY LIKE THE FOLLOWING: \n'
            error = error + 'EXPLICIT_ANGLE: 1'
            print(error)
            exit()
        nc = np.zeros((len(self.d)), dtype=complex)
        for i in range(0, len(self.lambda_array)):
            k0 = np.pi * 2 / self.lambda_array[i]
            for j in range(0, len(self.d)):
                nc[j] = self.n[j][i]

            for j in range(0, len(self.t)):
                Mp = tmm.tmm(k0, self.t[j], 'p', nc, self.d)
                Ms = tmm.tmm(k0, self.t[j], 's', nc, self.d)
                tp = 1.0 / Mp['M11']
                ts = 1.0 / Ms['M11']
                tp_i = Mp['theta_i']
                ts_i = Ms['theta_L']
                tp_L = Mp['theta_L']
                ts_L = Ms['theta_L']
                facp = nc[(len(self.d) - 1)] * np.costp_L / (nc[0] * np.costp_i)
                facs = nc[(len(self.d) - 1)] * np.costs_L / (nc[0] * np.costs_i)
                rp = Mp['M21'] / Mp['M11']
                rs = Ms['M21'] / Ms['M11']
                self.reflectivity_array_p[j][i] = np.real(rp * np.conjrp)
                self.reflectivity_array_s[j][i] = np.real(rs * np.conjrs)
                self.transmissivity_array_p[j][i] = np.real(tp * np.conjtp * facp)
                self.transmissivity_array_s[j][i] = np.real(ts * np.conjts * facs)
                self.emissivity_array_p[j][i] = 1.0 - self.reflectivity_array_p[j][i] - self.transmissivity_array_p[j][i]
                self.emissivity_array_s[j][i] = 1.0 - self.reflectivity_array_s[j][i] - self.transmissivity_array_s[j][i]

        return 1

    def thermal_emission(self):
        self.BBs = datalib.BB(self.lambda_array, self.T_ml)
        self.thermal_emission_array = self.BBs * self.emissivity_array
        return 1

    def thermal_emission_ea(self):
        self.BBs = datalib.BB(self.lambda_array, self.T_ml)
        for i in range(0, len(self.t)):
            for j in range(0, len(self.lambda_array)):
                self.thermal_emission_array_p[i][j] = self.BBs[j] * self.emissivity_array_p[i][j] * np.cosself.t[i]
                self.thermal_emission_array_s[i][j] = self.BBs[j] * self.emissivity_array_s[i][j] * np.cosself.t[i]

        return 1

    def stpv_se(self):
        self.spectral_efficiency_val = stpvlib.SpectralEfficiencyself.thermal_emission_arrayself.lambda_arrayself.lbg
        return 1

    def stpv_pd(self):
        self.power_density_val = stpvlib.Pwr_denself.thermal_emission_arrayself.lambda_arrayself.lbg
        return 1

    def stpv_etatpv(self):
        self.tpv_efficiency_val = stpvlib.Eta_TPV(self.thermal_emission_array, self.lambda_array, self.PV, self.T_cell)
        return 1

    def stpv_se_ea(self):
        self.spectral_efficiency_val = stpvlib.SpectralEfficiency_EA(self.thermal_emission_array_p, self.thermal_emission_array_s, self.lambda_array, self.lbg, self.t, self.w)

    def stpv_pd_ea(self):
        self.power_density_val = stpvlib.Pwr_den_EA(self.thermal_emission_array_p, self.thermal_emission_array_s, self.lambda_array, self.lbg, self.t, self.w)
        return 1

    def stpv_etatpv_ea(self):
        self.tpv_efficiency_val = stpvlib.Eta_TPV_EA(self.thermal_emission_array_p, self.thermal_emission_array_s, self.lambda_array, self.PV, self.T_cell, self.t, self.w)

    def stpv_etaabs(self):
        alpha = stpvlib.absorbed_power_ea(self.lambda_array, self.n, self.d, self.solarconc)
        beta = stpvlib.p_in(self.thermal_emission_array, self.lambda_array)
        print('alpha is ', alpha)
        print('beta is ', beta)
        self.absorber_efficiency_val = (alpha - beta) / alpha
        return 1

    def stpv_etaabs_ea(self):
        alpha = stpvlib.absorbed_power_ea(self.lambda_array, self.n, self.d, self.solarconc)
        beta = stpvlib.p_in_ea(self.thermal_emission_array_p, self.thermal_emission_array_s, self.lambda_array, self.t, self.w)
        self.absorber_efficiency_val = (alpha - beta) / alpha
        return 1

    def pv_conversion_efficiency(self):
        self.short_circuit_current_val = stpvlib.ambient_jscself.emissivity_arrayself.lambda_arrayself.lbg
        self.incident_power = stpvlib.integrated_solar_powerself.lambda_array
        self.conversion_efficiency_val = self.short_circuit_current_val * 0.828 * 0.706
        self.conversion_efficiency_val = self.conversion_efficiency_val / self.incident_power
        return 1

    def step_emissivity(self, lambda_0, delta_lambda):
        idx = 0
        for lam in self.lambda_array:
            if lam > lambda_0 - delta_lambda / 2 and lam < lambda_0 + delta_lambda / 2:
                self.emissivity_array[idx] = 1.0
                self.transmissivity_array[idx] = 0.0
                self.reflectivity_array[idx] = 0.0
                idx = idx + 1
            else:
                self.emissivity_array[idx] = 0.0
                self.transmissivity_array[idx] = 0.0
                self.reflectivity_array[idx] = 1.0
                idx = idx + 1

        return 1

    def step_emissivity_ea(self, lambda_0, delta_lambda):
        for j in range(0, len(self.t)):
            idx = -1
            for lam in self.lambda_array:
                idx = idx + 1
                if lam > lambda_0 - delta_lambda / 2 and lam < lambda_0 + delta_lambda / 2:
                    self.emissivity_array_p[j][idx] = 1.0
                    self.emissivity_array_s[j][idx] = 1.0
                    self.reflectivity_array_p[j][idx] = 0.0
                    self.reflectivity_array_s[j][idx] = 0.0
                    self.transmissivity_array_p[j][idx] = 0.0
                    self.transmissivity_array_s[j][idx] = 0.0
                else:
                    self.emissivity_array_p[j][idx] = 0.0
                    self.emissivity_array_s[j][idx] = 0.0
                    self.reflectivity_array_p[j][idx] = 1.0
                    self.reflectivity_array_s[j][idx] = 1.0
                    self.transmissivity_array_p[j][idx] = 0.0
                    self.transmissivity_array_s[j][idx] = 0.0

        return 1

    def step_reflectivity(self, lambda_0, delta_lambda):
        idx = 0
        for lam in self.lambda_array:
            if lam > lambda_0 - delta_lambda / 2 and lam < lambda_0 + delta_lambda / 2:
                self.emissivity_array[idx] = 0.0
                self.transmissivity_array[idx] = 0.0
                self.reflectivity_array[idx] = 1.0
                idx = idx + 1
            else:
                self.emissivity_array[idx] = 1.0
                self.transmissivity_array[idx] = 0.0
                self.reflectivity_array[idx] = 0.0
                idx = idx + 1

        return 1

    def thermal_color(self):
        string = 'Color at T = ' + str(self.T_ml) + ' K'
        colorlib.RenderColorself.thermal_emission_arrayself.lambda_arraystring
        self.thermal_rgb = colorlib.RGB_FromSpec(self.thermal_emission_array, self.lambda_array)
        return 1

    def ambient_color(self):
        string = 'Ambient Color'
        colorlib.RenderColorself.reflectivity_arrayself.lambda_arraystring
        self.reflective_rgb = colorlib.RGB_FromSpec(self.reflectivity_array, self.lambda_array)
        return 1

    def pure_color(self, wl):
        Spectrum = np.zeros_likeself.lambda_array
        for i in range(0, len(Spectrum)):
            if abs(self.lambda_array[i] - wl) < 5e-09:
                Spectrum[i] = 1

        colorlib.RenderColorSpectrumself.lambda_arraystr(wl)
        return 1

    def classify_color(self):
        self.color_name = colorlib.classify_color(self.reflectivity_array, self.lambda_array)

    def luminous_efficiency(self):
        self.luminous_efficiency_val = lightlib.Lum_efficiency(self.lambda_array, self.thermal_emission_array)
        return 1

    def luminous_efficiency_prime(self):
        self.luminous_efficiency_prime_val = lightlib.Lum_efficiency_primeself.lambda_arrayself.thermal_emission_array(self.BBs * self.emissivity_prime_array)

    def normalized_luminous_power(self):
        self.luminous_power_val = lightlib.normalized_powerself.lambda_arrayself.thermal_emission_arrayself.BBs
        return 1

    def cooling_power(self):
        self.radiative_power_val = coolinglib.Prad(self.thermal_emission_array_p, self.thermal_emission_array_s, self.lambda_array, self.t, self.w)
        self.atmospheric_power_val = coolinglib.Patm(self.emissivity_array_p, self.emissivity_array_s, self.T_amb, self.lambda_array, self.t, self.w)
        self.solar_power_val = coolinglib.Psun(self.theta_sun, self.lambda_array, self.n, self.d)
        self.cooling_power_val = self.radiative_power_val - self.atmospheric_power_val - self.solar_power_val
        return 1

    def insert_layer(self, layer_number, material, thickness):
        new_d = np.insertself.dlayer_numberthickness
        new_m = []
        for i in range(0, layer_number):
            new_m.appendself.matlist[i]

        new_m.appendmaterial
        for i in range(layer_number + 1, len(self.matlist) + 1):
            new_m.appendself.matlist[(i - 1)]

        self.d = None
        self.matlist = None
        self.n = None
        self.d = new_d
        self.matlist = new_m
        self.n = None
        self.n = np.zeros((len(self.d), len(self.lambda_array)), dtype=complex)
        for i in range(0, len(self.matlist)):
            self.n[:][i] = datalib.Material_RI(self.lambda_array, self.matlist[i])

        self.fresnel
        if self.explicit_angle:
            self.fresnel_ea
        else:
            if self.stpv_emitter_calc:
                self.thermal_emission
                self.stpv_se
                self.stpv_pd
                self.stpv_etatpv
                if self.explicit_angle:
                    self.thermal_emission_ea
                    self.stpv_se_ea
                    self.stpv_pd_ea
            if self.stpv_absorber_calc:
                self.thermal_emission
                if self.explicit_angle:
                    self.thermal_emission_ea
                    self.stpv_etaabs
                else:
                    self.stpv_etaabs
        return 1

    def layer_ri(self, layer):
        RI = np.zeros((len(self.lambda_array)), dtype=complex)
        for i in range(0, len(self.lambda_array)):
            RI[i] = self.n[layer][i]

        return RI

    def layer_alloy(self, layer, fraction, mat1, mat2, model):
        if model == 'Bruggeman':
            if isinstance(mat1, str):
                n_1 = datalib.Material_RI(self.lambda_array, mat1)
            else:
                n_1 = mat1
            n_2 = datalib.Material_RI(self.lambda_array, mat2)
            for i in range(0, len(self.lambda_array)):
                if isinstance(mat1, str):
                    eps1 = n_1[i] * n_1[i]
                else:
                    eps1 = n_1 * n_1
                eps2 = n_2[i] * n_2[i]
                flag = 1
                f1 = 1 - fraction
                f2 = fraction
                b = (2 * f1 - f2) * eps1 + (2 * f2 - f1) * eps2
                arg = 8 * eps1 * eps2 + b * b
                srarg = np.sqrtarg
                if np.imagarg < 0:
                    flag = -1
                else:
                    flag = 1
                epsBG = (b + flag * srarg) / 4.0
                self.n[layer][i] = np.sqrtepsBG

        else:
            if isinstance(mat1, str):
                n_1 = datalib.Material_RI(self.lambda_array, mat1)
            else:
                n_1 = mat1
            n_2 = datalib.Material_RI(self.lambda_array, mat2)
            f = fraction
            for i in range(0, len(self.lambda_array)):
                if isinstance(mat1, str):
                    epsD = n_1[i] * n_1[i]
                else:
                    epsD = n_1 * n_1
                epsM = n_2[i] * n_2[i]
                num = epsD * (2 * f * (epsM - epsD) + epsM + 2 * epsD)
                denom = 2 * epsD + epsM + f * (epsD - epsM)
                self.n[layer][i] = np.sqrt(num / denom)

        return 1

    def layer_static_ri(self, layer, RI):
        for i in range(0, len(self.lambda_array)):
            self.n[layer][i] = RI

        return 1

    def layer_lorentz(self, layer, omega_p, omega_0, gamma):
        c = 299792458.0
        ci = complex(0.0, 1.0)
        for i in range(0, len(self.lambda_array)):
            omega = 2 * np.pi * c / self.lambda_array[i]
            eps_lr = 1 + omega_p ** 2 / (omega_0 ** 2 - omega ** 2 - ci * omega * gamma)
            self.n[layer][i] = np.sqrteps_lr

        return 1

    def plot_te(self):
        plt.plot(self.lambda_array * 1000000000.0)self.thermal_emission_array'red'
        string = 'Thermal Emission at ' + str(self.T_ml) + ' K'
        plt.legendstring
        plt.show
        return 1

    def plot_reflectivity(self):
        plt.plot(self.lambda_array * 1000000000.0)self.reflectivity_array'red'
        string = 'Reflectivity'
        plt.legendstring
        plt.show
        return 1

    def plot_emissivity(self):
        plt.plot(self.lambda_array * 1000000000.0)self.emissivity_array'blue'
        string = 'Emissivity'
        plt.legend'Emissivity'
        plt.show
        return 1

    def find_spp(self, idx):
        k0 = np.pi * 2 / self.lambda_array[idx]
        L = len(self.d)
        nc = np.zeros(L, dtype=complex)
        for j in range(0, L):
            nc[j] = self.n[j][idx]

        b_beg = k0 * nc[(L - 1)]
        b_end = k0 * nc[0]
        a_beg = 1e-06
        a_end = 0.2 * b_end
        beta = np.linspaceb_begb_end100
        alpha = np.linspacea_bega_end100
        rr_max = -100
        rr_temp = 0
        a_spp = 0
        b_spp = 0
        for a in alpha:
            for b in beta:
                kx = b + a * complex(0.0, 1.0)
                rr_temp = tmm.tmm_ab(k0, kx, 'p', nc, self.d)
                if rr_temp > rr_max:
                    rr_max = rr_temp
                    a_spp = a
                    b_spp = b

        self.spp_resonance_val = b_spp + a_spp * complex(0.0, 1.0)
        return 1

    def find_pa(self, idx):
        k0 = np.pi * 2 / self.lambda_array[idx]
        L = len(self.d)
        nc = np.zeros(L, dtype=complex)
        for j in range(0, L):
            nc[j] = self.n[j][idx]

        b_beg = k0 * nc[(L - 1)]
        b_end = k0 * nc[0]
        a_beg = 1e-06
        a_end = 0.2 * b_end
        beta = np.linspaceb_begb_end100
        alpha = np.linspacea_bega_end100
        rr_min = 100
        rr_temp = 0
        a_spp = 0
        b_spp = 0
        for a in alpha:
            for b in beta:
                kx = b + a * complex(0.0, 1.0)
                rr_temp = tmm.tmm_ab(k0, kx, 'p', nc, self.d)
                if rr_temp < rr_min:
                    rr_min = rr_temp
                    a_spp = a
                    b_spp = b

        self.pa_resonance_val = b_spp + a_spp * complex(0.0, 1.0)
        return 1

    def inline_structure(self, args):
        if 'Lambda_List' in args:
            lamlist = args['Lambda_List']
            self.lambda_array = np.linspacelamlist[0]lamlist[1]int(lamlist[2])
        else:
            print(' Lambda array not specified! ')
            print(' Choosing default array of 1000 wl between 400 and 6000 nm')
            self.lambda_array = np.linspace4e-076e-061000
        if 'Thickness_List' in args:
            self.d = args['Thickness_List']
        else:
            print('  Thickness array not specified!')
            print('  Proceeding with default structure - optically thick W! ')
            self.d = [0, 9e-07, 0]
            self.matlist = ['Air', 'W', 'Air']
            self.n = np.zeros((len(self.d), len(self.lambda_array)), dtype=complex)
            for i in range(0, len(self.matlist)):
                self.n[:][i] = datalib.Material_RI(self.lambda_array, self.matlist[i])

        if 'Material_List' in args:
            self.matlist = args['Material_List']
            self.n = np.zeros((len(self.d), len(self.lambda_array)), dtype=complex)
            for i in range(0, len(self.matlist)):
                self.n[:][i] = datalib.Material_RI(self.lambda_array, self.matlist[i])

        else:
            print('  Material array not specified!')
            print('  Proceeding with default structure - optically thick W! ')
            self.d = [0, 9e-07, 0]
            self.matlist = ['Air', 'W', 'Air']
            self.n = np.zeros((len(self.d), len(self.lambda_array)), dtype=complex)
            for i in range(0, len(self.matlist)):
                self.n[:][i] = datalib.Material_RI(self.lambda_array, self.matlist[i])

        if 'Temperature' in args:
            self.T_ml = args['Temperature']
        else:
            if 'Structure_Temperature' in args:
                self.T_ml = args['Structure_Temperature']
            else:
                print(' Temperature not specified!')
                print(' Proceeding with default T = 300 K')
                self.T_ml = 300
        if 'PV_Temperature' in args:
            self.T_cell = args['PV_Temperature']
        else:
            self.T_cell = 300
        if 'Ambient_Temperature' in args:
            self.T_amb = args['Ambient_Temperature']
        else:
            self.T_amb = 300
        if 'STPV_EMIT' in args:
            self.stpv_emitter_calc = args['STPV_EMIT']
        else:
            self.stpv_emitter_calc = 0
        if 'STPV_ABS' in args:
            self.stpv_absorber_calc = args['STPV_ABS']
        else:
            self.stpv_absorber_calc = 0
        if 'COOLING' in args:
            self.cooling_calc = args['COOLING']
        else:
            self.cooling_calc = 0
        if 'LIGHTBULB' in args:
            self.lightbulb_calc = args['LIGHTBULB']
        else:
            self.lightbulb_calc = 0
        if 'COLOR' in args:
            self.color_calc = args['COLOR']
        else:
            self.color_calc = 0
        if 'EXPLICIT_ANGLE' in args:
            self.explicit_angle = args['EXPLICIT_ANGLE']
        else:
            self.explicit_angle = 0
        if 'DEG' in args:
            self.deg = args['DEG']
        else:
            self.deg = 7
        return 1