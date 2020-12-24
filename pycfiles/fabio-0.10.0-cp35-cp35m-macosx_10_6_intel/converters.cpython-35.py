# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/converters.py
# Compiled at: 2017-11-15 03:51:36
# Size of source mod 2**32: 3205 bytes
"""Converter module.

This is for the moment empty (populated only with almost pass through anonymous functions)
but aims to be populated with more sofisticated translators...

"""
from __future__ import with_statement, print_function
__author__ = 'Jérôme Kieffer'
__contact__ = 'jerome.kieffer@esrf.eu'
__license__ = 'MIT'
__copyright__ = 'European Synchrotron Radiation Facility, Grenoble, France'
import logging
logger = logging.getLogger(__name__)

def convert_data_integer(data):
    """
    convert data to integer
    """
    if data is not None:
        return data.astype(int)
    else:
        return data


CONVERSION_HEADER = {('edfimage', 'edfimage'): lambda header: header}
CONVERSION_DATA = {('edfimage', 'edfimage'): lambda data: data, 
 ('edfimage', 'cbfimage'): convert_data_integer, 
 ('edfimage', 'mar345image'): convert_data_integer, 
 ('edfimage', 'fit2dmaskimage'): convert_data_integer, 
 ('edfimage', 'kcdimage'): convert_data_integer, 
 ('edfimage', 'OXDimage'): convert_data_integer, 
 ('edfimage', 'pnmimage'): convert_data_integer}

def convert_data(inp, outp, data):
    """
    Return data converted to the output format ... over-simplistic
    implementation for the moment...

    :param str inp: input format (like "cbfimage")
    :param str outp: output format (like "cbfimage")
    :param numpy.ndarray data: the actual dataset to be transformed
    """
    return CONVERSION_DATA.get((inp, outp), lambda data: data)(data)


def convert_header(inp, outp, header):
    """
    Return header converted to the output format

    :param str inp: input format (like "cbfimage")
    :param str outp: output format (like "cbfimage")
    :param dict header: the actual set of headers to be transformed
    """
    return CONVERSION_HEADER.get((inp, outp), lambda header: header)(header)