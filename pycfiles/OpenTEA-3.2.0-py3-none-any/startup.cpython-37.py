# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/src/opentea/examples/calculator/startup.py
# Compiled at: 2020-01-31 05:30:01
# Size of source mod 2**32: 672 bytes
"""Startup script to call calculator gui."""
import os, inspect, yaml
from opentea.gui_forms.otinker import main_otinker

def main(schema_file=None):
    """Call the otinker gui."""
    if schema_file == None:
        schema_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema_calculator.yaml')
    with open(schema_file, 'r') as (fin):
        schema = yaml.load(fin, Loader=(yaml.FullLoader))
    base_dir = inspect.getfile(inspect.currentframe())
    base_dir = os.path.dirname(os.path.abspath(base_dir))
    main_otinker(schema, calling_dir=base_dir, tab_3d=True)


if __name__ == '__main__':
    main()