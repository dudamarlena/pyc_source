# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/libkeyutils.py
# Compiled at: 2019-05-16 13:41:33
r"""
Parsers for detection of Linux/Ebury 1.6 malware indicators
===========================================================

Libkeyutils - command ``find -L /lib /lib64 -name 'libkeyutils.so*'``
---------------------------------------------------------------------

Parses output of command ``find -L /lib /lib64 -name 'libkeyutils.so*'`` to find all potentially
affected libraries.

LibkeyutilsObjdumps - command ``find -L /lib /lib64 -name libkeyutils.so.1 -exec objdump -x "{}" \;``
-----------------------------------------------------------------------------------------------------

Parses output of command ``find -L /lib /lib64 -name libkeyutils.so.1 -exec objdump -x "{}" \;`` to
verify linked libraries.

https://www.welivesecurity.com/2017/10/30/windigo-ebury-update-2/
"""
import re
from .. import parser, CommandParser
from ..specs import Specs

@parser(Specs.libkeyutils)
class Libkeyutils(CommandParser):
    """
    This parser finds all 'libkeyutils.so*' libraries in either /lib or /lib64 directory and its
    sub-directories.

    Output of Command::

        /lib/libkeyutils.so.1
        /lib/tls/libkeyutils.so.1.6
        /lib64/libkeyutils.so

    Example::

        >>> shared[Libkeyutils].libraries
        ['/lib/libkeyutils.so.1', '/lib/tls/libkeyutils.so.1.6', '/lib64/libkeyutils.so']
    """

    def __init__(self, *args, **kwargs):
        self.libraries = []
        super(Libkeyutils, self).__init__(*args, **kwargs)

    def parse_content(self, content):
        self.libraries = list(content)


@parser(Specs.libkeyutils_objdumps)
class LibkeyutilsObjdumps(CommandParser):
    """
    This parser goes through objdumps of all 'libkeyutils.so.1' libraries in either /lib or /lib64
    directory, and its sub-directories, to finds linked libraries.

    Output of Command::

        /lib/libkeyutils.so.1:     file format elf32-i386
        /lib/libkeyutils.so.1
        architecture: i386, flags 0x00000150:
        HAS_SYMS, DYNAMIC, D_PAGED
        start address 0x00000f80
        ...

        Dynamic Section:
          NEEDED               libdl.so.2
          NEEDED               libc.so.6
          NEEDED               libsbr.so
          SONAME               libkeyutils.so.1
          INIT                 0x00000e54
        ...

        /lib64/libkeyutils.so.1:     file format elf64-x86-64
        /lib64/libkeyutils.so.1
        architecture: i386:x86-64, flags 0x00000150:
        HAS_SYMS, DYNAMIC, D_PAGED
        start address 0x00000000000014b0
        ...

        Dynamic Section:
          NEEDED               libdl.so.2
          NEEDED               libsbr.so.6
          NEEDED               libfake.so
          SONAME               libkeyutils.so.1
          INIT                 0x0000000000001390
        ...

    Example::

        >>> shared[LibkeyutilsObjdumps].linked_libraries
        {'/lib/libkeyutils.so.1': ['libdl.so.2', 'libc.so.6', 'libsbr.so'],
         '/lib64/libkeyutils.so.1': ['libdl.so.2', 'libsbr.so.6', 'libfake.so']}
    """
    FILE_PATTERN = re.compile('(.*libkeyutils.so.1):\\s*file format')
    NEED_PATTERN = re.compile('NEEDED\\s+(.*)\\s*$')

    def __init__(self, *args, **kwargs):
        self.linked_libraries = {}
        super(LibkeyutilsObjdumps, self).__init__(*args, **kwargs)

    def parse_content(self, content):
        file_name = None
        for line in content:
            r = LibkeyutilsObjdumps.FILE_PATTERN.search(line)
            if r:
                file_name = r.group(1)
            r = LibkeyutilsObjdumps.NEED_PATTERN.search(line)
            if r and file_name:
                library = r.group(1)
                if file_name not in self.linked_libraries:
                    self.linked_libraries[file_name] = [
                     library]
                else:
                    self.linked_libraries[file_name].append(library)

        return