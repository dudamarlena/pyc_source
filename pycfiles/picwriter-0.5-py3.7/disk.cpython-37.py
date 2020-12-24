# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\disk.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 14074 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk

class Disk(tk.Component):
    __doc__ = " Disk Resonator Cell class.\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **radius** (float): Radius of the disk resonator\n           * **coupling_gap** (float): Distance between the bus waveguide and resonator\n\n        Keyword Args:\n           * **wrap_angle** (float): Angle in *radians* between 0 and pi (defaults to 0) that determines how much the bus waveguide wraps along the resonator.  0 corresponds to a straight bus waveguide, and pi corresponds to a bus waveguide wrapped around half of the resonator.\n           * **parity** (1 or -1): If 1, resonator to left of bus waveguide, if -1 resonator to the right\n           * **port** (tuple): Cartesian coordinate of the input port (x1, y1)\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output'] = {'port': (x2, y2), 'direction': 'dir2'}\n\n        Where in the above (x1,y1) is the same as the 'port' input, (x2, y2) is the end of the component, and 'dir1', 'dir2' are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n\n    "

    def __init__(self, wgt, radius, coupling_gap, wrap_angle=0, parity=1, port=(0, 0), direction='EAST'):
        tk.Component.__init__(self, 'Disk', locals())
        self.portlist = {}
        self.port = port
        self.direction = direction
        self.radius = radius
        self.coupling_gap = coupling_gap
        self.wrap_angle = wrap_angle
        if wrap_angle > np.pi or wrap_angle < 0:
            raise ValueError('Warning! Wrap_angle is nor a valid angle between 0 and pi.')
        self.parity = parity
        self.resist = wgt.resist
        self.wgt = wgt
        self.wg_spec = {'layer':wgt.wg_layer,  'datatype':wgt.wg_datatype}
        self.clad_spec = {'layer':wgt.clad_layer,  'datatype':wgt.clad_datatype}
        self._Disk__build_cell()
        self._Disk__build_ports()
        self._auto_transform_()

    def __build_cell--- This code section failed: ---

 L.  77         0  LOAD_FAST                'self'
                2  LOAD_ATTR                wrap_angle
                4  LOAD_CONST               0
                6  COMPARE_OP               ==
             8_10  POP_JUMP_IF_FALSE   490  'to 490'

 L.  78        12  LOAD_CONST               2
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                radius
               18  BINARY_MULTIPLY  
               20  STORE_FAST               'bus_length'

 L.  80        22  LOAD_GLOBAL              gdspy
               24  LOAD_METHOD              Path
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                wgt
               30  LOAD_ATTR                wg_width
               32  LOAD_CONST               (0, 0)
               34  CALL_METHOD_2         2  '2 positional arguments'
               36  STORE_FAST               'path'

 L.  81        38  LOAD_FAST                'path'
               40  LOAD_ATTR                segment
               42  LOAD_CONST               2
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                radius
               48  BINARY_MULTIPLY  
               50  BUILD_TUPLE_1         1 
               52  LOAD_STR                 'direction'
               54  LOAD_STR                 '+x'
               56  BUILD_MAP_1           1 
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                wg_spec
               62  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               64  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               66  POP_TOP          

 L.  82        68  LOAD_GLOBAL              gdspy
               70  LOAD_METHOD              Path
               72  LOAD_CONST               2
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                wgt
               78  LOAD_ATTR                clad_width
               80  BINARY_MULTIPLY  
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                wgt
               86  LOAD_ATTR                wg_width
               88  BINARY_ADD       
               90  LOAD_CONST               (0, 0)
               92  CALL_METHOD_2         2  '2 positional arguments'
               94  STORE_FAST               'clad'

 L.  83        96  LOAD_FAST                'clad'
               98  LOAD_ATTR                segment
              100  LOAD_CONST               2
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                radius
              106  BINARY_MULTIPLY  
              108  BUILD_TUPLE_1         1 
              110  LOAD_STR                 'direction'
              112  LOAD_STR                 '+x'
              114  BUILD_MAP_1           1 
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                clad_spec
              120  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              122  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              124  POP_TOP          

 L.  86       126  LOAD_FAST                'self'
              128  LOAD_ATTR                parity
              130  LOAD_CONST               1
              132  COMPARE_OP               ==
          134_136  POP_JUMP_IF_FALSE   300  'to 300'

 L.  87       138  LOAD_GLOBAL              gdspy
              140  LOAD_ATTR                Round

 L.  89       142  LOAD_FAST                'self'
              144  LOAD_ATTR                radius

 L.  90       146  LOAD_FAST                'self'
              148  LOAD_ATTR                radius
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                wgt
              154  LOAD_ATTR                wg_width
              156  LOAD_CONST               2.0
              158  BINARY_TRUE_DIVIDE
              160  BINARY_ADD       
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                coupling_gap
              166  BINARY_ADD       
              168  BUILD_TUPLE_2         2 

 L.  92       170  LOAD_FAST                'self'
              172  LOAD_ATTR                radius
              174  BUILD_TUPLE_2         2 
              176  LOAD_STR                 'number_of_points'

 L.  93       178  LOAD_FAST                'self'
              180  LOAD_ATTR                wgt
              182  LOAD_METHOD              get_num_points_curve

 L.  94       184  LOAD_CONST               2
              186  LOAD_GLOBAL              np
              188  LOAD_ATTR                pi
              190  BINARY_MULTIPLY  
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                radius
              196  CALL_METHOD_2         2  '2 positional arguments'
              198  BUILD_MAP_1           1 

 L.  96       200  LOAD_FAST                'self'
              202  LOAD_ATTR                wg_spec
              204  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              206  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              208  STORE_FAST               'ring'

 L.  98       210  LOAD_GLOBAL              gdspy
              212  LOAD_ATTR                Round

 L. 100       214  LOAD_FAST                'self'
              216  LOAD_ATTR                radius

 L. 101       218  LOAD_FAST                'self'
              220  LOAD_ATTR                radius
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                wgt
              226  LOAD_ATTR                wg_width
              228  LOAD_CONST               2.0
              230  BINARY_TRUE_DIVIDE
              232  BINARY_ADD       
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                coupling_gap
              238  BINARY_ADD       
              240  BUILD_TUPLE_2         2 

 L. 103       242  LOAD_FAST                'self'
              244  LOAD_ATTR                radius
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                wgt
              250  LOAD_ATTR                clad_width
              252  BINARY_ADD       
              254  BUILD_TUPLE_2         2 
              256  LOAD_STR                 'number_of_points'

 L. 104       258  LOAD_FAST                'self'
              260  LOAD_ATTR                wgt
              262  LOAD_METHOD              get_num_points_curve

 L. 105       264  LOAD_CONST               2
              266  LOAD_GLOBAL              np
              268  LOAD_ATTR                pi
              270  BINARY_MULTIPLY  
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                radius
              276  LOAD_FAST                'self'
              278  LOAD_ATTR                wgt
              280  LOAD_ATTR                clad_width
              282  BINARY_ADD       
              284  CALL_METHOD_2         2  '2 positional arguments'
              286  BUILD_MAP_1           1 

 L. 107       288  LOAD_FAST                'self'
              290  LOAD_ATTR                clad_spec
              292  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              294  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              296  STORE_FAST               'clad_ring'
              298  JUMP_FORWARD       1952  'to 1952'
            300_0  COME_FROM           134  '134'

 L. 109       300  LOAD_FAST                'self'
              302  LOAD_ATTR                parity
              304  LOAD_CONST               -1
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_FALSE   478  'to 478'

 L. 110       312  LOAD_GLOBAL              gdspy
              314  LOAD_ATTR                Round

 L. 112       316  LOAD_FAST                'self'
              318  LOAD_ATTR                radius

 L. 113       320  LOAD_FAST                'self'
              322  LOAD_ATTR                radius
              324  UNARY_NEGATIVE   
              326  LOAD_FAST                'self'
              328  LOAD_ATTR                wgt
              330  LOAD_ATTR                wg_width
              332  LOAD_CONST               2.0
              334  BINARY_TRUE_DIVIDE
              336  BINARY_SUBTRACT  
              338  LOAD_FAST                'self'
              340  LOAD_ATTR                coupling_gap
              342  BINARY_SUBTRACT  
              344  BUILD_TUPLE_2         2 

 L. 115       346  LOAD_FAST                'self'
              348  LOAD_ATTR                radius
              350  BUILD_TUPLE_2         2 
              352  LOAD_STR                 'number_of_points'

 L. 116       354  LOAD_FAST                'self'
              356  LOAD_ATTR                wgt
              358  LOAD_METHOD              get_num_points_curve

 L. 117       360  LOAD_CONST               2
              362  LOAD_GLOBAL              np
              364  LOAD_ATTR                pi
              366  BINARY_MULTIPLY  
              368  LOAD_FAST                'self'
              370  LOAD_ATTR                radius
              372  CALL_METHOD_2         2  '2 positional arguments'
              374  BUILD_MAP_1           1 

 L. 119       376  LOAD_FAST                'self'
              378  LOAD_ATTR                wg_spec
              380  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              382  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              384  STORE_FAST               'ring'

 L. 121       386  LOAD_GLOBAL              gdspy
              388  LOAD_ATTR                Round

 L. 123       390  LOAD_FAST                'self'
              392  LOAD_ATTR                radius

 L. 124       394  LOAD_FAST                'self'
              396  LOAD_ATTR                radius
              398  UNARY_NEGATIVE   
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                wgt
              404  LOAD_ATTR                wg_width
              406  LOAD_CONST               2.0
              408  BINARY_TRUE_DIVIDE
              410  BINARY_SUBTRACT  
              412  LOAD_FAST                'self'
              414  LOAD_ATTR                coupling_gap
              416  BINARY_SUBTRACT  
              418  BUILD_TUPLE_2         2 

 L. 126       420  LOAD_FAST                'self'
              422  LOAD_ATTR                radius
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                wgt
              428  LOAD_ATTR                clad_width
              430  BINARY_ADD       
              432  BUILD_TUPLE_2         2 
              434  LOAD_STR                 'number_of_points'

 L. 127       436  LOAD_FAST                'self'
              438  LOAD_ATTR                wgt
              440  LOAD_METHOD              get_num_points_curve

 L. 128       442  LOAD_CONST               2
              444  LOAD_GLOBAL              np
              446  LOAD_ATTR                pi
              448  BINARY_MULTIPLY  
              450  LOAD_FAST                'self'
              452  LOAD_ATTR                radius
              454  LOAD_FAST                'self'
              456  LOAD_ATTR                wgt
              458  LOAD_ATTR                clad_width
              460  BINARY_ADD       
              462  CALL_METHOD_2         2  '2 positional arguments'
              464  BUILD_MAP_1           1 

 L. 130       466  LOAD_FAST                'self'
              468  LOAD_ATTR                clad_spec
              470  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              472  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              474  STORE_FAST               'clad_ring'
              476  JUMP_FORWARD       1952  'to 1952'
            478_0  COME_FROM           308  '308'

 L. 133       478  LOAD_GLOBAL              ValueError

 L. 134       480  LOAD_STR                 'Warning!  Parity value is not an acceptable value (must be +1 or -1).'
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  RAISE_VARARGS_1       1  'exception instance'
          486_488  JUMP_FORWARD       1952  'to 1952'
            490_0  COME_FROM             8  '8'

 L. 136       490  LOAD_FAST                'self'
              492  LOAD_ATTR                wrap_angle
              494  LOAD_CONST               0
              496  COMPARE_OP               >
          498_500  POP_JUMP_IF_FALSE  1952  'to 1952'

 L. 137       502  LOAD_FAST                'self'
              504  LOAD_ATTR                wrap_angle
              506  LOAD_CONST               2.0
              508  BINARY_TRUE_DIVIDE
              510  STORE_FAST               'theta'

 L. 138       512  LOAD_FAST                'self'
              514  LOAD_ATTR                radius
              516  LOAD_FAST                'self'
              518  LOAD_ATTR                wgt
              520  LOAD_ATTR                wg_width
              522  LOAD_CONST               2.0
              524  BINARY_TRUE_DIVIDE
              526  BINARY_ADD       
              528  LOAD_FAST                'self'
              530  LOAD_ATTR                coupling_gap
              532  BINARY_ADD       
              534  STORE_FAST               'rp'

 L. 139       536  LOAD_FAST                'rp'
              538  LOAD_GLOBAL              np
              540  LOAD_METHOD              sin
              542  LOAD_FAST                'theta'
              544  CALL_METHOD_1         1  '1 positional argument'
              546  BINARY_MULTIPLY  
              548  LOAD_FAST                'rp'
              550  LOAD_FAST                'rp'
              552  LOAD_GLOBAL              np
              554  LOAD_METHOD              cos
              556  LOAD_FAST                'theta'
              558  CALL_METHOD_1         1  '1 positional argument'
              560  BINARY_MULTIPLY  
              562  BINARY_SUBTRACT  
              564  ROT_TWO          
              566  STORE_FAST               'dx'
              568  STORE_FAST               'dy'

 L. 140       570  LOAD_CONST               4
              572  LOAD_FAST                'dx'
              574  BINARY_MULTIPLY  
              576  LOAD_CONST               2
              578  LOAD_FAST                'self'
              580  LOAD_ATTR                radius
              582  BINARY_MULTIPLY  
              584  COMPARE_OP               <
          586_588  POP_JUMP_IF_FALSE   600  'to 600'
              590  LOAD_CONST               2
              592  LOAD_FAST                'self'
              594  LOAD_ATTR                radius
              596  BINARY_MULTIPLY  
              598  JUMP_FORWARD        606  'to 606'
            600_0  COME_FROM           586  '586'
              600  LOAD_CONST               4
              602  LOAD_FAST                'dx'
              604  BINARY_MULTIPLY  
            606_0  COME_FROM           598  '598'
              606  STORE_FAST               'bus_length'

 L. 143       608  LOAD_GLOBAL              gdspy
              610  LOAD_METHOD              Path
              612  LOAD_FAST                'self'
              614  LOAD_ATTR                wgt
              616  LOAD_ATTR                wg_width
              618  LOAD_CONST               (0, 0)
              620  CALL_METHOD_2         2  '2 positional arguments'
              622  STORE_FAST               'path'

 L. 144       624  LOAD_GLOBAL              gdspy
              626  LOAD_METHOD              Path
              628  LOAD_CONST               2
              630  LOAD_FAST                'self'
              632  LOAD_ATTR                wgt
              634  LOAD_ATTR                clad_width
              636  BINARY_MULTIPLY  
              638  LOAD_FAST                'self'
              640  LOAD_ATTR                wgt
              642  LOAD_ATTR                wg_width
              644  BINARY_ADD       
              646  LOAD_CONST               (0, 0)
              648  CALL_METHOD_2         2  '2 positional arguments'
              650  STORE_FAST               'clad'

 L. 145       652  LOAD_CONST               4
              654  LOAD_FAST                'dx'
              656  BINARY_MULTIPLY  
              658  LOAD_FAST                'bus_length'
              660  COMPARE_OP               <
          662_664  POP_JUMP_IF_FALSE   746  'to 746'

 L. 146       666  LOAD_FAST                'path'
              668  LOAD_ATTR                segment

 L. 147       670  LOAD_FAST                'bus_length'
              672  LOAD_CONST               4
              674  LOAD_FAST                'dx'
              676  BINARY_MULTIPLY  
              678  BINARY_SUBTRACT  
              680  LOAD_CONST               2.0
              682  BINARY_TRUE_DIVIDE
              684  BUILD_TUPLE_1         1 
              686  LOAD_STR                 'direction'
              688  LOAD_STR                 '+x'
              690  BUILD_MAP_1           1 
              692  LOAD_FAST                'self'
              694  LOAD_ATTR                wg_spec
              696  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              698  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              700  POP_TOP          

 L. 149       702  LOAD_FAST                'clad'
              704  LOAD_ATTR                segment

 L. 150       706  LOAD_FAST                'bus_length'
              708  LOAD_CONST               4
              710  LOAD_FAST                'dx'
              712  BINARY_MULTIPLY  
              714  BINARY_SUBTRACT  
              716  LOAD_CONST               2.0
              718  BINARY_TRUE_DIVIDE
              720  BUILD_TUPLE_1         1 
              722  LOAD_STR                 'direction'
              724  LOAD_STR                 '+x'
              726  BUILD_MAP_1           1 
              728  LOAD_FAST                'self'
              730  LOAD_ATTR                clad_spec
              732  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              734  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              736  POP_TOP          

 L. 152       738  LOAD_FAST                'self'
              740  LOAD_ATTR                radius
              742  STORE_FAST               'xcenter'
              744  JUMP_FORWARD        754  'to 754'
            746_0  COME_FROM           662  '662'

 L. 154       746  LOAD_CONST               2
              748  LOAD_FAST                'dx'
              750  BINARY_MULTIPLY  
              752  STORE_FAST               'xcenter'
            754_0  COME_FROM           744  '744'

 L. 156       754  LOAD_FAST                'self'
              756  LOAD_ATTR                parity
              758  LOAD_CONST               1
              760  COMPARE_OP               ==
          762_764  POP_JUMP_IF_FALSE  1314  'to 1314'

 L. 157       766  LOAD_FAST                'path'
              768  LOAD_ATTR                arc

 L. 158       770  LOAD_FAST                'rp'

 L. 159       772  LOAD_GLOBAL              np
              774  LOAD_ATTR                pi
              776  LOAD_CONST               2.0
              778  BINARY_TRUE_DIVIDE

 L. 160       780  LOAD_GLOBAL              np
              782  LOAD_ATTR                pi
              784  LOAD_CONST               2.0
              786  BINARY_TRUE_DIVIDE
              788  LOAD_FAST                'theta'
              790  BINARY_SUBTRACT  
              792  BUILD_TUPLE_3         3 
              794  LOAD_STR                 'number_of_points'

 L. 161       796  LOAD_CONST               2
              798  LOAD_FAST                'self'
              800  LOAD_ATTR                wgt
              802  LOAD_METHOD              get_num_points_curve
              804  LOAD_FAST                'theta'
              806  LOAD_FAST                'rp'
              808  CALL_METHOD_2         2  '2 positional arguments'
              810  BINARY_MULTIPLY  
              812  BUILD_MAP_1           1 

 L. 162       814  LOAD_FAST                'self'
              816  LOAD_ATTR                wg_spec
              818  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              820  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              822  POP_TOP          

 L. 164       824  LOAD_FAST                'path'
              826  LOAD_ATTR                arc

 L. 165       828  LOAD_FAST                'rp'

 L. 166       830  LOAD_GLOBAL              np
              832  LOAD_ATTR                pi
              834  UNARY_NEGATIVE   
              836  LOAD_CONST               2.0
              838  BINARY_TRUE_DIVIDE
              840  LOAD_FAST                'theta'
              842  BINARY_SUBTRACT  

 L. 167       844  LOAD_GLOBAL              np
              846  LOAD_ATTR                pi
              848  UNARY_NEGATIVE   
              850  LOAD_CONST               2.0
              852  BINARY_TRUE_DIVIDE
              854  LOAD_FAST                'theta'
              856  BINARY_ADD       
              858  BUILD_TUPLE_3         3 
              860  LOAD_STR                 'number_of_points'

 L. 168       862  LOAD_CONST               2
              864  LOAD_FAST                'self'
              866  LOAD_ATTR                wgt
              868  LOAD_METHOD              get_num_points_curve
              870  LOAD_CONST               2
              872  LOAD_FAST                'theta'
              874  BINARY_MULTIPLY  
              876  LOAD_FAST                'rp'
              878  CALL_METHOD_2         2  '2 positional arguments'
              880  BINARY_MULTIPLY  
              882  BUILD_MAP_1           1 

 L. 169       884  LOAD_FAST                'self'
              886  LOAD_ATTR                wg_spec
              888  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              890  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              892  POP_TOP          

 L. 171       894  LOAD_FAST                'path'
              896  LOAD_ATTR                arc

 L. 172       898  LOAD_FAST                'rp'

 L. 173       900  LOAD_GLOBAL              np
              902  LOAD_ATTR                pi
              904  LOAD_CONST               2.0
              906  BINARY_TRUE_DIVIDE
              908  LOAD_FAST                'theta'
              910  BINARY_ADD       

 L. 174       912  LOAD_GLOBAL              np
              914  LOAD_ATTR                pi
              916  LOAD_CONST               2.0
              918  BINARY_TRUE_DIVIDE
              920  BUILD_TUPLE_3         3 
              922  LOAD_STR                 'number_of_points'

 L. 175       924  LOAD_CONST               2
              926  LOAD_FAST                'self'
              928  LOAD_ATTR                wgt
              930  LOAD_METHOD              get_num_points_curve
              932  LOAD_FAST                'theta'
              934  LOAD_FAST                'rp'
              936  CALL_METHOD_2         2  '2 positional arguments'
              938  BINARY_MULTIPLY  
              940  BUILD_MAP_1           1 

 L. 176       942  LOAD_FAST                'self'
              944  LOAD_ATTR                wg_spec
              946  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              948  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              950  POP_TOP          

 L. 178       952  LOAD_FAST                'clad'
              954  LOAD_ATTR                arc

 L. 179       956  LOAD_FAST                'rp'

 L. 180       958  LOAD_GLOBAL              np
              960  LOAD_ATTR                pi
              962  LOAD_CONST               2.0
              964  BINARY_TRUE_DIVIDE

 L. 181       966  LOAD_GLOBAL              np
              968  LOAD_ATTR                pi
              970  LOAD_CONST               2.0
              972  BINARY_TRUE_DIVIDE
              974  LOAD_FAST                'theta'
              976  BINARY_SUBTRACT  
              978  BUILD_TUPLE_3         3 
              980  LOAD_STR                 'number_of_points'

 L. 182       982  LOAD_CONST               2
              984  LOAD_FAST                'self'
              986  LOAD_ATTR                wgt
              988  LOAD_METHOD              get_num_points_curve
              990  LOAD_FAST                'theta'
              992  LOAD_FAST                'rp'
              994  CALL_METHOD_2         2  '2 positional arguments'
              996  BINARY_MULTIPLY  
              998  BUILD_MAP_1           1 

 L. 183      1000  LOAD_FAST                'self'
             1002  LOAD_ATTR                clad_spec
             1004  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1006  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1008  POP_TOP          

 L. 185      1010  LOAD_FAST                'clad'
             1012  LOAD_ATTR                arc

 L. 186      1014  LOAD_FAST                'rp'

 L. 187      1016  LOAD_GLOBAL              np
             1018  LOAD_ATTR                pi
             1020  UNARY_NEGATIVE   
             1022  LOAD_CONST               2.0
             1024  BINARY_TRUE_DIVIDE
             1026  LOAD_FAST                'theta'
             1028  BINARY_SUBTRACT  

 L. 188      1030  LOAD_GLOBAL              np
             1032  LOAD_ATTR                pi
             1034  UNARY_NEGATIVE   
             1036  LOAD_CONST               2.0
             1038  BINARY_TRUE_DIVIDE
             1040  LOAD_FAST                'theta'
             1042  BINARY_ADD       
             1044  BUILD_TUPLE_3         3 
             1046  LOAD_STR                 'number_of_points'

 L. 189      1048  LOAD_CONST               2
             1050  LOAD_FAST                'self'
             1052  LOAD_ATTR                wgt
             1054  LOAD_METHOD              get_num_points_curve
             1056  LOAD_CONST               2
             1058  LOAD_FAST                'theta'
             1060  BINARY_MULTIPLY  
             1062  LOAD_FAST                'rp'
             1064  CALL_METHOD_2         2  '2 positional arguments'
             1066  BINARY_MULTIPLY  
             1068  BUILD_MAP_1           1 

 L. 190      1070  LOAD_FAST                'self'
             1072  LOAD_ATTR                clad_spec
             1074  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1076  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1078  POP_TOP          

 L. 192      1080  LOAD_FAST                'clad'
             1082  LOAD_ATTR                arc

 L. 193      1084  LOAD_FAST                'rp'

 L. 194      1086  LOAD_GLOBAL              np
             1088  LOAD_ATTR                pi
             1090  LOAD_CONST               2.0
             1092  BINARY_TRUE_DIVIDE
             1094  LOAD_FAST                'theta'
             1096  BINARY_ADD       

 L. 195      1098  LOAD_GLOBAL              np
             1100  LOAD_ATTR                pi
             1102  LOAD_CONST               2.0
             1104  BINARY_TRUE_DIVIDE
             1106  BUILD_TUPLE_3         3 
             1108  LOAD_STR                 'number_of_points'

 L. 196      1110  LOAD_CONST               2
             1112  LOAD_FAST                'self'
             1114  LOAD_ATTR                wgt
             1116  LOAD_METHOD              get_num_points_curve
             1118  LOAD_FAST                'theta'
             1120  LOAD_FAST                'rp'
             1122  CALL_METHOD_2         2  '2 positional arguments'
             1124  BINARY_MULTIPLY  
             1126  BUILD_MAP_1           1 

 L. 197      1128  LOAD_FAST                'self'
             1130  LOAD_ATTR                clad_spec
             1132  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1134  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1136  POP_TOP          

 L. 201      1138  LOAD_GLOBAL              gdspy
             1140  LOAD_ATTR                Round

 L. 203      1142  LOAD_FAST                'xcenter'

 L. 207      1144  LOAD_FAST                'self'
             1146  LOAD_ATTR                radius
             1148  LOAD_FAST                'self'
             1150  LOAD_ATTR                wgt
             1152  LOAD_ATTR                wg_width
             1154  LOAD_CONST               2.0
             1156  BINARY_TRUE_DIVIDE
             1158  BINARY_ADD       
             1160  LOAD_FAST                'self'
             1162  LOAD_ATTR                coupling_gap
             1164  BINARY_ADD       
             1166  LOAD_CONST               2
             1168  LOAD_FAST                'dy'
             1170  BINARY_MULTIPLY  
             1172  BINARY_SUBTRACT  
             1174  BUILD_TUPLE_2         2 

 L. 209      1176  LOAD_FAST                'self'
             1178  LOAD_ATTR                radius
             1180  BUILD_TUPLE_2         2 
             1182  LOAD_STR                 'number_of_points'

 L. 210      1184  LOAD_FAST                'self'
             1186  LOAD_ATTR                wgt
             1188  LOAD_METHOD              get_num_points_curve

 L. 211      1190  LOAD_CONST               2
             1192  LOAD_GLOBAL              np
             1194  LOAD_ATTR                pi
             1196  BINARY_MULTIPLY  
             1198  LOAD_FAST                'self'
             1200  LOAD_ATTR                radius
             1202  CALL_METHOD_2         2  '2 positional arguments'
             1204  BUILD_MAP_1           1 

 L. 213      1206  LOAD_FAST                'self'
             1208  LOAD_ATTR                wg_spec
             1210  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1212  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1214  STORE_FAST               'ring'

 L. 215      1216  LOAD_GLOBAL              gdspy
             1218  LOAD_ATTR                Round

 L. 217      1220  LOAD_FAST                'xcenter'

 L. 221      1222  LOAD_FAST                'self'
             1224  LOAD_ATTR                radius
             1226  LOAD_FAST                'self'
             1228  LOAD_ATTR                wgt
             1230  LOAD_ATTR                wg_width
             1232  LOAD_CONST               2.0
             1234  BINARY_TRUE_DIVIDE
             1236  BINARY_ADD       
             1238  LOAD_FAST                'self'
             1240  LOAD_ATTR                coupling_gap
             1242  BINARY_ADD       
             1244  LOAD_CONST               2
             1246  LOAD_FAST                'dy'
             1248  BINARY_MULTIPLY  
             1250  BINARY_SUBTRACT  
             1252  BUILD_TUPLE_2         2 

 L. 223      1254  LOAD_FAST                'self'
             1256  LOAD_ATTR                radius
             1258  LOAD_FAST                'self'
             1260  LOAD_ATTR                wgt
             1262  LOAD_ATTR                clad_width
             1264  BINARY_ADD       
             1266  BUILD_TUPLE_2         2 
             1268  LOAD_STR                 'number_of_points'

 L. 224      1270  LOAD_FAST                'self'
             1272  LOAD_ATTR                wgt
             1274  LOAD_METHOD              get_num_points_curve

 L. 225      1276  LOAD_CONST               2
             1278  LOAD_GLOBAL              np
             1280  LOAD_ATTR                pi
             1282  BINARY_MULTIPLY  
             1284  LOAD_FAST                'self'
             1286  LOAD_ATTR                radius
             1288  LOAD_FAST                'self'
             1290  LOAD_ATTR                wgt
             1292  LOAD_ATTR                clad_width
             1294  BINARY_ADD       
             1296  CALL_METHOD_2         2  '2 positional arguments'
             1298  BUILD_MAP_1           1 

 L. 227      1300  LOAD_FAST                'self'
             1302  LOAD_ATTR                clad_spec
             1304  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1306  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1308  STORE_FAST               'clad_ring'
         1310_1312  JUMP_FORWARD       1882  'to 1882'
           1314_0  COME_FROM           762  '762'

 L. 230      1314  LOAD_FAST                'self'
             1316  LOAD_ATTR                parity
             1318  LOAD_CONST               -1
             1320  COMPARE_OP               ==
         1322_1324  POP_JUMP_IF_FALSE  1882  'to 1882'

 L. 231      1326  LOAD_FAST                'path'
             1328  LOAD_ATTR                arc

 L. 232      1330  LOAD_FAST                'rp'

 L. 233      1332  LOAD_GLOBAL              np
             1334  LOAD_ATTR                pi
             1336  UNARY_NEGATIVE   
             1338  LOAD_CONST               2.0
             1340  BINARY_TRUE_DIVIDE

 L. 234      1342  LOAD_GLOBAL              np
             1344  LOAD_ATTR                pi
             1346  UNARY_NEGATIVE   
             1348  LOAD_CONST               2.0
             1350  BINARY_TRUE_DIVIDE
             1352  LOAD_FAST                'theta'
             1354  BINARY_ADD       
             1356  BUILD_TUPLE_3         3 
             1358  LOAD_STR                 'number_of_points'

 L. 235      1360  LOAD_CONST               2
             1362  LOAD_FAST                'self'
             1364  LOAD_ATTR                wgt
             1366  LOAD_METHOD              get_num_points_curve
             1368  LOAD_FAST                'theta'
             1370  LOAD_FAST                'rp'
             1372  CALL_METHOD_2         2  '2 positional arguments'
             1374  BINARY_MULTIPLY  
             1376  BUILD_MAP_1           1 

 L. 236      1378  LOAD_FAST                'self'
             1380  LOAD_ATTR                wg_spec
             1382  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1384  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1386  POP_TOP          

 L. 238      1388  LOAD_FAST                'path'
             1390  LOAD_ATTR                arc

 L. 239      1392  LOAD_FAST                'rp'

 L. 240      1394  LOAD_GLOBAL              np
             1396  LOAD_ATTR                pi
             1398  LOAD_CONST               2.0
             1400  BINARY_TRUE_DIVIDE
             1402  LOAD_FAST                'theta'
             1404  BINARY_ADD       

 L. 241      1406  LOAD_GLOBAL              np
             1408  LOAD_ATTR                pi
             1410  LOAD_CONST               2.0
             1412  BINARY_TRUE_DIVIDE
             1414  LOAD_FAST                'theta'
             1416  BINARY_SUBTRACT  
             1418  BUILD_TUPLE_3         3 
             1420  LOAD_STR                 'number_of_points'

 L. 242      1422  LOAD_CONST               2
             1424  LOAD_FAST                'self'
             1426  LOAD_ATTR                wgt
             1428  LOAD_METHOD              get_num_points_curve
             1430  LOAD_CONST               2
             1432  LOAD_FAST                'theta'
             1434  BINARY_MULTIPLY  
             1436  LOAD_FAST                'rp'
             1438  CALL_METHOD_2         2  '2 positional arguments'
             1440  BINARY_MULTIPLY  
             1442  BUILD_MAP_1           1 

 L. 243      1444  LOAD_FAST                'self'
             1446  LOAD_ATTR                wg_spec
             1448  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1450  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1452  POP_TOP          

 L. 245      1454  LOAD_FAST                'path'
             1456  LOAD_ATTR                arc

 L. 246      1458  LOAD_FAST                'rp'

 L. 247      1460  LOAD_GLOBAL              np
             1462  LOAD_ATTR                pi
             1464  UNARY_NEGATIVE   
             1466  LOAD_CONST               2.0
             1468  BINARY_TRUE_DIVIDE
             1470  LOAD_FAST                'theta'
             1472  BINARY_SUBTRACT  

 L. 248      1474  LOAD_GLOBAL              np
             1476  LOAD_ATTR                pi
             1478  UNARY_NEGATIVE   
             1480  LOAD_CONST               2.0
             1482  BINARY_TRUE_DIVIDE
             1484  BUILD_TUPLE_3         3 
             1486  LOAD_STR                 'number_of_points'

 L. 249      1488  LOAD_CONST               2
             1490  LOAD_FAST                'self'
             1492  LOAD_ATTR                wgt
             1494  LOAD_METHOD              get_num_points_curve
             1496  LOAD_FAST                'theta'
             1498  LOAD_FAST                'rp'
             1500  CALL_METHOD_2         2  '2 positional arguments'
             1502  BINARY_MULTIPLY  
             1504  BUILD_MAP_1           1 

 L. 250      1506  LOAD_FAST                'self'
             1508  LOAD_ATTR                wg_spec
             1510  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1512  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1514  POP_TOP          

 L. 252      1516  LOAD_FAST                'clad'
             1518  LOAD_ATTR                arc

 L. 253      1520  LOAD_FAST                'rp'

 L. 254      1522  LOAD_GLOBAL              np
             1524  LOAD_ATTR                pi
             1526  UNARY_NEGATIVE   
             1528  LOAD_CONST               2.0
             1530  BINARY_TRUE_DIVIDE

 L. 255      1532  LOAD_GLOBAL              np
             1534  LOAD_ATTR                pi
             1536  UNARY_NEGATIVE   
             1538  LOAD_CONST               2.0
             1540  BINARY_TRUE_DIVIDE
             1542  LOAD_FAST                'theta'
             1544  BINARY_ADD       
             1546  BUILD_TUPLE_3         3 
             1548  LOAD_STR                 'number_of_points'

 L. 256      1550  LOAD_CONST               2
             1552  LOAD_FAST                'self'
             1554  LOAD_ATTR                wgt
             1556  LOAD_METHOD              get_num_points_curve
             1558  LOAD_FAST                'theta'
             1560  LOAD_FAST                'rp'
             1562  CALL_METHOD_2         2  '2 positional arguments'
             1564  BINARY_MULTIPLY  
             1566  BUILD_MAP_1           1 

 L. 257      1568  LOAD_FAST                'self'
             1570  LOAD_ATTR                clad_spec
             1572  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1574  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1576  POP_TOP          

 L. 259      1578  LOAD_FAST                'clad'
             1580  LOAD_ATTR                arc

 L. 260      1582  LOAD_FAST                'rp'

 L. 261      1584  LOAD_GLOBAL              np
             1586  LOAD_ATTR                pi
             1588  LOAD_CONST               2.0
             1590  BINARY_TRUE_DIVIDE
             1592  LOAD_FAST                'theta'
             1594  BINARY_ADD       

 L. 262      1596  LOAD_GLOBAL              np
             1598  LOAD_ATTR                pi
             1600  LOAD_CONST               2.0
             1602  BINARY_TRUE_DIVIDE
             1604  LOAD_FAST                'theta'
             1606  BINARY_SUBTRACT  
             1608  BUILD_TUPLE_3         3 
             1610  LOAD_STR                 'number_of_points'

 L. 263      1612  LOAD_CONST               2
             1614  LOAD_FAST                'self'
             1616  LOAD_ATTR                wgt
             1618  LOAD_METHOD              get_num_points_curve
             1620  LOAD_CONST               2
             1622  LOAD_FAST                'theta'
             1624  BINARY_MULTIPLY  
             1626  LOAD_FAST                'rp'
             1628  CALL_METHOD_2         2  '2 positional arguments'
             1630  BINARY_MULTIPLY  
             1632  BUILD_MAP_1           1 

 L. 264      1634  LOAD_FAST                'self'
             1636  LOAD_ATTR                clad_spec
             1638  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1640  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1642  POP_TOP          

 L. 266      1644  LOAD_FAST                'clad'
             1646  LOAD_ATTR                arc

 L. 267      1648  LOAD_FAST                'rp'

 L. 268      1650  LOAD_GLOBAL              np
             1652  LOAD_ATTR                pi
             1654  UNARY_NEGATIVE   
             1656  LOAD_CONST               2.0
             1658  BINARY_TRUE_DIVIDE
             1660  LOAD_FAST                'theta'
             1662  BINARY_SUBTRACT  

 L. 269      1664  LOAD_GLOBAL              np
             1666  LOAD_ATTR                pi
             1668  UNARY_NEGATIVE   
             1670  LOAD_CONST               2.0
             1672  BINARY_TRUE_DIVIDE
             1674  BUILD_TUPLE_3         3 
             1676  LOAD_STR                 'number_of_points'

 L. 270      1678  LOAD_CONST               2
             1680  LOAD_FAST                'self'
             1682  LOAD_ATTR                wgt
             1684  LOAD_METHOD              get_num_points_curve
             1686  LOAD_FAST                'theta'
             1688  LOAD_FAST                'rp'
             1690  CALL_METHOD_2         2  '2 positional arguments'
             1692  BINARY_MULTIPLY  
             1694  BUILD_MAP_1           1 

 L. 271      1696  LOAD_FAST                'self'
             1698  LOAD_ATTR                clad_spec
             1700  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1702  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1704  POP_TOP          

 L. 275      1706  LOAD_GLOBAL              gdspy
             1708  LOAD_ATTR                Round

 L. 277      1710  LOAD_FAST                'xcenter'

 L. 281      1712  LOAD_FAST                'self'
             1714  LOAD_ATTR                radius
             1716  UNARY_NEGATIVE   
             1718  LOAD_FAST                'self'
             1720  LOAD_ATTR                wgt
             1722  LOAD_ATTR                wg_width
             1724  LOAD_CONST               2.0
             1726  BINARY_TRUE_DIVIDE
             1728  BINARY_SUBTRACT  
             1730  LOAD_FAST                'self'
             1732  LOAD_ATTR                coupling_gap
             1734  BINARY_SUBTRACT  
             1736  LOAD_CONST               2
             1738  LOAD_FAST                'dy'
             1740  BINARY_MULTIPLY  
             1742  BINARY_ADD       
             1744  BUILD_TUPLE_2         2 

 L. 283      1746  LOAD_FAST                'self'
             1748  LOAD_ATTR                radius
             1750  BUILD_TUPLE_2         2 
             1752  LOAD_STR                 'number_of_points'

 L. 284      1754  LOAD_FAST                'self'
             1756  LOAD_ATTR                wgt
             1758  LOAD_METHOD              get_num_points_curve

 L. 285      1760  LOAD_CONST               2
           1762_0  COME_FROM           298  '298'
             1762  LOAD_GLOBAL              np
             1764  LOAD_ATTR                pi
             1766  BINARY_MULTIPLY  
             1768  LOAD_FAST                'self'
             1770  LOAD_ATTR                radius
             1772  CALL_METHOD_2         2  '2 positional arguments'
             1774  BUILD_MAP_1           1 

 L. 287      1776  LOAD_FAST                'self'
             1778  LOAD_ATTR                wg_spec
             1780  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1782  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1784  STORE_FAST               'ring'

 L. 289      1786  LOAD_GLOBAL              gdspy
             1788  LOAD_ATTR                Round

 L. 291      1790  LOAD_FAST                'xcenter'

 L. 295      1792  LOAD_FAST                'self'
             1794  LOAD_ATTR                radius
             1796  UNARY_NEGATIVE   
             1798  LOAD_FAST                'self'
             1800  LOAD_ATTR                wgt
             1802  LOAD_ATTR                wg_width
             1804  LOAD_CONST               2.0
             1806  BINARY_TRUE_DIVIDE
             1808  BINARY_SUBTRACT  
             1810  LOAD_FAST                'self'
             1812  LOAD_ATTR                coupling_gap
             1814  BINARY_SUBTRACT  
             1816  LOAD_CONST               2
             1818  LOAD_FAST                'dy'
             1820  BINARY_MULTIPLY  
             1822  BINARY_ADD       
             1824  BUILD_TUPLE_2         2 

 L. 297      1826  LOAD_FAST                'self'
             1828  LOAD_ATTR                radius
             1830  LOAD_FAST                'self'
             1832  LOAD_ATTR                wgt
             1834  LOAD_ATTR                clad_width
             1836  BINARY_ADD       
             1838  BUILD_TUPLE_2         2 
             1840  LOAD_STR                 'number_of_points'

 L. 298      1842  LOAD_FAST                'self'
             1844  LOAD_ATTR                wgt
             1846  LOAD_METHOD              get_num_points_curve

 L. 299      1848  LOAD_CONST               2
             1850  LOAD_GLOBAL              np
             1852  LOAD_ATTR                pi
             1854  BINARY_MULTIPLY  
             1856  LOAD_FAST                'self'
             1858  LOAD_ATTR                radius
             1860  LOAD_FAST                'self'
             1862  LOAD_ATTR                wgt
             1864  LOAD_ATTR                clad_width
             1866  BINARY_ADD       
             1868  CALL_METHOD_2         2  '2 positional arguments'
             1870  BUILD_MAP_1           1 

 L. 301      1872  LOAD_FAST                'self'
             1874  LOAD_ATTR                clad_spec
             1876  BUILD_MAP_UNPACK_WITH_CALL_2     2 
             1878  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1880  STORE_FAST               'clad_ring'
           1882_0  COME_FROM          1322  '1322'
           1882_1  COME_FROM          1310  '1310'

 L. 304      1882  LOAD_CONST               4
             1884  LOAD_FAST                'dx'
             1886  BINARY_MULTIPLY  
             1888  LOAD_FAST                'bus_length'
             1890  COMPARE_OP               <
         1892_1894  POP_JUMP_IF_FALSE  1952  'to 1952'

 L. 305      1896  LOAD_FAST                'path'
             1898  LOAD_ATTR                segment
             1900  LOAD_FAST                'bus_length'
             1902  LOAD_CONST               4
             1904  LOAD_FAST                'dx'
             1906  BINARY_MULTIPLY  
             1908  BINARY_SUBTRACT  
             1910  LOAD_CONST               2.0
             1912  BINARY_TRUE_DIVIDE
             1914  BUILD_TUPLE_1         1 
             1916  LOAD_FAST                'self'
             1918  LOAD_ATTR                wg_spec
             1920  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1922  POP_TOP          

 L. 306      1924  LOAD_FAST                'clad'
             1926  LOAD_ATTR                segment
             1928  LOAD_FAST                'bus_length'
             1930  LOAD_CONST               4
             1932  LOAD_FAST                'dx'
             1934  BINARY_MULTIPLY  
             1936  BINARY_SUBTRACT  
             1938  LOAD_CONST               2.0
           1940_0  COME_FROM           476  '476'
             1940  BINARY_TRUE_DIVIDE
             1942  BUILD_TUPLE_1         1 
             1944  LOAD_FAST                'self'
             1946  LOAD_ATTR                clad_spec
             1948  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
             1950  POP_TOP          
           1952_0  COME_FROM          1892  '1892'
           1952_1  COME_FROM           498  '498'
           1952_2  COME_FROM           486  '486'

 L. 308      1952  LOAD_CONST               (0, 0)
             1954  LOAD_FAST                'self'
             1956  STORE_ATTR               port_input

 L. 309      1958  LOAD_FAST                'bus_length'
             1960  LOAD_CONST               0
             1962  BUILD_TUPLE_2         2 
             1964  LOAD_FAST                'self'
             1966  STORE_ATTR               port_output

 L. 311      1968  LOAD_FAST                'self'
             1970  LOAD_METHOD              add
             1972  LOAD_FAST                'ring'
             1974  CALL_METHOD_1         1  '1 positional argument'
             1976  POP_TOP          

 L. 312      1978  LOAD_FAST                'self'
             1980  LOAD_METHOD              add
             1982  LOAD_FAST                'clad_ring'
             1984  CALL_METHOD_1         1  '1 positional argument'
             1986  POP_TOP          

 L. 313      1988  LOAD_FAST                'self'
             1990  LOAD_METHOD              add
             1992  LOAD_FAST                'path'
             1994  CALL_METHOD_1         1  '1 positional argument'
             1996  POP_TOP          

 L. 314      1998  LOAD_FAST                'self'
             2000  LOAD_METHOD              add
             2002  LOAD_FAST                'clad'
             2004  CALL_METHOD_1         1  '1 positional argument'
             2006  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 1762_0

    def __build_ports(self):
        self.portlist['input'] = {'port':self.port_input, 
         'direction':'WEST'}
        self.portlist['output'] = {'port':self.port_output,  'direction':'EAST'}


if __name__ == '__main__':
    from . import *
    top = gdspy.Cell('top')
    wgt = WaveguideTemplate(bend_radius=50, resist='+')
    wg1 = Waveguide([(0, 0), (100, 0)], wgt)
    tk.add(top, wg1)
    r1 = Disk(
 wgt, 60.0, 1.0, wrap_angle=np.pi / 2.0, parity=1, **wg1.portlist['output'])
    wg2 = Waveguide([
     r1.portlist['output']['port'],
     (
      r1.portlist['output']['port'][0] + 100, r1.portlist['output']['port'][1])], wgt)
    tk.add(top, wg2)
    r2 = Disk(wgt, 50.0, 0.8, wrap_angle=np.pi, parity=-1, **wg2.portlist['output'])
    wg3 = Waveguide([
     r2.portlist['output']['port'],
     (
      r2.portlist['output']['port'][0] + 100, r2.portlist['output']['port'][1])], wgt)
    tk.add(top, wg3)
    r3 = Disk(wgt, 40.0, 0.6, parity=1, **wg3.portlist['output'])
    wg4 = Waveguide([
     r3.portlist['output']['port'],
     (
      r3.portlist['output']['port'][0] + 100, r3.portlist['output']['port'][1])], wgt)
    tk.add(top, wg4)
    tk.add(top, r1)
    tk.add(top, r2)
    tk.add(top, r3)