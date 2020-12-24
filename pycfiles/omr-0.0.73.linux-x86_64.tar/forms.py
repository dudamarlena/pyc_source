# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/omr/forms.py
# Compiled at: 2014-05-04 13:52:16
"""forms.py: import built in and user form specifications.

Forms are loaded (and overwritten) in the following order::
  
- Built in 882E form
- "forms.yaml" in the package directory if not executable 
- "*.yaml" in the current directory (if executable)

"""
import sys, yaml, glob
from collections import OrderedDict
from os.path import exists, dirname
from pkg_resources import resource_filename

def read_form(path):
    try:
        with open(path, 'r') as (f):
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print e


DEFAULT = '\n882E:\n    front:\n        size: [50, 5]\n        pos: [258, 130]\n        space: [25.2, 49.2]\n        bub: [15, 39]\n        info: [746, 1234, 408, 575]\n        score: [1350, 1395, 360, 405]\n        refzone: \n        - [233, 249, 51, 81]\n        - [106, 125, 571, 601]\n        - [1574, 1592, 570, 600]\n        - [1492, 1502, 50, 79]\n        expected_dpi: [150, 150]\n        expected_size: [1664, 664]\n        size_tolerance: [0.04, 0.04]\n        ref_rc: [175, 525]\n        contrast: 178\n        trim_std: 4\n        min_ref: 127\n        radius: 10\n        signal: 1.1\n\n    back:\n        size: [50, 5]\n        pos: [258, 130]\n        space: [25.2, 49.2]\n        bub: [15, 39]\n        info: [746, 1234, 408, 575]\n        score: [1350, 1395, 360, 405]\n        refzone: \n        - [233, 249, 51, 81]\n        - [106, 125, 571, 601]\n        - [1574, 1592, 570, 600]\n        - [1492, 1502, 50, 79]\n        expected_dpi: [150, 150]\n        expected_size: [1664, 664]\n        size_tolerance: [0.04, 0.04]\n        ref_rc: [175, 525]\n        contrast: 178\n        trim_std: 4\n        min_ref: 127\n        radius: 10\n        signal: 1.1\n        \n'
FORMS = OrderedDict(yaml.safe_load(DEFAULT))
FILES = [resource_filename(__name__, 'forms.yaml')]
if getattr(sys, 'frozen', False):
    FILES += map(str, glob.glob(dirname(sys.executable), '*.yaml'))
map(FORMS.update, filter(None, map(read_form, filter(exists, FILES))))