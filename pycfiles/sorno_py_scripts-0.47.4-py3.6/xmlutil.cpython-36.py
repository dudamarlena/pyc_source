# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sorno/xmlutil.py
# Compiled at: 2019-08-09 12:21:44
# Size of source mod 2**32: 318 bytes
from __future__ import print_function
from xml.dom import minidom

def prettify(xml_str, indent=2):
    parsed = minidom.parseString(xml_str)
    return parsed.toprettyxml(indent=(' ' * indent))


if __name__ == '__main__':
    print(prettify('<fruits><fruit>apple</fruit><fruit>orange</fruit></fruits>'))