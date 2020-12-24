# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edloper/newdata/projects/epydoc/src/scripts/epydoc.py
# Compiled at: 2007-09-21 18:50:43
import sys, os.path
script_path = os.path.abspath(sys.path[0])
sys.path = [ p for p in sys.path if os.path.abspath(p) != script_path ]
from epydoc.cli import cli
cli()