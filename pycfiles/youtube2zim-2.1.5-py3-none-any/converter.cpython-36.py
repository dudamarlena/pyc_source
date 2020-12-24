# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/youtube/youtube2zim/converter.py
# Compiled at: 2020-03-13 12:16:48
# Size of source mod 2**32: 2802 bytes
import pathlib, subprocess
from zimscraperlib.logging import nicer_args_join
from zimscraperlib.imaging import resize_image
from .constants import logger

def hook_youtube_dl_ffmpeg--- This code section failed: ---

 L.  20         0  LOAD_FAST                'data'
                2  LOAD_ATTR                get
                4  LOAD_STR                 'status'
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  LOAD_STR                 'finished'
               10  COMPARE_OP               !=
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L.  21        14  LOAD_CONST               None
               16  RETURN_END_IF    
             18_0  COME_FROM            12  '12'

 L.  23        18  LOAD_GLOBAL              print
               20  LOAD_STR                 '#### '
               22  LOAD_FAST                'data'
               24  LOAD_STR                 'filename'
               26  BINARY_SUBSCR    
               28  LOAD_FAST                'video_format'
               30  LOAD_FAST                'low_quality'
               32  CALL_FUNCTION_4       4  '4 positional arguments'
               34  POP_TOP          

 L.  25        36  LOAD_CONST               None
               38  RETURN_VALUE     

 L.  40        40  POP_JUMP_IF_FALSE    46  'to 46'

 L.  41        42  LOAD_CONST               None
               44  RETURN_END_IF    
             46_0  COME_FROM            40  '40'

 L.  43        46  LOAD_STR                 'h264'
               48  LOAD_STR                 'libvpx'
               50  LOAD_CONST               ('mp4', 'webm')
               52  BUILD_CONST_KEY_MAP_2     2 
               54  STORE_FAST               'video_codecs'

 L.  44        56  LOAD_STR                 'aac'
               58  LOAD_STR                 'libvorbis'
               60  LOAD_CONST               ('mp4', 'webm')
               62  BUILD_CONST_KEY_MAP_2     2 
               64  STORE_FAST               'audio_codecs'

 L.  45        66  LOAD_STR                 '-movflags'
               68  LOAD_STR                 '+faststart'
               70  BUILD_LIST_2          2 
               72  BUILD_LIST_0          0 
               74  LOAD_CONST               ('mp4', 'webm')
               76  BUILD_CONST_KEY_MAP_2     2 
               78  STORE_FAST               'params'

 L.  47        80  LOAD_STR                 'ffmpeg'
               82  LOAD_STR                 '-y'
               84  LOAD_STR                 '-i'
               86  LOAD_STR                 'file:{}'
               88  LOAD_ATTR                format
               90  LOAD_GLOBAL              str
               92  LOAD_FAST                'src_path'
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  BUILD_LIST_4          4 
              100  STORE_FAST               'args'

 L.  49       102  LOAD_FAST                'low_quality'
              104  POP_JUMP_IF_FALSE   174  'to 174'

 L.  50       108  LOAD_FAST                'args'

 L.  51       110  LOAD_STR                 '-codec:v'

 L.  52       112  LOAD_FAST                'video_codecs'
              114  LOAD_FAST                'video_format'
              116  BINARY_SUBSCR    

 L.  53       118  LOAD_STR                 '-quality'

 L.  54       120  LOAD_STR                 'best'

 L.  55       122  LOAD_STR                 '-cpu-used'

 L.  56       124  LOAD_STR                 '0'

 L.  57       126  LOAD_STR                 '-b:v'

 L.  58       128  LOAD_STR                 '300k'

 L.  59       130  LOAD_STR                 '-qmin'

 L.  60       132  LOAD_STR                 '30'

 L.  61       134  LOAD_STR                 '-qmax'

 L.  62       136  LOAD_STR                 '42'

 L.  63       138  LOAD_STR                 '-maxrate'

 L.  64       140  LOAD_STR                 '300k'

 L.  65       142  LOAD_STR                 '-bufsize'

 L.  66       144  LOAD_STR                 '1000k'

 L.  67       146  LOAD_STR                 '-threads'

 L.  68       148  LOAD_STR                 '8'

 L.  69       150  LOAD_STR                 '-vf'

 L.  70       152  LOAD_STR                 "scale='480:trunc(ow/a/2)*2'"

 L.  71       154  LOAD_STR                 '-codec:a'

 L.  72       156  LOAD_FAST                'audio_codecs'
              158  LOAD_FAST                'video_format'
              160  BINARY_SUBSCR    

 L.  73       162  LOAD_STR                 '-b:a'

 L.  74       164  LOAD_STR                 '128k'
              166  BUILD_LIST_24        24 
              168  INPLACE_ADD      
              170  STORE_FAST               'args'
              172  JUMP_FORWARD        214  'to 214'
              174  ELSE                     '214'

 L.  77       174  LOAD_FAST                'args'

 L.  78       176  LOAD_STR                 '-codec:v'

 L.  79       178  LOAD_FAST                'video_codecs'
              180  LOAD_FAST                'video_format'
              182  BINARY_SUBSCR    

 L.  80       184  LOAD_STR                 '-quality'

 L.  81       186  LOAD_STR                 'best'

 L.  82       188  LOAD_STR                 '-cpu-used'

 L.  83       190  LOAD_STR                 '0'

 L.  84       192  LOAD_STR                 '-bufsize'

 L.  85       194  LOAD_STR                 '1000k'

 L.  86       196  LOAD_STR                 '-threads'

 L.  87       198  LOAD_STR                 '8'

 L.  88       200  LOAD_STR                 '-codec:a'

 L.  89       202  LOAD_FAST                'audio_codecs'
              204  LOAD_FAST                'video_format'
              206  BINARY_SUBSCR    
              208  BUILD_LIST_12        12 
              210  INPLACE_ADD      
              212  STORE_FAST               'args'
            214_0  COME_FROM           172  '172'

 L.  91       214  LOAD_FAST                'args'
              216  LOAD_FAST                'params'
              218  LOAD_FAST                'video_format'
              220  BINARY_SUBSCR    
              222  INPLACE_ADD      
              224  STORE_FAST               'args'

 L.  92       226  LOAD_FAST                'args'
              228  LOAD_STR                 'file:{}'
              230  LOAD_ATTR                format
              232  LOAD_GLOBAL              str
              234  LOAD_FAST                'tmp_path'
              236  CALL_FUNCTION_1       1  '1 positional argument'
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  BUILD_LIST_1          1 
              242  INPLACE_ADD      
              244  STORE_FAST               'args'

 L.  94       246  LOAD_GLOBAL              logger
              248  LOAD_ATTR                info

 L.  95       250  LOAD_STR                 '  converting {src} into {dst}'
              252  LOAD_ATTR                format
              254  LOAD_GLOBAL              str
              256  LOAD_FAST                'src_path'
              258  CALL_FUNCTION_1       1  '1 positional argument'
              260  LOAD_GLOBAL              str
              262  LOAD_FAST                'dst_path'
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  LOAD_CONST               ('src', 'dst')
              268  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              270  CALL_FUNCTION_1       1  '1 positional argument'
              272  POP_TOP          

 L.  97       274  LOAD_GLOBAL              logger
              276  LOAD_ATTR                debug
              278  LOAD_GLOBAL              nicer_args_join
              280  LOAD_FAST                'args'
              282  CALL_FUNCTION_1       1  '1 positional argument'
              284  CALL_FUNCTION_1       1  '1 positional argument'
              286  POP_TOP          

 L.  99       288  LOAD_GLOBAL              subprocess
              290  LOAD_ATTR                run
              292  LOAD_FAST                'args'
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  STORE_FAST               'ffmpeg'

 L. 100       298  LOAD_FAST                'ffmpeg'
              300  LOAD_ATTR                check_returncode
              302  CALL_FUNCTION_0       0  '0 positional arguments'
              304  POP_TOP          

 L. 103       306  LOAD_FAST                'src_path'
              308  LOAD_ATTR                unlink
              310  CALL_FUNCTION_0       0  '0 positional arguments'
              312  POP_TOP          

 L. 105       314  LOAD_FAST                'tmp_path'
              316  LOAD_ATTR                replace
              318  LOAD_FAST                'dst_path'
              320  CALL_FUNCTION_1       1  '1 positional argument'
              322  POP_TOP          

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 40