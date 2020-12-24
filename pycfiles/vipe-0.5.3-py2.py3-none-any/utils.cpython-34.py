# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/oozie/reader/utils.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 1588 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import re
pattern_whitespace = re.compile('\\s+')

def properties_to_dict(elem):
    """Take XML element containing properties and turn it into dictionary"""
    d = {}
    for child in elem:
        assert child.tag == 'property'
        name = get_text(child.find('name'))
        value = None
        value_elem = child.find('value')
        if value_elem is not None:
            value = value_elem.text.strip()
        d[name] = value

    return d


def get_text(elem):
    """Get the text content of the element and clean it up.

    Returns:
        string
    """
    stripped = elem.text.strip()
    return re.sub(pattern_whitespace, ' ', stripped)


def findall_to_text(elem, child_tag_name):
    """
    Returns:
        List[string]
    """
    return [get_text(e) for e in elem.findall(child_tag_name)]


def find_to_text(elem, child_tag_name):
    """
    Returns:
        string
    """
    return get_text(elem.find(child_tag_name))