# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pdfkit/__init__.py
# Compiled at: 2017-01-09 10:40:34
"""
Wkhtmltopdf python wrapper to convert html to pdf using the webkit rendering engine and qt
"""
__author__ = 'Golovanov Stanislav'
__version__ = '0.6.1'
__license__ = 'MIT'
from .pdfkit import PDFKit
from .api import from_url, from_file, from_string, configuration