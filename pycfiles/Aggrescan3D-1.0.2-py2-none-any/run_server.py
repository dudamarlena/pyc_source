# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/olek/Wszystkie_aggrescamy_swiata/aggrescan3d/a3d_gui/run_server.py
# Compiled at: 2018-08-29 04:56:53
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)))

def run_server():
    try:
        from a3d_gui import app
        app.run(host='0.0.0.0', debug=True)
    except ImportError:
        pass