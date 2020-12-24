# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nori/submodule.py
# Compiled at: 2013-10-29 11:30:32
"""
This is the SUBMODULE submodule for the nori library; see __main__.py
for license and usage information.

DOCSTRING CONTENTS:
-------------------

    1) About and Requirements
    2) API Variables
    3) API Functions
    4) API Classes
    5) Usage in Scripts
    6) Modification Notes

1) ABOUT AND REQUIREMENTS:
--------------------------

2) API VARIABLES:
-----------------

3) API FUNCTIONS:
-----------------

4) API CLASSES:
---------------

5) USAGE IN SCRIPTS:
--------------------

6) MODIFICATION NOTES:
----------------------

"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from pprint import pprint as pp
import sys
try:
    import paramiko
except ImportError:
    pass

from . import core
core.pyversion_check(7, 2)
core.exitvals['submodule'] = dict(num=999, descr='\nerror doing submodule stuff\n')
core.supported_features['submodule'] = 'submodule stuff'
if 'paramiko' in sys.modules:
    core.available_features.append('submodule')
if 'submodule' in core.available_features:
    core.config_settings['submodule_heading'] = dict(heading='Submodule')
    core.config_settings['submodule_setting'] = dict(descr='\nSubmodule stuff.\n', default='submodule stuff', requires=[
     'submodule'])

def validate_config():
    """
    Validate submodule-specific config settings.
    """
    pass


def main():
    core.process_command_line()


if __name__ == '__main__':
    main()