# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\User\Documents\GitHub\fourMs\MGT-python\musicalgestures\_videoreader.py
# Compiled at: 2020-04-26 09:07:30
# Size of source mod 2**32: 7565 bytes
import cv2, os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import numpy as np
from musicalgestures._videoadjust import mg_contrast_brightness, mg_skip_frames
from musicalgestures._cropvideo import *
from musicalgestures._utils import convert_to_avi, rotate_video, extract_wav, embed_audio_in_video, convert_to_grayscale

class ReadError(Exception):
    __doc__ = 'Base class for file read errors.'


def mg_videoreader--- This code section failed: ---

 L. 110         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              splitext
                6  LOAD_FAST                'filename'
                8  CALL_METHOD_1         1  ''
               10  LOAD_CONST               0
               12  BINARY_SUBSCR    
               14  STORE_FAST               'of'

 L. 111        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              splitext
               22  LOAD_FAST                'filename'
               24  CALL_METHOD_1         1  ''
               26  LOAD_CONST               1
               28  BINARY_SUBSCR    
               30  STORE_FAST               'fex'

 L. 113        32  LOAD_CONST               False
               34  STORE_FAST               'trimming'

 L. 114        36  LOAD_CONST               False
               38  STORE_FAST               'skipping'

 L. 115        40  LOAD_CONST               False
               42  STORE_FAST               'rotating'

 L. 116        44  LOAD_CONST               False
               46  STORE_FAST               'cbing'

 L. 117        48  LOAD_CONST               False
               50  STORE_FAST               'cropping'

 L. 119        52  LOAD_FAST                'fex'
               54  LOAD_STR                 '.avi'
               56  COMPARE_OP               !=
               58  POP_JUMP_IF_FALSE    92  'to 92'

 L. 120        60  LOAD_GLOBAL              print
               62  LOAD_STR                 'Converting from'
               64  LOAD_FAST                'fex'
               66  LOAD_STR                 'to .avi...'
               68  CALL_FUNCTION_3       3  ''
               70  POP_TOP          

 L. 121        72  LOAD_GLOBAL              convert_to_avi
               74  LOAD_FAST                'filename'
               76  CALL_FUNCTION_1       1  ''
               78  POP_TOP          

 L. 122        80  LOAD_STR                 '.avi'
               82  STORE_FAST               'fex'

 L. 123        84  LOAD_FAST                'of'
               86  LOAD_FAST                'fex'
               88  BINARY_ADD       
               90  STORE_FAST               'filename'
             92_0  COME_FROM            58  '58'

 L. 126        92  LOAD_FAST                'starttime'
               94  LOAD_CONST               0
               96  COMPARE_OP               !=
               98  POP_JUMP_IF_TRUE    108  'to 108'
              100  LOAD_FAST                'endtime'
              102  LOAD_CONST               0
              104  COMPARE_OP               !=
              106  POP_JUMP_IF_FALSE   176  'to 176'
            108_0  COME_FROM            98  '98'

 L. 127       108  LOAD_GLOBAL              print
              110  LOAD_STR                 'Trimming...'
              112  CALL_FUNCTION_1       1  ''
              114  POP_TOP          

 L. 128       116  LOAD_GLOBAL              ffmpeg_extract_subclip

 L. 129       118  LOAD_FAST                'filename'

 L. 129       120  LOAD_FAST                'starttime'

 L. 129       122  LOAD_FAST                'endtime'

 L. 129       124  LOAD_FAST                'of'
              126  LOAD_STR                 '_trim'
              128  BINARY_ADD       
              130  LOAD_FAST                'fex'
              132  BINARY_ADD       

 L. 128       134  LOAD_CONST               ('targetname',)
              136  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              138  STORE_FAST               'trimvideo'

 L. 130       140  LOAD_GLOBAL              print
              142  LOAD_STR                 'Trimming done.'
              144  CALL_FUNCTION_1       1  ''
              146  POP_TOP          

 L. 131       148  LOAD_FAST                'of'
              150  LOAD_STR                 '_trim'
              152  BINARY_ADD       
              154  STORE_FAST               'of'

 L. 132       156  LOAD_CONST               True
              158  STORE_FAST               'trimming'

 L. 133       160  LOAD_GLOBAL              cv2
              162  LOAD_METHOD              VideoCapture
              164  LOAD_FAST                'of'
              166  LOAD_FAST                'fex'
              168  BINARY_ADD       
              170  CALL_METHOD_1         1  ''
              172  STORE_FAST               'vidcap'
              174  JUMP_FORWARD        190  'to 190'
            176_0  COME_FROM           106  '106'

 L. 137       176  LOAD_GLOBAL              cv2
              178  LOAD_METHOD              VideoCapture
              180  LOAD_FAST                'of'
              182  LOAD_FAST                'fex'
              184  BINARY_ADD       
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'vidcap'
            190_0  COME_FROM           174  '174'

 L. 140       190  LOAD_GLOBAL              int
              192  LOAD_FAST                'vidcap'
              194  LOAD_METHOD              get
              196  LOAD_GLOBAL              cv2
              198  LOAD_ATTR                CAP_PROP_FPS
              200  CALL_METHOD_1         1  ''
              202  CALL_FUNCTION_1       1  ''
              204  STORE_FAST               'fps'

 L. 141       206  LOAD_GLOBAL              int
              208  LOAD_FAST                'vidcap'
              210  LOAD_METHOD              get
              212  LOAD_GLOBAL              cv2
              214  LOAD_ATTR                CAP_PROP_FRAME_WIDTH
              216  CALL_METHOD_1         1  ''
              218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'width'

 L. 142       222  LOAD_GLOBAL              int
              224  LOAD_FAST                'vidcap'
              226  LOAD_METHOD              get
              228  LOAD_GLOBAL              cv2
              230  LOAD_ATTR                CAP_PROP_FRAME_HEIGHT
              232  CALL_METHOD_1         1  ''
              234  CALL_FUNCTION_1       1  ''
              236  STORE_FAST               'height'

 L. 143       238  LOAD_GLOBAL              int
              240  LOAD_FAST                'vidcap'
              242  LOAD_METHOD              get
              244  LOAD_GLOBAL              cv2
              246  LOAD_ATTR                CAP_PROP_FRAME_COUNT
              248  CALL_METHOD_1         1  ''
              250  CALL_FUNCTION_1       1  ''
              252  STORE_FAST               'length'

 L. 145       254  LOAD_FAST                'fps'
              256  LOAD_CONST               0
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   280  'to 280'

 L. 146       264  LOAD_GLOBAL              ReadError
              266  LOAD_STR                 'Could not open '
              268  LOAD_FAST                'filename'
              270  FORMAT_VALUE          0  ''
              272  LOAD_STR                 '.'
              274  BUILD_STRING_3        3 
              276  CALL_FUNCTION_1       1  ''
              278  RAISE_VARARGS_1       1  'exception instance'
            280_0  COME_FROM           260  '260'

 L. 148       280  LOAD_FAST                'length'
              282  LOAD_FAST                'fps'
              284  BINARY_TRUE_DIVIDE
              286  STORE_FAST               'source_length_s'

 L. 149       288  LOAD_FAST                'of'
              290  LOAD_FAST                'fex'
              292  BINARY_ADD       
              294  STORE_FAST               'source_name'

 L. 150       296  LOAD_FAST                'source_length_s'
              298  STORE_FAST               'new_length_s'

 L. 151       300  LOAD_CONST               1
              302  STORE_FAST               'dilation_ratio'

 L. 152       304  LOAD_CONST               False
              306  STORE_FAST               'need_to_embed_audio'

 L. 154       308  LOAD_FAST                'skip'
              310  LOAD_CONST               0
              312  COMPARE_OP               !=
          314_316  POP_JUMP_IF_TRUE    352  'to 352'
              318  LOAD_FAST                'contrast'
              320  LOAD_CONST               0
              322  COMPARE_OP               !=
          324_326  POP_JUMP_IF_TRUE    352  'to 352'
              328  LOAD_FAST                'brightness'
              330  LOAD_CONST               0
              332  COMPARE_OP               !=
          334_336  POP_JUMP_IF_TRUE    352  'to 352'
              338  LOAD_FAST                'crop'
              340  LOAD_METHOD              lower
              342  CALL_METHOD_0         0  ''
              344  LOAD_STR                 'none'
              346  COMPARE_OP               !=
          348_350  POP_JUMP_IF_FALSE   364  'to 364'
            352_0  COME_FROM           334  '334'
            352_1  COME_FROM           324  '324'
            352_2  COME_FROM           314  '314'

 L. 155       352  LOAD_GLOBAL              extract_wav
              354  LOAD_FAST                'source_name'
              356  CALL_FUNCTION_1       1  ''
              358  STORE_FAST               'source_audio'

 L. 156       360  LOAD_CONST               True
              362  STORE_FAST               'need_to_embed_audio'
            364_0  COME_FROM           348  '348'

 L. 159       364  LOAD_FAST                'skip'
              366  LOAD_CONST               0
              368  COMPARE_OP               !=
          370_372  POP_JUMP_IF_FALSE   490  'to 490'

 L. 160       374  LOAD_GLOBAL              mg_skip_frames

 L. 161       376  LOAD_FAST                'of'

 L. 161       378  LOAD_FAST                'fex'

 L. 161       380  LOAD_FAST                'vidcap'

 L. 161       382  LOAD_FAST                'skip'

 L. 161       384  LOAD_FAST                'fps'

 L. 161       386  LOAD_FAST                'length'

 L. 161       388  LOAD_FAST                'width'

 L. 161       390  LOAD_FAST                'height'

 L. 160       392  CALL_FUNCTION_8       8  ''
              394  UNPACK_SEQUENCE_5     5 
              396  STORE_FAST               'vidcap'
              398  STORE_FAST               'length'
              400  STORE_FAST               'fps'
              402  STORE_FAST               'width'
              404  STORE_FAST               'height'

 L. 162       406  LOAD_FAST                'keep_all'
          408_410  POP_JUMP_IF_TRUE    432  'to 432'
              412  LOAD_FAST                'trimming'
          414_416  POP_JUMP_IF_FALSE   432  'to 432'

 L. 163       418  LOAD_GLOBAL              os
              420  LOAD_METHOD              remove
              422  LOAD_FAST                'of'
              424  LOAD_FAST                'fex'
              426  BINARY_ADD       
              428  CALL_METHOD_1         1  ''
              430  POP_TOP          
            432_0  COME_FROM           414  '414'
            432_1  COME_FROM           408  '408'

 L. 164       432  LOAD_FAST                'of'
              434  LOAD_STR                 '_skip'
              436  BINARY_ADD       
              438  STORE_FAST               'of'

 L. 165       440  LOAD_CONST               True
              442  STORE_FAST               'skipping'

 L. 166       444  LOAD_FAST                'length'
              446  LOAD_FAST                'fps'
              448  BINARY_TRUE_DIVIDE
              450  STORE_FAST               'new_length_s'

 L. 167       452  LOAD_FAST                'source_length_s'
              454  LOAD_FAST                'new_length_s'
              456  BINARY_TRUE_DIVIDE
              458  STORE_FAST               'dilation_ratio'

 L. 168       460  LOAD_FAST                'keep_all'
          462_464  POP_JUMP_IF_FALSE   490  'to 490'

 L. 169       466  LOAD_FAST                'vidcap'
              468  LOAD_METHOD              release
              470  CALL_METHOD_0         0  ''
              472  POP_TOP          

 L. 170       474  LOAD_GLOBAL              embed_audio_in_video
              476  LOAD_FAST                'source_audio'
              478  LOAD_FAST                'of'
              480  LOAD_FAST                'fex'
              482  BINARY_ADD       
              484  LOAD_FAST                'dilation_ratio'
              486  CALL_FUNCTION_3       3  ''
              488  POP_TOP          
            490_0  COME_FROM           462  '462'
            490_1  COME_FROM           370  '370'

 L. 173       490  LOAD_FAST                'endtime'
              492  LOAD_CONST               0
              494  COMPARE_OP               ==
          496_498  POP_JUMP_IF_FALSE   508  'to 508'

 L. 174       500  LOAD_FAST                'length'
              502  LOAD_FAST                'fps'
              504  BINARY_TRUE_DIVIDE
              506  STORE_FAST               'endtime'
            508_0  COME_FROM           496  '496'

 L. 176       508  LOAD_FAST                'rotate'
              510  LOAD_CONST               0
              512  COMPARE_OP               !=
          514_516  POP_JUMP_IF_FALSE   634  'to 634'

 L. 177       518  LOAD_FAST                'vidcap'
              520  LOAD_METHOD              release
              522  CALL_METHOD_0         0  ''
              524  POP_TOP          

 L. 178       526  LOAD_GLOBAL              print
              528  LOAD_STR                 'Rotating video by '
              530  LOAD_FAST                'rotate'
              532  FORMAT_VALUE          0  ''
              534  LOAD_STR                 ' degrees...'
              536  BUILD_STRING_3        3 
              538  LOAD_STR                 ''
              540  LOAD_CONST               ('end',)
              542  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              544  POP_TOP          

 L. 179       546  LOAD_GLOBAL              rotate_video
              548  LOAD_FAST                'of'
              550  LOAD_FAST                'fex'
              552  BINARY_ADD       
              554  LOAD_FAST                'rotate'
              556  CALL_FUNCTION_2       2  ''
              558  POP_TOP          

 L. 180       560  LOAD_GLOBAL              print
              562  LOAD_STR                 ' done.'
              564  CALL_FUNCTION_1       1  ''
              566  POP_TOP          

 L. 181       568  LOAD_FAST                'keep_all'
          570_572  POP_JUMP_IF_TRUE    600  'to 600'
              574  LOAD_FAST                'skipping'
          576_578  POP_JUMP_IF_TRUE    586  'to 586'
              580  LOAD_FAST                'trimming'
          582_584  POP_JUMP_IF_FALSE   600  'to 600'
            586_0  COME_FROM           576  '576'

 L. 182       586  LOAD_GLOBAL              os
              588  LOAD_METHOD              remove
              590  LOAD_FAST                'of'
              592  LOAD_FAST                'fex'
              594  BINARY_ADD       
              596  CALL_METHOD_1         1  ''
              598  POP_TOP          
            600_0  COME_FROM           582  '582'
            600_1  COME_FROM           570  '570'

 L. 183       600  LOAD_FAST                'of'
              602  LOAD_STR                 '_rot'
              604  BINARY_ADD       
              606  STORE_FAST               'of'

 L. 184       608  LOAD_CONST               True
              610  STORE_FAST               'rotating'

 L. 185       612  LOAD_FAST                'keep_all'
          614_616  POP_JUMP_IF_FALSE   634  'to 634'

 L. 186       618  LOAD_GLOBAL              embed_audio_in_video
              620  LOAD_FAST                'source_audio'
              622  LOAD_FAST                'of'
              624  LOAD_FAST                'fex'
              626  BINARY_ADD       
              628  LOAD_FAST                'dilation_ratio'
              630  CALL_FUNCTION_3       3  ''
              632  POP_TOP          
            634_0  COME_FROM           614  '614'
            634_1  COME_FROM           514  '514'

 L. 189       634  LOAD_FAST                'contrast'
              636  LOAD_CONST               0
              638  COMPARE_OP               !=
          640_642  POP_JUMP_IF_TRUE    654  'to 654'
              644  LOAD_FAST                'brightness'
              646  LOAD_CONST               0
              648  COMPARE_OP               !=
          650_652  POP_JUMP_IF_FALSE   784  'to 784'
            654_0  COME_FROM           640  '640'

 L. 190       654  LOAD_FAST                'keep_all'
          656_658  POP_JUMP_IF_TRUE    666  'to 666'
              660  LOAD_FAST                'rotating'
          662_664  POP_JUMP_IF_FALSE   680  'to 680'
            666_0  COME_FROM           656  '656'

 L. 191       666  LOAD_GLOBAL              cv2
              668  LOAD_METHOD              VideoCapture
              670  LOAD_FAST                'of'
              672  LOAD_FAST                'fex'
              674  BINARY_ADD       
              676  CALL_METHOD_1         1  ''
              678  STORE_FAST               'vidcap'
            680_0  COME_FROM           662  '662'

 L. 192       680  LOAD_GLOBAL              mg_contrast_brightness

 L. 193       682  LOAD_FAST                'of'

 L. 193       684  LOAD_FAST                'fex'

 L. 193       686  LOAD_FAST                'vidcap'

 L. 193       688  LOAD_FAST                'fps'

 L. 193       690  LOAD_FAST                'length'

 L. 193       692  LOAD_FAST                'width'

 L. 193       694  LOAD_FAST                'height'

 L. 193       696  LOAD_FAST                'contrast'

 L. 193       698  LOAD_FAST                'brightness'

 L. 192       700  CALL_FUNCTION_9       9  ''
              702  STORE_FAST               'vidcap'

 L. 194       704  LOAD_FAST                'keep_all'
          706_708  POP_JUMP_IF_TRUE    742  'to 742'
              710  LOAD_FAST                'rotating'
          712_714  POP_JUMP_IF_TRUE    728  'to 728'
              716  LOAD_FAST                'skipping'
          718_720  POP_JUMP_IF_TRUE    728  'to 728'
              722  LOAD_FAST                'trimming'
          724_726  POP_JUMP_IF_FALSE   742  'to 742'
            728_0  COME_FROM           718  '718'
            728_1  COME_FROM           712  '712'

 L. 195       728  LOAD_GLOBAL              os
              730  LOAD_METHOD              remove
              732  LOAD_FAST                'of'
              734  LOAD_FAST                'fex'
              736  BINARY_ADD       
              738  CALL_METHOD_1         1  ''
              740  POP_TOP          
            742_0  COME_FROM           724  '724'
            742_1  COME_FROM           706  '706'

 L. 196       742  LOAD_FAST                'of'
              744  LOAD_STR                 '_cb'
              746  BINARY_ADD       
              748  STORE_FAST               'of'

 L. 197       750  LOAD_CONST               True
              752  STORE_FAST               'cbing'

 L. 198       754  LOAD_FAST                'keep_all'
          756_758  POP_JUMP_IF_FALSE   784  'to 784'

 L. 199       760  LOAD_FAST                'vidcap'
              762  LOAD_METHOD              release
              764  CALL_METHOD_0         0  ''
              766  POP_TOP          

 L. 200       768  LOAD_GLOBAL              embed_audio_in_video
              770  LOAD_FAST                'source_audio'
              772  LOAD_FAST                'of'
              774  LOAD_FAST                'fex'
              776  BINARY_ADD       
              778  LOAD_FAST                'dilation_ratio'
              780  CALL_FUNCTION_3       3  ''
              782  POP_TOP          
            784_0  COME_FROM           756  '756'
            784_1  COME_FROM           650  '650'

 L. 203       784  LOAD_FAST                'crop'
              786  LOAD_METHOD              lower
              788  CALL_METHOD_0         0  ''
              790  LOAD_STR                 'none'
              792  COMPARE_OP               !=
          794_796  POP_JUMP_IF_FALSE   936  'to 936'

 L. 204       798  LOAD_FAST                'keep_all'
          800_802  POP_JUMP_IF_FALSE   818  'to 818'

 L. 205       804  LOAD_GLOBAL              cv2
              806  LOAD_METHOD              VideoCapture
              808  LOAD_FAST                'of'
              810  LOAD_FAST                'fex'
              812  BINARY_ADD       
              814  CALL_METHOD_1         1  ''
              816  STORE_FAST               'vidcap'
            818_0  COME_FROM           800  '800'

 L. 206       818  LOAD_GLOBAL              mg_cropvideo

 L. 207       820  LOAD_FAST                'fps'

 L. 207       822  LOAD_FAST                'width'

 L. 207       824  LOAD_FAST                'height'

 L. 207       826  LOAD_FAST                'length'

 L. 207       828  LOAD_FAST                'of'

 L. 207       830  LOAD_FAST                'fex'

 L. 207       832  LOAD_FAST                'crop'

 L. 207       834  LOAD_CONST               0.1

 L. 207       836  LOAD_CONST               1

 L. 206       838  LOAD_CONST               ('motion_box_thresh', 'motion_box_margin')
              840  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
              842  UNPACK_SEQUENCE_3     3 
              844  STORE_FAST               'vidcap'
              846  STORE_FAST               'width'
              848  STORE_FAST               'height'

 L. 208       850  LOAD_FAST                'keep_all'
          852_854  POP_JUMP_IF_TRUE    894  'to 894'
              856  LOAD_FAST                'cbing'
          858_860  POP_JUMP_IF_TRUE    880  'to 880'
              862  LOAD_FAST                'rotating'
          864_866  POP_JUMP_IF_TRUE    880  'to 880'
              868  LOAD_FAST                'skipping'
          870_872  POP_JUMP_IF_TRUE    880  'to 880'
              874  LOAD_FAST                'trimming'
          876_878  POP_JUMP_IF_FALSE   894  'to 894'
            880_0  COME_FROM           870  '870'
            880_1  COME_FROM           864  '864'
            880_2  COME_FROM           858  '858'

 L. 209       880  LOAD_GLOBAL              os
              882  LOAD_METHOD              remove
              884  LOAD_FAST                'of'
              886  LOAD_FAST                'fex'
              888  BINARY_ADD       
              890  CALL_METHOD_1         1  ''
              892  POP_TOP          
            894_0  COME_FROM           876  '876'
            894_1  COME_FROM           852  '852'

 L. 210       894  LOAD_FAST                'of'
              896  LOAD_STR                 '_crop'
              898  BINARY_ADD       
              900  STORE_FAST               'of'

 L. 211       902  LOAD_CONST               True
              904  STORE_FAST               'cropping'

 L. 212       906  LOAD_FAST                'keep_all'
          908_910  POP_JUMP_IF_FALSE   936  'to 936'

 L. 213       912  LOAD_FAST                'vidcap'
              914  LOAD_METHOD              release
              916  CALL_METHOD_0         0  ''
              918  POP_TOP          

 L. 214       920  LOAD_GLOBAL              embed_audio_in_video
              922  LOAD_FAST                'source_audio'
              924  LOAD_FAST                'of'
              926  LOAD_FAST                'fex'
              928  BINARY_ADD       
              930  LOAD_FAST                'dilation_ratio'
              932  CALL_FUNCTION_3       3  ''
              934  POP_TOP          
            936_0  COME_FROM           908  '908'
            936_1  COME_FROM           794  '794'

 L. 216       936  LOAD_FAST                'color'
              938  LOAD_CONST               False
              940  COMPARE_OP               ==
          942_944  POP_JUMP_IF_FALSE  1054  'to 1054'
              946  LOAD_FAST                'returned_by_process'
              948  LOAD_CONST               False
              950  COMPARE_OP               ==
          952_954  POP_JUMP_IF_FALSE  1054  'to 1054'

 L. 217       956  LOAD_FAST                'vidcap'
              958  LOAD_METHOD              release
              960  CALL_METHOD_0         0  ''
              962  POP_TOP          

 L. 218       964  LOAD_GLOBAL              print
              966  LOAD_STR                 'Converting to grayscale...'
              968  LOAD_STR                 ''
              970  LOAD_CONST               ('end',)
              972  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              974  POP_TOP          

 L. 219       976  LOAD_GLOBAL              convert_to_grayscale
              978  LOAD_FAST                'of'
              980  LOAD_FAST                'fex'
              982  BINARY_ADD       
              984  CALL_FUNCTION_1       1  ''
              986  UNPACK_SEQUENCE_2     2 
              988  STORE_FAST               'of_gray'
              990  STORE_FAST               'fex'

 L. 220       992  LOAD_GLOBAL              print
              994  LOAD_STR                 ' done.'
              996  CALL_FUNCTION_1       1  ''
              998  POP_TOP          

 L. 221      1000  LOAD_FAST                'keep_all'
         1002_1004  POP_JUMP_IF_TRUE   1050  'to 1050'
             1006  LOAD_FAST                'cropping'
         1008_1010  POP_JUMP_IF_TRUE   1036  'to 1036'
             1012  LOAD_FAST                'cbing'
         1014_1016  POP_JUMP_IF_TRUE   1036  'to 1036'
             1018  LOAD_FAST                'rotating'
         1020_1022  POP_JUMP_IF_TRUE   1036  'to 1036'
             1024  LOAD_FAST                'skipping'
         1026_1028  POP_JUMP_IF_TRUE   1036  'to 1036'
             1030  LOAD_FAST                'trimming'
         1032_1034  POP_JUMP_IF_FALSE  1050  'to 1050'
           1036_0  COME_FROM          1026  '1026'
           1036_1  COME_FROM          1020  '1020'
           1036_2  COME_FROM          1014  '1014'
           1036_3  COME_FROM          1008  '1008'

 L. 222      1036  LOAD_GLOBAL              os
             1038  LOAD_METHOD              remove
             1040  LOAD_FAST                'of'
             1042  LOAD_FAST                'fex'
             1044  BINARY_ADD       
             1046  CALL_METHOD_1         1  ''
             1048  POP_TOP          
           1050_0  COME_FROM          1032  '1032'
           1050_1  COME_FROM          1002  '1002'

 L. 223      1050  LOAD_FAST                'of_gray'
             1052  STORE_FAST               'of'
           1054_0  COME_FROM           952  '952'
           1054_1  COME_FROM           942  '942'

 L. 225      1054  LOAD_FAST                'color'
             1056  LOAD_CONST               True
             1058  COMPARE_OP               ==
         1060_1062  POP_JUMP_IF_TRUE   1074  'to 1074'
             1064  LOAD_FAST                'returned_by_process'
             1066  LOAD_CONST               True
             1068  COMPARE_OP               ==
         1070_1072  POP_JUMP_IF_FALSE  1082  'to 1082'
           1074_0  COME_FROM          1060  '1060'

 L. 226      1074  LOAD_FAST                'vidcap'
             1076  LOAD_METHOD              release
             1078  CALL_METHOD_0         0  ''
             1080  POP_TOP          
           1082_0  COME_FROM          1070  '1070'

 L. 228      1082  LOAD_FAST                'need_to_embed_audio'
         1084_1086  POP_JUMP_IF_FALSE  1114  'to 1114'

 L. 229      1088  LOAD_GLOBAL              embed_audio_in_video
             1090  LOAD_FAST                'source_audio'
             1092  LOAD_FAST                'of'
             1094  LOAD_FAST                'fex'
             1096  BINARY_ADD       
             1098  LOAD_FAST                'dilation_ratio'
             1100  CALL_FUNCTION_3       3  ''
             1102  POP_TOP          

 L. 230      1104  LOAD_GLOBAL              os
             1106  LOAD_METHOD              remove
             1108  LOAD_FAST                'source_audio'
             1110  CALL_METHOD_1         1  ''
             1112  POP_TOP          
           1114_0  COME_FROM          1084  '1084'

 L. 232      1114  LOAD_FAST                'length'
             1116  LOAD_FAST                'width'
             1118  LOAD_FAST                'height'
             1120  LOAD_FAST                'fps'
             1122  LOAD_FAST                'endtime'
             1124  LOAD_FAST                'of'
             1126  LOAD_FAST                'fex'
             1128  BUILD_TUPLE_7         7 
             1130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 1130