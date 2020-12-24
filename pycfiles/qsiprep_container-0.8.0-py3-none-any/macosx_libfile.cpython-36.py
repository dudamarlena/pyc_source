# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/wheel/wheel/macosx_libfile.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 11858 bytes
"""
This module contains function to analyse dynamic library
headers to extract system information

Currently only for MacOSX

Library file on macosx system starts with Mach-O or Fat field.
This can be distinguish by first 32 bites and it is called magic number.
Proper value of magic number is with suffix _MAGIC. Suffix _CIGAM means
reversed bytes order.
Both fields can occur in two types: 32 and 64 bytes.

FAT field inform that this library contains few version of library
(typically for different types version). It contains
information where Mach-O headers starts.

Each section started with Mach-O header contains one library
(So if file starts with this field it contains only one version).

After filed Mach-O there are section fields.
Each of them starts with two fields:
cmd - magic number for this command
cmdsize - total size occupied by this section information.

In this case only sections LC_VERSION_MIN_MACOSX (for macosx 10.13 and earlier)
and LC_BUILD_VERSION (for macosx 10.14 and newer) are interesting,
because them contains information about minimal system version.

Important remarks:
- For fat files this implementation looks for maximum number version.
  It not check if it is 32 or 64 and do not compare it with currently builded package.
  So it is possible to false report higher version that needed.
- All structures signatures are taken form macosx header files.
- I think that binary format will be more stable than `otool` output.
  and if apple introduce some changes both implementation will need to be updated.
"""
import ctypes, sys
FAT_MAGIC = 3405691582
FAT_CIGAM = 3199925962
FAT_MAGIC_64 = 3405691583
FAT_CIGAM_64 = 3216703178
MH_MAGIC = 4277009102
MH_CIGAM = 3472551422
MH_MAGIC_64 = 4277009103
MH_CIGAM_64 = 3489328638
LC_VERSION_MIN_MACOSX = 36
LC_BUILD_VERSION = 50
mach_header_fields = [
 (
  'magic', ctypes.c_uint32), ('cputype', ctypes.c_int),
 (
  'cpusubtype', ctypes.c_int), ('filetype', ctypes.c_uint32),
 (
  'ncmds', ctypes.c_uint32), ('sizeofcmds', ctypes.c_uint32),
 (
  'flags', ctypes.c_uint32)]
mach_header_fields_64 = mach_header_fields + [('reserved', ctypes.c_uint32)]
fat_header_fields = [
 (
  'magic', ctypes.c_uint32), ('nfat_arch', ctypes.c_uint32)]
fat_arch_fields = [
 (
  'cputype', ctypes.c_int), ('cpusubtype', ctypes.c_int),
 (
  'offset', ctypes.c_uint32), ('size', ctypes.c_uint32),
 (
  'align', ctypes.c_uint32)]
fat_arch_64_fields = [
 (
  'cputype', ctypes.c_int), ('cpusubtype', ctypes.c_int),
 (
  'offset', ctypes.c_uint64), ('size', ctypes.c_uint64),
 (
  'align', ctypes.c_uint32), ('reserved', ctypes.c_uint32)]
segment_base_fields = [
 (
  'cmd', ctypes.c_uint32), ('cmdsize', ctypes.c_uint32)]
segment_command_fields = [
 (
  'cmd', ctypes.c_uint32), ('cmdsize', ctypes.c_uint32),
 (
  'segname', ctypes.c_char * 16), ('vmaddr', ctypes.c_uint32),
 (
  'vmsize', ctypes.c_uint32), ('fileoff', ctypes.c_uint32),
 (
  'filesize', ctypes.c_uint32), ('maxprot', ctypes.c_int),
 (
  'initprot', ctypes.c_int), ('nsects', ctypes.c_uint32),
 (
  'flags', ctypes.c_uint32)]
segment_command_fields_64 = [
 (
  'cmd', ctypes.c_uint32), ('cmdsize', ctypes.c_uint32),
 (
  'segname', ctypes.c_char * 16), ('vmaddr', ctypes.c_uint64),
 (
  'vmsize', ctypes.c_uint64), ('fileoff', ctypes.c_uint64),
 (
  'filesize', ctypes.c_uint64), ('maxprot', ctypes.c_int),
 (
  'initprot', ctypes.c_int), ('nsects', ctypes.c_uint32),
 (
  'flags', ctypes.c_uint32)]
version_min_command_fields = segment_base_fields + [
 (
  'version', ctypes.c_uint32), ('sdk', ctypes.c_uint32)]
build_version_command_fields = segment_base_fields + [
 (
  'platform', ctypes.c_uint32), ('minos', ctypes.c_uint32),
 (
  'sdk', ctypes.c_uint32), ('ntools', ctypes.c_uint32)]

def swap32(x):
    return x << 24 & 4278190080 | x << 8 & 16711680 | x >> 8 & 65280 | x >> 24 & 255


def get_base_class_and_magic_number(lib_file, seek=None):
    if seek is None:
        seek = lib_file.tell()
    else:
        lib_file.seek(seek)
    magic_number = ctypes.c_uint32.from_buffer_copy(lib_file.read(ctypes.sizeof(ctypes.c_uint32))).value
    if magic_number in [FAT_CIGAM, FAT_CIGAM_64, MH_CIGAM, MH_CIGAM_64]:
        if sys.byteorder == 'little':
            BaseClass = ctypes.BigEndianStructure
        else:
            BaseClass = ctypes.LittleEndianStructure
        magic_number = swap32(magic_number)
    else:
        BaseClass = ctypes.Structure
    lib_file.seek(seek)
    return (BaseClass, magic_number)


def read_data(struct_class, lib_file):
    return struct_class.from_buffer_copy(lib_file.read(ctypes.sizeof(struct_class)))


def extract_macosx_min_system_version(path_to_lib):
    with open(path_to_lib, 'rb') as (lib_file):
        BaseClass, magic_number = get_base_class_and_magic_number(lib_file, 0)
        if magic_number not in [FAT_MAGIC, FAT_MAGIC_64, MH_MAGIC, MH_MAGIC_64]:
            return
        if magic_number in [FAT_MAGIC, FAT_CIGAM_64]:

            class FatHeader(BaseClass):
                _fields_ = fat_header_fields

            fat_header = read_data(FatHeader, lib_file)
            if magic_number == FAT_MAGIC:

                class FatArch(BaseClass):
                    _fields_ = fat_arch_fields

            else:

                class FatArch(BaseClass):
                    _fields_ = fat_arch_64_fields

            fat_arch_list = [read_data(FatArch, lib_file) for _ in range(fat_header.nfat_arch)]
            versions_list = []
            for el in fat_arch_list:
                try:
                    version = read_mach_header(lib_file, el.offset)
                    if version is not None:
                        versions_list.append(version)
                except ValueError:
                    pass

            if len(versions_list) > 0:
                return max(versions_list)
            else:
                return
        else:
            try:
                return read_mach_header(lib_file, 0)
            except ValueError:
                return


def read_mach_header(lib_file, seek=None):
    """
    This funcition parse mach-O header and extract
    information about minimal system version

    :param lib_file: reference to opened library file with pointer
    """
    if seek is not None:
        lib_file.seek(seek)
    else:
        base_class, magic_number = get_base_class_and_magic_number(lib_file)
        arch = '32' if magic_number == MH_MAGIC else '64'

        class SegmentBase(base_class):
            _fields_ = segment_base_fields

        if arch == '32':

            class MachHeader(base_class):
                _fields_ = mach_header_fields

        else:

            class MachHeader(base_class):
                _fields_ = mach_header_fields_64

    mach_header = read_data(MachHeader, lib_file)
    for _i in range(mach_header.ncmds):
        pos = lib_file.tell()
        segment_base = read_data(SegmentBase, lib_file)
        lib_file.seek(pos)
        if segment_base.cmd == LC_VERSION_MIN_MACOSX:

            class VersionMinCommand(base_class):
                _fields_ = version_min_command_fields

            version_info = read_data(VersionMinCommand, lib_file)
            return parse_version(version_info.version)
        if segment_base.cmd == LC_BUILD_VERSION:

            class VersionBuild(base_class):
                _fields_ = build_version_command_fields

            version_info = read_data(VersionBuild, lib_file)
            return parse_version(version_info.minos)
        lib_file.seek(pos + segment_base.cmdsize)
        continue


def parse_version(version):
    x = (version & 4294901760) >> 16
    y = (version & 65280) >> 8
    z = version & 255
    return (x, y, z)