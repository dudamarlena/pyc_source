# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\reascripts\activate_reapy_server.py
# Compiled at: 2020-03-21 05:22:27
# Size of source mod 2**32: 984 bytes
"""
Activate ``reapy`` server.

Running this ReaScript from inside REAPER sets the ``reapy`` server
that receives and executes API calls requests from outside. It will
automatically be run when importing ``reapy`` from outside, if it is
enabled.
"""
import reapy, os, site
from reapy.tools.network import Server

def run_main_loop():
    SERVER.accept()
    requests = SERVER.get_requests()
    results = SERVER.process_requests(requests)
    SERVER.send_results(results)
    reapy.defer(run_main_loop)


def get_new_reapy_server():
    server_port = reapy.config.REAPY_SERVER_PORT
    reapy.set_ext_state('reapy', 'server_port', server_port)
    server = Server(server_port)
    return server


if __name__ == '__main__':
    SERVER = get_new_reapy_server()
    run_main_loop()
    reapy.at_exit(reapy.delete_ext_state, 'reapy', 'server_port')