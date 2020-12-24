# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/tools/management/commands/videos.py
# Compiled at: 2018-10-12 14:27:15
# Size of source mod 2**32: 4620 bytes
import os
from django.conf import settings
from subprocess import Popen, DEVNULL
from django.core.management.base import BaseCommand
from djangoplus.tools.video import VideoUploader, VideoRecorder

class Command(BaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('video', default=None, nargs='?')
        parser.add_argument('--delete', action='store_true', dest='delete', default=False, help='Deletes the video')
        parser.add_argument('--upload', action='store_true', dest='upload', default=False, help='Uploads the video if it has not been uploaded yet')
        parser.add_argument('--force-upload', action='store_true', dest='force_upload', default=False, help='Uploads the video even it has already been uploaded')
        parser.add_argument('--clear', action='store_true', dest='clear', default=False, help='Deletes all uploaded videos')

    def handle--- This code section failed: ---

 L.  24         0  LOAD_GLOBAL              VideoUploader
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'youtube'

 L.  25         6  LOAD_FAST                'options'
                8  LOAD_METHOD              get
               10  LOAD_STR                 'video'
               12  CALL_METHOD_1         1  '1 positional argument'
               14  STORE_FAST               'video'

 L.  26        16  LOAD_FAST                'options'
               18  LOAD_METHOD              get
               20  LOAD_STR                 'delete'
               22  CALL_METHOD_1         1  '1 positional argument'
               24  STORE_FAST               'delete'

 L.  27        26  LOAD_FAST                'options'
               28  LOAD_METHOD              get
               30  LOAD_STR                 'upload'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  STORE_FAST               'upload'

 L.  28        36  LOAD_FAST                'options'
               38  LOAD_METHOD              get
               40  LOAD_STR                 'force_upload'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  STORE_FAST               'force_upload'

 L.  29        46  LOAD_FAST                'options'
               48  LOAD_METHOD              get
               50  LOAD_STR                 'clear'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  STORE_FAST               'clear'

 L.  30        56  LOAD_FAST                'video'
            58_60  POP_JUMP_IF_FALSE   336  'to 336'

 L.  31        62  LOAD_FAST                'upload'
               64  POP_JUMP_IF_TRUE     70  'to 70'
               66  LOAD_FAST                'force_upload'
               68  POP_JUMP_IF_FALSE   148  'to 148'
             70_0  COME_FROM            64  '64'

 L.  32        70  LOAD_STR                 '{}/{}'
               72  LOAD_METHOD              format
               74  LOAD_GLOBAL              settings
               76  LOAD_ATTR                BASE_DIR
               78  LOAD_FAST                'video'
               80  CALL_METHOD_2         2  '2 positional arguments'
               82  STORE_FAST               'video_path'

 L.  33        84  LOAD_GLOBAL              os
               86  LOAD_ATTR                path
               88  LOAD_METHOD              exists
               90  LOAD_FAST                'video_path'
               92  CALL_METHOD_1         1  '1 positional argument'
               94  POP_JUMP_IF_FALSE   132  'to 132'

 L.  34        96  LOAD_GLOBAL              VideoRecorder
               98  LOAD_METHOD              metadata
              100  LOAD_FAST                'video_path'
              102  CALL_METHOD_1         1  '1 positional argument'
              104  LOAD_METHOD              get
              106  LOAD_STR                 'title'
              108  LOAD_FAST                'video'
              110  CALL_METHOD_2         2  '2 positional arguments'
              112  STORE_FAST               'title'

 L.  35       114  LOAD_FAST                'youtube'
              116  LOAD_ATTR                upload_video
              118  LOAD_FAST                'video_path'
              120  LOAD_FAST                'title'
              122  LOAD_FAST                'force_upload'
              124  LOAD_CONST               ('force',)
              126  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              128  POP_TOP          
              130  JUMP_FORWARD        146  'to 146'
            132_0  COME_FROM            94  '94'

 L.  37       132  LOAD_GLOBAL              print
              134  LOAD_STR                 'Video {} does not exists.'
              136  LOAD_METHOD              format
              138  LOAD_FAST                'video_path'
              140  CALL_METHOD_1         1  '1 positional argument'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  POP_TOP          
            146_0  COME_FROM           130  '130'
              146  JUMP_FORWARD        724  'to 724'
            148_0  COME_FROM            68  '68'

 L.  38       148  LOAD_FAST                'delete'
              150  POP_JUMP_IF_FALSE   242  'to 242'

 L.  39       152  LOAD_FAST                'video'
              154  LOAD_METHOD              endswith
              156  LOAD_STR                 '.mkv'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_JUMP_IF_FALSE   230  'to 230'

 L.  40       162  LOAD_STR                 '{}/{}'
              164  LOAD_METHOD              format
              166  LOAD_GLOBAL              settings
              168  LOAD_ATTR                BASE_DIR
              170  LOAD_FAST                'video'
              172  CALL_METHOD_2         2  '2 positional arguments'
              174  STORE_FAST               'video_path'

 L.  41       176  LOAD_GLOBAL              os
              178  LOAD_ATTR                path
              180  LOAD_METHOD              exists
              182  LOAD_FAST                'video_path'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  POP_JUMP_IF_FALSE   214  'to 214'

 L.  42       188  LOAD_GLOBAL              os
              190  LOAD_METHOD              unlink
              192  LOAD_FAST                'video_path'
              194  CALL_METHOD_1         1  '1 positional argument'
              196  POP_TOP          

 L.  43       198  LOAD_GLOBAL              print
              200  LOAD_STR                 'The video {} deleted from file system.'
              202  LOAD_METHOD              format
              204  LOAD_FAST                'video_path'
              206  CALL_METHOD_1         1  '1 positional argument'
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  POP_TOP          
              212  JUMP_ABSOLUTE       240  'to 240'
            214_0  COME_FROM           186  '186'

 L.  45       214  LOAD_GLOBAL              print
              216  LOAD_STR                 'The video {} does not exists.'
              218  LOAD_METHOD              format
              220  LOAD_FAST                'video_path'
              222  CALL_METHOD_1         1  '1 positional argument'
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  POP_TOP          
              228  JUMP_FORWARD        240  'to 240'
            230_0  COME_FROM           160  '160'

 L.  47       230  LOAD_FAST                'youtube'
              232  LOAD_METHOD              delete_video
              234  LOAD_FAST                'video'
              236  CALL_METHOD_1         1  '1 positional argument'
              238  POP_TOP          
            240_0  COME_FROM           228  '228'
              240  JUMP_FORWARD        724  'to 724'
            242_0  COME_FROM           150  '150'

 L.  49       242  LOAD_CONST               None
              244  STORE_FAST               'vlc'

 L.  50       246  LOAD_GLOBAL              os
              248  LOAD_ATTR                path
              250  LOAD_METHOD              exists
              252  LOAD_STR                 '/Applications/VLC.app/Contents/MacOS/VLC'
              254  CALL_METHOD_1         1  '1 positional argument'
          256_258  POP_JUMP_IF_FALSE   266  'to 266'

 L.  51       260  LOAD_STR                 '/Applications/VLC.app/Contents/MacOS/VLC'
              262  STORE_FAST               'vlc'
              264  JUMP_FORWARD        284  'to 284'
            266_0  COME_FROM           256  '256'

 L.  52       266  LOAD_GLOBAL              os
              268  LOAD_ATTR                path
              270  LOAD_METHOD              exists
              272  LOAD_STR                 '/usr/bin/vlc'
              274  CALL_METHOD_1         1  '1 positional argument'
          276_278  POP_JUMP_IF_FALSE   284  'to 284'

 L.  53       280  LOAD_STR                 '/usr/bin/vlc'
              282  STORE_FAST               'vlc'
            284_0  COME_FROM           276  '276'
            284_1  COME_FROM           264  '264'

 L.  54       284  LOAD_FAST                'vlc'
          286_288  POP_JUMP_IF_FALSE   324  'to 324'

 L.  55       290  LOAD_STR                 '{} --play-and-exit --fullscreen {}'
              292  LOAD_METHOD              format
              294  LOAD_FAST                'vlc'
              296  LOAD_FAST                'video'
              298  CALL_METHOD_2         2  '2 positional arguments'
              300  STORE_FAST               'cmd'

 L.  56       302  LOAD_GLOBAL              Popen
              304  LOAD_FAST                'cmd'
              306  LOAD_METHOD              split
              308  CALL_METHOD_0         0  '0 positional arguments'
              310  LOAD_GLOBAL              DEVNULL
              312  LOAD_GLOBAL              DEVNULL
              314  LOAD_GLOBAL              DEVNULL
              316  LOAD_CONST               ('stdin', 'stdout', 'stderr')
              318  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              320  POP_TOP          
              322  JUMP_FORWARD        724  'to 724'
            324_0  COME_FROM           286  '286'

 L.  58       324  LOAD_GLOBAL              print
              326  LOAD_STR                 'VLC is not installed!'
              328  CALL_FUNCTION_1       1  '1 positional argument'
              330  POP_TOP          
          332_334  JUMP_FORWARD        724  'to 724'
            336_0  COME_FROM            58  '58'

 L.  60       336  LOAD_STR                 '{}/videos'
              338  LOAD_METHOD              format
              340  LOAD_GLOBAL              settings
              342  LOAD_ATTR                BASE_DIR
              344  CALL_METHOD_1         1  '1 positional argument'
              346  STORE_FAST               'directory'

 L.  62       348  BUILD_LIST_0          0 
              350  STORE_FAST               'local_videos'

 L.  63       352  LOAD_GLOBAL              os
              354  LOAD_ATTR                path
              356  LOAD_METHOD              exists
              358  LOAD_FAST                'directory'
              360  CALL_METHOD_1         1  '1 positional argument'
          362_364  POP_JUMP_IF_FALSE   466  'to 466'

 L.  64       366  SETUP_LOOP          466  'to 466'
              368  LOAD_GLOBAL              os
              370  LOAD_METHOD              listdir
              372  LOAD_FAST                'directory'
              374  CALL_METHOD_1         1  '1 positional argument'
              376  GET_ITER         
            378_0  COME_FROM           388  '388'
              378  FOR_ITER            464  'to 464'
              380  STORE_FAST               'file_name'

 L.  65       382  LOAD_STR                 '.mkv'
              384  LOAD_FAST                'file_name'
              386  COMPARE_OP               in
          388_390  POP_JUMP_IF_FALSE   378  'to 378'

 L.  66       392  LOAD_STR                 'videos/{}'
              394  LOAD_METHOD              format
              396  LOAD_FAST                'file_name'
              398  CALL_METHOD_1         1  '1 positional argument'
              400  STORE_FAST               'url'

 L.  67       402  LOAD_GLOBAL              os
              404  LOAD_ATTR                path
              406  LOAD_METHOD              join
              408  LOAD_FAST                'directory'
              410  LOAD_FAST                'file_name'
              412  CALL_METHOD_2         2  '2 positional arguments'
              414  STORE_FAST               'video_path'

 L.  68       416  LOAD_GLOBAL              VideoRecorder
              418  LOAD_METHOD              metadata
              420  LOAD_FAST                'video_path'
              422  CALL_METHOD_1         1  '1 positional argument'
              424  LOAD_METHOD              get
              426  LOAD_STR                 'title'
              428  LOAD_FAST                'file_name'
              430  CALL_METHOD_2         2  '2 positional arguments'
              432  STORE_FAST               'title'

 L.  69       434  LOAD_GLOBAL              dict
              436  LOAD_FAST                'file_name'
              438  LOAD_FAST                'url'
              440  LOAD_FAST                'title'
              442  LOAD_FAST                'video_path'
              444  LOAD_CONST               ('file_name', 'url', 'title', 'video_path')
              446  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              448  STORE_FAST               'local_video'

 L.  70       450  LOAD_FAST                'local_videos'
              452  LOAD_METHOD              append
              454  LOAD_FAST                'local_video'
              456  CALL_METHOD_1         1  '1 positional argument'
              458  POP_TOP          
          460_462  JUMP_BACK           378  'to 378'
              464  POP_BLOCK        
            466_0  COME_FROM_LOOP      366  '366'
            466_1  COME_FROM           362  '362'

 L.  72       466  LOAD_FAST                'upload'
          468_470  POP_JUMP_IF_TRUE    478  'to 478'
              472  LOAD_FAST                'force_upload'
          474_476  POP_JUMP_IF_FALSE   520  'to 520'
            478_0  COME_FROM           468  '468'

 L.  73       478  SETUP_LOOP          724  'to 724'
              480  LOAD_FAST                'local_videos'
              482  GET_ITER         
              484  FOR_ITER            516  'to 516'
              486  STORE_FAST               'local_video'

 L.  74       488  LOAD_FAST                'youtube'
              490  LOAD_ATTR                upload_video
              492  LOAD_FAST                'local_video'
              494  LOAD_STR                 'video_path'
              496  BINARY_SUBSCR    
              498  LOAD_FAST                'local_video'
              500  LOAD_STR                 'title'
              502  BINARY_SUBSCR    
              504  LOAD_FAST                'force_upload'
              506  LOAD_CONST               ('force',)
              508  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              510  POP_TOP          
          512_514  JUMP_BACK           484  'to 484'
              516  POP_BLOCK        
              518  JUMP_FORWARD        724  'to 724'
            520_0  COME_FROM           474  '474'

 L.  75       520  LOAD_FAST                'clear'
          522_524  POP_JUMP_IF_FALSE   562  'to 562'

 L.  76       526  SETUP_LOOP          724  'to 724'
              528  LOAD_FAST                'youtube'
              530  LOAD_METHOD              list_videos
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  GET_ITER         
            536_0  COME_FROM           146  '146'
              536  FOR_ITER            558  'to 558'
              538  STORE_FAST               'uploaded_video'

 L.  77       540  LOAD_FAST                'youtube'
              542  LOAD_METHOD              delete_video
              544  LOAD_FAST                'uploaded_video'
              546  LOAD_STR                 'id'
              548  BINARY_SUBSCR    
              550  CALL_METHOD_1         1  '1 positional argument'
              552  POP_TOP          
          554_556  JUMP_BACK           536  'to 536'
              558  POP_BLOCK        
              560  JUMP_FORWARD        724  'to 724'
            562_0  COME_FROM           522  '522'

 L.  79       562  LOAD_GLOBAL              print
              564  LOAD_STR                 'LOCAL VIDEOS'
              566  CALL_FUNCTION_1       1  '1 positional argument'
              568  POP_TOP          

 L.  80       570  LOAD_FAST                'local_videos'
          572_574  POP_JUMP_IF_FALSE   624  'to 624'

 L.  81       576  SETUP_LOOP          632  'to 632'
              578  LOAD_FAST                'local_videos'
              580  GET_ITER         
              582  FOR_ITER            620  'to 620'
              584  STORE_FAST               'local_video'

 L.  82       586  LOAD_GLOBAL              print
              588  LOAD_STR                 '{}\t{}\t{}'
              590  LOAD_METHOD              format
              592  LOAD_FAST                'local_video'
              594  LOAD_STR                 'file_name'
              596  BINARY_SUBSCR    
              598  LOAD_FAST                'local_video'
              600  LOAD_STR                 'url'
              602  BINARY_SUBSCR    
              604  LOAD_FAST                'local_video'
              606  LOAD_STR                 'title'
              608  BINARY_SUBSCR    
              610  CALL_METHOD_3         3  '3 positional arguments'
              612  CALL_FUNCTION_1       1  '1 positional argument'
              614  POP_TOP          
          616_618  JUMP_BACK           582  'to 582'
              620  POP_BLOCK        
              622  JUMP_FORWARD        632  'to 632'
            624_0  COME_FROM           572  '572'

 L.  84       624  LOAD_GLOBAL              print
              626  LOAD_STR                 'No local video was found!'
              628  CALL_FUNCTION_1       1  '1 positional argument'
            630_0  COME_FROM           240  '240'
              630  POP_TOP          
            632_0  COME_FROM           622  '622'
            632_1  COME_FROM_LOOP      576  '576'

 L.  86       632  LOAD_GLOBAL              print
              634  LOAD_STR                 '\nUPLOADED VIDEOS'
              636  CALL_FUNCTION_1       1  '1 positional argument'
              638  POP_TOP          

 L.  87       640  LOAD_FAST                'youtube'
              642  LOAD_METHOD              list_videos
              644  CALL_METHOD_0         0  '0 positional arguments'
              646  STORE_FAST               'uploaded_videos'

 L.  88       648  LOAD_FAST                'uploaded_videos'
          650_652  POP_JUMP_IF_FALSE   716  'to 716'

 L.  89       654  SETUP_LOOP          724  'to 724'
              656  LOAD_FAST                'uploaded_videos'
              658  GET_ITER         
              660  FOR_ITER            712  'to 712'
              662  STORE_FAST               'uploaded_video'

 L.  90       664  LOAD_STR                 'https://www.youtube.com/watch?v={}'
              666  LOAD_METHOD              format
              668  LOAD_FAST                'uploaded_video'
              670  LOAD_STR                 'id'
              672  BINARY_SUBSCR    
              674  CALL_METHOD_1         1  '1 positional argument'
              676  STORE_FAST               'url'

 L.  91       678  LOAD_GLOBAL              print
              680  LOAD_STR                 '{}\t{}\t{}'
              682  LOAD_METHOD              format
              684  LOAD_FAST                'uploaded_video'
              686  LOAD_STR                 'id'
              688  BINARY_SUBSCR    
              690  LOAD_FAST                'url'
              692  LOAD_FAST                'uploaded_video'
              694  LOAD_STR                 'snippet'
              696  BINARY_SUBSCR    
              698  LOAD_STR                 'title'
              700  BINARY_SUBSCR    
              702  CALL_METHOD_3         3  '3 positional arguments'
              704  CALL_FUNCTION_1       1  '1 positional argument'
              706  POP_TOP          
          708_710  JUMP_BACK           660  'to 660'
            712_0  COME_FROM           322  '322'
              712  POP_BLOCK        
              714  JUMP_FORWARD        724  'to 724'
            716_0  COME_FROM           650  '650'

 L.  93       716  LOAD_GLOBAL              print
              718  LOAD_STR                 'No uploaded video was found!'
              720  CALL_FUNCTION_1       1  '1 positional argument'
              722  POP_TOP          
            724_0  COME_FROM           714  '714'
            724_1  COME_FROM_LOOP      654  '654'
            724_2  COME_FROM           560  '560'
            724_3  COME_FROM_LOOP      526  '526'
            724_4  COME_FROM           518  '518'
            724_5  COME_FROM_LOOP      478  '478'
            724_6  COME_FROM           332  '332'

Parse error at or near `COME_FROM' instruction at offset 630_0