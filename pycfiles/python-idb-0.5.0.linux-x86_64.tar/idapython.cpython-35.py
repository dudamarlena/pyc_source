# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/env/lib/python3.5/site-packages/idb/idapython.py
# Compiled at: 2018-07-30 13:22:01
# Size of source mod 2**32: 58784 bytes
import re, logging, weakref, functools, collections, six, idb.netnode, idb.analysis
logger = logging.getLogger(__name__)

def memoized_method(*lru_args, **lru_kwargs):

    def decorator(func):

        @functools.wraps(func)
        def wrapped_func(self, *args, **kwargs):
            self_weak = weakref.ref(self)

            @functools.wraps(func)
            @functools.lru_cache(*lru_args, **lru_kwargs)
            def cached_method(*args, **kwargs):
                return func(self_weak(), *args, **kwargs)

            setattr(self, func.__name__, cached_method)
            return cached_method(*args, **kwargs)

        return wrapped_func

    return decorator


def is_flag_set(flags, flag):
    return flags & flag == flag


class FLAGS:
    OPND_OUTER = 128
    OPND_MASK = 7
    OPND_ALL = OPND_MASK
    MS_CLS = 1536
    FF_CODE = 1536
    FF_DATA = 1024
    FF_TAIL = 512
    FF_UNK = 0
    MS_COMM = 1046528
    FF_COMM = 2048
    FF_REF = 4096
    FF_LINE = 8192
    FF_NAME = 16384
    FF_LABL = 32768
    FF_FLOW = 65536
    FF_SIGN = 131072
    FF_BNOT = 262144
    FF_VAR = 524288
    MS_0TYPE = 15728640
    FF_0VOID = 0
    FF_0NUMH = 1048576
    FF_0NUMD = 2097152
    FF_0CHAR = 3145728
    FF_0SEG = 4194304
    FF_0OFF = 5242880
    FF_0NUMB = 6291456
    FF_0NUMO = 7340032
    FF_0ENUM = 8388608
    FF_0FOP = 9437184
    FF_0STRO = 10485760
    FF_0STK = 11534336
    FF_0FLT = 12582912
    FF_0CUST = 13631488
    MS_1TYPE = 251658240
    FF_1VOID = 0
    FF_1NUMH = 16777216
    FF_1NUMD = 33554432
    FF_1CHAR = 50331648
    FF_1SEG = 67108864
    FF_1OFF = 83886080
    FF_1NUMB = 100663296
    FF_1NUMO = 117440512
    FF_1ENUM = 134217728
    FF_1FOP = 150994944
    FF_1STRO = 167772160
    FF_1STK = 184549376
    FF_1FLT = 201326592
    FF_1CUST = 218103808
    MS_CODE = 4026531840
    FF_FUNC = 268435456
    FF_IMMD = 1073741824
    FF_JUMP = 2147483648
    DT_TYPE = 4026531840
    FF_BYTE = 0
    FF_WORD = 268435456
    FF_DWRD = 536870912
    FF_QWRD = 805306368
    FF_TBYT = 1073741824
    FF_ASCI = 1342177280
    FF_STRU = 1610612736
    FF_OWRD = 1879048192
    FF_FLOAT = 2147483648
    FF_DOUBLE = 2415919104
    FF_PACKREAL = 2684354560
    FF_ALIGN = 2952790016
    FF_3BYTE = 3221225472
    FF_CUSTOM = 3489660928
    FF_YWRD = 3758096384
    MS_VAL = 255
    FF_IVL = 256


class AFLAGS:
    AFL_LINNUM = 1
    AFL_USERSP = 2
    AFL_PUBNAM = 4
    AFL_WEAKNAM = 8
    AFL_HIDDEN = 16
    AFL_MANUAL = 32
    AFL_NOBRD = 64
    AFL_ZSTROFF = 128
    AFL_BNOT0 = 256
    AFL_BNOT1 = 512
    AFL_LIB = 1024
    AFL_TI = 2048
    AFL_TI0 = 4096
    AFL_TI1 = 8192
    AFL_LNAME = 16384
    AFL_TILCMT = 32768
    AFL_LZERO0 = 65536
    AFL_LZERO1 = 131072
    AFL_COLORED = 262144
    AFL_TERSESTR = 524288
    AFL_SIGN0 = 1048576
    AFL_SIGN1 = 2097152
    AFL_NORET = 4194304
    AFL_FIXEDSPD = 8388608
    AFL_ALIGNFLOW = 16777216
    AFL_USERTI = 33554432
    AFL_RETFP = 67108864
    AFL_USEMODSP = 134217728
    AFL_NOTCODE = 268435456


class ida_netnode:

    def __init__(self, db, api):
        self.idb = db
        self.api = api

    def netnode(self, *args, **kwargs):
        return idb.netnode.Netnode(self.idb, *args, **kwargs)


class idc:
    SEGPERM_EXEC = 1
    SEGPERM_WRITE = 2
    SEGPERM_READ = 4
    SEGPERM_MAXVAL = 7
    SFL_COMORG = 1
    SFL_OBOK = 2
    SFL_HIDDEN = 4
    SFL_DEBUG = 8
    SFL_LOADER = 16
    SFL_HIDETYPE = 32

    def __init__(self, db, api):
        self.idb = db
        self.api = api
        self.bit_dis = None
        self.seg_dis = None
        if self.idb.wordsize == 4:
            self.FUNCATTR_START = 0
            self.FUNCATTR_END = 4
            self.FUNCATTR_FLAGS = 8
            self.FUNCATTR_FRAME = 10
            self.FUNCATTR_FRSIZE = 14
            self.FUNCATTR_FRREGS = 18
            self.FUNCATTR_ARGSIZE = 20
            self.FUNCATTR_FPD = 24
            self.FUNCATTR_COLOR = 28
            self.SEGATTR_START = 0
            self.SEGATTR_END = 4
            self.SEGATTR_ORGBASE = 16
            self.SEGATTR_ALIGN = 20
            self.SEGATTR_COMB = 21
            self.SEGATTR_PERM = 22
            self.SEGATTR_BITNESS = 23
            self.SEGATTR_FLAGS = 24
            self.SEGATTR_SEL = 28
            self.SEGATTR_ES = 32
            self.SEGATTR_CS = 36
            self.SEGATTR_SS = 40
            self.SEGATTR_DS = 44
            self.SEGATTR_FS = 48
            self.SEGATTR_GS = 52
            self.SEGATTR_TYPE = 96
            self.SEGATTR_COLOR = 100
            self.BADADDR = 4294967295
        else:
            if self.idb.wordsize == 8:
                self.FUNCATTR_START = 0
                self.FUNCATTR_END = 8
                self.FUNCATTR_FLAGS = 16
                self.FUNCATTR_FRAME = 18
                self.FUNCATTR_FRSIZE = 26
                self.FUNCATTR_FRREGS = 34
                self.FUNCATTR_ARGSIZE = 36
                self.FUNCATTR_FPD = 44
                self.FUNCATTR_COLOR = 52
                self.FUNCATTR_OWNER = 18
                self.FUNCATTR_REFQTY = 26
                self.SEGATTR_START = 0
                self.SEGATTR_END = 8
                self.SEGATTR_ORGBASE = 32
                self.SEGATTR_ALIGN = 40
                self.SEGATTR_COMB = 41
                self.SEGATTR_PERM = 42
                self.SEGATTR_BITNESS = 43
                self.SEGATTR_FLAGS = 44
                self.SEGATTR_SEL = 48
                self.SEGATTR_ES = 56
                self.SEGATTR_CS = 64
                self.SEGATTR_SS = 72
                self.SEGATTR_DS = 80
                self.SEGATTR_FS = 88
                self.SEGATTR_GS = 96
                self.SEGATTR_TYPE = 184
                self.SEGATTR_COLOR = 188
                self.BADADDR = 18446744073709551615
            else:
                raise RuntimeError('unexpected wordsize')

    def ScreenEA(self):
        return self.api.ScreenEA

    def _get_segment(self, ea):
        segs = idb.analysis.Segments(self.idb).segments
        for seg in segs.values():
            if seg.startEA <= ea < seg.endEA:
                return seg

    def SegStart(self, ea):
        return self._get_segment(ea).startEA

    def SegEnd(self, ea):
        return self._get_segment(ea).endEA

    def FirstSeg(self):
        segs = idb.analysis.Segments(self.idb).segments
        for startEA in sorted(segs.keys()):
            return startEA

    def NextSeg(self, ea):
        segs = idb.analysis.Segments(self.idb).segments.values()
        segs = sorted(segs, key=lambda s: s.startEA)
        for i, seg in enumerate(segs):
            if seg.startEA <= ea < seg.endEA:
                if i < len(segs) - 1:
                    return segs[(i + 1)].startEA
                else:
                    return self.BADADDR

    def SegName(self, ea):
        segstrings = idb.analysis.SegStrings(self.idb).strings
        return segstrings[self._get_segment(ea).name_index]

    def GetSegmentAttr(self, ea, attr):
        if attr == self.SEGATTR_START:
            return self.SegStart(ea)
        if attr == self.SEGATTR_END:
            return self.SegEnd(ea)
        if attr == self.SEGATTR_ORGBASE:
            return self._get_segment(ea).orgbase
        if attr == self.SEGATTR_ALIGN:
            return self._get_segment(ea).align
        if attr == self.SEGATTR_COMB:
            return self._get_segment(ea).comb
        if attr == self.SEGATTR_PERM:
            return self._get_segment(ea).perm
        if attr == self.SEGATTR_BITNESS:
            return self._get_segment(ea).bitness
        if attr == self.SEGATTR_FLAGS:
            return self._get_segment(ea).flags
        if attr == self.SEGATTR_TYPE:
            return self._get_segment(ea).type
        if attr == self.SEGATTR_COLOR:
            return self._get_segment(ea).color
        raise NotImplementedError('segment attribute %d not yet implemented' % attr)

    def MinEA(self):
        segs = idb.analysis.Segments(self.idb).segments.values()
        segs = list(sorted(segs, key=lambda s: s.startEA))
        return segs[0].startEA

    def MaxEA(self):
        segs = idb.analysis.Segments(self.idb).segments.values()
        segs = list(sorted(segs, key=lambda s: s.startEA))
        return segs[(-1)].endEA

    def GetFlags(self, ea):
        try:
            return self.idb.id1.get_flags(ea)
        except KeyError:
            return 0

    def IdbByte(self, ea):
        flags = self.GetFlags(ea)
        if self.hasValue(flags):
            return flags & FLAGS.MS_VAL
        raise KeyError(ea)

    def Head(self, ea):
        flags = self.GetFlags(ea)
        while not self.api.ida_bytes.is_head(flags):
            ea -= 1
            flags = self.GetFlags(ea)

        return ea

    def ItemSize(self, ea):
        oea = ea
        flags = self.GetFlags(ea)
        if not self.api.ida_bytes.is_head(flags):
            raise ValueError('ItemSize must only be called on a head address.')
        ea += 1
        flags = self.GetFlags(ea)
        while flags is not None and not self.api.ida_bytes.is_head(flags):
            ea += 1
            flags = self.GetFlags(ea)

        return ea - oea

    def NextHead(self, ea):
        ea += 1
        flags = self.GetFlags(ea)
        while flags is not None and not self.api.ida_bytes.is_head(flags):
            ea += 1
            flags = self.GetFlags(ea)

        return ea

    def PrevHead(self, ea):
        ea = self.Head(ea)
        ea -= 1
        return self.Head(ea)

    def GetManyBytes(self, ea, size, use_dbg=False):
        """
        Raises:
          IndexError: if the range extends beyond a segment.
          KeyError: if a byte is not defined.
        """
        if use_dbg:
            raise NotImplementedError()
        if self.SegStart(ea) != self.SegStart(ea + size):
            if ea + size == self.SegEnd(ea):
                pass
            else:
                raise IndexError((ea, ea + size))
            ret = []
            try:
                for i in range(ea, ea + size):
                    ret.append(self.IdbByte(i))

            except KeyError:
                ret.extend([0 for _ in range(size - len(ret))])

            if six.PY2:
                pass
            return ''.join(map(chr, ret))
        else:
            return bytes(ret)

    def _load_dis(self, arch, mode):
        import capstone
        if self.bit_dis is None:
            self.bit_dis = {}
        if self.bit_dis.get((arch, mode)) is None:
            r = capstone.Cs(arch, mode)
            self.bit_dis[(arch, mode)] = r
        return self.bit_dis[(arch, mode)]

    def _disassemble(self, ea):
        import capstone
        size = self.ItemSize(ea)
        inst_buf = self.GetManyBytes(ea, size)
        segment = self._get_segment(ea)
        bitness = 16 << segment.bitness
        procname = self.api.idaapi.get_inf_structure().procname.lower()
        dis = None
        if procname == 'arm' and bitness == 64:
            dis = self._load_dis(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
        else:
            if procname == 'arm' and bitness == 32:
                if size == 2:
                    dis = self._load_dis(capstone.CS_ARCH_ARM, capstone.CS_MODE_THUMB)
                else:
                    dis = self._load_dis(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
            else:
                if procname in ('metapc', '8086', '80286r', '80286p', '80386r', '80386p',
                                '80486r', '80486p', '80586r', '80586p', '80686p',
                                'k62', 'p2', 'p3', 'athlon', 'p4', '8085'):
                    if bitness == 16:
                        dis = self._load_dis(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
                    else:
                        if bitness == 32:
                            dis = self._load_dis(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
                        elif bitness == 64:
                            dis = self._load_dis(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
                else:
                    if procname == 'mipsb':
                        if bitness == 32:
                            dis = self._load_dis(capstone.CS_ARCH_MIPS, capstone.CS_MODE_MIPS32 | capstone.CS_MODE_BIG_ENDIAN)
                        elif bitness == 64:
                            dis = self._load_dis(capstone.CS_ARCH_MIPS, capstone.CS_MODE_MIPS64 | capstone.CS_MODE_BIG_ENDIAN)
                    elif procname == 'mipsl':
                        if bitness == 32:
                            dis = self._load_dis(capstone.CS_ARCH_MIPS, capstone.CS_MODE_MIPS32 | capstone.CS_MODE_LITTLE_ENDIAN)
        if bitness == 64:
            dis = self._load_dis(capstone.CS_ARCH_MIPS, capstone.CS_MODE_MIPS64 | capstone.CS_MODE_LITTLE_ENDIAN)
        if dis is None:
            raise NotImplementedError('unknown arch %s bit:%s inst_len:%d' % (procname, bitness, len(inst_buf)))
        dis.detail = True
        try:
            op = next(dis.disasm(inst_buf, ea))
        except StopIteration:
            raise RuntimeError('failed to disassemble %s' % hex(ea))
        else:
            return op

    def GetMnem(self, ea):
        op = self._disassemble(ea)
        return op.mnemonic

    def GetDisasm(self, ea):
        op = self._disassemble(ea)
        return '%s\t%s' % (op.mnemonic, op.op_str)

    CIC_ITEM = 1
    CIC_FUNC = 2
    CIC_SEGM = 3
    DEFCOLOR = 4294967295

    def GetColor(self, ea, what):
        """
        Args:
          ea (int): effective address of thing.
          what (int): one of:
            - idc.CIC_ITEM
            - idc.CIC_FUNC
            - idc.CIC_SEGM

        Returns:
          int: the color in RGB. possibly idc.DEFCOLOR if not set.
        """
        if what != idc.CIC_ITEM:
            raise NotImplementedError()
        if not self.api.ida_nalt.is_colored_item(ea):
            return idc.DEFCOLOR
        nn = self.api.ida_netnode.netnode(ea)
        try:
            return nn.altval(tag='A', index=20) - 1
        except KeyError:
            return idc.DEFCOLOR

    def GetFunctionFlags(self, ea):
        func = self.api.ida_funcs.get_func(ea)
        return func.flags

    def GetFunctionAttr(self, ea, attr):
        func = self.api.ida_funcs.get_func(ea)
        if attr == self.FUNCATTR_START:
            return func.startEA
        if attr == self.FUNCATTR_END:
            return func.endEA
        if attr == self.FUNCATTR_FLAGS:
            return func.flags
        if attr == self.FUNCATTR_FRAME:
            return func.frame
        if attr == self.FUNCATTR_FRSIZE:
            return func.frsize
        if attr == self.FUNCATTR_FRREGS:
            return func.frregs
        if attr == self.FUNCATTR_ARGSIZE:
            return func.argsize
        if attr == self.FUNCATTR_FPD:
            return func.fpd
        if attr == self.FUNCATTR_COLOR:
            return func.color
        raise ValueError('unknown attr: %x' % attr)

    def GetFunctionName(self, ea):
        return self.api.ida_funcs.get_func_name(ea)

    def LocByName(self, name):
        try:
            key = ('N' + name).encode('utf-8')
            cursor = self.idb.id0.find(key)
            return idb.netnode.as_uint(cursor.value)
        except KeyError:
            return -1

    def GetInputMD5(self):
        return idb.analysis.Root(self.idb).md5

    def Comment(self, ea):
        return self.api.ida_bytes.get_cmt(ea, False)

    def RptCmt(self, ea):
        return self.api.ida_bytes.get_cmt(ea, True)

    def GetCommentEx(self, ea, repeatable):
        return self.api.ida_bytes.get_cmt(ea, repeatable)

    def GetType(self, ea):
        try:
            f = idb.analysis.Function(self.idb, ea)
        except Exception as e:
            logger.warning('failed to fetch function for GetType: %s', e)
            return

        try:
            name = f.get_name()
            sig = f.get_signature()
        except KeyError:
            return

        params = []
        for param in sig.parameters:
            params.append('%s %s' % (param.type, param.name))

        return '{rtype:s} {cc:s} {name:s}({params:s})'.format(rtype=sig.rtype, cc=sig.calling_convention, name=name, params=', '.join(params))

    @staticmethod
    def hasValue(flags):
        return flags & FLAGS.FF_IVL > 0

    @staticmethod
    def isDefArg0(flags):
        return flags & FLAGS.MS_0TYPE > 0

    @staticmethod
    def isDefArg1(flags):
        return flags & FLAGS.MS_1TYPE > 0

    @staticmethod
    def isOff0(flags):
        return flags & FLAGS.MS_0TYPE == FLAGS.FF_0CUST

    @staticmethod
    def isOff1(flags):
        return flags & FLAGS.MS_1TYPE == FLAGS.FF_1CUST

    @staticmethod
    def isChar0(flags):
        return flags & FLAGS.MS_0TYPE == FLAGS.FF_0CHAR

    @staticmethod
    def isChar1(flags):
        return flags & FLAGS.MS_1TYPE == FLAGS.FF_1CHAR

    @staticmethod
    def isSeg0(flags):
        return flags & FLAGS.MS_0TYPE == FLAGS.FF_0SEG

    @staticmethod
    def isSeg1(flags):
        return flags & FLAGS.MS_1TYPE == FLAGS.FF_1SEG

    @staticmethod
    def isEnum0(flags):
        return flags & FLAGS.MS_0TYPE == FLAGS.FF_0ENUM

    @staticmethod
    def isEnum1(flags):
        return flags & FLAGS.MS_1TYPE == FLAGS.FF_1ENUM

    @staticmethod
    def isStroff0(flags):
        return flags & FLAGS.MS_0TYPE == FLAGS.FF_0STRO

    @staticmethod
    def isStroff1(flags):
        return flags & FLAGS.MS_1TYPE == FLAGS.FF_1STRO

    @staticmethod
    def isStkvar0(flags):
        return flags & FLAGS.MS_0TYPE == FLAGS.FF_0STK

    @staticmethod
    def isStkvar1(flags):
        return flags & FLAGS.MS_1TYPE == FLAGS.FF_1STK

    @staticmethod
    def isFloat0(flags):
        return flags & FLAGS.MS_0TYPE == FLAGS.FF_0FLT

    @staticmethod
    def isFloat1(flags):
        return flags & FLAGS.MS_1TYPE == FLAGS.FF_1FLT

    @staticmethod
    def isCustFmt0(flags):
        return flags & FLAGS.MS_0TYPE == FLAGS.FF_0CUST

    @staticmethod
    def isCustFmt1(flags):
        return flags & FLAGS.MS_1TYPE == FLAGS.FF_1CUST

    @staticmethod
    def isNum0(flags):
        t = flags & FLAGS.MS_0TYPE
        return t == FLAGS.FF_0NUMB or t == FLAGS.FF_0NUMO or t == FLAGS.FF_0NUMD or t == FLAGS.FF_0NUMH

    @staticmethod
    def isNum1(flags):
        t = flags & FLAGS.MS_1TYPE
        return t == FLAGS.FF_1NUMB or t == FLAGS.FF_1NUMO or t == FLAGS.FF_1NUMD or t == FLAGS.FF_1NUMH

    @staticmethod
    def get_optype_flags0(flags):
        return flags & FLAGS.MS_0TYPE

    @staticmethod
    def get_optype_flags1(flags):
        return flags & FLAGS.MS_1TYPE

    def LineA(self, ea, num):
        nn = self.api.ida_netnode.netnode(ea)
        try:
            return nn.supstr(tag='S', index=1000 + num)
        except KeyError:
            return ''

    def LineB(self, ea, num):
        nn = self.api.ida_netnode.netnode(ea)
        try:
            return nn.supstr(tag='S', index=2000 + num)
        except KeyError:
            return ''


class ida_bytes:

    def __init__(self, db, api):
        self.idb = db
        self.api = api

    def get_cmt(self, ea, repeatable):
        flags = self.api.idc.GetFlags(ea)
        if not self.has_cmt(flags):
            return ''
        try:
            nn = self.api.ida_netnode.netnode(ea)
            if repeatable:
                return nn.supstr(tag='S', index=1)
            else:
                return nn.supstr(tag='S', index=0)
        except KeyError:
            return ''

    def get_flags(self, ea):
        return self.api.idc.GetFlags(ea)

    @staticmethod
    def is_func(flags):
        return flags & FLAGS.MS_CODE == FLAGS.FF_FUNC

    @staticmethod
    def has_immd(flags):
        return flags & FLAGS.MS_CODE == FLAGS.FF_IMMD

    @staticmethod
    def is_code(flags):
        return flags & FLAGS.MS_CLS == FLAGS.FF_CODE

    @staticmethod
    def is_data(flags):
        return flags & FLAGS.MS_CLS == FLAGS.FF_DATA

    @staticmethod
    def is_tail(flags):
        return flags & FLAGS.MS_CLS == FLAGS.FF_TAIL

    @staticmethod
    def is_not_tail(flags):
        return not ida_bytes.is_tail(flags)

    @staticmethod
    def is_unknown(flags):
        return flags & FLAGS.MS_CLS == FLAGS.FF_UNK

    @staticmethod
    def is_head(flags):
        return ida_bytes.is_code(flags) or ida_bytes.is_data(flags)

    @staticmethod
    def is_flow(flags):
        return flags & FLAGS.MS_COMM & FLAGS.FF_FLOW > 0

    @staticmethod
    def is_var(flags):
        return flags & FLAGS.MS_COMM & FLAGS.FF_VAR > 0

    @staticmethod
    def has_extra_cmts(flags):
        return flags & FLAGS.MS_COMM & FLAGS.FF_LINE > 0

    @staticmethod
    def has_cmt(flags):
        return flags & FLAGS.MS_COMM & FLAGS.FF_COMM > 0

    @staticmethod
    def has_ref(flags):
        return flags & FLAGS.MS_COMM & FLAGS.FF_REF > 0

    @staticmethod
    def has_name(flags):
        return flags & FLAGS.MS_COMM & FLAGS.FF_NAME > 0

    @staticmethod
    def has_dummy_name(flags):
        return flags & FLAGS.MS_COMM & FLAGS.FF_LABL > 0

    @staticmethod
    def has_auto_name(flags):
        raise NotImplementedError()

    @staticmethod
    def has_any_name(flags):
        raise NotImplementedError()

    @staticmethod
    def has_user_name(flags):
        raise NotImplementedError()

    @staticmethod
    def is_invsign(flags):
        return flags & FLAGS.MS_COMM & FLAGS.FF_SIGN > 0

    @staticmethod
    def is_bnot(flags):
        return flags & FLAGS.MS_COMM & FLAGS.FF_BNOT > 0

    @staticmethod
    def has_value(flags):
        return flags & FLAGS.FF_IVL > 0

    @staticmethod
    def is_byte(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_BYTE

    @staticmethod
    def is_word(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_WORD

    @staticmethod
    def is_dword(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_DWRD

    @staticmethod
    def is_qword(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_QWRD

    @staticmethod
    def is_oword(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_OWRD

    @staticmethod
    def is_yword(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_YWRD

    @staticmethod
    def is_tbyte(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_TBYT

    @staticmethod
    def is_float(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_FLOAT

    @staticmethod
    def is_double(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_DOUBLE

    @staticmethod
    def is_pack_real(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_PACKREAL

    @staticmethod
    def is_strlit(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_ASCI

    @staticmethod
    def is_struct(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_STRU

    @staticmethod
    def is_align(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_ALIGN

    @staticmethod
    def is_custom(flags):
        return flags & FLAGS.DT_TYPE == FLAGS.FF_CUSTOM

    def get_bytes(self, ea, count):
        return self.api.idc.GetManyBytes(ea, count)

    def next_that(self, ea, maxea, testf):
        for i in range(ea + 1, maxea):
            flags = self.get_flags(i)
            if testf(flags):
                return i

        return self.api.idc.BADADDR

    def next_not_tail(self, ea):
        while 1:
            ea += 1
            flags = self.get_flags(ea)
            if not self.is_tail(flags):
                break

        return ea

    def next_inited(self, ea, maxea):
        return self.next_that(ea, maxea, lambda flags: ida_bytes.has_value(flags))


class ida_nalt:

    def __init__(self, db, api):
        self.idb = db
        self.api = api

    def get_aflags(self, ea):
        nn = self.api.ida_netnode.netnode(ea)
        try:
            return nn.altval(tag='A', index=8)
        except KeyError:
            return 0

    def is_hidden_item(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_HIDDEN)

    def is_hidden_border(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_NOBRD)

    def uses_modsp(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_USEMODSP)

    def is_zstroff(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_ZSTROFF)

    def is__bnot0(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_BNOT0)

    def is__bnot1(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_BNOT1)

    def is_libitem(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_LIB)

    def has_ti(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_TI)

    def has_ti0(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_TI0)

    def has_ti1(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_TI1)

    def has_lname(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_LNAME)

    def is_tilcmt(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_TILCMT)

    def is_usersp(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_USERSP)

    def is_lzero0(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_LZERO0)

    def is_lzero1(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_LZERO1)

    def is_colored_item(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_COLORED)

    def is_terse_struc(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_TERSESTR)

    def is__invsign0(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_SIGN0)

    def is__invsign1(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_SIGN1)

    def is_noret(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_NORET)

    def is_fixed_spd(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_FIXEDSPD)

    def is_align_flow(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_ALIGNFLOW)

    def is_userti(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_USERTI)

    def is_retfp(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_RETFP)

    def is_notcode(self, ea):
        return is_flag_set(self.get_aflags(ea), AFLAGS.AFL_NOTCODE)

    def get_import_module_qty(self):
        return max(idb.analysis.Imports(self.idb).lib_names.keys())

    def get_import_module_name(self, mod_index):
        return idb.analysis.Imports(self.idb).lib_names[mod_index]

    def enum_import_names(self, mod_index, py_cb):
        imps = idb.analysis.Imports(self.idb)
        nnref = imps.lib_netnodes[mod_index]
        nn = idb.netnode.Netnode(self.idb, nnref)
        for funcaddr in nn.sups():
            funcname = nn.supstr(funcaddr)
            if not py_cb(funcaddr, funcname, None):
                return

    def get_imagebase(self):
        try:
            return idb.analysis.Root(self.idb).imagebase
        except KeyError:
            return 0


class ida_funcs:
    FUNC_NORET = 1
    FUNC_FAR = 2
    FUNC_LIB = 4
    FUNC_STATICDEF = 8
    FUNC_FRAME = 16
    FUNC_USERFAR = 32
    FUNC_HIDDEN = 64
    FUNC_THUNK = 128
    FUNC_BOTTOMBP = 256
    FUNC_NORET_PENDING = 512
    FUNC_SP_READY = 1024
    FUNC_PURGED_OK = 16384
    FUNC_TAIL = 32768

    def __init__(self, db, api):
        self.idb = db
        self.api = api

    def get_func(self, ea):
        """
        get the func_t associated with the given address.
        if the address is not the start of a function (or function tail), then searches
         for a function that contains the given address.
        note: the range search is pretty slow, since we parse everything on-demand.
        """
        nn = self.api.ida_netnode.netnode('$ funcs')
        try:
            v = nn.supval(tag='S', index=ea)
        except KeyError:
            for func in idb.analysis.Functions(self.idb).functions.values():
                if not func.startEA <= ea < func.endEA:
                    pass
                else:
                    if is_flag_set(func.flags, self.FUNC_TAIL):
                        return self.get_func(func.owner)
                    else:
                        return func

            return
        else:
            func = idb.analysis.func_t(v, wordsize=self.idb.wordsize)
            if is_flag_set(func.flags, self.FUNC_TAIL):
                return self.get_func(func.owner)
            else:
                return func

    def get_func_cmt(self, ea, repeatable):
        func = self.get_func(ea)
        if func is None:
            return ''
        nn = self.api.ida_netnode.netnode('$ funcs')
        try:
            if repeatable:
                tag = 'R'
            else:
                tag = 'C'
            return nn.supstr(tag=tag, index=func.startEA)
        except KeyError:
            return ''

    def get_func_name(self, ea):
        func = self.get_func(ea)
        if func.startEA != ea:
            raise KeyError(ea)
        if is_flag_set(func.flags, func.FUNC_TAIL):
            raise KeyError(ea)
        nn = self.api.ida_netnode.netnode(ea)
        try:
            return nn.name()
        except:
            if self.idb.wordsize == 4:
                return 'sub_%04x' % ea
            if self.idb.wordsize == 8:
                return 'sub_%08x' % ea
            raise RuntimeError('unexpected wordsize')


class BasicBlock(object):
    __doc__ = '\n    interface extracted from: https://raw.githubusercontent.com/gabtremblay/idabearclean/master/idaapi.py\n    '

    def __init__(self, flowchart, startEA, lastInstEA, endEA):
        self.fc = flowchart
        self.id = startEA
        self.startEA = startEA
        self.lastInstEA = lastInstEA
        self.endEA = endEA
        self.type = NotImplementedError()

    def preds(self):
        for pred in self.fc.preds[self.startEA]:
            yield self.fc.bbs[pred]

    def succs(self):
        for succ in self.fc.succs[self.startEA]:
            yield self.fc.bbs[succ]

    def __str__(self):
        return 'BasicBlock(startEA: 0x%x, endEA: 0x%x)' % (self.startEA, self.endEA)


def is_empty(s):
    for c in s:
        return False

    return True


class idaapi:
    fl_U = 0
    fl_CF = 16
    fl_CN = 17
    fl_JF = 18
    fl_JN = 19
    fl_USobsolete = 20
    fl_F = 21
    dr_U = 0
    dr_O = 1
    dr_W = 2
    dr_R = 3
    dr_T = 4
    dr_I = 5

    def __init__(self, db, api):
        self.idb = db
        self.api = api

    def _find_bb_end(self, ea):
        """
        Args:
          ea (int): address at which a basic block begins. behavior undefined if its not a block start.

        Returns:
          int: the address of the final instruction in the basic block. it may be the same as the start.
        """
        if not is_empty(idb.analysis.get_crefs_from(self.idb, ea, types=[
         idaapi.fl_JN, idaapi.fl_JF, idaapi.fl_F])):
            return ea
        while 1:
            last_ea = ea
            ea = self.api.idc.NextHead(ea)
            flags = self.api.idc.GetFlags(ea)
            if flags == 0:
                return last_ea
            if self.api.ida_bytes.has_ref(flags):
                return last_ea
            if self.api.ida_bytes.is_func(flags):
                return last_ea
            if not self.api.ida_bytes.is_flow(flags):
                return last_ea
            if not is_empty(idb.analysis.get_crefs_from(self.idb, ea, types=[
             idaapi.fl_JN, idaapi.fl_JF, idaapi.fl_F])):
                return ea

    def _find_bb_start(self, ea):
        """
        Args:
          ea (int): address at which a basic block ends. behavior undefined if its not a block end.

        Returns:
          int: the address of the first instruction in the basic block. it may be the same as the end.
        """
        while 1:
            flags = self.api.idc.GetFlags(ea)
            if self.api.ida_bytes.has_ref(flags):
                return ea
            if self.api.ida_bytes.is_func(flags):
                return ea
            last_ea = ea
            ea = self.api.idc.PrevHead(ea)
            if not is_empty(idb.analysis.get_crefs_from(self.idb, ea, types=[
             idaapi.fl_JN, idaapi.fl_JF, idaapi.fl_F])):
                return last_ea
            if not self.api.ida_bytes.is_flow(flags):
                return last_ea

    def _get_flow_preds(self, ea):
        flags = self.api.idc.GetFlags(ea)
        if flags is not None and self.api.ida_bytes.is_flow(flags):
            yield idb.analysis.Xref(self.api.idc.PrevHead(ea), ea, idaapi.fl_F)
        for xref in idb.analysis.get_crefs_to(self.idb, ea, types=[
         idaapi.fl_JN, idaapi.fl_JF, idaapi.fl_F]):
            yield xref

    def _get_flow_succs(self, ea):
        nextea = self.api.idc.NextHead(ea)
        nextflags = self.api.idc.GetFlags(nextea)
        if nextflags is not None and self.api.ida_bytes.is_flow(nextflags):
            yield idb.analysis.Xref(ea, nextea, idaapi.fl_F)
        for xref in idb.analysis.get_crefs_from(self.idb, ea, types=[
         idaapi.fl_JN, idaapi.fl_JF, idaapi.fl_F]):
            yield xref

    def FlowChart(self, func):
        """
        Example::

            f = idaapi.FlowChart(idaapi.get_func(here()))
            for block in f:
                if p:
                    print "%x - %x [%d]:" % (block.startEA, block.endEA, block.id)
                for succ_block in block.succs():
                    if p:
                        print "  %x - %x [%d]:" % (succ_block.startEA, succ_block.endEA, succ_block.id)

                for pred_block in block.preds():
                    if p:
                        print "  %x - %x [%d]:" % (pred_block.startEA, pred_block.endEA, pred_block.id)

        via: https://github.com/EiNSTeiN-/idapython/blob/master/examples/ex_gdl_qflow_chart.py
        """

        class _FlowChart:

            def __init__(self, db, api, ea):
                self.idb = db
                logger.debug('creating flowchart for %x', ea)
                seen = set([])
                bbs_by_start = {}
                bbs_by_end = {}
                preds = collections.defaultdict(lambda : set([]))
                succs = collections.defaultdict(lambda : set([]))
                lastInstEA = api.idaapi._find_bb_end(ea)
                logger.debug('found end. %x -> %x', ea, lastInstEA)
                block = BasicBlock(self, ea, lastInstEA, api.idc.NextHead(lastInstEA))
                bbs_by_start[ea] = block
                bbs_by_end[lastInstEA] = block
                q = [
                 block]
                while q:
                    logger.debug('iteration')
                    logger.debug('queue: [%s]', ', '.join(map(str, q)))
                    block = q[0]
                    q = q[1:]
                    logger.debug('exploring %s', block)
                    if block.startEA in seen:
                        logger.debug('already seen!')
                        continue
                        logger.debug('new!')
                        seen.add(block.startEA)
                        for xref in api.idaapi._get_flow_preds(block.startEA):
                            if xref.src not in bbs_by_end:
                                pred_start = api.idaapi._find_bb_start(xref.src)
                                pred = BasicBlock(self, pred_start, xref.src, api.idc.NextHead(xref.src))
                                bbs_by_start[pred.startEA] = pred
                                bbs_by_end[pred.lastInstEA] = pred
                            else:
                                pred = bbs_by_end[xref.src]
                            logger.debug('pred: %s', pred)
                            preds[block.startEA].add(pred.startEA)
                            succs[pred.startEA].add(block.startEA)
                            q.append(pred)

                        for xref in api.idaapi._get_flow_succs(block.lastInstEA):
                            if xref.dst not in bbs_by_start:
                                succ_end = api.idaapi._find_bb_end(xref.dst)
                                succ = BasicBlock(self, xref.dst, succ_end, api.idc.NextHead(succ_end))
                                bbs_by_start[succ.startEA] = succ
                                bbs_by_end[succ.lastInstEA] = succ
                            else:
                                succ = bbs_by_start[xref.dst]
                            logger.debug('succ: %s', succ)
                            succs[block.startEA].add(succ.startEA)
                            preds[succ.startEA].add(block.startEA)
                            q.append(succ)

                self.preds = preds
                self.succs = succs
                self.bbs = bbs_by_start

            def __iter__(self):
                for bb in self.bbs.values():
                    yield bb

        return _FlowChart(self.idb, self.api, func.startEA)

    def get_next_fixup_ea(self, ea):
        nn = self.api.ida_netnode.netnode('$ fixups')
        for index in nn.sups(tag='S'):
            if ea <= index:
                return index

        raise KeyError(ea)

    def contains_fixups(self, ea, size):
        try:
            next_fixup = self.get_next_fixup_ea(ea)
        except KeyError:
            return False
        else:
            if next_fixup < ea + size:
                return True
            else:
                return False

    def getseg(self, ea):
        segs = idb.analysis.Segments(self.idb).segments
        for seg in segs.values():
            if seg.startEA <= ea < seg.endEA:
                return seg

    def get_segm_name(self, ea):
        return self.api.idc.SegName(ea)

    def get_segm_end(self, ea):
        return self.api.idc.SegEnd(ea)

    def get_inf_structure(self):
        return idb.analysis.Root(self.idb).idainfo

    def get_imagebase(self):
        return self.api.ida_nalt.get_imagebase()


class StringItem:

    def __init__(self, ea, length, strtype, s):
        self.ea = ea
        self.length = length
        self.strtype = strtype
        self.s = s

    def __str__(self):
        return self.s


class _Strings:
    C = 0
    C_16 = 1
    C_32 = 2
    PASCAL = 4
    PASCAL_16 = 5
    LEN2 = 8
    LEN2_16 = 9
    LEN4 = 12
    LEN4_16 = 13
    ASCII_BYTE = b' !"#\\$%&\'\\(\\)\\*\\+,-\\./0123456789:;<=>\\?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\\[\\]\\^_`abcdefghijklmnopqrstuvwxyz\\{\\|\\}\\\\~\t'

    def __init__(self, db, api):
        self.db = db
        self.api = api
        self.cache = None
        self.strtypes = [
         0]
        self.minlen = 5
        self.only_7bit = True
        self.ignore_instructions = False
        self.display_only_existing_strings = False

    def clear_cache(self):
        self.cache = None

    @memoized_method()
    def get_seg_data(self, seg):
        start = self.api.idc.SegStart(seg)
        end = self.api.idc.SegEnd(start)
        IdbByte = self.api.idc.IdbByte
        get_flags = self.api.ida_bytes.get_flags
        has_value = self.api.ida_bytes.has_value
        data = []
        for i in range(start, end):
            b = IdbByte(i)
            if b == 0:
                flags = get_flags(i)
                if not has_value(flags):
                    break
                data.append(b)

        if six.PY2:
            return ''.join(map(chr, data))
        else:
            return bytes(data)

    def parse_C_strings(self, va, buf):
        reg = b'([%s]{%d,})' % (_Strings.ASCII_BYTE, self.minlen)
        ascii_re = re.compile(reg)
        for match in ascii_re.finditer(buf):
            s = match.group().decode('ascii')
            yield StringItem(va + match.start(), len(s), _Strings.C, s)

    def parse_C_16_strings(self, va, buf):
        reg = b'((?:[%s]\x00){%d,})' % (_Strings.ASCII_BYTE, self.minlen)
        uni_re = re.compile(reg)
        for match in uni_re.finditer(buf):
            try:
                s = match.group().decode('utf-16')
            except UnicodeDecodeError:
                continue
            else:
                yield StringItem(va + match.start(), len(s), _Strings.C_16, s)

    def parse_C_32_strings(self, va, buf):
        reg = b'((?:[%s]\x00\x00\x00){%d,})' % (_Strings.ASCII_BYTE, self.minlen)
        uni_re = re.compile(reg)
        for match in uni_re.finditer(buf):
            try:
                s = match.group().decode('utf-32')
            except UnicodeDecodeError:
                continue
            else:
                yield StringItem(va + match.start(), len(s), _Strings.C_32, s)

    def parse_PASCAL_strings(self, va, buf):
        raise NotImplementedError('parse PASCAL strings')

    def parse_PASCAL_16_strings(self, va, buf):
        raise NotImplementedError('parse PASCAL_16 strings')

    def parse_LEN2_strings(self, va, buf):
        raise NotImplementedError('parse LEN2 strings')

    def parse_LEN2_16_strings(self, va, buf):
        raise NotImplementedError('parse LEN2_16 strings')

    def parse_LEN4_strings(self, va, buf):
        raise NotImplementedError('parse LEN4 strings')

    def parse_LEN4_16_strings(self, va, buf):
        raise NotImplementedError('parse LEN4_16 strings')

    def refresh(self):
        ret = []
        for seg in self.api.idautils.Segments():
            buf = self.get_seg_data(seg)
            for parser in (self.parse_C_strings,
             self.parse_C_16_strings,
             self.parse_C_32_strings,
             self.parse_PASCAL_strings,
             self.parse_PASCAL_16_strings,
             self.parse_LEN2_strings,
             self.parse_LEN2_16_strings,
             self.parse_LEN4_strings,
             self.parse_LEN4_16_strings):
                try:
                    ret.extend(list(parser(seg, buf)))
                except NotImplementedError as e:
                    logger.warning('warning: %s', e)

        self.cache = ret[:]
        return ret

    def setup(self, strtypes=[
 0], minlen=5, only_7bit=True, ignore_instructions=False, display_only_existing_strings=False):
        self.strtypes = strtypes
        self.minlen = minlen
        self.only_7bit = only_7bit
        self.ignore_instructions = ignore_instructions
        self.display_only_existing_strings = display_only_existing_strings

    def __iter__(self):
        if self.cache is None:
            self.refresh()
        for s in self.cache:
            yield s

    def __getitem__(self, index):
        if self.cache is None:
            self.refresh()
        return self.cache[index]


class idautils:

    def __init__(self, db, api):
        self.idb = db
        self.api = api
        self.strings = _Strings(db, api)

    def GetInputFileMD5(self):
        return self.api.idc.GetInputMD5()

    def Segments(self):
        return sorted(idb.analysis.Segments(self.idb).segments.keys())

    def Functions(self):
        ret = []
        for ea, func in idb.analysis.Functions(self.idb).functions.items():
            if is_flag_set(func.flags, func.FUNC_TAIL):
                pass
            else:
                ret.append(func.startEA)

        return list(sorted(ret))

    def CodeRefsTo(self, ea, flow):
        if flow:
            flags = self.api.idc.GetFlags(ea)
            if flags is not None and self.api.ida_bytes.is_flow(flags):
                yield self.api.idc.PrevHead(ea)
            for xref in idb.analysis.get_crefs_to(self.idb, ea, types=[
             idaapi.fl_JN, idaapi.fl_JF, idaapi.fl_F]):
                yield xref.src

    def CodeRefsFrom(self, ea, flow):
        if flow:
            nextea = self.api.idc.NextHead(ea)
            nextflags = self.api.idc.GetFlags(nextea)
            if self.api.ida_bytes.is_flow(nextflags):
                yield nextea
            for xref in idb.analysis.get_crefs_from(self.idb, ea, types=[
             idaapi.fl_JN, idaapi.fl_JF, idaapi.fl_F]):
                yield xref.dst

    def Strings(self, default_setup=False):
        return self.strings


class ida_entry:

    def __init__(self, db, api):
        self.idb = db
        self.api = api

    def get_entry_qty(self):
        ents = idb.analysis.EntryPoints(self.idb)
        return len(ents.functions) + len(ents.main_entry)

    def get_entry_ordinal(self, index):
        ents = idb.analysis.EntryPoints(self.idb)
        try:
            return ents.ordinals[(index + 1)]
        except KeyError:
            return sorted(ents.main_entry)[(index - len(ents.functions) - 1)]

    def get_entry(self, ordinal):
        ents = idb.analysis.EntryPoints(self.idb)
        return ents.functions[ordinal]

    def get_entry_name(self, ordinal):
        ents = idb.analysis.EntryPoints(self.idb)
        try:
            return ents.function_names[ordinal]
        except KeyError:
            return ents.main_entry_name[ordinal]

    def get_entry_forwarder(self, ordinal):
        ents = idb.analysis.EntryPoints(self.idb)
        return ents.forwarded_symbols.get(ordinal)


class ida_name:

    def __init__(self, db, api):
        self.idb = db
        self.api = api

    def get_name(self, ea):
        flags = self.api.ida_bytes.get_flags(ea)
        if not self.api.ida_bytes.has_name(flags):
            return ''
        try:
            nn = self.api.ida_netnode.netnode(ea)
            return nn.name()
        except KeyError:
            return ''


class IDAPython:

    def __init__(self, db, ScreenEA=None):
        self.idb = db
        self.ScreenEA = ScreenEA
        self.idc = idc(db, self)
        self.idaapi = idaapi(db, self)
        self.idautils = idautils(db, self)
        self.ida_funcs = ida_funcs(db, self)
        self.ida_bytes = ida_bytes(db, self)
        self.ida_netnode = ida_netnode(db, self)
        self.ida_nalt = ida_nalt(db, self)
        self.ida_entry = ida_entry(db, self)
        self.ida_name = ida_name(db, self)