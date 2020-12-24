# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/connor/Bioinformatics/samsum/samsum/testing_utils.py
# Compiled at: 2019-12-03 18:06:13
# Size of source mod 2**32: 566 bytes
"""Modified from sourmash's sourmash/tests/sourmash_tst_utils.py"""
import os, sys
from pkg_resources import Requirement, resource_filename, ResolutionError
import traceback

def get_test_data(filename):
    filepath = None
    try:
        filepath = resource_filename(Requirement.parse('samsum'), 'tests/test-data/' + filename)
    except ResolutionError:
        pass

    if not filepath or not os.path.isfile(filepath):
        filepath = os.path.join(os.path.dirname(__file__), 'test-data', filename)
    return filepath