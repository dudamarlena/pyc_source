# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shliyana/anaconda3/lib/python3.7/site-packages/htrc/metadata/marc.py
# Compiled at: 2019-05-06 10:39:58
# Size of source mod 2**32: 1313 bytes
"""
MARC CODE HANDLING
"""
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
import xml.etree.ElementTree as ET

def parse_marc(raw):
    raw = raw.replace(' xmlns', ' xmlnamespace')
    ET.register_namespace('', 'http://www.loc.gov/MARC21/slim')
    return ET.fromstring(raw)


def get_marc_value(xml, tag, code):
    xpath = "{marc}datafield[@tag='{tag}']/{marc}subfield[@code='{code}']".format(tag=tag,
      code=code,
      marc='')
    results = xml.findall(xpath)
    if results:
        return results[0].text


def get_lccn_from_marc(xml):
    return get_marc_value(xml, '010', 'a')


def get_title_from_marc(xml):
    return get_marc_value(xml, '245', 'a')


def get_volume_from_marc(xml):
    return get_marc_value(xml, '974', 'c')


def get_lcc_from_marc(xml):
    lcc = list()
    val = get_marc_value(xml, '050', 'a')
    if val:
        lcc.append(val)
    val = get_marc_value(xml, '050', 'b')
    if val:
        lcc[(-1)] += val
    val = get_marc_value(xml, '991', 'h')
    if val:
        lcc.append(val)
    val = get_marc_value(xml, '991', 'i')
    if val:
        lcc[(-1)] += val
    return ';'.join(lcc)