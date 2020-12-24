# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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