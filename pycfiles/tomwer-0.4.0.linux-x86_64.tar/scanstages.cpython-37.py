# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/synctools/utils/scanstages.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 8822 bytes
"""
Utils to mock scans
"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '09/01/2020'
import shutil, glob
from tomwer.core.scan.scanbase import TomoBase
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.hdf5scan import HDF5TomoScan
import silx.utils.enum as _Enum
from silx.io.url import DataUrl
import os
from tomwer.synctools.rsyncmanager import RSyncManager

class ScanStages:
    __doc__ = '\n    Util class to copy all the files of scan to a destination dir until\n    a define advancement of the acquisition.\n\n    :param TomoBase scan: scan to copy.\n    '

    class AcquisitionStage(_Enum):
        ACQUI_NOT_STARTED = (0, )
        ACQUI_STARTED = (1, )
        ACQUI_ON_GOING = (2, )
        ACQUI_ENDED = (3, )
        RECONSTRUCTION_ADDED = (4, )
        COMPLETE = (99, )

        def get_command_name(self):
            """Return the name of the AcquisitionStage to give by a command
            option"""
            return self.name.lower().replace('_', '-')

        @staticmethod
        def get_command_names():
            return [stage.get_command_name() for stage in ScanStages.AcquisitionStage]

        @staticmethod
        def from_command_name(name):
            """Return the AcquisitionStage fitting a command option"""
            name_ = name.replace('-', '_').upper()
            return getattr(ScanStages.AcquisitionStage, name_)

    def __init__(self, scan: TomoBase):
        assert isinstance(scan, TomoBase)
        self.scan = scan

    def rsync_until(self, stage: AcquisitionStage, dest_dir: str) -> None:
        """

        :param stage:
        :type: AcquisitionStage
        :param dest_dir:
        :type: str
        """
        stage = ScanStages.AcquisitionStage.from_value(stage)
        if not dest_dir.endswith(os.path.basename(self.scan.path)):
            dest_dir = os.path.join(dest_dir, os.path.basename(self.scan.path))
        for t_stage in ScanStages.AcquisitionStage:
            if t_stage.value <= stage.value:
                self._rsync_stage(t_stage, dest_dir=dest_dir)

    def _rsync_stage--- This code section failed: ---

 L. 103         0  LOAD_FAST                'dest_dir'
                2  LOAD_METHOD              endswith
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                path
                8  LOAD_METHOD              basename
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                scan
               14  LOAD_ATTR                path
               16  CALL_METHOD_1         1  '1 positional argument'
               18  CALL_METHOD_1         1  '1 positional argument'
               20  POP_JUMP_IF_TRUE     48  'to 48'

 L. 104        22  LOAD_GLOBAL              os
               24  LOAD_ATTR                path
               26  LOAD_METHOD              join
               28  LOAD_FAST                'dest_dir'
               30  LOAD_GLOBAL              os
               32  LOAD_ATTR                path
               34  LOAD_METHOD              basename
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                scan
               40  LOAD_ATTR                path
               42  CALL_METHOD_1         1  '1 positional argument'
               44  CALL_METHOD_2         2  '2 positional arguments'
               46  STORE_FAST               'dest_dir'
             48_0  COME_FROM            20  '20'

 L. 105        48  LOAD_GLOBAL              ScanStages
               50  LOAD_ATTR                AcquisitionStage
               52  LOAD_METHOD              from_value
               54  LOAD_FAST                'stage'
               56  CALL_METHOD_1         1  '1 positional argument'
               58  STORE_FAST               'stage'

 L. 106        60  LOAD_FAST                'stage'
               62  LOAD_GLOBAL              ScanStages
               64  LOAD_ATTR                AcquisitionStage
               66  LOAD_ATTR                ACQUI_NOT_STARTED
               68  COMPARE_OP               is
               70  POP_JUMP_IF_FALSE    76  'to 76'

 L. 107        72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'

 L. 108        76  LOAD_FAST                'stage'
               78  LOAD_GLOBAL              ScanStages
               80  LOAD_ATTR                AcquisitionStage
               82  LOAD_ATTR                ACQUI_STARTED
               84  COMPARE_OP               is
               86  POP_JUMP_IF_FALSE   202  'to 202'

 L. 109        88  LOAD_GLOBAL              isinstance
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                scan
               94  LOAD_GLOBAL              EDFTomoScan
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  POP_JUMP_IF_FALSE   180  'to 180'

 L. 110       100  LOAD_GLOBAL              os
              102  LOAD_ATTR                path
              104  LOAD_METHOD              isdir
              106  LOAD_FAST                'dest_dir'
              108  CALL_METHOD_1         1  '1 positional argument'
              110  POP_JUMP_IF_TRUE    122  'to 122'

 L. 111       112  LOAD_GLOBAL              os
              114  LOAD_METHOD              mkdir
              116  LOAD_FAST                'dest_dir'
              118  CALL_METHOD_1         1  '1 positional argument'
              120  POP_TOP          
            122_0  COME_FROM           110  '110'

 L. 112       122  LOAD_FAST                'self'
              124  LOAD_ATTR                scan
              126  LOAD_METHOD              get_info_file
              128  CALL_METHOD_0         0  '0 positional arguments'
              130  STORE_FAST               'info_file'

 L. 113       132  LOAD_FAST                'info_file'
              134  LOAD_CONST               None
              136  COMPARE_OP               is-not
              138  POP_JUMP_IF_FALSE   198  'to 198'

 L. 114       140  LOAD_GLOBAL              os
              142  LOAD_ATTR                path
              144  LOAD_METHOD              join
              146  LOAD_FAST                'dest_dir'
              148  LOAD_GLOBAL              os
              150  LOAD_ATTR                path
              152  LOAD_METHOD              basename
              154  LOAD_FAST                'info_file'
              156  CALL_METHOD_1         1  '1 positional argument'
              158  CALL_METHOD_2         2  '2 positional arguments'
              160  STORE_FAST               'file_info_dest'

 L. 115       162  LOAD_GLOBAL              RSyncManager
              164  CALL_FUNCTION_0       0  '0 positional arguments'
              166  LOAD_ATTR                syncFile
              168  LOAD_FAST                'info_file'
              170  LOAD_FAST                'file_info_dest'
              172  LOAD_CONST               ('src', 'dst')
              174  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              176  POP_TOP          
              178  JUMP_FORWARD       1156  'to 1156'
            180_0  COME_FROM            98  '98'

 L. 116       180  LOAD_GLOBAL              isinstance
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                scan
              186  LOAD_GLOBAL              HDF5TomoScan
              188  CALL_FUNCTION_2       2  '2 positional arguments'
              190  POP_JUMP_IF_FALSE   198  'to 198'

 L. 117       192  LOAD_GLOBAL              NotImplementedError
              194  CALL_FUNCTION_0       0  '0 positional arguments'
              196  RAISE_VARARGS_1       1  'exception instance'
            198_0  COME_FROM           190  '190'
            198_1  COME_FROM           138  '138'
          198_200  JUMP_FORWARD       1156  'to 1156'
            202_0  COME_FROM            86  '86'

 L. 118       202  LOAD_FAST                'stage'
              204  LOAD_GLOBAL              ScanStages
              206  LOAD_ATTR                AcquisitionStage
              208  LOAD_ATTR                ACQUI_ON_GOING
              210  COMPARE_OP               is
          212_214  POP_JUMP_IF_FALSE   338  'to 338'

 L. 120       216  LOAD_GLOBAL              isinstance
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                scan
              222  LOAD_GLOBAL              EDFTomoScan
              224  CALL_FUNCTION_2       2  '2 positional arguments'
          226_228  POP_JUMP_IF_FALSE   314  'to 314'

 L. 121       230  LOAD_FAST                'self'
              232  LOAD_ATTR                scan
              234  LOAD_METHOD              getProjectionsUrl
              236  CALL_METHOD_0         0  '0 positional arguments'
              238  STORE_FAST               'urls'

 L. 122       240  LOAD_GLOBAL              len
              242  LOAD_FAST                'urls'
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  LOAD_CONST               2
              248  BINARY_FLOOR_DIVIDE
              250  STORE_FAST               'n_url'

 L. 123       252  LOAD_GLOBAL              list
              254  LOAD_FAST                'urls'
              256  LOAD_METHOD              keys
              258  CALL_METHOD_0         0  '0 positional arguments'
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  STORE_FAST               'keys'

 L. 124       264  SETUP_LOOP          334  'to 334'
              266  LOAD_FAST                'n_url'
              268  LOAD_CONST               0
              270  COMPARE_OP               >
          272_274  POP_JUMP_IF_FALSE   310  'to 310'

 L. 125       276  LOAD_FAST                'n_url'
              278  LOAD_CONST               1
              280  INPLACE_SUBTRACT 
              282  STORE_FAST               'n_url'

 L. 126       284  LOAD_FAST                'self'
              286  LOAD_ATTR                _copy_url_file
              288  LOAD_FAST                'urls'
              290  LOAD_FAST                'keys'
              292  LOAD_FAST                'n_url'
              294  BINARY_SUBSCR    
              296  BINARY_SUBSCR    
              298  LOAD_FAST                'dest_dir'
              300  LOAD_CONST               ('url', 'dest_dir')
              302  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              304  POP_TOP          
          306_308  JUMP_BACK           266  'to 266'
            310_0  COME_FROM           272  '272'
              310  POP_BLOCK        
              312  JUMP_FORWARD       1156  'to 1156'
            314_0  COME_FROM           226  '226'

 L. 128       314  LOAD_GLOBAL              isinstance
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                scan
              320  LOAD_GLOBAL              HDF5TomoScan
              322  CALL_FUNCTION_2       2  '2 positional arguments'
          324_326  POP_JUMP_IF_FALSE  1156  'to 1156'

 L. 129       328  LOAD_GLOBAL              NotImplementedError
              330  CALL_FUNCTION_0       0  '0 positional arguments'
              332  RAISE_VARARGS_1       1  'exception instance'
            334_0  COME_FROM_LOOP      264  '264'
          334_336  JUMP_FORWARD       1156  'to 1156'
            338_0  COME_FROM           212  '212'

 L. 130       338  LOAD_FAST                'stage'
              340  LOAD_GLOBAL              ScanStages
              342  LOAD_ATTR                AcquisitionStage
              344  LOAD_ATTR                ACQUI_ENDED
              346  COMPARE_OP               is
          348_350  POP_JUMP_IF_FALSE   542  'to 542'

 L. 131       352  LOAD_GLOBAL              isinstance
              354  LOAD_FAST                'self'
              356  LOAD_ATTR                scan
              358  LOAD_GLOBAL              EDFTomoScan
              360  CALL_FUNCTION_2       2  '2 positional arguments'
          362_364  POP_JUMP_IF_FALSE   518  'to 518'

 L. 132       366  SETUP_LOOP          444  'to 444'
              368  LOAD_FAST                'self'
              370  LOAD_ATTR                scan
              372  LOAD_METHOD              getProjectionsUrl
              374  CALL_METHOD_0         0  '0 positional arguments'
              376  LOAD_METHOD              items
              378  CALL_METHOD_0         0  '0 positional arguments'
              380  GET_ITER         
            382_0  COME_FROM           420  '420'
              382  FOR_ITER            442  'to 442'
              384  UNPACK_SEQUENCE_2     2 
              386  STORE_FAST               '_'
              388  STORE_FAST               'url'

 L. 133       390  LOAD_FAST                'url'
              392  LOAD_METHOD              file_path
              394  CALL_METHOD_0         0  '0 positional arguments'
              396  LOAD_METHOD              replace
              398  LOAD_FAST                'self'
              400  LOAD_ATTR                scan
              402  LOAD_ATTR                path

 L. 134       404  LOAD_FAST                'dest_dir'
              406  CALL_METHOD_2         2  '2 positional arguments'
              408  STORE_FAST               'file_target'

 L. 135       410  LOAD_GLOBAL              os
              412  LOAD_ATTR                path
              414  LOAD_METHOD              exists
              416  LOAD_FAST                'file_target'
              418  CALL_METHOD_1         1  '1 positional argument'
          420_422  POP_JUMP_IF_TRUE    382  'to 382'

 L. 136       424  LOAD_FAST                'self'
              426  LOAD_ATTR                _copy_url_file
              428  LOAD_FAST                'url'
              430  LOAD_FAST                'dest_dir'
              432  LOAD_CONST               ('url', 'dest_dir')
              434  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              436  POP_TOP          
          438_440  JUMP_BACK           382  'to 382'
              442  POP_BLOCK        
            444_0  COME_FROM_LOOP      366  '366'

 L. 137       444  LOAD_GLOBAL              os
              446  LOAD_ATTR                path
              448  LOAD_METHOD              join
              450  LOAD_FAST                'self'
              452  LOAD_ATTR                scan
              454  LOAD_ATTR                path
              456  LOAD_GLOBAL              os
              458  LOAD_ATTR                path
              460  LOAD_METHOD              basename
              462  LOAD_FAST                'self'
              464  LOAD_ATTR                scan
              466  LOAD_ATTR                path
              468  CALL_METHOD_1         1  '1 positional argument'
              470  LOAD_STR                 '.xml'
              472  BINARY_ADD       
              474  CALL_METHOD_2         2  '2 positional arguments'
              476  STORE_FAST               'xml_file'

 L. 138       478  LOAD_GLOBAL              os
              480  LOAD_ATTR                path
              482  LOAD_METHOD              join
              484  LOAD_FAST                'dest_dir'
              486  LOAD_GLOBAL              os
              488  LOAD_ATTR                path
              490  LOAD_METHOD              basename
              492  LOAD_FAST                'xml_file'
              494  CALL_METHOD_1         1  '1 positional argument'
              496  CALL_METHOD_2         2  '2 positional arguments'
              498  STORE_FAST               'xml_dest'

 L. 139       500  LOAD_GLOBAL              RSyncManager
              502  CALL_FUNCTION_0       0  '0 positional arguments'
              504  LOAD_ATTR                syncFile
              506  LOAD_FAST                'xml_file'
              508  LOAD_FAST                'xml_dest'
              510  LOAD_CONST               ('src', 'dst')
              512  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              514  POP_TOP          
              516  JUMP_FORWARD       1156  'to 1156'
            518_0  COME_FROM           362  '362'

 L. 140       518  LOAD_GLOBAL              isinstance
              520  LOAD_FAST                'self'
              522  LOAD_ATTR                scan
              524  LOAD_GLOBAL              HDF5TomoScan
              526  CALL_FUNCTION_2       2  '2 positional arguments'
          528_530  POP_JUMP_IF_FALSE  1156  'to 1156'

 L. 141       532  LOAD_GLOBAL              NotImplementedError
              534  CALL_FUNCTION_0       0  '0 positional arguments'
              536  RAISE_VARARGS_1       1  'exception instance'
          538_540  JUMP_FORWARD       1156  'to 1156'
            542_0  COME_FROM           348  '348'

 L. 142       542  LOAD_FAST                'stage'
              544  LOAD_GLOBAL              ScanStages
              546  LOAD_ATTR                AcquisitionStage
              548  LOAD_ATTR                RECONSTRUCTION_ADDED
              550  COMPARE_OP               is
          552_554  POP_JUMP_IF_FALSE  1034  'to 1034'

 L. 144       556  LOAD_GLOBAL              isinstance
              558  LOAD_FAST                'self'
              560  LOAD_ATTR                scan
              562  LOAD_GLOBAL              EDFTomoScan
              564  CALL_FUNCTION_2       2  '2 positional arguments'
          566_568  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 145       570  LOAD_GLOBAL              EDFTomoScan
              572  LOAD_ATTR                getPYHST_ReconsFile
              574  LOAD_FAST                'self'
              576  LOAD_ATTR                scan
              578  LOAD_ATTR                path
              580  LOAD_CONST               ('scanID',)
              582  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              584  STORE_FAST               'pyhst_files'

 L. 146       586  LOAD_FAST                'pyhst_files'
          588_590  POP_JUMP_IF_FALSE   646  'to 646'

 L. 147       592  SETUP_LOOP          646  'to 646'
              594  LOAD_FAST                'pyhst_files'
              596  GET_ITER         
              598  FOR_ITER            644  'to 644'
              600  STORE_FAST               'par_file'

 L. 148       602  LOAD_GLOBAL              os
              604  LOAD_ATTR                path
              606  LOAD_METHOD              join
              608  LOAD_FAST                'dest_dir'

 L. 149       610  LOAD_GLOBAL              os
              612  LOAD_ATTR                path
              614  LOAD_METHOD              basename
              616  LOAD_FAST                'par_file'
              618  CALL_METHOD_1         1  '1 positional argument'
              620  CALL_METHOD_2         2  '2 positional arguments'
              622  STORE_FAST               'par_file_dst'

 L. 150       624  LOAD_GLOBAL              RSyncManager
              626  CALL_FUNCTION_0       0  '0 positional arguments'
              628  LOAD_ATTR                syncFile
              630  LOAD_FAST                'par_file'
              632  LOAD_FAST                'par_file_dst'
              634  LOAD_CONST               ('src', 'dst')
              636  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              638  POP_TOP          
          640_642  JUMP_BACK           598  'to 598'
              644  POP_BLOCK        
            646_0  COME_FROM_LOOP      592  '592'
            646_1  COME_FROM           588  '588'

 L. 151       646  SETUP_LOOP          730  'to 730'
              648  LOAD_GLOBAL              EDFTomoScan
              650  LOAD_ATTR                getReconstructionsPaths
              652  LOAD_FAST                'self'
              654  LOAD_ATTR                scan
              656  LOAD_ATTR                path
              658  LOAD_CONST               ('scanID',)
              660  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              662  GET_ITER         
              664  FOR_ITER            728  'to 728'
              666  STORE_FAST               'reconstructed_file'

 L. 152       668  LOAD_GLOBAL              os
              670  LOAD_ATTR                path
              672  LOAD_METHOD              isfile
              674  LOAD_FAST                'reconstructed_file'
              676  CALL_METHOD_1         1  '1 positional argument'
          678_680  POP_JUMP_IF_TRUE    686  'to 686'
              682  LOAD_ASSERT              AssertionError
              684  RAISE_VARARGS_1       1  'exception instance'
            686_0  COME_FROM           678  '678'

 L. 153       686  LOAD_GLOBAL              os
              688  LOAD_ATTR                path
              690  LOAD_METHOD              join
              692  LOAD_FAST                'dest_dir'
              694  LOAD_GLOBAL              os
              696  LOAD_ATTR                path
              698  LOAD_METHOD              basename
              700  LOAD_FAST                'reconstructed_file'
              702  CALL_METHOD_1         1  '1 positional argument'
              704  CALL_METHOD_2         2  '2 positional arguments'
              706  STORE_FAST               'recons_file_dest'

 L. 154       708  LOAD_GLOBAL              RSyncManager
              710  CALL_FUNCTION_0       0  '0 positional arguments'
              712  LOAD_ATTR                syncFile
              714  LOAD_FAST                'reconstructed_file'

 L. 155       716  LOAD_FAST                'recons_file_dest'
              718  LOAD_CONST               ('src', 'dst')
              720  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              722  POP_TOP          
          724_726  JUMP_BACK           664  'to 664'
              728  POP_BLOCK        
            730_0  COME_FROM_LOOP      646  '646'

 L. 157       730  SETUP_LOOP          822  'to 822'
              732  LOAD_GLOBAL              glob
              734  LOAD_METHOD              glob
              736  LOAD_GLOBAL              os
              738  LOAD_ATTR                path
              740  LOAD_METHOD              join
              742  LOAD_FAST                'self'
              744  LOAD_ATTR                scan
              746  LOAD_ATTR                path
              748  LOAD_STR                 '*.par'
              750  CALL_METHOD_2         2  '2 positional arguments'
              752  CALL_METHOD_1         1  '1 positional argument'
              754  GET_ITER         
              756  FOR_ITER            820  'to 820'
              758  STORE_FAST               'par_file'

 L. 158       760  LOAD_GLOBAL              os
              762  LOAD_ATTR                path
              764  LOAD_METHOD              join
              766  LOAD_FAST                'self'
              768  LOAD_ATTR                scan
              770  LOAD_ATTR                path
              772  LOAD_FAST                'par_file'
              774  CALL_METHOD_2         2  '2 positional arguments'
              776  STORE_FAST               'par_file_src'

 L. 159       778  LOAD_GLOBAL              os
              780  LOAD_ATTR                path
              782  LOAD_METHOD              join
              784  LOAD_FAST                'dest_dir'
              786  LOAD_GLOBAL              os
              788  LOAD_ATTR                path
              790  LOAD_METHOD              basename
              792  LOAD_FAST                'par_file'
              794  CALL_METHOD_1         1  '1 positional argument'
              796  CALL_METHOD_2         2  '2 positional arguments'
              798  STORE_FAST               'par_file_dst'

 L. 160       800  LOAD_GLOBAL              RSyncManager
              802  CALL_FUNCTION_0       0  '0 positional arguments'
              804  LOAD_ATTR                syncFile
              806  LOAD_FAST                'par_file_src'
              808  LOAD_FAST                'par_file_dst'
              810  LOAD_CONST               ('src', 'dst')
              812  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              814  POP_TOP          
          816_818  JUMP_BACK           756  'to 756'
              820  POP_BLOCK        
            822_0  COME_FROM_LOOP      730  '730'

 L. 162       822  SETUP_LOOP          914  'to 914'
              824  LOAD_GLOBAL              glob
              826  LOAD_METHOD              glob
              828  LOAD_GLOBAL              os
              830  LOAD_ATTR                path
              832  LOAD_METHOD              join
              834  LOAD_FAST                'self'
              836  LOAD_ATTR                scan
              838  LOAD_ATTR                path
              840  LOAD_STR                 '*.info'
              842  CALL_METHOD_2         2  '2 positional arguments'
              844  CALL_METHOD_1         1  '1 positional argument'
              846  GET_ITER         
              848  FOR_ITER            912  'to 912'
              850  STORE_FAST               'info_file'

 L. 163       852  LOAD_GLOBAL              os
              854  LOAD_ATTR                path
              856  LOAD_METHOD              join
              858  LOAD_FAST                'self'
              860  LOAD_ATTR                scan
              862  LOAD_ATTR                path
              864  LOAD_FAST                'info_file'
              866  CALL_METHOD_2         2  '2 positional arguments'
              868  STORE_FAST               'info_file_src'

 L. 164       870  LOAD_GLOBAL              os
              872  LOAD_ATTR                path
              874  LOAD_METHOD              join
              876  LOAD_FAST                'dest_dir'
              878  LOAD_GLOBAL              os
              880  LOAD_ATTR                path
              882  LOAD_METHOD              basename
              884  LOAD_FAST                'info_file'
              886  CALL_METHOD_1         1  '1 positional argument'
              888  CALL_METHOD_2         2  '2 positional arguments'
              890  STORE_FAST               'info_file_dst'

 L. 165       892  LOAD_GLOBAL              RSyncManager
              894  CALL_FUNCTION_0       0  '0 positional arguments'
              896  LOAD_ATTR                syncFile
              898  LOAD_FAST                'info_file_src'
              900  LOAD_FAST                'info_file_dst'
              902  LOAD_CONST               ('src', 'dst')
              904  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              906  POP_TOP          
          908_910  JUMP_BACK           848  'to 848'
              912  POP_BLOCK        
            914_0  COME_FROM_LOOP      822  '822'

 L. 167       914  LOAD_GLOBAL              glob
              916  LOAD_METHOD              glob
              918  LOAD_GLOBAL              os
              920  LOAD_ATTR                path
              922  LOAD_METHOD              join
              924  LOAD_FAST                'self'
              926  LOAD_ATTR                scan
              928  LOAD_ATTR                path
              930  LOAD_STR                 '*.xml'
              932  CALL_METHOD_2         2  '2 positional arguments'
              934  CALL_METHOD_1         1  '1 positional argument'
              936  STORE_FAST               'xml_files'

 L. 168       938  SETUP_LOOP         1032  'to 1032'
              940  LOAD_FAST                'xml_files'
              942  GET_ITER         
              944  FOR_ITER           1008  'to 1008'
              946  STORE_FAST               'xml_file'

 L. 169       948  LOAD_GLOBAL              os
              950  LOAD_ATTR                path
              952  LOAD_METHOD              join
              954  LOAD_FAST                'self'
              956  LOAD_ATTR                scan
              958  LOAD_ATTR                path
              960  LOAD_FAST                'xml_file'
              962  CALL_METHOD_2         2  '2 positional arguments'
              964  STORE_FAST               '_xml_file'

 L. 170       966  LOAD_GLOBAL              os
              968  LOAD_ATTR                path
              970  LOAD_METHOD              join
              972  LOAD_FAST                'dest_dir'

 L. 171       974  LOAD_GLOBAL              os
              976  LOAD_ATTR                path
              978  LOAD_METHOD              basename
              980  LOAD_FAST                '_xml_file'
              982  CALL_METHOD_1         1  '1 positional argument'
              984  CALL_METHOD_2         2  '2 positional arguments'
              986  STORE_FAST               'xml_dest'

 L. 172       988  LOAD_GLOBAL              RSyncManager
              990  CALL_FUNCTION_0       0  '0 positional arguments'
              992  LOAD_ATTR                syncFile
              994  LOAD_FAST                '_xml_file'
              996  LOAD_FAST                'xml_dest'
              998  LOAD_CONST               ('src', 'dst')
             1000  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1002  POP_TOP          
         1004_1006  JUMP_BACK           944  'to 944'
             1008  POP_BLOCK        
             1010  JUMP_FORWARD       1032  'to 1032'
           1012_0  COME_FROM           566  '566'

 L. 173      1012  LOAD_GLOBAL              isinstance
             1014  LOAD_FAST                'self'
             1016  LOAD_ATTR                scan
             1018  LOAD_GLOBAL              HDF5TomoScan
             1020  CALL_FUNCTION_2       2  '2 positional arguments'
         1022_1024  POP_JUMP_IF_FALSE  1156  'to 1156'

 L. 174      1026  LOAD_GLOBAL              NotImplementedError
             1028  CALL_FUNCTION_0       0  '0 positional arguments'
             1030  RAISE_VARARGS_1       1  'exception instance'
           1032_0  COME_FROM          1010  '1010'
           1032_1  COME_FROM_LOOP      938  '938'
             1032  JUMP_FORWARD       1156  'to 1156'
           1034_0  COME_FROM           552  '552'

 L. 175      1034  LOAD_FAST                'stage'
             1036  LOAD_GLOBAL              ScanStages
             1038  LOAD_ATTR                AcquisitionStage
             1040  LOAD_ATTR                COMPLETE
             1042  COMPARE_OP               is
         1044_1046  POP_JUMP_IF_FALSE  1146  'to 1146'

 L. 176      1048  LOAD_GLOBAL              isinstance
             1050  LOAD_FAST                'self'
             1052  LOAD_ATTR                scan
             1054  LOAD_GLOBAL              EDFTomoScan
             1056  CALL_FUNCTION_2       2  '2 positional arguments'
         1058_1060  POP_JUMP_IF_FALSE  1124  'to 1124'

 L. 177      1062  SETUP_LOOP         1144  'to 1144'
             1064  LOAD_GLOBAL              os
             1066  LOAD_METHOD              listdir
             1068  LOAD_FAST                'self'
             1070  LOAD_ATTR                scan
             1072  LOAD_ATTR                path
             1074  CALL_METHOD_1         1  '1 positional argument'
             1076  GET_ITER         
             1078  FOR_ITER           1120  'to 1120'
             1080  STORE_FAST               'file_'

 L. 178      1082  LOAD_GLOBAL              os
             1084  LOAD_ATTR                path
             1086  LOAD_METHOD              join
             1088  LOAD_FAST                'self'
             1090  LOAD_ATTR                scan
             1092  LOAD_ATTR                path
             1094  LOAD_FAST                'file_'
             1096  CALL_METHOD_2         2  '2 positional arguments'
             1098  STORE_FAST               'file_fp'

 L. 179      1100  LOAD_GLOBAL              RSyncManager
             1102  CALL_FUNCTION_0       0  '0 positional arguments'
             1104  LOAD_ATTR                syncFile
             1106  LOAD_FAST                'file_fp'
             1108  LOAD_FAST                'dest_dir'
             1110  LOAD_CONST               ('src', 'dst')
             1112  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1114  POP_TOP          
         1116_1118  JUMP_BACK          1078  'to 1078'
             1120  POP_BLOCK        
             1122  JUMP_FORWARD       1144  'to 1144'
           1124_0  COME_FROM          1058  '1058'

 L. 180      1124  LOAD_GLOBAL              isinstance
             1126  LOAD_FAST                'self'
             1128  LOAD_ATTR                scan
             1130  LOAD_GLOBAL              HDF5TomoScan
           1132_0  COME_FROM           516  '516'
           1132_1  COME_FROM           312  '312'
             1132  CALL_FUNCTION_2       2  '2 positional arguments'
           1134_0  COME_FROM           178  '178'
         1134_1136  POP_JUMP_IF_FALSE  1156  'to 1156'

 L. 181      1138  LOAD_GLOBAL              NotImplementedError
             1140  CALL_FUNCTION_0       0  '0 positional arguments'
             1142  RAISE_VARARGS_1       1  'exception instance'
           1144_0  COME_FROM          1122  '1122'
           1144_1  COME_FROM_LOOP     1062  '1062'
             1144  JUMP_FORWARD       1156  'to 1156'
           1146_0  COME_FROM          1044  '1044'

 L. 183      1146  LOAD_GLOBAL              ValueError
             1148  LOAD_STR                 'given stage is not recognized'
             1150  LOAD_FAST                'stage'
             1152  CALL_FUNCTION_2       2  '2 positional arguments'
             1154  RAISE_VARARGS_1       1  'exception instance'
           1156_0  COME_FROM          1144  '1144'
           1156_1  COME_FROM          1134  '1134'
           1156_2  COME_FROM          1032  '1032'
           1156_3  COME_FROM          1022  '1022'
           1156_4  COME_FROM           538  '538'
           1156_5  COME_FROM           528  '528'
           1156_6  COME_FROM           334  '334'
           1156_7  COME_FROM           324  '324'
           1156_8  COME_FROM           198  '198'

Parse error at or near `COME_FROM_LOOP' instruction at offset 334_0

    def _copy_url_file(self, url, dest_dir):
        assert isinstance(url, DataUrl)
        file_target = url.file_path().replace(self.scan.path, dest_dir)
        if not os.path.exists(file_target):
            shutil.copyfile(src=(url.file_path()), dst=file_target)