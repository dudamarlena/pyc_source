# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/vcf/__init__.py
# Compiled at: 2016-03-18 12:17:02
# Size of source mod 2**32: 384 bytes
"""
A VCFv4.0 and 4.1 parser for Python.

Online version of PyVCF documentation is available at http://pyvcf.rtfd.org/
"""
from vcf.parser import Reader, Writer
from vcf.parser import VCFReader, VCFWriter
from vcf.filters import Base as Filter
from vcf.parser import RESERVED_INFO, RESERVED_FORMAT
from vcf.sample_filter import SampleFilter
VERSION = '0.6.8'