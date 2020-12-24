# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\formats\executable\pe32.py
# Compiled at: 2010-05-01 15:45:14
"""
Portable Executable (PE) 32 bit, little endian
Used on MSWindows systems (including DOS) for EXEs and DLLs

1999 paper:
http://download.microsoft.com/download/1/6/1/161ba512-40e2-4cc9-843a-923143f3456c/pecoff.doc

2006 with updates relevant for .NET:
http://download.microsoft.com/download/9/c/5/9c5b2167-8017-4bae-9fde-d599bac8184a/pecoff_v8.doc
"""
from construct import *
import time

class UTCTimeStampAdapter(Adapter):

    def _decode(self, obj, context):
        return time.ctime(obj)

    def _encode(self, obj, context):
        return int(time.mktime(time.strptime(obj)))


def UTCTimeStamp(name):
    return UTCTimeStampAdapter(ULInt32(name))


class NamedSequence(Adapter):
    """
    creates a mapping between the elements of a sequence and their respective
    names. this is useful for sequences of a variable length, where each
    element in the sequence has a name (as is the case with the data 
    directories of the PE header)
    """
    __slots__ = [
     'mapping', 'rev_mapping']
    prefix = 'unnamed_'

    def __init__(self, subcon, mapping):
        Adapter.__init__(self, subcon)
        self.mapping = mapping
        self.rev_mapping = dict((v, k) for (k, v) in mapping.iteritems())

    def _encode(self, obj, context):
        d = obj.__dict__
        obj2 = [None] * len(d)
        for (name, value) in d.iteritems():
            if name in self.rev_mapping:
                index = self.rev_mapping[name]
            elif name.startswith('__'):
                obj2.pop(-1)
                continue
            elif name.startswith(self.prefix):
                index = int(name.split(self.prefix)[1])
            else:
                raise ValueError('no mapping defined for %r' % (name,))
            obj2[index] = value

        return obj2

    def _decode(self, obj, context):
        obj2 = Container()
        for (i, item) in enumerate(obj):
            if i in self.mapping:
                name = self.mapping[i]
            else:
                name = '%s%d' % (self.prefix, i)
            setattr(obj2, name, item)

        return obj2


msdos_header = Struct('msdos_header', Magic('MZ'), ULInt16('partPag'), ULInt16('page_count'), ULInt16('relocation_count'), ULInt16('header_size'), ULInt16('minmem'), ULInt16('maxmem'), ULInt16('relocation_stackseg'), ULInt16('exe_stackptr'), ULInt16('checksum'), ULInt16('exe_ip'), ULInt16('relocation_codeseg'), ULInt16('table_offset'), ULInt16('overlay'), Padding(8), ULInt16('oem_id'), ULInt16('oem_info'), Padding(20), ULInt32('coff_header_pointer'), Anchor('_assembly_start'), OnDemand(HexDumpAdapter(Field('code', lambda ctx: ctx.coff_header_pointer - ctx._assembly_start))))
symbol_table = Struct('symbol_table', String('name', 8, padchar='\x00'), ULInt32('value'), Enum(ExprAdapter(SLInt16('section_number'), encoder=lambda obj, ctx: obj + 1, decoder=lambda obj, ctx: obj - 1), UNDEFINED=-1, ABSOLUTE=-2, DEBUG=-3, _default_=Pass), Enum(ULInt8('complex_type'), NULL=0, POINTER=1, FUNCTION=2, ARRAY=3), Enum(ULInt8('base_type'), NULL=0, VOID=1, CHAR=2, SHORT=3, INT=4, LONG=5, FLOAT=6, DOUBLE=7, STRUCT=8, UNION=9, ENUM=10, MOE=11, BYTE=12, WORD=13, UINT=14, DWORD=15), Enum(ULInt8('storage_class'), END_OF_FUNCTION=255, NULL=0, AUTOMATIC=1, EXTERNAL=2, STATIC=3, REGISTER=4, EXTERNAL_DEF=5, LABEL=6, UNDEFINED_LABEL=7, MEMBER_OF_STRUCT=8, ARGUMENT=9, STRUCT_TAG=10, MEMBER_OF_UNION=11, UNION_TAG=12, TYPE_DEFINITION=13, UNDEFINED_STATIC=14, ENUM_TAG=15, MEMBER_OF_ENUM=16, REGISTER_PARAM=17, BIT_FIELD=18, BLOCK=100, FUNCTION=101, END_OF_STRUCT=102, FILE=103, SECTION=104, WEAK_EXTERNAL=105), ULInt8('number_of_aux_symbols'), Array(lambda ctx: ctx.number_of_aux_symbols, Bytes('aux_symbols', 18)))
coff_header = Struct('coff_header', Magic('PE\x00\x00'), Enum(ULInt16('machine_type'), UNKNOWN=0, AM33=467, AMD64=34404, ARM=448, EBC=3772, I386=332, IA64=512, M32R=36929, MIPS16=614, MIPSFPU=870, MIPSFPU16=1126, POWERPC=496, POWERPCFP=497, R4000=358, SH3=418, SH3DSP=419, SH4=422, SH5=424, THUMB=450, WCEMIPSV2=361, _default_=Pass), ULInt16('number_of_sections'), UTCTimeStamp('time_stamp'), ULInt32('symbol_table_pointer'), ULInt32('number_of_symbols'), ULInt16('optional_header_size'), FlagsEnum(ULInt16('characteristics'), RELOCS_STRIPPED=1, EXECUTABLE_IMAGE=2, LINE_NUMS_STRIPPED=4, LOCAL_SYMS_STRIPPED=8, AGGRESSIVE_WS_TRIM=16, LARGE_ADDRESS_AWARE=32, MACHINE_16BIT=64, BYTES_REVERSED_LO=128, MACHINE_32BIT=256, DEBUG_STRIPPED=512, REMOVABLE_RUN_FROM_SWAP=1024, SYSTEM=4096, DLL=8192, UNIPROCESSOR_ONLY=16384, BIG_ENDIAN_MACHINE=32768), Pointer(lambda ctx: ctx.symbol_table_pointer, Array(lambda ctx: ctx.number_of_symbols, symbol_table)))

def PEPlusField(name):
    return IfThenElse(name, lambda ctx: ctx.pe_type == 'PE32_plus', ULInt64(None), ULInt32(None))


optional_header = Struct('optional_header', Enum(ULInt16('pe_type'), PE32=267, PE32_plus=523), ULInt8('major_linker_version'), ULInt8('minor_linker_version'), ULInt32('code_size'), ULInt32('initialized_data_size'), ULInt32('uninitialized_data_size'), ULInt32('entry_point_pointer'), ULInt32('base_of_code'), If(lambda ctx: ctx.pe_type == 'PE32', ULInt32('base_of_data')), PEPlusField('image_base'), ULInt32('section_aligment'), ULInt32('file_alignment'), ULInt16('major_os_version'), ULInt16('minor_os_version'), ULInt16('major_image_version'), ULInt16('minor_image_version'), ULInt16('major_subsystem_version'), ULInt16('minor_subsystem_version'), Padding(4), ULInt32('image_size'), ULInt32('headers_size'), ULInt32('checksum'), Enum(ULInt16('subsystem'), UNKNOWN=0, NATIVE=1, WINDOWS_GUI=2, WINDOWS_CUI=3, POSIX_CIU=7, WINDOWS_CE_GUI=9, EFI_APPLICATION=10, EFI_BOOT_SERVICE_DRIVER=11, EFI_RUNTIME_DRIVER=12, EFI_ROM=13, XBOX=14, _defualt_=Pass), FlagsEnum(ULInt16('dll_characteristics'), NO_BIND=2048, WDM_DRIVER=8192, TERMINAL_SERVER_AWARE=32768), PEPlusField('reserved_stack_size'), PEPlusField('stack_commit_size'), PEPlusField('reserved_heap_size'), PEPlusField('heap_commit_size'), ULInt32('loader_flags'), ULInt32('number_of_data_directories'), NamedSequence(Array(lambda ctx: ctx.number_of_data_directories, Struct('data_directories', ULInt32('address'), ULInt32('size'))), mapping={0: 'export_table', 
   1: 'import_table', 
   2: 'resource_table', 
   3: 'exception_table', 
   4: 'certificate_table', 
   5: 'base_relocation_table', 
   6: 'debug', 
   7: 'architecture', 
   8: 'global_ptr', 
   9: 'tls_table', 
   10: 'load_config_table', 
   11: 'bound_import', 
   12: 'import_address_table', 
   13: 'delay_import_descriptor', 
   14: 'complus_runtime_header'}))
section = Struct('section', String('name', 8, padchar='\x00'), ULInt32('virtual_size'), ULInt32('virtual_address'), ULInt32('raw_data_size'), ULInt32('raw_data_pointer'), ULInt32('relocations_pointer'), ULInt32('line_numbers_pointer'), ULInt16('number_of_relocations'), ULInt16('number_of_line_numbers'), FlagsEnum(ULInt32('characteristics'), TYPE_REG=0, TYPE_DSECT=1, TYPE_NOLOAD=2, TYPE_GROUP=4, TYPE_NO_PAD=8, TYPE_COPY=16, CNT_CODE=32, CNT_INITIALIZED_DATA=64, CNT_UNINITIALIZED_DATA=128, LNK_OTHER=256, LNK_INFO=512, TYPE_OVER=1024, LNK_REMOVE=2048, LNK_COMDAT=4096, MEM_FARDATA=32768, MEM_PURGEABLE=131072, MEM_16BIT=131072, MEM_LOCKED=262144, MEM_PRELOAD=524288, ALIGN_1BYTES=1048576, ALIGN_2BYTES=2097152, ALIGN_4BYTES=3145728, ALIGN_8BYTES=4194304, ALIGN_16BYTES=5242880, ALIGN_32BYTES=6291456, ALIGN_64BYTES=7340032, ALIGN_128BYTES=8388608, ALIGN_256BYTES=9437184, ALIGN_512BYTES=10485760, ALIGN_1024BYTES=11534336, ALIGN_2048BYTES=12582912, ALIGN_4096BYTES=13631488, ALIGN_8192BYTES=14680064, LNK_NRELOC_OVFL=16777216, MEM_DISCARDABLE=33554432, MEM_NOT_CACHED=67108864, MEM_NOT_PAGED=134217728, MEM_SHARED=268435456, MEM_EXECUTE=536870912, MEM_READ=1073741824, MEM_WRITE=2147483648), OnDemandPointer(lambda ctx: ctx.raw_data_pointer, HexDumpAdapter(Field('raw_data', lambda ctx: ctx.raw_data_size))), OnDemandPointer(lambda ctx: ctx.line_numbers_pointer, Array(lambda ctx: ctx.number_of_line_numbers, Struct('line_numbers', ULInt32('type'), ULInt16('line_number')))), OnDemandPointer(lambda ctx: ctx.relocations_pointer, Array(lambda ctx: ctx.number_of_relocations, Struct('relocations', ULInt32('virtual_address'), ULInt32('symbol_table_index'), ULInt16('type')))))
pe32_file = Struct('pe32_file', msdos_header, coff_header, Anchor('_start_of_optional_header'), optional_header, Anchor('_end_of_optional_header'), Padding(lambda ctx: min(0, ctx.coff_header.optional_header_size - ctx._end_of_optional_header + ctx._start_of_optional_header)), Array(lambda ctx: ctx.coff_header.number_of_sections, section))
if __name__ == '__main__':
    print pe32_file.parse_stream(open('../../test/notepad.exe', 'rb'))
    print pe32_file.parse_stream(open('../../test/sqlite3.dll', 'rb'))