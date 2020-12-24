# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/__init__.py
# Compiled at: 2016-03-11 21:01:27
"""
:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Foods Canada
:group: Microbial Biodiversity Bioinformatics
:contact: mbb@agr.gc.ca 
:license: LGPL v3
"""
import os
TESTDATA = {'specimen': os.path.join(os.path.dirname(__file__), '../test-data/specimen_data.xml'), 
   'sequence': os.path.join(os.path.dirname(__file__), '../test-data/sequence_data.fa'), 
   'tracefiles_tar': os.path.join(os.path.dirname(__file__), '../test-data/trace_files.tar')}