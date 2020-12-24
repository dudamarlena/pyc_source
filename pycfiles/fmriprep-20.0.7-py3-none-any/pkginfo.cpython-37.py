# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/wheel/wheel/pkginfo.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 1257 bytes
"""Tools for reading and writing PKG-INFO / METADATA without caring
about the encoding."""
from email.parser import Parser
try:
    unicode
    _PY3 = False
except NameError:
    _PY3 = True

if not _PY3:
    from email.generator import Generator

    def read_pkg_info_bytes(bytestr):
        return Parser().parsestr(bytestr)


    def read_pkg_info(path):
        with open(path, 'r') as (headers):
            message = Parser().parse(headers)
        return message


    def write_pkg_info(path, message):
        with open(path, 'w') as (metadata):
            Generator(metadata, mangle_from_=False, maxheaderlen=0).flatten(message)


else:
    from email.generator import BytesGenerator

    def read_pkg_info_bytes(bytestr):
        headers = bytestr.decode(encoding='ascii', errors='surrogateescape')
        message = Parser().parsestr(headers)
        return message


    def read_pkg_info(path):
        with open(path, 'r', encoding='ascii',
          errors='surrogateescape') as (headers):
            message = Parser().parse(headers)
        return message


    def write_pkg_info(path, message):
        with open(path, 'wb') as (out):
            BytesGenerator(out, mangle_from_=False, maxheaderlen=0).flatten(message)