# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bin\ddp_spec.py
# Compiled at: 2015-04-10 09:22:09
import os, sys
from shutil import copy
from ddp import *
project_path = inc.get_project_path()
x = spec.SPEC()
if len(sys.argv) == 2:
    try:
        x.legend_loc = int(sys.argv[1])
    except TypeError:
        print 'lengend location should be a number in range 1..4.'

x.save_spec()
if os.path.exists('/var/www/html/images'):
    spec_path = os.path.join(project_path, 'spectrum.png')
    copy(spec_path, '/var/www/html/images')