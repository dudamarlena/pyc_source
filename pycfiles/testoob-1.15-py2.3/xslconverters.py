# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/xslconverters.py
# Compiled at: 2009-10-07 18:08:46
"""XSL converters for XML output"""

def _read_file(filename):
    from os.path import join, dirname
    f = open(join(dirname(__file__), filename))
    try:
        return f.read()
    finally:
        f.close()


import html_xsl
BASIC_CONVERTER = html_xsl.XSL