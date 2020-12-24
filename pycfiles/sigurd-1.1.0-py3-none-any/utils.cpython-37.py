# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\clems\pycharmprojects\comparison_sigurdr_siegfried\sigurd\nib_marburg\utils.py
# Compiled at: 2019-10-20 13:30:51
# Size of source mod 2**32: 770 bytes
"""

"""
import os
from lxml import etree
__author__ = [
 'Clément Besnier <clemsciences@aol.com>']

def extract_annotations(entry):
    return {child.tag:child.get('tag') for child in entry.getchildren()}


def extract_by_tag(tag, tokens):
    return [token[tag] for token in tokens if tag in token]


def get_root(filename, parser):
    tree = etree.parse(filename, parser=parser)
    return tree.getroot()


def get_data(data_directory, parser):
    for filename in os.listdir(data_directory):
        print(filename)
        if filename.endswith('xml'):
            tree = etree.parse((os.path.join(data_directory, filename)), parser=parser)
            yield tree.getroot()
        else:
            print('None')