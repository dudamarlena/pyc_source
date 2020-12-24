# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sravan953/Documents/CU/Projects/virtual-scanner/virtualscanner/coms/coms_ui/utest_coms_ui.py
# Compiled at: 2019-06-24 16:04:04
# Size of source mod 2**32: 675 bytes
"""
This script unit starts and tests the communications between server and client(s)
Parameters
----------
    void
    Requires coms_server_flask to be running before the unit test is run (i.e.: run coms_server_flask.py first)

Returns
-------
    payload

Performs
--------
    tests multiple cases of the server client interactions via the html pages rendered

Author: Sairam Geethanath
Date: 03/11/2019
Version 0.0
Copyright of the Board of Trustees of  Columbia University in the City of New York
"""
import webbrowser
webbrowser.open('http://0.0.0.0:5000/')