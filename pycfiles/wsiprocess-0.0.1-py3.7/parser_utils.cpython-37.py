# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/wsiprocess/annotationparser/parser_utils.py
# Compiled at: 2019-12-13 21:43:43
# Size of source mod 2**32: 226 bytes
from lxml import etree

def detect_type(path):
    try:
        tree = etree.parse(path)
        root = tree.getroot()
        if root.tag == 'ASAP_Annotations':
            return 'ASAP'
    except:
        return 'Unknown'