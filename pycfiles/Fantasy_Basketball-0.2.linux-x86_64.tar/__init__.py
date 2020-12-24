# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devin/software/my_projects/fantasy_basketball/test_env/lib/python2.7/site-packages/Fantasy_Basketball/__init__.py
# Compiled at: 2014-10-18 17:09:37
import os
from Download import download_data
from Process import get_player_stats
from Plot import Plotter
from Util import mkdir_p
default_dir = os.path.expanduser('~/.fantasy_basketball')
default_raw_data_dir = os.path.join(default_dir, 'raw_data')
default_processed_data_dir = os.path.join(default_dir, 'processed_data')
default_html_dir = os.path.join(default_dir, 'html')
default_plot_dir = os.path.join(default_dir, 'plot')