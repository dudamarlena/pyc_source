# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dumpall/thirdparty/dsstore.py
# Compiled at: 2019-10-27 08:50:35
# Size of source mod 2**32: 14335 bytes
import struct

class ParsingError(Exception):
    pass


class DataBlock(object):
    __doc__ = '\n    Class for a basic DataBlock inside of the DS_Store format.\n    '

    def __init__(self, data, debug=False):
        super(DataBlock, self).__init__()
        self.data = data
        self.pos = 0
        self.debug = debug

    def offset_read(self, length, offset=None):
        """
        Returns an byte array of length from data at the given offset or pos.
        If no offset is given, pos will be increased by length.
        Throws ParsingError if offset+length > len(self.data)
        """
        if not offset:
            offset_position = self.pos
        else:
            offset_position = offset
        if len(self.data) < offset_position + length:
            raise ParsingError('Offset+Length > len(self.data)')
        if not offset:
            self.pos += length
        value = self.data[offset_position:offset_position + length]
        self._log('Reading: {}-{} => {}'.format(hex(offset_position), hex(offset_position + length), value))
        return value

    def skip(self, length):
        """
        Increases pos by length without reading data!
        """
        self.pos += length

    def read_filename--- This code section failed: ---

 L.  55         0  LOAD_GLOBAL              struct
                2  LOAD_METHOD              unpack_from
                4  LOAD_STR                 '>I'
                6  LOAD_FAST                'self'
                8  LOAD_METHOD              offset_read
               10  LOAD_CONST               4
               12  CALL_METHOD_1         1  '1 positional argument'
               14  CALL_METHOD_2         2  '2 positional arguments'
               16  UNPACK_SEQUENCE_1     1 
               18  STORE_FAST               'length'

 L.  57        20  LOAD_FAST                'self'
               22  LOAD_METHOD              offset_read
               24  LOAD_CONST               2
               26  LOAD_FAST                'length'
               28  BINARY_MULTIPLY  
               30  CALL_METHOD_1         1  '1 positional argument'
               32  LOAD_METHOD              decode
               34  LOAD_STR                 'utf-16be'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  STORE_FAST               'filename'

 L.  59        40  LOAD_GLOBAL              struct
               42  LOAD_METHOD              unpack_from
               44  LOAD_STR                 '>I'
               46  LOAD_FAST                'self'
               48  LOAD_METHOD              offset_read
               50  LOAD_CONST               4
               52  CALL_METHOD_1         1  '1 positional argument'
               54  CALL_METHOD_2         2  '2 positional arguments'
               56  UNPACK_SEQUENCE_1     1 
               58  STORE_FAST               'structure_id'

 L.  61        60  LOAD_GLOBAL              struct
               62  LOAD_METHOD              unpack_from
               64  LOAD_STR                 '>4s'
               66  LOAD_FAST                'self'
               68  LOAD_METHOD              offset_read
               70  LOAD_CONST               4
               72  CALL_METHOD_1         1  '1 positional argument'
               74  CALL_METHOD_2         2  '2 positional arguments'
               76  UNPACK_SEQUENCE_1     1 
               78  STORE_FAST               'structure_type'

 L.  63        80  LOAD_FAST                'structure_type'
               82  LOAD_METHOD              decode
               84  CALL_METHOD_0         0  '0 positional arguments'
               86  STORE_FAST               'structure_type'

 L.  64        88  LOAD_FAST                'self'
               90  LOAD_METHOD              _log
               92  LOAD_STR                 'Structure type '
               94  LOAD_FAST                'structure_type'
               96  CALL_METHOD_2         2  '2 positional arguments'
               98  POP_TOP          

 L.  66       100  LOAD_CONST               -1
              102  STORE_FAST               'skip'

 L.  68   104_106  SETUP_LOOP          742  'to 742'
            108_0  COME_FROM           722  '722'
            108_1  COME_FROM           714  '714'
            108_2  COME_FROM           576  '576'
              108  LOAD_FAST                'skip'
              110  LOAD_CONST               0
              112  COMPARE_OP               <
          114_116  POP_JUMP_IF_FALSE   740  'to 740'

 L.  69       118  LOAD_FAST                'structure_type'
              120  LOAD_STR                 'bool'
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   134  'to 134'

 L.  70       126  LOAD_CONST               1
              128  STORE_FAST               'skip'
          130_132  JUMP_FORWARD        570  'to 570'
            134_0  COME_FROM           124  '124'

 L.  72       134  LOAD_FAST                'structure_type'
              136  LOAD_STR                 'type'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_TRUE    206  'to 206'

 L.  73       142  LOAD_FAST                'structure_type'
              144  LOAD_STR                 'long'
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_TRUE    206  'to 206'

 L.  74       150  LOAD_FAST                'structure_type'
              152  LOAD_STR                 'shor'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_TRUE    206  'to 206'

 L.  75       158  LOAD_FAST                'structure_type'
              160  LOAD_STR                 'fwsw'
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_TRUE    206  'to 206'

 L.  76       166  LOAD_FAST                'structure_type'
              168  LOAD_STR                 'fwvh'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_TRUE    206  'to 206'

 L.  77       174  LOAD_FAST                'structure_type'
              176  LOAD_STR                 'icvt'
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_TRUE    206  'to 206'

 L.  78       182  LOAD_FAST                'structure_type'
              184  LOAD_STR                 'lsvt'
              186  COMPARE_OP               ==
              188  POP_JUMP_IF_TRUE    206  'to 206'

 L.  79       190  LOAD_FAST                'structure_type'
              192  LOAD_STR                 'vSrn'
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_TRUE    206  'to 206'

 L.  80       198  LOAD_FAST                'structure_type'
              200  LOAD_STR                 'vstl'
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   214  'to 214'
            206_0  COME_FROM           196  '196'
            206_1  COME_FROM           188  '188'
            206_2  COME_FROM           180  '180'
            206_3  COME_FROM           172  '172'
            206_4  COME_FROM           164  '164'
            206_5  COME_FROM           156  '156'
            206_6  COME_FROM           148  '148'
            206_7  COME_FROM           140  '140'

 L.  82       206  LOAD_CONST               4
              208  STORE_FAST               'skip'
          210_212  JUMP_FORWARD        570  'to 570'
            214_0  COME_FROM           204  '204'

 L.  84       214  LOAD_FAST                'structure_type'
              216  LOAD_STR                 'comp'
              218  COMPARE_OP               ==
          220_222  POP_JUMP_IF_TRUE    324  'to 324'

 L.  85       224  LOAD_FAST                'structure_type'
              226  LOAD_STR                 'dutc'
              228  COMPARE_OP               ==
          230_232  POP_JUMP_IF_TRUE    324  'to 324'

 L.  86       234  LOAD_FAST                'structure_type'
              236  LOAD_STR                 'icgo'
              238  COMPARE_OP               ==
          240_242  POP_JUMP_IF_TRUE    324  'to 324'

 L.  87       244  LOAD_FAST                'structure_type'
              246  LOAD_STR                 'icsp'
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_TRUE    324  'to 324'

 L.  88       254  LOAD_FAST                'structure_type'
              256  LOAD_STR                 'logS'
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_TRUE    324  'to 324'

 L.  89       264  LOAD_FAST                'structure_type'
              266  LOAD_STR                 'lg1S'
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_TRUE    324  'to 324'

 L.  90       274  LOAD_FAST                'structure_type'
              276  LOAD_STR                 'lssp'
              278  COMPARE_OP               ==
          280_282  POP_JUMP_IF_TRUE    324  'to 324'

 L.  91       284  LOAD_FAST                'structure_type'
              286  LOAD_STR                 'modD'
              288  COMPARE_OP               ==
          290_292  POP_JUMP_IF_TRUE    324  'to 324'

 L.  92       294  LOAD_FAST                'structure_type'
              296  LOAD_STR                 'moDD'
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_TRUE    324  'to 324'

 L.  93       304  LOAD_FAST                'structure_type'
              306  LOAD_STR                 'phyS'
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_TRUE    324  'to 324'

 L.  94       314  LOAD_FAST                'structure_type'
              316  LOAD_STR                 'ph1S'
              318  COMPARE_OP               ==
          320_322  POP_JUMP_IF_FALSE   330  'to 330'
            324_0  COME_FROM           310  '310'
            324_1  COME_FROM           300  '300'
            324_2  COME_FROM           290  '290'
            324_3  COME_FROM           280  '280'
            324_4  COME_FROM           270  '270'
            324_5  COME_FROM           260  '260'
            324_6  COME_FROM           250  '250'
            324_7  COME_FROM           240  '240'
            324_8  COME_FROM           230  '230'
            324_9  COME_FROM           220  '220'

 L.  96       324  LOAD_CONST               8
              326  STORE_FAST               'skip'
              328  JUMP_FORWARD        570  'to 570'
            330_0  COME_FROM           320  '320'

 L.  97       330  LOAD_FAST                'structure_type'
              332  LOAD_STR                 'blob'
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   366  'to 366'

 L.  98       340  LOAD_GLOBAL              struct
              342  LOAD_METHOD              unpack_from
              344  LOAD_STR                 '>I'
              346  LOAD_FAST                'self'
              348  LOAD_METHOD              offset_read
              350  LOAD_CONST               4
              352  CALL_METHOD_1         1  '1 positional argument'
              354  CALL_METHOD_2         2  '2 positional arguments'
              356  UNPACK_SEQUENCE_1     1 
              358  STORE_FAST               'blen'

 L.  99       360  LOAD_FAST                'blen'
              362  STORE_FAST               'skip'
              364  JUMP_FORWARD        570  'to 570'
            366_0  COME_FROM           336  '336'

 L. 101       366  LOAD_FAST                'structure_type'
              368  LOAD_STR                 'ustr'
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_TRUE    406  'to 406'

 L. 102       376  LOAD_FAST                'structure_type'
              378  LOAD_STR                 'cmmt'
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_TRUE    406  'to 406'

 L. 103       386  LOAD_FAST                'structure_type'
              388  LOAD_STR                 'extn'
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_TRUE    406  'to 406'

 L. 104       396  LOAD_FAST                'structure_type'
              398  LOAD_STR                 'GRP0'
              400  COMPARE_OP               ==
          402_404  POP_JUMP_IF_FALSE   436  'to 436'
            406_0  COME_FROM           392  '392'
            406_1  COME_FROM           382  '382'
            406_2  COME_FROM           372  '372'

 L. 106       406  LOAD_GLOBAL              struct
              408  LOAD_METHOD              unpack_from
              410  LOAD_STR                 '>I'
              412  LOAD_FAST                'self'
              414  LOAD_METHOD              offset_read
              416  LOAD_CONST               4
              418  CALL_METHOD_1         1  '1 positional argument'
              420  CALL_METHOD_2         2  '2 positional arguments'
              422  UNPACK_SEQUENCE_1     1 
              424  STORE_FAST               'blen'

 L. 107       426  LOAD_CONST               2
              428  LOAD_FAST                'blen'
              430  BINARY_MULTIPLY  
              432  STORE_FAST               'skip'
              434  JUMP_FORWARD        570  'to 570'
            436_0  COME_FROM           402  '402'

 L. 108       436  LOAD_FAST                'structure_type'
              438  LOAD_STR                 'BKGD'
              440  COMPARE_OP               ==
          442_444  POP_JUMP_IF_FALSE   452  'to 452'

 L. 109       446  LOAD_CONST               12
              448  STORE_FAST               'skip'
              450  JUMP_FORWARD        570  'to 570'
            452_0  COME_FROM           442  '442'

 L. 111       452  LOAD_FAST                'structure_type'
              454  LOAD_STR                 'ICVO'
              456  COMPARE_OP               ==
          458_460  POP_JUMP_IF_TRUE    482  'to 482'

 L. 112       462  LOAD_FAST                'structure_type'
              464  LOAD_STR                 'LSVO'
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_TRUE    482  'to 482'

 L. 113       472  LOAD_FAST                'structure_type'
              474  LOAD_STR                 'dscl'
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   488  'to 488'
            482_0  COME_FROM           468  '468'
            482_1  COME_FROM           458  '458'

 L. 115       482  LOAD_CONST               1
              484  STORE_FAST               'skip'
              486  JUMP_FORWARD        570  'to 570'
            488_0  COME_FROM           478  '478'

 L. 116       488  LOAD_FAST                'structure_type'
              490  LOAD_STR                 'Iloc'
              492  COMPARE_OP               ==
          494_496  POP_JUMP_IF_TRUE    508  'to 508'
              498  LOAD_FAST                'structure_type'
              500  LOAD_STR                 'fwi0'
              502  COMPARE_OP               ==
          504_506  POP_JUMP_IF_FALSE   514  'to 514'
            508_0  COME_FROM           494  '494'

 L. 117       508  LOAD_CONST               16
              510  STORE_FAST               'skip'
              512  JUMP_FORWARD        570  'to 570'
            514_0  COME_FROM           504  '504'

 L. 118       514  LOAD_FAST                'structure_type'
              516  LOAD_STR                 'dilc'
              518  COMPARE_OP               ==
          520_522  POP_JUMP_IF_FALSE   530  'to 530'

 L. 119       524  LOAD_CONST               32
              526  STORE_FAST               'skip'
              528  JUMP_FORWARD        570  'to 570'
            530_0  COME_FROM           520  '520'

 L. 120       530  LOAD_FAST                'structure_type'
              532  LOAD_STR                 'lsvo'
              534  COMPARE_OP               ==
          536_538  POP_JUMP_IF_FALSE   546  'to 546'

 L. 121       540  LOAD_CONST               76
              542  STORE_FAST               'skip'
              544  JUMP_FORWARD        570  'to 570'
            546_0  COME_FROM           536  '536'

 L. 122       546  LOAD_FAST                'structure_type'
              548  LOAD_STR                 'icvo'
              550  COMPARE_OP               ==
          552_554  POP_JUMP_IF_FALSE   558  'to 558'

 L. 123       556  JUMP_FORWARD        570  'to 570'
            558_0  COME_FROM           552  '552'

 L. 124       558  LOAD_FAST                'structure_type'
              560  LOAD_STR                 'info'
              562  COMPARE_OP               ==
          564_566  POP_JUMP_IF_FALSE   570  'to 570'

 L. 125       568  JUMP_FORWARD        570  'to 570'
            570_0  COME_FROM           568  '568'
            570_1  COME_FROM           564  '564'
            570_2  COME_FROM           556  '556'
            570_3  COME_FROM           544  '544'
            570_4  COME_FROM           528  '528'
            570_5  COME_FROM           512  '512'
            570_6  COME_FROM           486  '486'
            570_7  COME_FROM           450  '450'
            570_8  COME_FROM           434  '434'
            570_9  COME_FROM           364  '364'
           570_10  COME_FROM           328  '328'
           570_11  COME_FROM           210  '210'
           570_12  COME_FROM           130  '130'

 L. 129       570  LOAD_FAST                'skip'
              572  LOAD_CONST               0
              574  COMPARE_OP               <=
              576  POP_JUMP_IF_FALSE   108  'to 108'

 L. 132       578  LOAD_FAST                'self'
              580  LOAD_METHOD              _log
              582  LOAD_STR                 'Re-reading!'
              584  CALL_METHOD_1         1  '1 positional argument'
              586  POP_TOP          

 L. 134       588  LOAD_FAST                'self'
              590  LOAD_METHOD              skip
              592  LOAD_CONST               -8
              594  CALL_METHOD_1         1  '1 positional argument'
              596  POP_TOP          

 L. 135       598  LOAD_FAST                'filename'
              600  LOAD_FAST                'self'
              602  LOAD_METHOD              offset_read
              604  LOAD_CONST               2
              606  CALL_METHOD_1         1  '1 positional argument'
              608  LOAD_METHOD              decode
              610  LOAD_STR                 'utf-16be'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  INPLACE_ADD      
              616  STORE_FAST               'filename'

 L. 137       618  LOAD_GLOBAL              struct
              620  LOAD_METHOD              unpack_from
              622  LOAD_STR                 '>I'
              624  LOAD_FAST                'self'
              626  LOAD_METHOD              offset_read
              628  LOAD_CONST               4
              630  CALL_METHOD_1         1  '1 positional argument'
              632  CALL_METHOD_2         2  '2 positional arguments'
              634  UNPACK_SEQUENCE_1     1 
              636  STORE_FAST               'structure_id'

 L. 138       638  LOAD_GLOBAL              struct
              640  LOAD_METHOD              unpack_from
              642  LOAD_STR                 '>4s'
              644  LOAD_FAST                'self'
              646  LOAD_METHOD              offset_read
              648  LOAD_CONST               4
              650  CALL_METHOD_1         1  '1 positional argument'
              652  CALL_METHOD_2         2  '2 positional arguments'
              654  UNPACK_SEQUENCE_1     1 
              656  STORE_FAST               'structure_type'

 L. 139       658  LOAD_FAST                'structure_type'
              660  LOAD_METHOD              decode
              662  CALL_METHOD_0         0  '0 positional arguments'
              664  STORE_FAST               'structure_type'

 L. 142       666  LOAD_GLOBAL              struct
              668  LOAD_METHOD              unpack_from

 L. 143       670  LOAD_STR                 '>4s'
              672  LOAD_FAST                'self'
              674  LOAD_ATTR                offset_read
              676  LOAD_CONST               4
              678  LOAD_FAST                'self'
              680  LOAD_ATTR                pos
              682  LOAD_CONST               ('offset',)
              684  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              686  CALL_METHOD_2         2  '2 positional arguments'
              688  STORE_FAST               'future_structure_type'

 L. 145       690  LOAD_FAST                'self'
              692  LOAD_METHOD              _log

 L. 146       694  LOAD_STR                 'Re-read structure_id {} / structure_type {}'
              696  LOAD_METHOD              format

 L. 147       698  LOAD_FAST                'structure_id'
              700  LOAD_FAST                'structure_type'
              702  CALL_METHOD_2         2  '2 positional arguments'
              704  CALL_METHOD_1         1  '1 positional argument'
              706  POP_TOP          

 L. 150       708  LOAD_FAST                'structure_type'
              710  LOAD_STR                 'blob'
              712  COMPARE_OP               !=
              714  POP_JUMP_IF_FALSE   108  'to 108'
              716  LOAD_FAST                'future_structure_type'
              718  LOAD_STR                 'blob'
              720  COMPARE_OP               !=
              722  POP_JUMP_IF_FALSE   108  'to 108'

 L. 151       724  LOAD_STR                 ''
              726  STORE_FAST               'structure_type'

 L. 152       728  LOAD_FAST                'self'
              730  LOAD_METHOD              _log
              732  LOAD_STR                 'Forcing another round!'
              734  CALL_METHOD_1         1  '1 positional argument'
              736  POP_TOP          
              738  JUMP_BACK           108  'to 108'
            740_0  COME_FROM           114  '114'
              740  POP_BLOCK        
            742_0  COME_FROM_LOOP      104  '104'

 L. 155       742  LOAD_FAST                'self'
              744  LOAD_METHOD              skip
              746  LOAD_FAST                'skip'
              748  CALL_METHOD_1         1  '1 positional argument'
              750  POP_TOP          

 L. 156       752  LOAD_FAST                'self'
              754  LOAD_METHOD              _log
              756  LOAD_STR                 'Filename {}'
              758  LOAD_METHOD              format
              760  LOAD_FAST                'filename'
              762  CALL_METHOD_1         1  '1 positional argument'
              764  CALL_METHOD_1         1  '1 positional argument'
              766  POP_TOP          

 L. 157       768  LOAD_FAST                'filename'
              770  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 210_212

    def _log(self, *args):
        if self.debug:
            print(('[DEBUG] {}'.format)(*args))


class DS_Store(DataBlock, object):
    __doc__ = '\n    Represents the .DS_Store file from the given binary data. \n    '

    def __init__(self, data, debug=False):
        super(DS_Store, self).__init__datadebug
        self.data = data
        self.root = self._DS_Store__read_header()
        self.offsets = self._DS_Store__read_offsets()
        self.toc = self._DS_Store__read_TOC()
        self.freeList = self._DS_Store__read_freelist()
        self.debug = debug

    def __read_header(self):
        """
        Checks if self.data is actually a .DS_Store file by checking the magic bytes.
        It returns the file's root block.
        """
        if len(self.data) < 36:
            raise ParsingError('Length of data is too short!')
        else:
            magic1, magic2 = struct.unpack_from'>II'self.offset_read(8)
            if not magic1 == 1:
                if not magic2 == 1114989617:
                    raise ParsingError('Magic byte 1 does not match!')
            offset, size, offset2 = struct.unpack_from'>III'self.offset_read(12)
            self._log('Offset 1: {}'.format(offset))
            self._log('Size: {}'.format(size))
            self._log('Offset 2: {}'.format(offset2))
            assert offset == offset2, 'Offsets do not match!'
        self.skip(16)
        return DataBlock((self.offset_readsize(offset + 4)), debug=(self.debug))

    def __read_offsets(self):
        """
        Reads the offsets which follow the header.
        """
        start_pos = self.root.pos
        count, = struct.unpack_from'>I'self.root.offset_read(4)
        self._log('Offset count: {}'.format(count))
        self.root.skip(4)
        offsets = []
        for i in range(count):
            address, = struct.unpack_from'>I'self.root.offset_read(4)
            self._log('Offset {} is {}'.formatiaddress)
            if address == 0:
                continue
            offsets.append(address)

        section_end = start_pos + (count // 256 + 1) * 256 * 4 - count * 4
        self.root.skip(section_end)
        self._log('Skipped {} to {}'.formathex(self.root.pos + section_end)hex(self.root.pos))
        self._log('Offsets: {}'.format(offsets))
        return offsets

    def __read_TOC(self):
        """
        Reads the table of contents (TOCs) from the file.
        """
        self._log('POS {}'.format(hex(self.root.pos)))
        count, = struct.unpack_from'>I'self.root.offset_read(4)
        self._log('Toc count: {}'.format(count))
        toc = {}
        for i in range(count):
            toc_len, = struct.unpack_from'>b'self.root.offset_read(1)
            toc_name, = struct.unpack_from'>{}s'.format(toc_len)self.root.offset_read(toc_len)
            block_id, = struct.unpack_from'>I'self.root.offset_read(4)
            toc[toc_name.decode()] = block_id

        self._log('Toc {}'.format(toc))
        return toc

    def __read_freelist(self):
        """
        Read the free list from the header.
        The free list has n=0..31 buckets with the index 2^n
        """
        freelist = {}
        for i in range(32):
            freelist[2 ** i] = []
            blkcount, = struct.unpack_from'>I'self.root.offset_read(4)
            for j in range(blkcount):
                free_offset, = struct.unpack_from'>I'self.root.offset_read(4)
                freelist[(2 ** i)].append(free_offset)

        self._log('Freelist: {}'.format(freelist))
        return freelist

    def __block_by_id(self, block_id):
        """
        Create a DataBlock from a given block ID (e.g. from the ToC)
        """
        if len(self.offsets) < block_id:
            raise ParsingError('BlockID out of range!')
        addr = self.offsets[block_id]
        offset = int(addr) >> 5 << 5
        size = 1 << (int(addr) & 31)
        self._log('New block: addr {} offset {} size {}'.format(addr, offset + 4, size))
        return DataBlock((self.offset_readsize(offset + 4)), debug=(self.debug))

    def traverse_root(self):
        """
        Traverse from the root block and extract all file names.
        """
        root = self._DS_Store__block_by_id(self.toc['DSDB'])
        root_id, = struct.unpack'>I'root.offset_read(4)
        self._log'Root-ID 'root_id
        internal_block_count, = struct.unpack'>I'root.offset_read(4)
        record_count, = struct.unpack'>I'root.offset_read(4)
        block_count, = struct.unpack'>I'root.offset_read(4)
        unknown, = struct.unpack'>I'root.offset_read(4)
        return self.traverse(root_id)

    def traverse(self, block_id):
        """
        Traverses a block identified by the given block_id and extracts the file names.
        """
        node = self._DS_Store__block_by_id(block_id)
        next_pointer, = struct.unpack'>I'node.offset_read(4)
        count, = struct.unpack'>I'node.offset_read(4)
        self._log('Next Ptr {} with {} '.formathex(next_pointer)hex(count))
        filenames = []
        if next_pointer > 0:
            for i in range(0, count, 1):
                next_id, = struct.unpack'>I'node.offset_read(4)
                self._log('Child: {}'.format(next_id))
                files = self.traverse(next_id)
                filenames += files
                filename = node.read_filename()
                self._log'Filename: 'filename
                filenames.append(filename)

            files = self.traverse(next_pointer)
            filenames += files
        else:
            for i in range(0, count, 1):
                f = node.read_filename()
                filenames.append(f)

        return filenames