# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/BioUtil/vcf.py
# Compiled at: 2016-09-06 23:21:57
# Size of source mod 2**32: 3924 bytes
"""
This module serves as a wrapper for vcf module [https://github.com/jamescasbon/PyVCF]
open() and vcfFile class is for directly init of vcf file object,
vcfReader and vcfWriter is wraper for vcf.Reader and vcf.Writer,
which accept file name as first argument (other than fsock), 
and also could accept vcf file without header (by additionally provide header infomation)

This file is under GPLv2 Lisense

Sein Tao <sein.tao@gmail.com>, 2015
"""
import vcf, csv, types, os, builtins
from .xz import xzopen
from itertools import chain
from copy import copy, deepcopy
from .decorator import context_decorator
__all__ = [
 'vcfFile', 'open', 'vcfWriter', 'vcfReader']
_vcf = vcf
_Reader = vcf.Reader
_Writer = vcf.Writer
Record = vcf.model._Record
Call = vcf.model._Call

class vcfFile(object):

    def __new__(cls, file, mode='r', template=None, prepend_chr=False):
        if mode == 'r':
            obj = vcf.Reader((xzopen(file, mode)), prepend_chr=prepend_chr, filename=file)
            obj.close = types.MethodType(lambda self: self._reader.close(), obj)
            return obj
        if mode == 'w':
            obj = vcf.Writer(xzopen(file, mode), template)
            obj.write = obj.write_record
            return obj
        raise ValueError('Unkonw mode: ' + mode)


def _read_header(self, header, template):
    if header:
        if template:
            raise ValueError('only one of header and template should specified')
    if header:
        header_fh = xzopen(header, 'r')
        template = vcf.Reader(header_fh)
        header_fh.close()
    return template


@context_decorator
class vcfReader(vcf.Reader):

    def __init__(self, file=None, header=None, fsock=None, template=None, **kwargs):
        if fsock:
            self._fsock = fsock
        else:
            if file:
                self._fsock = xzopen(file, 'r')
            template = _read_header(self, header, template)
            sup = super(self.__class__, self)
            if template:
                self._parse_metainfo = types.MethodType(lambda self: None, self)
                (sup.__init__)(self._fsock, filename=file, **kwargs)
                for attr in ('metadata', 'infos', 'filters', 'alts', 'contigs', 'formats',
                             '_column_headers', 'samples', '_sample_indexes'):
                    setattr(self, attr, deepcopy(getattr(template, attr)))

            else:
                (sup.__init__)(self._fsock, filename=file, **kwargs)

    def close(self):
        try:
            self._fsock.close()
        except AttributeError:
            pass


@context_decorator
class vcfWriter(vcf.Writer):

    def __init__(self, file=None, header=None, fsock=None, template=None, write_header=True, **kwargs):
        template = _read_header(self, header, template)
        if fsock:
            self._fsock = fsock
        else:
            if file:
                self._fsock = xzopen(file, 'w')
            sup = super(self.__class__, self)
            if write_header is False:
                null = builtins.open(os.devnull, 'w')
                (sup.__init__)(null, template, **kwargs)
                null.close()
                self.stream = self._fsock
                self.writer = csv.writer((self.stream), delimiter='\t', lineterminator=(kwargs.get('lineterminator', '\n')))
            else:
                (sup.__init__)((self._fsock), template, **kwargs)
        self.write = self.write_record


def open(file, mode='r', header=None, **kwargs):
    """wrapper for vcfReader and vcfWriter"""
    if 'r' in mode:
        return vcfReader(file, header=header, **kwargs)
    if 'w' in mode:
        return vcfWriter(file, header=header, **kwargs)
    raise ValueError('unknown mode: %s' % mode)