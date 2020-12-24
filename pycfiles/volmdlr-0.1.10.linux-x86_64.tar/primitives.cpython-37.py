# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/volmdlr/primitives.py
# Compiled at: 2020-03-11 05:21:08
# Size of source mod 2**32: 8023 bytes
"""
Common abstract primitives
"""
from scipy.optimize import linprog
import math
from numpy import zeros

class RoundedLineSegments:

    def __init__(self, points, radius, line_class, arc_class, closed=False, adapt_radius=False, name=''):
        self.points = points
        self.radius = radius
        self.closed = closed
        self.adapt_radius = adapt_radius
        self.name = name
        self.npoints = len(points)
        primitives = self.Primitives(line_class, arc_class)
        return primitives

    def frame_mapping(self, frame, side, copy=True):
        """
        side = 'old' or 'new'
        """
        if copy:
            return self.__class__([p.frame_mapping(frame, side, copy=True) for p in self.points],
              radius=(self.radius), adapt_radius=(self.adapt_radius),
              name=(self.name))
        for p in self.points:
            p.frame_mapping(frame, side, copy=False)

    def Primitives--- This code section failed: ---

 L.  39         0  BUILD_MAP_0           0 
                2  STORE_DEREF              'alpha'

 L.  40         4  BUILD_MAP_0           0 
                6  STORE_FAST               'dist'

 L.  41         8  BUILD_MAP_0           0 
               10  STORE_FAST               'lines_length'

 L.  43        12  LOAD_GLOBAL              sorted
               14  LOAD_DEREF               'self'
               16  LOAD_ATTR                radius
               18  LOAD_METHOD              keys
               20  CALL_METHOD_0         0  '0 positional arguments'
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  STORE_FAST               'rounded_points_indices'

 L.  44        26  BUILD_LIST_0          0 
               28  STORE_FAST               'groups'

 L.  45        30  BUILD_MAP_0           0 
               32  STORE_FAST               'arcs'

 L.  46        34  BUILD_LIST_0          0 
               36  STORE_FAST               'primitives'

 L.  49        38  LOAD_DEREF               'self'
               40  LOAD_ATTR                radius
               42  BUILD_MAP_0           0 
               44  COMPARE_OP               !=
            46_48  POP_JUMP_IF_FALSE  1182  'to 1182'

 L.  50        50  LOAD_FAST                'rounded_points_indices'
               52  LOAD_CONST               0
               54  BINARY_SUBSCR    
               56  BUILD_LIST_1          1 
               58  STORE_FAST               'group'

 L.  51        60  LOAD_DEREF               'self'
               62  LOAD_METHOD              ArcFeatures
               64  LOAD_FAST                'rounded_points_indices'
               66  LOAD_CONST               0
               68  BINARY_SUBSCR    
               70  CALL_METHOD_1         1  '1 positional argument'
               72  UNPACK_SEQUENCE_5     5 
               74  STORE_FAST               '_'
               76  STORE_FAST               '_'
               78  STORE_FAST               '_'
               80  STORE_FAST               'dist0'
               82  STORE_FAST               'alpha0'

 L.  52        84  LOAD_FAST                'dist0'
               86  LOAD_FAST                'dist'
               88  LOAD_FAST                'rounded_points_indices'
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  STORE_SUBSCR     

 L.  53        96  LOAD_FAST                'alpha0'
               98  LOAD_DEREF               'alpha'
              100  LOAD_FAST                'rounded_points_indices'
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  STORE_SUBSCR     

 L.  55       108  SETUP_LOOP          324  'to 324'
              110  LOAD_FAST                'rounded_points_indices'
              112  LOAD_CONST               1
              114  LOAD_CONST               None
              116  BUILD_SLICE_2         2 
              118  BINARY_SUBSCR    
              120  GET_ITER         
              122  FOR_ITER            322  'to 322'
              124  STORE_FAST               'i'

 L.  57       126  LOAD_DEREF               'self'
              128  LOAD_METHOD              ArcFeatures
              130  LOAD_FAST                'i'
              132  CALL_METHOD_1         1  '1 positional argument'
              134  UNPACK_SEQUENCE_5     5 
              136  STORE_FAST               'ps2'
              138  STORE_FAST               'pi2'
              140  STORE_FAST               'pe2'
              142  STORE_FAST               'dist2'
              144  STORE_FAST               'alpha2'

 L.  58       146  LOAD_FAST                'dist2'
              148  LOAD_FAST                'dist'
              150  LOAD_FAST                'i'
              152  STORE_SUBSCR     

 L.  59       154  LOAD_FAST                'alpha2'
              156  LOAD_DEREF               'alpha'
              158  LOAD_FAST                'i'
              160  STORE_SUBSCR     

 L.  60       162  LOAD_FAST                'i'
              164  LOAD_CONST               1
              166  BINARY_SUBTRACT  
              168  LOAD_DEREF               'self'
              170  LOAD_ATTR                radius
              172  COMPARE_OP               in
          174_176  POP_JUMP_IF_FALSE   294  'to 294'

 L.  61       178  LOAD_DEREF               'self'
              180  LOAD_ATTR                points
              182  LOAD_FAST                'i'
              184  LOAD_CONST               1
              186  BINARY_SUBTRACT  
              188  BINARY_SUBSCR    
              190  STORE_FAST               'p1'

 L.  62       192  LOAD_DEREF               'self'
              194  LOAD_ATTR                points
              196  LOAD_FAST                'i'
              198  BINARY_SUBSCR    
              200  STORE_FAST               'p2'

 L.  63       202  LOAD_FAST                'p2'
              204  LOAD_FAST                'p1'
              206  BINARY_SUBTRACT  
              208  LOAD_METHOD              Norm
              210  CALL_METHOD_0         0  '0 positional arguments'
              212  STORE_FAST               'l'

 L.  64       214  LOAD_FAST                'l'
              216  LOAD_FAST                'lines_length'
              218  LOAD_FAST                'i'
              220  LOAD_CONST               1
              222  BINARY_SUBTRACT  
              224  STORE_SUBSCR     

 L.  65       226  LOAD_FAST                'dist'
              228  LOAD_FAST                'i'
              230  LOAD_CONST               1
              232  BINARY_SUBTRACT  
              234  BINARY_SUBSCR    
              236  STORE_FAST               'dist1'

 L.  67       238  LOAD_FAST                'dist1'
              240  LOAD_FAST                'dist2'
              242  BINARY_ADD       
              244  LOAD_FAST                'l'
              246  COMPARE_OP               <=
          248_250  POP_JUMP_IF_FALSE   270  'to 270'

 L.  68       252  LOAD_FAST                'groups'
              254  LOAD_METHOD              append
              256  LOAD_FAST                'group'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  POP_TOP          

 L.  69       262  LOAD_FAST                'i'
              264  BUILD_LIST_1          1 
              266  STORE_FAST               'group'
              268  JUMP_FORWARD        292  'to 292'
            270_0  COME_FROM           248  '248'

 L.  71       270  LOAD_DEREF               'self'
              272  LOAD_ATTR                adapt_radius
          274_276  POP_JUMP_IF_TRUE    282  'to 282'

 L.  72       278  LOAD_GLOBAL              ValueError
              280  RAISE_VARARGS_1       1  'exception instance'
            282_0  COME_FROM           274  '274'

 L.  73       282  LOAD_FAST                'group'
              284  LOAD_METHOD              append
              286  LOAD_FAST                'i'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  POP_TOP          
            292_0  COME_FROM           268  '268'
              292  JUMP_BACK           122  'to 122'
            294_0  COME_FROM           174  '174'

 L.  75       294  LOAD_FAST                'group'
              296  BUILD_LIST_0          0 
              298  COMPARE_OP               !=
          300_302  POP_JUMP_IF_FALSE   314  'to 314'

 L.  76       304  LOAD_FAST                'groups'
              306  LOAD_METHOD              append
              308  LOAD_FAST                'group'
              310  CALL_METHOD_1         1  '1 positional argument'
              312  POP_TOP          
            314_0  COME_FROM           300  '300'

 L.  77       314  LOAD_FAST                'i'
              316  BUILD_LIST_1          1 
              318  STORE_FAST               'group'
              320  JUMP_BACK           122  'to 122'
              322  POP_BLOCK        
            324_0  COME_FROM_LOOP      108  '108'

 L.  78       324  LOAD_FAST                'group'
              326  BUILD_LIST_0          0 
              328  COMPARE_OP               !=
          330_332  POP_JUMP_IF_FALSE   344  'to 344'

 L.  79       334  LOAD_FAST                'groups'
              336  LOAD_METHOD              append
              338  LOAD_FAST                'group'
              340  CALL_METHOD_1         1  '1 positional argument'
              342  POP_TOP          
            344_0  COME_FROM           330  '330'

 L.  80       344  LOAD_DEREF               'self'
              346  LOAD_ATTR                adapt_radius
          348_350  POP_JUMP_IF_FALSE  1120  'to 1120'

 L.  81       352  LOAD_DEREF               'self'
              354  LOAD_ATTR                closed
          356_358  POP_JUMP_IF_FALSE   420  'to 420'

 L.  82       360  LOAD_CONST               0
              362  LOAD_FAST                'groups'
              364  LOAD_CONST               0
              366  BINARY_SUBSCR    
              368  COMPARE_OP               in
          370_372  POP_JUMP_IF_FALSE   420  'to 420'

 L.  83       374  LOAD_DEREF               'self'
              376  LOAD_ATTR                npoints
              378  LOAD_FAST                'groups'
              380  LOAD_CONST               -1
              382  BINARY_SUBSCR    
              384  COMPARE_OP               in
          386_388  POP_JUMP_IF_FALSE   420  'to 420'

 L.  84       390  LOAD_FAST                'groups'
              392  LOAD_CONST               0
              394  BINARY_SUBSCR    
              396  LOAD_FAST                'groups'
              398  LOAD_CONST               -1
              400  BINARY_SUBSCR    
              402  BINARY_ADD       
              404  STORE_FAST               'new_group'

 L.  85       406  LOAD_FAST                'new_group'
              408  LOAD_FAST                'groups'
              410  LOAD_CONST               0
              412  STORE_SUBSCR     

 L.  86       414  LOAD_FAST                'groups'
              416  LOAD_CONST               -1
              418  DELETE_SUBSCR    
            420_0  COME_FROM           386  '386'
            420_1  COME_FROM           370  '370'
            420_2  COME_FROM           356  '356'

 L.  88       420  BUILD_LIST_0          0 
              422  STORE_FAST               'groups2'

 L.  89       424  LOAD_CONST               0
              426  STORE_DEREF              'ndof'

 L.  90       428  BUILD_MAP_0           0 
              430  STORE_FAST               'dof'

 L.  91       432  LOAD_CONST               0
              434  STORE_FAST               'neq_ub'

 L.  92       436  BUILD_LIST_0          0 
              438  STORE_FAST               'bounds'

 L.  93   440_442  SETUP_LOOP          830  'to 830'
              444  LOAD_FAST                'groups'
              446  GET_ITER         
          448_450  FOR_ITER            828  'to 828'
              452  STORE_FAST               'group'

 L.  94       454  LOAD_GLOBAL              len
              456  LOAD_FAST                'group'
              458  CALL_FUNCTION_1       1  '1 positional argument'
              460  STORE_FAST               'lg'

 L.  95       462  LOAD_FAST                'lg'
              464  LOAD_CONST               1
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_FALSE   740  'to 740'

 L.  97       472  LOAD_FAST                'group'
              474  LOAD_CONST               0
              476  BINARY_SUBSCR    
              478  STORE_FAST               'ipoint'

 L.  98       480  LOAD_DEREF               'self'
              482  LOAD_ATTR                closed
          484_486  POP_JUMP_IF_FALSE   618  'to 618'

 L.  99       488  LOAD_FAST                'ipoint'
              490  LOAD_CONST               0
              492  COMPARE_OP               ==
          494_496  POP_JUMP_IF_FALSE   530  'to 530'

 L. 100       498  LOAD_DEREF               'self'
              500  LOAD_ATTR                points
              502  LOAD_CONST               -1
              504  BINARY_SUBSCR    
              506  STORE_FAST               'p1'

 L. 101       508  LOAD_DEREF               'self'
              510  LOAD_ATTR                points
              512  LOAD_CONST               0
              514  BINARY_SUBSCR    
              516  STORE_FAST               'p2'

 L. 102       518  LOAD_DEREF               'self'
              520  LOAD_ATTR                points
              522  LOAD_CONST               1
              524  BINARY_SUBSCR    
              526  STORE_FAST               'p3'
              528  JUMP_FORWARD        616  'to 616'
            530_0  COME_FROM           494  '494'

 L. 103       530  LOAD_FAST                'ipoint'
              532  LOAD_DEREF               'self'
              534  LOAD_ATTR                npoints
              536  LOAD_CONST               1
              538  BINARY_SUBTRACT  
              540  COMPARE_OP               ==
          542_544  POP_JUMP_IF_FALSE   578  'to 578'

 L. 104       546  LOAD_DEREF               'self'
              548  LOAD_ATTR                points
              550  LOAD_CONST               -2
              552  BINARY_SUBSCR    
              554  STORE_FAST               'p1'

 L. 105       556  LOAD_DEREF               'self'
              558  LOAD_ATTR                points
              560  LOAD_CONST               -1
              562  BINARY_SUBSCR    
              564  STORE_FAST               'p2'

 L. 106       566  LOAD_DEREF               'self'
              568  LOAD_ATTR                points
              570  LOAD_CONST               0
              572  BINARY_SUBSCR    
              574  STORE_FAST               'p3'
              576  JUMP_FORWARD        616  'to 616'
            578_0  COME_FROM           542  '542'

 L. 108       578  LOAD_DEREF               'self'
              580  LOAD_ATTR                points
              582  LOAD_FAST                'ipoint'
              584  LOAD_CONST               1
              586  BINARY_SUBTRACT  
              588  BINARY_SUBSCR    
              590  STORE_FAST               'p1'

 L. 109       592  LOAD_DEREF               'self'
              594  LOAD_ATTR                points
              596  LOAD_FAST                'ipoint'
              598  BINARY_SUBSCR    
              600  STORE_FAST               'p2'

 L. 110       602  LOAD_DEREF               'self'
              604  LOAD_ATTR                points
              606  LOAD_FAST                'ipoint'
              608  LOAD_CONST               1
              610  BINARY_ADD       
              612  BINARY_SUBSCR    
              614  STORE_FAST               'p3'
            616_0  COME_FROM           576  '576'
            616_1  COME_FROM           528  '528'
              616  JUMP_FORWARD        656  'to 656'
            618_0  COME_FROM           484  '484'

 L. 113       618  LOAD_DEREF               'self'
              620  LOAD_ATTR                points
              622  LOAD_FAST                'ipoint'
              624  LOAD_CONST               1
              626  BINARY_SUBTRACT  
              628  BINARY_SUBSCR    
              630  STORE_FAST               'p1'

 L. 114       632  LOAD_DEREF               'self'
              634  LOAD_ATTR                points
              636  LOAD_FAST                'ipoint'
              638  BINARY_SUBSCR    
              640  STORE_FAST               'p2'

 L. 115       642  LOAD_DEREF               'self'
              644  LOAD_ATTR                points
              646  LOAD_FAST                'ipoint'
              648  LOAD_CONST               1
              650  BINARY_ADD       
              652  BINARY_SUBSCR    
              654  STORE_FAST               'p3'
            656_0  COME_FROM           616  '616'

 L. 118       656  LOAD_FAST                'p1'
              658  LOAD_METHOD              point_distance
              660  LOAD_FAST                'p2'
              662  CALL_METHOD_1         1  '1 positional argument'
              664  STORE_FAST               'd1'

 L. 119       666  LOAD_FAST                'p2'
              668  LOAD_METHOD              point_distance
              670  LOAD_FAST                'p3'
              672  CALL_METHOD_1         1  '1 positional argument'
              674  STORE_FAST               'd2'

 L. 121       676  LOAD_FAST                'dist'
              678  LOAD_FAST                'ipoint'
              680  BINARY_SUBSCR    
              682  LOAD_GLOBAL              min
              684  LOAD_FAST                'd1'
              686  LOAD_FAST                'd2'
              688  CALL_FUNCTION_2       2  '2 positional arguments'
              690  COMPARE_OP               >
          692_694  POP_JUMP_IF_FALSE   824  'to 824'

 L. 122       696  LOAD_GLOBAL              min
              698  LOAD_DEREF               'self'
              700  LOAD_ATTR                radius
              702  LOAD_FAST                'ipoint'
              704  BINARY_SUBSCR    
              706  LOAD_GLOBAL              min
              708  LOAD_FAST                'd1'
              710  LOAD_FAST                'd2'
              712  CALL_FUNCTION_2       2  '2 positional arguments'
              714  LOAD_GLOBAL              math
              716  LOAD_METHOD              tan
              718  LOAD_DEREF               'alpha'
              720  LOAD_FAST                'ipoint'
              722  BINARY_SUBSCR    
              724  CALL_METHOD_1         1  '1 positional argument'
              726  BINARY_MULTIPLY  
              728  CALL_FUNCTION_2       2  '2 positional arguments'
              730  LOAD_DEREF               'self'
              732  LOAD_ATTR                radius
              734  LOAD_FAST                'ipoint'
              736  STORE_SUBSCR     
              738  JUMP_BACK           448  'to 448'
            740_0  COME_FROM           468  '468'

 L. 126       740  LOAD_FAST                'bounds'
              742  LOAD_METHOD              extend
              744  LOAD_CLOSURE             'alpha'
              746  LOAD_CLOSURE             'self'
              748  BUILD_TUPLE_2         2 
              750  LOAD_LISTCOMP            '<code_object <listcomp>>'
              752  LOAD_STR                 'RoundedLineSegments.Primitives.<locals>.<listcomp>'
              754  MAKE_FUNCTION_8          'closure'
              756  LOAD_FAST                'group'
              758  GET_ITER         
              760  CALL_FUNCTION_1       1  '1 positional argument'
              762  CALL_METHOD_1         1  '1 positional argument'
              764  POP_TOP          

 L. 127       766  LOAD_FAST                'dof'
              768  LOAD_METHOD              update
              770  LOAD_CLOSURE             'ndof'
              772  BUILD_TUPLE_1         1 
              774  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              776  LOAD_STR                 'RoundedLineSegments.Primitives.<locals>.<dictcomp>'
              778  MAKE_FUNCTION_8          'closure'
              780  LOAD_GLOBAL              enumerate
              782  LOAD_FAST                'group'
              784  CALL_FUNCTION_1       1  '1 positional argument'
              786  GET_ITER         
              788  CALL_FUNCTION_1       1  '1 positional argument'
              790  CALL_METHOD_1         1  '1 positional argument'
              792  POP_TOP          

 L. 128       794  LOAD_DEREF               'ndof'
              796  LOAD_FAST                'lg'
              798  INPLACE_ADD      
              800  STORE_DEREF              'ndof'

 L. 129       802  LOAD_FAST                'groups2'
              804  LOAD_METHOD              append
              806  LOAD_FAST                'group'
              808  CALL_METHOD_1         1  '1 positional argument'
              810  POP_TOP          

 L. 130       812  LOAD_FAST                'neq_ub'
              814  LOAD_FAST                'lg'
              816  LOAD_CONST               1
              818  BINARY_SUBTRACT  
              820  INPLACE_ADD      
              822  STORE_FAST               'neq_ub'
            824_0  COME_FROM           692  '692'
          824_826  JUMP_BACK           448  'to 448'
              828  POP_BLOCK        
            830_0  COME_FROM_LOOP      440  '440'

 L. 134       830  LOAD_DEREF               'ndof'
              832  LOAD_CONST               0
              834  COMPARE_OP               >
          836_838  POP_JUMP_IF_FALSE  1120  'to 1120'

 L. 135       840  LOAD_GLOBAL              zeros
              842  LOAD_DEREF               'ndof'
              844  CALL_FUNCTION_1       1  '1 positional argument'
              846  STORE_FAST               'C'

 L. 136       848  SETUP_LOOP          892  'to 892'
              850  LOAD_FAST                'dof'
              852  LOAD_METHOD              items
              854  CALL_METHOD_0         0  '0 positional arguments'
              856  GET_ITER         
              858  FOR_ITER            890  'to 890'
              860  UNPACK_SEQUENCE_2     2 
              862  STORE_FAST               'j'
              864  STORE_FAST               'i'

 L. 137       866  LOAD_GLOBAL              math
              868  LOAD_METHOD              tan
              870  LOAD_DEREF               'alpha'
              872  LOAD_FAST                'j'
              874  BINARY_SUBSCR    
              876  CALL_METHOD_1         1  '1 positional argument'
              878  UNARY_NEGATIVE   
              880  LOAD_FAST                'C'
              882  LOAD_FAST                'i'
              884  STORE_SUBSCR     
          886_888  JUMP_BACK           858  'to 858'
              890  POP_BLOCK        
            892_0  COME_FROM_LOOP      848  '848'

 L. 139       892  LOAD_GLOBAL              zeros
              894  LOAD_FAST                'neq_ub'
              896  LOAD_DEREF               'ndof'
              898  BUILD_TUPLE_2         2 
              900  CALL_FUNCTION_1       1  '1 positional argument'
              902  STORE_FAST               'A_ub'

 L. 140       904  LOAD_GLOBAL              zeros
              906  LOAD_FAST                'neq_ub'
              908  CALL_FUNCTION_1       1  '1 positional argument'
              910  STORE_FAST               'b_ub'

 L. 141       912  LOAD_CONST               0
              914  STORE_FAST               'ieq_ub'

 L. 143       916  SETUP_LOOP         1026  'to 1026'
              918  LOAD_FAST                'groups2'
              920  GET_ITER         
              922  FOR_ITER           1024  'to 1024'
              924  STORE_FAST               'group'

 L. 144       926  SETUP_LOOP         1020  'to 1020'
              928  LOAD_GLOBAL              zip
              930  LOAD_FAST                'group'
              932  LOAD_CONST               None
              934  LOAD_CONST               -1
              936  BUILD_SLICE_2         2 
              938  BINARY_SUBSCR    
              940  LOAD_FAST                'group'
              942  LOAD_CONST               1
              944  LOAD_CONST               None
              946  BUILD_SLICE_2         2 
              948  BINARY_SUBSCR    
              950  CALL_FUNCTION_2       2  '2 positional arguments'
              952  GET_ITER         
              954  FOR_ITER           1018  'to 1018'
              956  UNPACK_SEQUENCE_2     2 
              958  STORE_FAST               'ip1'
              960  STORE_FAST               'ip2'

 L. 145       962  LOAD_CONST               1
              964  LOAD_FAST                'A_ub'
              966  LOAD_FAST                'ieq_ub'
              968  LOAD_FAST                'dof'
              970  LOAD_FAST                'ip1'
              972  BINARY_SUBSCR    
              974  BUILD_TUPLE_2         2 
              976  STORE_SUBSCR     

 L. 146       978  LOAD_CONST               1
              980  LOAD_FAST                'A_ub'
              982  LOAD_FAST                'ieq_ub'
              984  LOAD_FAST                'dof'
              986  LOAD_FAST                'ip2'
              988  BINARY_SUBSCR    
              990  BUILD_TUPLE_2         2 
              992  STORE_SUBSCR     

 L. 147       994  LOAD_FAST                'lines_length'
              996  LOAD_FAST                'ip1'
              998  BINARY_SUBSCR    
             1000  LOAD_FAST                'b_ub'
             1002  LOAD_FAST                'ieq_ub'
             1004  STORE_SUBSCR     

 L. 148      1006  LOAD_FAST                'ieq_ub'
             1008  LOAD_CONST               1
             1010  INPLACE_ADD      
             1012  STORE_FAST               'ieq_ub'
         1014_1016  JUMP_BACK           954  'to 954'
             1018  POP_BLOCK        
           1020_0  COME_FROM_LOOP      926  '926'
         1020_1022  JUMP_BACK           922  'to 922'
             1024  POP_BLOCK        
           1026_0  COME_FROM_LOOP      916  '916'

 L. 150      1026  LOAD_GLOBAL              linprog
             1028  LOAD_FAST                'C'
             1030  LOAD_FAST                'A_ub'
             1032  LOAD_FAST                'b_ub'
             1034  LOAD_FAST                'bounds'
             1036  LOAD_CONST               ('bounds',)
             1038  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1040  STORE_FAST               'd'

 L. 152      1042  SETUP_LOOP         1120  'to 1120'
             1044  LOAD_FAST                'dof'
             1046  LOAD_METHOD              items
             1048  CALL_METHOD_0         0  '0 positional arguments'
             1050  GET_ITER         
             1052  FOR_ITER           1118  'to 1118'
             1054  UNPACK_SEQUENCE_2     2 
             1056  STORE_FAST               'ipoint'
             1058  STORE_FAST               'dof_point'

 L. 153      1060  LOAD_FAST                'd'
             1062  LOAD_ATTR                x
             1064  LOAD_FAST                'dof_point'
             1066  BINARY_SUBSCR    
             1068  LOAD_GLOBAL              math
             1070  LOAD_METHOD              tan
             1072  LOAD_DEREF               'alpha'
             1074  LOAD_FAST                'ipoint'
             1076  BINARY_SUBSCR    
             1078  CALL_METHOD_1         1  '1 positional argument'
             1080  BINARY_MULTIPLY  
             1082  STORE_FAST               'r'

 L. 154      1084  LOAD_FAST                'r'
             1086  LOAD_CONST               1e-10
             1088  COMPARE_OP               >
         1090_1092  POP_JUMP_IF_FALSE  1106  'to 1106'

 L. 155      1094  LOAD_FAST                'r'
             1096  LOAD_DEREF               'self'
             1098  LOAD_ATTR                radius
             1100  LOAD_FAST                'ipoint'
             1102  STORE_SUBSCR     
             1104  JUMP_BACK          1052  'to 1052'
           1106_0  COME_FROM          1090  '1090'

 L. 157      1106  LOAD_DEREF               'self'
             1108  LOAD_ATTR                radius
             1110  LOAD_FAST                'ipoint'
             1112  DELETE_SUBSCR    
         1114_1116  JUMP_BACK          1052  'to 1052'
             1118  POP_BLOCK        
           1120_0  COME_FROM_LOOP     1042  '1042'
           1120_1  COME_FROM           836  '836'
           1120_2  COME_FROM           348  '348'

 L. 161      1120  SETUP_LOOP         1182  'to 1182'
             1122  LOAD_DEREF               'self'
             1124  LOAD_ATTR                radius
             1126  LOAD_METHOD              items
             1128  CALL_METHOD_0         0  '0 positional arguments'
             1130  GET_ITER         
             1132  FOR_ITER           1180  'to 1180'
             1134  UNPACK_SEQUENCE_2     2 
             1136  STORE_FAST               'ipoint'
             1138  STORE_FAST               'r'

 L. 162      1140  LOAD_DEREF               'self'
             1142  LOAD_METHOD              ArcFeatures
             1144  LOAD_FAST                'ipoint'
             1146  CALL_METHOD_1         1  '1 positional argument'
             1148  UNPACK_SEQUENCE_5     5 
             1150  STORE_FAST               'ps'
             1152  STORE_FAST               'pi'
             1154  STORE_FAST               'pe'
             1156  STORE_FAST               '_'
             1158  STORE_FAST               '_'

 L. 163      1160  LOAD_FAST                'arc_class'
             1162  LOAD_FAST                'ps'
             1164  LOAD_FAST                'pi'
             1166  LOAD_FAST                'pe'
             1168  CALL_FUNCTION_3       3  '3 positional arguments'
             1170  LOAD_FAST                'arcs'
             1172  LOAD_FAST                'ipoint'
             1174  STORE_SUBSCR     
         1176_1178  JUMP_BACK          1132  'to 1132'
             1180  POP_BLOCK        
           1182_0  COME_FROM_LOOP     1120  '1120'
           1182_1  COME_FROM            46  '46'

 L. 166  1182_1184  SETUP_LOOP         1452  'to 1452'
             1186  LOAD_GLOBAL              range
             1188  LOAD_DEREF               'self'
             1190  LOAD_ATTR                npoints
             1192  LOAD_CONST               1
             1194  BINARY_SUBTRACT  
             1196  CALL_FUNCTION_1       1  '1 positional argument'
             1198  GET_ITER         
             1200  FOR_ITER           1450  'to 1450'
             1202  STORE_FAST               'iline'

 L. 167      1204  LOAD_FAST                'iline'
             1206  LOAD_DEREF               'self'
             1208  LOAD_ATTR                radius
             1210  COMPARE_OP               in
         1212_1214  POP_JUMP_IF_FALSE  1350  'to 1350'

 L. 168      1216  LOAD_FAST                'arcs'
             1218  LOAD_FAST                'iline'
             1220  BINARY_SUBSCR    
             1222  STORE_FAST               'arc1'

 L. 169      1224  LOAD_FAST                'primitives'
             1226  LOAD_METHOD              append
             1228  LOAD_FAST                'arc1'
             1230  CALL_METHOD_1         1  '1 positional argument'
             1232  POP_TOP          

 L. 170      1234  LOAD_FAST                'iline'
             1236  LOAD_CONST               1
             1238  BINARY_ADD       
             1240  LOAD_DEREF               'self'
             1242  LOAD_ATTR                radius
             1244  COMPARE_OP               in
         1246_1248  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 171      1250  LOAD_FAST                'arcs'
             1252  LOAD_FAST                'iline'
             1254  LOAD_CONST               1
             1256  BINARY_ADD       
             1258  BINARY_SUBSCR    
             1260  STORE_FAST               'arc2'

 L. 172      1262  LOAD_FAST                'arc1'
             1264  LOAD_ATTR                end
             1266  LOAD_FAST                'arc2'
             1268  LOAD_ATTR                start
             1270  COMPARE_OP               !=
         1272_1274  POP_JUMP_IF_FALSE  1348  'to 1348'

 L. 173      1276  LOAD_FAST                'primitives'
             1278  LOAD_METHOD              append
             1280  LOAD_FAST                'line_class'
             1282  LOAD_FAST                'arc1'
             1284  LOAD_ATTR                end
             1286  LOAD_FAST                'arc2'
             1288  LOAD_ATTR                start
             1290  CALL_FUNCTION_2       2  '2 positional arguments'
             1292  CALL_METHOD_1         1  '1 positional argument'
             1294  POP_TOP          
             1296  JUMP_FORWARD       1348  'to 1348'
           1298_0  COME_FROM          1246  '1246'

 L. 175      1298  LOAD_FAST                'arc1'
             1300  LOAD_ATTR                end
             1302  LOAD_DEREF               'self'
             1304  LOAD_ATTR                points
             1306  LOAD_FAST                'iline'
             1308  LOAD_CONST               1
             1310  BINARY_ADD       
             1312  BINARY_SUBSCR    
             1314  COMPARE_OP               !=
         1316_1318  POP_JUMP_IF_FALSE  1446  'to 1446'

 L. 176      1320  LOAD_FAST                'primitives'
             1322  LOAD_METHOD              append
             1324  LOAD_FAST                'line_class'
             1326  LOAD_FAST                'arc1'
             1328  LOAD_ATTR                end
             1330  LOAD_DEREF               'self'
             1332  LOAD_ATTR                points
             1334  LOAD_FAST                'iline'
             1336  LOAD_CONST               1
             1338  BINARY_ADD       
             1340  BINARY_SUBSCR    
             1342  CALL_FUNCTION_2       2  '2 positional arguments'
             1344  CALL_METHOD_1         1  '1 positional argument'
             1346  POP_TOP          
           1348_0  COME_FROM          1296  '1296'
           1348_1  COME_FROM          1272  '1272'
             1348  JUMP_BACK          1200  'to 1200'
           1350_0  COME_FROM          1212  '1212'

 L. 178      1350  LOAD_DEREF               'self'
             1352  LOAD_ATTR                points
             1354  LOAD_FAST                'iline'
             1356  BINARY_SUBSCR    
             1358  STORE_FAST               'p1'

 L. 179      1360  LOAD_FAST                'iline'
             1362  LOAD_CONST               1
             1364  BINARY_ADD       
             1366  LOAD_DEREF               'self'
             1368  LOAD_ATTR                radius
             1370  COMPARE_OP               in
         1372_1374  POP_JUMP_IF_FALSE  1420  'to 1420'

 L. 180      1376  LOAD_FAST                'arcs'
             1378  LOAD_FAST                'iline'
             1380  LOAD_CONST               1
             1382  BINARY_ADD       
             1384  BINARY_SUBSCR    
             1386  STORE_FAST               'arc2'

 L. 181      1388  LOAD_FAST                'p1'
             1390  LOAD_FAST                'arc2'
             1392  LOAD_ATTR                start
             1394  COMPARE_OP               !=
         1396_1398  POP_JUMP_IF_FALSE  1446  'to 1446'

 L. 182      1400  LOAD_FAST                'primitives'
             1402  LOAD_METHOD              append
             1404  LOAD_FAST                'line_class'
             1406  LOAD_FAST                'p1'
             1408  LOAD_FAST                'arc2'
             1410  LOAD_ATTR                start
             1412  CALL_FUNCTION_2       2  '2 positional arguments'
             1414  CALL_METHOD_1         1  '1 positional argument'
             1416  POP_TOP          
             1418  JUMP_BACK          1200  'to 1200'
           1420_0  COME_FROM          1372  '1372'

 L. 184      1420  LOAD_FAST                'primitives'
             1422  LOAD_METHOD              append
             1424  LOAD_FAST                'line_class'
             1426  LOAD_FAST                'p1'
             1428  LOAD_DEREF               'self'
             1430  LOAD_ATTR                points
             1432  LOAD_FAST                'iline'
             1434  LOAD_CONST               1
             1436  BINARY_ADD       
             1438  BINARY_SUBSCR    
             1440  CALL_FUNCTION_2       2  '2 positional arguments'
             1442  CALL_METHOD_1         1  '1 positional argument'
             1444  POP_TOP          
           1446_0  COME_FROM          1396  '1396'
           1446_1  COME_FROM          1316  '1316'
         1446_1448  JUMP_BACK          1200  'to 1200'
             1450  POP_BLOCK        
           1452_0  COME_FROM_LOOP     1182  '1182'

 L. 186      1452  LOAD_DEREF               'self'
             1454  LOAD_ATTR                closed
         1456_1458  POP_JUMP_IF_FALSE  1678  'to 1678'

 L. 187      1460  LOAD_DEREF               'self'
             1462  LOAD_ATTR                npoints
             1464  LOAD_CONST               1
             1466  BINARY_SUBTRACT  
             1468  LOAD_DEREF               'self'
             1470  LOAD_ATTR                radius
             1472  COMPARE_OP               in
         1474_1476  POP_JUMP_IF_FALSE  1588  'to 1588'

 L. 188      1478  LOAD_FAST                'arcs'
             1480  LOAD_DEREF               'self'
             1482  LOAD_ATTR                npoints
             1484  LOAD_CONST               1
             1486  BINARY_SUBTRACT  
             1488  BINARY_SUBSCR    
             1490  STORE_FAST               'arc1'

 L. 189      1492  LOAD_FAST                'primitives'
             1494  LOAD_METHOD              append
             1496  LOAD_FAST                'arc1'
             1498  CALL_METHOD_1         1  '1 positional argument'
             1500  POP_TOP          

 L. 190      1502  LOAD_CONST               0
             1504  LOAD_DEREF               'self'
             1506  LOAD_ATTR                radius
             1508  COMPARE_OP               in
         1510_1512  POP_JUMP_IF_FALSE  1558  'to 1558'

 L. 191      1514  LOAD_FAST                'arcs'
             1516  LOAD_CONST               0
             1518  BINARY_SUBSCR    
             1520  STORE_FAST               'arc2'

 L. 192      1522  LOAD_FAST                'arc1'
             1524  LOAD_ATTR                end
             1526  LOAD_FAST                'arc2'
             1528  LOAD_ATTR                start
             1530  COMPARE_OP               !=
         1532_1534  POP_JUMP_IF_FALSE  1586  'to 1586'

 L. 193      1536  LOAD_FAST                'primitives'
             1538  LOAD_METHOD              append
             1540  LOAD_FAST                'line_class'
             1542  LOAD_FAST                'arc1'
             1544  LOAD_ATTR                end
             1546  LOAD_FAST                'arc2'
             1548  LOAD_ATTR                start
             1550  CALL_FUNCTION_2       2  '2 positional arguments'
             1552  CALL_METHOD_1         1  '1 positional argument'
             1554  POP_TOP          
             1556  JUMP_FORWARD       1586  'to 1586'
           1558_0  COME_FROM          1510  '1510'

 L. 195      1558  LOAD_FAST                'primitives'
             1560  LOAD_METHOD              append
             1562  LOAD_FAST                'line_class'
             1564  LOAD_FAST                'arc1'
             1566  LOAD_ATTR                end
             1568  LOAD_DEREF               'self'
             1570  LOAD_ATTR                points
             1572  LOAD_FAST                'iline'
             1574  LOAD_CONST               1
             1576  BINARY_ADD       
             1578  BINARY_SUBSCR    
             1580  CALL_FUNCTION_2       2  '2 positional arguments'
             1582  CALL_METHOD_1         1  '1 positional argument'
             1584  POP_TOP          
           1586_0  COME_FROM          1556  '1556'
           1586_1  COME_FROM          1532  '1532'
             1586  JUMP_FORWARD       1678  'to 1678'
           1588_0  COME_FROM          1474  '1474'

 L. 197      1588  LOAD_DEREF               'self'
             1590  LOAD_ATTR                points
             1592  LOAD_DEREF               'self'
             1594  LOAD_ATTR                npoints
             1596  LOAD_CONST               1
             1598  BINARY_SUBTRACT  
             1600  BINARY_SUBSCR    
             1602  STORE_FAST               'p1'

 L. 198      1604  LOAD_CONST               0
             1606  LOAD_DEREF               'self'
             1608  LOAD_ATTR                radius
             1610  COMPARE_OP               in
         1612_1614  POP_JUMP_IF_FALSE  1656  'to 1656'

 L. 199      1616  LOAD_FAST                'arcs'
             1618  LOAD_CONST               0
             1620  BINARY_SUBSCR    
             1622  STORE_FAST               'arc2'

 L. 200      1624  LOAD_FAST                'p1'
             1626  LOAD_FAST                'arc2'
             1628  LOAD_ATTR                start
             1630  COMPARE_OP               !=
         1632_1634  POP_JUMP_IF_FALSE  1678  'to 1678'

 L. 201      1636  LOAD_FAST                'primitives'
             1638  LOAD_METHOD              append
             1640  LOAD_FAST                'line_class'
             1642  LOAD_FAST                'p1'
             1644  LOAD_FAST                'arc2'
             1646  LOAD_ATTR                start
             1648  CALL_FUNCTION_2       2  '2 positional arguments'
             1650  CALL_METHOD_1         1  '1 positional argument'
             1652  POP_TOP          
             1654  JUMP_FORWARD       1678  'to 1678'
           1656_0  COME_FROM          1612  '1612'

 L. 203      1656  LOAD_FAST                'primitives'
             1658  LOAD_METHOD              append
             1660  LOAD_FAST                'line_class'
             1662  LOAD_FAST                'p1'
             1664  LOAD_DEREF               'self'
             1666  LOAD_ATTR                points
             1668  LOAD_CONST               0
             1670  BINARY_SUBSCR    
             1672  CALL_FUNCTION_2       2  '2 positional arguments'
             1674  CALL_METHOD_1         1  '1 positional argument'
             1676  POP_TOP          
           1678_0  COME_FROM          1654  '1654'
           1678_1  COME_FROM          1632  '1632'
           1678_2  COME_FROM          1586  '1586'
           1678_3  COME_FROM          1456  '1456'

 L. 205      1678  LOAD_FAST                'primitives'
             1680  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 1450