# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dmoral/.config/spyder-py3/certobs/certobs/__init__.py
# Compiled at: 2019-09-16 10:53:10
# Size of source mod 2**32: 34935 bytes


def pointingscan--- This code section failed: ---

 L.   4         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              numpy
                6  STORE_FAST               'np'

 L.   5         8  LOAD_CONST               0
               10  LOAD_CONST               ('datetime',)
               12  IMPORT_NAME              datetime
               14  IMPORT_FROM              datetime
               16  STORE_FAST               'datetime'
               18  POP_TOP          

 L.   6        20  LOAD_CONST               0
               22  LOAD_CONST               None
               24  IMPORT_NAME_ATTR         astropy.units
               26  IMPORT_FROM              units
               28  STORE_FAST               'u'
               30  POP_TOP          

 L.   7        32  LOAD_CONST               0
               34  LOAD_CONST               ('Time', 'TimeDelta', 'TimezoneInfo')
               36  IMPORT_NAME_ATTR         astropy.time
               38  IMPORT_FROM              Time
               40  STORE_FAST               'Time'
               42  IMPORT_FROM              TimeDelta
               44  STORE_FAST               'TimeDelta'
               46  IMPORT_FROM              TimezoneInfo
               48  STORE_FAST               'TimezoneInfo'
               50  POP_TOP          

 L.   8        52  LOAD_CONST               0
               54  LOAD_CONST               ('SkyCoord', 'EarthLocation', 'AltAz', 'Angle', 'ITRS')
               56  IMPORT_NAME_ATTR         astropy.coordinates
               58  IMPORT_FROM              SkyCoord
               60  STORE_FAST               'SkyCoord'
               62  IMPORT_FROM              EarthLocation
               64  STORE_FAST               'EarthLocation'
               66  IMPORT_FROM              AltAz
               68  STORE_FAST               'AltAz'
               70  IMPORT_FROM              Angle
               72  STORE_FAST               'Angle'
               74  IMPORT_FROM              ITRS
               76  STORE_FAST               'ITRS'
               78  POP_TOP          

 L.   9        80  LOAD_CONST               0
               82  LOAD_CONST               ('get_body', 'get_moon', 'solar_system_ephemeris')
               84  IMPORT_NAME_ATTR         astropy.coordinates
               86  IMPORT_FROM              get_body
               88  STORE_FAST               'get_body'
               90  IMPORT_FROM              get_moon
               92  STORE_FAST               'get_moon'
               94  IMPORT_FROM              solar_system_ephemeris
               96  STORE_FAST               'solar_system_ephemeris'
               98  POP_TOP          

 L.  11       100  LOAD_CONST               0
              102  LOAD_CONST               None
              104  IMPORT_NAME_ATTR         matplotlib.pyplot
              106  IMPORT_FROM              pyplot
              108  STORE_FAST               'plt'
              110  POP_TOP          

 L.  13       112  LOAD_FAST                'plt'
              114  LOAD_ATTR                style
              116  LOAD_METHOD              use
              118  LOAD_STR                 'seaborn'
              120  CALL_METHOD_1         1  '1 positional argument'
              122  POP_TOP          

 L.  18       124  LOAD_FAST                'EarthLocation'
              126  LOAD_FAST                'Angle'
              128  LOAD_STR                 '40d26m33.233s'
              130  CALL_FUNCTION_1       1  '1 positional argument'
              132  LOAD_FAST                'Angle'
              134  LOAD_STR                 '-3d57m5.70s'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  LOAD_CONST               655.15
              140  LOAD_FAST                'u'
              142  LOAD_ATTR                m
              144  BINARY_MULTIPLY  
              146  LOAD_CONST               ('lat', 'lon', 'height')
              148  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              150  STORE_FAST               'VIL1'

 L.  19       152  LOAD_FAST                'EarthLocation'
              154  LOAD_FAST                'Angle'
              156  LOAD_STR                 '40d26m44.2s'
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  LOAD_FAST                'Angle'
              162  LOAD_STR                 '-3d57m9.4s'
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  LOAD_CONST               664.8
              168  LOAD_FAST                'u'
              170  LOAD_ATTR                m
              172  BINARY_MULTIPLY  
              174  LOAD_CONST               ('lat', 'lon', 'height')
              176  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              178  STORE_FAST               'VIL2'

 L.  23       180  LOAD_FAST                'TimezoneInfo'
              182  LOAD_CONST               2
              184  LOAD_FAST                'u'
              186  LOAD_ATTR                hour
              188  BINARY_MULTIPLY  
              190  LOAD_CONST               ('utc_offset',)
              192  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              194  STORE_FAST               'utc_plus_two_hours'

 L.  26       196  LOAD_GLOBAL              open
              198  LOAD_STR                 'certobs/CERT-Cat.dat'
              200  LOAD_STR                 'r'
              202  LOAD_STR                 'iso-8859-1'
              204  LOAD_CONST               ('mode', 'encoding')
              206  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              208  STORE_FAST               'f'

 L.  27       210  LOAD_CONST               (10, 21, 17, 9)
              212  STORE_FAST               'wid'

 L.  28       214  LOAD_FAST                'np'
              216  LOAD_ATTR                genfromtxt
              218  LOAD_FAST                'f'
              220  LOAD_CONST               (0, 1, 2, 3)
              222  LOAD_CONST               3
              224  LOAD_CONST               12

 L.  29       226  LOAD_STR                 'U7'
              228  LOAD_STR                 'U18'
              230  LOAD_GLOBAL              float
              232  LOAD_GLOBAL              float
              234  BUILD_TUPLE_4         4 
              236  LOAD_FAST                'wid'
              238  LOAD_CONST               ('usecols', 'skip_header', 'skip_footer', 'dtype', 'delimiter')
              240  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              242  STORE_FAST               'cat'

 L.  30       244  BUILD_LIST_0          0 
              246  STORE_FAST               'cata'

 L.  31       248  SETUP_LOOP          272  'to 272'
              250  LOAD_FAST                'cat'
              252  GET_ITER         
              254  FOR_ITER            270  'to 270'
              256  STORE_FAST               'i'

 L.  32       258  LOAD_FAST                'cata'
              260  LOAD_METHOD              append
              262  LOAD_FAST                'i'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  POP_TOP          
              268  JUMP_BACK           254  'to 254'
              270  POP_BLOCK        
            272_0  COME_FROM_LOOP      248  '248'

 L.  37       272  LOAD_FAST                'Time'
              274  LOAD_FAST                'datetime'
              276  LOAD_METHOD              utcnow
              278  CALL_METHOD_0         0  '0 positional arguments'
              280  LOAD_STR                 'utc'
              282  LOAD_CONST               ('scale',)
              284  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              286  STORE_FAST               'nowtime'

 L.  41       288  LOAD_GLOBAL              input
              290  LOAD_STR                 'Select the operation mode for the observation: transit/tracking/scanning/tipping-curve:\n'
              292  CALL_FUNCTION_1       1  '1 positional argument'
              294  STORE_FAST               'mode'

 L.  43       296  LOAD_FAST                'mode'
              298  LOAD_STR                 'tracking'
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_TRUE    326  'to 326'
              306  LOAD_FAST                'mode'
              308  LOAD_STR                 'Tracking'
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_TRUE    326  'to 326'
              316  LOAD_FAST                'mode'
              318  LOAD_STR                 'TRACKING'
              320  COMPARE_OP               ==
          322_324  POP_JUMP_IF_FALSE  1766  'to 1766'
            326_0  COME_FROM           312  '312'
            326_1  COME_FROM           302  '302'

 L.  45       326  LOAD_GLOBAL              input
              328  LOAD_STR                 'Enter the starting time of the observation in the next format: 2010-12-31 00:00:00 (UTC time) \n'
              330  CALL_FUNCTION_1       1  '1 positional argument'
              332  BUILD_LIST_1          1 
              334  STORE_FAST               'otime'

 L.  46       336  LOAD_FAST                'Time'
              338  LOAD_FAST                'otime'
              340  LOAD_STR                 'iso'
              342  LOAD_STR                 'utc'
              344  LOAD_CONST               ('format', 'scale')
              346  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              348  STORE_FAST               'obs_time'

 L.  57       350  LOAD_FAST                'solar_system_ephemeris'
              352  LOAD_METHOD              set
              354  LOAD_STR                 'builtin'
              356  CALL_METHOD_1         1  '1 positional argument'
              358  SETUP_WITH          474  'to 474'
              360  POP_TOP          

 L.  58       362  LOAD_FAST                'get_body'
              364  LOAD_STR                 'sun'
              366  LOAD_FAST                'obs_time'
              368  LOAD_FAST                'VIL2'
              370  CALL_FUNCTION_3       3  '3 positional arguments'
              372  STORE_FAST               'sun'

 L.  59       374  LOAD_FAST                'get_body'
              376  LOAD_STR                 'moon'
              378  LOAD_FAST                'obs_time'
              380  LOAD_FAST                'VIL2'
              382  CALL_FUNCTION_3       3  '3 positional arguments'
              384  STORE_FAST               'moon'

 L.  60       386  LOAD_FAST                'get_body'
              388  LOAD_STR                 'mercury'
              390  LOAD_FAST                'obs_time'
              392  LOAD_FAST                'VIL2'
              394  CALL_FUNCTION_3       3  '3 positional arguments'
              396  STORE_FAST               'mercury'

 L.  61       398  LOAD_FAST                'get_body'
              400  LOAD_STR                 'venus'
              402  LOAD_FAST                'obs_time'
              404  LOAD_FAST                'VIL2'
              406  CALL_FUNCTION_3       3  '3 positional arguments'
              408  STORE_FAST               'venus'

 L.  62       410  LOAD_FAST                'get_body'
              412  LOAD_STR                 'mars'
              414  LOAD_FAST                'obs_time'
              416  LOAD_FAST                'VIL2'
              418  CALL_FUNCTION_3       3  '3 positional arguments'
              420  STORE_FAST               'mars'

 L.  63       422  LOAD_FAST                'get_body'
              424  LOAD_STR                 'jupiter'
              426  LOAD_FAST                'obs_time'
              428  LOAD_FAST                'VIL2'
              430  CALL_FUNCTION_3       3  '3 positional arguments'
              432  STORE_FAST               'jupiter'

 L.  64       434  LOAD_FAST                'get_body'
              436  LOAD_STR                 'saturn'
              438  LOAD_FAST                'obs_time'
              440  LOAD_FAST                'VIL2'
              442  CALL_FUNCTION_3       3  '3 positional arguments'
              444  STORE_FAST               'saturn'

 L.  65       446  LOAD_FAST                'get_body'
              448  LOAD_STR                 'uranus'
              450  LOAD_FAST                'obs_time'
              452  LOAD_FAST                'VIL2'
              454  CALL_FUNCTION_3       3  '3 positional arguments'
              456  STORE_FAST               'uranus'

 L.  66       458  LOAD_FAST                'get_body'
              460  LOAD_STR                 'neptune'
              462  LOAD_FAST                'obs_time'
              464  LOAD_FAST                'VIL2'
              466  CALL_FUNCTION_3       3  '3 positional arguments'
              468  STORE_FAST               'neptune'
              470  POP_BLOCK        
              472  LOAD_CONST               None
            474_0  COME_FROM_WITH      358  '358'
              474  WITH_CLEANUP_START
              476  WITH_CLEANUP_FINISH
              478  END_FINALLY      

 L.  71       480  LOAD_FAST                'moon'
              482  LOAD_FAST                'mercury'
              484  LOAD_FAST                'venus'
              486  LOAD_FAST                'mars'
              488  LOAD_FAST                'jupiter'
              490  LOAD_FAST                'saturn'
              492  LOAD_FAST                'uranus'
              494  LOAD_FAST                'neptune'
              496  BUILD_LIST_8          8 
              498  STORE_FAST               'solar'

 L.  72       500  LOAD_STR                 'moon'
              502  LOAD_STR                 'mercury'
              504  LOAD_STR                 'venus'
              506  LOAD_STR                 'mars'
              508  LOAD_STR                 'jupiter'
              510  LOAD_STR                 'saturn'
              512  LOAD_STR                 'uranus'
              514  LOAD_STR                 'neptune'
              516  BUILD_LIST_8          8 
              518  STORE_FAST               'ss'

 L.  75       520  LOAD_GLOBAL              input
              522  LOAD_STR                 'Enter the name of the radio-source. Press ENTER if the source is neither in the catalogue nor a planet:\n'
              524  CALL_FUNCTION_1       1  '1 positional argument'
              526  STORE_FAST               'source'

 L.  77       528  BUILD_LIST_0          0 
              530  STORE_FAST               'name'

 L.  78       532  BUILD_LIST_0          0 
              534  STORE_FAST               'ra'

 L.  79       536  BUILD_LIST_0          0 
              538  STORE_FAST               'dec'

 L.  81       540  SETUP_LOOP          690  'to 690'
              542  LOAD_GLOBAL              enumerate
              544  LOAD_FAST                'ss'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  GET_ITER         
              550  FOR_ITER            688  'to 688'
              552  UNPACK_SEQUENCE_2     2 
              554  STORE_FAST               'i'
              556  STORE_FAST               'item'

 L.  84       558  LOAD_FAST                'source'
              560  LOAD_FAST                'item'
              562  COMPARE_OP               ==
          564_566  POP_JUMP_IF_FALSE   610  'to 610'

 L.  85       568  LOAD_FAST                'ss'
              570  LOAD_FAST                'i'
              572  BINARY_SUBSCR    
              574  STORE_FAST               'name'

 L.  86       576  LOAD_FAST                'solar'
              578  LOAD_FAST                'i'
              580  BINARY_SUBSCR    
              582  LOAD_ATTR                ra
              584  LOAD_ATTR                degree
              586  LOAD_CONST               0
              588  BINARY_SUBSCR    
              590  STORE_FAST               'ra'

 L.  87       592  LOAD_FAST                'solar'
              594  LOAD_FAST                'i'
              596  BINARY_SUBSCR    
              598  LOAD_ATTR                dec
              600  LOAD_ATTR                degree
              602  LOAD_CONST               0
              604  BINARY_SUBSCR    
              606  STORE_FAST               'dec'
              608  JUMP_BACK           550  'to 550'
            610_0  COME_FROM           564  '564'

 L.  89       610  SETUP_LOOP          684  'to 684'
              612  LOAD_GLOBAL              enumerate
              614  LOAD_FAST                'cata'
              616  CALL_FUNCTION_1       1  '1 positional argument'
              618  GET_ITER         
            620_0  COME_FROM           638  '638'
              620  FOR_ITER            682  'to 682'
              622  UNPACK_SEQUENCE_2     2 
              624  STORE_FAST               'a'
              626  STORE_FAST               'atem'

 L.  92       628  LOAD_FAST                'source'
              630  LOAD_FAST                'atem'
              632  LOAD_CONST               0
              634  BINARY_SUBSCR    
              636  COMPARE_OP               ==
          638_640  POP_JUMP_IF_FALSE   620  'to 620'

 L.  93       642  LOAD_FAST                'cata'
              644  LOAD_FAST                'a'
              646  BINARY_SUBSCR    
              648  LOAD_CONST               1
              650  BINARY_SUBSCR    
              652  STORE_FAST               'name'

 L.  94       654  LOAD_FAST                'cata'
              656  LOAD_FAST                'a'
              658  BINARY_SUBSCR    
              660  LOAD_CONST               2
              662  BINARY_SUBSCR    
              664  STORE_FAST               'ra'

 L.  95       666  LOAD_FAST                'cata'
              668  LOAD_FAST                'a'
              670  BINARY_SUBSCR    
              672  LOAD_CONST               3
              674  BINARY_SUBSCR    
              676  STORE_FAST               'dec'
          678_680  JUMP_BACK           620  'to 620'
              682  POP_BLOCK        
            684_0  COME_FROM_LOOP      610  '610'
          684_686  JUMP_BACK           550  'to 550'
              688  POP_BLOCK        
            690_0  COME_FROM_LOOP      540  '540'

 L.  96       690  LOAD_FAST                'name'
              692  BUILD_LIST_0          0 
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   730  'to 730'

 L.  97       700  LOAD_STR                 'unknown source'
              702  STORE_FAST               'name'

 L.  98       704  LOAD_GLOBAL              float
              706  LOAD_GLOBAL              input
              708  LOAD_STR                 'Enter manually the desired right ascension: '
              710  CALL_FUNCTION_1       1  '1 positional argument'
              712  CALL_FUNCTION_1       1  '1 positional argument'
              714  STORE_FAST               'ra'

 L.  99       716  LOAD_GLOBAL              float
              718  LOAD_GLOBAL              input
              720  LOAD_STR                 'Enter manually the desired declination: '
              722  CALL_FUNCTION_1       1  '1 positional argument'
              724  CALL_FUNCTION_1       1  '1 positional argument'
              726  STORE_FAST               'dec'
              728  JUMP_FORWARD        730  'to 730'
            730_0  COME_FROM           728  '728'
            730_1  COME_FROM           696  '696'

 L. 104       730  LOAD_FAST                'sun'
              732  LOAD_ATTR                ra
              734  LOAD_ATTR                degree
              736  LOAD_CONST               0
              738  BINARY_SUBSCR    
              740  STORE_FAST               'ra_sun'

 L. 105       742  LOAD_FAST                'sun'
              744  LOAD_ATTR                dec
              746  LOAD_ATTR                degree
              748  LOAD_CONST               0
              750  BINARY_SUBSCR    
              752  STORE_FAST               'dec_sun'

 L. 106       754  LOAD_FAST                'SkyCoord'
              756  LOAD_FAST                'Angle'
              758  LOAD_FAST                'ra_sun'
              760  LOAD_FAST                'u'
              762  LOAD_ATTR                deg
              764  LOAD_CONST               ('unit',)
              766  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              768  LOAD_FAST                'Angle'
              770  LOAD_FAST                'dec_sun'
              772  LOAD_FAST                'u'
              774  LOAD_ATTR                deg
              776  LOAD_CONST               ('unit',)
              778  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              780  LOAD_STR                 'icrs'
              782  LOAD_CONST               ('frame',)
              784  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              786  STORE_FAST               'suncoords'

 L. 109       788  LOAD_GLOBAL              abs
              790  LOAD_FAST                'ra_sun'
              792  LOAD_FAST                'ra'
              794  BINARY_SUBTRACT  
              796  CALL_FUNCTION_1       1  '1 positional argument'
              798  STORE_FAST               'ra_dif'

 L. 110       800  LOAD_GLOBAL              abs
              802  LOAD_FAST                'dec_sun'
              804  LOAD_FAST                'dec'
              806  BINARY_SUBTRACT  
              808  CALL_FUNCTION_1       1  '1 positional argument'
              810  STORE_FAST               'dec_dif'

 L. 111       812  LOAD_FAST                'ra_dif'
              814  LOAD_CONST               1.5
              816  COMPARE_OP               <
          818_820  POP_JUMP_IF_FALSE   840  'to 840'

 L. 112       822  LOAD_FAST                'dec_dif'
              824  LOAD_CONST               1.5
              826  COMPARE_OP               <
          828_830  POP_JUMP_IF_FALSE   840  'to 840'

 L. 113       832  LOAD_GLOBAL              print
              834  LOAD_STR                 'WARNING: YOU FLEW TOO CLOSE TO THE SUN!!!!!!!!!!!!!!!!!!!!'
              836  CALL_FUNCTION_1       1  '1 positional argument'
              838  POP_TOP          
            840_0  COME_FROM           828  '828'
            840_1  COME_FROM           818  '818'

 L. 116       840  LOAD_FAST                'SkyCoord'
              842  LOAD_FAST                'Angle'
              844  LOAD_FAST                'ra'
              846  LOAD_FAST                'u'
              848  LOAD_ATTR                deg
              850  LOAD_CONST               ('unit',)
              852  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              854  LOAD_FAST                'Angle'
              856  LOAD_FAST                'dec'
              858  LOAD_FAST                'u'
              860  LOAD_ATTR                deg
              862  LOAD_CONST               ('unit',)
              864  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              866  LOAD_STR                 'icrs'
              868  LOAD_CONST               ('frame',)
              870  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              872  STORE_FAST               'obj'

 L. 118       874  LOAD_FAST                'obj'
              876  LOAD_METHOD              transform_to
              878  LOAD_FAST                'ITRS'
              880  LOAD_FAST                'obs_time'
              882  LOAD_CONST               ('obstime',)
              884  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              886  CALL_METHOD_1         1  '1 positional argument'
              888  STORE_FAST               'obj_itrs'

 L. 120       890  LOAD_FAST                'VIL2'
              892  LOAD_ATTR                lon
              894  LOAD_FAST                'obj_itrs'
              896  LOAD_ATTR                spherical
              898  LOAD_ATTR                lon
              900  BINARY_SUBTRACT  
              902  STORE_FAST               'local_ha'

 L. 121       904  LOAD_FAST                'local_ha'
              906  LOAD_ATTR                wrap_at
              908  LOAD_CONST               24
              910  LOAD_FAST                'u'
              912  LOAD_ATTR                hourangle
              914  BINARY_MULTIPLY  
              916  LOAD_CONST               True
              918  LOAD_CONST               ('inplace',)
              920  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              922  POP_TOP          

 L. 123       924  LOAD_FAST                'obj_itrs'
              926  LOAD_ATTR                spherical
              928  LOAD_ATTR                lat
              930  STORE_FAST               'local_dec'

 L. 124       932  LOAD_GLOBAL              print
              934  LOAD_STR                 'Local apparent HA, Dec={} {}'
              936  LOAD_METHOD              format
              938  LOAD_FAST                'local_ha'
              940  LOAD_ATTR                to_string
              942  LOAD_FAST                'u'
              944  LOAD_ATTR                hourangle

 L. 125       946  LOAD_STR                 ':'
              948  LOAD_CONST               ('unit', 'sep')
              950  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              952  LOAD_FAST                'local_dec'
              954  LOAD_ATTR                to_string
              956  LOAD_FAST                'u'
              958  LOAD_ATTR                deg
              960  LOAD_STR                 ':'
              962  LOAD_CONST               True
              964  LOAD_CONST               ('unit', 'sep', 'alwayssign')
              966  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              968  CALL_METHOD_2         2  '2 positional arguments'
              970  CALL_FUNCTION_1       1  '1 positional argument'
              972  POP_TOP          

 L. 136       974  LOAD_GLOBAL              float
              976  LOAD_GLOBAL              input
              978  LOAD_STR                 'Enter the duration of the observation, in minutes: '
              980  CALL_FUNCTION_1       1  '1 positional argument'
              982  CALL_FUNCTION_1       1  '1 positional argument'
              984  STORE_FAST               'duration'

 L. 140       986  LOAD_GLOBAL              float
              988  LOAD_GLOBAL              input
              990  LOAD_STR                 'Enter the time interval between two consecutive pointings (in seconds): '
              992  CALL_FUNCTION_1       1  '1 positional argument'
              994  CALL_FUNCTION_1       1  '1 positional argument'
              996  STORE_FAST               'dt'

 L. 144       998  LOAD_FAST                'duration'
             1000  LOAD_CONST               60
             1002  BINARY_MULTIPLY  
             1004  LOAD_FAST                'dt'
             1006  BINARY_TRUE_DIVIDE
             1008  STORE_FAST               'pointings'

 L. 147      1010  LOAD_FAST                'TimeDelta'
             1012  LOAD_FAST                'dt'
             1014  LOAD_STR                 'sec'
             1016  LOAD_CONST               ('format',)
             1018  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1020  STORE_FAST               'dt2'

 L. 149      1022  LOAD_FAST                'np'
             1024  LOAD_METHOD              linspace
             1026  LOAD_CONST               0.0
             1028  LOAD_FAST                'pointings'
             1030  LOAD_FAST                'pointings'
             1032  LOAD_CONST               1
             1034  BINARY_ADD       
             1036  CALL_METHOD_3         3  '3 positional arguments'
             1038  STORE_FAST               'suc'

 L. 150      1040  LOAD_FAST                'obs_time'
             1042  LOAD_CONST               0
             1044  BINARY_SUBSCR    
             1046  LOAD_FAST                'dt2'
             1048  LOAD_FAST                'suc'
             1050  BINARY_MULTIPLY  
             1052  BINARY_ADD       
             1054  STORE_FAST               't'

 L. 153      1056  LOAD_FAST                'TimeDelta'
             1058  LOAD_CONST               300
             1060  LOAD_STR                 'sec'
             1062  LOAD_CONST               ('format',)
             1064  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1066  STORE_FAST               'pre'

 L. 154      1068  LOAD_FAST                'obs_time'
             1070  LOAD_CONST               0
             1072  BINARY_SUBSCR    
             1074  LOAD_FAST                'pre'
             1076  BINARY_SUBTRACT  
             1078  STORE_FAST               't0'

 L. 155      1080  LOAD_FAST                'obs_time'
             1082  LOAD_CONST               0
             1084  BINARY_SUBSCR    
             1086  LOAD_FAST                'pre'
             1088  BINARY_ADD       
             1090  STORE_FAST               'tf'

 L. 158      1092  BUILD_LIST_0          0 
             1094  STORE_FAST               'completecoords'

 L. 159      1096  BUILD_LIST_0          0 
             1098  STORE_FAST               'time'

 L. 160      1100  BUILD_LIST_0          0 
             1102  STORE_FAST               'alti'

 L. 161      1104  BUILD_LIST_0          0 
             1106  STORE_FAST               'azi'

 L. 162      1108  SETUP_LOOP         1236  'to 1236'
             1110  LOAD_FAST                'suc'
             1112  LOAD_METHOD              astype
             1114  LOAD_GLOBAL              int
             1116  CALL_METHOD_1         1  '1 positional argument'
             1118  GET_ITER         
             1120  FOR_ITER           1234  'to 1234'
             1122  STORE_FAST               'i'

 L. 164      1124  LOAD_FAST                'obj'
             1126  LOAD_METHOD              transform_to
             1128  LOAD_FAST                'AltAz'
             1130  LOAD_FAST                't'
             1132  LOAD_FAST                'i'
             1134  BINARY_SUBSCR    
             1136  LOAD_FAST                'VIL2'
             1138  LOAD_CONST               ('obstime', 'location')
             1140  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1142  CALL_METHOD_1         1  '1 positional argument'
             1144  STORE_FAST               'new'

 L. 165      1146  LOAD_FAST                'new'
             1148  LOAD_ATTR                alt
             1150  LOAD_ATTR                degree
             1152  STORE_FAST               'alt_i'

 L. 166      1154  LOAD_FAST                'new'
             1156  LOAD_ATTR                az
             1158  LOAD_ATTR                degree
             1160  STORE_FAST               'az_i'

 L. 167      1162  LOAD_FAST                'alti'
             1164  LOAD_METHOD              append
             1166  LOAD_FAST                'alt_i'
             1168  CALL_METHOD_1         1  '1 positional argument'
             1170  POP_TOP          

 L. 168      1172  LOAD_FAST                'azi'
             1174  LOAD_METHOD              append
             1176  LOAD_FAST                'az_i'
             1178  CALL_METHOD_1         1  '1 positional argument'
             1180  POP_TOP          

 L. 170      1182  LOAD_FAST                'time'
             1184  LOAD_METHOD              append
             1186  LOAD_FAST                't'
             1188  LOAD_FAST                'i'
             1190  BINARY_SUBSCR    
             1192  LOAD_ATTR                isot
             1194  CALL_METHOD_1         1  '1 positional argument'
             1196  POP_TOP          

 L. 171      1198  LOAD_FAST                'time'
             1200  LOAD_FAST                'i'
             1202  BINARY_SUBSCR    
             1204  LOAD_FAST                'alti'
             1206  LOAD_FAST                'i'
             1208  BINARY_SUBSCR    
             1210  LOAD_FAST                'azi'
             1212  LOAD_FAST                'i'
             1214  BINARY_SUBSCR    
             1216  BUILD_TUPLE_3         3 
             1218  STORE_FAST               'cco'

 L. 172      1220  LOAD_FAST                'completecoords'
             1222  LOAD_METHOD              append
             1224  LOAD_FAST                'cco'
             1226  CALL_METHOD_1         1  '1 positional argument'
             1228  POP_TOP          
         1230_1232  JUMP_BACK          1120  'to 1120'
             1234  POP_BLOCK        
           1236_0  COME_FROM_LOOP     1108  '1108'

 L. 175      1236  SETUP_LOOP         1308  'to 1308'
             1238  LOAD_FAST                'suc'
             1240  LOAD_METHOD              astype
             1242  LOAD_GLOBAL              int
             1244  CALL_METHOD_1         1  '1 positional argument'
             1246  GET_ITER         
           1248_0  COME_FROM          1266  '1266'
             1248  FOR_ITER           1306  'to 1306'
             1250  STORE_FAST               'i'

 L. 176      1252  LOAD_FAST                'completecoords'
             1254  LOAD_FAST                'i'
             1256  BINARY_SUBSCR    
             1258  LOAD_CONST               1
             1260  BINARY_SUBSCR    
             1262  LOAD_CONST               10
             1264  COMPARE_OP               <
         1266_1268  POP_JUMP_IF_FALSE  1248  'to 1248'

 L. 177      1270  LOAD_FAST                'np'
             1272  LOAD_ATTR                ma
             1274  LOAD_ATTR                masked
             1276  LOAD_FAST                'completecoords'
             1278  LOAD_FAST                'i'
             1280  STORE_SUBSCR     

 L. 178      1282  LOAD_GLOBAL              print
             1284  LOAD_STR                 'Object non visible at the '
             1286  LOAD_GLOBAL              str
             1288  LOAD_FAST                'i'
             1290  CALL_FUNCTION_1       1  '1 positional argument'
             1292  BINARY_ADD       
             1294  LOAD_STR                 'position of the observation'
             1296  BINARY_ADD       
             1298  CALL_FUNCTION_1       1  '1 positional argument'
             1300  POP_TOP          
         1302_1304  JUMP_BACK          1248  'to 1248'
             1306  POP_BLOCK        
           1308_0  COME_FROM_LOOP     1236  '1236'

 L. 183      1308  BUILD_LIST_0          0 
             1310  STORE_FAST               'r'

 L. 184      1312  BUILD_LIST_0          0 
             1314  STORE_FAST               'elev'

 L. 185      1316  LOAD_CONST               1.00031
             1318  STORE_FAST               'n0'

 L. 186      1320  SETUP_LOOP         1422  'to 1422'
             1322  LOAD_FAST                'suc'
             1324  LOAD_METHOD              astype
             1326  LOAD_GLOBAL              int
             1328  CALL_METHOD_1         1  '1 positional argument'
             1330  GET_ITER         
             1332  FOR_ITER           1420  'to 1420'
             1334  STORE_FAST               'i'

 L. 188      1336  LOAD_FAST                'np'
             1338  LOAD_METHOD              deg2rad
             1340  LOAD_FAST                'alti'
             1342  LOAD_FAST                'i'
             1344  BINARY_SUBSCR    
             1346  LOAD_CONST               4.7
             1348  LOAD_CONST               2.24
             1350  LOAD_FAST                'alti'
             1352  LOAD_FAST                'i'
             1354  BINARY_SUBSCR    
             1356  BINARY_ADD       
             1358  BINARY_TRUE_DIVIDE
             1360  BINARY_ADD       
             1362  CALL_METHOD_1         1  '1 positional argument'
             1364  STORE_FAST               'p'

 L. 189      1366  LOAD_FAST                'r'
             1368  LOAD_METHOD              append
             1370  LOAD_FAST                'n0'
             1372  LOAD_CONST               1
             1374  BINARY_SUBTRACT  
             1376  LOAD_CONST               1
             1378  BINARY_MULTIPLY  
             1380  LOAD_FAST                'np'
             1382  LOAD_METHOD              tan
             1384  LOAD_FAST                'p'
             1386  CALL_METHOD_1         1  '1 positional argument'
             1388  BINARY_TRUE_DIVIDE
             1390  CALL_METHOD_1         1  '1 positional argument'
             1392  POP_TOP          

 L. 190      1394  LOAD_FAST                'elev'
             1396  LOAD_METHOD              append
             1398  LOAD_FAST                'alti'
             1400  LOAD_FAST                'i'
             1402  BINARY_SUBSCR    
             1404  LOAD_FAST                'r'
             1406  LOAD_FAST                'i'
             1408  BINARY_SUBSCR    
             1410  BINARY_ADD       
             1412  CALL_METHOD_1         1  '1 positional argument'
             1414  POP_TOP          
         1416_1418  JUMP_BACK          1332  'to 1332'
             1420  POP_BLOCK        
           1422_0  COME_FROM_LOOP     1320  '1320'

 L. 194      1422  LOAD_STR                 'isot'
             1424  LOAD_FAST                't'
             1426  STORE_ATTR               format

 L. 195      1428  LOAD_FAST                't0'
             1430  LOAD_ATTR                isot
             1432  STORE_FAST               't0'

 L. 196      1434  LOAD_FAST                'tf'
             1436  LOAD_ATTR                isot
             1438  STORE_FAST               'tf'

 L. 199      1440  BUILD_LIST_0          0 
             1442  STORE_FAST               'tt'

 L. 200      1444  SETUP_LOOP         1472  'to 1472'
             1446  LOAD_FAST                'time'
             1448  GET_ITER         
             1450  FOR_ITER           1470  'to 1470'
             1452  STORE_FAST               'i'

 L. 201      1454  LOAD_FAST                'tt'
             1456  LOAD_METHOD              append
             1458  LOAD_FAST                'i'
             1460  BUILD_LIST_1          1 
             1462  CALL_METHOD_1         1  '1 positional argument'
             1464  POP_TOP          
         1466_1468  JUMP_BACK          1450  'to 1450'
             1470  POP_BLOCK        
           1472_0  COME_FROM_LOOP     1444  '1444'

 L. 205      1472  LOAD_FAST                'np'
             1474  LOAD_ATTR                around
             1476  LOAD_FAST                'elev'
             1478  LOAD_CONST               4
             1480  LOAD_CONST               ('decimals',)
             1482  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1484  STORE_FAST               'elev'

 L. 206      1486  LOAD_FAST                'np'
             1488  LOAD_ATTR                around
             1490  LOAD_FAST                'azi'
             1492  LOAD_CONST               4
             1494  LOAD_CONST               ('decimals',)
             1496  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1498  STORE_FAST               'azi'

 L. 207      1500  LOAD_FAST                'np'
             1502  LOAD_METHOD              column_stack
             1504  LOAD_FAST                'time'
             1506  LOAD_FAST                'azi'
             1508  LOAD_FAST                'elev'
             1510  BUILD_TUPLE_3         3 
             1512  CALL_METHOD_1         1  '1 positional argument'
             1514  STORE_FAST               'final'

 L. 208      1516  LOAD_FAST                'np'
             1518  LOAD_METHOD              column_stack
             1520  LOAD_FAST                't0'
             1522  LOAD_FAST                'azi'
             1524  LOAD_CONST               0
             1526  BINARY_SUBSCR    
             1528  LOAD_FAST                'elev'
             1530  LOAD_CONST               0
             1532  BINARY_SUBSCR    
             1534  BUILD_TUPLE_3         3 
             1536  CALL_METHOD_1         1  '1 positional argument'
             1538  STORE_FAST               'r0'

 L. 209      1540  LOAD_FAST                'np'
             1542  LOAD_METHOD              column_stack
             1544  LOAD_FAST                'tf'
             1546  LOAD_FAST                'azi'
             1548  LOAD_CONST               -1
             1550  BINARY_SUBSCR    
             1552  LOAD_FAST                'elev'
             1554  LOAD_CONST               -1
             1556  BINARY_SUBSCR    
             1558  BUILD_TUPLE_3         3 
             1560  CALL_METHOD_1         1  '1 positional argument'
             1562  STORE_FAST               'rf'

 L. 210      1564  LOAD_FAST                'np'
             1566  LOAD_METHOD              vstack
             1568  LOAD_FAST                'r0'
             1570  LOAD_FAST                'final'
             1572  LOAD_FAST                'rf'
             1574  BUILD_TUPLE_3         3 
             1576  CALL_METHOD_1         1  '1 positional argument'
             1578  STORE_FAST               'final'

 L. 212      1580  LOAD_FAST                'np'
             1582  LOAD_METHOD              hstack
             1584  LOAD_FAST                'final'
             1586  LOAD_FAST                'np'
             1588  LOAD_METHOD              zeros
             1590  LOAD_FAST                'final'
             1592  LOAD_ATTR                shape
             1594  LOAD_CONST               0
             1596  BINARY_SUBSCR    
             1598  LOAD_CONST               10
             1600  BUILD_TUPLE_2         2 
             1602  CALL_METHOD_1         1  '1 positional argument'
             1604  BUILD_TUPLE_2         2 
             1606  CALL_METHOD_1         1  '1 positional argument'
             1608  STORE_FAST               'final'

 L. 233      1610  LOAD_STR                 '<FILE>\n<HEADER>\nGENERATION DATE       : '
             1612  LOAD_GLOBAL              str
             1614  LOAD_FAST                'nowtime'
             1616  CALL_FUNCTION_1       1  '1 positional argument'
             1618  BINARY_ADD       
             1620  LOAD_STR                 '\nANTENNA               : VIL-2\nLATITUDE              : 40d26m44.2s\nLONGITUDE             : -3d57m9.4s\nHEIGHT            [KM]: 0.6648\nTARGET                : '
             1622  BINARY_ADD       
             1624  LOAD_GLOBAL              str
             1626  LOAD_FAST                'source'
             1628  CALL_FUNCTION_1       1  '1 positional argument'
             1630  BINARY_ADD       
             1632  LOAD_STR                 '\nTRAJECTORY DATA SOURCE: CESAR/JPL\nS -DL-FREQUENCY  [MHZ]: 2277.000\nX -DL-FREQUENCY  [MHZ]: 0.000\nKA-DL-FREQUENCY  [MHZ]: 0.000\nANALYSIS PERIOD-START : '
             1634  BINARY_ADD       
             1636  LOAD_GLOBAL              str
             1638  LOAD_FAST                'obs_time'
             1640  LOAD_CONST               0
             1642  BINARY_SUBSCR    
             1644  CALL_FUNCTION_1       1  '1 positional argument'
             1646  BINARY_ADD       
             1648  LOAD_STR                 '\nANALYSIS PERIOD-END   : '
             1650  BINARY_ADD       
             1652  LOAD_GLOBAL              str
             1654  LOAD_FAST                'obs_time'
             1656  LOAD_CONST               -1
             1658  BINARY_SUBSCR    
             1660  CALL_FUNCTION_1       1  '1 positional argument'
             1662  BINARY_ADD       
             1664  LOAD_STR                 '\nNUMBER OF PASSES      : 2\n</HEADER>\n<PASS>\n'
             1666  BINARY_ADD       
             1668  LOAD_GLOBAL              str
             1670  LOAD_FAST                'obs_time'
             1672  LOAD_CONST               0
             1674  BINARY_SUBSCR    
             1676  CALL_FUNCTION_1       1  '1 positional argument'
             1678  BINARY_ADD       
             1680  LOAD_STR                 '  '
             1682  BINARY_ADD       
             1684  LOAD_GLOBAL              str
             1686  LOAD_FAST                'obs_time'
             1688  LOAD_CONST               -1
             1690  BINARY_SUBSCR    
             1692  CALL_FUNCTION_1       1  '1 positional argument'
             1694  BINARY_ADD       

 L. 234      1696  LOAD_STR                 '\n<ZPASS>\n</ZPASS>\n<WRAP>\n</WRAP>\n<INIT_TRAVEL_RANGE>\n<LOWER/>\n</INIT_TRAVEL_RANGE>\n   Date - Time        AZ (Deg) EL (Deg) TxRx dXEl (deg) TxRx dEl (deg)  Range (km) Range Rate (km/s)    S-Dop (Hz)      X-Dop (Hz)      Ka-Dop(Hz)      S-EIRP(dBw)     X-EIRP(dBW)     Ka-EIRP(dBW)\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
             1698  BINARY_ADD       
             1700  STORE_FAST               'header'

 L. 244      1702  LOAD_STR                 'date'
             1704  LOAD_FAST                'obs_time'
             1706  STORE_ATTR               out_subfmt

 L. 245      1708  LOAD_FAST                'np'
             1710  LOAD_ATTR                savetxt
             1712  LOAD_STR                 'certobs/track-'
             1714  LOAD_GLOBAL              str
             1716  LOAD_FAST                'source'
             1718  CALL_FUNCTION_1       1  '1 positional argument'
             1720  BINARY_ADD       
             1722  LOAD_GLOBAL              str
             1724  LOAD_FAST                'obs_time'
             1726  LOAD_CONST               0
             1728  BINARY_SUBSCR    
             1730  CALL_FUNCTION_1       1  '1 positional argument'
             1732  BINARY_ADD       
             1734  LOAD_STR                 '.txt'
             1736  BINARY_ADD       
             1738  LOAD_FAST                'final'
             1740  LOAD_STR                 '%s'
             1742  LOAD_STR                 ' '
             1744  LOAD_FAST                'header'
             1746  LOAD_STR                 '</PASS>\n</FILE>'
             1748  LOAD_STR                 ''
             1750  LOAD_CONST               ('fmt', 'delimiter', 'header', 'footer', 'comments')
             1752  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1754  POP_TOP          

 L. 247      1756  LOAD_STR                 'date_hms'
             1758  LOAD_FAST                'obs_time'
             1760  STORE_ATTR               out_subfmt
         1762_1764  JUMP_FORWARD       5700  'to 5700'
           1766_0  COME_FROM           322  '322'

 L. 249      1766  LOAD_FAST                'mode'
             1768  LOAD_STR                 'transit'
             1770  COMPARE_OP               ==
         1772_1774  POP_JUMP_IF_TRUE   1796  'to 1796'
             1776  LOAD_FAST                'mode'
             1778  LOAD_STR                 'Transit'
             1780  COMPARE_OP               ==
         1782_1784  POP_JUMP_IF_TRUE   1796  'to 1796'
             1786  LOAD_FAST                'mode'
             1788  LOAD_STR                 'TRANSIT'
             1790  COMPARE_OP               ==
         1792_1794  POP_JUMP_IF_FALSE  2872  'to 2872'
           1796_0  COME_FROM          1782  '1782'
           1796_1  COME_FROM          1772  '1772'

 L. 251      1796  LOAD_GLOBAL              input
             1798  LOAD_STR                 'Enter the starting time of the observation in the next format: 2010-12-31 00:00:00 (UTC time) \n'
             1800  CALL_FUNCTION_1       1  '1 positional argument'
             1802  BUILD_LIST_1          1 
             1804  STORE_FAST               'otime'

 L. 252      1806  LOAD_FAST                'Time'
             1808  LOAD_FAST                'otime'
             1810  LOAD_STR                 'iso'
             1812  LOAD_STR                 'utc'
             1814  LOAD_CONST               ('format', 'scale')
             1816  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1818  STORE_FAST               'obs_time'

 L. 263      1820  LOAD_FAST                'solar_system_ephemeris'
             1822  LOAD_METHOD              set
             1824  LOAD_STR                 'builtin'
             1826  CALL_METHOD_1         1  '1 positional argument'
             1828  SETUP_WITH         1932  'to 1932'
             1830  POP_TOP          

 L. 265      1832  LOAD_FAST                'get_body'
             1834  LOAD_STR                 'moon'
             1836  LOAD_FAST                'obs_time'
             1838  LOAD_FAST                'VIL2'
             1840  CALL_FUNCTION_3       3  '3 positional arguments'
             1842  STORE_FAST               'moon'

 L. 266      1844  LOAD_FAST                'get_body'
             1846  LOAD_STR                 'mercury'
             1848  LOAD_FAST                'obs_time'
             1850  LOAD_FAST                'VIL2'
             1852  CALL_FUNCTION_3       3  '3 positional arguments'
             1854  STORE_FAST               'mercury'

 L. 267      1856  LOAD_FAST                'get_body'
             1858  LOAD_STR                 'venus'
             1860  LOAD_FAST                'obs_time'
             1862  LOAD_FAST                'VIL2'
             1864  CALL_FUNCTION_3       3  '3 positional arguments'
             1866  STORE_FAST               'venus'

 L. 268      1868  LOAD_FAST                'get_body'
             1870  LOAD_STR                 'mars'
             1872  LOAD_FAST                'obs_time'
             1874  LOAD_FAST                'VIL2'
             1876  CALL_FUNCTION_3       3  '3 positional arguments'
             1878  STORE_FAST               'mars'

 L. 269      1880  LOAD_FAST                'get_body'
             1882  LOAD_STR                 'jupiter'
             1884  LOAD_FAST                'obs_time'
             1886  LOAD_FAST                'VIL2'
             1888  CALL_FUNCTION_3       3  '3 positional arguments'
             1890  STORE_FAST               'jupiter'

 L. 270      1892  LOAD_FAST                'get_body'
             1894  LOAD_STR                 'saturn'
             1896  LOAD_FAST                'obs_time'
             1898  LOAD_FAST                'VIL2'
             1900  CALL_FUNCTION_3       3  '3 positional arguments'
             1902  STORE_FAST               'saturn'

 L. 271      1904  LOAD_FAST                'get_body'
             1906  LOAD_STR                 'uranus'
             1908  LOAD_FAST                'obs_time'
             1910  LOAD_FAST                'VIL2'
             1912  CALL_FUNCTION_3       3  '3 positional arguments'
             1914  STORE_FAST               'uranus'

 L. 272      1916  LOAD_FAST                'get_body'
             1918  LOAD_STR                 'neptune'
             1920  LOAD_FAST                'obs_time'
             1922  LOAD_FAST                'VIL2'
             1924  CALL_FUNCTION_3       3  '3 positional arguments'
             1926  STORE_FAST               'neptune'
             1928  POP_BLOCK        
             1930  LOAD_CONST               None
           1932_0  COME_FROM_WITH     1828  '1828'
             1932  WITH_CLEANUP_START
             1934  WITH_CLEANUP_FINISH
             1936  END_FINALLY      

 L. 277      1938  LOAD_FAST                'moon'
             1940  LOAD_FAST                'mercury'
             1942  LOAD_FAST                'venus'
             1944  LOAD_FAST                'mars'
             1946  LOAD_FAST                'jupiter'
             1948  LOAD_FAST                'saturn'
             1950  LOAD_FAST                'uranus'
             1952  LOAD_FAST                'neptune'
             1954  BUILD_LIST_8          8 
             1956  STORE_FAST               'solar'

 L. 278      1958  LOAD_STR                 'moon'
             1960  LOAD_STR                 'mercury'
             1962  LOAD_STR                 'venus'
             1964  LOAD_STR                 'mars'
             1966  LOAD_STR                 'jupiter'
             1968  LOAD_STR                 'saturn'
             1970  LOAD_STR                 'uranus'
             1972  LOAD_STR                 'neptune'
             1974  BUILD_LIST_8          8 
             1976  STORE_FAST               'ss'

 L. 281      1978  LOAD_GLOBAL              input
             1980  LOAD_STR                 'Enter the name of the radio-source. Press ENTER if the source is neither in the catalogue nor a planet:\n'
             1982  CALL_FUNCTION_1       1  '1 positional argument'
             1984  STORE_FAST               'source'

 L. 283      1986  BUILD_LIST_0          0 
             1988  STORE_FAST               'name'

 L. 284      1990  BUILD_LIST_0          0 
             1992  STORE_FAST               'ra'

 L. 285      1994  BUILD_LIST_0          0 
             1996  STORE_FAST               'dec'

 L. 287      1998  SETUP_LOOP         2148  'to 2148'
             2000  LOAD_GLOBAL              enumerate
             2002  LOAD_FAST                'ss'
             2004  CALL_FUNCTION_1       1  '1 positional argument'
             2006  GET_ITER         
             2008  FOR_ITER           2146  'to 2146'
             2010  UNPACK_SEQUENCE_2     2 
             2012  STORE_FAST               'i'
             2014  STORE_FAST               'item'

 L. 290      2016  LOAD_FAST                'source'
             2018  LOAD_FAST                'item'
             2020  COMPARE_OP               ==
         2022_2024  POP_JUMP_IF_FALSE  2068  'to 2068'

 L. 291      2026  LOAD_FAST                'ss'
             2028  LOAD_FAST                'i'
             2030  BINARY_SUBSCR    
             2032  STORE_FAST               'name'

 L. 292      2034  LOAD_FAST                'solar'
             2036  LOAD_FAST                'i'
             2038  BINARY_SUBSCR    
             2040  LOAD_ATTR                ra
             2042  LOAD_ATTR                degree
             2044  LOAD_CONST               0
             2046  BINARY_SUBSCR    
             2048  STORE_FAST               'ra'

 L. 293      2050  LOAD_FAST                'solar'
             2052  LOAD_FAST                'i'
             2054  BINARY_SUBSCR    
             2056  LOAD_ATTR                dec
             2058  LOAD_ATTR                degree
             2060  LOAD_CONST               0
             2062  BINARY_SUBSCR    
             2064  STORE_FAST               'dec'
             2066  JUMP_BACK          2008  'to 2008'
           2068_0  COME_FROM          2022  '2022'

 L. 295      2068  SETUP_LOOP         2142  'to 2142'
             2070  LOAD_GLOBAL              enumerate
             2072  LOAD_FAST                'cata'
             2074  CALL_FUNCTION_1       1  '1 positional argument'
             2076  GET_ITER         
           2078_0  COME_FROM          2096  '2096'
             2078  FOR_ITER           2140  'to 2140'
             2080  UNPACK_SEQUENCE_2     2 
             2082  STORE_FAST               'a'
             2084  STORE_FAST               'atem'

 L. 298      2086  LOAD_FAST                'source'
             2088  LOAD_FAST                'atem'
             2090  LOAD_CONST               0
             2092  BINARY_SUBSCR    
             2094  COMPARE_OP               ==
         2096_2098  POP_JUMP_IF_FALSE  2078  'to 2078'

 L. 299      2100  LOAD_FAST                'cata'
             2102  LOAD_FAST                'a'
             2104  BINARY_SUBSCR    
             2106  LOAD_CONST               1
             2108  BINARY_SUBSCR    
             2110  STORE_FAST               'name'

 L. 300      2112  LOAD_FAST                'cata'
             2114  LOAD_FAST                'a'
             2116  BINARY_SUBSCR    
             2118  LOAD_CONST               2
             2120  BINARY_SUBSCR    
             2122  STORE_FAST               'ra'

 L. 301      2124  LOAD_FAST                'cata'
             2126  LOAD_FAST                'a'
             2128  BINARY_SUBSCR    
             2130  LOAD_CONST               3
             2132  BINARY_SUBSCR    
             2134  STORE_FAST               'dec'
         2136_2138  JUMP_BACK          2078  'to 2078'
             2140  POP_BLOCK        
           2142_0  COME_FROM_LOOP     2068  '2068'
         2142_2144  JUMP_BACK          2008  'to 2008'
             2146  POP_BLOCK        
           2148_0  COME_FROM_LOOP     1998  '1998'

 L. 302      2148  LOAD_FAST                'name'
             2150  BUILD_LIST_0          0 
             2152  COMPARE_OP               ==
         2154_2156  POP_JUMP_IF_FALSE  2188  'to 2188'

 L. 303      2158  LOAD_STR                 'unknown source'
             2160  STORE_FAST               'name'

 L. 304      2162  LOAD_GLOBAL              float
             2164  LOAD_GLOBAL              input
             2166  LOAD_STR                 'Enter manually the desired right ascension: '
             2168  CALL_FUNCTION_1       1  '1 positional argument'
             2170  CALL_FUNCTION_1       1  '1 positional argument'
             2172  STORE_FAST               'ra'

 L. 305      2174  LOAD_GLOBAL              float
             2176  LOAD_GLOBAL              input
             2178  LOAD_STR                 'Enter manually the desired declination: '
             2180  CALL_FUNCTION_1       1  '1 positional argument'
             2182  CALL_FUNCTION_1       1  '1 positional argument'
             2184  STORE_FAST               'dec'
             2186  JUMP_FORWARD       2188  'to 2188'
           2188_0  COME_FROM          2186  '2186'
           2188_1  COME_FROM          2154  '2154'

 L. 310      2188  LOAD_FAST                'SkyCoord'
             2190  LOAD_FAST                'Angle'
             2192  LOAD_FAST                'ra'
             2194  LOAD_FAST                'u'
             2196  LOAD_ATTR                deg
             2198  LOAD_CONST               ('unit',)
             2200  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2202  LOAD_FAST                'Angle'
             2204  LOAD_FAST                'dec'
             2206  LOAD_FAST                'u'
             2208  LOAD_ATTR                deg
             2210  LOAD_CONST               ('unit',)
             2212  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2214  LOAD_STR                 'icrs'
             2216  LOAD_CONST               ('frame',)
             2218  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2220  STORE_FAST               'obj'

 L. 313      2222  LOAD_FAST                'obj'
             2224  LOAD_METHOD              transform_to
             2226  LOAD_FAST                'ITRS'
             2228  LOAD_FAST                'obs_time'
             2230  LOAD_CONST               ('obstime',)
             2232  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2234  CALL_METHOD_1         1  '1 positional argument'
             2236  STORE_FAST               'obj_itrs'

 L. 315      2238  LOAD_FAST                'VIL2'
             2240  LOAD_ATTR                lon
             2242  LOAD_FAST                'obj_itrs'
             2244  LOAD_ATTR                spherical
             2246  LOAD_ATTR                lon
             2248  BINARY_SUBTRACT  
             2250  STORE_FAST               'local_ha'

 L. 316      2252  LOAD_FAST                'local_ha'
             2254  LOAD_ATTR                wrap_at
             2256  LOAD_CONST               24
             2258  LOAD_FAST                'u'
             2260  LOAD_ATTR                hourangle
             2262  BINARY_MULTIPLY  
             2264  LOAD_CONST               True
             2266  LOAD_CONST               ('inplace',)
             2268  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2270  POP_TOP          

 L. 318      2272  LOAD_FAST                'obj_itrs'
             2274  LOAD_ATTR                spherical
             2276  LOAD_ATTR                lat
             2278  STORE_FAST               'local_dec'

 L. 319      2280  LOAD_GLOBAL              print
             2282  LOAD_STR                 'Local apparent HA, Dec={} {}'
             2284  LOAD_METHOD              format
             2286  LOAD_FAST                'local_ha'
             2288  LOAD_ATTR                to_string
             2290  LOAD_FAST                'u'
             2292  LOAD_ATTR                hourangle

 L. 320      2294  LOAD_STR                 ':'
             2296  LOAD_CONST               ('unit', 'sep')
             2298  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2300  LOAD_FAST                'local_dec'
             2302  LOAD_ATTR                to_string
             2304  LOAD_FAST                'u'
             2306  LOAD_ATTR                deg
             2308  LOAD_STR                 ':'
             2310  LOAD_CONST               True
             2312  LOAD_CONST               ('unit', 'sep', 'alwayssign')
             2314  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2316  CALL_METHOD_2         2  '2 positional arguments'
             2318  CALL_FUNCTION_1       1  '1 positional argument'
             2320  POP_TOP          

 L. 329      2322  LOAD_GLOBAL              float
             2324  LOAD_GLOBAL              input
             2326  LOAD_STR                 'Enter the duration of the transit, in minutes: '
             2328  CALL_FUNCTION_1       1  '1 positional argument'
             2330  CALL_FUNCTION_1       1  '1 positional argument'
             2332  STORE_FAST               'duration'

 L. 331      2334  LOAD_FAST                'obs_time'
             2336  LOAD_CONST               0
             2338  BINARY_SUBSCR    
             2340  STORE_FAST               't'

 L. 335      2342  LOAD_FAST                'TimeDelta'
             2344  LOAD_CONST               300
             2346  LOAD_STR                 'sec'
             2348  LOAD_CONST               ('format',)
             2350  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2352  STORE_FAST               'pre'

 L. 336      2354  LOAD_FAST                'TimeDelta'
             2356  LOAD_FAST                'duration'
             2358  LOAD_CONST               60
             2360  BINARY_MULTIPLY  
             2362  LOAD_STR                 'sec'
             2364  LOAD_CONST               ('format',)
             2366  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2368  STORE_FAST               'dur'

 L. 337      2370  LOAD_FAST                't'
             2372  LOAD_FAST                'pre'
             2374  BINARY_SUBTRACT  
             2376  STORE_FAST               't0'

 L. 338      2378  LOAD_FAST                't'
             2380  LOAD_FAST                'dur'
             2382  BINARY_ADD       
             2384  STORE_FAST               'obs_time_end'

 L. 339      2386  LOAD_FAST                't'
             2388  LOAD_FAST                'dur'
             2390  BINARY_ADD       
             2392  LOAD_FAST                'pre'
             2394  BINARY_ADD       
             2396  STORE_FAST               'tf'

 L. 342      2398  BUILD_LIST_0          0 
             2400  STORE_FAST               'completecoords'

 L. 343      2402  BUILD_LIST_0          0 
             2404  STORE_FAST               'time'

 L. 347      2406  LOAD_FAST                'obj'
             2408  LOAD_METHOD              transform_to
             2410  LOAD_FAST                'AltAz'
             2412  LOAD_FAST                't'
             2414  LOAD_FAST                'VIL2'
             2416  LOAD_CONST               ('obstime', 'location')
             2418  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2420  CALL_METHOD_1         1  '1 positional argument'
             2422  STORE_FAST               'new'

 L. 348      2424  LOAD_FAST                'new'
             2426  LOAD_ATTR                alt
             2428  LOAD_ATTR                degree
             2430  STORE_FAST               'alti'

 L. 349      2432  LOAD_FAST                'new'
             2434  LOAD_ATTR                az
             2436  LOAD_ATTR                degree
             2438  STORE_FAST               'azi'

 L. 350      2440  LOAD_FAST                't'
             2442  LOAD_ATTR                isot
             2444  LOAD_FAST                'azi'
             2446  LOAD_FAST                'alti'
             2448  BUILD_TUPLE_3         3 
             2450  STORE_FAST               'completecoords'

 L. 353      2452  LOAD_FAST                'alti'
             2454  LOAD_CONST               10
             2456  COMPARE_OP               <
         2458_2460  POP_JUMP_IF_FALSE  2478  'to 2478'

 L. 354      2462  LOAD_FAST                'np'
             2464  LOAD_ATTR                ma
             2466  LOAD_ATTR                masked
             2468  STORE_FAST               'completecoords'

 L. 355      2470  LOAD_GLOBAL              print
             2472  LOAD_STR                 'Too low pointing'
             2474  CALL_FUNCTION_1       1  '1 positional argument'
             2476  POP_TOP          
           2478_0  COME_FROM          2458  '2458'

 L. 360      2478  BUILD_LIST_0          0 
             2480  STORE_FAST               'r'

 L. 361      2482  BUILD_LIST_0          0 
             2484  STORE_FAST               'elev'

 L. 362      2486  LOAD_CONST               1.00031
             2488  STORE_FAST               'n0'

 L. 363      2490  LOAD_FAST                'np'
             2492  LOAD_METHOD              deg2rad
             2494  LOAD_FAST                'alti'
             2496  LOAD_CONST               4.7
             2498  LOAD_CONST               2.24
             2500  LOAD_FAST                'alti'
             2502  BINARY_ADD       
             2504  BINARY_TRUE_DIVIDE
             2506  BINARY_ADD       
             2508  CALL_METHOD_1         1  '1 positional argument'
             2510  STORE_FAST               'p'

 L. 364      2512  LOAD_FAST                'n0'
             2514  LOAD_CONST               1
             2516  BINARY_SUBTRACT  
             2518  LOAD_CONST               1
             2520  BINARY_MULTIPLY  
             2522  LOAD_FAST                'np'
             2524  LOAD_METHOD              tan
             2526  LOAD_FAST                'p'
             2528  CALL_METHOD_1         1  '1 positional argument'
             2530  BINARY_TRUE_DIVIDE
             2532  STORE_FAST               'r'

 L. 365      2534  LOAD_FAST                'alti'
             2536  LOAD_FAST                'r'
             2538  BINARY_ADD       
             2540  BUILD_LIST_1          1 
             2542  STORE_FAST               'elev'

 L. 368      2544  LOAD_CONST               85
             2546  STORE_FAST               'max_elev'

 L. 369      2548  LOAD_GLOBAL              max
             2550  LOAD_FAST                'elev'
             2552  CALL_FUNCTION_1       1  '1 positional argument'
             2554  LOAD_FAST                'max_elev'
             2556  COMPARE_OP               >
         2558_2560  POP_JUMP_IF_FALSE  2570  'to 2570'

 L. 370      2562  LOAD_GLOBAL              print
             2564  LOAD_STR                 'DANGER: TOO HIGH ELEVATION. THERE MIGHT BE TRACKING ISSUES'
             2566  CALL_FUNCTION_1       1  '1 positional argument'
             2568  POP_TOP          
           2570_0  COME_FROM          2558  '2558'

 L. 373      2570  LOAD_STR                 'isot'
             2572  LOAD_FAST                't'
             2574  STORE_ATTR               format

 L. 374      2576  LOAD_FAST                't0'
             2578  LOAD_ATTR                isot
             2580  STORE_FAST               't0'

 L. 375      2582  LOAD_FAST                'tf'
             2584  LOAD_ATTR                isot
             2586  STORE_FAST               'tf'

 L. 377      2588  BUILD_LIST_0          0 
             2590  STORE_FAST               'tt'

 L. 378      2592  SETUP_LOOP         2620  'to 2620'
             2594  LOAD_FAST                'time'
             2596  GET_ITER         
             2598  FOR_ITER           2618  'to 2618'
             2600  STORE_FAST               'i'

 L. 379      2602  LOAD_FAST                'tt'
             2604  LOAD_METHOD              append
             2606  LOAD_FAST                'i'
             2608  BUILD_LIST_1          1 
             2610  CALL_METHOD_1         1  '1 positional argument'
             2612  POP_TOP          
         2614_2616  JUMP_BACK          2598  'to 2598'
             2618  POP_BLOCK        
           2620_0  COME_FROM_LOOP     2592  '2592'

 L. 383      2620  LOAD_FAST                'np'
             2622  LOAD_ATTR                around
             2624  LOAD_FAST                'elev'
             2626  LOAD_CONST               4
             2628  LOAD_CONST               ('decimals',)
             2630  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2632  STORE_FAST               'elev'

 L. 384      2634  LOAD_FAST                'np'
             2636  LOAD_ATTR                around
             2638  LOAD_FAST                'azi'
             2640  LOAD_CONST               4
             2642  LOAD_CONST               ('decimals',)
             2644  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2646  STORE_FAST               'azi'

 L. 386      2648  LOAD_FAST                'np'
             2650  LOAD_METHOD              column_stack
             2652  LOAD_FAST                't0'
             2654  LOAD_FAST                'azi'
             2656  LOAD_FAST                'elev'
             2658  BUILD_TUPLE_3         3 
             2660  CALL_METHOD_1         1  '1 positional argument'
             2662  STORE_FAST               'r0'

 L. 387      2664  LOAD_FAST                'np'
             2666  LOAD_METHOD              column_stack
             2668  LOAD_FAST                'tf'
             2670  LOAD_FAST                'azi'
             2672  LOAD_FAST                'elev'
             2674  BUILD_TUPLE_3         3 
             2676  CALL_METHOD_1         1  '1 positional argument'
             2678  STORE_FAST               'rf'

 L. 388      2680  LOAD_FAST                'np'
             2682  LOAD_METHOD              vstack
             2684  LOAD_FAST                'r0'
             2686  LOAD_FAST                'rf'
             2688  BUILD_TUPLE_2         2 
             2690  CALL_METHOD_1         1  '1 positional argument'
             2692  STORE_FAST               'final'

 L. 389      2694  LOAD_FAST                'np'
             2696  LOAD_METHOD              hstack
             2698  LOAD_FAST                'final'
             2700  LOAD_FAST                'np'
             2702  LOAD_METHOD              zeros
             2704  LOAD_FAST                'final'
             2706  LOAD_ATTR                shape
             2708  LOAD_CONST               0
             2710  BINARY_SUBSCR    
             2712  LOAD_CONST               10
             2714  BUILD_TUPLE_2         2 
             2716  CALL_METHOD_1         1  '1 positional argument'
             2718  BUILD_TUPLE_2         2 
             2720  CALL_METHOD_1         1  '1 positional argument'
             2722  STORE_FAST               'final'

 L. 410      2724  LOAD_STR                 '<FILE>\n<HEADER>\nGENERATION DATE       : '
             2726  LOAD_GLOBAL              str
             2728  LOAD_FAST                'nowtime'
             2730  CALL_FUNCTION_1       1  '1 positional argument'
             2732  BINARY_ADD       
             2734  LOAD_STR                 '\nANTENNA               : VIL-2\nLATITUDE              : 40d26m44.2s\nLONGITUDE             : -3d57m9.4s\nHEIGHT            [KM]: 0.6648\nTARGET                : '
             2736  BINARY_ADD       
             2738  LOAD_GLOBAL              str
             2740  LOAD_FAST                'source'
             2742  CALL_FUNCTION_1       1  '1 positional argument'
             2744  BINARY_ADD       
             2746  LOAD_STR                 '\nTRAJECTORY DATA SOURCE: CESAR/JPL\nS -DL-FREQUENCY  [MHZ]: 2277.000\nX -DL-FREQUENCY  [MHZ]: 0.000\nKA-DL-FREQUENCY  [MHZ]: 0.000\nANALYSIS PERIOD-START : '
             2748  BINARY_ADD       
             2750  LOAD_GLOBAL              str
             2752  LOAD_FAST                'obs_time'
             2754  LOAD_CONST               0
             2756  BINARY_SUBSCR    
             2758  CALL_FUNCTION_1       1  '1 positional argument'
             2760  BINARY_ADD       
             2762  LOAD_STR                 '\nANALYSIS PERIOD-END   : '
             2764  BINARY_ADD       
             2766  LOAD_GLOBAL              str
             2768  LOAD_FAST                'obs_time_end'
             2770  CALL_FUNCTION_1       1  '1 positional argument'
             2772  BINARY_ADD       
             2774  LOAD_STR                 '\nNUMBER OF PASSES      : 2\n</HEADER>\n<PASS>\n'
             2776  BINARY_ADD       
             2778  LOAD_GLOBAL              str
             2780  LOAD_FAST                'obs_time'
             2782  LOAD_CONST               0
             2784  BINARY_SUBSCR    
             2786  CALL_FUNCTION_1       1  '1 positional argument'
             2788  BINARY_ADD       
             2790  LOAD_STR                 '  '
             2792  BINARY_ADD       
             2794  LOAD_GLOBAL              str
             2796  LOAD_FAST                'obs_time_end'
             2798  CALL_FUNCTION_1       1  '1 positional argument'
             2800  BINARY_ADD       

 L. 411      2802  LOAD_STR                 '\n<ZPASS>\n</ZPASS>\n<WRAP>\n</WRAP>\n<INIT_TRAVEL_RANGE>\n<LOWER/>\n</INIT_TRAVEL_RANGE>\n   Date - Time        AZ (Deg) EL (Deg) TxRx dXEl (deg) TxRx dEl (deg)  Range (km) Range Rate (km/s)    S-Dop (Hz)      X-Dop (Hz)      Ka-Dop(Hz)      S-EIRP(dBw)     X-EIRP(dBW)     Ka-EIRP(dBW)\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
             2804  BINARY_ADD       
             2806  STORE_FAST               'header'

 L. 421      2808  LOAD_STR                 'date'
             2810  LOAD_FAST                'obs_time'
             2812  STORE_ATTR               out_subfmt

 L. 422      2814  LOAD_FAST                'np'
             2816  LOAD_ATTR                savetxt
             2818  LOAD_STR                 'certobs/transit-'
             2820  LOAD_GLOBAL              str
             2822  LOAD_FAST                'source'
             2824  CALL_FUNCTION_1       1  '1 positional argument'
             2826  BINARY_ADD       
             2828  LOAD_GLOBAL              str
             2830  LOAD_FAST                'obs_time'
             2832  LOAD_CONST               0
             2834  BINARY_SUBSCR    
             2836  CALL_FUNCTION_1       1  '1 positional argument'
             2838  BINARY_ADD       
             2840  LOAD_STR                 '.txt'
             2842  BINARY_ADD       
             2844  LOAD_FAST                'final'
             2846  LOAD_STR                 '%s'
             2848  LOAD_STR                 ' '
             2850  LOAD_FAST                'header'
             2852  LOAD_STR                 '</PASS>\n</FILE>'
             2854  LOAD_STR                 ''
             2856  LOAD_CONST               ('fmt', 'delimiter', 'header', 'footer', 'comments')
             2858  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2860  POP_TOP          

 L. 424      2862  LOAD_STR                 'date_hms'
             2864  LOAD_FAST                'obs_time'
             2866  STORE_ATTR               out_subfmt
         2868_2870  JUMP_FORWARD       5700  'to 5700'
           2872_0  COME_FROM          1792  '1792'

 L. 427      2872  LOAD_FAST                'mode'
             2874  LOAD_STR                 'tipping curve'
             2876  COMPARE_OP               ==
         2878_2880  POP_JUMP_IF_TRUE   2932  'to 2932'
             2882  LOAD_FAST                'mode'
             2884  LOAD_STR                 'tipping'
             2886  COMPARE_OP               ==
         2888_2890  POP_JUMP_IF_TRUE   2932  'to 2932'
             2892  LOAD_FAST                'mode'
             2894  LOAD_STR                 'tip'
             2896  COMPARE_OP               ==
         2898_2900  POP_JUMP_IF_TRUE   2932  'to 2932'
             2902  LOAD_FAST                'mode'
             2904  LOAD_STR                 'TIPPING'
             2906  COMPARE_OP               ==
         2908_2910  POP_JUMP_IF_TRUE   2932  'to 2932'
             2912  LOAD_FAST                'mode'
             2914  LOAD_STR                 'TIP'
             2916  COMPARE_OP               ==
         2918_2920  POP_JUMP_IF_TRUE   2932  'to 2932'
             2922  LOAD_FAST                'mode'
             2924  LOAD_STR                 'Tipping'
             2926  COMPARE_OP               ==
         2928_2930  POP_JUMP_IF_FALSE  3482  'to 3482'
           2932_0  COME_FROM          2918  '2918'
           2932_1  COME_FROM          2908  '2908'
           2932_2  COME_FROM          2898  '2898'
           2932_3  COME_FROM          2888  '2888'
           2932_4  COME_FROM          2878  '2878'

 L. 429      2932  LOAD_GLOBAL              input
             2934  LOAD_STR                 'Enter the starting time of the observation in the next format: 2010-12-31 00:00:00 (UTC time) \n'
             2936  CALL_FUNCTION_1       1  '1 positional argument'
             2938  BUILD_LIST_1          1 
             2940  STORE_FAST               'otime'

 L. 430      2942  LOAD_FAST                'Time'
             2944  LOAD_FAST                'otime'
             2946  LOAD_STR                 'iso'
             2948  LOAD_STR                 'utc'
             2950  LOAD_CONST               ('format', 'scale')
             2952  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2954  STORE_FAST               'obs_time'

 L. 435      2956  LOAD_CONST               2
             2958  STORE_FAST               'dt'

 L. 436      2960  LOAD_FAST                'TimeDelta'
             2962  LOAD_FAST                'dt'
             2964  LOAD_STR                 'sec'
             2966  LOAD_CONST               ('format',)
             2968  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2970  STORE_FAST               'dt2'

 L. 438      2972  LOAD_FAST                'TimeDelta'
             2974  LOAD_CONST               300
             2976  LOAD_STR                 'sec'
             2978  LOAD_CONST               ('format',)
             2980  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2982  STORE_FAST               'pre'

 L. 440      2984  LOAD_FAST                'obs_time'
             2986  LOAD_CONST               0
             2988  BINARY_SUBSCR    
             2990  LOAD_FAST                'pre'
             2992  BINARY_SUBTRACT  
             2994  STORE_FAST               't0'

 L. 442      2996  LOAD_FAST                'np'
             2998  LOAD_METHOD              linspace
             3000  LOAD_CONST               0
             3002  LOAD_CONST               90
             3004  LOAD_CONST               91
             3006  CALL_METHOD_3         3  '3 positional arguments'
             3008  STORE_FAST               'suc'

 L. 443      3010  LOAD_GLOBAL              list
             3012  CALL_FUNCTION_0       0  '0 positional arguments'
             3014  STORE_FAST               't'

 L. 444      3016  LOAD_FAST                't'
             3018  LOAD_METHOD              append
             3020  LOAD_FAST                'obs_time'
             3022  LOAD_CONST               0
             3024  BINARY_SUBSCR    
             3026  CALL_METHOD_1         1  '1 positional argument'
             3028  POP_TOP          

 L. 445      3030  SETUP_LOOP         3086  'to 3086'
             3032  LOAD_GLOBAL              enumerate
             3034  LOAD_FAST                'suc'
             3036  CALL_FUNCTION_1       1  '1 positional argument'
             3038  GET_ITER         
           3040_0  COME_FROM          3054  '3054'
             3040  FOR_ITER           3084  'to 3084'
             3042  UNPACK_SEQUENCE_2     2 
             3044  STORE_FAST               'i'
             3046  STORE_FAST               'tex'

 L. 446      3048  LOAD_FAST                'i'
             3050  LOAD_CONST               0
             3052  COMPARE_OP               >
         3054_3056  POP_JUMP_IF_FALSE  3040  'to 3040'

 L. 447      3058  LOAD_FAST                't'
             3060  LOAD_METHOD              append
             3062  LOAD_FAST                't'
             3064  LOAD_FAST                'i'
             3066  LOAD_CONST               1
             3068  BINARY_SUBTRACT  
             3070  BINARY_SUBSCR    
             3072  LOAD_FAST                'dt2'
             3074  BINARY_ADD       
             3076  CALL_METHOD_1         1  '1 positional argument'
             3078  POP_TOP          
         3080_3082  JUMP_BACK          3040  'to 3040'
             3084  POP_BLOCK        
           3086_0  COME_FROM_LOOP     3030  '3030'

 L. 449      3086  LOAD_GLOBAL              float
             3088  LOAD_GLOBAL              input
             3090  LOAD_STR                 'Enter the azimuth for the tipping curve: '
             3092  CALL_FUNCTION_1       1  '1 positional argument'
             3094  CALL_FUNCTION_1       1  '1 positional argument'
             3096  STORE_FAST               'azimuth'

 L. 453      3098  BUILD_LIST_0          0 
             3100  STORE_FAST               'elev'

 L. 454      3102  BUILD_LIST_0          0 
             3104  STORE_FAST               'azi'

 L. 455      3106  SETUP_LOOP         3150  'to 3150'
             3108  LOAD_GLOBAL              enumerate
             3110  LOAD_FAST                'suc'
             3112  CALL_FUNCTION_1       1  '1 positional argument'
             3114  GET_ITER         
             3116  FOR_ITER           3148  'to 3148'
             3118  UNPACK_SEQUENCE_2     2 
             3120  STORE_FAST               'i'
             3122  STORE_FAST               'tex'

 L. 456      3124  LOAD_FAST                'elev'
             3126  LOAD_METHOD              append
             3128  LOAD_FAST                'tex'
             3130  CALL_METHOD_1         1  '1 positional argument'
             3132  POP_TOP          

 L. 457      3134  LOAD_FAST                'azi'
             3136  LOAD_METHOD              append
             3138  LOAD_FAST                'azimuth'
             3140  CALL_METHOD_1         1  '1 positional argument'
             3142  POP_TOP          
         3144_3146  JUMP_BACK          3116  'to 3116'
             3148  POP_BLOCK        
           3150_0  COME_FROM_LOOP     3106  '3106'

 L. 461      3150  BUILD_LIST_0          0 
             3152  STORE_FAST               'completecoords'

 L. 463      3154  SETUP_LOOP         3212  'to 3212'
             3156  LOAD_GLOBAL              enumerate
             3158  LOAD_FAST                'suc'
             3160  CALL_FUNCTION_1       1  '1 positional argument'
             3162  GET_ITER         
             3164  FOR_ITER           3210  'to 3210'
             3166  UNPACK_SEQUENCE_2     2 
             3168  STORE_FAST               'i'
             3170  STORE_FAST               'tex'

 L. 464      3172  LOAD_FAST                't'
             3174  LOAD_FAST                'i'
             3176  BINARY_SUBSCR    
             3178  LOAD_ATTR                isot
             3180  LOAD_FAST                'elev'
             3182  LOAD_FAST                'i'
             3184  BINARY_SUBSCR    
             3186  LOAD_FAST                'azi'
             3188  LOAD_FAST                'i'
             3190  BINARY_SUBSCR    
             3192  BUILD_TUPLE_3         3 
             3194  STORE_FAST               'cco'

 L. 465      3196  LOAD_FAST                'completecoords'
             3198  LOAD_METHOD              append
             3200  LOAD_FAST                'cco'
             3202  CALL_METHOD_1         1  '1 positional argument'
             3204  POP_TOP          
         3206_3208  JUMP_BACK          3164  'to 3164'
             3210  POP_BLOCK        
           3212_0  COME_FROM_LOOP     3154  '3154'

 L. 468      3212  SETUP_LOOP         3246  'to 3246'
             3214  LOAD_GLOBAL              enumerate
             3216  LOAD_FAST                't'
             3218  CALL_FUNCTION_1       1  '1 positional argument'
             3220  GET_ITER         
             3222  FOR_ITER           3244  'to 3244'
             3224  UNPACK_SEQUENCE_2     2 
             3226  STORE_FAST               'i'
             3228  STORE_FAST               'tex'

 L. 469      3230  LOAD_STR                 'isot'
             3232  LOAD_FAST                't'
             3234  LOAD_FAST                'i'
             3236  BINARY_SUBSCR    
             3238  STORE_ATTR               format
         3240_3242  JUMP_BACK          3222  'to 3222'
             3244  POP_BLOCK        
           3246_0  COME_FROM_LOOP     3212  '3212'

 L. 471      3246  LOAD_FAST                't0'
             3248  LOAD_ATTR                isot
             3250  STORE_FAST               't0'

 L. 472      3252  LOAD_FAST                't'
             3254  LOAD_CONST               -1
             3256  BINARY_SUBSCR    
             3258  LOAD_FAST                't'
             3260  LOAD_CONST               0
             3262  BINARY_SUBSCR    
             3264  BINARY_SUBTRACT  
             3266  STORE_FAST               'duration'

 L. 476      3268  BUILD_LIST_0          0 
             3270  STORE_FAST               'final'

 L. 477      3272  LOAD_FAST                'np'
             3274  LOAD_METHOD              column_stack
             3276  LOAD_FAST                't'
             3278  LOAD_FAST                'azi'
             3280  LOAD_FAST                'elev'
             3282  BUILD_TUPLE_3         3 
             3284  CALL_METHOD_1         1  '1 positional argument'
             3286  STORE_FAST               'final'

 L. 478      3288  LOAD_FAST                't0'
             3290  LOAD_FAST                'azi'
             3292  LOAD_CONST               0
             3294  BINARY_SUBSCR    
             3296  LOAD_FAST                'elev'
             3298  LOAD_CONST               0
             3300  BINARY_SUBSCR    
             3302  BUILD_TUPLE_3         3 
             3304  STORE_FAST               'r0'

 L. 480      3306  LOAD_FAST                'np'
             3308  LOAD_METHOD              vstack
             3310  LOAD_FAST                'r0'
             3312  LOAD_FAST                'final'
             3314  BUILD_TUPLE_2         2 
             3316  CALL_METHOD_1         1  '1 positional argument'
             3318  STORE_FAST               'final'

 L. 481      3320  LOAD_FAST                'np'
             3322  LOAD_METHOD              hstack
             3324  LOAD_FAST                'final'
             3326  LOAD_FAST                'np'
             3328  LOAD_METHOD              zeros
             3330  LOAD_FAST                'final'
             3332  LOAD_ATTR                shape
             3334  LOAD_CONST               0
             3336  BINARY_SUBSCR    
             3338  LOAD_CONST               10
             3340  BUILD_TUPLE_2         2 
             3342  CALL_METHOD_1         1  '1 positional argument'
             3344  BUILD_TUPLE_2         2 
             3346  CALL_METHOD_1         1  '1 positional argument'
             3348  STORE_FAST               'final'

 L. 502      3350  LOAD_STR                 '<FILE>\n<HEADER>\nGENERATION DATE       : '
             3352  LOAD_GLOBAL              str
             3354  LOAD_FAST                'nowtime'
             3356  CALL_FUNCTION_1       1  '1 positional argument'
             3358  BINARY_ADD       
             3360  LOAD_STR                 '\nANTENNA               : VIL-2\nLATITUDE              : 40d26m44.2s\nLONGITUDE             : -3d57m9.4s\nHEIGHT            [KM]: 0.6648\nTARGET                : TIPPING CURVE\nTRAJECTORY DATA SOURCE: CESAR/JPL\nS -DL-FREQUENCY  [MHZ]: 2277.000\nX -DL-FREQUENCY  [MHZ]: 0.000\nKA-DL-FREQUENCY  [MHZ]: 0.000\nANALYSIS PERIOD-START : '
             3362  BINARY_ADD       
             3364  LOAD_GLOBAL              str
             3366  LOAD_FAST                'obs_time'
             3368  LOAD_CONST               0
             3370  BINARY_SUBSCR    
             3372  CALL_FUNCTION_1       1  '1 positional argument'
             3374  BINARY_ADD       
             3376  LOAD_STR                 '\nANALYSIS PERIOD-END   : '
             3378  BINARY_ADD       
             3380  LOAD_GLOBAL              str
             3382  LOAD_FAST                'obs_time'
             3384  LOAD_CONST               -1
             3386  BINARY_SUBSCR    
             3388  CALL_FUNCTION_1       1  '1 positional argument'
             3390  BINARY_ADD       
             3392  LOAD_STR                 '\nNUMBER OF PASSES      : 2\n</HEADER>\n<PASS>\n'
             3394  BINARY_ADD       
             3396  LOAD_GLOBAL              str
             3398  LOAD_FAST                'obs_time'
             3400  LOAD_CONST               0
             3402  BINARY_SUBSCR    
             3404  CALL_FUNCTION_1       1  '1 positional argument'
             3406  BINARY_ADD       
             3408  LOAD_STR                 '  '
             3410  BINARY_ADD       
             3412  LOAD_GLOBAL              str
             3414  LOAD_FAST                'obs_time'
             3416  LOAD_CONST               -1
             3418  BINARY_SUBSCR    
             3420  CALL_FUNCTION_1       1  '1 positional argument'
             3422  BINARY_ADD       

 L. 503      3424  LOAD_STR                 '\n<ZPASS>\n</ZPASS>\n<WRAP>\n</WRAP>\n<INIT_TRAVEL_RANGE>\n<LOWER/>\n</INIT_TRAVEL_RANGE>\n   Date - Time        AZ (Deg) EL (Deg) TxRx dXEl (deg) TxRx dEl (deg)  Range (km) Range Rate (km/s)    S-Dop (Hz)      X-Dop (Hz)      Ka-Dop(Hz)      S-EIRP(dBw)     X-EIRP(dBW)     Ka-EIRP(dBW)\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
             3426  BINARY_ADD       
             3428  STORE_FAST               'header'

 L. 513      3430  LOAD_STR                 'date'
             3432  LOAD_FAST                'obs_time'
             3434  STORE_ATTR               out_subfmt

 L. 514      3436  LOAD_FAST                'np'
             3438  LOAD_ATTR                savetxt
             3440  LOAD_STR                 'certobs/tip-'
             3442  LOAD_GLOBAL              str
             3444  LOAD_FAST                'nowtime'
             3446  CALL_FUNCTION_1       1  '1 positional argument'
             3448  BINARY_ADD       
             3450  LOAD_STR                 '.txt'
             3452  BINARY_ADD       
             3454  LOAD_FAST                'final'
             3456  LOAD_STR                 '%s'
             3458  LOAD_STR                 ' '
             3460  LOAD_FAST                'header'
             3462  LOAD_STR                 '</PASS>\n</FILE>'
             3464  LOAD_STR                 ''
             3466  LOAD_CONST               ('fmt', 'delimiter', 'header', 'footer', 'comments')
             3468  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             3470  POP_TOP          

 L. 516      3472  LOAD_STR                 'date_hms'
             3474  LOAD_FAST                'obs_time'
             3476  STORE_ATTR               out_subfmt
         3478_3480  JUMP_FORWARD       5700  'to 5700'
           3482_0  COME_FROM          2928  '2928'

 L. 518      3482  LOAD_FAST                'mode'
             3484  LOAD_STR                 'scanning'
             3486  COMPARE_OP               ==
         3488_3490  POP_JUMP_IF_TRUE   3532  'to 3532'
             3492  LOAD_FAST                'mode'
             3494  LOAD_STR                 'Scanning'
             3496  COMPARE_OP               ==
         3498_3500  POP_JUMP_IF_TRUE   3532  'to 3532'
             3502  LOAD_FAST                'mode'
             3504  LOAD_STR                 'SCANNING'
             3506  COMPARE_OP               ==
         3508_3510  POP_JUMP_IF_TRUE   3532  'to 3532'
             3512  LOAD_FAST                'mode'
             3514  LOAD_STR                 'SCAN'
             3516  COMPARE_OP               ==
         3518_3520  POP_JUMP_IF_TRUE   3532  'to 3532'
             3522  LOAD_FAST                'mode'
             3524  LOAD_STR                 'scan'
             3526  COMPARE_OP               ==
         3528_3530  POP_JUMP_IF_FALSE  5692  'to 5692'
           3532_0  COME_FROM          3518  '3518'
           3532_1  COME_FROM          3508  '3508'
           3532_2  COME_FROM          3498  '3498'
           3532_3  COME_FROM          3488  '3488'

 L. 520      3532  LOAD_GLOBAL              input
             3534  LOAD_STR                 'Enter the starting time of the observation in the next format: 2010-12-31 00:00:00 (UTC time) \n'
             3536  CALL_FUNCTION_1       1  '1 positional argument'
             3538  BUILD_LIST_1          1 
             3540  STORE_FAST               'otime'

 L. 521      3542  LOAD_FAST                'Time'
             3544  LOAD_FAST                'otime'
             3546  LOAD_STR                 'iso'
             3548  LOAD_STR                 'utc'
             3550  LOAD_CONST               ('format', 'scale')
             3552  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             3554  STORE_FAST               'obs_time'

 L. 532      3556  LOAD_FAST                'solar_system_ephemeris'
             3558  LOAD_METHOD              set
             3560  LOAD_STR                 'builtin'
             3562  CALL_METHOD_1         1  '1 positional argument'
             3564  SETUP_WITH         3680  'to 3680'
             3566  POP_TOP          

 L. 533      3568  LOAD_FAST                'get_body'
             3570  LOAD_STR                 'sun'
             3572  LOAD_FAST                'obs_time'
             3574  LOAD_FAST                'VIL2'
             3576  CALL_FUNCTION_3       3  '3 positional arguments'
             3578  STORE_FAST               'sun'

 L. 534      3580  LOAD_FAST                'get_body'
             3582  LOAD_STR                 'moon'
             3584  LOAD_FAST                'obs_time'
             3586  LOAD_FAST                'VIL2'
             3588  CALL_FUNCTION_3       3  '3 positional arguments'
             3590  STORE_FAST               'moon'

 L. 535      3592  LOAD_FAST                'get_body'
             3594  LOAD_STR                 'mercury'
             3596  LOAD_FAST                'obs_time'
             3598  LOAD_FAST                'VIL2'
             3600  CALL_FUNCTION_3       3  '3 positional arguments'
             3602  STORE_FAST               'mercury'

 L. 536      3604  LOAD_FAST                'get_body'
             3606  LOAD_STR                 'venus'
             3608  LOAD_FAST                'obs_time'
             3610  LOAD_FAST                'VIL2'
             3612  CALL_FUNCTION_3       3  '3 positional arguments'
             3614  STORE_FAST               'venus'

 L. 537      3616  LOAD_FAST                'get_body'
             3618  LOAD_STR                 'mars'
             3620  LOAD_FAST                'obs_time'
             3622  LOAD_FAST                'VIL2'
             3624  CALL_FUNCTION_3       3  '3 positional arguments'
             3626  STORE_FAST               'mars'

 L. 538      3628  LOAD_FAST                'get_body'
             3630  LOAD_STR                 'jupiter'
             3632  LOAD_FAST                'obs_time'
             3634  LOAD_FAST                'VIL2'
             3636  CALL_FUNCTION_3       3  '3 positional arguments'
             3638  STORE_FAST               'jupiter'

 L. 539      3640  LOAD_FAST                'get_body'
             3642  LOAD_STR                 'saturn'
             3644  LOAD_FAST                'obs_time'
             3646  LOAD_FAST                'VIL2'
             3648  CALL_FUNCTION_3       3  '3 positional arguments'
             3650  STORE_FAST               'saturn'

 L. 540      3652  LOAD_FAST                'get_body'
             3654  LOAD_STR                 'uranus'
             3656  LOAD_FAST                'obs_time'
             3658  LOAD_FAST                'VIL2'
             3660  CALL_FUNCTION_3       3  '3 positional arguments'
             3662  STORE_FAST               'uranus'

 L. 541      3664  LOAD_FAST                'get_body'
             3666  LOAD_STR                 'neptune'
             3668  LOAD_FAST                'obs_time'
             3670  LOAD_FAST                'VIL2'
             3672  CALL_FUNCTION_3       3  '3 positional arguments'
             3674  STORE_FAST               'neptune'
             3676  POP_BLOCK        
             3678  LOAD_CONST               None
           3680_0  COME_FROM_WITH     3564  '3564'
             3680  WITH_CLEANUP_START
             3682  WITH_CLEANUP_FINISH
             3684  END_FINALLY      

 L. 547      3686  LOAD_GLOBAL              float
             3688  LOAD_GLOBAL              input
             3690  LOAD_STR                 'Enter manually the right ascension for the first observing point: '
             3692  CALL_FUNCTION_1       1  '1 positional argument'
             3694  CALL_FUNCTION_1       1  '1 positional argument'
             3696  STORE_FAST               'ra1'

 L. 548      3698  LOAD_GLOBAL              float
             3700  LOAD_GLOBAL              input
             3702  LOAD_STR                 'Enter manually the declination for the first observing point: '
             3704  CALL_FUNCTION_1       1  '1 positional argument'
             3706  CALL_FUNCTION_1       1  '1 positional argument'
             3708  STORE_FAST               'dec1'

 L. 549      3710  LOAD_GLOBAL              float
             3712  LOAD_GLOBAL              input
             3714  LOAD_STR                 'Enter manually the right ascension for the last observing point: '
             3716  CALL_FUNCTION_1       1  '1 positional argument'
             3718  CALL_FUNCTION_1       1  '1 positional argument'
             3720  STORE_FAST               'ra2'

 L. 550      3722  LOAD_GLOBAL              float
             3724  LOAD_GLOBAL              input
             3726  LOAD_STR                 'Enter manually the declination for the last observing point: '
             3728  CALL_FUNCTION_1       1  '1 positional argument'
             3730  CALL_FUNCTION_1       1  '1 positional argument'
             3732  STORE_FAST               'dec2'

 L. 553      3734  LOAD_CONST               0.308
             3736  STORE_FAST               'dra'

 L. 554      3738  LOAD_CONST               0.308
             3740  STORE_FAST               'ddec'

 L. 556      3742  LOAD_FAST                'ra1'
             3744  LOAD_FAST                'ra2'
             3746  COMPARE_OP               >=
         3748_3750  POP_JUMP_IF_FALSE  3770  'to 3770'

 L. 557      3752  LOAD_FAST                'ra1'
             3754  LOAD_FAST                'dra'
             3756  BINARY_ADD       
             3758  STORE_FAST               'ra1'

 L. 558      3760  LOAD_FAST                'ra2'
             3762  LOAD_FAST                'dra'
             3764  BINARY_SUBTRACT  
             3766  STORE_FAST               'ra2'
             3768  JUMP_FORWARD       3786  'to 3786'
           3770_0  COME_FROM          3748  '3748'

 L. 560      3770  LOAD_FAST                'ra1'
             3772  LOAD_FAST                'dra'
             3774  BINARY_SUBTRACT  
             3776  STORE_FAST               'ra1'

 L. 561      3778  LOAD_FAST                'ra2'
             3780  LOAD_FAST                'dra'
             3782  BINARY_ADD       
             3784  STORE_FAST               'ra2'
           3786_0  COME_FROM          3768  '3768'

 L. 563      3786  LOAD_FAST                'dec1'
             3788  LOAD_FAST                'dec2'
             3790  COMPARE_OP               >=
         3792_3794  POP_JUMP_IF_FALSE  3814  'to 3814'

 L. 564      3796  LOAD_FAST                'dec1'
             3798  LOAD_FAST                'ddec'
             3800  BINARY_ADD       
             3802  STORE_FAST               'dec1'

 L. 565      3804  LOAD_FAST                'dec2'
             3806  LOAD_FAST                'ddec'
             3808  BINARY_SUBTRACT  
             3810  STORE_FAST               'dec2'
             3812  JUMP_FORWARD       3830  'to 3830'
           3814_0  COME_FROM          3792  '3792'

 L. 567      3814  LOAD_FAST                'dec1'
             3816  LOAD_FAST                'ddec'
             3818  BINARY_SUBTRACT  
             3820  STORE_FAST               'dec1'

 L. 568      3822  LOAD_FAST                'dec2'
             3824  LOAD_FAST                'ddec'
             3826  BINARY_ADD       
             3828  STORE_FAST               'dec2'
           3830_0  COME_FROM          3812  '3812'

 L. 570      3830  LOAD_GLOBAL              abs
             3832  LOAD_FAST                'ra2'
             3834  LOAD_FAST                'ra1'
             3836  BINARY_SUBTRACT  
             3838  CALL_FUNCTION_1       1  '1 positional argument'
             3840  STORE_FAST               'deltara'

 L. 572      3842  LOAD_GLOBAL              int
             3844  LOAD_FAST                'np'
             3846  LOAD_ATTR                around
             3848  LOAD_FAST                'deltara'
             3850  LOAD_FAST                'dra'
             3852  BINARY_TRUE_DIVIDE
             3854  LOAD_CONST               1
             3856  BINARY_ADD       
             3858  LOAD_CONST               0
             3860  LOAD_CONST               ('decimals',)
             3862  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3864  CALL_FUNCTION_1       1  '1 positional argument'
             3866  STORE_FAST               'nra'

 L. 574      3868  LOAD_GLOBAL              abs
             3870  LOAD_FAST                'dec2'
             3872  LOAD_FAST                'dec1'
             3874  BINARY_SUBTRACT  
             3876  CALL_FUNCTION_1       1  '1 positional argument'
             3878  STORE_FAST               'deltadec'

 L. 575      3880  LOAD_GLOBAL              int
             3882  LOAD_FAST                'np'
             3884  LOAD_ATTR                around
             3886  LOAD_FAST                'deltadec'
             3888  LOAD_FAST                'ddec'
             3890  BINARY_TRUE_DIVIDE
             3892  LOAD_CONST               1
             3894  BINARY_ADD       
             3896  LOAD_CONST               0
             3898  LOAD_CONST               ('decimals',)
             3900  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3902  CALL_FUNCTION_1       1  '1 positional argument'
             3904  STORE_FAST               'ndec'

 L. 579      3906  LOAD_FAST                'sun'
             3908  LOAD_ATTR                ra
             3910  LOAD_ATTR                degree
             3912  LOAD_CONST               0
             3914  BINARY_SUBSCR    
             3916  STORE_FAST               'ra_sun'

 L. 580      3918  LOAD_FAST                'sun'
             3920  LOAD_ATTR                dec
             3922  LOAD_ATTR                degree
             3924  LOAD_CONST               0
             3926  BINARY_SUBSCR    
             3928  STORE_FAST               'dec_sun'

 L. 581      3930  LOAD_FAST                'SkyCoord'
             3932  LOAD_FAST                'Angle'
             3934  LOAD_FAST                'ra_sun'
             3936  LOAD_FAST                'u'
             3938  LOAD_ATTR                deg
             3940  LOAD_CONST               ('unit',)
             3942  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3944  LOAD_FAST                'Angle'
             3946  LOAD_FAST                'dec_sun'
             3948  LOAD_FAST                'u'
             3950  LOAD_ATTR                deg
             3952  LOAD_CONST               ('unit',)
             3954  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3956  LOAD_STR                 'icrs'
             3958  LOAD_CONST               ('frame',)
             3960  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             3962  STORE_FAST               'suncoords'

 L. 584      3964  LOAD_GLOBAL              abs
             3966  LOAD_FAST                'ra_sun'
             3968  LOAD_FAST                'ra1'
             3970  BINARY_SUBTRACT  
             3972  CALL_FUNCTION_1       1  '1 positional argument'
             3974  STORE_FAST               'ra_dif'

 L. 585      3976  LOAD_GLOBAL              abs
             3978  LOAD_FAST                'dec_sun'
             3980  LOAD_FAST                'dec1'
             3982  BINARY_SUBTRACT  
             3984  CALL_FUNCTION_1       1  '1 positional argument'
             3986  STORE_FAST               'dec_dif'

 L. 586      3988  LOAD_FAST                'ra_dif'
             3990  LOAD_CONST               1.5
             3992  COMPARE_OP               <
         3994_3996  POP_JUMP_IF_FALSE  4016  'to 4016'

 L. 587      3998  LOAD_FAST                'dec_dif'
             4000  LOAD_CONST               1.5
             4002  COMPARE_OP               <
         4004_4006  POP_JUMP_IF_FALSE  4016  'to 4016'

 L. 588      4008  LOAD_GLOBAL              print
             4010  LOAD_STR                 'WARNING: YOU FLEW TOO CLOSE TO THE SUN!!!!!!!!!!!!!!!!!!!!'
             4012  CALL_FUNCTION_1       1  '1 positional argument'
             4014  POP_TOP          
           4016_0  COME_FROM          4004  '4004'
           4016_1  COME_FROM          3994  '3994'

 L. 590      4016  LOAD_FAST                'np'
             4018  LOAD_METHOD              linspace
             4020  LOAD_CONST               0
             4022  LOAD_FAST                'nra'
             4024  LOAD_CONST               1
             4026  BINARY_SUBTRACT  
             4028  LOAD_FAST                'nra'
             4030  CALL_METHOD_3         3  '3 positional arguments'
             4032  STORE_FAST               'nnra'

 L. 591      4034  LOAD_FAST                'np'
             4036  LOAD_METHOD              linspace
             4038  LOAD_CONST               0
             4040  LOAD_FAST                'ndec'
             4042  LOAD_CONST               1
             4044  BINARY_SUBTRACT  
             4046  LOAD_FAST                'ndec'
             4048  CALL_METHOD_3         3  '3 positional arguments'
             4050  STORE_FAST               'nndec'

 L. 593      4052  BUILD_LIST_0          0 
             4054  STORE_FAST               'ra'

 L. 594      4056  BUILD_LIST_0          0 
             4058  STORE_FAST               'dec'

 L. 595      4060  SETUP_LOOP         4094  'to 4094'
             4062  LOAD_FAST                'nnra'
             4064  GET_ITER         
             4066  FOR_ITER           4092  'to 4092'
             4068  STORE_FAST               'i'

 L. 596      4070  LOAD_FAST                'ra'
             4072  LOAD_METHOD              append
             4074  LOAD_FAST                'ra1'
             4076  LOAD_FAST                'dra'
             4078  LOAD_FAST                'i'
             4080  BINARY_MULTIPLY  
             4082  BINARY_ADD       
             4084  CALL_METHOD_1         1  '1 positional argument'
             4086  POP_TOP          
         4088_4090  JUMP_BACK          4066  'to 4066'
             4092  POP_BLOCK        
           4094_0  COME_FROM_LOOP     4060  '4060'

 L. 597      4094  SETUP_LOOP         4128  'to 4128'
             4096  LOAD_FAST                'nndec'
             4098  GET_ITER         
             4100  FOR_ITER           4126  'to 4126'
             4102  STORE_FAST               'i'

 L. 598      4104  LOAD_FAST                'dec'
             4106  LOAD_METHOD              append
             4108  LOAD_FAST                'dec1'
             4110  LOAD_FAST                'ddec'
             4112  LOAD_FAST                'i'
             4114  BINARY_MULTIPLY  
             4116  BINARY_ADD       
             4118  CALL_METHOD_1         1  '1 positional argument'
             4120  POP_TOP          
         4122_4124  JUMP_BACK          4100  'to 4100'
             4126  POP_BLOCK        
           4128_0  COME_FROM_LOOP     4094  '4094'

 L. 600      4128  LOAD_FAST                'dec'
             4130  LOAD_CONST               None
             4132  LOAD_CONST               None
             4134  LOAD_CONST               -1
             4136  BUILD_SLICE_3         3 
             4138  BINARY_SUBSCR    
             4140  STORE_FAST               'decr'

 L. 602      4142  LOAD_FAST                'np'
             4144  LOAD_ATTR                zeros
             4146  LOAD_FAST                'nra'
             4148  LOAD_FAST                'ndec'
             4150  BUILD_TUPLE_2         2 
             4152  LOAD_GLOBAL              object
             4154  LOAD_CONST               ('dtype',)
             4156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4158  STORE_FAST               'ccc'

 L. 603      4160  SETUP_LOOP         4320  'to 4320'
             4162  LOAD_FAST                'nnra'
             4164  LOAD_METHOD              astype
             4166  LOAD_GLOBAL              int
             4168  CALL_METHOD_1         1  '1 positional argument'
             4170  GET_ITER         
             4172  FOR_ITER           4318  'to 4318'
             4174  STORE_FAST               'i'

 L. 604      4176  SETUP_LOOP         4314  'to 4314'
             4178  LOAD_FAST                'nndec'
             4180  LOAD_METHOD              astype
             4182  LOAD_GLOBAL              int
             4184  CALL_METHOD_1         1  '1 positional argument'
             4186  GET_ITER         
             4188  FOR_ITER           4312  'to 4312'
             4190  STORE_FAST               'j'

 L. 605      4192  LOAD_FAST                'i'
             4194  LOAD_CONST               2
             4196  BINARY_MODULO    
             4198  LOAD_CONST               0
             4200  COMPARE_OP               ==
         4202_4204  POP_JUMP_IF_FALSE  4258  'to 4258'

 L. 606      4206  LOAD_FAST                'SkyCoord'
             4208  LOAD_FAST                'Angle'
             4210  LOAD_FAST                'ra'
             4212  LOAD_FAST                'i'
             4214  BINARY_SUBSCR    
             4216  LOAD_FAST                'u'
             4218  LOAD_ATTR                deg
             4220  LOAD_CONST               ('unit',)
             4222  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4224  LOAD_FAST                'Angle'
             4226  LOAD_FAST                'dec'
             4228  LOAD_FAST                'j'
             4230  BINARY_SUBSCR    
             4232  LOAD_FAST                'u'
             4234  LOAD_ATTR                deg
             4236  LOAD_CONST               ('unit',)
             4238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4240  LOAD_STR                 'icrs'
             4242  LOAD_CONST               ('frame',)
             4244  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4246  LOAD_FAST                'ccc'
             4248  LOAD_FAST                'i'
             4250  BINARY_SUBSCR    
             4252  LOAD_FAST                'j'
             4254  STORE_SUBSCR     
             4256  JUMP_BACK          4188  'to 4188'
           4258_0  COME_FROM          4202  '4202'

 L. 608      4258  LOAD_FAST                'SkyCoord'
             4260  LOAD_FAST                'Angle'
             4262  LOAD_FAST                'ra'
             4264  LOAD_FAST                'i'
             4266  BINARY_SUBSCR    
             4268  LOAD_FAST                'u'
             4270  LOAD_ATTR                deg
             4272  LOAD_CONST               ('unit',)
             4274  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4276  LOAD_FAST                'Angle'
             4278  LOAD_FAST                'decr'
             4280  LOAD_FAST                'j'
             4282  BINARY_SUBSCR    
             4284  LOAD_FAST                'u'
             4286  LOAD_ATTR                deg
             4288  LOAD_CONST               ('unit',)
             4290  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4292  LOAD_STR                 'icrs'
             4294  LOAD_CONST               ('frame',)
             4296  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4298  LOAD_FAST                'ccc'
             4300  LOAD_FAST                'i'
             4302  BINARY_SUBSCR    
             4304  LOAD_FAST                'j'
             4306  STORE_SUBSCR     
         4308_4310  JUMP_BACK          4188  'to 4188'
             4312  POP_BLOCK        
           4314_0  COME_FROM_LOOP     4176  '4176'
         4314_4316  JUMP_BACK          4172  'to 4172'
             4318  POP_BLOCK        
           4320_0  COME_FROM_LOOP     4160  '4160'

 L. 612      4320  LOAD_CONST               2
             4322  STORE_FAST               'dt'

 L. 613      4324  LOAD_FAST                'TimeDelta'
             4326  LOAD_FAST                'dt'
             4328  LOAD_STR                 'sec'
             4330  LOAD_CONST               ('format',)
             4332  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4334  STORE_FAST               'dt2'

 L. 614      4336  LOAD_FAST                'nra'
             4338  LOAD_FAST                'ndec'
             4340  BINARY_MULTIPLY  
             4342  STORE_FAST               'pointings'

 L. 616      4344  LOAD_FAST                'TimeDelta'
             4346  LOAD_CONST               300
             4348  LOAD_STR                 'sec'
             4350  LOAD_CONST               ('format',)
             4352  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4354  STORE_FAST               'pre'

 L. 618      4356  LOAD_FAST                'obs_time'
             4358  LOAD_CONST               0
             4360  BINARY_SUBSCR    
             4362  LOAD_FAST                'pre'
             4364  BINARY_SUBTRACT  
             4366  STORE_FAST               't0'

 L. 620      4368  LOAD_FAST                'np'
             4370  LOAD_METHOD              linspace
             4372  LOAD_CONST               0.0
             4374  LOAD_FAST                'pointings'
             4376  LOAD_FAST                'pointings'
             4378  LOAD_CONST               1
             4380  BINARY_ADD       
             4382  CALL_METHOD_3         3  '3 positional arguments'
             4384  STORE_FAST               'suc'

 L. 621      4386  LOAD_GLOBAL              list
             4388  CALL_FUNCTION_0       0  '0 positional arguments'
             4390  STORE_FAST               't'

 L. 622      4392  LOAD_FAST                't'
             4394  LOAD_METHOD              append
             4396  LOAD_FAST                't0'
             4398  CALL_METHOD_1         1  '1 positional argument'
             4400  POP_TOP          

 L. 623      4402  LOAD_FAST                't'
             4404  LOAD_METHOD              append
             4406  LOAD_FAST                'obs_time'
             4408  LOAD_CONST               0
             4410  BINARY_SUBSCR    
             4412  CALL_METHOD_1         1  '1 positional argument'
             4414  POP_TOP          

 L. 624      4416  LOAD_FAST                'np'
             4418  LOAD_METHOD              sqrt
             4420  LOAD_FAST                'deltara'
             4422  LOAD_CONST               3
             4424  BINARY_TRUE_DIVIDE
             4426  LOAD_CONST               2
             4428  BINARY_POWER     
             4430  LOAD_FAST                'deltadec'
             4432  LOAD_CONST               3
             4434  BINARY_TRUE_DIVIDE
             4436  LOAD_CONST               2
             4438  BINARY_POWER     
             4440  BINARY_ADD       
             4442  CALL_METHOD_1         1  '1 positional argument'
             4444  STORE_FAST               'dt3'

 L. 625      4446  LOAD_FAST                'TimeDelta'
             4448  LOAD_FAST                'dt3'
             4450  LOAD_STR                 'sec'
             4452  LOAD_CONST               ('format',)
             4454  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4456  STORE_FAST               'dt3'

 L. 627      4458  SETUP_LOOP         4556  'to 4556'
             4460  LOAD_GLOBAL              enumerate
             4462  LOAD_FAST                'suc'
             4464  CALL_FUNCTION_1       1  '1 positional argument'
             4466  GET_ITER         
           4468_0  COME_FROM          4482  '4482'
             4468  FOR_ITER           4554  'to 4554'
             4470  UNPACK_SEQUENCE_2     2 
             4472  STORE_FAST               'i'
             4474  STORE_FAST               'tex'

 L. 628      4476  LOAD_FAST                'i'
             4478  LOAD_CONST               1
             4480  COMPARE_OP               >
         4482_4484  POP_JUMP_IF_FALSE  4468  'to 4468'

 L. 629      4486  LOAD_FAST                'i'
             4488  LOAD_CONST               1
             4490  BINARY_SUBTRACT  
             4492  LOAD_FAST                'nra'
             4494  BINARY_MODULO    
             4496  LOAD_CONST               0
             4498  COMPARE_OP               !=
         4500_4502  POP_JUMP_IF_FALSE  4528  'to 4528'

 L. 630      4504  LOAD_FAST                't'
             4506  LOAD_METHOD              append
             4508  LOAD_FAST                't'
             4510  LOAD_FAST                'i'
             4512  LOAD_CONST               1
             4514  BINARY_SUBTRACT  
             4516  BINARY_SUBSCR    
             4518  LOAD_FAST                'dt2'
             4520  BINARY_ADD       
             4522  CALL_METHOD_1         1  '1 positional argument'
             4524  POP_TOP          
             4526  JUMP_BACK          4468  'to 4468'
           4528_0  COME_FROM          4500  '4500'

 L. 632      4528  LOAD_FAST                't'
             4530  LOAD_METHOD              append
             4532  LOAD_FAST                't'
             4534  LOAD_FAST                'i'
             4536  LOAD_CONST               1
             4538  BINARY_SUBTRACT  
             4540  BINARY_SUBSCR    
             4542  LOAD_FAST                'dt3'
             4544  BINARY_ADD       
             4546  CALL_METHOD_1         1  '1 positional argument'
             4548  POP_TOP          
         4550_4552  JUMP_BACK          4468  'to 4468'
             4554  POP_BLOCK        
           4556_0  COME_FROM_LOOP     4458  '4458'

 L. 635      4556  BUILD_LIST_0          0 
             4558  STORE_FAST               'completecoords'

 L. 636      4560  BUILD_LIST_0          0 
             4562  STORE_FAST               'time'

 L. 637      4564  LOAD_FAST                'ccc'
             4566  LOAD_METHOD              flatten
             4568  CALL_METHOD_0         0  '0 positional arguments'
             4570  STORE_FAST               'ccc_f'

 L. 638      4572  LOAD_FAST                'np'
             4574  LOAD_ATTR                zeros
             4576  LOAD_FAST                'np'
             4578  LOAD_METHOD              shape
             4580  LOAD_FAST                'ccc_f'
             4582  CALL_METHOD_1         1  '1 positional argument'
             4584  LOAD_GLOBAL              object
             4586  LOAD_CONST               ('dtype',)
             4588  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4590  STORE_FAST               'ccc_n'

 L. 640      4592  SETUP_LOOP         4696  'to 4696'
             4594  LOAD_GLOBAL              enumerate
             4596  LOAD_FAST                'ccc_f'
             4598  CALL_FUNCTION_1       1  '1 positional argument'
             4600  GET_ITER         
             4602  FOR_ITER           4694  'to 4694'
             4604  UNPACK_SEQUENCE_2     2 
             4606  STORE_FAST               'i'
             4608  STORE_FAST               'tex'

 L. 641      4610  LOAD_FAST                'ccc_f'
             4612  LOAD_FAST                'i'
             4614  BINARY_SUBSCR    
             4616  LOAD_METHOD              transform_to
             4618  LOAD_FAST                'AltAz'
             4620  LOAD_FAST                't'
             4622  LOAD_FAST                'i'
             4624  BINARY_SUBSCR    
             4626  LOAD_FAST                'VIL2'
             4628  LOAD_CONST               ('obstime', 'location')
             4630  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4632  CALL_METHOD_1         1  '1 positional argument'
             4634  LOAD_FAST                'ccc_n'
             4636  LOAD_FAST                'i'
             4638  STORE_SUBSCR     

 L. 643      4640  LOAD_FAST                't'
             4642  LOAD_FAST                'i'
             4644  BINARY_SUBSCR    
             4646  LOAD_ATTR                isot
             4648  LOAD_FAST                'ccc_n'
             4650  LOAD_FAST                'i'
             4652  BINARY_SUBSCR    
             4654  LOAD_ATTR                alt
             4656  LOAD_ATTR                degree
             4658  LOAD_FAST                'ccc_n'
             4660  LOAD_FAST                'i'
             4662  BINARY_SUBSCR    
             4664  LOAD_ATTR                az
             4666  LOAD_ATTR                degree
             4668  BUILD_TUPLE_3         3 
             4670  STORE_FAST               'cco'

 L. 644      4672  LOAD_GLOBAL              list
             4674  LOAD_FAST                'cco'
             4676  CALL_FUNCTION_1       1  '1 positional argument'
             4678  STORE_FAST               'ccl'

 L. 645      4680  LOAD_FAST                'completecoords'
             4682  LOAD_METHOD              append
             4684  LOAD_FAST                'ccl'
             4686  CALL_METHOD_1         1  '1 positional argument'
             4688  POP_TOP          
         4690_4692  JUMP_BACK          4602  'to 4602'
             4694  POP_BLOCK        
           4696_0  COME_FROM_LOOP     4592  '4592'

 L. 647      4696  LOAD_FAST                'completecoords'
             4698  LOAD_CONST               1
             4700  BINARY_SUBSCR    
             4702  LOAD_CONST               1
             4704  BINARY_SUBSCR    
             4706  LOAD_FAST                'completecoords'
             4708  LOAD_CONST               0
             4710  BINARY_SUBSCR    
             4712  LOAD_CONST               1
             4714  STORE_SUBSCR     

 L. 648      4716  LOAD_FAST                'completecoords'
             4718  LOAD_CONST               1
             4720  BINARY_SUBSCR    
             4722  LOAD_CONST               2
             4724  BINARY_SUBSCR    
             4726  LOAD_FAST                'completecoords'
             4728  LOAD_CONST               0
             4730  BINARY_SUBSCR    
             4732  LOAD_CONST               2
             4734  STORE_SUBSCR     

 L. 650      4736  LOAD_FAST                'plt'
             4738  LOAD_ATTR                subplots
             4740  LOAD_CONST               2
             4742  LOAD_CONST               1
             4744  LOAD_CONST               (18, 18)
             4746  LOAD_CONST               ('figsize',)
             4748  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4750  UNPACK_SEQUENCE_2     2 
             4752  STORE_FAST               'figure'
             4754  UNPACK_SEQUENCE_2     2 
             4756  STORE_FAST               'ax'
             4758  STORE_FAST               'ay'

 L. 653      4760  LOAD_FAST                'pointings'
             4762  LOAD_CONST               500
             4764  COMPARE_OP               >
         4766_4768  POP_JUMP_IF_FALSE  4982  'to 4982'

 L. 654      4770  SETUP_LOOP         4980  'to 4980'
             4772  LOAD_GLOBAL              enumerate
             4774  LOAD_FAST                'ccc_f'
             4776  CALL_FUNCTION_1       1  '1 positional argument'
             4778  GET_ITER         
           4780_0  COME_FROM          4798  '4798'
             4780  FOR_ITER           4978  'to 4978'
             4782  UNPACK_SEQUENCE_2     2 
             4784  STORE_FAST               'i'
             4786  STORE_FAST               'tex'

 L. 655      4788  LOAD_FAST                'i'
             4790  LOAD_CONST               100
             4792  BINARY_MODULO    
             4794  LOAD_CONST               0
             4796  COMPARE_OP               ==
         4798_4800  POP_JUMP_IF_FALSE  4780  'to 4780'

 L. 656      4802  LOAD_FAST                'ax'
             4804  LOAD_METHOD              annotate
             4806  LOAD_FAST                'i'
             4808  LOAD_FAST                'ccc_f'
             4810  LOAD_FAST                'i'
             4812  BINARY_SUBSCR    
             4814  LOAD_ATTR                ra
             4816  LOAD_ATTR                deg
             4818  LOAD_FAST                'ccc_f'
             4820  LOAD_FAST                'i'
             4822  BINARY_SUBSCR    
             4824  LOAD_ATTR                dec
             4826  LOAD_ATTR                deg
             4828  BUILD_TUPLE_2         2 
             4830  CALL_METHOD_2         2  '2 positional arguments'
             4832  POP_TOP          

 L. 657      4834  LOAD_FAST                'ax'
             4836  LOAD_METHOD              set_xlabel
             4838  LOAD_STR                 'Right Ascension (deg)'
             4840  CALL_METHOD_1         1  '1 positional argument'
             4842  POP_TOP          

 L. 658      4844  LOAD_FAST                'ax'
             4846  LOAD_METHOD              set_ylabel
             4848  LOAD_STR                 'Declination (deg)'
             4850  CALL_METHOD_1         1  '1 positional argument'
             4852  POP_TOP          

 L. 659      4854  LOAD_FAST                'ax'
             4856  LOAD_ATTR                scatter
             4858  LOAD_FAST                'ccc_f'
             4860  LOAD_FAST                'i'
             4862  BINARY_SUBSCR    
             4864  LOAD_ATTR                ra
             4866  LOAD_ATTR                deg
             4868  LOAD_FAST                'ccc_f'
             4870  LOAD_FAST                'i'
             4872  BINARY_SUBSCR    
             4874  LOAD_ATTR                dec
             4876  LOAD_ATTR                deg
             4878  LOAD_CONST               12000
             4880  LOAD_CONST               0.35
             4882  LOAD_CONST               ('s', 'alpha')
             4884  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             4886  POP_TOP          

 L. 660      4888  LOAD_FAST                'ay'
             4890  LOAD_METHOD              annotate
             4892  LOAD_FAST                'i'
             4894  LOAD_FAST                'ccc_n'
             4896  LOAD_FAST                'i'
             4898  BINARY_SUBSCR    
             4900  LOAD_ATTR                az
             4902  LOAD_ATTR                deg
             4904  LOAD_FAST                'ccc_n'
             4906  LOAD_FAST                'i'
             4908  BINARY_SUBSCR    
             4910  LOAD_ATTR                alt
             4912  LOAD_ATTR                deg
             4914  BUILD_TUPLE_2         2 
             4916  CALL_METHOD_2         2  '2 positional arguments'
             4918  POP_TOP          

 L. 661      4920  LOAD_FAST                'ay'
             4922  LOAD_METHOD              set_xlabel
             4924  LOAD_STR                 'Azimuth (deg)'
             4926  CALL_METHOD_1         1  '1 positional argument'
             4928  POP_TOP          

 L. 662      4930  LOAD_FAST                'ay'
             4932  LOAD_METHOD              set_ylabel
             4934  LOAD_STR                 'Elevation (deg)'
             4936  CALL_METHOD_1         1  '1 positional argument'
             4938  POP_TOP          

 L. 663      4940  LOAD_FAST                'ay'
             4942  LOAD_ATTR                scatter
             4944  LOAD_FAST                'ccc_n'
             4946  LOAD_FAST                'i'
             4948  BINARY_SUBSCR    
             4950  LOAD_ATTR                az
             4952  LOAD_ATTR                deg
             4954  LOAD_FAST                'ccc_n'
             4956  LOAD_FAST                'i'
             4958  BINARY_SUBSCR    
             4960  LOAD_ATTR                alt
             4962  LOAD_ATTR                deg
             4964  LOAD_CONST               12000
             4966  LOAD_CONST               0.35
             4968  LOAD_CONST               ('s', 'alpha')
             4970  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             4972  POP_TOP          
         4974_4976  JUMP_BACK          4780  'to 4780'
             4978  POP_BLOCK        
           4980_0  COME_FROM_LOOP     4770  '4770'
             4980  JUMP_FORWARD       5178  'to 5178'
           4982_0  COME_FROM          4766  '4766'

 L. 665      4982  SETUP_LOOP         5178  'to 5178'
             4984  LOAD_GLOBAL              enumerate
             4986  LOAD_FAST                'ccc_f'
             4988  CALL_FUNCTION_1       1  '1 positional argument'
             4990  GET_ITER         
             4992  FOR_ITER           5176  'to 5176'
             4994  UNPACK_SEQUENCE_2     2 
             4996  STORE_FAST               'i'
             4998  STORE_FAST               'tex'

 L. 666      5000  LOAD_FAST                'ax'
             5002  LOAD_METHOD              annotate
             5004  LOAD_FAST                'i'
             5006  LOAD_FAST                'ccc_f'
             5008  LOAD_FAST                'i'
             5010  BINARY_SUBSCR    
             5012  LOAD_ATTR                ra
             5014  LOAD_ATTR                deg
             5016  LOAD_FAST                'ccc_f'
             5018  LOAD_FAST                'i'
             5020  BINARY_SUBSCR    
             5022  LOAD_ATTR                dec
             5024  LOAD_ATTR                deg
             5026  BUILD_TUPLE_2         2 
             5028  CALL_METHOD_2         2  '2 positional arguments'
             5030  POP_TOP          

 L. 667      5032  LOAD_FAST                'ax'
             5034  LOAD_METHOD              set_xlabel
             5036  LOAD_STR                 'Right Ascension (deg)'
             5038  CALL_METHOD_1         1  '1 positional argument'
             5040  POP_TOP          

 L. 668      5042  LOAD_FAST                'ax'
             5044  LOAD_METHOD              set_ylabel
             5046  LOAD_STR                 'Declination (deg)'
             5048  CALL_METHOD_1         1  '1 positional argument'
             5050  POP_TOP          

 L. 669      5052  LOAD_FAST                'ax'
             5054  LOAD_ATTR                scatter
             5056  LOAD_FAST                'ccc_f'
             5058  LOAD_FAST                'i'
             5060  BINARY_SUBSCR    
             5062  LOAD_ATTR                ra
             5064  LOAD_ATTR                deg
             5066  LOAD_FAST                'ccc_f'
             5068  LOAD_FAST                'i'
             5070  BINARY_SUBSCR    
             5072  LOAD_ATTR                dec
             5074  LOAD_ATTR                deg
             5076  LOAD_CONST               12000
             5078  LOAD_CONST               0.35
             5080  LOAD_CONST               ('s', 'alpha')
             5082  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5084  POP_TOP          

 L. 670      5086  LOAD_FAST                'ay'
             5088  LOAD_METHOD              annotate
             5090  LOAD_FAST                'i'
             5092  LOAD_FAST                'ccc_n'
             5094  LOAD_FAST                'i'
             5096  BINARY_SUBSCR    
             5098  LOAD_ATTR                az
             5100  LOAD_ATTR                deg
             5102  LOAD_FAST                'ccc_n'
             5104  LOAD_FAST                'i'
             5106  BINARY_SUBSCR    
             5108  LOAD_ATTR                alt
             5110  LOAD_ATTR                deg
             5112  BUILD_TUPLE_2         2 
             5114  CALL_METHOD_2         2  '2 positional arguments'
             5116  POP_TOP          

 L. 671      5118  LOAD_FAST                'ay'
             5120  LOAD_METHOD              set_xlabel
             5122  LOAD_STR                 'Azimuth (deg)'
             5124  CALL_METHOD_1         1  '1 positional argument'
             5126  POP_TOP          

 L. 672      5128  LOAD_FAST                'ay'
             5130  LOAD_METHOD              set_ylabel
             5132  LOAD_STR                 'Elevation (deg)'
             5134  CALL_METHOD_1         1  '1 positional argument'
             5136  POP_TOP          

 L. 673      5138  LOAD_FAST                'ay'
             5140  LOAD_ATTR                scatter
             5142  LOAD_FAST                'ccc_n'
             5144  LOAD_FAST                'i'
             5146  BINARY_SUBSCR    
             5148  LOAD_ATTR                az
             5150  LOAD_ATTR                deg
             5152  LOAD_FAST                'ccc_n'
             5154  LOAD_FAST                'i'
             5156  BINARY_SUBSCR    
             5158  LOAD_ATTR                alt
             5160  LOAD_ATTR                deg
             5162  LOAD_CONST               12000
             5164  LOAD_CONST               0.35
             5166  LOAD_CONST               ('s', 'alpha')
             5168  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5170  POP_TOP          
         5172_5174  JUMP_BACK          4992  'to 4992'
             5176  POP_BLOCK        
           5178_0  COME_FROM_LOOP     4982  '4982'
           5178_1  COME_FROM          4980  '4980'

 L. 678      5178  SETUP_LOOP         5240  'to 5240'
             5180  LOAD_GLOBAL              enumerate
             5182  LOAD_FAST                'ccc_f'
             5184  CALL_FUNCTION_1       1  '1 positional argument'
             5186  GET_ITER         
           5188_0  COME_FROM          5210  '5210'
             5188  FOR_ITER           5238  'to 5238'
             5190  UNPACK_SEQUENCE_2     2 
             5192  STORE_FAST               'i'
             5194  STORE_FAST               'tex'

 L. 679      5196  LOAD_FAST                'completecoords'
             5198  LOAD_FAST                'i'
             5200  BINARY_SUBSCR    
             5202  LOAD_CONST               1
             5204  BINARY_SUBSCR    
             5206  LOAD_CONST               10
             5208  COMPARE_OP               <
         5210_5212  POP_JUMP_IF_FALSE  5188  'to 5188'

 L. 680      5214  LOAD_FAST                'np'
             5216  LOAD_ATTR                ma
             5218  LOAD_ATTR                masked
             5220  LOAD_FAST                'completecoords'
             5222  LOAD_FAST                'i'
             5224  STORE_SUBSCR     

 L. 681      5226  LOAD_GLOBAL              print
             5228  LOAD_STR                 'Too low scanning position'
             5230  CALL_FUNCTION_1       1  '1 positional argument'
             5232  POP_TOP          
         5234_5236  JUMP_BACK          5188  'to 5188'
             5238  POP_BLOCK        
           5240_0  COME_FROM_LOOP     5178  '5178'

 L. 686      5240  BUILD_LIST_0          0 
             5242  STORE_FAST               'r'

 L. 687      5244  BUILD_LIST_0          0 
             5246  STORE_FAST               'elev'

 L. 688      5248  BUILD_LIST_0          0 
             5250  STORE_FAST               'azi'

 L. 689      5252  LOAD_CONST               1.00031
             5254  STORE_FAST               'n0'

 L. 690      5256  SETUP_LOOP         5390  'to 5390'
             5258  LOAD_GLOBAL              enumerate
             5260  LOAD_FAST                'ccc_f'
             5262  CALL_FUNCTION_1       1  '1 positional argument'
             5264  GET_ITER         
             5266  FOR_ITER           5388  'to 5388'
             5268  UNPACK_SEQUENCE_2     2 
             5270  STORE_FAST               'i'
             5272  STORE_FAST               'tex'

 L. 692      5274  LOAD_FAST                'np'
             5276  LOAD_METHOD              deg2rad
             5278  LOAD_FAST                'ccc_n'
             5280  LOAD_FAST                'i'
             5282  BINARY_SUBSCR    
             5284  LOAD_ATTR                alt
             5286  LOAD_ATTR                deg
             5288  LOAD_CONST               4.7
             5290  LOAD_CONST               2.24
             5292  LOAD_FAST                'ccc_n'
             5294  LOAD_FAST                'i'
             5296  BINARY_SUBSCR    
             5298  LOAD_ATTR                alt
             5300  LOAD_ATTR                deg
             5302  BINARY_ADD       
             5304  BINARY_TRUE_DIVIDE
             5306  BINARY_ADD       
             5308  CALL_METHOD_1         1  '1 positional argument'
             5310  STORE_FAST               'p'

 L. 693      5312  LOAD_FAST                'r'
             5314  LOAD_METHOD              append
             5316  LOAD_FAST                'n0'
             5318  LOAD_CONST               1
             5320  BINARY_SUBTRACT  
             5322  LOAD_CONST               1
             5324  BINARY_MULTIPLY  
             5326  LOAD_FAST                'np'
             5328  LOAD_METHOD              tan
             5330  LOAD_FAST                'p'
             5332  CALL_METHOD_1         1  '1 positional argument'
             5334  BINARY_TRUE_DIVIDE
             5336  CALL_METHOD_1         1  '1 positional argument'
             5338  POP_TOP          

 L. 694      5340  LOAD_FAST                'elev'
             5342  LOAD_METHOD              append
             5344  LOAD_FAST                'ccc_n'
             5346  LOAD_FAST                'i'
             5348  BINARY_SUBSCR    
             5350  LOAD_ATTR                alt
             5352  LOAD_ATTR                deg
             5354  LOAD_FAST                'r'
             5356  LOAD_FAST                'i'
             5358  BINARY_SUBSCR    
             5360  BINARY_ADD       
             5362  CALL_METHOD_1         1  '1 positional argument'
             5364  POP_TOP          

 L. 695      5366  LOAD_FAST                'azi'
             5368  LOAD_METHOD              append
             5370  LOAD_FAST                'ccc_n'
             5372  LOAD_FAST                'i'
             5374  BINARY_SUBSCR    
             5376  LOAD_ATTR                az
             5378  LOAD_ATTR                deg
             5380  CALL_METHOD_1         1  '1 positional argument'
             5382  POP_TOP          
         5384_5386  JUMP_BACK          5266  'to 5266'
             5388  POP_BLOCK        
           5390_0  COME_FROM_LOOP     5256  '5256'

 L. 698      5390  LOAD_FAST                'azi'
             5392  LOAD_METHOD              insert
             5394  LOAD_CONST               0
             5396  LOAD_FAST                'azi'
             5398  LOAD_CONST               0
             5400  BINARY_SUBSCR    
             5402  CALL_METHOD_2         2  '2 positional arguments'
             5404  POP_TOP          

 L. 699      5406  LOAD_FAST                'elev'
             5408  LOAD_METHOD              insert
             5410  LOAD_CONST               0
             5412  LOAD_FAST                'elev'
             5414  LOAD_CONST               0
             5416  BINARY_SUBSCR    
             5418  CALL_METHOD_2         2  '2 positional arguments'
             5420  POP_TOP          

 L. 701      5422  SETUP_LOOP         5456  'to 5456'
             5424  LOAD_GLOBAL              enumerate
             5426  LOAD_FAST                't'
             5428  CALL_FUNCTION_1       1  '1 positional argument'
             5430  GET_ITER         
             5432  FOR_ITER           5454  'to 5454'
             5434  UNPACK_SEQUENCE_2     2 
             5436  STORE_FAST               'i'
             5438  STORE_FAST               'tex'

 L. 702      5440  LOAD_STR                 'isot'
             5442  LOAD_FAST                't'
             5444  LOAD_FAST                'i'
             5446  BINARY_SUBSCR    
             5448  STORE_ATTR               format
         5450_5452  JUMP_BACK          5432  'to 5432'
             5454  POP_BLOCK        
           5456_0  COME_FROM_LOOP     5422  '5422'

 L. 705      5456  LOAD_FAST                't'
             5458  LOAD_CONST               -1
             5460  BINARY_SUBSCR    
             5462  LOAD_FAST                't'
             5464  LOAD_CONST               0
             5466  BINARY_SUBSCR    
             5468  BINARY_SUBTRACT  
             5470  STORE_FAST               'duration'

 L. 709      5472  LOAD_FAST                'np'
             5474  LOAD_ATTR                around
             5476  LOAD_FAST                'elev'
             5478  LOAD_CONST               4
             5480  LOAD_CONST               ('decimals',)
             5482  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             5484  STORE_FAST               'elev'

 L. 710      5486  LOAD_FAST                'np'
             5488  LOAD_ATTR                around
             5490  LOAD_FAST                'azi'
             5492  LOAD_CONST               4
             5494  LOAD_CONST               ('decimals',)
             5496  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             5498  STORE_FAST               'azi'

 L. 711      5500  LOAD_FAST                'np'
             5502  LOAD_METHOD              column_stack
             5504  LOAD_FAST                't'
             5506  LOAD_FAST                'azi'
             5508  LOAD_FAST                'elev'
             5510  BUILD_TUPLE_3         3 
             5512  CALL_METHOD_1         1  '1 positional argument'
             5514  STORE_FAST               'final'

 L. 712      5516  LOAD_FAST                'np'
             5518  LOAD_METHOD              hstack
             5520  LOAD_FAST                'final'
             5522  LOAD_FAST                'np'
             5524  LOAD_METHOD              zeros
             5526  LOAD_FAST                'final'
             5528  LOAD_ATTR                shape
             5530  LOAD_CONST               0
             5532  BINARY_SUBSCR    
             5534  LOAD_CONST               10
             5536  BUILD_TUPLE_2         2 
             5538  CALL_METHOD_1         1  '1 positional argument'
             5540  BUILD_TUPLE_2         2 
             5542  CALL_METHOD_1         1  '1 positional argument'
             5544  STORE_FAST               'final'

 L. 733      5546  LOAD_STR                 '<FILE>\n<HEADER>\nGENERATION DATE       : '
             5548  LOAD_GLOBAL              str
             5550  LOAD_FAST                'nowtime'
             5552  CALL_FUNCTION_1       1  '1 positional argument'
             5554  BINARY_ADD       
             5556  LOAD_STR                 '\nANTENNA               : VIL-2\nLATITUDE              : 40d26m44.2s\nLONGITUDE             : -3d57m9.4s\nHEIGHT            [KM]: 0.6648\nTARGET                : SCANNING\nTRAJECTORY DATA SOURCE: CESAR/JPL\nS -DL-FREQUENCY  [MHZ]: 2277.000\nX -DL-FREQUENCY  [MHZ]: 0.000\nKA-DL-FREQUENCY  [MHZ]: 0.000\nANALYSIS PERIOD-START : '
             5558  BINARY_ADD       
             5560  LOAD_GLOBAL              str
             5562  LOAD_FAST                'obs_time'
             5564  LOAD_CONST               0
             5566  BINARY_SUBSCR    
             5568  CALL_FUNCTION_1       1  '1 positional argument'
             5570  BINARY_ADD       
             5572  LOAD_STR                 '\nANALYSIS PERIOD-END   : '
             5574  BINARY_ADD       
             5576  LOAD_GLOBAL              str
             5578  LOAD_FAST                'obs_time'
             5580  LOAD_CONST               -1
             5582  BINARY_SUBSCR    
             5584  CALL_FUNCTION_1       1  '1 positional argument'
             5586  BINARY_ADD       
             5588  LOAD_STR                 '\nNUMBER OF PASSES      : 2\n</HEADER>\n<PASS>\n'
             5590  BINARY_ADD       
             5592  LOAD_GLOBAL              str
             5594  LOAD_FAST                'obs_time'
             5596  LOAD_CONST               0
             5598  BINARY_SUBSCR    
             5600  CALL_FUNCTION_1       1  '1 positional argument'
             5602  BINARY_ADD       
             5604  LOAD_STR                 '  '
             5606  BINARY_ADD       
             5608  LOAD_GLOBAL              str
             5610  LOAD_FAST                'obs_time'
             5612  LOAD_CONST               -1
             5614  BINARY_SUBSCR    
             5616  CALL_FUNCTION_1       1  '1 positional argument'
             5618  BINARY_ADD       

 L. 734      5620  LOAD_STR                 '\n<ZPASS>\n</ZPASS>\n<WRAP>\n</WRAP>\n<INIT_TRAVEL_RANGE>\n<LOWER/>\n</INIT_TRAVEL_RANGE>\n   Date - Time        AZ (Deg) EL (Deg) TxRx dXEl (deg) TxRx dEl (deg)  Range (km) Range Rate (km/s)    S-Dop (Hz)      X-Dop (Hz)      Ka-Dop(Hz)      S-EIRP(dBw)     X-EIRP(dBW)     Ka-EIRP(dBW)\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
             5622  BINARY_ADD       
             5624  STORE_FAST               'header'

 L. 744      5626  LOAD_STR                 'date'
             5628  LOAD_FAST                'obs_time'
             5630  STORE_ATTR               out_subfmt

 L. 745      5632  LOAD_FAST                'np'
             5634  LOAD_ATTR                savetxt
             5636  LOAD_STR                 'certobs/scan-'
             5638  LOAD_GLOBAL              str
             5640  LOAD_FAST                'nowtime'
             5642  CALL_FUNCTION_1       1  '1 positional argument'
             5644  BINARY_ADD       
             5646  LOAD_STR                 '.txt'
             5648  BINARY_ADD       
             5650  LOAD_FAST                'final'
             5652  LOAD_STR                 '%s'
             5654  LOAD_STR                 ' '
             5656  LOAD_FAST                'header'
             5658  LOAD_STR                 '</PASS>\n</FILE>'
             5660  LOAD_STR                 ''
             5662  LOAD_CONST               ('fmt', 'delimiter', 'header', 'footer', 'comments')
             5664  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             5666  POP_TOP          

 L. 750      5668  LOAD_STR                 '\n<PASS>\n'
             5670  LOAD_GLOBAL              str
             5672  LOAD_FAST                'nowtime'
             5674  CALL_FUNCTION_1       1  '1 positional argument'
             5676  BINARY_ADD       

 L. 751      5678  LOAD_STR                 '\n<ZPASS>\n</ZPASS>\n<WRAP>\n</WRAP>\n<INIT_TRAVEL_RANGE>\n<LOWER/>\n</INIT_TRAVEL_RANGE>\n   Date - Time        AZ (Deg) EL (Deg) TxRx dXEl (deg) TxRx dEl (deg)  Range (km) Range Rate (km/s)    S-Dop (Hz)      X-Dop (Hz)      Ka-Dop(Hz)      S-EIRP(dBw)     X-EIRP(dBW)     Ka-EIRP(dBW)\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
             5680  BINARY_ADD       
             5682  STORE_FAST               'inter'

 L. 761      5684  LOAD_STR                 'date_hms'
             5686  LOAD_FAST                'obs_time'
             5688  STORE_ATTR               out_subfmt
             5690  JUMP_FORWARD       5700  'to 5700'
           5692_0  COME_FROM          3528  '3528'

 L. 764      5692  LOAD_GLOBAL              ValueError
             5694  LOAD_STR                 'Invalid observing mode'
             5696  CALL_FUNCTION_1       1  '1 positional argument'
             5698  RAISE_VARARGS_1       1  'exception instance'
           5700_0  COME_FROM          5690  '5690'
           5700_1  COME_FROM          3478  '3478'
           5700_2  COME_FROM          2868  '2868'
           5700_3  COME_FROM          1762  '1762'

Parse error at or near `JUMP_FORWARD' instruction at offset 3478_3480